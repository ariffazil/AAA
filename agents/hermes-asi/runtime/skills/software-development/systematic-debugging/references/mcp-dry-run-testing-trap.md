# MCP Tool Behavior — Dry-Run Testing Trap

**Date:** 2026-05-17  
**Context:** TREE777 Week 1 verification, `arif_heart_critique` tool testing  
**Lesson:** Don't infer MCP tool behavior from dry-run mocks.

---

## The Trap

When testing a workflow engine in `--dry-run` mode, all MCP tools are mocked. If you then test a tool's response characteristics (e.g., "does `arif_heart_critique` return `{worked: True}` for all inputs?"), the mock gives you an answer — but that answer reflects the mock, not the real tool.

**Symptom:** Agent raises a defect based on dry-run mock behavior. The defect appears real because the test logic is sound, but the evidence is from the wrong execution layer.

---

## What Happened

1. Agent ran `workflow-session-cycle` in dry-run mode
2. `arif_heart_critique` was mocked in the engine's `_run_step()` handler → always returned `{"worked": True}`
3. Agent concluded the real MCP always approves everything (D2 defect)
4. Arif ran `arif_heart_critique` live → returned `worked: false, risk_tier: CRITICAL, human_decision_required: true`
5. **D2 closed as false** — the claim was wrong, not the tool

---

## The Rule

```
DRY-RUN MODE ≠ REAL MCP BEHAVIOR

For tool RESPONSE CHARACTERISTICS (not just availability):
→ Test against the live MCP, not in dry-run

Dry-run sufficient for: state machine, gating, branching, recovery, loop guards, persistence
Real execution required for: response shape, risk tier accuracy, decision boundaries, failure branch paths
```

---

## How to Test MCP Behavior Correctly

**Option A:** Test engine logic in dry-run, test MCP separately by calling the tool manually
**Option B:** Run engine in real mode with live MCP (full end-to-end)
**Option C:** Inject specific tool responses to test branching (bypasses mock, tests engine branch resolution — not whether real tool would actually return that value)

---

## The Hybrid Approach (most reliable)

1. Test engine logic in `--dry-run --resume` → confirms state machine correct
2. Test specific tool responses manually → confirms tool behavior
3. If both pass, the integrated system works

---

## Related Skills

- `systematic-debugging/SKILL.md` — Phase 1 requires "evidence from the correct execution layer"
- `fabrication-prevention` — verify before claiming. Agent claimed `arif_heart_critique` always returns `{worked: True}` without running the real tool.

## Session Context

- Workflow: `/root/AAA/wiki/workflows/workflow-session-cycle/`
- Engine: `/root/AAA/wiki/workflows/_runtime/tree777_executor.py`
- Defects report: `/root/AAA/wiki/workflows/_runtime/defects-report.md`
- The D3 defect (infinite loop) was found via dry-run — appropriate use of dry-run for engine logic