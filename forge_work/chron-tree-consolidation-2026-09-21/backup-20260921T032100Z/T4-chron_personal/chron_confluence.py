#!/usr/bin/env python3
"""CHRON Confluence Scorer — weighted multi-component trading decision.

Per CHRON × WEALTH × HERMES synthesis 2026-09-18:
  score = regime × 0.35 + zone_quality × 0.25 + macro_alignment × 0.25 + hermes_signal × 0.15
  threshold: score > 0.65 → PROCEED

Plus CHRON calibration gate: if mean_brier > 0.25 → HOLD regardless.

The 4 components are READ-ONLY inputs — this module doesn't compute regime,
zone, or macro. The caller must wire those from WEALTH/CHRON/HERMES organs.

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

MYT = timezone(timedelta(hours=8))

# Default weights — synthesis §V
W_REGIME = 0.35
W_ZONE = 0.25
W_MACRO = 0.25
W_HERMES = 0.15

# Default threshold
THRESHOLD_PROCEED = 0.65
CALIBRATION_GATE_BRIER = 0.25  # if mean_brier > 0.25 → HOLD regardless

OUTPUT_PATH = Path("/root/.hermes/cron/state/chron_personal/confluence_log.jsonl")


@dataclass
class ConfluenceInput:
    """Read-only inputs to the confluence scorer.

    Each score in [0.0, 1.0]:
      - regime: how strongly the EMA 20/50/200 alignment confirms trend
                (1.0 = strong uptrend, 0.5 = sideways, 0.0 = strong downtrend)
      - zone_quality: strength of S/R zone retest (0..1)
      - macro_alignment: how aligned macro transmission is with direction
                         (1.0 = strongly aligned, 0.5 = neutral, 0.0 = adverse)
      - hermes_signal: how supportive HERMES PLAUSIBLE/CLAIM signals are
                       (1.0 = strongly aligned, 0.5 = neutral, 0.0 = contrary)
    """

    instrument: str
    regime_score: float
    zone_quality: float
    macro_alignment: float
    hermes_signal: float
    mean_brier: Optional[float] = None
    direction: str = "up"  # up | down | range
    regime_label: str = ""  # e.g. "UPTREND" / "SIDEWAYS" / "DOWNTREND"
    macro_channel: str = ""  # e.g. "fiscal_energy"
    hermes_signal_count: int = 0
    seasonal_bias: Optional[dict] = None  # from chron_seasonal
    event_risk: Optional[dict] = None  # from chron_event_timers
    notes: list[str] = field(default_factory=list)


@dataclass
class ConfluenceOutput:
    """Confluence decision — what the trader agent should do."""

    instrument: str
    score: float
    breakdown: dict
    decision: str  # PROCEED | HOLD | SABAR | BLOCK
    gates: dict = field(default_factory=dict)
    seasonal: Optional[dict] = None
    event_risk: Optional[dict] = None
    notes: list[str] = field(default_factory=list)
    computed_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def score_confluence(inp: ConfluenceInput) -> ConfluenceOutput:
    """Compute weighted confluence score + apply gates.

    Score formula (synthesis §V):
      score = W_REGIME × regime + W_ZONE × zone + W_MACRO × macro + W_HERMES × hermes

    Decision gates (in priority order):
      1. Calibration gate: if mean_brier provided and > 0.25 → HOLD
      2. Score threshold: if score > 0.65 → PROCEED; if 0.50 ≤ score ≤ 0.65 → SABAR;
         if 0.30 ≤ score < 0.50 → HOLD; if score < 0.30 → BLOCK

    The calibration gate is the sovereign override per synthesis gap5
    ("CHRON Brier calibration gate on position sizing").

    PROCEED = strong confluence, low calibration risk, align the trade
    SABAR   = borderline; wait for clearer signal or smaller size
    HOLD    = conflicting evidence; do not enter
    BLOCK   = strong adverse confluence; exit if held
    """
    # Clamp inputs
    r = clamp01(inp.regime_score)
    z = clamp01(inp.zone_quality)
    m = clamp01(inp.macro_alignment)
    h = clamp01(inp.hermes_signal)

    raw_score = W_REGIME * r + W_ZONE * z + W_MACRO * m + W_HERMES * h
    score = round(raw_score, 4)

    breakdown = {
        "regime": {
            "score": round(r, 4),
            "weight": W_REGIME,
            "contribution": round(W_REGIME * r, 4),
            "label": inp.regime_label,
        },
        "zone": {
            "score": round(z, 4),
            "weight": W_ZONE,
            "contribution": round(W_ZONE * z, 4),
        },
        "macro": {
            "score": round(m, 4),
            "weight": W_MACRO,
            "contribution": round(W_MACRO * m, 4),
            "channel": inp.macro_channel,
        },
        "hermes": {
            "score": round(h, 4),
            "weight": W_HERMES,
            "contribution": round(W_HERMES * h, 4),
            "aligned_signals": inp.hermes_signal_count,
        },
    }

    gates: dict = {}
    notes = list(inp.notes)

    # Gate 1: CHRON calibration
    if inp.mean_brier is not None:
        brier_ok = inp.mean_brier <= CALIBRATION_GATE_BRIER
        gates["calibration"] = {
            "mean_brier": inp.mean_brier,
            "threshold": CALIBRATION_GATE_BRIER,
            "passed": brier_ok,
        }
        if not brier_ok:
            notes.append(
                f"calibration gate HOLD: mean_brier={inp.mean_brier:.4f} > {CALIBRATION_GATE_BRIER}"
            )

    # Gate 2: Event risk timer gate (CHRON macro risk window)
    if inp.event_risk and inp.event_risk.get("risk_active"):
        gates["event_risk"] = {
            "active_events": [e.get("title") for e in inp.event_risk.get("active_events", [])],
            "passed": False,
        }
        notes.append("macro event risk active: trade gated by CHRON event timer")

    # Gate 3: Score thresholds
    if score > THRESHOLD_PROCEED:
        decision = "PROCEED"
    elif score >= 0.50:
        decision = "SABAR"
    elif score >= 0.30:
        decision = "HOLD"
    else:
        decision = "BLOCK"

    # Override on calibration gate failure
    if not gates.get("calibration", {}).get("passed", True):
        decision = "HOLD"

    # Override on event risk gate failure (downgrade PROCEED to SABAR or HOLD)
    if not gates.get("event_risk", {}).get("passed", True):
        if decision == "PROCEED":
            decision = "SABAR"

    return ConfluenceOutput(
        instrument=inp.instrument,
        score=score,
        breakdown=breakdown,
        decision=decision,
        gates=gates,
        seasonal=inp.seasonal_bias,
        event_risk=inp.event_risk,
        notes=notes,
        computed_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )


def hermes_signal_from_adjustments(adjustments: list[dict]) -> tuple[float, int]:
    """Derive hermes_signal score from HERMES→WEALTH adjustments.

    Args:
      adjustments: list of adjustment dicts from hermes_wealth_bridge

    Returns:
      (score, count) — score is 0.5 (neutral) if no adjustments;
        score moves up for positive deltas, down for negative deltas.

    Algorithm:
      - positive delta → +0.05 per signal (capped +0.15)
      - negative delta → -0.05 per signal (capped -0.15)
      - 0.5 baseline
    """
    if not adjustments:
        return 0.5, 0

    net_delta = sum(a.get("delta", 0.0) for a in adjustments)
    # Net delta of +0.30 (3 positive deltas of +0.10) = +0.15 boost. Symmetric for negative.
    capped = max(-0.15, min(0.15, net_delta * 0.5))
    score = 0.5 + capped
    return clamp01(score), len(adjustments)


def log_confluence(out: ConfluenceOutput, path: Path = OUTPUT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(out.to_dict(), default=str) + "\n")


# ── CLI ────────────────────────────────────────────────────────


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="CHRON confluence scorer")
    ap.add_argument(
        "--instrument",
        type=str,
        required=True,
        help="XAUUSD | OIL | GAS | KLCI | USMYR",
    )
    ap.add_argument(
        "--regime",
        type=float,
        required=True,
        help="Regime score 0..1 (UP=1.0, SIDEWAYS=0.5, DOWN=0.0)",
    )
    ap.add_argument(
        "--zone",
        type=float,
        required=True,
        help="Zone quality 0..1 (strength 3/3+ = high)",
    )
    ap.add_argument("--macro", type=float, required=True, help="Macro alignment 0..1")
    ap.add_argument(
        "--hermes",
        type=float,
        required=True,
        help="HERMES signal alignment 0..1 (0.5 = neutral)",
    )
    ap.add_argument(
        "--direction", type=str, default="up", choices=["up", "down", "range"]
    )
    ap.add_argument(
        "--regime-label", type=str, default="", help="UPTREND | DOWNTREND | SIDEWAYS"
    )
    ap.add_argument("--macro-channel", type=str, default="")
    ap.add_argument("--hermes-count", type=int, default=0)
    ap.add_argument(
        "--mean-brier",
        type=float,
        default=None,
        help="CHRON mean_brier for calibration gate",
    )
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    # Auto-fetch seasonal bias and event timers if modules available
    s_bias = None
    try:
        from chron_seasonal import get_seasonal_bias
        s_bias = get_seasonal_bias(args.instrument).to_dict()
    except Exception:
        pass

    e_risk = None
    try:
        from chron_event_timers import check_instrument_event_risk
        e_risk = check_instrument_event_risk(args.instrument)
    except Exception:
        pass

    inp = ConfluenceInput(
        instrument=args.instrument,
        regime_score=args.regime,
        zone_quality=args.zone,
        macro_alignment=args.macro,
        hermes_signal=args.hermes,
        mean_brier=args.mean_brier,
        direction=args.direction,
        regime_label=args.regime_label,
        macro_channel=args.macro_channel,
        hermes_signal_count=args.hermes_count,
        seasonal_bias=s_bias,
        event_risk=e_risk,
    )

    out = score_confluence(inp)
    log_confluence(out)

    if not args.quiet:
        print(
            f"Confluence — {args.instrument} ({args.direction}) — {datetime.now(MYT).strftime('%Y-%m-%d %H:%M MYT')}"
        )
        print(
            f"  Regime     {out.breakdown['regime']['score']:.4f} × {W_REGIME} = {out.breakdown['regime']['contribution']:.4f}  [{args.regime_label or '-'}]"
        )
        print(
            f"  Zone       {out.breakdown['zone']['score']:.4f} × {W_ZONE} = {out.breakdown['zone']['contribution']:.4f}"
        )
        print(
            f"  Macro      {out.breakdown['macro']['score']:.4f} × {W_MACRO} = {out.breakdown['macro']['contribution']:.4f}  [{args.macro_channel or '-'}]"
        )
        print(
            f"  HERMES     {out.breakdown['hermes']['score']:.4f} × {W_HERMES} = {out.breakdown['hermes']['contribution']:.4f}  ({args.hermes_count} signals)"
        )
        print(f"  SCORE: {out.score:.4f}")
        if out.gates:
            print(f"  Gates: {json.dumps(out.gates, indent=None)}")
        print(f"  DECISION: {out.decision}")
        if out.notes:
            for n in out.notes:
                print(f"    note: {n}")
        print(f"  Log: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
