#!/usr/bin/env python3
"""
compile_reality_plan.py — forge_compile_reality_plan CLI

Compiles a natural-language intent + current reality state into a valid
reality-plan.schema.json instance with SHA-256 plan_hash.

Distinct from forge_compile_task (aforge), which produces TaskIR for coding.
This tool produces a RealityPlan for institutional/consequence-bearing work.

Usage:
    python3 compile_reality_plan.py \\
        --intent "deploy a-forge v2.3 to KVM4" \\
        --action-class MUTATE \\
        --severity MEDIUM \\
        --output /tmp/plan.json

Exit 0 on success, 1 on validation failure. Prints plan_hash on success.

Stdlib + jsonschema + pyyaml + hashlib only. No new pip packages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    print("FATAL: pyyaml required", file=sys.stderr)
    sys.exit(1)

try:
    import jsonschema
except ImportError:
    print("FATAL: jsonschema required", file=sys.stderr)
    sys.exit(1)


SCHEMA_PATH = Path("/root/AAA/schemas/reality-plan.schema.json")
REALITY_OBJECTS_ROOT = Path("/root/AAA/state/reality_objects")

VALID_OUTPUT_KINDS = ("chat", "artifact", "action", "workflow", "mixed", "none")
VALID_SENSORS = (
    "service_health_probe",
    "process_state",
    "version_readback",
    "database_readback",
    "geological_evidence",
    "financial_market_witness",
    "delivery_acknowledgement",
    "human_response",
    "temporal_chain",
    "none",
)
VALID_AUTHORITY_CLASSES = (
    "informational",
    "advisory",
    "declarative",
    "executable",
    "constitution",
)

# action_class -> risk_class used to decide authority_requirement
CONSTITUTION_CLASS_RISKS = {"MUTATE", "DEPLOY", "IRREVERSIBLE", "F13_BINARY"}
READ_CLASS_RISKS = {"READ", "OBSERVE", "QUERY"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── output_kind inference ────────────────────────────────────────────────────
OUTPUT_KIND_KEYWORDS = {
    "action": ("deploy", "run", "execute", "mutate"),
    "workflow": ("schedule", "workflow", "multi-step"),
    "artifact": ("create file", "write", "save"),
    "chat": ("explain", "tell me", "what is"),
    "mixed": ("bundle", "deploy system", "full delivery", "architecture"),
}


def infer_output_kind(intent: str) -> list[str]:
    """Return output_kind as a list (schema requires array, minItems 1)."""
    lower = intent.lower()
    # Check chat FIRST — it is the only one that can stand alone.
    if any(k in lower for k in OUTPUT_KIND_KEYWORDS["chat"]):
        return ["chat"]
    matched: list[str] = []
    # mixed takes precedence — AAOS v2.0 Level 5 Bundle Law
    if any(k in lower for k in OUTPUT_KIND_KEYWORDS["mixed"]):
        matched.append("mixed")
    # workflow takes precedence over action if both fire
    if any(k in lower for k in OUTPUT_KIND_KEYWORDS["workflow"]):
        matched.append("workflow")
    if any(k in lower for k in OUTPUT_KIND_KEYWORDS["action"]):
        matched.append("action")
    if any(k in lower for k in OUTPUT_KIND_KEYWORDS["artifact"]):
        matched.append("artifact")
    if not matched:
        matched.append("none")
    # Dedup, preserve order
    seen = set()
    out = []
    for k in matched:
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out


# ── persistence decision ─────────────────────────────────────────────────────
PERSISTENCE_KEYWORD_REASONS = {
    "audit": "audit_provenance_required",
    "irreversible": "authority_trace_required",
    "deploy": "external_consequence",
    "record": "projection_consistency_required",
    "seal": "recovery_required",
}


def compute_persistence(intent: str) -> dict:
    lower = intent.lower()
    reasons: list[str] = []
    for kw, reason in PERSISTENCE_KEYWORD_REASONS.items():
        if kw in lower and reason not in reasons:
            reasons.append(reason)
    return {"required": bool(reasons), "reasons": reasons}


# ── authority_requirement ────────────────────────────────────────────────────
def compute_authority(action_class: str, intent: str, output_kind: list[str]) -> dict:
    """
    required = True iff action crosses constitution-class authority.
    chat-only plans force required=False (schema invariant).
    """
    if output_kind == ["chat"]:
        return {"required": False, "applies_to": "transition"}
    ac = (action_class or "").upper()
    required = ac in CONSTITUTION_CLASS_RISKS
    klass = "constitution" if required else ("executable" if ac == "WRITE" else "informational")
    return {
        "required": required,
        "class": klass,
        "applies_to": "transition",
    }


# ── transition ───────────────────────────────────────────────────────────────
def compute_transition(intent: str, output_kind: list[str]) -> Optional[dict]:
    if not any(k in output_kind for k in ("action", "workflow")):
        return None
    lower = intent.lower()
    reversible = not (("deploy" in lower) or ("irreversible" in lower))
    return {
        "reversible": reversible,
        "scope": "single_target",
    }


# ── observation.sensor picker ────────────────────────────────────────────────
SENSOR_KEYWORDS = {
    "service_health_probe": ("deploy", "http", "endpoint", "service"),
    "database_readback": ("database", "db ", "sql", "postgres", "redis"),
    "version_readback": ("version", "release", "tag"),
    "geological_evidence": ("geology", "seismic", "well", "basin"),
    "financial_market_witness": ("price", "market", "xauusd", "stock", "share"),
    "delivery_acknowledgement": ("deliver", "ship", "send"),
    "human_response": ("ask arif", "human", "sovereign", "arif"),
    "temporal_chain": ("schedule", "cron", "recurring"),
}


def pick_sensor(intent: str) -> str:
    lower = intent.lower()
    for sensor, keywords in SENSOR_KEYWORDS.items():
        if any(k in lower for k in keywords):
            return sensor
    return "process_state"


# ── current_state from WRO ───────────────────────────────────────────────────
def load_default_current_state() -> dict:
    """Pick the first WRO and use its observed_fact as the from-state."""
    if not REALITY_OBJECTS_ROOT.exists():
        return {"evidence_ref": None}
    for f in sorted(REALITY_OBJECTS_ROOT.glob("*.y*ml")):
        try:
            data = yaml.safe_load(f.read_text())
        except Exception:
            continue
        if isinstance(data, dict) and data.get("schema") == "arifos.wro.v1":
            fact = data.get("observed_fact", "")
            return {
                "evidence_ref": f"reality_object:{data.get('id', f.stem)}",
                "observed_fact": fact.strip() if isinstance(fact, str) else str(fact),
            }
    return {"evidence_ref": None}


# ── intended_delta ───────────────────────────────────────────────────────────
def compute_intended_delta(current_state: dict) -> dict:
    fact = current_state.get("observed_fact")
    if fact:
        return {"from": fact, "to": f"post_action_state_derived_from_intent"}
    return {"from": None, "to": None}


# ── verification ─────────────────────────────────────────────────────────────
def compute_verification(action_class: str) -> dict:
    ac = (action_class or "").upper()
    before: list[str] = []
    after: list[str] = []
    if ac in CONSTITUTION_CLASS_RISKS:
        before.append("reality_object_gate --gate")
        after.append("sensor_witness_check")
    if ac in READ_CLASS_RISKS:
        before.append("schema_lookup")
    return {"before": before, "after": after}


# ── hash ─────────────────────────────────────────────────────────────────────
def canonicalize_and_hash(plan: dict) -> str:
    """
    SHA-256 of canonicalized JSON (sorted keys, no whitespace, UTF-8).
    Excludes the plan_hash field itself if present (it is meta).
    """
    body = {k: v for k, v in plan.items() if k != "plan_hash"}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ── build plan ───────────────────────────────────────────────────────────────
def build_plan(
    intent: str,
    action_class: str,
    severity: str,
    current_state: Optional[dict] = None,
    capability_ref: Optional[str] = None,
) -> dict:
    output_kind = infer_output_kind(intent)
    persistence = compute_persistence(intent)

    # If user did not pass current_state, derive default from WRO
    if current_state is None:
        current_state = load_default_current_state()

    intended_delta = compute_intended_delta(current_state)
    authority = compute_authority(action_class, intent, output_kind)
    transition = compute_transition(intent, output_kind)
    sensor = pick_sensor(intent)
    verification = compute_verification(action_class)

    # minimal_provenance
    intent_hash = hashlib.sha256(intent.encode("utf-8")).hexdigest()
    consequence_class = (
        "constitution" if (action_class or "").upper() in CONSTITUTION_CLASS_RISKS
        else "informational"
    )

    plan: dict[str, Any] = {
        "intent": intent,
        "current_state": current_state,
        "intended_delta": intended_delta,
        "output_kind": output_kind,
        "persistence": persistence,
        "authority_requirement": authority,
        "verification": verification,
        "observation": {
            "sensor": sensor,
            "evidence_ref": current_state.get("evidence_ref"),
            "status": "pending",
        },
        "task_status": "ACTIVE_INVESTIGATION",
        "minimal_provenance": {
            "intent_hash": intent_hash,
            "consequence_class": consequence_class,
            "capability_refs": [capability_ref] if capability_ref else [],
            "observed_outcome": "unobserved",
        },
        "created_at": now_iso(),
    }
    if transition is not None:
        if capability_ref:
            transition["capability"] = capability_ref
        plan["transition"] = transition

    plan["plan_hash"] = canonicalize_and_hash(plan)
    return plan


# ── validate against schema ─────────────────────────────────────────────────
def validate_against_schema(plan: dict) -> tuple[bool, list[str]]:
    if not SCHEMA_PATH.exists():
        return False, [f"schema not found at {SCHEMA_PATH}"]
    try:
        schema = json.loads(SCHEMA_PATH.read_text())
    except Exception as e:
        return False, [f"schema parse error: {e}"]
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(plan), key=lambda e: e.path)
    violations = [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors]
    return (len(violations) == 0, violations)


# ── CLI ──────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(
        description="forge_compile_reality_plan — compile an intent into a RealityPlan JSON",
    )
    ap.add_argument("--intent", required=True, help="natural-language intent")
    ap.add_argument(
        "--action-class",
        default="READ",
        help="risk/action class: READ | WRITE | MUTATE | DEPLOY | IRREVERSIBLE | F13_BINARY",
    )
    ap.add_argument(
        "--severity",
        default="LOW",
        help="severity hint: TRIVIAL|LOW|MEDIUM|HIGH|CATASTROPHIC",
    )
    ap.add_argument(
        "--current-state-json",
        default=None,
        help="optional path to JSON file overriding default current_state",
    )
    ap.add_argument(
        "--capability-ref",
        default=None,
        help="optional capability_ref to attach to transition / minimal_provenance",
    )
    ap.add_argument(
        "--output",
        required=True,
        help="output path for the compiled RealityPlan JSON",
    )
    args = ap.parse_args()

    current_state: Optional[dict] = None
    if args.current_state_json:
        try:
            current_state = json.loads(Path(args.current_state_json).read_text())
        except Exception as e:
            print(f"FATAL: cannot read current_state_json: {e}", file=sys.stderr)
            return 1

    plan = build_plan(
        intent=args.intent,
        action_class=args.action_class,
        severity=args.severity,
        current_state=current_state,
        capability_ref=args.capability_ref,
    )

    ok, violations = validate_against_schema(plan)
    if not ok:
        print("VALIDATION FAILED:", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False))

    print(f"OK  plan_hash={plan['plan_hash']}")
    print(f"    output_kind={plan['output_kind']}")
    print(f"    persistence.required={plan['persistence']['required']}")
    print(f"    authority.required={plan['authority_requirement']['required']}")
    print(f"    sensor={plan['observation']['sensor']}")
    print(f"    wrote={out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
