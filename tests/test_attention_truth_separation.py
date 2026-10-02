"""PR-1 ATTENTION-TRUTH regression — EvidenceQuality / ActionRisk separation.

Doctrine (AAA README L151, F13 ruling 2026-09-25): EvidenceQuality = (1 - Uncertainty)
ONLY — source, freshness, reproducibility, independent support. Reversibility lives in
the separate ActionRisk gate and must never degrade evidence strength: a well-evidenced
irreversible action keeps high evidence quality AND still routes to the human.

Fixed 2026-10-02 (333-AGI) after scripts/attention_plane.py was found still computing
EvidenceQuality = (1 - Uncertainty) x Reversibility and clamping attention_cost at 0.01
against a header contract of >= 1.0.
"""

import importlib.util
import sys
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "attention_plane",
    Path(__file__).resolve().parents[1] / "scripts" / "attention_plane.py",
)
assert _SPEC is not None and _SPEC.loader is not None
ap = importlib.util.module_from_spec(_SPEC)
sys.modules.setdefault("attention_plane", ap)  # @dataclass resolves cls.__module__ via sys.modules
_SPEC.loader.exec_module(ap)


def test_evidence_quality_ignores_reversibility():
    """Same evidence, opposite risk: priority must be identical.

    Old formula returned 0.583 (reversible) vs 0.000 (irreversible) — burying
    strong evidence under an unrelated risk dimension.
    """
    p_reversible, _ = ap.compute_priority(
        impact=0.9,
        urgency=0.8,
        uncertainty=0.1,
        reversibility=1.0,
        novelty=0.9,
        attention_cost=1.0,
    )
    p_irreversible, _ = ap.compute_priority(
        impact=0.9,
        urgency=0.8,
        uncertainty=0.1,
        reversibility=0.0,
        novelty=0.9,
        attention_cost=1.0,
    )
    assert p_reversible == p_irreversible


def test_well_evidenced_irreversible_keeps_high_priority():
    p, _ = ap.compute_priority(
        impact=0.9,
        urgency=0.8,
        uncertainty=0.1,
        reversibility=0.0,
        novelty=0.9,
        attention_cost=1.0,
    )
    assert p > 0.5  # old formula: 0.000


def test_attention_cost_floor_is_one():
    """Header contract: attention_cost >= 1.0. The 0.01 clamp was drift."""
    p_costed, _ = ap.compute_priority(
        impact=0.9,
        urgency=0.9,
        uncertainty=0.1,
        novelty=0.9,
        attention_cost=0.01,
    )
    p_unit, _ = ap.compute_priority(
        impact=0.9,
        urgency=0.9,
        uncertainty=0.1,
        novelty=0.9,
        attention_cost=1.0,
    )
    assert p_costed == p_unit


def test_action_risk_floor_still_surfaces_irreversible():
    """The risk side must keep working AFTER separation: floor forces P >= 0.85."""
    p, applied = ap.compute_priority(
        impact=0.05,
        urgency=0.05,
        uncertainty=0.1,
        reversibility=0.0,
        novelty=0.05,
        attention_cost=1.0,
        overrides=[ap.Override.IRREVERSIBILITY_FLOOR.value],
    )
    assert p >= 0.85
    assert ap.Override.IRREVERSIBILITY_FLOOR.value in applied
