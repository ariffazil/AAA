---
name: claude-code-spawn
description: "Spawn Claude Code as a governed execution harness. Use when a coding task needs autonomous execution — feature implementation, refactoring, bug fixing, PR review, or any multi-step coding work. Routes through arifOS F1-F13 constitutional governance with structured JSON return. Parameterized across Hermes and OpenClaw runtimes."
version: 1.0.0
owner: HERMES
risk_tier: T2
floor_scope: F1 F2 F4 F7 F11 F13
autonomy_tier: T1.5
forbidden:
  - Never use --dangerously-skip-permissions
  - Never omit --max-turns (runaway loop prevention)
  - Never spawn without --output-format json
  - Never spawn without constitutional context
capability_tier: fed-reasoning-heavy
ecology_state: WARM
supersedes: [hermes-claude-code-spawn, openclaw-claude-code-spawn]
---

# Claude Code Spawn — Governed Execution (Parameterized)

Delegate coding tasks to Claude Code CLI (`/root/.local/bin/claude`, v2.1.218) under arifOS constitutional governance.

**Agent detection:** Use `$AGENT_RUNTIME` env var or context to determine which variant applies. Values: `hermes`, `openclaw`.

## Prerequisites (verify before spawn)

```bash
claude --version 2>/dev/null            # must be v2.x+
[ -d /root/AAA/plugins/claude-code-federation ]   # plugin present
curl -sf http://127.0.0.1:8088/health >/dev/null  # kernel alive
# Hermes additionally checks:
[ -f /tmp/opencode/session_state.json ] # session bound (else bind first)
```

If any fail → do NOT spawn. Report the gap, route to 888-APEX for HOLD.

## Agent-Specific Bindings

### Hermes (`AGENT_RUNTIME=hermes`)

**3 modes available:**

#### Mode 1: PRINT MODE (PREFERRED — one-shot, structured)

```
terminal(command="claude -p '<TASK>' --max-turns 15 --output-format json \
  --allowedTools 'Read,Edit,Write,Glob,Grep,Bash,WebSearch,WebFetch' \
  --permission-mode plan \
  --plugin-dir /root/AAA/plugins/claude-code-federation \
  --append-system-prompt 'You are a governed executor of the arifOS federation. F1: snapshot before mutate. F2: label claims OBS/DER/INT/SPEC. F7: cap confidence 0.90. F11: trace every action. F13: Arif holds final veto. Never use --dangerously-skip-permissions. Digital ops = MUBAH (auto-do).'",
  workdir="/root",
  timeout=300)
```

**Parse the JSON result:**
```json
{
  "type": "result",
  "subtype": "success",
  "result": "The task output text",
  "session_id": "75e2167f-...",
  "num_turns": 3,
  "total_cost_usd": 0.078,
  "stop_reason": "end_turn"
}
```

**Key fields to report to user:** `result` (output), `num_turns`, `total_cost_usd`, `session_id`.
**Failure subtypes:** `error_max_turns`, `error_budget`, `error_rate_limit`, `error_other`.

#### Mode 2: TASK-ONLY (analysis — no mutation)

```
terminal(command="claude -p '<ANALYSIS_TASK>' --max-turns 5 --output-format json \
  --allowedTools 'Read,Glob,Grep' \
  --permission-mode plan \
  --plugin-dir /root/AAA/plugins/claude-code-federation",
  workdir="/root",
  timeout=120)
```

Use when: review code, explain architecture, estimate effort, research — anything that must NOT mutate.

#### Mode 3: TMUX INTERACTIVE (multi-turn — rare, requires governance)

Only when the task genuinely needs iterative human-in-the-loop work:

```bash
tmux new-session -d -s cc-work -x 140 -y 40
tmux send-keys -t cc-work 'cd /root && claude --permission-mode plan' Enter
sleep 5 && tmux send-keys -t cc-work Enter   # workspace trust dialog
sleep 2 && tmux send-keys -t cc-work '<TASK>' Enter
sleep 15 && tmux capture-pane -t cc-work -p -S -50
# ... iterate ...
tmux kill-session -t cc-work   # ALWAYS clean up
```

