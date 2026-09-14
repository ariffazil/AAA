#!/usr/bin/env python3
"""
decision_schema.py — Canonical Agentic Hook Decision Envelope (aaa.hook-decision.v1)

Canonical Path: /root/AAA/hooks/lib/decision_schema.py
Authority: AAA-HOOK-FORGE-V1.0 · §6.2 canonical decision envelope, §I3 monotonicity.

PURPOSE
-------
A hook emits exactly one constrained decision object. Free-form model prose is
NEVER authorization. The verdict vocabulary comes from exactly one place —
``event_schema.VERDICT_LADDER`` — so no competing ladder can drift into being.

This module also owns the monotonic composition law:

    compose(a, b) -> the STRONGER of the two restrictions

which is what makes "a downstream hook may never weaken an upstream
restriction" mechanically checkable rather than merely documented.

Zero external dependencies — Python standard library only.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

from event_schema import (  # single source of truth — do not redefine
    LEGACY_VERDICT_ALIASES,
    RISK_CLASSES,
    VERDICT_LADDER,
    VERDICT_RANK,
    canonical_json,
    new_id,
    sha256_hex,
    utc_now_iso,
)

DECISION_SCHEMA_VERSION = "aaa.hook-decision.v1"

DEFAULT_POLICY_BUNDLE_ID = "AAA-HOOK-POLICY-V1"
DEFAULT_TTL_SECONDS = 300
MAX_TTL_SECONDS = 3_600
MAX_REASON_CODES = 32
MAX_CONSTRAINT_TARGETS = 64

RFC3339_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|\+00:00)$")

# ---------------------------------------------------------------------------
# Default authority by risk class (§4). This is the *pre-policy* default; the
# policy engine may strengthen it, never weaken it below this floor.
# ---------------------------------------------------------------------------
RISK_DEFAULT_VERDICT: Dict[str, str] = {
    "R0": "ALLOW",
    "R1": "ALLOW",
    "R2": "ALLOW_WITH_CONSTRAINTS",
    "R3": "HOLD",
    "R4": "DENY",
}

# Risk classes that may never be resolved to ALLOW by an automated gate.
NON_AUTO_ALLOW_RISKS: frozenset = frozenset({"R3", "R4"})

# Reason codes that indicate a hard restriction that only an authenticated
# human override may relax (§I3).
SOVEREIGN_GATED_REASON_CODES: frozenset = frozenset({
    "F13_SOVEREIGN_BOUNDARY",
    "FORBIDDEN_TARGET",
    "SECRET_MATERIAL",
    "CONSTITUTIONAL_POLICY_CHANGE",
    "PRODUCTION_EFFECT",
    "EXTERNAL_COMMUNICATION",
    "IDENTITY_CHANGE",
    "CREDENTIAL_CHANGE",
    "DESTRUCTIVE_OPERATION",
    "EVIDENCE_DESTRUCTION",
    "PERMISSION_WIDENING",
    "UNBOUNDED_RECURSION",
    "POLICY_INTEGRITY_FAILURE",
})

TOP_LEVEL_ALLOWED: frozenset = frozenset({
    "schema_version",
    "event_id",
    "decision_id",
    "verdict",
    "reason_codes",
    "constraints",
    "mutated_action",
    "evidence_refs",
    "policy_bundle_id",
    "expires_at",
    "decided_at",
    "authority_floor",
})

CONSTRAINTS_ALLOWED: frozenset = frozenset({
    "max_retries",
    "timeout_ms",
    "allowed_targets",
    "rollback_required",
})


# ---------------------------------------------------------------------------
# Ladder primitives (§I3)
# ---------------------------------------------------------------------------

def normalize_verdict(verdict: Any) -> Optional[str]:
    """Coerce legacy/native vocabulary onto the canonical ladder.

    Returns None if the value is not a recognised verdict. Never invents
    a verdict from free text.
    """
    if isinstance(verdict, dict):
        verdict = verdict.get("verdict")
    elif hasattr(verdict, "verdict"):
        verdict = getattr(verdict, "verdict")
    if not isinstance(verdict, str):
        return None
    name = verdict.strip().upper().replace("-", "_").replace(" ", "_")
    if name in VERDICT_RANK:
        return name
    if name in LEGACY_VERDICT_ALIASES:
        return LEGACY_VERDICT_ALIASES[name]
    return None


def verdict_rank(verdict: Any) -> Optional[int]:
    v = normalize_verdict(verdict)
    return None if v is None else VERDICT_RANK[v]


def is_at_least(verdict: Any, floor: Any) -> bool:
    """True when ``verdict`` is at least as restrictive as ``floor``."""
    vr, fr = verdict_rank(verdict), verdict_rank(floor)
    if vr is None or fr is None:
        # Unknown restriction is treated as maximally restrictive — safe default.
        return False
    return vr >= fr


def is_restrictive(verdict: Any) -> bool:
    """True when the verdict blocks or defers the proposed action."""
    r = verdict_rank(verdict)
    return r is not None and r >= VERDICT_RANK["DEFER"]


def is_blocking(verdict: Any) -> bool:
    """True when the proposed action must not execute."""
    r = verdict_rank(verdict)
    return r is not None and r >= VERDICT_RANK["HOLD"]


def most_restrictive(*verdicts: Any) -> str:
    """Return the strongest restriction among the arguments.

    This is the monotonic composition law (§I3). Unknown values are ignored
    only when at least one known verdict exists; if nothing is known, the
    safe default is HOLD.
    """
    best: Optional[str] = None
    best_rank = -1
    for v in verdicts:
        r = verdict_rank(v)
        if r is None:
            continue
        if r > best_rank:
            best, best_rank = normalize_verdict(v), r
    return best if best is not None else "HOLD"


def compose_chain(verdicts: Iterable[Any]) -> str:
    """Fold a chain of decisions into the single governing restriction."""
    return most_restrictive(*list(verdicts))


def default_verdict_for_risk(risk_class: Any) -> str:
    if not isinstance(risk_class, str):
        return "HOLD"
    return RISK_DEFAULT_VERDICT.get(risk_class.strip().upper(), "HOLD")


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def build_constraints(
    *,
    max_retries: int = 0,
    timeout_ms: int = 0,
    allowed_targets: Optional[List[str]] = None,
    rollback_required: bool = False,
) -> Dict[str, Any]:
    return {
        "max_retries": max(0, int(max_retries)),
        "timeout_ms": max(0, int(timeout_ms)),
        "allowed_targets": list(allowed_targets or [])[:MAX_CONSTRAINT_TARGETS],
        "rollback_required": bool(rollback_required),
    }


def make_decision(
    *,
    event_id: str,
    verdict: str,
    reason_codes: Optional[List[str]] = None,
    constraints: Optional[Dict[str, Any]] = None,
    mutated_action: Optional[Dict[str, Any]] = None,
    evidence_refs: Optional[List[str]] = None,
    policy_bundle_id: str = DEFAULT_POLICY_BUNDLE_ID,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
    authority_floor: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a canonical decision envelope.

    Raises ValueError on an unrecognised verdict — a decision without a
    ladder-membership verdict is not a decision.
    """
    canon = normalize_verdict(verdict)
    if canon is None:
        raise ValueError(f"verdict not on canonical ladder: {verdict!r}")

    ttl = max(1, min(int(ttl_seconds), MAX_TTL_SECONDS))
    expires = (
        datetime.now(timezone.utc) + timedelta(seconds=ttl)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    decision: Dict[str, Any] = {
        "schema_version": DECISION_SCHEMA_VERSION,
        "event_id": event_id,
        "decision_id": new_id(),
        "verdict": canon,
        "reason_codes": list(dict.fromkeys(reason_codes or []))[:MAX_REASON_CODES],
        "constraints": constraints or build_constraints(),
        "mutated_action": mutated_action,
        "evidence_refs": list(evidence_refs or [])[:256],
        "policy_bundle_id": policy_bundle_id,
        "expires_at": expires,
        "decided_at": utc_now_iso(),
    }
    if authority_floor is not None:
        decision["authority_floor"] = normalize_verdict(authority_floor) or "HOLD"
    return decision


def decision_digest(decision: Dict[str, Any]) -> str:
    return sha256_hex(decision)


# ---------------------------------------------------------------------------
# Expiry
# ---------------------------------------------------------------------------

def is_expired(decision: Dict[str, Any], now: Optional[datetime] = None) -> bool:
    exp = decision.get("expires_at")
    if not isinstance(exp, str) or not RFC3339_UTC_RE.match(exp):
        return True  # unparseable expiry is treated as expired (fail-closed)
    try:
        parsed = datetime.strptime(exp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        try:
            parsed = datetime.fromisoformat(exp.replace("Z", "+00:00"))
        except ValueError:
            return True
    return (now or datetime.now(timezone.utc)) >= parsed


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _err(errors: List[str], msg: str) -> None:
    errors.append(msg)


def validate_decision(decision: Any) -> Tuple[bool, List[str]]:
    """Validate a canonical decision envelope (§6.2).

    Returns (ok, errors). Never raises on malformed input.
    """
    errors: List[str] = []

    if not isinstance(decision, dict):
        return False, ["decision must be a JSON object"]

    for key in decision:
        if key not in TOP_LEVEL_ALLOWED:
            _err(errors, f"unknown top-level field: {key}")

    for req in ("schema_version", "event_id", "decision_id", "verdict",
                "reason_codes", "constraints", "policy_bundle_id", "expires_at"):
        if req not in decision:
            _err(errors, f"missing required field: {req}")

    if errors and "verdict" not in decision:
        return False, errors

    if decision.get("schema_version") != DECISION_SCHEMA_VERSION:
        _err(errors,
             f"schema_version must be {DECISION_SCHEMA_VERSION!r}, "
             f"got {decision.get('schema_version')!r}")

    for fld in ("event_id", "decision_id"):
        v = decision.get(fld)
        if not isinstance(v, str) or not v.strip():
            _err(errors, f"{fld} must be a non-empty string")

    verdict = decision.get("verdict")
    canon = normalize_verdict(verdict)
    if canon is None:
        _err(errors,
             f"verdict not on canonical ladder {VERDICT_LADDER}: {verdict!r} "
             "(free-form prose is not authorization)")
    elif canon != verdict:
        _err(errors, f"verdict must be canonical form {canon!r}, got {verdict!r}")

    rc = decision.get("reason_codes")
    if not isinstance(rc, list):
        _err(errors, "reason_codes must be a list")
    else:
        if len(rc) > MAX_REASON_CODES:
            _err(errors, f"reason_codes exceeds {MAX_REASON_CODES}")
        for item in rc:
            if not isinstance(item, str) or not item.strip():
                _err(errors, "reason_codes entries must be non-empty strings")

    cons = decision.get("constraints")
    if not isinstance(cons, dict):
        _err(errors, "constraints must be an object")
    else:
        for k in cons:
            if k not in CONSTRAINTS_ALLOWED:
                _err(errors, f"unknown constraints field: {k}")
        for intf in ("max_retries", "timeout_ms"):
            if intf in cons and not isinstance(cons[intf], int):
                _err(errors, f"constraints.{intf} must be an integer")
            if isinstance(cons.get(intf), int) and cons[intf] < 0:
                _err(errors, f"constraints.{intf} must be >= 0")
        if "allowed_targets" in cons and not isinstance(cons["allowed_targets"], list):
            _err(errors, "constraints.allowed_targets must be a list")
        if "rollback_required" in cons and not isinstance(cons["rollback_required"], bool):
            _err(errors, "constraints.rollback_required must be a boolean")

    ma = decision.get("mutated_action")
    if ma is not None and not isinstance(ma, dict):
        _err(errors, "mutated_action must be an object or null")

    er = decision.get("evidence_refs")
    if er is not None:
        if not isinstance(er, list):
            _err(errors, "evidence_refs must be a list")
        elif len(er) > 256:
            _err(errors, "evidence_refs exceeds 256 entries")

    pbid = decision.get("policy_bundle_id")
    if not isinstance(pbid, str) or not pbid.strip():
        _err(errors, "policy_bundle_id must be a non-empty string")

    exp = decision.get("expires_at")
    if not isinstance(exp, str) or not RFC3339_UTC_RE.match(exp):
        _err(errors, "expires_at must be RFC3339 UTC")

    af = decision.get("authority_floor")
    if af is not None:
        if normalize_verdict(af) is None:
            _err(errors, f"authority_floor not on canonical ladder: {af!r}")
        elif is_blocking(verdict) and not is_at_least(af, verdict):
            # The floor must never be weaker than the assertion it floors.
            _err(errors, "authority_floor is weaker than verdict (monotonicity breach)")

    return (len(errors) == 0), errors


def is_valid_decision(decision: Any) -> bool:
    ok, _ = validate_decision(decision)
    return ok


def requires_sovereign(decision: Dict[str, Any]) -> bool:
    """True when only an authenticated human override may relax this decision."""
    if is_blocking(decision.get("verdict")):
        return True
    return any(c in SOVEREIGN_GATED_REASON_CODES
               for c in (decision.get("reason_codes") or []))


from dataclasses import dataclass, field


@dataclass
class HookDecision:
    event_id: str
    verdict: str
    reason_codes: List[str] = field(default_factory=list)
    risk_class: str = "R1"
    constitutional_floors: List[str] = field(default_factory=lambda: ["F1", "F4"])
    message: str = ""
    timestamp: str = field(default_factory=utc_now_iso)
    policy_bundle_id: str = DEFAULT_POLICY_BUNDLE_ID

    def __post_init__(self):
        norm = normalize_verdict(self.verdict)
        if norm is None:
            raise ValueError(f"Invalid verdict: {self.verdict}")
        self.verdict = norm


def compose_decisions(a: HookDecision, b: HookDecision) -> HookDecision:
    v = most_restrictive(a.verdict, b.verdict)
    combined_floors = list(dict.fromkeys(a.constitutional_floors + b.constitutional_floors))
    combined_reasons = list(dict.fromkeys(a.reason_codes + b.reason_codes))
    return HookDecision(
        event_id=a.event_id,
        verdict=v,
        reason_codes=combined_reasons,
        risk_class=a.risk_class if a.risk_class >= b.risk_class else b.risk_class,
        constitutional_floors=combined_floors,
        message=f"{a.message}; {b.message}".strip("; "),
    )


__all__ = [
    "DECISION_SCHEMA_VERSION",
    "DEFAULT_POLICY_BUNDLE_ID",
    "DEFAULT_TTL_SECONDS",
    "MAX_TTL_SECONDS",
    "RISK_DEFAULT_VERDICT",
    "NON_AUTO_ALLOW_RISKS",
    "SOVEREIGN_GATED_REASON_CODES",
    "normalize_verdict",
    "verdict_rank",
    "is_at_least",
    "is_restrictive",
    "is_blocking",
    "most_restrictive",
    "compose_chain",
    "default_verdict_for_risk",
    "build_constraints",
    "make_decision",
    "decision_digest",
    "is_expired",
    "validate_decision",
    "is_valid_decision",
    "requires_sovereign",
    "HookDecision",
    "compose_decisions",
]

