---
name: opencode-forge
description: OpenCode-native /forge — execution primitive. After identity is established via /init, /forge mutates code under the agent's authority band. The flow: /init → /forge → /propose-seal.
tags: [forge, execution, coding-agent, opencode]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
---
# OpenCode /forge — Execution Primitive

When OpenCode is invoked, after `/init` establishes identity, `/forge` is the action layer. It mutates code under the agent's authority band (T0/T1/T2/T3).

## Output format

```
FORGE ROUTED
────────────────────────────────────
Task:         <code mutation description>
Executor:     OpenCode (self)
Authority:    T1 (auto-mutate, MUBAH digital ops)
Risk:         REVERSIBLE (git revert available)
────────────────────────────────────
Pre-check:
  F1  AMANAH    ✅ (git revert path exists)
  F4  CLARITY   ✅ (ΔS measured before/after)
  F11 AUDIT     ✅ (commit + receipt trail)
  F13 SOVEREIGN ⚠️ (no F13 ack needed for T1)
────────────────────────────────────
Plan:
  1. <step 1>
  2. <step 2>
  N. <step N>
────────────────────────────────────
→ Executing...
→ After: test, lint, LSP gate
→ Receipt emitted to session
→ /propose-seal to commit to VAULT999
```

## Implementation

```python
def opencode_forge(task: str):
    """OpenCode-native /forge"""

    # 1. /init guard
    envelope = read_federation_session()
    if not envelope.get("session_id"):
        return "ERROR: /init first."

    # 2. Classify tier
    tier = classify_tier(task)
    if tier == "T3":
        return "🛑 888_HOLD — use /propose-seal for irreversible work"

    # 3. Measure entropy_before
    entropy_before = measure_session_entropy()

    # 4. Execute the task
    # - read files
    # - plan edit
    # - apply patch
    # - run tests
    # - commit

    result = execute_coding_task(task)

    # 5. LSP gate check (mandatory before commit)
    if not lsp_gate_passed(result):
        return "🛑 LSP GATE FAILED — fix errors before commit"

    # 6. Measure entropy_after
    entropy_after = measure_session_entropy()
    delta_s = entropy_after - entropy_before

    # 7. Build receipt
    receipt = {
        "ts": now_iso(),
        "event": "OPENCODE_FORGE_EXECUTED",
        "actor": "opencode-zen",
        "warga": "FI-001 PRIMARY",
        "session": envelope["session_id"],
        "task": task,
        "files_changed": result["files"],
        "tests_passed": result["tests_passed"],
        "tests_failed": result["tests_failed"],
        "lsp_gate": "PASSED",
        "delta_s": delta_s,
    }

    return render_forge_result(receipt)
```

## Task classification (T0-T3)

| Tier | Examples | Behavior |
|---|---|---|
| **T0** | Read, grep, git log, port check | Auto-do, no announcement |
| **T1** | Edit, build, test, lint, format, commit, push, restart own session | Auto-do, F2 evidence in commit body |
| **T2** | Multi-file refactor, new dependency, deploy after green tests | Announce 10s window, then proceed |
| **T3** | rm -rf, DROP TABLE, force-push to main, paid API > $10/mo, F1-F13 changes | 888_HOLD — request sovereign ack |

## Digital Ops Policy (2026-06-30)

For OpenCode, **digital/code/AI/infra = MUBAH (auto-execute)**. The T3 list above is the EXCEPTION, not the rule. FARD only on physical reality, other humans, real money.

## Authority

OpenCode's authority chain:
```
OpenCode-Zen (333-AGI bound)
   ↓
delegate_task from Hermes/OpenClaw
   ↓
A-FORGE execute (if forge tier)
   ↓
git push → arifOS deploy guard (test + drift check)
```

## Doctrine

- /forge is the action layer between /init and /propose-seal
- /forge is NOT the seal — that's /propose-seal → 888-APEX
- F1 reversibility is the hard gate — if ΔS > 0, HALT and HOLD
- F11 audit — every /forge appends a receipt to the session
- F13 sovereignty — T3 requires Arif's ack, no exceptions

## Error states

| Condition | Response |
|---|---|
| No /init called | `ERROR: /init first. No session bound.` |
| Task classified T3 | `🛑 888_HOLD — use /propose-seal for irreversible work` |
| LSP gate failed | `🛑 LSP GATE FAILED — fix errors before commit` |
| Test failures | `🛑 TESTS FAILED — fix or HOLD before commit` |
| ΔS > 0 after execution | `🛑 F1 VIOLATION — ΔS positive. Rollback initiated.` |
| Commit blocked (deploy guard) | `⛔ deploy guard — local HEAD ahead of origin. Push first.` |