**Session binding (Hermes):**
```bash
# If /tmp/opencode/session_state.json is missing or stale:
curl -sf -X POST http://127.0.0.1:8088/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"actor_id":"hermes-agent","intent":"Spawn Claude Code governed executor","requested_authority":"FULL"}}}'
```

Record the CC spawn in the audit trail with both session IDs (Hermes + CC).

### OpenClaw (`AGENT_RUNTIME=openclaw`)

**3 methods available:**

#### Method 1: ACP HARNESS (PREFERRED — production path)

OpenClaw acpx has `claude` registered (`/root/.openclaw/openclaw.json` → `plugins.entries.acpx.config.agents.claude`).

```
/acp spawn claude --mode persistent --bind here
```

Then task directly in the bound conversation. The harness uses:
- Workspace: `/root`
- Plugin dir: `/root/AAA/plugins/claude-code-federation`
- Permission mode: `plan` (F12 — explicit approval for mutations)

Follow-up commands: `/new`, `/reset`, `/acp close`

#### Method 2: DIRECT CLI (one-shot print mode)

```
terminal(command="claude -p '<TASK>' \
  --max-turns 15 --output-format json \
  --allowedTools 'Read,Edit,Write,Glob,Grep,Bash,WebSearch,WebFetch' \
  --permission-mode plan \
  --plugin-dir /root/AAA/plugins/claude-code-federation \
  --append-system-prompt 'You are a governed executor of the arifOS AAA Federation under Muhammad Arif bin Fazil (F13 SOVEREIGN). F1: snapshot before mutate. F2: label claims OBS/DER/INT/SPEC. F7: cap confidence 0.90. F11: trace every action. Never use --dangerously-skip-permissions. Digital ops = MUBAH (auto-do).'",
  workdir="/root",
  timeout=300)
```

#### Method 3: CLI BACKEND FALLBACK (zero-config)

With the anthropic plugin enabled (`plugins.entries.anthropic.enabled: true`), the `claude-cli` CLI backend automatically registers. When API providers fail, OpenClaw falls back to CC automatically.

**Session map (OpenClaw):**

| What | Where |
|------|-------|
| OpenClaw session | `~/.openclaw/agents/claude/` |
| CC session | `~/.claude/projects/` |
| ACP tracking | `~/.openclaw/acpx/` |
| Kernel session | `/tmp/opencode/session_state.json` |

## Governance Contract (non-bypassable — all agents)

| Rule | Why |
|------|-----|
| **NEVER** `--dangerously-skip-permissions` | F1/F12/F13 — one flag kills the whole safety stack |
| **ALWAYS** `--max-turns` (5-15) | F8 — runaway loop and cost control |
| **ALWAYS** `--permission-mode plan` | F12 — plan mode requires explicit approval for mutations |
| **ALWAYS** `--plugin-dir` arifos-federation | Loads constitutional hooks + Trinity agents |
| **ALWAYS** `--append-system-prompt` constitutional | F1-F13 in the context window |
| **ALWAYS** `--output-format json` | F2/F4 — structured evidence, machine-parseable |
| **F1** Snapshot before any mutation work | Reversible-first |
| **F11** Record CC `session_id` in the audit chain | Traceability across spawns |

## Cleanup

- tmux sessions: `tmux kill-session -t <name>` when done (never leave orphans)
- CC `--no-session-persistence` flag in pure CI to avoid disk accumulation
- Report `total_cost_usd` to the user for spend transparency

## Failure Handling

| Symptom | Action |
|---------|--------|
| `error_rate_limit` | Wait 30s, retry once, then route to FED for model fallback |
| `error_budget` | Report to user — budget cap hit. Do NOT retry. |
| `error_max_turns` | Report partial result, suggest `--max-turns 30` for next round |
| CC binary not found | Check `/root/.local/bin/claude`, report installation gap |
| Kernel down (:8088) | HOLD — do not spawn ungoverned |
