#!/usr/bin/env python3
"""
vss_parser_engine.py — VSS-1 Causal Scene Graph Parser.

AAA owns the schema and the relation→verifier contract.
LLM substrates are pluggable. Both gates fail closed.

F2  every entity/assertion must be prompt-groundable
F7  near stays near; no invented geometry
F9  schema is AAA-owned; model is substrate
F11 receipt per parse
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple

import jsonschema

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

_HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_CANDIDATES = (
    os.path.join(_HERE, "vss_assertion_ledger.schema.json"),
    os.path.join(_HERE, "schema", "vss_assertion_ledger.schema.json"),
)

# AAA-owned. LLM cannot choose these freely.
# HARD_COUNT + count_v1 is an orthogonal overlay when the prompt states an integer count.
RELATION_CONTRACT = {
    "inside": {"verifiers": {"containment_v1"}, "classes": {"HARD_GEOMETRIC"}},
    "on": {"verifiers": {"containment_v1", "count_v1"}, "classes": {"HARD_GEOMETRIC", "HARD_COUNT"}},
    "supported_by": {"verifiers": {"containment_v1"}, "classes": {"HARD_GEOMETRIC"}},
    "beside": {"verifiers": {"perspective_v1"}, "classes": {"SOFT_STYLE"}},
    "behind": {"verifiers": {"perspective_v1"}, "classes": {"SOFT_STYLE"}},
    "in_front_of": {"verifiers": {"perspective_v1"}, "classes": {"SOFT_STYLE"}},
    "near": {"verifiers": {"none"}, "classes": {"SOFT_STYLE"}, "min_tolerance": 0.3},
    "illuminates": {"verifiers": {"shadow_v1"}, "classes": {"OPTICAL_LIGHTING"}},
    "casts_shadow_towards": {"verifiers": {"shadow_v1"}, "classes": {"OPTICAL_LIGHTING"}},
    "reflects": {"verifiers": {"none"}, "classes": {"SOFT_STYLE"}},
    "occludes": {"verifiers": {"none"}, "classes": {"SOFT_STYLE"}},
}

SYSTEM_PROMPT = """You are the VSS-1 Causal Scene Graph Parser for arifOS / AAA.
Your sole duty is to compile a raw text prompt into a strict, machine-readable Assertion Ledger JSON matching the schema.

STRICT CONSTITUTIONAL RULES:
1. F7 HUMILITY (Anti-Overclaim): NEVER invent spatial relations, precise positions, or implicit entities not explicitly stated or strictly required.
   - If prompt says "a person near a car", relation MUST be "near". Do NOT use "inside" or "supported_by".
2. UNCERTAINTY HANDLING: If spatial placement, posture, or count is underspecified, record it under `uncertainties`.
3. UNSUPPORTED CLAIMS: Abstract/non-visual terms (e.g. "feeling melancholic", "smelling like rain") MUST be routed to `unsupported_claims`.
4. VERIFIER MAPPING CONTRACT:
   - "inside" / "on" / "supported_by" -> verifier: "containment_v1", class: "HARD_GEOMETRIC", failure_action: "LOCAL_REPAIR"
   - explicit integer counts -> verifier: "count_v1", class: "HARD_COUNT", failure_action: "LOCAL_REPAIR"
   - "beside" / "behind" / "in_front_of" -> verifier: "perspective_v1", class: "SOFT_STYLE"
   - "near" -> verifier: "none", class: "SOFT_STYLE", tolerance >= 0.3
   - "illuminates" / "casts_shadow_towards" -> verifier: "shadow_v1", class: "OPTICAL_LIGHTING"
   - "reflects" / "occludes" -> verifier: "none", class: "SOFT_STYLE"
