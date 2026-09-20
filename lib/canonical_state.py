"""canonical_state.py — P1.0 Canonical State Envelope

The minimum sufficient vocabulary that every federation job must speak.

DITEMPA BUKAN DIBERI ⚒️

## Why this exists (2026-09-21 F13 directive)

> "You have less of a 'too many cron jobs' problem than a 'same words
> describing different realities' problem."

The federation has many jobs that share vocabulary — "drift", "reconciler",
"check", "probe" — but answer different questions. Before any consolidation
can be mechanical, every job must speak the SAME minimal state envelope so
that two jobs' outputs are comparable.

## The Invariants

- UNKNOWN != OK     — absence of evidence is not evidence of health
- HOLD != FAIL      — a held decision is not a failed system
- DRIFT != FAILURE  — drift is a state, not a breakdown
- EXECUTION_SUCCESS != OUTCOME_SUCCESS — process exit 0 ≠ outcome achieved

## Envelope Schema (every job emits one of these)

    {
      "fact_domain":   "<string>",          # e.g. "deployment", "registry", "tool-count", "routing"
      "observed_state": "<string>",          # e.g. "behind_origin_main", "cards_consistent"
      "expected_state": "<string>",          # canonical expected
      "health":        "HEALTHY|DEGRADED|FAILED|UNKNOWN",
      "convergence":   "SYNCED|INTENTIONAL_HOLD|DRIFT|UNKNOWN",
      "reason_code":   "<string>",           # e.g. "EVIDENCE_MISSING", "DIRTY_TREE", "QUOTA_EXHAUSTED"
      "evidence_ref":  "<string>",           # path or URL proving the claim
      "owner":         "<string>",           # who is responsible for acting
      "next_actor":    "<machine|human|hold>",
      "observed_at":   "<ISO-8601 UTC>",
      "job_id":        "<string>",           # who emitted this
      "job_class":     "ACTUATOR|DETECTOR|AUDITOR|WITNESS|LEARNING_LOOP|HEALTH_PROBE"
    }

## Classification (mutually exclusive — every job gets exactly one)

    ACTUATOR       — mutates state as a primary effect
    DETECTOR       — observes state, reports, never mutates
    AUDITOR        — observes, compares two sources, reports agreement/disagreement
    WITNESS        — records without judgment
    LEARNING_LOOP  — observes → proposes → verifies → promotes (capability metabolism)
    HEALTH_PROBE   — actively probes external endpoints and may flip routing state
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ── Enums (string constants, not magic) ───────────────────────────

HEALTH_HEALTHY   = "HEALTHY"
HEALTH_DEGRADED  = "DEGRADED"
HEALTH_FAILED    = "FAILED"
HEALTH_UNKNOWN   = "UNKNOWN"
_HEALTHS = {HEALTH_HEALTHY, HEALTH_DEGRADED, HEALTH_FAILED, HEALTH_UNKNOWN}

CONV_SYNCED      = "SYNCED"
CONV_HOLD        = "INTENTIONAL_HOLD"
CONV_DRIFT       = "DRIFT"
CONV_UNKNOWN     = "UNKNOWN"
_CONVS = {CONV_SYNCED, CONV_HOLD, CONV_DRIFT, CONV_UNKNOWN}

NEXT_MACHINE     = "machine"
NEXT_HUMAN       = "human"
NEXT_HOLD        = "hold"

CLASS_ACTUATOR        = "ACTUATOR"
CLASS_DETECTOR        = "DETECTOR"
CLASS_AUDITOR         = "AUDITOR"
CLASS_WITNESS         = "WITNESS"
CLASS_LEARNING_LOOP   = "LEARNING_LOOP"
CLASS_HEALTH_PROBE    = "HEALTH_PROBE"
_CLASSES = {
    CLASS_ACTUATOR, CLASS_DETECTOR, CLASS_AUDITOR,
    CLASS_WITNESS, CLASS_LEARNING_LOOP, CLASS_HEALTH_PROBE,
}


# ── Reasons (machine-readable codes) ───────────────────────────────

class Reason:
    EVIDENCE_MISSING       = "EVIDENCE_MISSING"
    DIRTY_TREE             = "DIRTY_TREE"
    GIT_AHEAD_OF_ORIGIN    = "GIT_AHEAD_OF_ORIGIN"
    GIT_BEHIND_ORIGIN      = "GIT_BEHIND_ORIGIN"
    KERNEL_REPORTS_DRIFT   = "KERNEL_REPORTS_DRIFT"
    CARD_MISSING           = "CARD_MISSING"
    FI_SLOT_CONFLICT       = "FI_SLOT_CONFLICT"
    TOOL_COUNT_MISMATCH    = "TOOL_COUNT_MISMATCH"
    PROVIDER_429           = "PROVIDER_429"
    PROVIDER_401           = "PROVIDER_401"
    PROVIDER_DEAD          = "PROVIDER_DEAD"
    NO_ATOMS_TO_PROMOTE    = "NO_ATOMS_TO_PROMOTE"
    VERIFICATION_REJECTED  = "VERIFICATION_REJECTED"
    DEPLOY_IN_PROGRESS     = "DEPLOY_IN_PROGRESS"
    OBSERVATION_OK         = "OBSERVATION_OK"
    RUNTIME_CODE_MISMATCH  = "RUNTIME_CODE_MISMATCH"
    CONTRACT_DRIFT         = "CONTRACT_DRIFT"
    VAULT_UNREACHABLE      = "VAULT_UNREACHABLE"
    ORGAN_REASON_MISSING   = "ORGAN_REASON_MISSING"


# ── Dataclass for the envelope ─────────────────────────────────────

@dataclass(frozen=True)
class CanonicalState:
    fact_domain: str
    observed_state: str
    expected_state: str
    health: str
    convergence: str
    reason_code: str
    evidence_ref: str
    owner: str
    next_actor: str
    job_id: str
    job_class: str
    observed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str = ""

    def __post_init__(self):
        # Enforce enum membership — fail loud, do not silently coerce.
        if self.health not in _HEALTHS:
            raise ValueError(f"health must be one of {_HEALTHS}, got {self.health!r}")
        if self.convergence not in _CONVS:
            raise ValueError(f"convergence must be one of {_CONVS}, got {self.convergence!r}")
        if self.job_class not in _CLASSES:
            raise ValueError(f"job_class must be one of {_CLASSES}, got {self.job_class!r}")
        if self.next_actor not in (NEXT_MACHINE, NEXT_HUMAN, NEXT_HOLD):
            raise ValueError(f"next_actor must be one of ({NEXT_MACHINE},{NEXT_HUMAN},{NEXT_HOLD}), got {self.next_actor!r}")
        # The four canonical invariants
        if self.health == HEALTH_UNKNOWN and self.convergence == CONV_SYNCED:
            raise ValueError("UNKNOWN != OK: an UNKNOWN health cannot claim SYNCED convergence")
        if self.convergence == CONV_HOLD and self.health == HEALTH_FAILED:
            raise ValueError("HOLD != FAIL: an INTENTIONAL_HOLD is not a FAILED")
        if self.convergence == CONV_DRIFT and self.health == HEALTH_FAILED:
            raise ValueError("DRIFT != FAILURE: drift is a state, not a breakdown")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


# ── Emit helper ────────────────────────────────────────────────────

def vitality_from_kernel_payload(
    payload: dict[str, Any] | None,
    *,
    local_ahead_of_origin: bool | None = None,
) -> CanonicalState:
    """Map a live arifOS /health JSON onto HEALTH × CONVERGENCE.

    Does not mutate the kernel. UNKNOWN if the payload cannot be read.
    Unpushed source with built==deployed and process serving is
    HEALTHY + INTENTIONAL_HOLD, not FAILED.
    """
    if not payload:
        return CanonicalState(
            fact_domain="kernel-health",
            observed_state="no payload",
            expected_state="reachable /health JSON",
            health=HEALTH_UNKNOWN,
            convergence=CONV_UNKNOWN,
            reason_code=Reason.EVIDENCE_MISSING,
            evidence_ref="curl :8088/health",
            owner="arifos",
            next_actor=NEXT_MACHINE,
            job_id="vitality-kernel",
            job_class=CLASS_DETECTOR,
        )

    sr = payload.get("software_release") or {}
    layer = payload.get("layer_health") or {}
    runtime_layer = layer.get("runtime") or {}
    constitutional = layer.get("constitutional") or {}
    vault = constitutional.get("vault999") or payload.get("vault999_health")
    code_runtime_drift = bool(runtime_layer.get("runtime_matches_build") is False)
    # Prefer explicit runtime_drift over the collapsed status field.
    if payload.get("runtime_drift") is True:
        code_runtime_drift = True
    sr_drift = bool(sr.get("drift") is True or payload.get("software_release", {}).get("drift") is True)
    contract_drift = bool(payload.get("contract_drift") is True)
    built = str(sr.get("built_commit") or "")
    deployed = str(sr.get("deployed_commit") or "")
    source = str(sr.get("source_commit") or "")
    built_eq_deployed = bool(built and deployed and built == deployed)
    floors_ok = (constitutional.get("status") == "healthy")

    if code_runtime_drift:
        health, conv, reason = HEALTH_DEGRADED, CONV_DRIFT, Reason.RUNTIME_CODE_MISMATCH
        observed = "live process does not match deployed commit"
    elif not floors_ok and constitutional:
        health, conv, reason = HEALTH_DEGRADED, CONV_DRIFT, Reason.KERNEL_REPORTS_DRIFT
        observed = f"constitutional={constitutional.get('status')}"
    elif vault and vault not in ("healthy", "HEALTHY"):
        health, conv, reason = HEALTH_DEGRADED, CONV_UNKNOWN, Reason.VAULT_UNREACHABLE
        observed = f"vault999={vault}"
    elif sr_drift and built_eq_deployed:
        # Source tree moved; running artifact still matches its build.
        ahead = local_ahead_of_origin
        if ahead is True or (source and built and source != built):
            health, conv, reason = HEALTH_HEALTHY, CONV_HOLD, Reason.GIT_AHEAD_OF_ORIGIN
            observed = f"source={source[:12]} built={built[:12]} deployed={deployed[:12]} (unpushed or unbuilt source)"
        else:
            health, conv, reason = HEALTH_HEALTHY, CONV_DRIFT, Reason.KERNEL_REPORTS_DRIFT
            observed = f"software_release.drift=true source={source[:12]} built={built[:12]}"
    elif contract_drift:
        health, conv, reason = HEALTH_DEGRADED, CONV_DRIFT, Reason.CONTRACT_DRIFT
        observed = "contract_drift=true"
    elif payload.get("status") == "degraded":
        # Collapsed status without a classifiable reason — do not upgrade to OK.
        reasons = payload.get("degraded_reasons") or []
        if not reasons:
            health, conv, reason = HEALTH_UNKNOWN, CONV_UNKNOWN, Reason.ORGAN_REASON_MISSING
            observed = "status=degraded and degraded_reasons empty"
        elif sr_drift:
            health, conv, reason = HEALTH_HEALTHY, CONV_HOLD, Reason.GIT_AHEAD_OF_ORIGIN
            observed = "status=degraded from software_release.drift only"
        else:
            health, conv, reason = HEALTH_DEGRADED, CONV_DRIFT, Reason.KERNEL_REPORTS_DRIFT
            observed = f"status=degraded reasons={len(reasons)}"
    else:
        health, conv, reason = HEALTH_HEALTHY, CONV_SYNCED, Reason.OBSERVATION_OK
        observed = f"status={payload.get('status')} service_health={payload.get('service_health')}"

    return CanonicalState(
        fact_domain="kernel-health",
        observed_state=observed,
        expected_state="HEALTHY + SYNCED, or HEALTHY + INTENTIONAL_HOLD when source is held",
        health=health,
        convergence=conv,
        reason_code=reason,
        evidence_ref="GET http://127.0.0.1:8088/health",
        owner="arifos",
        next_actor=NEXT_MACHINE,
        job_id="vitality-kernel",
        job_class=CLASS_DETECTOR,
        notes=f"collapsed_status={payload.get('status')}",
    )


def vitality_from_organ_payload(
    organ: str,
    payload: dict[str, Any] | None,
    *,
    evidence_ref: str,
) -> CanonicalState:
    """Classify WELL/GEOX/FRAME-style /health without inventing reasons."""
    if not payload:
        return CanonicalState(
            fact_domain=f"{organ}-health",
            observed_state="no payload",
            expected_state="reachable /health JSON",
            health=HEALTH_UNKNOWN,
            convergence=CONV_UNKNOWN,
            reason_code=Reason.EVIDENCE_MISSING,
            evidence_ref=evidence_ref,
            owner=organ,
            next_actor=NEXT_MACHINE,
            job_id=f"vitality-{organ}",
            job_class=CLASS_DETECTOR,
        )

    status = str(payload.get("status") or "")
    drift = payload.get("drift")
    dep = payload.get("deployment_drift")
    if isinstance(dep, dict):
        drift = dep.get("drift") if drift is None else drift
    reasons = payload.get("degraded_reasons")

    if status in ("ok", "healthy", "aligned", "ok-v3-vector"):
        health = HEALTH_HEALTHY
        conv = CONV_DRIFT if drift is True else CONV_SYNCED
        reason = Reason.KERNEL_REPORTS_DRIFT if drift is True else Reason.OBSERVATION_OK
        observed = f"status={status} drift={drift}"
    elif status == "degraded":
        if reasons in (None, [], ""):
            # Organ cannot say why — that is UNKNOWN, not FAIL.
            if drift is True:
                health, conv, reason = HEALTH_HEALTHY, CONV_DRIFT, Reason.ORGAN_REASON_MISSING
                observed = "status=degraded drift=true degraded_reasons=null"
            else:
                health, conv, reason = HEALTH_UNKNOWN, CONV_UNKNOWN, Reason.ORGAN_REASON_MISSING
                observed = "status=degraded degraded_reasons=null"
        else:
            health, conv, reason = HEALTH_DEGRADED, CONV_DRIFT, Reason.KERNEL_REPORTS_DRIFT
            observed = f"status=degraded reasons={reasons!r}"[:200]
    elif status in ("fail", "failed", "down"):
        health, conv, reason = HEALTH_FAILED, CONV_UNKNOWN, Reason.PROVIDER_DEAD
        observed = f"status={status}"
    else:
        health, conv, reason = HEALTH_UNKNOWN, CONV_UNKNOWN, Reason.EVIDENCE_MISSING
        observed = f"status={status!r}"

    return CanonicalState(
        fact_domain=f"{organ}-health",
        observed_state=observed,
        expected_state="HEALTHY + (SYNCED|INTENTIONAL_HOLD|DRIFT) with a reason",
        health=health,
        convergence=conv,
        reason_code=reason,
        evidence_ref=evidence_ref,
        owner=organ,
        next_actor=NEXT_MACHINE,
        job_id=f"vitality-{organ}",
        job_class=CLASS_DETECTOR,
        notes=f"collapsed_status={status}",
    )


def emit(state: CanonicalState, sink: str | os.PathLike | None = None) -> None:
    """Print envelope as JSON to stdout; optionally append to sink file."""
    payload = state.to_json()
    print(payload)
    if sink:
        p = Path(sink)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a") as f:
            f.write(payload + "\n")


# ── Self-test (run when invoked as main) ──────────────────────────

def _self_test() -> int:
    """Enforce the four invariants at construction time."""
    failures = 0

    # Case 1: UNKNOWN + SYNCED → must raise
    try:
        CanonicalState(
            fact_domain="test", observed_state="x", expected_state="x",
            health=HEALTH_UNKNOWN, convergence=CONV_SYNCED,
            reason_code=Reason.OBSERVATION_OK, evidence_ref="self_test",
            owner="test", next_actor=NEXT_MACHINE, job_id="test", job_class=CLASS_DETECTOR,
        )
        print("FAIL: UNKNOWN + SYNCED did not raise")
        failures += 1
    except ValueError as e:
        print(f"OK : UNKNOWN != OK — rejected: {e}")

    # Case 2: HOLD + FAILED → must raise
    try:
        CanonicalState(
            fact_domain="test", observed_state="x", expected_state="x",
            health=HEALTH_FAILED, convergence=CONV_HOLD,
            reason_code=Reason.OBSERVATION_OK, evidence_ref="self_test",
            owner="test", next_actor=NEXT_MACHINE, job_id="test", job_class=CLASS_DETECTOR,
        )
        print("FAIL: HOLD + FAILED did not raise")
        failures += 1
    except ValueError as e:
        print(f"OK : HOLD != FAIL — rejected: {e}")

    # Case 3: DRIFT + FAILED → must raise
    try:
        CanonicalState(
            fact_domain="test", observed_state="x", expected_state="x",
            health=HEALTH_FAILED, convergence=CONV_DRIFT,
            reason_code=Reason.OBSERVATION_OK, evidence_ref="self_test",
            owner="test", next_actor=NEXT_MACHINE, job_id="test", job_class=CLASS_DETECTOR,
        )
        print("FAIL: DRIFT + FAILED did not raise")
        failures += 1
    except ValueError as e:
        print(f"OK : DRIFT != FAILURE — rejected: {e}")

    # Case 4: valid case → must NOT raise
    try:
        s = CanonicalState(
            fact_domain="deployment",
            observed_state="source=3fae5b3 built=5a294a4 deployed=5a294a4 drift=true",
            expected_state="source==built==deployed drift=false",
            health=HEALTH_DEGRADED,
            convergence=CONV_DRIFT,
            reason_code=Reason.KERNEL_REPORTS_DRIFT,
            evidence_ref="curl :8088/health -> software_release.drift=true",
            owner="arifos-deploy-reconciler",
            next_actor=NEXT_MACHINE,
            job_id="arifos-drift-check",
            job_class=CLASS_DETECTOR,
        )
        print(f"OK : valid envelope accepted: health={s.health}, convergence={s.convergence}")
    except ValueError as e:
        print(f"FAIL: valid envelope rejected: {e}")
        failures += 1

    # Case 5: HEALTHY + SYNCED → must NOT raise
    try:
        s = CanonicalState(
            fact_domain="tool-count",
            observed_state="arifOS MCP /health reports 8 tools",
            expected_state="CAPABILITY_INDEX.json reports 8 tools",
            health=HEALTH_HEALTHY,
            convergence=CONV_SYNCED,
            reason_code=Reason.OBSERVATION_OK,
            evidence_ref="curl :8088/health + /root/AAA/registries/CAPABILITY_INDEX.json",
            owner="arifos-federation-audit",
            next_actor=NEXT_MACHINE,
            job_id="arifos-federation-audit",
            job_class=CLASS_AUDITOR,
        )
        print(f"OK : HEALTHY+SYNCED accepted")
    except ValueError as e:
        print(f"FAIL: HEALTHY+SYNCED rejected: {e}")
        failures += 1

    # Case 6: HEALTHY + INTENTIONAL_HOLD (unpushed source, process serving)
    try:
        s = CanonicalState(
            fact_domain="deployment",
            observed_state="source ahead of origin; built==deployed; process serving",
            expected_state="source==built==deployed OR explicit HOLD",
            health=HEALTH_HEALTHY,
            convergence=CONV_HOLD,
            reason_code=Reason.GIT_AHEAD_OF_ORIGIN,
            evidence_ref="self_test",
            owner="arifos-deploy-reconciler",
            next_actor=NEXT_MACHINE,
            job_id="test-hold",
            job_class=CLASS_ACTUATOR,
        )
        print(f"OK : HEALTHY+INTENTIONAL_HOLD accepted: health={s.health}, convergence={s.convergence}")
    except ValueError as e:
        print(f"FAIL: HEALTHY+INTENTIONAL_HOLD rejected: {e}")
        failures += 1

    return failures


if __name__ == "__main__":
    sys.exit(_self_test())
