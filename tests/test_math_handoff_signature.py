#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_math_handoff_signature.py
==============================
APEX-MATH-CANON-2026-09-23 §5.1 / §5.2 enforcement gate (Prong (b) compliance).

Compiles the **Per-Agent Math Competency Signature** into a machine-enforceable
mechanism. Cross-agent math handoff is valid iff both sender and receiver hold
the math in their competency signature. Seal authority requires competency
in the math being asserted.

Run: pytest /root/AAA/tests/test_math_handoff_signature.py -v
Or:   python3 -m pytest /root/AAA/tests/test_math_handoff_signature.py -v
Or:   python3 /root/AAA/tests/test_math_handoff_signature.py  (smoke mode)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import FrozenSet, Optional, Set, Tuple


# -----------------------------------------------------------------------------
# The 18 mathematical layers (APEX MATH Canon §3)
# -----------------------------------------------------------------------------
ALL_LAYERS: FrozenSet[str] = frozenset(
    {
        "L0",  # Logic & Computability
        "L0.5",  # Constraint Satisfaction (operational logic)
        "L1",  # Probability & Bayesian Inference
        "L1.5",  # Statistical Learning Theory
        "L2",  # Information Theory
        "L3",  # Optimization Theory
        "L4",  # Control Theory
        "L4.5",  # Numerical Analysis & Algorithmic Stability
        "L5",  # Dynamical Systems
        "L6",  # Game Theory
        "L7",  # Information Geometry
        "L7.5",  # Topology
        "L8",  # Active Inference
        "L8.5",  # Causal Inference
        "L9",  # Category Theory
        "L10",  # Computational Thermodynamics
        "L11",  # Quantum Information (formal analogy — HOLD per canon §10)
        "L12",  # Possibility-Space Geometry
    }
)

VALID_LAYERS = ALL_LAYERS  # Alias for clarity


# -----------------------------------------------------------------------------
# Competency signature + per-agent signatures (Canon §5)
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class CompetencySignature:
    """Per-agent set of math layers the agent can reason about (Canon §5)."""

    layers: FrozenSet[str]
    agent_id: str

    def __contains__(self, layer: str) -> bool:
        return layer in self.layers


# Per-agent signatures per APEX-MATH-CANON §5.
# These are INT-interpretive assignments requiring empirical audit (Canon §10 OPEN 2).
AGENT_SIGNATURES: dict[str, CompetencySignature] = {
    "333-AGI": CompetencySignature(frozenset({"L0", "L0.5", "L1", "L2", "L3", "L9", "L12"}), "333-AGI"),
    "555-ASI": CompetencySignature(frozenset({"L1", "L1.5", "L2", "L4", "L5", "L8", "L10"}), "555-ASI"),
    "888-APEX": CompetencySignature(frozenset({"L0", "L0.5", "L6", "L8.5", "L10", "L11"}), "888-APEX"),
    "A-FORGE": CompetencySignature(frozenset({"L3", "L4", "L4.5", "L8"}), "A-FORGE"),
    "HERMES": CompetencySignature(frozenset({"L1", "L2", "L6", "L7.5"}), "HERMES"),
    "VAULT999": CompetencySignature(frozenset({"L2", "L9", "L10"}), "VAULT999"),
    "GEOX": CompetencySignature(frozenset({"L5", "L6", "L7.5", "L8"}), "GEOX"),
    "WEALTH": CompetencySignature(frozenset({"L3", "L6", "L10"}), "WEALTH"),
    "WELL": CompetencySignature(frozenset({"L4", "L4.5", "L8", "L10"}), "WELL"),
    # i-ARIF holds ALL layers + meta-L9 (per Canon §5 — sovereign decides which math for which loop)
    "i-ARIF": CompetencySignature(ALL_LAYERS, "i-ARIF"),
}


def get_signature(agent_id: str) -> Optional[CompetencySignature]:
    return AGENT_SIGNATURES.get(agent_id)


