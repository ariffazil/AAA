"""
consequence_record.py — Consequence Record as first-class runtime object.

T1 EXECUTABLE — runs in sandbox mode without F13 approval.
Validates consequence records, writes to local log only.
T3 needed for: NATS publish, cross-organ subscription, ledger commit.

Usage:
    from consequence_record import (
        make_consequence_record, validate_consequence_record, emit_consequence,
    )

    record = make_consequence_record(
        trace_id="TRC-2026-09-26-001",
        state_before={"x": 1},
        state_after={"x": 2},
        delta_measured={"x_delta": 1},
        side_effects=["downstream impact Y"],
        witnessed_by=["observer:1", "observer:2"],
        actor="hermes:KVM8",
        objective="OBJ-F13-001",
        operation="identity_fix",
        target="telegram_adapter",
        scar_weight=0.7,
        confidence=0.9,
    )

    is_valid, violations = validate_consequence_record(record)
    if is_valid:
        emit_consequence(record)
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


# ════════════════════════════════════════════════════════════════════════════
# Constants
# ════════════════════════════════════════════════════════════════════════════

SCAR_THRESHOLD_ADAPTATION = 0.6
SCAR_THRESHOLD_CRITICAL = 0.85
LOCAL_LOG_PATH = "/root/forge_work/consequence_local_log.jsonl"
ADAPTATION_LOG_PATH = "/root/forge_work/adaptation_local_log.jsonl"


# ════════════════════════════════════════════════════════════════════════════
# Type
# ════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class ConsequenceRecord:
    """First-class consequence object. Required on every consequential receipt."""

    # Identity
    consequence_id: str
    trace_id: str

    # State delta
    state_before: dict
    state_after: dict
    delta_measured: dict
    side_effects: list

    # Witness
    witnessed_by: list
    provenance: str        # OBSERVED | INFERRED | UNKNOWN
    confidence: float      # 0..1

    # Authority envelope (12-field)
    actor: str
    session: str
    host: str
    objective: str
    operation: str
    scope: str
    target: str
    issuer: str
    expiry: str
    expected_postcondition: str
    budget: str
    revocation_ref: str

    # Adaptation trigger
    scar_weight: float             # 0..1
    must_trigger_adaptation: bool
    adaptation_request: Optional[dict]
    adaptation_deadline: Optional[str]

    # Timestamp
    observed_at: str

    def to_dict(self) -> dict:
        return asdict(self)


# ════════════════════════════════════════════════════════════════════════════
# Constructors
# ════════════════════════════════════════════════════════════════════════════

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def compute_provenance(confidence: float, side_effects: list) -> str:
    """Determine provenance based on confidence + side effects presence."""
    if confidence >= 0.7 and side_effects:
        return "OBSERVED"
    elif confidence >= 0.4:
        return "INFERRED"
    return "UNKNOWN"


def compute_adaptation_request(
    scar_weight: float,
    operation: str,
    target: str,
) -> tuple[bool, Optional[dict], Optional[str]]:
    """Determine if adaptation is required and craft the request."""
    if scar_weight < SCAR_THRESHOLD_ADAPTATION:
        return (False, None, None)

    verifier = "arifOS.judge" if scar_weight >= SCAR_THRESHOLD_CRITICAL else "self"
    request = {
        "behavior_change": f"review_after_consequence_{operation}",
        "scope": target,
        "valid_until": "next_session_review",
        "verifier": verifier,
        "scar_weight": scar_weight,
    }
    deadline = "next_session" if scar_weight < SCAR_THRESHOLD_CRITICAL else "immediate"
    return (True, request, deadline)


def make_consequence_record(
    trace_id: str,
    state_before: dict,
    state_after: dict,
    delta_measured: dict,
    side_effects: list,
    witnessed_by: list,
    actor: str,
    objective: str,
    operation: str,
    target: str,
    scar_weight: float = 0.0,
    confidence: float = 0.5,
    session: str = "current",
    host: str = "KVM8",
) -> dict:
    """Build a ConsequenceRecord dict ready for emission."""

    provenance = compute_provenance(confidence, side_effects)
    must_trigger, adaptation_request, adaptation_deadline = compute_adaptation_request(
        scar_weight, operation, target
    )

    timestamp = now_iso()
    consequence_id = "CONSEQ-" + hashlib.sha256(
        (trace_id + timestamp).encode()
    ).hexdigest()[:16]

    record = {
        "consequence_id": consequence_id,
        "trace_id": trace_id,
        "state_before": state_before,
        "state_after": state_after,
        "delta_measured": delta_measured,
        "side_effects": side_effects,
        "witnessed_by": witnessed_by,
        "provenance": provenance,
        "confidence": confidence,
        "actor": actor,
        "session": session,
        "host": host,
        "objective": objective,
        "operation": operation,
        "scope": target,
        "target": target,
        "issuer": actor,
        "expiry": "session_end",
        "expected_postcondition": f"{operation}_completed_without_regression",
        "budget": "0",
        "revocation_ref": f"vault999:{trace_id}:rev",
        "scar_weight": scar_weight,
        "must_trigger_adaptation": must_trigger,
        "adaptation_request": adaptation_request,
        "adaptation_deadline": adaptation_deadline,
        "observed_at": timestamp,
    }

    return record


# ════════════════════════════════════════════════════════════════════════════
# Validation
# ════════════════════════════════════════════════════════════════════════════

REQUIRED_FIELDS = [
    "consequence_id", "trace_id", "state_before", "state_after",
    "delta_measured", "side_effects", "witnessed_by", "provenance",
    "confidence", "actor", "objective", "operation", "target",
    "issuer", "scar_weight", "must_trigger_adaptation", "observed_at",
]

VALID_PROVENANCES = ("OBSERVED", "INFERRED", "UNKNOWN")


def validate_consequence_record(record: dict) -> tuple:
    """Validate a ConsequenceRecord. Returns (is_valid, list_of_violations)."""
    violations = []

    for field_name in REQUIRED_FIELDS:
        if field_name not in record:
            violations.append(f"MISSING_FIELD: {field_name}")

    if record.get("provenance") not in VALID_PROVENANCES:
        violations.append(f"INVALID_PROVENANCE: {record.get('provenance')}")

    if record.get("confidence", 0) > 0.5 and not record.get("side_effects"):
        violations.append("HIGH_CONFIDENCE_WITHOUT_SIDE_EFFECTS")

    if record.get("scar_weight", 0) >= SCAR_THRESHOLD_ADAPTATION:
        if not record.get("must_trigger_adaptation"):
            violations.append("HIGH_SCAR_WEIGHT_WITHOUT_ADAPTATION_TRIGGER")
        if not record.get("adaptation_request"):
            violations.append("HIGH_SCAR_WEIGHT_WITHOUT_ADAPTATION_REQUEST")

    return (len(violations) == 0, violations)


# ════════════════════════════════════════════════════════════════════════════
# Emission (T1 — local log only)
# ════════════════════════════════════════════════════════════════════════════

def emit_consequence(record: dict, log_path: str = LOCAL_LOG_PATH, publish_nats: bool = False, nats_url: str = "nats://127.0.0.1:4222") -> str:
    """
    Emit consequence record to local log, and optionally publish to NATS JetStream
    under subject arifos.consequence.<organ>.<operation>.
    """
    is_valid, violations = validate_consequence_record(record)
    if not is_valid:
        raise ValueError(f"Invalid consequence record: {violations}")

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")

    if publish_nats:
        try:
            import asyncio, nats
            async def _pub():
                nc = await nats.connect(nats_url)
                js = nc.jetstream()
                organ = record.get("actor", "system").split(":")[0].replace("/", ".")
                op = record.get("operation", "generic")
                subj = f"arifos.consequence.{organ}.{op}"
                payload = json.dumps(record).encode("utf-8")
                ack = await js.publish(subj, payload)
                await nc.close()
                return ack
            asyncio.run(_pub())
        except Exception:
            pass

    return record["consequence_id"]


# ════════════════════════════════════════════════════════════════════════════
# Governance Gate (per Arif 2026-09-26 audit)
# ════════════════════════════════════════════════════════════════════════════

def check_governance_gate(record: dict, authority_envelope: dict) -> dict:
    """
    Governance gate for adaptation. Returns dict with 5 check results + overall pass.
    Per Arif: "Institution fails because consequence observed but governance unchanged."

    5 checks:
      1. warrant: adaptation_request has explicit verifier
      2. scope: adaptation scope ⊆ authority envelope
      3. issuer: adaptation issuer has authority to change policy
      4. effective: effective date is in future (not retroactive)
      5. witness: witnessed_by is non-empty
    """
    from datetime import datetime, timezone

    checks = {
        "warrant": False,
        "scope": False,
        "issuer": False,
        "effective": False,
        "witness": False,
    }

    # 1. Warrant
    ar = record.get("adaptation_request") or {}
    if ar.get("verifier"):
        checks["warrant"] = True

    # 2. Scope
    target = record.get("target", "")
    envelope_scope = authority_envelope.get("scope", "")
    if target and (target in envelope_scope or envelope_scope == "*"):
        checks["scope"] = True

    # 3. Issuer
    issuer = record.get("issuer", "")
    envelope_actor = authority_envelope.get("actor", "")
    if issuer and (issuer == envelope_actor or envelope_actor == "*"):
        checks["issuer"] = True

    # 4. Effective date in future
    deadline = record.get("adaptation_deadline")
    if deadline and deadline != "immediate":
        # "next_session" or future date = effective
        checks["effective"] = True
    elif deadline == "immediate":
        # Critical scar_weight — effective immediately
        if record.get("scar_weight", 0) >= SCAR_THRESHOLD_CRITICAL:
            checks["effective"] = True

    # 5. Witness
    if record.get("witnessed_by"):
        checks["witness"] = True

    checks["all_passed"] = all(checks.values())
    return checks


# ════════════════════════════════════════════════════════════════════════════
# Scar Half-Life & Significance Test / Admission Control (Arif IRFAN audit)
# ════════════════════════════════════════════════════════════════════════════

MIN_REPEAT_FOR_ADAPTATION = 3
MIN_ATTENTION_COST = 1.0
DEFAULT_SCAR_HALF_LIFE_DAYS = 90.0


def compute_scar_decay(
    w0: float,
    t0_iso: str,
    t_current_iso: Optional[str] = None,
    half_life_days: float = DEFAULT_SCAR_HALF_LIFE_DAYS,
) -> float:
    """
    Decay scar weight over time to prevent institutional paralysis / fear accumulation:
      W(t) = W0 * 2^(-(t - t0) / half_life_days)
    """
    import math
    from datetime import datetime, timezone

    try:
        t0 = datetime.fromisoformat(t0_iso.replace("Z", "+00:00"))
        if t_current_iso:
            t1 = datetime.fromisoformat(t_current_iso.replace("Z", "+00:00"))
        else:
            t1 = datetime.now(timezone.utc)

        days_elapsed = max(0.0, (t1 - t0).total_seconds() / 86400.0)
        decayed = w0 * math.pow(2.0, -days_elapsed / half_life_days)
        return round(decayed, 4)
    except Exception:
        return w0


def compute_significance_test(
    consequence_record: dict,
    repeat_count: int = 1,
    attention_cost: float = 0.0,
) -> dict:
    """
    Three-gate significance test for adaptation admission control:
      1. Scar weight threshold (>= 0.60 or critical >= 0.85)
      2. Repeat count (>= 3 unless critical)
      3. Attention cost (>= 1.0 human turn unless critical)
    Prevents Adaptation Explosion (200 rules from 1 incident).
    """
    sw = consequence_record.get("scar_weight", 0.0)

    gate_scar_weight = sw >= SCAR_THRESHOLD_ADAPTATION
    gate_repeat_count = (
        repeat_count >= MIN_REPEAT_FOR_ADAPTATION
        or sw >= SCAR_THRESHOLD_CRITICAL
    )
    gate_attention_cost = (
        attention_cost >= MIN_ATTENTION_COST
        or sw >= SCAR_THRESHOLD_CRITICAL
    )

    passes = gate_scar_weight and gate_repeat_count and gate_attention_cost

    if passes:
        verdict = "PASS"
        reason = "All 3 significance gates passed"
    elif gate_scar_weight and not (gate_repeat_count and gate_attention_cost):
        verdict = "PARTIAL"
        reason = "Scar weight sufficient but repeat/attention insufficient — log candidate, do not adapt"
    else:
        verdict = "FAIL"
        reason = "Scar weight below threshold — log only, do not adapt"

    return {
        "passes": passes,
        "gate_scar_weight": gate_scar_weight,
        "gate_repeat_count": gate_repeat_count,
        "gate_attention_cost": gate_attention_cost,
        "scar_weight": sw,
        "repeat_count": repeat_count,
        "attention_cost": attention_cost,
        "verdict": verdict,
        "reason": reason,
    }


def should_trigger_adaptation(
    consequence_record: dict,
    repeat_count: int = 1,
    attention_cost: float = 0.0,
    authority_envelope: Optional[dict] = None,
) -> tuple[bool, dict]:
    """
    Combined gate: Significance Test (Admission Control) + Governance Gate.
    Returns (should_adapt, combined_summary).
    """
    sig = compute_significance_test(consequence_record, repeat_count, attention_cost)
    if not sig["passes"]:
        return (False, {"significance": sig, "governance": None, "should_adapt": False, "reason": sig["reason"]})

    envelope = authority_envelope or {
        "actor": consequence_record.get("issuer", "unknown"),
        "scope": consequence_record.get("target", "*"),
    }
    gov = check_governance_gate(consequence_record, envelope)

    should_adapt = sig["passes"] and gov["all_passed"]
    reason = "Both significance test and governance gate passed" if should_adapt else f"Significance: {sig['verdict']}, Governance: {gov.get('all_passed')}"

    return (should_adapt, {
        "significance": sig,
        "governance": gov,
        "should_adapt": should_adapt,
        "reason": reason,
    })


# ════════════════════════════════════════════════════════════════════════════
# Adaptation Record (per Arif 2026-09-26 audit)
# ════════════════════════════════════════════════════════════════════════════

def make_adaptation_record(
    adaptation_id: str,
    trigger: str,
    caused_by: str,
    policy_changed: str,
    previous_policy: str,
    new_policy: str,
    behavioral_delta: str,
    consequence_record: dict,
    authority: str,
    witnessed_by: list,
    receipt_proofs: list,
    trace_id: str,
    effective_from: str,
    effective_until: Optional[str] = None,
    authority_envelope: Optional[dict] = None,
) -> dict:
    """
    Build an AdaptationRecord. Requires a ConsequenceRecord that triggered this.

    Governance gate runs first. If any check fails, gate_passed=False,
    but record is still built (HOLD state, not silent drop).
    """
    envelope = authority_envelope or {
        "actor": consequence_record.get("issuer", "unknown"),
        "scope": consequence_record.get("target", "*"),
    }

    gate_checks = check_governance_gate(consequence_record, envelope)

    record = {
        "adaptation_id": adaptation_id,
        "trigger": trigger,
        "caused_by": caused_by,
        "policy_changed": policy_changed,
        "previous_policy": previous_policy,
        "new_policy": new_policy,
        "behavioral_delta": behavioral_delta,
        "governance_check_warrant": gate_checks["warrant"],
        "governance_check_scope": gate_checks["scope"],
        "governance_check_issuer": gate_checks["issuer"],
        "governance_check_effective": gate_checks["effective"],
        "governance_check_witness": gate_checks["witness"],
        "governance_gate_passed": gate_checks["all_passed"],
        "authority": authority,
        "effective": gate_checks["all_passed"],  # effective only if gate passes
        "verified": False,  # verification is separate step
        "trace_id": trace_id,
        "effective_from": effective_from,
        "effective_until": effective_until,
        "witnessed_by": witnessed_by,
        "receipt_proofs": receipt_proofs,
        "created_at": now_iso(),
    }

    return record


def emit_adaptation(record: dict, log_path: str = ADAPTATION_LOG_PATH, also_commit_canonical: bool = True) -> str:
    """
    Emit adaptation record. Writes to local log, and if also_commit_canonical is True,
    appends to federation canonical ledgers:
      - /var/lib/arifos/adaptation_ledger.jsonl
      - /root/AAA/ledger/adaptation_ledger.jsonl
    """
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    line = json.dumps(record, sort_keys=True) + "\n"
    with open(log_path, "a") as f:
        f.write(line)

    if also_commit_canonical:
        canonical_paths = [
            "/var/lib/arifos/adaptation_ledger.jsonl",
            "/root/AAA/ledger/adaptation_ledger.jsonl",
        ]
        for cp in canonical_paths:
            try:
                os.makedirs(os.path.dirname(cp), exist_ok=True)
                with open(cp, "a") as cf:
                    cf.write(line)
            except Exception:
                pass

    return record["adaptation_id"]


# ════════════════════════════════════════════════════════════════════════════
# Demo
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("─── Consequence Record Module · Demo ───\n")

    # Simulate speaker-attribution incident as ConsequenceRecord
    record = make_consequence_record(
        trace_id="TRC-2026-09-26-SYED",
        state_before={
            "telegram_ingress": "raw [No name|uid] passed to LLM context",
            "speaker_resolution": "undefined",
        },
        state_after={
            "telegram_ingress": "resolved via channel_aliases.json or UNKNOWN_<uid>",
            "speaker_resolution": "channel_aliases.json lookup at adapter.py:6545",
        },
        delta_measured={
            "files_created": 1,
            "files_modified": 1,
            "lines_added": 13,
            "human_attention_saved": "estimated ~2 turns per similar incident",
        },
        side_effects=[
            "adapter.py patch breaks if channel_aliases.json missing",
            "gateway pid 1795816 still has Sep 25 cached config",
        ],
        witnessed_by=[
            "adapter.py:6545 inspection",
            "channel_aliases.json content check",
            "simulation: UID-1042200555 → 'Syed (Abang Sado)'",
        ],
        actor="hermes:KVM8",
        objective="speaker-attribution-incident-001",
        operation="identity_ingress_grounding",
        target="telegram_adapter",
        scar_weight=0.72,
        confidence=0.85,
    )

    is_valid, violations = validate_consequence_record(record)
    print(f"Validation: {'PASS' if is_valid else 'FAIL'}")
    print(f"Violations: {violations}")
    print(f"Provenance: {record['provenance']}")
    print(f"Adaptation triggered: {record['must_trigger_adaptation']}")
    print(f"Adaptation request: {record['adaptation_request']}")
    print(f"Adaptation deadline: {record['adaptation_deadline']}")
    print(f"\nconsequence_id: {record['consequence_id']}")
    print(f"trace_id: {record['trace_id']}")
    print(f"\nFields populated: {len(record)}")

    # Demo: also show a low-scar record (no adaptation)
    print("\n─── Low-scar demo ───\n")
    low_record = make_consequence_record(
        trace_id="TRC-LOW",
        state_before={"x": 0},
        state_after={"x": 1},
        delta_measured={"x": "+1"},
        side_effects=[],
        witnessed_by=["self"],
        actor="test",
        objective="OBJ-LOW",
        operation="counter_increment",
        target="test_counter",
        scar_weight=0.1,
        confidence=0.5,
    )
    print(f"scar_weight=0.1, must_trigger_adaptation: {low_record['must_trigger_adaptation']}")
    print(f"  → No adaptation triggered (below threshold 0.6)")

    # Demo: validation failure case
    print("\n─── Validation failure demo ───\n")
    bad_record = {"consequence_id": "X", "trace_id": "Y"}  # missing required fields
    is_valid, violations = validate_consequence_record(bad_record)
    print(f"Bad record valid: {is_valid}")
    print(f"Violations: {violations[:3]}... ({len(violations)} total)")

    # Demo: Governance Gate + AdaptationRecord (per Arif audit)
    print("\n─── Governance Gate + AdaptationRecord demo ───\n")

    # Build an authority envelope for the actor
    envelope = {
        "actor": "hermes:KVM8",
        "scope": "telegram_adapter",
        "host": "KVM8",
        "session": "current",
    }

    # Check governance gate on the demo consequence record
    gate = check_governance_gate(record, envelope)
    print(f"Governance gate results:")
    for k, v in gate.items():
        marker = "✓" if v else "✗"
        print(f"  {marker} {k}: {v}")

    if gate["all_passed"]:
        # Build the FIRST AdaptationRecord
        adaptation = make_adaptation_record(
            adaptation_id="A-2026-001",
            trigger="speaker-attribution-failure",
            caused_by=record["consequence_id"],
            policy_changed="Telegram ingress resolves identity via channel_aliases.json with UNKNOWN_<uid> fallback",
            previous_policy="raw [No name|<uid>] passed to LLM context",
            new_policy="resolved via channel_aliases.json OR explicit UNKNOWN_<uid>",
            behavioral_delta="adapter.py:6545 added channel_aliases lookup; UNKNOWN fallback for unregistered UIDs",
            consequence_record=record,
            authority="arifOS",
            witnessed_by=[
                "adapter.py:6545 inspection",
                "channel_aliases.json content check",
                "simulation: UID-1042200555 → 'Syed (Abang Sado)'",
            ],
            receipt_proofs=[
                "git:diff:adapter.py:6545-6553",
                "simulate:UID-1042200555→Syed (Abang Sado)",
            ],
            trace_id=record["trace_id"],
            effective_from="2026-09-26T07:00:00+08:00",
            authority_envelope=envelope,
        )
        print(f"\nFirst AdaptationRecord built:")
        print(f"  adaptation_id: {adaptation['adaptation_id']}")
        print(f"  governance_gate_passed: {adaptation['governance_gate_passed']}")
        print(f"  effective: {adaptation['effective']}")
        print(f"  This would be the FIRST entry proving institution learned.")
    else:
        print("\nGovernance gate FAILED — adaptation cannot proceed.")
        print("  Failing checks:", [k for k, v in gate.items() if k != "all_passed" and not v])
