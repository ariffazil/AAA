#!/usr/bin/env python3
"""
qwen_throttle_check.py — Agent-facing throttle check
═══════════════════════════════════════════════════════
Reads /root/.local/share/arifos/qwen_credits.json
Returns: exit 0 = OK, exit 1 = THROTTLE (route to flash)
Usage: python3 qwen_throttle_check.py [--json]
"""

import json
import sys
from pathlib import Path

STATE_FILE = Path("/root/.local/share/arifos/qwen_credits.json")
THROTTLE_FILE = Path("/root/.local/share/arifos/qwen_throttle")


def check():
    # Fast path: check throttle flag file first
    if THROTTLE_FILE.exists():
        return {"throttle": True, "reason": "throttle_flag_file", "recommendation": "USE_FLASH_ONLY"}

    if not STATE_FILE.exists():
        return {"throttle": False, "reason": "no_state", "recommendation": "USE_NORMALLY"}

    try:
        state = json.loads(STATE_FILE.read_text())
        t = state.get("throttle", {})
        return {
            "throttle": t.get("throttle", False),
            "pct_7d": t.get("pct_7d", 0),
            "pct_5hr": t.get("pct_5hr", 0),
            "pct_max": t.get("pct_max", 0),
            "window": t.get("window_breached"),
            "recommendation": t.get("recommendation", "USE_NORMALLY"),
            "timestamp": state.get("timestamp", "unknown"),
        }
    except Exception as e:
        return {"throttle": False, "reason": f"parse_error:{e}", "recommendation": "USE_NORMALLY"}


if __name__ == "__main__":
    result = check()
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        status = "🚨 THROTTLE" if result["throttle"] else "✅ OK"
        print(f"Qwen Token Plan: {status}")
        if result.get("pct_max"):
            print(f"  Credit usage: {result['pct_max']}% (7d: {result['pct_7d']}%, 5hr: {result['pct_5hr']}%)")
        print(f"  → {result['recommendation']}")

    sys.exit(1 if result["throttle"] else 0)
