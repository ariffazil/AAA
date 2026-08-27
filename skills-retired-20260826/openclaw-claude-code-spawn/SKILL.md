---
name: openclaw-claude-code-spawn
description: Spawn Claude Code as a governed coding executor from OpenClaw gateway. Use when OpenClaw receives a coding task that needs autonomous execution. Routes through /acp spawn or direct CLI, with arifOS F1-F13 constitutional governance.
version: 1.0.0
owner: HERMES
risk_tier: T2
floor_scope: F1 F2 F4 F7 F11 F13
autonomy_tier: T1.5
forbidden:
  - Never --dangerously-skip-permissions
  - Never spawn without constitutional context
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# OpenClaw → Claude Code Spawn (Governed)

Delegate coding tasks from OpenClaw gateway to Claude Code under arifOS constitutional governance.

## Prerequisites

```bash
# From an OpenClaw session: verify CC is callable
claude --version                        # v2.1.218+
[ -d /root/AAA/plugins/claude-code-federation ]
curl -sf http://127.0.0.1:8088/health >/dev/null  # kernel alive
```

## Method 1: ACP HARVESS (PREFERRED — production path)

OpenClaw acpx now has `claude` registered (`/root/.openclaw/openclaw.json` → `plugins.entries.acpx.config.agents.claude`).

```
/acp spawn claude --mode persistent --bind here
```

Then task directly in the bound conversation. The harness uses:
- Workspace: `/root`
- Plugin dir: `/root/AAA/plugins/claude-code-federation`
- Permission mode: `plan` (F12 — explicit approval for mutations)

Follow-up commands: `/new`, `/reset`, `/acp close`

## Method 2: DIRECT CLI (one-shot print mode)

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

## Method 3: CLI BACKEND FALLBACK (zero-config)

With the anthropic plugin now enabled (`plugins.entries.anthropic.enabled: true`), the `claude-cli` CLI backend automatically registers. When API providers fail, OpenClaw falls back to CC automatically.

## Governance Contract

| Rule | Why |
|------|-----|
| **ALWAYS** `--permission-mode plan` | F12 |
| **ALWAYS** `--plugin-dir` arifos-federation | Constitutional hooks loaded |
| **ALWAYS** `--append-system-prompt` constitutional | F1-F13 in context |
| **ALWAYS** `--output-format json` | F2 structured evidence |
| **NEVER** `--dangerously-skip-permissions` | F1/F12/F13 |
| **Agent permissionMode: plan** in OpenClaw config | F12 |

## Session Map

| What | Where |
|------|-------|
| OpenClaw session | `~/.openclaw/agents/claude/` |
| CC session | `~/.claude/projects/` |
| ACP tracking | `~/.openclaw/acpx/` |
| Kernel session | `/tmp/opencode/session_state.json` |
