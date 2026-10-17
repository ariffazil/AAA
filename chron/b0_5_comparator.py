"""
B0.5 OFFLINE INSTRUMENTATION — expanding-window base-rate comparator.

Pure test-local function. No runtime wiring. No CHRON writes. No
arifFlow / VAULT999 / Claim Ledger / A-FORGE / kernel mutations.
"""
from __future__ import annotations

from typing import Callable, Dict, Sequence, Tuple


def brier(p: float, y: int) -> float:
    return (p - y) ** 2


def expand_window(
    predictions: Sequence[dict],
    outcomes: Dict[str, int],
    duplicate_identity_rule: Callable[[dict], str],
    evaluation_window: Tuple[float, float],
    exclude_current: bool = True,
) -> dict:
    t_start, t_end = evaluation_window

    in_window = [p for p in predictions if t_start <= p.get("timestamp", -1) <= t_end]

    raw_count = len(in_window)
    collapsed: Dict[str, dict] = {}
    for p in in_window:
        k = duplicate_identity_rule(p)
        collapsed[k] = p
    effective = list(collapsed.values())
    duplicate_rows_collapsed = raw_count - len(effective)

    if exclude_current and effective:
        effective_for_baseline = effective[:-1]
    else:
        effective_for_baseline = effective

    insufficient = {
        "model_brier": None,
        "base_rate_probability": None,
        "base_rate_brier": None,
        "effective_sample_count": len(effective),
        "raw_sample_count": raw_count,
        "duplicate_rows_collapsed": duplicate_rows_collapsed,
        "evaluation_window": evaluation_window,
        "model_beats_baseline": None,
        "insufficient_evidence": True,
    }

    if len(effective_for_baseline) < 2:
        return insufficient

    model_brier_sum = 0.0
    model_n = 0
    for p in effective:
        pid = p.get("prediction_id")
        if pid not in outcomes:
            continue
        prob = float(p.get("predicted_probability", 0.5))
        outc = int(outcomes[pid])
        model_brier_sum += brier(prob, outc)
        model_n += 1
    if model_n == 0:
        return insufficient

    model_brier = model_brier_sum / model_n

    n_pos = 0
    n_total = 0
    for p in effective_for_baseline:
        pid = p.get("prediction_id")
        if pid not in outcomes:
            continue
        n_pos += int(outcomes[pid])
        n_total += 1
    if n_total == 0:
        return {
            "model_brier": model_brier,
            "base_rate_probability": None,
            "base_rate_brier": None,
            "effective_sample_count": len(effective),
            "raw_sample_count": raw_count,
            "duplicate_rows_collapsed": duplicate_rows_collapsed,
            "evaluation_window": evaluation_window,
            "model_beats_baseline": None,
            "insufficient_evidence": True,
        }
    base_rate = n_pos / n_total
    current_outcome = int(outcomes.get(effective[-1].get("prediction_id"), 0))
    base_rate_brier = brier(base_rate, current_outcome)

    return {
        "model_brier": model_brier,
        "base_rate_probability": base_rate,
        "base_rate_brier": base_rate_brier,
        "effective_sample_count": len(effective),
        "raw_sample_count": raw_count,
        "duplicate_rows_collapsed": duplicate_rows_collapsed,
        "evaluation_window": evaluation_window,
        "model_beats_baseline": model_brier < base_rate_brier,
        "insufficient_evidence": False,
    }
