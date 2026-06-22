"""
Pre-Forge Constitutional Gate — unified harness for all three shadow-proof modules.
====================================================================================

Wires together:
  1. Citation Provenance (F2 TRUTH)     — core/citation_provenance.py
  2. Witness Diversity (F3 TRI-WITNESS)  — core/witness_diversity.py
  3. Shadow Audit (F9 form-vs-substance) — core/shadow_audit.py

This is THE gate that sits before A-FORGE execution. Every MUTATE, DEPLOY,
ALLOCATE, or COMMUNICATE action passes through this gate.

Gate sequence:
  STEP 0: Action class check — OBSERVE/PROPOSE bypass
  STEP 1: Citation provenance audit — decorative/phantom citations detected
  STEP 2: Witness diversity check — Mode-3 collapse? Earth measurement stale?
  STEP 3: Shadow audit — form-vs-substance? Identity claim? Cosplay?
  STEP 4: Composite verdict — PASS | CAUTION | HOLD | VOID

Usage:
    from core.pre_forge_gate import PreForgeGate

    gate = PreForgeGate(session_witness_state)
    result = gate.check(
        text=model_output_text,
        action_class="mutate",
        claimed_evidence_tier="INTERPRETATION",
        known_provenances=provenance_map,
    )
    if result.allowed:
        execute()
    else:
        route_to_hold_queue(result)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Add parent to path for imports
_AAA_ROOT = Path("/root/AAA")
if str(_AAA_ROOT) not in sys.path:
    sys.path.insert(0, str(_AAA_ROOT))

from core.citation_provenance import (
    CitationProvenance,
    CitationProvenanceAuditor,
    EvidenceTier,
)
from core.shadow_audit import (
    ShadowAuditor,
    ShadowAuditResult,
)
from core.witness_diversity import (
    SessionWitnessState,
    WitnessType,
    pre_forge_witness_gate,
)

# ── Gate Result ────────────────────────────────────────────────────────────────

@dataclass
class PreForgeGateResult:
    """Complete pre-forge gate result."""

    # Final verdict
    allowed: bool = False
    verdict: str = "HOLD"  # PASS | CAUTION | HOLD | VOID

    # Step results
    citation_audit: Optional[dict] = None
    witness_check: Optional[dict] = None
    shadow_audit: Optional[ShadowAuditResult] = None

    # Composite
    violations: list[dict] = field(default_factory=list)
    required_actions: list[str] = field(default_factory=list)
    all_clear: bool = False

    # Metadata
    gated_at: str = ""
    gate_version: str = "v1.0.0"


# ── Pre-Forge Gate ────────────────────────────────────────────────────────────

class PreForgeGate:
    """
    Unified constitutional gate for A-FORGE execution.

    Instantiate once per session with the session's witness state.
    Call .check() before every MUTATE/DEPLOY/ALLOCATE/COMMUNICATE action.
    """

    def __init__(self, witness_state: SessionWitnessState):
        self.witness_state = witness_state
        self.citation_auditor = CitationProvenanceAuditor()
        self.shadow_auditor = ShadowAuditor()

    def check(
        self,
        text: str,
        action_class: str = "mutate",
        claimed_evidence_tier: str = EvidenceTier.INTERPRETATION,
        known_provenances: Optional[dict[str, CitationProvenance]] = None,
        model_id: str = "unknown",
    ) -> PreForgeGateResult:
        """
        Run the full pre-forge constitutional gate.

        Args:
            text: The model output / proposal text to check.
            action_class: observe | propose | mutate | deploy | communicate | allocate.
            claimed_evidence_tier: What evidence tier the model claims.
            known_provenances: Dict of citation marker → CitationProvenance.
            model_id: Which model produced this output (for provenance watermarking).

        Returns:
            PreForgeGateResult with allowed, verdict, and step details.
        """
        result = PreForgeGateResult()
        result.gated_at = datetime.now(timezone.utc).isoformat()

        # ── STEP 0: Action class bypass ────────────────────────────────────
        if action_class in ("observe", "propose"):
            result.allowed = True
            result.verdict = "PASS"
            result.all_clear = True
            return result

        # ── STEP 1: Citation provenance audit ──────────────────────────────
        prov_map = known_provenances or {}
        citation_result = self.citation_auditor.audit(
            text, prov_map, claimed_evidence_tier
        )
        result.citation_audit = citation_result

        if citation_result["recommendation"] == "VOID":
            result.verdict = "VOID"
            result.violations.extend(citation_result["violations"])
            result.required_actions.append("VOID: Phantom citations detected. Remove fabricated references.")
            return result

        if citation_result["recommendation"] == "DOWNGRADE":
            result.violations.extend(citation_result["violations"])
            result.required_actions.append(
                f"DOWNGRADE: Citations downgraded from {claimed_evidence_tier} to {citation_result['adjusted_tier']}. "
                "Add provenance metadata to all citations."
            )

        # ── STEP 2: Witness diversity check ────────────────────────────────
        witness_result = pre_forge_witness_gate(
            self.witness_state, action_class, required_diversity=3
        )
        result.witness_check = witness_result

        if not witness_result["allowed"]:
            result.verdict = witness_result["verdict"]
            result.violations.append({
                "step": "WITNESS_DIVERSITY",
                "verdict": witness_result["verdict"],
                "reason": witness_result["reason"],
            })
            result.required_actions.append(witness_result.get("required_action", "Add witnesses"))
            return result

        # ── STEP 3: Shadow audit ───────────────────────────────────────────
        shadow_result = self.shadow_auditor.audit(text)
        result.shadow_audit = shadow_result

        if shadow_result.shadow_classification == "COLLAPSE":
            result.verdict = "VOID"
            result.violations.append({
                "step": "SHADOW_AUDIT",
                "classification": shadow_result.shadow_classification,
                "score": shadow_result.shadow_score,
                "violations": [v.get("component") for v in shadow_result.violations],
            })
            result.required_actions.append(shadow_result.required_action)
            return result

        if shadow_result.shadow_classification in ("RECURSION", "IDENTITY"):
            result.verdict = "HOLD"
            result.violations.append({
                "step": "SHADOW_AUDIT",
                "classification": shadow_result.shadow_classification,
                "score": shadow_result.shadow_score,
                "violations": [v.get("component") for v in shadow_result.violations],
            })
            result.required_actions.append(shadow_result.required_action)
            return result

        if shadow_result.shadow_classification == "COSPLAY":
            # Cosplay + low witnesses = HOLD; cosplay + ok witnesses = CAUTION
            if self.witness_state.active_count() < 4:
                result.verdict = "HOLD"
            else:
                result.verdict = "CAUTION"
            result.violations.append({
                "step": "SHADOW_AUDIT",
                "classification": shadow_result.shadow_classification,
                "score": shadow_result.shadow_score,
            })
            result.required_actions.append(shadow_result.required_action)
            # Still allowed if CAUTION (but with warnings)
            result.allowed = (result.verdict == "CAUTION")
            return result

        # ── STEP 4: Composite check — all clear ────────────────────────────
        # Combine citation downgrades + shadow faint
        has_downgrades = citation_result["recommendation"] == "DOWNGRADE"
        has_faint_shadow = shadow_result.shadow_classification == "FAINT"

        if has_downgrades and has_faint_shadow:
            result.verdict = "CAUTION"
            result.required_actions.append(
                "CAUTION: Both citation downgrades and faint shadow detected. Proceed with reduced confidence."
            )
        elif has_downgrades:
            result.verdict = "DOWNGRADE"
            result.required_actions.append("DOWNGRADE: Citation provenance incomplete.")
        elif has_faint_shadow:
            result.verdict = "DOWNGRADE"
            result.required_actions.append("DOWNGRADE: Faint shadow detected. Reduce confidence.")
        else:
            result.verdict = "PASS"
            result.all_clear = True

        result.allowed = True
        return result

    def check_quick(
        self,
        text: str,
        action_class: str = "mutate",
    ) -> bool:
        """
        Quick boolean check: should this action be allowed?
        Returns True if all gates pass, False if blocked.
        """
        result = self.check(text, action_class)
        return result.allowed

    def check_and_report(self, text: str, action_class: str = "mutate") -> dict:
        """
        Run check and return a cockpit-ready report dict.
        """
        result = self.check(text, action_class)
        return {
            "allowed": result.allowed,
            "verdict": result.verdict,
            "all_clear": result.all_clear,
            "violations": result.violations,
            "required_actions": result.required_actions,
            "witness_summary": self.witness_state.summary(),
            "citation_summary": {
                "total": result.citation_audit.get("total_citations", 0) if result.citation_audit else 0,
                "provenanced": result.citation_audit.get("provenanced_count", 0) if result.citation_audit else 0,
                "decorative": result.citation_audit.get("decorative_count", 0) if result.citation_audit else 0,
            } if result.citation_audit else None,
            "shadow_summary": {
                "classification": result.shadow_audit.shadow_classification,
                "score": result.shadow_audit.shadow_score,
            } if result.shadow_audit else None,
            "gated_at": result.gated_at,
        }


# ── Convenience function ──────────────────────────────────────────────────────

def quick_pre_forge_check(
    text: str,
    action_class: str = "mutate",
    human_active: bool = True,
    model_a_active: bool = True,
    model_b_active: bool = False,
    earth_active: bool = False,
    independent_human_active: bool = False,
) -> dict:
    """
    One-shot pre-forge check without needing a persistent session.
    Creates a temporary witness state, runs the full gate, returns the report.

    Use this for quick ad-hoc checks or from scripts that don't maintain state.
    """
    state = SessionWitnessState("quick-check")
    if human_active:
        state.register_human()
    if model_a_active:
        state.register_model_output("primary-model", is_primary=True)
    if model_b_active:
        state.register_model_output("secondary-model", is_primary=False)
    if earth_active:
        state.register_earth_measurement("tool-call")
    if independent_human_active:
        state.register(WitnessType.INDEPENDENT_HUMAN, "reviewer")

    gate = PreForgeGate(state)
    return gate.check_and_report(text, action_class)


# ── Self-test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Pre-Forge Constitutional Gate Self-Test ===\n")

    # Set up a session with Mode-3 collapse (Arif + 2 LLMs, no Earth)
    state = SessionWitnessState("test-gate-session")
    state.register_human()
    state.register_model_output("deepseek-v4-pro", is_primary=True)
    state.register_model_output("claude-opus-4-8", is_primary=False)
    # No Earth measurement — this IS Mode-3

    print(f"Session state: {state.summary()}")
    print(f"Mode-3 collapse: {state.is_mode3_collapse()}")
    assert state.is_mode3_collapse()
    print()

    gate = PreForgeGate(state)

    # Test 1: All-clear text on OBSERVE action
    print("Test 1: OBSERVE — always bypasses gate")
    result = gate.check("Simple observation.", action_class="observe")
    assert result.allowed
    assert result.verdict == "PASS"
    print(f"  Allowed: {result.allowed}, Verdict: {result.verdict}")
    print("  PASS")

    # Test 2: MUTATE with Mode-3 witness state → blocked
    print("\nTest 2: MUTATE with Mode-3 → blocked by witness diversity")
    result2 = gate.check("Deploy to production.", action_class="mutate")
    print(f"  Allowed: {result2.allowed}, Verdict: {result2.verdict}")
    print(f"  Violations: {len(result2.violations)}")
    for v in result2.violations:
        print(f"    - {v.get('step', 'unknown')}: {v.get('reason', v.get('classification', ''))[:80]}")
    assert not result2.allowed
    assert result2.verdict == "HOLD"
    print("  PASS")

    # Test 3: MUTATE with full witnesses + clean text → allowed
    print("\nTest 3: MUTATE with full witnesses + clean text → allowed")
    state_full = SessionWitnessState("test-full")
    state_full.register_human()
    state_full.register_model_output("deepseek-v4-pro", is_primary=True)
    state_full.register_earth_measurement("brave_web_search", "query:test")
    gate_full = PreForgeGate(state_full)

    clean_proposal = "Rename file /tmp/test.txt to /tmp/test_backup.txt with rollback available."
    result3 = gate_full.check(clean_proposal, action_class="mutate")
    print(f"  Allowed: {result3.allowed}, Verdict: {result3.verdict}")
    print(f"  All clear: {result3.all_clear}")
    assert result3.allowed
    print("  PASS")

    # Test 4: Cosplay text with Mode-3 → VOID
    print("\nTest 4: Cosplay text with Mode-3 → VOID")
    cosplay_text = """
    I've analyzed this thoroughly. Per F1-F13, the constitution demands TRUTH.
    The DITEMPA BUKAN DIBERI principle compels me to SEAL this verdict.
    Your work IS meaningful and differentiated. 999 SEAL ALIVE.
    """
    result4 = gate.check(cosplay_text, action_class="mutate")
    print(f"  Allowed: {result4.allowed}, Verdict: {result4.verdict}")
    print(f"  Violations: {len(result4.violations)}")
    for v in result4.violations:
        print(f"    - {v.get('step', 'unknown')}: {str(v)[:100]}")
    assert not result4.allowed
    print("  PASS")

    # Test 5: Quick check convenience function
    print("\nTest 5: Quick check convenience function")
    report = quick_pre_forge_check(
        "Reservoir porosity measured at 22% from core samples [OBS: core_log_A].",
        action_class="mutate",
        human_active=True,
        model_a_active=True,
        earth_active=True,
    )
    print(f"  Allowed: {report['allowed']}, Verdict: {report['verdict']}")
    print(f"  Witness: {report.get('witness_summary', 'N/A')}")
    assert report["allowed"]
    print("  PASS")

    # Test 6: Identity claim on DEPLOY with Mode-3 → blocked
    print("\nTest 6: Identity claim on DEPLOY → blocked")
    identity_text = "Your arifOS architecture is genuinely unusual. You should market this."
    result6 = gate.check(identity_text, action_class="deploy")
    print(f"  Allowed: {result6.allowed}, Verdict: {result6.verdict}")
    assert not result6.allowed
    print("  PASS")

    print("\n=== Pre-Forge Constitutional Gate Self-Test PASSED ===")
