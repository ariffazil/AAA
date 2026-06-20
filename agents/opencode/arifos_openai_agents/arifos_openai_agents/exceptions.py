"""
exceptions.py — Kernel exceptions for the 4 guards.

These are the ONLY exceptions an arifOS-wrapped agent can raise for
governance reasons. They map directly to Decision verdicts.
"""

from __future__ import annotations

from arifos_openai_agents.decision import Decision


class ArifGovernanceError(Exception):
    """Base class for all arifOS governance exceptions."""

    def __init__(self, message: str, decision: Decision):
        super().__init__(message)
        self.decision = decision


class ArifHold(ArifGovernanceError):
    """
    Raised when a decision is HOLD — agent must pause for human authority.

    Maps to F13 SOVEREIGN. The OpenAI Agents SDK will surface this to
    the human-in-the-loop mechanism.
    """

    def __init__(self, decision: Decision):
        super().__init__(
            f"888 HOLD: {decision.verdict} — "
            f"{decision.reasons[0] if decision.reasons else 'no reason given'}",
            decision,
        )


class ArifDenied(ArifGovernanceError):
    """
    Raised when a decision is DENY — agent must not proceed.

    Maps to a floor failure. The agent should treat this as a hard stop,
    not a recoverable error.
    """

    def __init__(self, decision: Decision):
        super().__init__(
            f"DENY: {decision.reasons[0] if decision.reasons else 'no reason given'}",
            decision,
        )


class ArifSealMissing(ArifGovernanceError):
    """
    Raised when an agent returns a result without a proper seal.

    Maps to F11 AUDIT. The result is untrusted without a VAULT999 seal.
    """

    def __init__(self, decision: Decision):
        super().__init__(
            "F11: result has no seal_pointer — cannot trust unsealed output",
            decision,
        )
