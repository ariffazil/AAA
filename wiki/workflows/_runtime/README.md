# TREE777 Workflow Runtime Engine

## Location
`/root/AAA/wiki/workflows/_runtime/`

## Files
- `tree777_executor.py` — Main execution engine (Python state machine)
- `runtime_config.json` — Runtime configuration
- `README.md` — This file

## Usage
```bash
# Fresh run
python3 _runtime/tree777_executor.py workflow-session-cycle

# Resume from last gate
python3 _runtime/tree777_executor.py workflow-session-cycle --resume

# Dry run (no actual execution)
python3 _runtime/tree777_executor.py workflow-session-cycle --dry-run
```

## Architecture
Each workflow has:
- `plan.json` — Step definitions, branching, void conditions, recovery rules
- `state.json` — Current execution state (written by engine)
- `gates/` — Per-step gate files: `{"status": "passed/failed/pending", "passed": true/false/null}`
- `artifacts/` — Step outputs written before gate advances
- `reasoning/SUMMARY_MD.md` — Design rationale

## Recovery
- Resume from last validated gate (not from scratch)
- Idempotent — safe to retry
- Gate files track pass/fail/retry count

## Governance
- Risk band enforced per workflow
- High-risk workflows require 888_JUDGE verdict before step-04+
- Escalation paths: clarify → 888_HOLD → VOID

DITEMPA BUKAN DIBERI — Engine forged, not given.
