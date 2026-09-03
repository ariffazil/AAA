# TREE777 Workflow Runtime — Engine Design Notes
**Source:** TREE777 Week 1 build session, 2026-05-17  
**Lesson type:** Design insight from dry-run testing

---

## Key Insight: Verification Runs AFTER Execution, Not Before

The engine's `_verify()` method runs **after** `_run_step()` returns. This creates a critical sequencing issue:

```
Step executes → writes artifact → gate enters "entered" state → verify runs
```

In dry-run mode, this means:
- `arif_session_init` dry-run outputs `"dry_run": True` — no `session_id` written to `state.json`
- Verify then checks `state.json` for `session_id` → **fails** (correct behavior)
- Escalation → 888_HOLD → state = `hold`

**This is CORRECT constitutional behavior.** The 888_HOLD escalation in dry-run proves the governance gate works. The lesson: 
> A real execution (non-dry-run) calls `arif_session_init` via MCP, which writes `session_id` to `state.json` **before** verify runs. The engine and the governance are both working correctly — dry-run tests the gate logic, not the MCP integration.

**Rule:** When testing workflow engine in dry-run, expect 888_HOLD on steps where state depends on real MCP execution. This is the feature working, not a bug.

---

## Branch Resolution — How the Engine Decides Next Step

The engine reads `step["branch"]` dict where keys are outcome labels and values are target step_ids:

```python
branch = step.get("branch", {})
# For REFLECT step:
if "worked" in output_str and "true" in output_str.lower():
    outcome = list(branch.keys())[0]
```

**Current heuristic-based branch resolution is fragile.** A real router (Week 2) would make this deterministic. Current limits:
- `heart_critique` returns `{"worked": True}` — but output is serialized to string, `True` becomes `"true"`, `"true" in "true"` matches
- `"failed" in output_str` is too loose — any dict key containing "failed" triggers the wrong branch
- `"alternative"` check catches "no_alternative" as matching "alternative" (substring match problem)

**Current workaround:** Default to first branch value if no match found. This means the engine will advance in the normal sequence even if branch resolution is ambiguous. This is acceptable for Week 1 — it's a known gap to fix in Week 2.

---

## datetime.datetime.utcnow() Deprecation

Python 3.12+ deprecates `datetime.datetime.utcnow()`. Replace with:
```python
from datetime import datetime, timezone
def _now(self) -> str:
    return datetime.now(timezone.utc).isoformat()
```

The engine was fixed mid-session to use `datetime.now(timezone.utc)` throughout.

---

## Verification Command Patterns

Three verified patterns in the workflow engine:

| Pattern | Example | Notes |
|---------|---------|-------|
| `test -f ` | `test -f artifacts/step-01-reason.json` | Glob support: `ls artifacts/step-03-*` |
| `grep <pattern> [filepath]` | `grep session_id state.json` | Falls back to state.json if no path |
| `(empty)` | no verification | Always passes |

**Path substitution:** `<config_path>` in verification strings is replaced with `self.state.get("config_path", "")` before use.

---

## Recovery Behavior

**Idempotent by design:**
- `python3 executor.py workflow-session-cycle` (fresh) → skips already-passed gates
- `python3 executor.py workflow-session-cycle --resume` → finds last passed gate, resumes from next

**Safety limit:** `max_iterations = len(plan["steps"]) * 2` prevents infinite loops on broken branch resolution.

**State file format:**
```json
{
  "workflow_id": "workflow-session-cycle",
  "status": "completed|failed|hold|init",
  "current_step": "step-05",
  "completed_steps": ["step-00", "step-01", "step-02"],
  "artifacts": {"step-00": "/path/to/step-00.json"},
  "session_id": null,
  "last_updated": "2026-05-17T..."
}
```

---

## Gate File Format

Each step gets a gate file at `workflows/<workflow_id>/gates/<step_id>.json`:
```json
{
  "step_id": "step-00",
  "status": "passed|failed|pending|entered",
  "entered_at": "2026-05-17T...",
  "verified_at": "2026-05-17T...",
  "passed": true,
  "verification_output": "grep 'session_id' in state.json → False",
  "step_output": {"session_id": "session-..."},
  "retry_count": 0,
  "escalation_triggered": false
}
```

Engine reads gate files on every run to determine which steps to skip or retry.

---

## 3 Canonical Workflows Summary

| Workflow | Steps | Branching | Risk | Domain |
|----------|-------|-----------|------|--------|
| `workflow-session-cycle` | 10 | step-05/06/07 | medium | general |
| `workflow-scar-to-skill` | 7 | step-00/02/04 | high | governance |
| `workflow-agent-onboarding` | 7 | step-00 | high | federation |

All stored at: `/root/AAA/wiki/workflows/`

---

## Related

- `federation-runtime-audit/SKILL.md` — parent skill
- `AAA/wiki/workflows/_runtime/tree777_executor.py` — engine source
- `AAA/wiki/workflows/workflow-*/plan.json` — workflow definitions