#!/usr/bin/env python3
"""Musyawawah Runtime Gate — REFERENCE IMPLEMENTATION (Path A, Phase 1)

F13 strategic judgment 2026-09-08:
  "AAA can prototype intent. arifOS should enforce only validated intent."
  "Reference first. Constitution later."

This is a STANDALONE Python module that demonstrates the musyawawah_reference
check. It is NOT yet wired into the arifOS kernel. The intent is to:

  1. Specify the contract (action_class + musyawawah_reference + override)
  2. Test the logic against real-world scenarios (Phase A3)
  3. Collect failure-mode evidence (Phase A4-A5)
  4. THEN propose integration into arifOS kernel (Path B)

Target integration point (deferred to Path B):
  /root/arifOS/arifosmcp/runtime/pre_execution_gate.py
  Line ~275 (action_class determination)

Constitutional: F1 AMANAH (fail-closed), F11 AUDIT (verdict logged),
                F13 SOVEREIGN (override pathway preserved).

DITEMPA BUKAN DIBERI — Phase A1, 2026-09-08 by FI-003 under F13 APEX Verdict.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# Pattern: musyawarah/YYYY-MM-DD-<topic>/<file>
# Example: musyawawah/2026-09-08-no-gate-task6/CONVERGENCE.md
MUSYAWARAH_REF_PATTERN = re.compile(
    r"^musyaw[a]?wah/\d{4}-\d{2}-\d{2}-[a-zA-Z0-9_-]+/[^/]+\.(md|jsonl|yaml)$"
)


class ActionClass(str, Enum):
    """Maps to arifOS authority tiers (per F13 autonomy doctrine).

    T0 = OBSERVE_ONLY/OBSERVE: read-only baseline.
    T1 = EXECUTE_REVERSIBLE: edit/test/commit, reversible.
    T2 = EXECUTE_HIGH_IMPACT: task-scoped grant, requires musyawawah.
    T3 = SEAL: irreversible, requires musyawawah + F13 authority.
    """
    OBSERVE_ONLY = "OBSERVE_ONLY"
    OBSERVE = "OBSERVE"
    EXECUTE_REVERSIBLE = "EXECUTE_REVERSIBLE"
    EXECUTE_HIGH_IMPACT = "EXECUTE_HIGH_IMPACT"
    SEAL = "SEAL"


class Verdict(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_BYPASS = "ALLOW_BYPASS"  # F13 sovereign override (logged)
    DENY = "DENY"


# Baseline affordances — no musyawawah needed (per CCC doctrine: T0/T1 = default)
BASELINE_ACTIONS: frozenset[ActionClass] = frozenset({
    ActionClass.OBSERVE_ONLY,
    ActionClass.OBSERVE,
    ActionClass.EXECUTE_REVERSIBLE,
})

# Restricted actions — task-scoped grant, require musyawawah_reference
RESTRICTED_ACTIONS: frozenset[ActionClass] = frozenset({
    ActionClass.EXECUTE_HIGH_IMPACT,
    ActionClass.SEAL,
})


@dataclass(frozen=True)
class InvocationContext:
    """Mock of the payload that arifOS pre_execution_gate.py would carry.

    In real integration (Path B), this would be derived from:
      - forge_* tool name + arguments
      - actor_id, session_id
      - requested action_class
      - payload.musyawawah_reference (from agent)
      - payload.ack_irreversible (F13 sovereign override flag)
    """
    action_class: ActionClass
    musyawawah_reference: Optional[str] = None   # e.g. "musyawawah/2026-09-08-task-xyz"
    ack_irreversible: bool = False               # F13 sovereign direct command
    actor_id: Optional[str] = None
    tool_name: Optional[str] = None               # which forge_* chokepoint
    payload_keys: Optional[tuple] = None         # all payload keys (for audit)


def verify_musyawawah_in_vault999(reference: str) -> bool:
    """Reference verification against VAULT999.

    Format: musyawawah/<YYYY-MM-DD>-<topic>/<file>.{md,jsonl,yaml}
    Example: musyawawah/2026-09-08-no-gate-task6/CONVERGENCE.md

    TODO(Path B): integrate with real arifOS VAULT999 lookup.
    Phase A: structural validation via regex only.
    """
    if not reference or not isinstance(reference, str):
        return False
    return bool(MUSYAWARAH_REF_PATTERN.match(reference))


def check_musyawawah_reference(ctx: InvocationContext) -> Verdict:
    """Reference implementation of the musyawawah_reference check.

    Decision tree:
      1. action_class in BASELINE_ACTIONS   -> ALLOW (no musyawawah needed)
      2. action_class in RESTRICTED_ACTIONS:
         a. ack_irreversible=True            -> ALLOW_BYPASS (F13 override, logged)
         b. musyawawah_reference absent      -> DENY (fail-closed)
         c. musyawawah_reference invalid     -> DENY (fail-closed)
         d. musyawawah_reference valid       -> ALLOW

    Per F13 strategic judgment: "Reference first. Constitution later."
    This function will be the contract reference for Path B kernel integration.
    """
    if ctx.action_class in BASELINE_ACTIONS:
        return Verdict.ALLOW

    # Restricted actions (T2/T3) - require musyawawah_reference
    if ctx.ack_irreversible:
        return Verdict.ALLOW_BYPASS

    if not ctx.musyawawah_reference:
        return Verdict.DENY

    if not verify_musyawawah_in_vault999(ctx.musyawawah_reference):
        return Verdict.DENY

    return Verdict.ALLOW


def check_with_log(ctx: InvocationContext) -> tuple:
    """Returns (verdict, reason) for audit log (F11 AUDIT compliance)."""
    verdict = check_musyawawah_reference(ctx)

    if ctx.action_class in BASELINE_ACTIONS:
        reason = f"baseline action {ctx.action_class.value}, no musyawawah required"
    elif verdict == Verdict.ALLOW_BYPASS:
        reason = f"F13 sovereign override (ack_irreversible=True) - bypass logged for {ctx.tool_name}"
    elif verdict == Verdict.ALLOW:
        reason = f"musyawawah_reference verified: {ctx.musyawawah_reference}"
    elif ctx.action_class in RESTRICTED_ACTIONS and not ctx.musyawawah_reference:
        reason = f"restricted action {ctx.action_class.value} WITHOUT musyawawah_reference - fail-closed DENY"
    elif not verify_musyawawah_in_vault999(ctx.musyawawah_reference or ""):
        reason = f"invalid musyawawah_reference format: {ctx.musyawawah_reference}"
    else:
        reason = "unknown denial path"

    return verdict, reason


if __name__ == "__main__":
    # Smoke test - exercise core paths
    print("Musyawawah Runtime Gate - reference implementation smoke test")
    print("=" * 60)
    cases = [
        ("T0 baseline", InvocationContext(action_class=ActionClass.OBSERVE_ONLY)),
        ("T1 baseline", InvocationContext(action_class=ActionClass.EXECUTE_REVERSIBLE)),
        ("T2 no ref", InvocationContext(action_class=ActionClass.EXECUTE_HIGH_IMPACT)),
        ("T2 with ref", InvocationContext(
            action_class=ActionClass.EXECUTE_HIGH_IMPACT,
            musyawawah_reference="musyawawah/2026-09-08-no-gate-task6/CONVERGENCE.md",
        )),
        ("T2 invalid ref", InvocationContext(
            action_class=ActionClass.EXECUTE_HIGH_IMPACT,
            musyawawah_reference="malicious-ref",
        )),
        ("T2 F13 override", InvocationContext(
            action_class=ActionClass.EXECUTE_HIGH_IMPACT,
            ack_irreversible=True,
        )),
        ("T3 SEAL no ref", InvocationContext(action_class=ActionClass.SEAL)),
        ("T3 SEAL with ref", InvocationContext(
            action_class=ActionClass.SEAL,
            musyawawah_reference="musyawawah/2026-09-08-no-gate-task6/CONVERGENCE.md",
        )),
    ]
    for label, ctx in cases:
        v, r = check_with_log(ctx)
        print(f"  [{v.value:14}] {label:25} {r}")
