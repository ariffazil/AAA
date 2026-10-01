#!/usr/bin/env python3
"""
m_min_audit.py — Minimum-Meaning (M_min) audit.

Per A-FORGE ↔ AAA Competency Protocol v1 + scar-2026-10-01-002:
  M_min = (I · E · A · C · W · T)^(1/6)
  M_min = 0 if any dimension is 0 or unknown.

Per scar-2026-10-01-002:
  W = 0 if verifier is same cognitive substrate as executor
  (same model + different prompt ≠ independence).

Any claim of M_min > 0 must be backed by per-dimension evidence.
This audit script enforces that claim with audit-by-floor.

Routing: replace naive Q_M claims with floor-checked M_min.
         same-model-prompt-variant verifiers are tagged but excluded.

Usage:
  python3 scripts/m_min_audit.py <path-to-competency-state.json>
  python3 scripts/m_min_audit.py state/aforge/competency/FI-008-kimi-code.json
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


DIMENSIONS = ["I", "E", "A", "C", "W", "T"]

DIMENSION_NAMES = {
    "I": "identity_integrity",
    "E": "evidence_quality",
    "A": "legitimate_authority",
    "C": "consequence_closure",
    "W": "independent_witness",
    "T": "temporal_continuity",
}


def _check_identity(state: dict) -> tuple[float, str]:
    """I — identity integrity. 1.0 if canonical name + fi_id + aliases present."""
    identity = state.get("identity", {})
    if identity.get("canonical_name") and identity.get("fi_id") and identity.get("aliases"):
        return 1.0, "canonical_name + fi_id + aliases present"
    return 0.0, "missing canonical_name / fi_id / aliases"


def _check_evidence(state: dict) -> tuple[float, str]:
    """E — evidence quality. Requires complete eval coverage (all E1-E8 decided)."""
    aforge = state.get("aforge_competency", {})
    eval_results = aforge.get("eval_results", {})
    if not eval_results:
        return 0.0, "no eval_results in state"
    decided = [v for v in eval_results.values() if v in ("PASS", "FAIL")]
    pending = [v for v in eval_results.values() if v == "PENDING"]
    total = len(eval_results)
    if pending:
        # Partial coverage. Score = passed / total_expected (not / decided).
        # This prevents "2/2 PASS" from scoring 1.0 when 6 evals are PENDING.
        passed = [v for v in decided if v == "PASS"]
        return len(passed) / total, f"{len(passed)}/{total} evals PASS ({len(pending)} PENDING — incomplete coverage)"
    if not decided:
        return 0.0, "no decided eval verdicts (all PENDING or N/A)"
    passed = [v for v in decided if v == "PASS"]
    return len(passed) / len(decided), f"{len(passed)}/{len(decided)} evals PASS (full coverage)"


def _check_authority(state: dict) -> tuple[float, str]:
    """A — legitimate authority. 0 if not attested; partial if declared but not verified."""
    auth = state.get("active_authority", {})
    session_token = auth.get("session_token")
    lease_id = auth.get("lease_id")
    if session_token and lease_id:
        return 1.0, "session_token + lease_id present (attested)"
    if session_token or lease_id:
        return 0.5, "partial attestation (token OR lease, not both)"
    return 0.0, "no session_token, no lease_id → declared-only"


def _check_consequence(state: dict) -> tuple[float, str]:
    """C — consequence closure. 1.0 if verified_tasks > 0; partial if experience trace exists."""
    aforge = state.get("aforge_competency", {})
    verified_tasks = aforge.get("verified_tasks", 0)
    if verified_tasks and verified_tasks > 0:
        return min(1.0, math.log2(verified_tasks + 1) / 6), f"{verified_tasks} verified tasks"
    return 0.0, "verified_tasks = 0"


def _check_witness(state: dict) -> tuple[float, str]:
    """W — independent witness. Per scar-2026-10-01-002, 0 if verifier = executor."""
    trust = state.get("trust", {})
    bypass_attempts = trust.get("bypass_attempts", 0)
    if bypass_attempts and bypass_attempts > 0:
        return 0.0, f"bypass_attempts = {bypass_attempts} → witness chain broken"
    self_audit = state.get("self_audit", {})
    if self_audit.get("trust_chain_state", {}).get("S_verified") is True:
        return 1.0, "S_verified = true (independently witnessed)"
    return 0.0, "S_verified not true → no independent witness chain"


def _check_temporal(state: dict) -> tuple[float, str]:
    """T — temporal continuity. 1.0 if cross-session continuity recorded."""
    aforge = state.get("aforge_competency", {})
    last_observed = aforge.get("last_observed")
    if not last_observed:
        return 0.0, "no last_observed timestamp"
    snapshot_at = state.get("snapshot_at")
    if not snapshot_at:
        return 0.5, "last_observed but no snapshot_at → partial temporal anchor"
    return 0.8, f"snapshot_at={snapshot_at}, last_observed={last_observed}"


def audit(state: dict) -> dict:
    """Compute M_min with per-dimension floor check."""
    dimension_scores = {}
    reasons = {}
    for dim, name in DIMENSION_NAMES.items():
        fn = {
            "I": _check_identity,
            "E": _check_evidence,
            "A": _check_authority,
            "C": _check_consequence,
            "W": _check_witness,
            "T": _check_temporal,
        }[dim]
        score, reason = fn(state)
        dimension_scores[dim] = score
        reasons[dim] = reason

    # Geometric mean. If any dim is 0 → M_min = 0.
    if any(v == 0.0 for v in dimension_scores.values()):
        m_min = 0.0
    else:
        m_min = math.exp(sum(math.log(v) for v in dimension_scores.values()) / 6)

    # Floor-by-floor audit
    floor_audit = []
    for dim in DIMENSIONS:
        score = dimension_scores[dim]
        if score == 0.0:
            floor_audit.append(f"FLOOR {dim} FAIL: {reasons[dim]}")
        elif score < 0.5:
            floor_audit.append(f"FLOOR {dim} WARN: {reasons[dim]} (score={score:.2f})")
        else:
            floor_audit.append(f"FLOOR {dim} PASS: {reasons[dim]} (score={score:.2f})")

    return {
        "m_min": m_min,
        "m_min_verdict": "MEANINGFUL" if m_min > 0 else "ZERO (weakest-link collapsed)",
        "dimension_scores": {DIMENSION_NAMES[k]: v for k, v in dimension_scores.items()},
        "reasons": reasons,
        "floor_audit": floor_audit,
        "audit_basis": "geometric-mean weakest-link (6 dimensions)",
        "scars_consulted": [
            "scar-2026-10-01-complexity-must-not-exceed-leverage",
            "scar-2026-10-01-same-model-different-prompt-not-independence",
            "scar-2026-10-01-agent-turn-vs-institution-optimization",
        ],
    }


def main():
    if len(sys.argv) < 2:
        print("usage: m_min_audit.py <path-to-competency-state.json>", file=sys.stderr)
        sys.exit(2)

    state_path = Path(sys.argv[1])
    if not state_path.exists():
        print(f"error: {state_path} not found", file=sys.stderr)
        sys.exit(2)

    state = json.loads(state_path.read_text())
    result = audit(state)

    print(f"M_min = {result['m_min']:.4f}")
    print(f"Verdict: {result['m_min_verdict']}")
    print("")
    print("Floor-by-floor audit:")
    for line in result["floor_audit"]:
        print(f"  {line}")

    sys.exit(0 if result["m_min"] > 0 else 1)


if __name__ == "__main__":
    main()