# -----------------------------------------------------------------------------
# Handoff rule (Canon §5.1)
# -----------------------------------------------------------------------------
def handoff_valid(
    sender: str,
    receiver: str,
    asserted_math: Set[str],
) -> Tuple[bool, str]:
    """
    handoff_valid(s, r, m) ⟺ (m ⊆ s.competency) ∧ (m ⊆ r.competency)

    Returns (is_valid, reason).
    On violation, returns reason beginning with 'MATH_HANDOFF_VIOLATION:'.
    """
    sender_sig = get_signature(sender)
    receiver_sig = get_signature(receiver)

    if sender_sig is None:
        return False, f"MATH_HANDOFF_VIOLATION: UNKNOWN_SENDER_AGENT: {sender}"
    if receiver_sig is None:
        return False, f"MATH_HANDOFF_VIOLATION: UNKNOWN_RECEIVER_AGENT: {receiver}"

    # Reject any unknown layers (defense in depth)
    unknown_layers = asserted_math - ALL_LAYERS
    if unknown_layers:
        return False, f"MATH_HANDOFF_VIOLATION: UNKNOWN_LAYER: {unknown_layers}"

    # HOLD_special_handling clause (Canon §5.1) — block layers awaiting sovereign resolution
    held_layers = asserted_math & HOLD_LAYERS
    if held_layers:
        return (
            False,
            f"MATH_HANDOFF_VIOLATION: HOLD_SPECIAL_HANDLING: {sorted(held_layers)} awaiting sovereign resolution per Canon §10 OPEN",
        )

    missing_sender = asserted_math - sender_sig.layers
    if missing_sender:
        return False, f"MATH_HANDOFF_VIOLATION: SENDER_LACKS_COMPETENCY: {sender} lacks {sorted(missing_sender)}"

    missing_receiver = asserted_math - receiver_sig.layers
    if missing_receiver:
        return False, f"MATH_HANDOFF_VIOLATION: RECEIVER_LACKS_COMPETENCY: {receiver} lacks {sorted(missing_receiver)}"

    return True, "HANDOFF_VALID"


# -----------------------------------------------------------------------------
# Seal authority rule (Canon §5.2)
# -----------------------------------------------------------------------------
def may_seal(
    agent: str,
    claim_layers: Set[str],
    floor_pass: bool = True,
    w3: float = 1.0,
) -> Tuple[bool, str]:
    """
    may_seal(a, c) ⟺ F1_F13_pass(a, c) ∧ a.competency ⊇ math(c) ∧ W³(c) ≥ 0.85

    This implementation checks the math-competency clause. Floor compliance
    and W³ are passed as parameters (canon-validated by arif_judge upstream).
    Default values assume floors passed and W³ satisfied for test simplicity.
    """
    if not floor_pass:
        return False, "SEAL_DENIED: F1_F13_FLOOR_VIOLATION"
    if w3 < 0.85:
        return False, f"SEAL_DENIED: W3_BELOW_THRESHOLD: w3={w3} < 0.85"

    sig = get_signature(agent)
    if sig is None:
        return False, f"SEAL_DENIED: UNKNOWN_AGENT: {agent}"

    unknown_layers = claim_layers - ALL_LAYERS
    if unknown_layers:
        return False, f"SEAL_DENIED: UNKNOWN_LAYER: {unknown_layers}"

    missing = claim_layers - sig.layers
    if missing:
        return False, f"SEAL_DENIED: INSUFFICIENT_COMPETENCY: {agent} cannot seal claim involving {sorted(missing)}"

    return True, "MAY_SEAL: competency verified"


# -----------------------------------------------------------------------------
# Signature audit (Canon §10 OPEN 2 — empirical validation)
# -----------------------------------------------------------------------------
def audit_agent_signature(agent_id: str) -> dict:
    """
    Returns a structured audit report for an agent's signature.
    Per Canon §10 OPEN 2, per-agent signatures are INT assignments that need
    empirical validation. This function produces the audit input.
    """
    sig = get_signature(agent_id)
    if sig is None:
        return {"agent": agent_id, "status": "UNKNOWN_AGENT", "layers": None}

    missing_layers = ALL_LAYERS - sig.layers
    return {
        "agent": agent_id,
        "status": "KNOWN",
        "layers_held": sorted(sig.layers),
        "layers_missing": sorted(missing_layers),
        "n_held": len(sig.layers),
        "n_total": len(ALL_LAYERS),
        "coverage_pct": round(100.0 * len(sig.layers) / len(ALL_LAYERS), 1),
        "audit_note": "INT assignment per Canon §5; requires empirical validation.",
    }


# =============================================================================
# TESTS
# =============================================================================


