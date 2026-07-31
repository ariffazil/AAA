#!/usr/bin/env python3
"""
qwen_credit_monitor.py — Qwen Token Plan Credit Monitor
═══════════════════════════════════════════════════════════
Cron: every 5 minutes · Action: probe health + estimate credit usage
Output: /root/.local/share/arifos/qwen_credits.json
Throttle: >80% of 7-day OR 5-hour window → throttle flag ON

Plan limits (Individual Pro):
  - 40,000 Credits per 7 days
  - 12,000 Credits per 5 hours
  - Credit Packs: $15/20K Credits (up to 5)

Since Qwen's billing API requires browser cookies (not API key),
this monitor uses a HEURISTIC approach:
  1. Probe /v1/models to verify key liveness
  2. Estimate credits from tracked token usage in token_bank.db
  3. Hard throttle: probe actual chat request for latency as health signal
  4. Write throttle flag when estimated usage > 80% of any window

DITEMPA BUKAN DIBERI.
"""

import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Config ────────────────────────────────────────────────────
STATE_FILE = Path("/root/.local/share/arifos/qwen_credits.json")
TOKEN_BANK_DB = Path("/root/.local/share/arifos/token_bank.db")
THROTTLE_FILE = Path("/root/.local/share/arifos/qwen_throttle")
LOG_FILE = Path("/root/.local/share/arifos/qwen_credit_monitor.log")

PLAN_CREDITS_7D = 40_000
PLAN_CREDITS_5HR = 12_000
THROTTLE_PCT = 0.80

QWEN_KEY = os.environ.get("QWEN_API_KEY", "")
QWEN_URL = "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"

# Approximate credit-to-token ratios per model
# These are CONSERVATIVE estimates (overestimate credit consumption)
# Actual coefficients are tiered and proprietary to Qwen Cloud
CREDIT_PER_1K_INPUT = {
    "deepseek-v4-pro": 0.5,
    "qwen3.7-max": 0.6,
    "qwen3.7-plus": 0.4,
    "qwen3.6-flash": 0.15,
    "glm-5.2": 0.4,
    "qwen3.8-max-preview": 0.05,  # 90% off promo
}
CREDIT_PER_1K_OUTPUT = {
    "deepseek-v4-pro": 1.5,
    "qwen3.7-max": 1.8,
    "qwen3.7-plus": 1.2,
    "qwen3.6-flash": 0.5,
    "glm-5.2": 1.2,
    "qwen3.8-max-preview": 0.15,  # 90% off promo
}
DEFAULT_INPUT_RATE = 0.5
DEFAULT_OUTPUT_RATE = 1.5


