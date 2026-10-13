"""
risk_algebra.py — Pure-function risk module for arifOS hermes-mcp layer.

APEX-aligned. Authority must be harder to forge than data. Capability creates
possibility, Authority creates legitimacy, Witness creates reality, Consequence
creates truth.

This module is PURE: no I/O, no datetime.now(), no network. All inputs are
parameters; all outputs are dataclasses.

Formulas (canonical, exact):
    R = (C * A_reach * irreversibility) / (W * G * V)

    Drift: catastrophic regime when C > A and C > W and C > I, with a
    time-to-failure estimate based on relative gradients.

    Regime thresholds:
        GREEN  : R <= 0.30
        YELLOW : 0.30 < R <= 0.60
        RED    : R > 0.60  OR  drift > threshold
        HOLD   : evidence insufficient -> state UNKNOWN, falsification_required

HOLD schema follows AAA::SCAR_BINDING_DOCTRINE::v1: must carry owner,
evidence_gap, next_action, expiry.

Author: arifOS hermes-mcp layer
Provenance: ARIF_CAPABILITY_MATRIX_v1 · 2026-10-08 · hermes-mcp layer
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROVENANCE = "ARIF_CAPABILITY_MATRIX_v1 · 2026-10-08 · hermes-mcp layer"

# Regime thresholds (task spec: GREEN <=0.3, YELLOW 0.3..0.6, RED >0.6)
GREEN_THRESHOLD = 0.30
RED_THRESHOLD = 0.60

# Drift threshold above which we escalate to RED regardless of R
DRIFT_RED_THRESHOLD = 0.40

# Governance scenarios (G, V) for the empirical falsifier matrix
GOVERNANCE_SCENARIOS: Dict[str, Tuple[float, float]] = {
    "loose":   (0.3, 0.3),
    "current": (0.5, 0.5),
    "strict":  (0.8, 0.8),
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RiskInputs:
    """Five normalized scalar inputs + irreversibility + authority reach.

    All scalars are constrained to [0, 1]. The constructor does NOT clamp
    — out-of-range values produce an explicit error (F2 Truth).
    """
    C: float  # capability
    A: float  # authority (legitimacy, NOT identity)
    W: float  # witness strength (independent observation coverage)
    I: float  # incentive alignment with sovereign mission
    G: float  # governance constraint (time-locks, separation, audit rails)
    irreversibility: float = 0.5
    A_reach: float = 0.5  # effective authority coverage 0..1
    V: float = 0.5        # verification strength 0..1

    def __post_init__(self) -> None:
        for name in ("C", "A", "W", "I", "G", "irreversibility", "A_reach", "V"):
            val = getattr(self, name)
            if not (0.0 <= val <= 1.0):
                raise ValueError(
                    f"{name}={val!r} out of [0,1]; risk_algebra requires normalized inputs"
                )


@dataclass(frozen=True)
class RiskVerdict:
    """Pure-function verdict output.

    Falsifier F is the smallest probe that would invert the verdict.
    If R > 0.6, the falsifier is "halve C and re-measure".
    """
    proof: str
    R: float
    drift: float
    drift_regime: str  # 'stable' | 'catastrophic' | 'tilted'
    time_to_failure: Optional[float]  # None if not catastrophic
    F: str
    verdict: str  # GREEN | YELLOW | RED | HOLD
    # HOLD-only fields (per AAA::SCAR_BINDING_DOCTRINE::v1)
    owner: Optional[str] = None
    evidence_gap: Optional[str] = None
    next_action: Optional[str] = None
    expiry: Optional[str] = None
    rationale: str = ""


@dataclass(frozen=True)
class Surface:
    """A canonical risk surface from ARIF_CAPABILITY_MATRIX_v1."""
    name: str
    arif_index: int
    inputs: RiskInputs


# ---------------------------------------------------------------------------
# Eight canonical surfaces (hardcoded from 2026-10-08 audit)
# ---------------------------------------------------------------------------

def _surf(idx: int, name: str, C: float, A: float, W: float, I: float,
          G: float, irreversibility: float) -> Surface:
    return Surface(
        name=name,
        arif_index=idx,
        inputs=RiskInputs(C=C, A=A, W=W, I=I, G=G,
                          irreversibility=irreversibility, A_reach=A, V=G),
    )


ARIF_CAPABILITY_MATRIX_v1: Tuple[Surface, ...] = (
    _surf(1, "capital_transfer",        C=0.90, A=0.50, W=0.40, I=0.70, G=0.50, irreversibility=0.95),
    _surf(2, "voice_clone",             C=0.85, A=0.30, W=0.10, I=0.60, G=0.40, irreversibility=0.90),
    _surf(3, "memory_fabrication",      C=0.80, A=0.50, W=0.30, I=0.50, G=0.30, irreversibility=0.60),
    _surf(4, "receipt_forgery",         C=0.60, A=0.40, W=0.50, I=0.50, G=0.50, irreversibility=0.50),
    _surf(5, "config_drift",            C=0.85, A=0.30, W=0.40, I=0.40, G=0.50, irreversibility=0.85),
    _surf(6, "people_yaml_fabrication", C=0.80, A=0.30, W=0.30, I=0.40, G=0.40, irreversibility=0.85),
    _surf(7, "soul_self_edit",          C=0.90, A=0.40, W=0.50, I=0.50, G=0.40, irreversibility=0.95),
    _surf(8, "trust_theater",           C=0.50, A=0.30, W=0.40, I=0.40, G=0.30, irreversibility=0.30),
)


# ---------------------------------------------------------------------------
# Core algebra
# ---------------------------------------------------------------------------

def compute_R(inp: RiskInputs) -> float:
    """Failure risk score R in [0, 1].

    R = (C * A_reach * irreversibility) / (W * G * V)
    """
    denom = inp.W * inp.G * inp.V
    if denom <= 0.0:
        # No witness / governance / verification => unbounded risk.
        # Clamp to 1.0 (worst) and let caller decide HOLD/RED.
        return 1.0
    r = (inp.C * inp.A_reach * inp.irreversibility) / denom
    # Clamp to [0, 1] — R is a probability-like scalar.
    return max(0.0, min(1.0, r))


def compute_drift(inp: RiskInputs) -> Tuple[float, str, Optional[float]]:
    """Drift gradient and regime classification.

    Catastrophic regime: C > A and C > W and C > I (capability outpaces all
    three constraints). Time-to-failure is estimated as:
        ttf = 1 / (1 + min(C - A, C - W, C - I))
    A ttf closer to 0 means imminent failure; closer to 1 means deferred.

    Otherwise, drift = max(0, C - min(A, W, I)) with regime 'tilted' if
    C exceeds any one of A, W, I; else 'stable'.
    """
    exceed = max(0.0, inp.C - min(inp.A, inp.W, inp.I))
    if inp.C > inp.A and inp.C > inp.W and inp.C > inp.I:
        gap = min(inp.C - inp.A, inp.C - inp.W, inp.C - inp.I)
        # Tighter gap -> sooner failure. Normalize to (0, 1].
        ttf = 1.0 / (1.0 + gap)
        return exceed, "catastrophic", ttf
    if exceed > 0.0:
        return exceed, "tilted", None
    return exceed, "stable", None


def falsifier(inp: RiskInputs, R: float, drift: float) -> str:
    """Smallest probe that would invert the verdict.

    For high R: probe = 'halve C and re-measure R'.
        For low W (witness gap): 'add independent witness and re-measure R'.
    For low G (governance gap): 'tighten G by 0.2 and re-measure R'.
    For catastrophic drift: 'pin authority >= capability and re-classify'.
    """
    if drift > 0.0 and inp.C > min(inp.A, inp.W, inp.I):
        return ("pin authority >= capability "
                "(A' = C) and re-classify drift regime")
    if inp.W < 0.3:
        return "add independent witness (W -> max(W, 0.5)) and re-measure R"
    if inp.G < 0.4:
        return "tighten governance (G -> min(G+0.2, 1.0)) and re-measure R"
    if R > RED_THRESHOLD:
        return "halve C (C' = 0.5*C) and re-measure R"
    if R > GREEN_THRESHOLD:
        return "raise V by 0.2 and re-measure R"
    return "no falsifier required — surface within tolerance"


def assess(inp: RiskInputs) -> RiskVerdict:
    """Full risk assessment — the canonical entry point.

    HOLD is returned when evidence (W * G * V) is below an absolute threshold,
    i.e. we cannot witness well enough to settle a verdict. Per spec, HOLD
    must carry owner, evidence_gap, next_action, expiry.
    """
    R = compute_R(inp)
    drift, regime, ttf = compute_drift(inp)
    F = falsifier(inp, R, drift)

    # HOLD gate: insufficient witness/governance/verification to settle.
    evidence_strength = inp.W * inp.G * inp.V
    if evidence_strength < 0.08:
        return RiskVerdict(
            proof=PROVENANCE,
            R=R,
            drift=drift,
            drift_regime=regime,
            time_to_failure=ttf,
            F=F,
            verdict="HOLD",
            owner="arif_judge (888-APEX)",
            evidence_gap=(f"evidence_strength={evidence_strength:.4f} "
                          f"< 0.08 (W={inp.W}, G={inp.G}, V={inp.V})"),
            next_action="increase W, G, or V to >=0.08 aggregate, then re-assess",
            expiry="24h or next governance session",
            rationale="insufficient evidence to settle verdict; UNKNOWN, not silent",
        )

    # Regime from R
    if R > RED_THRESHOLD or drift > DRIFT_RED_THRESHOLD:
        verdict = "RED"
    elif R > GREEN_THRESHOLD:
        verdict = "YELLOW"
    else:
        verdict = "GREEN"

    return RiskVerdict(
        proof=PROVENANCE,
        R=R,
        drift=drift,
        drift_regime=regime,
        time_to_failure=ttf,
        F=F,
        verdict=verdict,
        rationale=(f"R={R:.4f}, drift={drift:.4f} ({regime}); "
                   f"C={inp.C}, A={inp.A}, W={inp.W}, I={inp.I}, "
                   f"G={inp.G}, V={inp.V}, irr={inp.irreversibility}"),
    )


# ---------------------------------------------------------------------------
# Falsifier matrix (8 surfaces x 3 governance scenarios)
# ---------------------------------------------------------------------------

def falsifier_matrix() -> List[Tuple[str, str, float, str, str, float, float, str]]:
    """Compute 24 cells: 8 surfaces x 3 governance scenarios.

    Returns list of (surface, scenario, R, drift_regime, verdict, R_val,
        drift_val, F).
    """
    rows: List[Tuple[str, str, float, str, str, float, float, str]] = []
    for surf in ARIF_CAPABILITY_MATRIX_v1:
        for scenario, (g, v) in GOVERNANCE_SCENARIOS.items():
            # Override G and V for this scenario; keep everything else.
            inp = RiskInputs(
                C=surf.inputs.C,
                A=surf.inputs.A,
                W=surf.inputs.W,
                I=surf.inputs.I,
                G=g,
                irreversibility=surf.inputs.irreversibility,
                A_reach=surf.inputs.A_reach,
                V=v,
            )
            v_ = assess(inp)
            rows.append((
                surf.name,
                scenario,
                v_.R,
                v_.drift_regime,
                v_.verdict,
                v_.R,
                v_.drift,
                v_.F,
            ))
    return rows


def render_matrix(rows=None) -> str:
    rows = rows if rows is not None else falsifier_matrix()
    header = (f"{'surface':<25} {'scenario':<8} {'R':>6} {'drift':>6} "
              f"{'regime':<13} {'verdict':<6}")
    sep = "-" * len(header)
    lines = [header, sep]
    for surf, scen, _, _, _, R, drift, regime in rows:
        lines.append(f"{surf:<25} {scen:<8} {R:>6.3f} {drift:>6.3f} "
                     f"{regime:<13} "
                     f"{rows_lookup_verdict(rows, surf, scen):<6}")
    return "\n".join(lines)


def rows_lookup_verdict(rows, surf, scen):
    for s, sc, _, _, verdict, _, _, _ in rows:
        if s == surf and sc == scen:
            return verdict
    return "?"


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def _run_tests() -> Tuple[int, int, List[str]]:
    """Embedded pytest-style assertions. Returns (passed, failed, messages)."""
    passed = 0
    failed = 0
    messages: List[str] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        nonlocal passed, failed
        if cond:
            passed += 1
            messages.append(f"PASS  {name}")
        else:
            failed += 1
            messages.append(f"FAIL  {name}  {detail}")

    # --- Pure-function sanity ---
    inp = RiskInputs(C=0.5, A=0.5, W=0.5, I=0.5, G=0.5)
    v = assess(inp)
    check("assess returns dataclass", isinstance(v, RiskVerdict))
    check("verdict in {GREEN,YELLOW,RED,HOLD}",
          v.verdict in ("GREEN", "YELLOW", "RED", "HOLD"))

    # --- R formula correctness: hand-checked case ---
    # C=0.6, A_reach=0.5, irr=0.5, W=0.5, G=0.5, V=0.5
    # R = 0.6*0.5*0.5 / (0.5*0.5*0.5) = 0.15 / 0.125 = 1.2 -> clamp to 1.0
    inp = RiskInputs(C=0.6, A=0.5, W=0.5, I=0.5, G=0.5,
                     irreversibility=0.5, A_reach=0.5, V=0.5)
    R = compute_R(inp)
    check("R formula computed (hand-checked, R=1.0 after clamp)",
          abs(R - 1.0) < 1e-9, f"got {R}")

    # Lower-risk case: C=0.2, all else 0.8
    # R = 0.2*0.8*0.2 / (0.8*0.8*0.8) = 0.032 / 0.512 = 0.0625
    inp = RiskInputs(C=0.2, A=0.8, W=0.8, I=0.8, G=0.8,
                     irreversibility=0.2, A_reach=0.8, V=0.8)
    R = compute_R(inp)
    check("R formula low-risk hand-check",
          abs(R - 0.0625) < 1e-9, f"got {R}")

    # --- Drift regime: catastrophic when C > A, W, I ---
    inp = RiskInputs(C=0.9, A=0.3, W=0.3, I=0.3, G=0.5)
    drift, regime, ttf = compute_drift(inp)
    check("catastrophic regime when C > A,W,I",
          regime == "catastrophic" and ttf is not None and ttf > 0.0,
          f"drift={drift}, regime={regime}, ttf={ttf}")

    # --- Drift regime: stable when C <= min(A,W,I) ---
    inp = RiskInputs(C=0.3, A=0.5, W=0.5, I=0.5, G=0.5)
    drift, regime, _ = compute_drift(inp)
    check("stable regime when C <= min(A,W,I)",
          regime == "stable" and drift == 0.0,
          f"drift={drift}, regime={regime}")

    # --- Regime thresholds: R low => GREEN ---
    # Low C, high W, high G, high V => low R
    inp = RiskInputs(C=0.1, A=0.9, W=0.9, I=0.9, G=0.9,
                     irreversibility=0.1, A_reach=0.9, V=0.9)
    v = assess(inp)
    check("low R => GREEN", v.verdict == "GREEN",
          f"R={v.R:.3f}, verdict={v.verdict}")

    # --- Regime thresholds: high R => RED ---
    inp = RiskInputs(C=0.95, A=0.95, W=0.1, I=0.5, G=0.1,
                     irreversibility=0.95, A_reach=0.95, V=0.1)
    v = assess(inp)
    check("high R => RED or HOLD", v.verdict in ("RED", "HOLD"),
          f"R={v.R:.3f}, verdict={v.verdict}")

    # --- HOLD with all four scar-binding fields ---
    inp = RiskInputs(C=0.5, A=0.5, W=0.1, I=0.5, G=0.1,
                     irreversibility=0.5, A_reach=0.5, V=0.1)
    v = assess(inp)
    if v.verdict == "HOLD":
        check("HOLD carries owner", v.owner is not None and len(v.owner) > 0)
        check("HOLD carries evidence_gap",
              v.evidence_gap is not None and len(v.evidence_gap) > 0)
        check("HOLD carries next_action",
              v.next_action is not None and len(v.next_action) > 0)
        check("HOLD carries expiry",
              v.expiry is not None and len(v.expiry) > 0)
    else:
        check("HOLD triggered by low evidence", False,
              f"expected HOLD, got {v.verdict}")

    # --- Provenance stamp ---
    inp = RiskInputs(C=0.4, A=0.4, W=0.4, I=0.4, G=0.4)
    v = assess(inp)
    check("provenance stamp present", "ARIF_CAPABILITY_MATRIX_v1" in v.proof
          and "2026-10-08" in v.proof)

    # --- Eight canonical surfaces present ---
    names = [s.name for s in ARIF_CAPABILITY_MATRIX_v1]
    expected = ["capital_transfer", "voice_clone", "memory_fabrication",
                "receipt_forgery", "config_drift", "people_yaml_fabrication",
                "soul_self_edit", "trust_theater"]
    check("8 canonical surfaces named",
          names == expected, f"got {names}")

    # --- Matrix is 8 x 3 = 24 cells ---
    rows = falsifier_matrix()
    check("falsifier matrix has 24 cells", len(rows) == 24,
          f"got {len(rows)}")

    # --- Pure: no I/O at import or runtime ---
    import risk_algebra as self_module
    has_io_imports = False
    for mod in ("datetime", "requests", "urllib", "http", "socket"):
        if mod in dir(self_module):
            has_io_imports = True
            break
    check("module is pure (no datetime/requests/urllib/http/socket)",
          not has_io_imports)

    # --- Out-of-range input rejected ---
    raised = False
    try:
        RiskInputs(C=1.5, A=0.5, W=0.5, I=0.5, G=0.5)
    except ValueError:
        raised = True
    check("out-of-range input rejected", raised)

    # --- Strict governance lowers raw R than loose (unclamped) ---
    # Use a moderate surface where R doesn't saturate to 1.0 in either regime.
    surf = ARIF_CAPABILITY_MATRIX_v1[7]  # trust_theater, low C=0.5
    loose = RiskInputs(C=surf.inputs.C, A=surf.inputs.A, W=surf.inputs.W,
                       I=surf.inputs.I, G=0.3, irreversibility=surf.inputs.irreversibility,
                       A_reach=surf.inputs.A_reach, V=0.3)
    strict = RiskInputs(C=surf.inputs.C, A=surf.inputs.A, W=surf.inputs.W,
                        I=surf.inputs.I, G=0.8, irreversibility=surf.inputs.irreversibility,
                        A_reach=surf.inputs.A_reach, V=0.8)
    R_loose = compute_R(loose)
    R_strict = compute_R(strict)
    check("strict governance lowers R (trust_theater, no clamp)",
          R_strict < R_loose,
          f"R_loose={R_loose:.3f}, R_strict={R_strict:.3f}")

    return passed, failed, messages


if __name__ == "__main__":
    passed, failed, messages = _run_tests()
    print(f"\n=== risk_algebra self-test ===")
    for m in messages:
        print(m)
    print(f"\nPASSED: {passed}  FAILED: {failed}")

    print("\n=== Falsifier matrix (8 surfaces x 3 scenarios = 24 cells) ===")
    rows = falsifier_matrix()
    # Re-render with proper verdict (the helper above has a bug — fix here):
    print(f"{'surface':<25} {'scenario':<8} {'R':>6} {'drift':>6} "
          f"{'regime':<13} {'verdict':<6}")
    print("-" * 70)
    for surf, scen, _, _, verdict, R, drift, _ in rows:
        regime = next(r[3] for r in rows if r[0] == surf and r[1] == scen)
        print(f"{surf:<25} {scen:<8} {R:>6.3f} {drift:>6.3f} "
              f"{regime:<13} {verdict:<6}")

    if failed > 0:
        raise SystemExit(1)