def test_all_layers_unique_and_complete():
    """The 18 layers must be exactly 18 and unique."""
    assert len(ALL_LAYERS) == 18, f"Expected 18 layers, got {len(ALL_LAYERS)}"
    # Sanity-check naming convention: L<digit>[.5]
    for layer in ALL_LAYERS:
        assert layer.startswith("L"), f"Layer name must start with L: {layer}"


def test_per_agent_signatures_match_canon_section_5():
    """Each agent's signature must match the canonical assignment in §5."""
    expected = {
        "333-AGI": {"L0", "L0.5", "L1", "L2", "L3", "L9", "L12"},
        "555-ASI": {"L0", "L0.5", "L1", "L1.5", "L2", "L4", "L5", "L8", "L10"},
        "888-APEX": {"L0", "L0.5", "L6", "L8.5", "L10", "L11"},
        "A-FORGE": {"L3", "L4", "L4.5", "L8"},
        "HERMES": {"L1", "L2", "L6", "L7.5"},
        "VAULT999": {"L2", "L9", "L10"},
        "GEOX": {"L4.5", "L5", "L6", "L7.5", "L8", "L8.5"},
        "WEALTH": {"L1", "L1.5", "L3", "L6", "L10"},
        "WELL": {"L4", "L4.5", "L8", "L10"},
        "i-ARIF": set(ALL_LAYERS),
    }
    for agent, want in expected.items():
        got = AGENT_SIGNATURES[agent].layers
        assert got == want, f"{agent}: expected {want}, got {got}"


def test_i_arif_holds_every_layer():
    """i-ARIF (sovereign) holds all 18 layers + meta-L9 (Canon §5)."""
    sig = AGENT_SIGNATURES["i-ARIF"]
    for layer in ALL_LAYERS:
        assert layer in sig, f"i-ARIF must hold {layer}"


def test_555_validates_own_jurisdiction():
    """555 (auditor) validates its own L1.5 / L2 / L8 claims to itself."""
    valid, _ = handoff_valid("555-ASI", "555-ASI", {"L1.5", "L2", "L8"})
    assert valid, "555 must accept its own competency"


def test_888_seals_within_jurisdiction():
    """888 (judge) seals causal (L8.5) and game (L6) — within signature."""
    valid, msg = may_seal("888-APEX", {"L6", "L8.5", "L10"})
    assert valid, f"888 must seal its own jurisdiction: {msg}"


def test_888_cannot_seal_topology_L7_5():
    """888 (judge) does NOT have L7.5 (topology) — must be denied."""
    valid, msg = may_seal("888-APEX", {"L7.5"})
    assert not valid
    assert "INSUFFICIENT_COMPETENCY" in msg
    assert "L7.5" in msg


def test_888_cannot_seal_active_inference_L8():
    """888 has L8.5 (causal) but NOT L8 (active inference) — must be denied."""
    valid, msg = may_seal("888-APEX", {"L8"})
    assert not valid
    assert "INSUFFICIENT_COMPETENCY" in msg


def test_333_cannot_hand_off_active_inference_L8():
    """333 (architect) does NOT have L8 (active inference) — sender fails."""
    valid, msg = handoff_valid("333-AGI", "555-ASI", {"L8"})
    assert not valid, "333 lacks L8 in its signature"
    assert "SENDER_LACKS_COMPETENCY" in msg


def test_a_forge_has_numerical_stability_L4_5():
    """A-FORGE (actor) holds L4.5 (numerical stability) — critical for actuation."""
    valid, msg = may_seal("A-FORGE", {"L3", "L4", "L4.5", "L8"})
    assert valid, f"A-FORGE must hold L4.5: {msg}"


def test_cross_agent_causal_handoff_555_to_888():
    """555 sends L8.5 (causal) to 888. 555 lacks L8.5 → sender fails."""
    valid, msg = handoff_valid("555-ASI", "888-APEX", {"L8.5"})
    assert not valid, "555 lacks L8.5 in its signature"
    assert "SENDER_LACKS_COMPETENCY" in msg


def test_cross_agent_active_inference_555_to_888():
    """555 (has L8) sends L8 to 888 (no L8). Receiver fails."""
    valid, msg = handoff_valid("555-ASI", "888-APEX", {"L8"})
    assert not valid, "888 lacks L8"
    assert "RECEIVER_LACKS_COMPETENCY" in msg


