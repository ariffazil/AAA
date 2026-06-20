"""
decision.py — Single Decision object shared across all 4 guards.

The Decision is the lingua franca of the arifOS kernel. Every guard returns
one, every tool wrapper consumes one, every audit seal records one. This
prevents governance drift across agents — no agent can invent its own
arifOS shape.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class CognitionLane(str, Enum):
    """
    What KIND of thinking is the agent doing right now?

    The kernel classifies intent into one of 4 lanes. Each lane has
    different floor checks and required authority.

    OBSERVE  — read-only. No state mutation. Lowest authority needed.
    PLAN     — reasoning, no side effects. Mid authority.
    MUTATE   — modifying local state. Higher authority + reversibility.
    EXECUTE  — cross-system action. Highest authority + lease required.
    """

    OBSERVE = "OBSERVE"
    PLAN = "PLAN"
    MUTATE = "MUTATE"
    EXECUTE = "EXECUTE"


class ActionClass(str, Enum):
    """
    What is the agent ABOUT TO DO?

    Used by pretool to classify the action before it executes.
    Maps to arifOS action_class taxonomy (L1-L13 floors, leases, etc.).
    """

    OBSERVE = "OBSERVE"
    COMPUTE = "COMPUTE"
    PROPOSE = "PROPOSE"
    MUTATE_LOCAL = "MUTATE_LOCAL"
    MUTATE_EXTERNAL = "MUTATE_EXTERNAL"
    DEPLOY = "DEPLOY"
    SPEND = "SPEND"
    PUBLISH = "PUBLISH"
    DELETE = "DELETE"
    SIGN = "SIGN"
    GRANT_ACCESS = "GRANT_ACCESS"
    CREDENTIAL_CHANGE = "CREDENTIAL_CHANGE"
    CONSTITUTION_CHANGE = "CONSTITUTION_CHANGE"


class FloorVerdict(BaseModel):
    """One floor's verdict for a given decision."""

    floor_id: str  # "F1", "F2", ..., "F13"
    verdict: Literal["PASS", "WARN", "FAIL", "HOLD"]
    reason: str
    evidence: dict[str, Any] = Field(default_factory=dict)


class RiskEnvelope(BaseModel):
    """Risk assessment for a decision."""

    blast_radius: Literal["NONE", "LOCAL", "SESSION", "FEDERATION", "EXTERNAL"] = "NONE"
    reversibility: Literal["REVERSIBLE", "PARTIAL", "IRREVERSIBLE"] = "REVERSIBLE"
    human_ack_required: bool = False
    estimated_tokens: int = 0
    estimated_time_seconds: int = 0


class Decision(BaseModel):
    """
    THE single decision object for the arifOS kernel.

    Every guard returns one. Every tool wrapper consumes one. Every audit
    seal records one. This is the lingua franca — agents cannot invent
    their own shape, cannot drift from the contract, cannot hide behind
    partial implementations.

    Verdict semantics:
        ALLOW     — proceed, decision is sealed
        DENY      — block, do not proceed
        HOLD      — pause, request human authority (F13 SOVEREIGN)
        DEGRADED  — proceed with warnings, attach to seal
    """

    verdict: Literal["ALLOW", "DENY", "HOLD", "DEGRADED"]
    cognition_lane: CognitionLane
    action_class: ActionClass | None = None
    lease_id: str | None = None
    floor_verdicts: list[FloorVerdict] = Field(default_factory=list)
    risk: RiskEnvelope = Field(default_factory=RiskEnvelope)
    required_human_ack: bool = False
    reasons: list[str] = Field(default_factory=list)
    next_safe_action: str | None = None
    seal_pointer: str | None = None  # VAULT999 entry id once sealed
    taint: Literal["UNTRUSTED", "TRUSTED", "VERIFIED"] = "UNTRUSTED"

    def is_permitted(self) -> bool:
        """True if the decision permits execution."""
        return self.verdict in ("ALLOW", "DEGRADED")

    def is_blocking(self) -> bool:
        """True if the decision blocks execution."""
        return self.verdict in ("DENY", "HOLD")

    def is_holding(self) -> bool:
        """True if the decision requires human authority (888 HOLD)."""
        return self.verdict == "HOLD" or self.required_human_ack

    def failed_floors(self) -> list[str]:
        """List of floors that failed (for diagnostics)."""
        return [f.floor_id for f in self.floor_verdicts if f.verdict == "FAIL"]

    def to_envelope(self) -> dict[str, Any]:
        """Serialise for transport across MCP / A2A boundaries."""
        return {
            "verdict": self.verdict,
            "cognition_lane": self.cognition_lane.value,
            "action_class": self.action_class.value if self.action_class else None,
            "lease_id": self.lease_id,
            "floor_verdicts": [f.model_dump() for f in self.floor_verdicts],
            "risk": self.risk.model_dump(),
            "required_human_ack": self.required_human_ack,
            "reasons": self.reasons,
            "next_safe_action": self.next_safe_action,
            "seal_pointer": self.seal_pointer,
            "taint": self.taint,
        }
