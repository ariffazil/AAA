"""AAA Constitutional Models — types for governance overlay.

Identity, verdicts, delegation, memory grades.
DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ── Authority Bands ──────────────────────────────────────────────────────


class AuthorityBand(str, Enum):
    """What an agent may do. Escalating risk."""

    OBSERVE = "observe"
    REASON = "reason"
    DRAFT = "draft"
    EXECUTE = "execute"
    MUTATE = "mutate"
    SEAL = "seal"


# ── Verdicts ─────────────────────────────────────────────────────────────


class Verdict(str, Enum):
    """Constitutional verdict from 888_JUDGE."""

    SEAL = "SEAL"
    HOLD = "HOLD"
    SABAR = "SABAR"
    VOID = "VOID"


# ── Memory Grades ────────────────────────────────────────────────────────


class MemoryGrade(str, Enum):
    """Evidence grading for memory/state."""

    L1_GROUND_TRUTH = "L1"  # Sealed, ratified, immutable
    L2_VERIFIED = "L2"  # Live tool/source checked
    L3_CACHED = "L3"  # Previously known, may be stale
    L4_INFERRED = "L4"  # Reasoning only, not truth


# ── Agent Identity ───────────────────────────────────────────────────────


class AgentIdentity(BaseModel):
    """Registered agent identity — bounded agency, not a cosmetic name."""

    agent_id: str
    principal: str = "unknown"  # Who it serves
    role: str = "observer"  # What it may do
    authority_band: AuthorityBand = AuthorityBand.OBSERVE
    tool_scope: list[str] = Field(default_factory=list)
    memory_scope: str = "session"  # session | organ | federation
    revocation_path: str = "arifos-judge"
    human_veto: bool = True  # F13 always applies


# ── Delegation Rule ──────────────────────────────────────────────────────


class DelegationRule(BaseModel):
    """A single cross-organ boundary rule."""

    source: str | None = None  # None = any source
    target_contains: str | None = None  # substring match on target skill/message
    verdict: str = "blocked"  # blocked | warned
    reason: str = ""
    floor: str | None = None  # Which F1-F13 floor is violated


# ── Constitutional Check Result ──────────────────────────────────────────


class FloorCheckResult(BaseModel):
    """Result of an F1-F13 floor check."""

    passed: bool
    floors_checked: list[str] = Field(default_factory=list)
    floors_violated: list[str] = Field(default_factory=list)
    verdict: Verdict = Verdict.SEAL
    rationale: str = ""
    confidence: float = 0.92


# ── Audit Record ─────────────────────────────────────────────────────────


class AuditRecord(BaseModel):
    """Record for VAULT999 receipt."""

    event: str
    agent_id: str
    task_id: str | None = None
    verdict: Verdict = Verdict.SEAL
    floors_checked: list[str] = Field(default_factory=list)
    floors_violated: list[str] = Field(default_factory=list)
    evidence: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = ""
    receipt_id: str | None = None
