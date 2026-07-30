"""
Mission Router Schemas — Pydantic contracts for the governed orchestration engine.

Six stable mission states. No seventh. Ambiguous → HOLD_FOR_INTENT.
"""

from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class MissionState(str, Enum):
    """Stable machine identifiers beneath human phrases. SIX ONLY."""
    OBSERVE = "OBSERVE"    # "What is happening?"
    EXPLAIN = "EXPLAIN"    # "Why did this happen?"
    DECIDE = "DECIDE"      # "Should we do X?"
    ACT = "ACT"            # "Execute the plan"
    MONITOR = "MONITOR"    # "Watch this for me"
    RECALL = "RECALL"      # "What did we decide?"


class RiskClass(str, Enum):
    C1 = "C1"  # Read-only, no external effects
    C2 = "C2"  # Read-only, external API calls
    C3 = "C3"  # Advisory with consequence modeling
    C4 = "C4"  # Reversible mutation under judgment
    C5 = "C5"  # Irreversible action — requires sovereign


class OrganName(str, Enum):
    ARIFOS = "arifOS"
    AFORGE = "A-FORGE"
    GEOX = "GEOX"
    WEALTH = "WEALTH"
    WELL = "WELL"
    VAULT999 = "VAULT999"


class ExecutionMode(str, Enum):
    READ_ONLY = "read_only"
    ADVISORY = "advisory"
    DRY_RUN = "dry_run"
    MUTATE = "mutate"
    SEAL = "seal"


class CapabilityRef(BaseModel):
    """A semantic capability — what needs to be done, not which tool does it."""
    capability: str = Field(..., description="Semantic capability name, e.g. 'prospect_evaluation'")
    organ: OrganName
    mode: ExecutionMode = ExecutionMode.READ_ONLY
    required_evidence: list[str] = Field(default_factory=list)
    reason: str = Field("", description="Why this capability was selected")


class PipelineStage(BaseModel):
    """One stage in the execution graph."""
    step: int
    organ: OrganName
    capability: str
    mode: ExecutionMode
    resolved_tool: Optional[str] = Field(None, description="Resolved from registry spine at build time")
    resolved_tool_healthy: Optional[bool] = Field(None)
    input_requirements: list[str] = Field(default_factory=list)
    output_evidence: list[str] = Field(default_factory=list)
    depends_on: list[int] = Field(default_factory=list)
    selection_reason: str = ""
    fallback_tool: Optional[str] = Field(None)
    fallback_healthy: Optional[bool] = Field(None)


class RouterInput(BaseModel):
    """P0 router contract — what the human or upstream agent provides."""
    intent: str = Field(..., description="Human intent in natural language")
    actor_id: str = Field(default="anonymous")
    context: dict[str, Any] = Field(default_factory=dict)
    requested_action: str = Field(default="analysis")
    requested_mutation: bool = Field(default=False)
    evidence: list[str] = Field(default_factory=list)


class RouterOutput(BaseModel):
    """P0 router contract — what the router returns."""
    mission: MissionState
    risk_class: RiskClass
    pipeline: list[PipelineStage]
    mutation_allowed: bool
    missing_evidence: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    status: str = Field(default="READY_FOR_DRY_RUN")
    selection_log: list[str] = Field(default_factory=list)
    # HOLD states
    hold_reason: Optional[str] = Field(None)
    hold_missing: list[str] = Field(default_factory=list)
    # Integrity
    router_version: str = "1.0.0"
    spine_hash: Optional[str] = Field(None)
    generated_at: Optional[str] = Field(None)


# ── Mission → Capability Map ──────────────────────────────────────
# These are SEMANTIC capabilities, not tool names.
# The registry spine resolves each to the current callable implementation.

