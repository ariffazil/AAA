---
name: f13-mid-stream-corrections
description: Protocol for handling F13 SOVEREIGN constitutional corrections that arrive DURING the dispatch loop (after agents have started, before HTML complete). The constitutional-edit pattern — corrections win over agent polish, always.
forged: 2026-08-12
source: PETRONAS v12 DRAFT_SPEC dispatch (3 agents running when F13 ruling arrived mid-stream)
---

# F13 Mid-Stream Corrections — Constitutional Edit Protocol

## The Problem

F13 SOVEREIGN may issue constitutional corrections DURING a sovereign-petition-forge dispatch loop. This happens because:
- F13 reads agent progress in real time
- F13 sees emergent structure that prompts new rulings
- F13's judgment matures as the artifact crystallizes
- Sometimes F13 simply changes their mind

**The trap:** Treating F13 corrections as suggestions, or as "feedback to incorporate later". They are NOT suggestions. They are CONSTITUTIONAL EDITS — equivalent to changing the law, not the comment.

## The Protocol

### Step 1 — KILL stale dispatches IMMEDIATELY

```bash
# List running processes
ps -ef | grep -iE "(qwen|opencode)" | grep -v grep

# Kill via process tool (preferred)
process(action="kill", session_id="proc_xxx")
```

A process working on stale spec will produce HTML that violates the new corrections. Kill it. **No exceptions. No "let it finish first". No "it's almost done anyway".**

### Step 2 — Update the canonical spec

Bump version: `v1.0` → `v1.1` → `v1.2`. Add CHANGELOG entry. Be explicit about WHAT was corrected and WHY.

```markdown
## CHANGELOG

- **v1.0** (2026-08-12 15:30 MYT): Initial spec
- **v1.1** (2026-08-12 15:35 MYT): F13 SOVEREIGN correction:
  - LOCKED identity: Muhammad Arif bin Fazil (NOT anonymous)
  - REMOVED conspiracy framings
  - ADDED Companies House #17027115 source
```

### Step 3 — Verify the spec is canonical

Read back the spec. Make sure F13 corrections are EXPLICIT (not implied). The agent has no context outside the spec — if it's not written, it doesn't exist.

### Step 4 — Re-dispatch

Re-launch the parallel CLIs (qwen + opencode-zen/deepseek + opencode-zen/gpt-5.6-luna) with the new spec.

### Step 5 — Honor the constitutional receipt

When apex_judge returns `eff=HOLD, f13_required=TRUE` for the dispatched artifact, **that's the system working correctly**. Don't fight it. The Constitution's job is to LIMIT the agent. The Sovereign's job is to CHOOSE.

## The 3-Strikes Rule for F13 Corrections

If F13 issues a 3rd correction on the same artifact, STOP dispatching. Re-read the trajectory. The corrections are converging on a pattern — that's the trajectory's own lesson. Document it.

## Real Example (2026-08-12)

1. Initial spec dispatched to 3 CLIs (qwen + deepseek + gpt-5.6-luna) at v12.0
2. 90 seconds later, F13 issued 3 corrections:
   - LOCKED identity (full name, not anonymous)
   - REMOVED conspiracy framings (14-day Federal Court, sengaja London, personally benefited)
   - ADDED Clifford Chance US$6B financing data point
3. Killed all 3 stale dispatches within 30 seconds
4. Updated spec to v12.1 with CHANGELOG entry
5. Re-dispatched all 3 to v12.1 spec
6. Discovered existing `surat-final-v12.html` (25KB) — different dispatch cycle from prior session
7. Patched existing artifact instead of regenerating

Total time from F13 correction to corrected spec: ~2 minutes. Total stale compute wasted: ~3 agent-minutes. Total compute saved by detecting existing artifact: ~30 agent-minutes (avoided redundant regeneration).

## Why This Matters

Sovereign work is constitutional work. The spec is law while it's active. F13 corrections are constitutional amendments, not feedback. Treating them otherwise produces artifacts that violate F13 sovereignty — which is the entire point of having F13.

## Anti-patterns

- ❌ **"Let it finish first, then amend"** — produces artifact that violates new spec
- ❌ **"I'll incorporate F13 corrections in next iteration"** — there IS no next iteration if this is dispatch candidate
- ❌ **"F13 correction seems minor, skip it"** — F13 is sovereign; you are not
- ❌ **"Stale process will adapt somehow"** — it won't; it's working from spec it already loaded
- ❌ **"I'll fix the HTML after all 3 complete"** — defeats parallel independence; defers correction

DITEMPA BUKAN DIBERI — Constitutional edits are not feedback. They are law.