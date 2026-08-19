#!/usr/bin/env python3
"""
VSS-2 ledger adapter — project a VSS-1 Assertion Ledger into verifier work orders.

No VLM. No pixels. Fail-closed if the ledger fails VSS-1 schema or contract.

F9: the work order NEVER includes raw_prompt. Pixel verifiers stay blind.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

PARSER_DIR = Path("/root/AAA/skills/forge-vss-parser")
if str(PARSER_DIR) not in sys.path:
    sys.path.insert(0, str(PARSER_DIR))

from vss_parser_engine import VSSParserEngine  # noqa: E402

# VSS-1 verifier token → VSS-2 suite name. "none" is unrouted (no pixel check).
VERIFIER_DISPATCH = {
    "containment_v1": "count_containment",
    "count_v1": "count_containment",
    "perspective_v1": "perspective_depth",
    "shadow_v1": "shadow_light",
    "none": None,
}


def _entity_index(ledger: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {e["id"]: e for e in ledger.get("entities", []) if isinstance(e, dict) and "id" in e}


def project_ledger(
    ledger: Any,
    engine: Optional[VSSParserEngine] = None,
) -> Dict[str, Any]:
    """Validate a VSS-1 ledger and project it into a VSS-2 work order."""
    if not isinstance(ledger, dict):
        return {
            "ok": False,
            "error_code": "E_LEDGER_NOT_OBJECT",
            "validation_message": "assertions must be a VSS-1 ledger object",
        }

    engine = engine or VSSParserEngine()
    valid, msg = engine.validate(ledger)
    if not valid:
        code = "E_CONTRACT_INVALID" if str(msg).startswith("CONTRACT") else "E_SCHEMA_INVALID"
        return {"ok": False, "error_code": code, "validation_message": msg}

    entities = _entity_index(ledger)
    routed: Dict[str, List[dict]] = {
        "count_containment": [],
        "perspective_depth": [],
        "shadow_light": [],
    }
    unrouted: List[dict] = []
    counts: Dict[str, int] = {}
    containments: List[dict] = []

    for entity in entities.values():
        label = entity.get("label") or entity["id"]
        count = int(entity.get("count", 1))
        if count > 1:
            counts[label] = count

    for assertion in ledger.get("assertions", []):
        target_suite = VERIFIER_DISPATCH.get(assertion.get("verifier"))
        subject = entities.get(assertion["subject"], {})
        target = entities.get(assertion["target"], {})
        item = {
            "id": assertion["id"],
            "subject_id": assertion["subject"],
            "subject_label": subject.get("label", assertion["subject"]),
            "relation": assertion["relation"],
            "target_id": assertion["target"],
            "target_label": target.get("label", assertion["target"]),
            "class": assertion["class"],
            "verifier": assertion["verifier"],
            "tolerance": assertion["tolerance"],
            "failure_action": assertion["failure_action"],
        }
        if target_suite is None:
            unrouted.append(item)
            continue
        routed[target_suite].append(item)
        if assertion["relation"] in {"inside", "on", "supported_by"}:
            containments.append(
                {
                    "subject": item["subject_label"],
                    "relation": assertion["relation"],
                    "target": item["target_label"],
                }
            )
        if assertion["class"] == "HARD_COUNT":
            label = item["subject_label"]
            counts[label] = int(subject.get("count", counts.get(label, 1)))

    light_source_count = sum(
        1 for e in entities.values() if e.get("type") == "light_source"
    )

    work_order = {
        "scene_id": ledger["scene_id"],
        "routed": routed,
        "unrouted": unrouted,
        "counts": counts,
        "containments": containments,
        "light_source_count": light_source_count,
        "unsupported_claim_count": len(ledger.get("unsupported_claims", [])),
        "uncertainty_count": len(ledger.get("uncertainties", [])),
        "f9_prompt_stripped": True,
    }
    if "raw_prompt" in work_order or "raw_prompt" in routed:
        return {"ok": False, "error_code": "E_PROMPT_LEAK"}

    return {"ok": True, "work_order": work_order}
