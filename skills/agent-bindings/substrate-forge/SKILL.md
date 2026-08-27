---
name: substrate-forge
description: "/forge — routes execution to A-FORGE or a coding runtime. The execution primitive after /init establishes identity and /propose-seal establishes evidence. /forge = 'go execute this mutation under my authority.' Parameterized across Hermes, OpenClaw, and OpenCode runtimes."
tags: [forge, execution, coding-agent, telegram-native, hermes, openclaw, opencode]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
supersedes: [hermes-forge, openclaw-forge, opencode-forge]
---

# /forge — Execution Primitive (Parameterized)

When `/forge <task description>` is invoked, the agent routes execution to the appropriate executor. This is NOT the seal — it is the action after /init and before /propose-seal.

**Agent detection:** Use `$AGENT_RUNTIME` env var or context to determine which variant applies. Values: `hermes`, `openclaw`, `opencode`.

## Output format

```
FORGE ROUTED
────────────────────────────────────
Task:         <task description>
Executor:     <see Agent-Specific Bindings>
Authority:    T1 (auto-mutate)
Risk:         REVERSIBLE
────────────────────────────────────
Routing:
  <see Agent-Specific Bindings>
────────────────────────────────────
Pre-check:
  F1  AMANAH    ✅ reversible path exists
  F4  CLARITY   ✅ ΔS measured before/after
  F11 AUDIT     ✅ (commit + receipt trail)
  F13 SOVEREIGN ⚠️ (no F13 ack needed for T1)
────────────────────────────────────
→ Executing in background...
→ Receipt will be appended to session
→ /forge-status to check progress

DITEMPA BUKAN DIBERI 🔥
```

## Agent-Specific Bindings

### Hermes (`AGENT_RUNTIME=hermes`)

| Field | Value |
|-------|-------|
| Executor options | OpenCode-Zen (delegate_task), A-FORGE (forge_execute), Hermes (self-execute) |
| Code-gen routing | `delegate_task` → opencode binary |
| Audit/verify routing | Hermes self-execute with read-only tools |
| PDF generation | Hermes self-execute via report generation |
| Actor label in receipt | `hermes-<executor>` |

### OpenClaw (`AGENT_RUNTIME=openclaw`)

| Field | Value |
|-------|-------|
| Executor options | OpenCode-Zen (spawn subagent), A-FORGE (forge_execute), OpenClaw (self-execute) |
| Code-gen routing | `spawn_opencode_subagent` in temp worktree (`/tmp/openclaw-worktree`) |
| Audit/verify routing | OpenClaw self-execute with verify tools |
| PDF generation | OpenClaw self-execute via report generation |
| Actor label in receipt | `openclaw-<executor>` |

### OpenCode (`AGENT_RUNTIME=opencode`)

| Field | Value |
|-------|-------|
| Executor | OpenCode (self) — coding agent, always self-execute |
| Warga | FI-001 PRIMARY |
| Extra gates | LSP gate check (mandatory before commit) |
| Extra gates | Test results must pass |
| Authority chain | OpenCode-Zen → delegate_task from Hermes/OpenClaw → A-FORGE → git push → deploy guard |
| Actor label in receipt | `opencode-zen` |
| Digital Ops Policy | digital/code/AI/infra = MUBAH (auto-execute) per 2026-06-30 directive |

## Task classification

| Task type | Executor | Pattern |
|---|---|---|
| Code generation / refactor | OpenCode-Zen | delegate_task (Hermes) / spawn subagent (OpenClaw) / self (OpenCode) |
| Code review | Calling agent | self-execute with read-only tools |
| Infra / deploy / restart | A-FORGE | call_aforge_execute (requires lease) |
| Audit / verification | Calling agent | self-execute with verify tools |
| F1-F13 constitutional | 888-HOLD | route to propose-seal, not forge |
| PDF generation | Calling agent | self-execute via report generation |

## T0-T3 Tier Classification (OpenCode primary, applies to all)