MISSION_CAPABILITY_MAP: dict[MissionState, list[CapabilityRef]] = {
    MissionState.OBSERVE: [
        CapabilityRef(capability="system_health", organ=OrganName.ARIFOS, mode=ExecutionMode.READ_ONLY,
                      reason="Establish current federation state before any observation"),
        CapabilityRef(capability="data_query", organ=OrganName.GEOX, mode=ExecutionMode.READ_ONLY,
                      reason="Query earth evidence if subject is geological"),
        CapabilityRef(capability="market_query", organ=OrganName.WEALTH, mode=ExecutionMode.READ_ONLY,
                      reason="Query capital signals if subject is economic"),
        CapabilityRef(capability="human_readiness", organ=OrganName.WELL, mode=ExecutionMode.READ_ONLY,
                      reason="Check operator state before analysis"),
    ],
    MissionState.EXPLAIN: [
        CapabilityRef(capability="structured_reasoning", organ=OrganName.ARIFOS, mode=ExecutionMode.READ_ONLY,
                      reason="Multi-hypothesis reasoning under epistemic discipline"),
        CapabilityRef(capability="domain_interpretation", organ=OrganName.GEOX, mode=ExecutionMode.READ_ONLY,
                      reason="Earth-science interpretation of evidence"),
        CapabilityRef(capability="capital_diagnosis", organ=OrganName.WEALTH, mode=ExecutionMode.READ_ONLY,
                      reason="Capital/economic interpretation of signals"),
        CapabilityRef(capability="contradiction_scan", organ=OrganName.GEOX, mode=ExecutionMode.READ_ONLY,
                      reason="Falsification: what evidence contradicts each hypothesis"),
    ],
    MissionState.DECIDE: [
        CapabilityRef(capability="structured_reasoning", organ=OrganName.ARIFOS, mode=ExecutionMode.ADVISORY,
                      reason="Constitutional reasoning with consequence mapping"),
        CapabilityRef(capability="consequence_modeling", organ=OrganName.GEOX, mode=ExecutionMode.ADVISORY,
                      reason="Model geological consequences of each path"),
        CapabilityRef(capability="capital_exposure", organ=OrganName.WEALTH, mode=ExecutionMode.ADVISORY,
                      reason="Model economic consequences of each path"),
        CapabilityRef(capability="falsification", organ=OrganName.GEOX, mode=ExecutionMode.READ_ONLY,
                      reason="Attempt to destroy the preferred case before presenting it"),
        CapabilityRef(capability="constitutional_judgment", organ=OrganName.ARIFOS, mode=ExecutionMode.ADVISORY,
                      reason="Floor check, reversibility test, uncertainty bounds"),
    ],
    MissionState.ACT: [
        CapabilityRef(capability="authority_validation", organ=OrganName.ARIFOS, mode=ExecutionMode.READ_ONLY,
                      reason="Validate that actor has authority for requested mutation"),
        CapabilityRef(capability="execution_planning", organ=OrganName.AFORGE, mode=ExecutionMode.DRY_RUN,
                      reason="Build execution plan with dependency graph and rollback"),
        CapabilityRef(capability="constitutional_judgment", organ=OrganName.ARIFOS, mode=ExecutionMode.ADVISORY,
                      reason="Judge before mutation — never skip"),
        CapabilityRef(capability="forge_execute", organ=OrganName.AFORGE, mode=ExecutionMode.MUTATE,
                      reason="Execute only after SEAL verdict. SCT-enforced."),
        CapabilityRef(capability="verification", organ=OrganName.ARIFOS, mode=ExecutionMode.READ_ONLY,
                      reason="Verify result independently of executor"),
        CapabilityRef(capability="immutable_record", organ=OrganName.VAULT999, mode=ExecutionMode.SEAL,
                      reason="Seal execution receipt to immutable ledger"),
    ],
    MissionState.MONITOR: [
        CapabilityRef(capability="system_health", organ=OrganName.ARIFOS, mode=ExecutionMode.READ_ONLY,
                      reason="Continuous health probe baseline"),
        CapabilityRef(capability="machine_health", organ=OrganName.WELL, mode=ExecutionMode.READ_ONLY,
                      reason="VPS reliability, Docker health, service status"),
        CapabilityRef(capability="market_health", organ=OrganName.WEALTH, mode=ExecutionMode.READ_ONLY,
                      reason="Market/economic anomaly detection"),
        CapabilityRef(capability="delta_report", organ=OrganName.ARIFOS, mode=ExecutionMode.READ_ONLY,
                      reason="Compare current state vs baseline, surface only deltas"),
    ],
    MissionState.RECALL: [
        CapabilityRef(capability="governed_recall", organ=OrganName.ARIFOS, mode=ExecutionMode.READ_ONLY,
                      reason="L1-L6 semantic memory traversal with provenance"),
        CapabilityRef(capability="chain_verification", organ=OrganName.VAULT999, mode=ExecutionMode.READ_ONLY,
                      reason="Verify hash-chain integrity of sealed records"),
    ],
}


# ── Intent Classification Keywords ────────────────────────────────
# Deterministic, no model. Ambiguous → HOLD_FOR_INTENT.

INTENT_KEYWORDS: dict[MissionState, list[str]] = {
    MissionState.OBSERVE: [
        "what is", "what's happening", "check", "status", "show me", "look at",
        "gather", "collect", "probe", "scan", "inspect", "current state",
        "bagaimana", "apa status", "tengok", "periksa", "check sekarang",
    ],
    MissionState.EXPLAIN: [
        "why", "explain", "what caused", "how did", "interpret", "analyze",
        "what does this mean", "understand", "diagnose", "root cause",
        "kenapa", "mengapa", "jelaskan", "analisa", "tafsir",
    ],
    MissionState.DECIDE: [
        "should we", "should i", "decide", "recommend", "compare", "evaluate",
        "assess", "what if", "option", "choice", "path", "risk",
        "patut", "pilih", "baik mana", "patutkah", "nilaikan",
    ],
    MissionState.ACT: [
        "execute", "deploy", "build", "make the change", "do it", "run",
        "apply", "implement", "commit", "push", "release",
        "buat", "laksana", "jalan", "deploy", "commit",
    ],
    MissionState.MONITOR: [
        "watch", "monitor", "alert", "track", "keep an eye", "observe continuously",
        "notify", "surveillance", "patrol",
        "pantau", "awas", "jaga", "perhati",
    ],
    MissionState.RECALL: [
        "what did we", "remember", "recall", "retrieve", "find", "search history",
        "what happened with", "past decision", "previous", "what did i",
        "ingat", "cari balik", "apa keputusan", "sejarah",
    ],
}