5. OUTPUT FORMAT: Output ONLY valid JSON matching the schema. Zero conversational prose, zero markdown wrappers.
"""


def _resolve_schema_path(explicit: Optional[str] = None) -> str:
    if explicit:
        if not os.path.exists(explicit):
            raise FileNotFoundError(f"Schema file missing at: {explicit}")
        return explicit
    for path in SCHEMA_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"Schema file missing. Tried: {SCHEMA_CANDIDATES}")


def _strip_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(line for line in lines if not line.strip().startswith("```")).strip()
    return cleaned


class VSSParserEngine:
    def __init__(self, schema_path: Optional[str] = None):
        resolved = _resolve_schema_path(schema_path)
        with open(resolved, "r", encoding="utf-8") as handle:
            self.schema = json.load(handle)
        self.schema_path = resolved

    def validate_ledger(self, ledger_data: Dict[str, Any]) -> Tuple[bool, str]:
        """JSON Schema gate. Fail-closed."""
        try:
            jsonschema.validate(instance=ledger_data, schema=self.schema)
            return True, "VALID_SCHEMA"
        except jsonschema.exceptions.ValidationError as err:
            path_str = "/".join(str(p) for p in err.path) if err.path else "root"
            return False, f"SCHEMA_VIOLATION [{path_str}]: {err.message}"
        except Exception as exc:
            return False, f"UNEXPECTED_VALIDATION_ERROR: {exc}"

    def validate_contract(self, ledger_data: Dict[str, Any]) -> Tuple[bool, str]:
        """AAA relation→verifier mapping. Fail-closed even if schema-valid."""
        entity_ids = {e.get("id") for e in ledger_data.get("entities", []) if isinstance(e, dict)}
        seen_assert_ids: set[str] = set()

        for assertion in ledger_data.get("assertions", []):
            if not isinstance(assertion, dict):
                return False, "CONTRACT_VIOLATION: assertion is not an object"
            aid = assertion.get("id")
            if aid in seen_assert_ids:
                return False, f"CONTRACT_VIOLATION: duplicate assertion id {aid}"
            seen_assert_ids.add(aid)

            relation = assertion.get("relation")
            spec = RELATION_CONTRACT.get(relation)
            if spec is None:
                return False, f"CONTRACT_VIOLATION: unknown relation {relation!r}"

            verifier = assertion.get("verifier")
            klass = assertion.get("class")
            if verifier not in spec["verifiers"]:
                return False, (
                    f"CONTRACT_VIOLATION [{aid}]: relation={relation} "
                    f"forbids verifier={verifier}; allowed={sorted(spec['verifiers'])}"
                )
            if klass not in spec["classes"]:
                return False, (
                    f"CONTRACT_VIOLATION [{aid}]: relation={relation} "
                    f"forbids class={klass}; allowed={sorted(spec['classes'])}"
                )

            min_tol = spec.get("min_tolerance")
            if min_tol is not None and float(assertion.get("tolerance", 0)) < min_tol:
                return False, (
                    f"CONTRACT_VIOLATION [{aid}]: relation={relation} "
                    f"requires tolerance>={min_tol}"
                )

            subject = assertion.get("subject")
            target = assertion.get("target")
            if subject not in entity_ids:
                return False, f"CONTRACT_VIOLATION [{aid}]: subject {subject!r} not in entities"
            if target not in entity_ids:
                return False, f"CONTRACT_VIOLATION [{aid}]: target {target!r} not in entities"

        return True, "VALID_CONTRACT"

    def validate(self, ledger_data: Dict[str, Any]) -> Tuple[bool, str]:
        ok, msg = self.validate_ledger(ledger_data)
        if not ok:
            return ok, msg
        return self.validate_contract(ledger_data)

    def parse(self, raw_prompt: str, llm_runner_fn: Callable[..., str]) -> Dict[str, Any]:
        """Substrate propose → schema + contract gates. Fail-closed."""
        if not raw_prompt or not str(raw_prompt).strip():
            return {"status": "FAIL_CLOSED", "error_code": "E_EMPTY_PROMPT"}

        scene_id = f"scene_{uuid.uuid4().hex[:8]}"
        user_input = f"SCENE_ID: {scene_id}\nRAW_PROMPT: {raw_prompt}"
        raw_response = ""

        try:
            raw_response = llm_runner_fn(system_prompt=SYSTEM_PROMPT, user_prompt=user_input)
            parsed_json = json.loads(_strip_fences(raw_response))
        except json.JSONDecodeError as exc:
            logging.error("LLM produced non-JSON payload: %s", exc)
            return {
                "status": "FAIL_CLOSED",
                "error_code": "E_NON_JSON_OUTPUT",
                "raw_response": raw_response,
            }
        except Exception as exc:
            logging.error("Substrate execution failure: %s", exc)
            return {
                "status": "FAIL_CLOSED",
                "error_code": "E_SUBSTRATE_FAILURE",
                "error_detail": str(exc),
            }

        if not isinstance(parsed_json, dict):
            return {
                "status": "FAIL_CLOSED",
                "error_code": "E_NON_OBJECT_OUTPUT",
                "raw_response": raw_response[:1000],
            }

        if not parsed_json.get("scene_id"):
            parsed_json["scene_id"] = scene_id
        if not parsed_json.get("raw_prompt"):
            parsed_json["raw_prompt"] = raw_prompt

        is_valid, msg = self.validate(parsed_json)
        if not is_valid:
            logging.warning("Ledger rejected by AAA gate: %s", msg)
            code = "E_CONTRACT_INVALID" if msg.startswith("CONTRACT") else "E_SCHEMA_INVALID"
            return {
                "status": "FAIL_CLOSED",
                "error_code": code,
                "validation_message": msg,
                "parsed_payload": parsed_json,
            }

        return {"status": "SUCCESS", "ledger": parsed_json}

    def parse_prompt(self, prompt: str, llm_client: Any, scene_id: Optional[str] = None) -> Dict[str, Any]:
        """Compatibility wrapper for clients exposing .generate(system, prompt, temperature)."""

        def _runner(system_prompt: str, user_prompt: str) -> str:
            return llm_client.generate(system=system_prompt, prompt=user_prompt, temperature=0.0)

        return self.parse(prompt, _runner)


def stub_llm_runner(system_prompt: str, user_prompt: str) -> str:
    """Schema-valid empty ledger. Not a parser. Pipeline tests only."""
    scene_match = re.search(r"SCENE_ID: (\S+)", user_prompt)
    prompt_match = re.search(r"RAW_PROMPT: (.+)", user_prompt, re.DOTALL)
    scene_id = scene_match.group(1) if scene_match else f"scene_{uuid.uuid4().hex[:8]}"
    raw_prompt = prompt_match.group(1).strip() if prompt_match else "empty"
    return json.dumps(
        {
            "scene_id": scene_id,
            "raw_prompt": raw_prompt or "empty",
            "entities": [],
            "assertions": [],
            "uncertainties": [],
            "unsupported_claims": [],
        }
    )


MOCK_VALID_PAYLOAD = {
    "scene_id": "scene_a1b2c3d4",
    "raw_prompt": "An apple inside a transparent bowl on a table.",
    "entities": [
        {"id": "apple_1", "label": "apple", "type": "object", "count": 1, "attributes": ["red"]},
        {"id": "bowl_1", "label": "bowl", "type": "container", "count": 1, "attributes": ["transparent"]},
        {"id": "table_1", "label": "table", "type": "surface", "count": 1, "attributes": []},
    ],
    "assertions": [
        {
            "id": "assert_001",
            "subject": "apple_1",
            "relation": "inside",
            "target": "bowl_1",
            "class": "HARD_GEOMETRIC",
            "verifier": "containment_v1",
            "tolerance": 0.05,
            "failure_action": "LOCAL_REPAIR",
            "status": "UNVERIFIED",
        },
        {
            "id": "assert_002",
            "subject": "bowl_1",
            "relation": "on",
            "target": "table_1",
            "class": "HARD_GEOMETRIC",
            "verifier": "containment_v1",
            "tolerance": 0.05,
            "failure_action": "LOCAL_REPAIR",
            "status": "UNVERIFIED",
        },
    ],
    "uncertainties": [],
    "unsupported_claims": [],
}


if __name__ == "__main__":
    engine = VSSParserEngine()
    ok, err = engine.validate(MOCK_VALID_PAYLOAD)
    print(f"Self-Test Validation Status: {ok} -> {err}")
    stub = engine.parse("An apple inside a transparent bowl on a table.", stub_llm_runner)
    print(f"Stub parse: {stub['status']}")
    sys.exit(0 if ok and stub["status"] == "SUCCESS" else 1)
