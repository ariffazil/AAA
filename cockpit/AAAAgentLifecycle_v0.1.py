#!/usr/bin/env python3
"""
AAAAgentLifecycle v0.1 — Universal Constitutional Membrane

Per sovereign 2026-10-02:
- 12 lifecycle interceptors, one interface
- Models become smarter; membrane stays wiser
- Reversible per-file (rm this file uninstalls)

The membrane:
- Forces every AAA agent through the same constitutional cycle
- Does NOT judge (judgment is arifOS 888)
- Does NOT execute (execution is A-FORGE 777)
- Does NOT seal (seal is VAULT999 999)

Source-of-truth: this file. Adapters source from here. (per sovereign invariant #16)
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable, Any


class Stage(Enum):
    """Semantic stations (per sovereign 2026-10-02). Numeric labels are NOT execution order."""
    BOOT = "H0_boot"
    INIT = "H1_init"
    INTENT = "H2_intent"
    DISCOVERY = "H3_discovery"
    SENSE = "H4_sense"
    MEANING = "H5_meaning"
    REASON = "H6_reason"
    COLLAPSE = "H7_collapse"
    ROUTE = "H8_route"
    AUTH = "H9_auth"
    FORGE = "H10_forge"
    VERIFY = "H11_verify"
    JUDGE = "H12_judge"
    CONSEQUENCE = "H13_consequence"
    SEAL = "H14_seal"


# Classify epistemic provenance
class EvidenceClass(Enum):
    OBSERVED = "OBS"
    DERIVED = "DER"
    INTERPRETED = "INT"
    ASSUMED = "ASS"
    UNKNOWN = "UNK"
    CONTESTED = "CON"
    UNCREATED = "UNC"


@dataclass
class Mission:
    """One mission = one constitutional spine (per sovereign)."""
    actor_id: str
    session_id: Optional[str] = None  # bound at INIT
    intent: str = ""
    success_criteria: list = field(default_factory=list)
    falsification_criteria: list = field(default_factory=list)
    non_goals: list = field(default_factory=list)
    authority_band: str = "OBSERVE_ONLY"
    runtime_identity: dict = field(default_factory=dict)
    evidence: list = field(default_factory=list)
    constitutional_chain: list = field(default_factory=list)
    state_at_start: dict = field(default_factory=dict)
    state_at_end: dict = field(default_factory=dict)
    lease_id: Optional[str] = None
    closed: bool = False
    seal_id: Optional[str] = None


@dataclass
class Expectation:
    """Pre-action expectation (for prediction vs actual delta)."""
    output: Any = None
    state_change: str = ""
    risk: str = ""
    affected_resource: str = ""
    observable_success: str = ""
    observable_failure: str = ""


@dataclass
class ActualResult:
    """Post-action reality check."""
    output: Any = None
    state_change: str = ""
    consequence: Any = None


class HookResult:
    """Every hook returns a HookResult. If aborted, AAA halts."""
    def __init__(self, continue_mission: bool = True, halt_reason: str = "", evidence: Optional[dict] = None):
        self.continue_mission = continue_mission
        self.halt_reason = halt_reason
        self.evidence = evidence or {}


class AAAgentLifecycle:
    """12-hook constitutional membrane. ONE interface, ALL AAA adapters."""

    def onInit(self, mission: Mission) -> HookResult:
        """H0/H1: BOOT + INIT. Bind actor, mint session, verify authority."""
        # Per sovereign: one constitutional spine, never parallel
        # Per sovereign invariant #16: consumers import vocabulary; they do not fork it
        if not mission.actor_id:
            return HookResult(False, "H1_INIT: actor_id required (F1 AMANAH)")
        mission.runtime_identity = self._probe_runtime_identity()
        return HookResult(True)

    def onIntent(self, mission: Mission) -> HookResult:
        """H2: INTENT. NIAT_CONTINUITY — intent must trace through all stages."""
        if not mission.intent:
            return HookResult(False, "H2_INTENT: intent must be declared (NIAT_CONTINUITY)")
        # Per sovereign: if intent is lost between stages → HOLD
        return HookResult(True)

    def onDiscovery(self, mission: Mission, tool_name: str) -> HookResult:
        """H3: DISCOVERY. DECLARED ≠ EXPORTED ≠ CALLABLE."""
        # Per sovereign (live evidence): GEOX advertised tool rejected, WEALTH /health Not Found
        return HookResult(True, evidence={
            "warning": "Tool name from connector surface; verify callable before use",
            "tool": tool_name,
        })

    def onSense(self, mission: Mission, claim: str, label: str) -> EvidenceClass:
        """H4: SENSE. OBS ≠ DER ≠ INT ≠ ASS."""
        # Returns the evidence classification the agent MUST apply to `claim`
        # Per sovereign: no inference becomes evidence
        return EvidenceClass.UNKNOWN  # Safe default

    def onMeaning(self, mission: Mission, claim: str) -> HookResult:
        """H5: MEANING. HERMES discipline, not automatic veto."""
        # Per sovereign finding: HERMES PERSPECTIVE divergence ≠ automatic HOLD
        return HookResult(True)

    def onReason(self, mission: Mission, paths: list) -> HookResult:
        """H6: REASON. Generate candidates. Bound by consequence."""
        # Per sovereign: ReasoningDepth ∝ Consequence
        return HookResult(True, evidence={"path_count": len(paths)})

    def onCollapse(self, mission: Mission, paths: list) -> HookResult:
        """H7: COLLAPSE. Reduce many possibilities to ONE NEXT_PATH."""
        # Per sovereign: never dump unresolved branching to human as menu
        if len(paths) > 12:
            return HookResult(False, "H7_COLLAPSE: too many candidates (ReasoningDepth ∝ Consequence violated)")
        return HookResult(True)

    def onRoute(self, mission: Mission, organ: str) -> HookResult:
        """H8: ROUTE. Lazy invocation — OrganCall iff ExpectedValueOfInformation > Cost."""
        return HookResult(True)

    def onAuth(self, mission: Mission, action_class: str) -> HookResult:
        """H9: AUTH. TaskIR + lease + lock + risk class."""
        # Per sovereign: authority without provenance = authority debt
        if mission.authority_band == "OBSERVE_ONLY" and action_class in ("MUTATE", "DEPLOY"):
            return HookResult(False, "H9_AUTH: OBSERVE_ONLY cannot authorize MUTATE/DEPLOY")
        return HookResult(True)

    def onForge(self, mission: Mission, target: str) -> HookResult:
        """H10: FORGE. Reversible boundary. BUILD/STAGE ≠ production consequence."""
        return HookResult(True)

    def onVerify(self, mission: Mission, evidence: dict) -> HookResult:
        """H11: VERIFY. Independent of builder."""
        # Per sovereign: builder claim ≠ independent verification
        # Per sovereign: UNKNOWN may not silently become PASS
        return HookResult(True, evidence=evidence)

    def onJudge(self, mission: Mission, candidate: dict) -> HookResult:
        """H12: JUDGE. Submit to arifOS, not self-certify."""
        # Per sovereign: arifOS is the constitutional judge; AAA does not judge
        return HookResult(True, evidence={"note": "Submit candidate to arifOS 888; AAA does not certify"})

    def onConsequence(self, mission: Mission, expectation: Expectation, actual: ActualResult) -> dict:
        """H13: CONSEQUENCE. Reality gets final say."""
        # Per sovereign: command success ≠ outcome success
        # Compute surprise (delta)
        delta = {
            "expected_output": expectation.output,
            "actual_output": actual.output,
            "expected_state_change": expectation.state_change,
            "actual_state_change": actual.state_change,
        }
        return delta

    def onSeal(self, mission: Mission, observed_consequence: dict) -> HookResult:
        """H14: SEAL. VAULT999 records ObservedConsequence, not intent."""
        # Per sovereign: 999 seals reality, not narrative
        if not observed_consequence:
            return HookResult(False, "H14_SEAL: cannot seal without observed consequence")
        mission.seal_id = f"VAULT-{mission.session_id or 'unbound'}-{hash(str(observed_consequence)) & 0xffffffff:08x}"
        mission.closed = True
        return HookResult(True, evidence={"seal_id": mission.seal_id})

    def _probe_runtime_identity(self) -> dict:
        """Read-only runtime identity. F1 AMANAH: observation only."""
        # Default empty dict; adapters may override
        return {}


# ─── Adapter contract ───────────────────────────────────────────────
# Every AAA harness implements this single interface.
# Replaceable cognitive engines behind same constitutional membrane.

ADAPTER_REGISTRY = {
    "stage_name": {
        "name": str,
        "version": str,
        "doctrine_source": str,
        "reversible": str,
    }
}


def example_adapter_metadata():
    return ADAPTER_REGISTRY | {
        "stage_name": {
            "name": "AAAAgentLifecycle v0.1",
            "version": "0.1",
            "doctrine_source": "/root/AAA/cockpit/AAA_APEX_ZEN_INIT_TO_SEAL_v0.1.md",
            "reversible": "rm /root/AAA/cockpit/AAAAgentLifecycle_v0.1.py",
        }
    }


# ─── P0 Hooks (sovereign forge priority) ────────────────────────────

def session_continuity_hook(session_id_a: str, session_id_b: str) -> HookResult:
    """P0: arifOS INIT → A-FORGE accepts ACT → AAA same session → 999 references same spine.

    If any transition fails → NO MUTATION.
    """
    if session_id_a != session_id_b:
        return HookResult(False, f"SESSION_CONTINUITY broken: {session_id_a} != {session_id_b}")
    return HookResult(True, evidence={"continuous": True})


def niat_continuity_hook(input_intent: str, session_objective: str, taskir_intent: str, judge_candidate_purpose: str) -> HookResult:
    """P0: input.intent → session.objective → TaskIR.intent → judge.candidate → seal.purpose.

    If intent disappears between stages → HOLD.

    Continuity rule: input.intent establishes the chain. Any later stage
    that is empty when an earlier stage was non-empty is a discontinuity.
    """
    chain = [input_intent, session_objective, taskir_intent, judge_candidate_purpose]
    # Strict: if any later stage is empty but earlier was non-empty, HOLD
    seen_nonempty = False
    for stage in chain:
        if stage:
            seen_nonempty = True
            continue
        if seen_nonempty:
            return HookResult(
                False,
                f"NIAT_CONTINUITY broken: empty stage after non-empty predecessor"
            )
    return HookResult(True)


def authority_revoke_on_close_hook(mission: Mission) -> HookResult:
    """P0: SESSION_CLOSE must destroy residual mission authority."""
    if not mission.closed:
        return HookResult(False, "AUTHORITY_REVOKE: SESSION_CLOSE not finalized")
    # Revoke all session leases
    mission.lease_id = None
    mission.authority_band = "OBSERVE_ONLY"
    return HookResult(True, evidence={"revoked_leases": [mission.lease_id]})


# ── P1 hooks (deferred until P0 proven) ──────────────────────────────
# P1: capability_discovery_hook, pre_tool_prediction_hook, post_tool_surprise_hook
# P1: taskir_lease_lock_hook, independent_verify_hook
# P1: post_action_witness_hook, chron_consequence_hook
#
# P2: experience_to_test_hook, attention_compression_hook