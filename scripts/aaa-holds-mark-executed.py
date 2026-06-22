#!/usr/bin/env python3
"""
Mark an 888_HOLD as executed in the state file.
Called by OpenClaw agent after successful execution.

Usage: python3 aaa-holds-mark-executed.py <hold_id>
"""
import json
import sys
from pathlib import Path

STATE_FILE = Path("/root/.openclaw/workspace/.aaa-holds-state.json")


def main():
    if len(sys.argv) < 2:
        print("Usage: aaa-holds-mark-executed.py <hold_id>", file=sys.stderr)
        sys.exit(1)

    hold_id = sys.argv[1]

    state = {"executed": [], "pending": [], "last_check": None}
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
        except Exception:
            pass

    if hold_id in state.get("pending", []):
        state["pending"].remove(hold_id)

    if hold_id not in state.get("executed", []):
        state["executed"].append(hold_id)

    STATE_FILE.write_text(json.dumps(state, indent=2))
    print(f"OK: Hold {hold_id} marked as executed.")


if __name__ == "__main__":
    main()
