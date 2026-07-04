"""Verdict Routing — 888_JUDGE constitutional verdicts.

Routes floor check results to A2A wire format.
Maps: SEAL→COMPLETED, HOLD→INPUT_REQUIRED, VOID→REJECTED.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

from aaa_a2a.models import Verdict

# ── Constitutional → A2A Wire Format ─────────────────────────────────────

VERDICT_TO_A2A_STATE: dict[str, str] = {
    Verdict.SEAL: "TASK_STATE_COMPLETED",
    Verdict.HOLD: "TASK_STATE_INPUT_REQUIRED",
    Verdict.SABAR: "TASK_STATE_INPUT_REQUIRED",
    Verdict.VOID: "TASK_STATE_REJECTED",
}


def verdict_to_a2a_state(verdict: Verdict | str) -> str:
    """Convert constitutional verdict to A2A wire format state."""
    if isinstance(verdict, str):
        try:
            verdict = Verdict(verdict)
        except ValueError:
            return "TASK_STATE_SUBMITTED"
    return VERDICT_TO_A2A_STATE.get(verdict, "TASK_STATE_SUBMITTED")


def verdict_requires_human(verdict: Verdict | str) -> bool:
    """Check if verdict requires human review (HOLD/SABAR)."""
    if isinstance(verdict, str):
        try:
            verdict = Verdict(verdict)
        except ValueError:
            return False
    return verdict in (Verdict.HOLD, Verdict.SABAR)


def verdict_is_terminal(verdict: Verdict | str) -> bool:
    """Check if verdict is terminal (SEAL/VOID)."""
    if isinstance(verdict, str):
        try:
            verdict = Verdict(verdict)
        except ValueError:
            return False
    return verdict in (Verdict.SEAL, Verdict.VOID)
