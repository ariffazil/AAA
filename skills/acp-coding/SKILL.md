---
name: acp-coding
description: ACP harness coding agents — Claude Code, Codex, Pi, OpenCode, Gemini CLI. Use when: (1) Spawning coding agents for complex tasks, (2) Code review and refactoring, (3) Multi-file changes across codebases, (4) Thread-bound persistent coding sessions, (5) Relaying work to external ACP harnesses.
---

# ACP Coding Skill

Spawn and manage ACP harness coding agents (Claude Code, Codex, Pi, etc.).

## Quick Start

### Spawn Coding Agent

```json
{
  "tool": "sessions_spawn",
  "runtime": "acp",
  "agentId": "claude",
  "mode": "session",
  "thread": true,
  "task": "Your coding task here"
}
```

| Parameter | Description | Options |
|-----------|-------------|---------|
| `runtime` | Must be "acp" | acp |
| `agentId` | Agent to spawn | claude, codex, pi, opencode, gemini |
| `mode` | "session" (persistent) or "run" (one-shot) | session, run |
| `thread` | Bind to thread | true, false |
| `task` | Initial task | string |

### Supported Agents

| Agent | ID | Best For |
|-------|-----|----------|
| Claude Code | `claude` | Complex reasoning, large refactors |
| Codex | `codex` | Fast implementation, tests |
| Pi | `pi` | Conversational coding |
| OpenCode | `opencode` | Open source alternatives |
| Gemini | `gemini` | Google ecosystem |

## Code Review Pattern

```json
{
  "tool": "sessions_spawn",
  "runtime": "acp",
  "agentId": "claude",
  "mode": "run",
  "task": "Review this PR for: (1) Security issues, (2) Performance bottlenecks, (3) Test coverage gaps. File: /path/to/pr.diff"
}
```

## Persistent Session Workflow

1. **Spawn with thread binding**
2. **Send follow-up tasks** via `sessions_send`
3. **Check status** via `subagents list`
4. **Kill if needed** via `subagents kill`

### Follow-up Commands

```json
{
  "tool": "sessions_send",
  "sessionKey": "agent:claude:acp:<id>",
  "message": "Continue with: add error handling to the auth module"
}
```

## Direct acpx Path

When ACP runtime unavailable, use direct acpx:

```bash
# Check if acpx available
./extensions/acpx/node_modules/.bin/acpx --version

# One-shot execution
acpx claude exec --cwd /path --format quiet "task"

# Persistent session
acpx claude sessions new --name my-session
acpx claude -s my-session --format quiet "task"
```

## Multi-Agent Patterns

### Parallel Implementation

Spawn multiple agents for different approaches:

```json
{
  "sessions_spawn": [{"agentId": "claude", "task": "..."},
                     {"agentId": "codex", "task": "..."}]
}
```

### Agent Chain

1. Codex: Implement feature
2. Claude: Review and optimize
3. Pi: Write documentation

## F11 (Command Auth) Notes

- Coding agents can modify files — reversible via git
- Review diffs before merge
- 888_HOLD for destructive operations (db migrations, etc.)
