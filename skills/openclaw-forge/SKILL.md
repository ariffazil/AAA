---
name: openclaw-forge
description: OpenClaw-native /forge — routes execution to a coding agent or A-FORGE. The execution primitive after /init establishes identity and /propose-seal establishes evidence. /forge = "go execute this mutation under my authority."
tags: [forge, execution, coding-agent, telegram-native, openclaw]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
---
# OpenClaw /forge — Execution Primitive

When a user types `/forge <task description>` to the OpenClaw bot, OpenClaw routes the execution to the appropriate executor.

## Output format

```
FORGE ROUTED
────────────────────────────────────
Task:         <task description>
Executor:     <OpenCode-Zen | A-FORGE | delegate_task>
Authority:    T1 (auto-mutate)
Risk:         REVERSIBLE
────────────────────────────────────
Routing:
  if code-gen → OpenCode-Zen (delegate_task → opencode binary)
  if infra/deploy → A-FORGE (forge_execute)
  if audit/verify → OpenClaw (self-execute)
────────────────────────────────────
Pre-check:
  F1  AMANAH    ✅ reversible path exists
  F4  CLARITY   ✅ ΔS measured before/after
  F13 SOVEREIGN ⚠️ (no F13 ack needed for T1)
────────────────────────────────────
→ Executing in background...
→ Receipt will be appended to session
→ /forge-status to check progress

DITEMPA BUKAN DIBERI 🔥
```

## Implementation

```python
def openclaw_forge_handler(event, task: str):
    """Telegram-native /forge handler for OpenClaw"""

    # 1. /init guard
    envelope = read_federation_session()
    if not envelope.get("session_id"):
        return "ERROR: /init first. No session bound."

    # 2. Classify the task
    executor = classify_task_executor(task)

    # 3. Measure ΔS_before
    entropy_before = measure_session_entropy()

    # 4. Route to executor
    if executor == "opencode":
        # Delegate to OpenCode-Zen (coding agent)
        result = spawn_opencode_subagent(
            task=task,
            worktree="/tmp/openclaw-worktree",
            toolsets=["code", "terminal"],
            timeout=300
        )
    elif executor == "aforge":
        # Route to A-FORGE (infra/deploy)
        result = call_aforge_execute(
            task=task,
            lease_type="T1"
        )
    else:
        # OpenClaw self-executes (audit/verify)
        result = self_execute(task)

    # 5. Measure ΔS_after
    entropy_after = measure_session_entropy()
    delta_s = entropy_after - entropy_before

    # 6. Build receipt
    receipt = {
        "ts": now_iso(),
        "event": "FORGE_EXECUTED",
        "actor": "openclaw-" + executor,
        "session": envelope["session_id"],
        "task": task,
        "result_summary": summarize(result),
        "delta_s": delta_s,
        "evidence_hash": sha256_of_result(result),
    }

    # 7. Return with receipt
    return render_forge_result(receipt)
```

## Task classification

| Task type | Executor | Pattern |
|---|---|---|
| Code generation / refactor | OpenCode-Zen | spawn subagent in temp worktree |
| Code review | OpenClaw | self-execute with read-only tools |
| Infra / deploy / restart | A-FORGE | call_aforge_execute (requires lease) |
| Audit / verification | OpenClaw | self-execute with verify tools |
| F1-F13 constitutional | 888-HOLD | route to propose-seal, not forge |
| PDF generation | OpenClaw | self-execute via report generation |

## Doctrine

- /forge = the action layer between /init and /propose-seal
- /forge is NOT the seal — seal is /propose-seal → 888-APEX
- /forge is "go execute" AFTER /init establishes identity
- F1 reversibility is the hard gate — if ΔS > 0, HALT and HOLD
- F11 audit — every /forge appends a receipt to the session

## ZEN

```
/init         = WHO AM I?
/forge        = GO DO IT
/propose-seal = RECORD IT PERMANENTLY

Together:
  /init → /forge → /propose-seal

The forge cycle:
  identity → action → evidence → verdict → permanent record

OpenClaw is the executor. Hermes is the auditor. 888 is the judge.
```

## Error states

| Condition | Response |
|---|---|
| No /init called | `ERROR: /init first. No session bound.` |
| Task classified T3 | `🛑 888_HOLD — use /propose-seal for irreversible work` |
| ΔS > 0 after execution | `🛑 F1 VIOLATION — ΔS positive. Rollback initiated.` |
| A-FORGE unreachable | `⚠️ A-FORGE offline. Self-executing within OpenClaw authority.` |
| OpenCode busy (max 3 concurrent) | `⏳ Queue full. /forge queued — priority = NORMAL` |