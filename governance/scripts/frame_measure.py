#!/usr/bin/env python3
"""FRAME — W-Vector Measurement Infrastructure

Computes 5 measurable W-vector dimensions from existing telemetry.
No new data collection required — this is computation on existing signals.

Usage: python3 frame_measure.py [--json] [--verbose]

Dimensions:
  W1: Objective Fidelity (RSI ledger)
  W2: Authority Boundary Integrity (SCT + arif_judge — GAP: no structured log)
  W3: Context Integrity (carry_forward open loop tracking)
  W4: Tool Control (forge_shell_ledger — GAP: no structured log)
  W5: Feedback Integrity (RSI ledger — diagnosis → remediation ratio)

Aggregated: W = weighted average with w2=2.0 (authority load-bearing)
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

RSI_LEDGER = Path("/root/.local/share/arifos/rsi-ledger.jsonl")
CARRY_FORWARD = Path("/root/.local/share/arifos/carry_forward.json")

# Default weights (F13 can override)
WEIGHTS = {"w1": 1.0, "w2": 2.0, "w3": 0.5, "w4": 0.5, "w5": 1.0}

THRESHOLDS = {
    "CAUTION": 0.5,
    "HOLD": 0.3,
}


def load_rsi_ledger():
    entries = []
    if RSI_LEDGER.exists():
        for line in RSI_LEDGER.read_text().splitlines():
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def load_carry_forward():
    if CARRY_FORWARD.exists():
        return json.loads(CARRY_FORWARD.read_text())
    return {}


def compute_w1(entries):
    """W1 — Objective Fidelity: ratio of sessions that advanced declared objective."""
    if not entries:
        return {"score": None, "numerator": 0, "denominator": 0, "verdict": "NO_DATA"}

    total = 0
    advanced = 0

    for d in entries:
        total += 1
        bottleneck = d.get("bottleneck", "")
        fix_installed = d.get("fix_installed", False)
        fix = d.get("fix", d.get("fix_description", ""))
        remediate = d.get("remediate", {})
        if isinstance(remediate, dict):
            fix_installed = fix_installed or remediate.get("fix_installed", False)

        if fix == "none_required" or fix == "none":
            advanced += 1
        elif fix_installed and fix_installed != "False":
            advanced += 1
        elif bottleneck and bottleneck not in ("none", ""):
            pass  # unresolved bottleneck = not advanced
        else:
            advanced += 1  # default: assume objective met

    score = advanced / total if total > 0 else 0
    verdict = "OK" if score >= 0.5 else ("CAUTION" if score >= 0.3 else "HOLD")

    return {
        "score": round(score, 3),
        "numerator": advanced,
        "denominator": total,
        "verdict": verdict,
        "threshold_caution": 0.5,
        "threshold_hold": 0.3,
    }


def compute_w2():
    """W2 — Authority Boundary Integrity: SCT token claims + arif_judge log.
    GAP: No structured log exists for authority boundary violations.
    Returns NO_DATA until infrastructure is built."""
    return {
        "score": None,
        "verdict": "NO_DATA",
        "gap": "No structured SCT claims log or arif_judge verdict log exists. "
        "W2 requires: (1) SCT token claim audit trail, (2) arif_judge verdict log with "
        "action_class and gating outcome. Signal source: arifOS kernel :8088.",
        "recommendation": "Instrument arifOS kernel to append authority claims to "
        "/root/.local/share/arifos/authority-claims.jsonl",
    }


def compute_w3(cf):
    """W3 — Context Integrity: open loop tracking across sessions."""
    open_loops = cf.get("open_loops_888_HOLD", [])
    resolved = cf.get("resolved_this_session", [])

    # Count actual open loops (filter out resolved strings and dicts)
    actual_open = [
        x for x in open_loops
        if isinstance(x, dict) and x.get("status") not in ("RESOLVED", "resolved")
    ]
    resolved_count = len(resolved)

    # W3: ratio of resolved vs total (resolved + open)
    total = resolved_count + len(actual_open)
    score = resolved_count / total if total > 0 else 1.0  # no loops = perfect
    verdict = "OK" if score >= 0.5 else ("CAUTION" if score >= 0.3 else "HOLD")

    return {
        "score": round(score, 3),
        "resolved": resolved_count,
        "open": len(actual_open),
        "total": total,
        "verdict": verdict,
        "open_loop_ids": [x.get("id", "unknown") for x in actual_open],
    }


def compute_w4():
    """W4 — Tool Control: least-power routing ratio.
    GAP: No forge_shell_ledger exists to measure tool power usage.
    Returns NO_DATA until infrastructure is built."""
    return {
        "score": None,
        "verdict": "NO_DATA",
        "gap": "No forge_shell_ledger or tool call power-classification log exists. "
        "W4 requires: (1) tool call log with power class per call, "
        "(2) route-least-power decision tracking.",
        "recommendation": "Instrument A-FORGE to log tool calls with power classification "
        "to /root/.local/share/arifos/tool-power-log.jsonl",
    }


def compute_w5(entries):
    """W5 — Feedback Integrity: diagnosis → remediation ratio."""
    diagnosed = 0
    remediated = 0

    for d in entries:
        bottleneck = d.get("bottleneck", "")
        fix_installed = d.get("fix_installed", False)
        remediate = d.get("remediate", {})
        if isinstance(remediate, dict):
            fix_installed = fix_installed or remediate.get("fix_installed", False)

        if bottleneck and bottleneck not in ("none", ""):
            diagnosed += 1
            if fix_installed and fix_installed != "False":
                remediated += 1

    score = remediated / diagnosed if diagnosed > 0 else 0
    verdict = "OK" if score >= 0.5 else ("CAUTION" if score >= 0.2 else "HOLD")

    return {
        "score": round(score, 3),
        "numerator": remediated,
        "denominator": diagnosed,
        "verdict": verdict,
        "threshold_caution": 0.5,
        "threshold_hold": 0.2,
    }


def compute_aggregate(w_scores, weights=WEIGHTS):
    """Weighted average of available dimensions. Missing dimensions excluded."""
    available = {}
    for dim, score_data in w_scores.items():
        if score_data.get("score") is not None:
            available[dim] = score_data["score"]

    if not available:
        return {"score": None, "verdict": "NO_DATA", "available_dims": 0}

    total_weight = sum(weights.get(f"w{i+1}", 1.0) for i, dim in enumerate(
        ["w1", "w2", "w3", "w4", "w5"]
    ) if dim.replace("w", "w") in [k.replace("w", "w") for k in available.keys()])

    # Simpler: just use available dimensions
    weighted_sum = 0
    weight_sum = 0
    dim_map = {"W1": "w1", "W2": "w2", "W3": "w3", "W4": "w4", "W5": "w5"}
    for dim_key, score in available.items():
        w_key = dim_map.get(dim_key, dim_key.lower())
        w = weights.get(w_key, 1.0)
        weighted_sum += score * w
        weight_sum += w

    agg = weighted_sum / weight_sum if weight_sum > 0 else 0
    verdict = "OK" if agg >= 0.5 else ("CAUTION" if agg >= 0.3 else "HOLD")

    return {
        "score": round(agg, 3),
        "verdict": verdict,
        "available_dims": len(available),
        "missing_dims": 5 - len(available),
        "weights_used": {k: v for k, v in weights.items() if k in [dim_map.get(d, d) for d in available]},
    }


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    as_json = "--json" in sys.argv

    entries = load_rsi_ledger()
    cf = load_carry_forward()

    w_scores = {
        "W1": compute_w1(entries),
        "W2": compute_w2(),
        "W3": compute_w3(cf),
        "W4": compute_w4(),
        "W5": compute_w5(entries),
    }

    aggregate = compute_aggregate(w_scores)

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dimensions": w_scores,
        "aggregate": aggregate,
        "rsi_entries": len(entries),
        "carry_forward_loops": len(cf.get("open_loops_888_HOLD", [])),
    }

    if as_json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 60)
        print("FRAME — W-Vector Measurement Report")
        print(f"Timestamp: {result['timestamp']}")
        print(f"RSI entries: {result['rsi_entries']}")
        print("=" * 60)

        for dim, data in w_scores.items():
            score = data.get("score", "N/A")
            verdict = data.get("verdict", "UNKNOWN")
            icon = "✅" if verdict == "OK" else ("⚠️" if verdict == "CAUTION" else ("🔴" if verdict == "HOLD" else "❓"))
            print(f"\n{icon} {dim}: {score} — {verdict}")
            if verbose and data.get("gap"):
                print(f"   GAP: {data['gap']}")
            if verbose and data.get("recommendation"):
                print(f"   REC: {data['recommendation']}")
            if dim == "W3" and data.get("open_loop_ids"):
                print(f"   Open loops: {data['open_loop_ids']}")

        print(f"\n{'=' * 60}")
        agg_score = aggregate.get("score", "N/A")
        agg_verdict = aggregate.get("verdict", "UNKNOWN")
        agg_icon = "✅" if agg_verdict == "OK" else ("⚠️" if agg_verdict == "CAUTION" else ("🔴" if agg_verdict == "HOLD" else "❓"))
        print(f"{agg_icon} AGGREGATE W: {agg_score} — {agg_verdict}")
        print(f"   Available dims: {aggregate.get('available_dims', 0)}/5")
        print(f"   Missing dims: {aggregate.get('missing_dims', 0)}")
        print("=" * 60)


if __name__ == "__main__":
    main()