def test_unknown_agent_rejected():
    """Unknown sender/receiver → MATH_HANDOFF_VIOLATION."""
    valid, msg = handoff_valid("UNKNOWN", "333-AGI", {"L0"})
    assert not valid
    assert "UNKNOWN_SENDER_AGENT" in msg

    valid, msg = handoff_valid("333-AGI", "GHOST", {"L0"})
    assert not valid
    assert "UNKNOWN_RECEIVER_AGENT" in msg


def test_unknown_layer_rejected():
    """Unknown layer (e.g., 'L99') is rejected — defense in depth."""
    valid, msg = handoff_valid("333-AGI", "555-ASI", {"L0", "L99"})
    assert not valid
    assert "UNKNOWN_LAYER" in msg


def test_seal_authority_requires_floor_compliance():
    """may_seal must reject if F1-F13 floors fail."""
    valid, msg = may_seal("888-APEX", {"L6", "L10"}, floor_pass=False, w3=1.0)
    assert not valid
    assert "FLOOR_VIOLATION" in msg


def test_seal_authority_requires_w3_threshold():
    """may_seal must reject if W³ < 0.85 (APEX REALITY KERNEL W³ law)."""
    valid, msg = may_seal("888-APEX", {"L6", "L10"}, floor_pass=True, w3=0.5)
    assert not valid
    assert "W3_BELOW_THRESHOLD" in msg


def test_handoff_uses_disjoint_sets():
    """Sender and receiver signatures may overlap but neither must fully contain the other."""
    # 333 and 555 share {L1, L2} but neither contains the other
    sig_333 = AGENT_SIGNATURES["333-AGI"].layers
    sig_555 = AGENT_SIGNATURES["555-ASI"].layers
    overlap = sig_333 & sig_555
    assert "L1" in overlap and "L2" in overlap
    assert not sig_333.issubset(sig_555)
    assert not sig_555.issubset(sig_333)


def test_audit_report_shape():
    """audit_agent_signature returns expected schema."""
    report = audit_agent_signature("333-AGI")
    assert report["agent"] == "333-AGI"
    assert report["status"] == "KNOWN"
    assert "L0" in report["layers_held"]
    assert "L4.5" in report["layers_missing"]  # 333 doesn't have L4.5
    assert report["n_total"] == 18


def test_audit_report_for_sovereign():
    """i-ARIF audit shows 100% coverage + zero missing."""
    report = audit_agent_signature("i-ARIF")
    assert report["coverage_pct"] == 100.0
    assert report["layers_missing"] == []
    assert report["n_held"] == 18


def test_signature_uniqueness():
    """Each non-sovereign agent has a distinct signature (no two equal)."""
    non_sovereign = [(k, v.layers) for k, v in AGENT_SIGNATURES.items() if k != "i-ARIF"]
    sigs = [layers for _, layers in non_sovereign]
    assert len(sigs) == len(set(sigs)), "Two non-sovereign agents have identical signatures"


def test_empty_handoff_is_valid():
    """Empty math set trivially passes (nothing to validate)."""
    valid, msg = handoff_valid("333-AGI", "555-ASI", set())
    assert valid, f"Empty math should be trivially valid: {msg}"


def test_handoff_chain_333_555_888_on_shared_math():
    """A 333→555→888 chain on shared math (L2) succeeds."""
    valid_1, _ = handoff_valid("333-AGI", "555-ASI", {"L2"})
    assert valid_1, "333→555 on L2 must succeed (both have L2)"
    valid_2, _ = handoff_valid("555-ASI", "888-APEX", {"L2"})
    # 888 doesn't have L2 → fails at receiver
    assert not valid_2, "888 lacks L2"


# -----------------------------------------------------------------------------
# Smoke test runner (when not invoked via pytest)
# -----------------------------------------------------------------------------
def smoke() -> int:
    """Run all test_* functions in-process. Returns number of failures."""
    failures = 0
    tests = sorted((name, fn) for name, fn in globals().items() if name.startswith("test_") and callable(fn))
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as e:
            failures += 1
            print(f"  FAIL  {name}: {e}")
        except Exception as e:
            failures += 1
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed, {failures} failed")
    return failures


if __name__ == "__main__":
    print("APEX-MATH-CANON-2026-09-23 §5.1/§5.2 enforcement gate (Prong b compliance)")
    print("=" * 70)
    failures = smoke()
    sys.exit(0 if failures == 0 else 1)
