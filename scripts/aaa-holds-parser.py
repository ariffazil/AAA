#!/usr/bin/env python3
"""
AAA_HOLDS.md Deterministic Parser
Parses the Completed Holds table for APPROVED holds that have not been executed.
Outputs JSON to stdout. No LLM. No hallucination. Pure line parsing.

SOT: /root/.openclaw/workspace/AAA_HOLDS.md
State: /root/.openclaw/workspace/.aaa-holds-state.json
"""
import json
import re
import sys
from pathlib import Path

HOLDS_FILE = Path("/root/.openclaw/workspace/AAA_HOLDS.md")
STATE_FILE = Path("/root/.openclaw/workspace/.aaa-holds-state.json")


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"executed": [], "pending": [], "last_check": None}


def parse_completed_holds(text: str) -> list[dict]:
    """Extract APPROVED holds from Completed Holds table."""
    holds = []
    lines = text.splitlines()
    in_completed = False
    header_seen = False

    for line in lines:
        stripped = line.strip()

        # Detect section start
        if re.match(r"##\s+Completed\s+Holds", stripped, re.IGNORECASE):
            in_completed = True
            header_seen = False
            continue

        # Detect next section — stop parsing
        if in_completed and re.match(r"##\s+", stripped):
            break

        if not in_completed:
            continue

        # Skip header row and separator row
        if not header_seen:
            if stripped.startswith("|") and "ID" in stripped and "Decision" in stripped:
                header_seen = True
            continue

        if stripped.startswith("|") and all(set(c) <= set("-: |") for c in stripped):
            continue

        # Parse data row
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")]
            # Remove leading/trailing empties from pipe delimiters
            while cells and cells[0] == "":
                cells.pop(0)
            while cells and cells[-1] == "":
                cells.pop()

            if len(cells) < 5:
                continue
            if not any(cells):
                continue

            hold = {
                "id": cells[0],
                "when": cells[1],
                "request": cells[2],
                "decision": cells[3],
                "decided_by": cells[4],
            }
            if hold["decision"].upper() == "APPROVED":
                holds.append(hold)

    return holds


def main():
    if not HOLDS_FILE.exists():
        print(json.dumps({"holds": [], "count": 0, "status": "no_file"}))
        sys.exit(0)

    text = HOLDS_FILE.read_text()
    state = load_state()
    executed_ids = set(state.get("executed", []))
    pending_ids = set(state.get("pending", []))

    approved = parse_completed_holds(text)

    # Filter out already executed or pending
    new_holds = []
    for h in approved:
        if h["id"] not in executed_ids and h["id"] not in pending_ids:
            new_holds.append(h)

    result = {
        "holds": new_holds,
        "count": len(new_holds),
        "status": "has_work" if new_holds else "no_work",
        "total_approved": len(approved),
        "executed_count": len(executed_ids),
        "pending_count": len(pending_ids),
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
