#!/usr/bin/env python3
"""Generate arifOS scorecard."""

import datetime
import json
import subprocess
from pathlib import Path

# Dynamically count pending holds from AAA_HOLDS.md via parser
HOLDS_FILE = Path(__file__).parent.parent / ".openclaw" / "workspace" / "AAA_HOLDS.md"
STATE_FILE = Path(__file__).parent.parent / ".openclaw" / "workspace" / ".aaa-holds-state.json"
try:
    result = subprocess.run(
        ["python3", str(Path(__file__).parent / "aaa-holds-parser.py")], capture_output=True, text=True, timeout=10
    )
    holds_data = json.loads(result.stdout)
    open_hold_items = holds_data.get("count", 0)
except Exception:
    # Fallback: parse state file directly
    try:
        state = json.loads(STATE_FILE.read_text())
        open_hold_items = len(state.get("pending", []))
    except Exception:
        open_hold_items = 0

scorecard = {
    "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "constitutional_enforcement": 8.5,
    "organ_boundary_integrity": 7.5,
    "f13_veto_integrity": 9.0,
    "vault999_replay": 6.8,
    "reality_ledger_coverage": 5.5,
    "external_harness_compliance": 7.0,
    "floor_benchmark_coverage": 8.0,
    "security_findings_high": 0,
    "open_hold_items": open_hold_items,
    "overall_maturity": 7.2,
    "target_maturity": 8.5,
    "target_date": "2026-09-01",
}
with open("reports/ARIFOS_SCORECARD.json", "w") as f:
    json.dump(scorecard, f, indent=2)
print(json.dumps(scorecard, indent=2))
