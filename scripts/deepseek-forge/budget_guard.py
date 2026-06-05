#!/usr/bin/env python3
"""
DeepSeek Budget Guard — Federation Cost Enforcer
═══════════════════════════════════════════════════
Tracks every DeepSeek API call across the arifOS federation.
Hard stop at $4.75. Alert at $4.00. Warn at $3.00.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

VAULT_PATH = Path("/root/.arifos/deepseek_budget.jsonl")
BUDGET_CEILING = 4.75
ALERT_THRESHOLD = 4.00
WARN_THRESHOLD = 3.00

# Pricing per 1M tokens (USD)
PRICING = {
    "deepseek-v4-flash": {
        "input_cache_hit": 0.0028,
        "input_cache_miss": 0.14,
        "output": 0.28,
    },
    "deepseek-v4-pro": {
        "input_cache_hit": 0.003625,
        "input_cache_miss": 0.435,
        "output": 0.87,
    },
}


def _load_ledger() -> list[dict]:
    if not VAULT_PATH.exists():
        return []
    return [json.loads(line) for line in VAULT_PATH.read_text().splitlines() if line.strip()]


def _save_entry(entry: dict) -> None:
    VAULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with VAULT_PATH.open("a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


def current_spend() -> float:
    """Total USD spent so far."""
    return sum(e.get("cost_usd", 0.0) for e in _load_ledger())


def check_budget() -> dict:
    """Return budget status. Raise if exceeded."""
    spent = current_spend()
    remaining = BUDGET_CEILING - spent

    status = {
        "spent_usd": round(spent, 4),
        "remaining_usd": round(remaining, 4),
        "ceiling_usd": BUDGET_CEILING,
        "percent_used": round(spent / BUDGET_CEILING * 100, 1),
        "verdict": "PROCEED",
        "timestamp": datetime.now(UTC).isoformat(),
    }

    if spent >= BUDGET_CEILING:
        status["verdict"] = "HOLD"
        status["reason"] = f"Budget ceiling ${BUDGET_CEILING} exceeded. Spent: ${spent:.4f}"
        raise RuntimeError(status["reason"])

    if spent >= ALERT_THRESHOLD:
        status["verdict"] = "ALERT"
        status["reason"] = f"Budget alert: ${spent:.4f} / ${BUDGET_CEILING}"
    elif spent >= WARN_THRESHOLD:
        status["verdict"] = "WARN"
        status["reason"] = f"Budget warning: ${spent:.4f} / ${BUDGET_CEILING}"

    return status


def estimate_cost(model: str, input_tokens: int, output_tokens: int, cache_hit_ratio: float = 0.5) -> float:
    """Estimate cost for a call before making it."""
    rates = PRICING.get(model, PRICING["deepseek-v4-flash"])
    input_hit = input_tokens * cache_hit_ratio * (rates["input_cache_hit"] / 1_000_000)
    input_miss = input_tokens * (1 - cache_hit_ratio) * (rates["input_cache_miss"] / 1_000_000)
    output_cost = output_tokens * (rates["output"] / 1_000_000)
    return input_hit + input_miss + output_cost


def log_usage(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_hit_tokens: int = 0,
    purpose: str = "",
    actor: str = "anonymous",
) -> dict:
    """Log a completed call and return cost breakdown."""
    rates = PRICING.get(model, PRICING["deepseek-v4-flash"])
    cache_miss = input_tokens - cache_hit_tokens

    cost_hit = cache_hit_tokens * (rates["input_cache_hit"] / 1_000_000)
    cost_miss = cache_miss * (rates["input_cache_miss"] / 1_000_000)
    cost_out = output_tokens * (rates["output"] / 1_000_000)
    total = cost_hit + cost_miss + cost_out

    entry = {
        "ts": datetime.now(UTC).isoformat(),
        "model": model,
        "input_tokens": input_tokens,
        "cache_hit_tokens": cache_hit_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(total, 6),
        "cost_breakdown": {
            "input_hit": round(cost_hit, 6),
            "input_miss": round(cost_miss, 6),
            "output": round(cost_out, 6),
        },
        "purpose": purpose,
        "actor": actor,
    }
    _save_entry(entry)
    return entry


def report() -> dict:
    """Generate a human-readable budget report."""
    ledger = _load_ledger()
    if not ledger:
        return {"message": "No DeepSeek usage yet. Budget: $5.00 / $4.75 guarded."}

    total = sum(e["cost_usd"] for e in ledger)
    by_model: dict[str, dict] = {}
    by_actor: dict[str, float] = {}

    for e in ledger:
        m = e["model"]
        by_model.setdefault(m, {"calls": 0, "tokens_in": 0, "tokens_out": 0, "cost": 0.0})
        by_model[m]["calls"] += 1
        by_model[m]["tokens_in"] += e["input_tokens"]
        by_model[m]["tokens_out"] += e["output_tokens"]
        by_model[m]["cost"] += e["cost_usd"]

        a = e.get("actor", "unknown")
        by_actor[a] = by_actor.get(a, 0.0) + e["cost_usd"]

    return {
        "total_spent_usd": round(total, 4),
        "remaining_usd": round(BUDGET_CEILING - total, 4),
        "calls_total": len(ledger),
        "by_model": {k: {kk: round(vv, 4) if isinstance(vv, float) else vv for kk, vv in v.items()} for k, v in by_model.items()},
        "by_actor": {k: round(v, 4) for k, v in by_actor.items()},
        "status": check_budget()["verdict"],
    }


if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"

    if cmd == "report":
        print(json.dumps(report(), indent=2))
    elif cmd == "check":
        print(json.dumps(check_budget(), indent=2))
    elif cmd == "estimate":
        # usage: budget_guard.py estimate <model> <input_tokens> <output_tokens> [cache_hit_ratio]
        if len(sys.argv) < 5:
            print("Usage: budget_guard.py estimate <model> <input_tokens> <output_tokens> [cache_hit_ratio]")
            raise SystemExit(1)
        model = sys.argv[2]
        inp = sys.argv[3]
        out = sys.argv[4]
        rest = sys.argv[5:]
        ratio = float(rest[0]) if rest else 0.5
        cost = estimate_cost(model, int(inp), int(out), ratio)
        print(f"Estimated cost: ${cost:.6f} USD")
    else:
        print("Usage: budget_guard.py [report|check|estimate <model> <input> <output> [ratio]]")