| Tier | Examples | Behavior |
|---|---|---|
| **T0** | Read, grep, git log, port check | Auto-do, no announcement |
| **T1** | Edit, build, test, lint, format, commit, push, restart own session | Auto-do, F2 evidence in commit body |
| **T2** | Multi-file refactor, new dependency, deploy after green tests | Announce 10s window, then proceed |
| **T3** | rm -rf, DROP TABLE, force-push to main, paid API > $10/mo, F1-F13 changes | 888_HOLD — request sovereign ack |

## Implementation

```python
def forge_handler(task: str, agent_runtime: str):
    """Parameterized /forge handler"""

    # 1. /init guard
    envelope = read_federation_session()
    if not envelope.get("session_id"):
        return "ERROR: /init first. No session bound."

    # 2. Classify tier
    tier = classify_tier(task)
    if tier == "T3":
        return "🛑 888_HOLD — use /propose-seal for irreversible work"

    # 3. Measure ΔS_before
    entropy_before = measure_session_entropy()

    # 4. Route to executor
    executor = classify_task_executor(task, agent_runtime)

    if agent_runtime == "opencode":
        # OpenCode self-executes coding tasks
        result = execute_coding_task(task)
        # LSP gate check (mandatory before commit)
        if not lsp_gate_passed(result):
            return "🛑 LSP GATE FAILED — fix errors before commit"
    elif agent_runtime == "openclaw":
        if executor == "opencode":
            result = spawn_opencode_subagent(
                task=task,
                worktree="/tmp/openclaw-worktree",
                toolsets=["code", "terminal"],
                timeout=300
            )
        elif executor == "aforge":
            result = call_aforge_execute(task=task, lease_type="T1")
        else:
            result = self_execute(task)
    elif agent_runtime == "hermes":
        if executor == "opencode":
            result = delegate_task(task=task, toolsets=["code", "terminal"], timeout=300)
        elif executor == "aforge":
            result = call_aforge_execute(task=task, lease_type="T1")
        else:
            result = self_execute(task)

    # 5. Measure ΔS_after
    entropy_after = measure_session_entropy()
    delta_s = entropy_after - entropy_before

    # 6. Build receipt
    receipt = {
        "ts": now_iso(),
        "event": "FORGE_EXECUTED",
        "actor": f"{agent_runtime}-{executor}",
        "session": envelope["session_id"],
        "task": task,
        "result_summary": summarize(result),
        "delta_s": delta_s,
        "evidence_hash": sha256_of_result(result),
    }

    # 7. Return with receipt
    return render_forge_result(receipt)
```

## Doctrine

- `/forge` = the action layer between /init and /propose-seal
- `/forge` is NOT the seal — seal is /propose-seal → 888-APEX
- `/forge` is the "go execute" that happens AFTER /init establishes identity
- F1 reversibility is the hard gate — if ΔS > 0, HALT and HOLD
- F11 audit — every /forge appends a receipt to the session
- F13 sovereignty — T3 requires Arif's ack, no exceptions

## ZEN

```
/init         = WHO AM I?
/forge        = GO DO IT
/propose-seal = RECORD IT PERMANENTLY

Together:
  /init → /forge → /propose-seal

The forge cycle:
  identity → action → evidence → verdict → permanent record

Without /init:   /forge has no actor context
Without /forge:  /propose-seal has nothing to seal
Without /propose-seal:  /forge result is temporary
```

## Error states

| Condition | Response |
|---|---|
| No /init called | `ERROR: /init first. No session bound.` |
| Task classified T3 | `🛑 888_HOLD — use /propose-seal for irreversible work` |
| LSP gate failed (OpenCode) | `🛑 LSP GATE FAILED — fix errors before commit` |
| Test failures (OpenCode) | `🛑 TESTS FAILED — fix or HOLD before commit` |
| ΔS > 0 after execution | `🛑 F1 VIOLATION — ΔS positive. Rollback initiated.` |
| A-FORGE unreachable | `⚠️ A-FORGE offline. Self-executing within agent authority.` |
| OpenCode busy (max 3 concurrent) | `⏳ Queue full. /forge queued — priority = NORMAL` |
| Commit blocked (deploy guard) | `⛔ deploy guard — local HEAD ahead of origin. Push first.` |