def log(msg: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def probe_key_liveness() -> dict:
    """Probe Qwen Token Plan key liveness via /v1/models."""
    try:
        result = subprocess.run(
            [
                "curl",
                "-s",
                "-w",
                "\n%{http_code}\n%{time_total}",
                f"{QWEN_URL}/models",
                "-H",
                f"Authorization: Bearer {QWEN_KEY}",
                "--max-time",
                "8",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        lines = result.stdout.strip().split("\n")
        if len(lines) < 2:
            return {"alive": False, "error": "unexpected_output"}

        http_code = lines[-2].strip()
        latency = float(lines[-1].strip()) if lines[-1].strip() else 0

        if http_code == "200":
            try:
                body = json.loads("\n".join(lines[:-2]))
                models = [m["id"] for m in body.get("data", [])]
                return {
                    "alive": True,
                    "models": len(models),
                    "model_list": models,
                    "latency_s": latency,
                    "http_code": int(http_code),
                }
            except json.JSONDecodeError:
                return {"alive": True, "models": "parse_error", "latency_s": latency}
        else:
            return {"alive": False, "http_code": int(http_code), "latency_s": latency}
    except Exception as e:
        return {"alive": False, "error": str(e)}


def estimate_credits_from_token_bank() -> dict:
    """Estimate credit usage from token_bank.db (last 7d and 5hr)."""
    usage_7d = {"input_tokens": 0, "output_tokens": 0, "credits": 0.0, "requests": 0}
    usage_5hr = {"input_tokens": 0, "output_tokens": 0, "credits": 0.0, "requests": 0}

    if not TOKEN_BANK_DB.exists():
        return {"7d": usage_7d, "5hr": usage_5hr, "note": "no_token_bank_db"}

    now = datetime.now(timezone.utc)
    cutoff_7d = now - timedelta(days=7)
    cutoff_5hr = now - timedelta(hours=5)

    try:
        conn = sqlite3.connect(str(TOKEN_BANK_DB))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Try to query spend records — schema may vary
        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

        spend_table = None
        for t in ["token_spend", "spend_records", "spend", "usage"]:
            if t in tables:
                spend_table = t
                break

        if spend_table:
            # Query last 7 days
            cur.execute(
                f"SELECT model, input_tokens, output_tokens, created_at FROM {spend_table} WHERE created_at >= ?",
                (cutoff_7d.isoformat(),),
            )
            for row in cur.fetchall():
                model = row["model"] or "unknown"
                inp = row["input_tokens"] or 0
                out = row["output_tokens"] or 0
                inp_rate = CREDIT_PER_1K_INPUT.get(model, DEFAULT_INPUT_RATE)
                out_rate = CREDIT_PER_1K_OUTPUT.get(model, DEFAULT_OUTPUT_RATE)

                usage_7d["input_tokens"] += inp
                usage_7d["output_tokens"] += out
                usage_7d["credits"] += (inp / 1000) * inp_rate + (out / 1000) * out_rate
                usage_7d["requests"] += 1

                if row["created_at"] >= cutoff_5hr.isoformat():
                    usage_5hr["input_tokens"] += inp
                    usage_5hr["output_tokens"] += out
                    usage_5hr["credits"] += (inp / 1000) * inp_rate + (out / 1000) * out_rate
                    usage_5hr["requests"] += 1

        conn.close()
    except Exception as e:
        return {"7d": usage_7d, "5hr": usage_5hr, "note": f"db_error: {e}"}

    return {"7d": usage_7d, "5hr": usage_5hr}


def estimate_credits_from_state() -> dict:
    """Fallback: read from persisted state file to estimate credits."""
    usage_7d = {"input_tokens": 0, "output_tokens": 0, "credits": 0.0, "requests": 0}
    usage_5hr = {"input_tokens": 0, "output_tokens": 0, "credits": 0.0, "requests": 0}

    if not STATE_FILE.exists():
        return {"7d": usage_7d, "5hr": usage_5hr, "note": "no_state_file"}

    try:
        state = json.loads(STATE_FILE.read_text())
        usage_7d = state.get("usage_7d", usage_7d)
        usage_5hr = state.get("usage_5hr", usage_5hr)
    except Exception:
        pass

    return {"7d": usage_7d, "5hr": usage_5hr}


def compute_throttle(usage: dict) -> dict:
    """Determine throttle state from credit usage."""
    pct_7d = min(1.0, usage["7d"]["credits"] / PLAN_CREDITS_7D) if PLAN_CREDITS_7D else 0
    pct_5hr = min(1.0, usage["5hr"]["credits"] / PLAN_CREDITS_5HR) if PLAN_CREDITS_5HR else 0
    max_pct = max(pct_7d, pct_5hr)

    throttle = max_pct >= THROTTLE_PCT

    return {
        "throttle": throttle,
        "pct_7d": round(pct_7d * 100, 1),
        "pct_5hr": round(pct_5hr * 100, 1),
        "pct_max": round(max_pct * 100, 1),
        "window_breached": "7d" if pct_7d >= THROTTLE_PCT else ("5hr" if pct_5hr >= THROTTLE_PCT else None),
        "recommendation": "USE_FLASH_ONLY" if throttle else "USE_NORMALLY",
    }


def write_state(state: dict):
    """Write state to JSON file and throttle flag."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, default=str))

    if state.get("throttle", {}).get("throttle", False):
        THROTTLE_FILE.write_text("1")
        log(
            f"🚨 THROTTLE: {state['throttle']['pct_7d']}% 7d / {state['throttle']['pct_5hr']}% 5hr — {state['throttle']['recommendation']}"
        )
    else:
        if THROTTLE_FILE.exists():
            THROTTLE_FILE.unlink()
            log("✅ THROTTLE CLEARED")


def main():
    log("── Qwen Credit Monitor ──")

    # 1. Probe key liveness
    probe = probe_key_liveness()
    log(f"  Probe: alive={probe.get('alive')} models={probe.get('models', '?')} latency={probe.get('latency_s', '?')}s")

    if not probe.get("alive"):
        log("  ⚠️ Key probe failed — writing degraded state")
        state = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "key_alive": False,
            "probe": probe,
            "throttle": {
                "throttle": True,
                "recommendation": "KEY_DEAD_FALLBACK_TO_BAILIAN",
                "reason": "key_probe_failed",
            },
        }
        write_state(state)
        return

    # 2. Estimate credit usage
    db_usage = estimate_credits_from_token_bank()
    state_usage = estimate_credits_from_state()

    # Merge: prefer DB over state file
    usage = db_usage if db_usage["7d"]["credits"] > 0 else state_usage

    # 3. Compute throttle
    throttle = compute_throttle(usage)

    # 4. Build state
    state = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "plan": {
            "tier": "Individual Pro",
            "credits_7d": PLAN_CREDITS_7D,
            "credits_5hr": PLAN_CREDITS_5HR,
            "throttle_pct": int(THROTTLE_PCT * 100),
        },
        "key_alive": True,
        "probe": probe,
        "usage_7d": usage["7d"],
        "usage_5hr": usage["5hr"],
        "throttle": throttle,
    }

    write_state(state)

    # Summary
    u = usage["7d"]
    log(
        f"  7d: {u['credits']:.1f} credits | {u['input_tokens']:,} in + {u['output_tokens']:,} out | {u['requests']} req — {throttle['pct_7d']}%"
    )
    u5 = usage["5hr"]
    log(
        f"  5hr: {u5['credits']:.1f} credits | {u5['input_tokens']:,} in + {u5['output_tokens']:,} out | {u5['requests']} req — {throttle['pct_5hr']}%"
    )
    log(f"  Verdict: {'🚨 THROTTLE' if throttle['throttle'] else '✅ NORMAL'} → {throttle['recommendation']}")


if __name__ == "__main__":
    main()
