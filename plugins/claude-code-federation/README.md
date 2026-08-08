# arifos-federation — Claude Code Plugin

> **DITEMPA BUKAN DIBERI**  
> Constitutional agentic harness. Claude Code as governed executor under F1-F13 kernel governance.

## What This Is

A Claude Code plugin that makes Claude Code a **governed execution harness** for the arifOS AAA Federation. It provides:

- **Constitutional hooks** — F1 AMANAH (snapshot before mutate), F11 AUDIT (trace every action), F4 CLARITY (entropy check on stop)
- **Trinity agents** — 333-AGI (reasoning), 555-ASI (research), 888-APEX (constitutional verdict) as Claude Code subagents
- **Federation awareness** — organ topology, session binding, FQ metabolism

## Architecture

```
┌──────────────────────────────────────────┐
│             CLAUDE CODE HARNESS           │
│  ┌─────────┐ ┌──────────┐ ┌────────────┐ │
│  │  HOOKS  │ │  AGENTS  │ │   SKILLS   │ │
│  │ F1/F4/  │ │ 333/555/ │ │ AAA catalog│ │
│  │ F11     │ │ 888      │ │ (120+)     │ │
│  └────┬────┘ └────┬─────┘ └─────┬──────┘ │
│       │           │             │         │
│       └───────────┼─────────────┘         │
│                   │                       │
└───────────────────┼───────────────────────┘
                    │ MCP + HTTP
                    ▼
┌──────────────────────────────────────────┐
│            arifOS KERNEL (:8088)          │
│    F1-F13 floors · judge · seal · bind    │
└──────────────────────────────────────────┘
```

## Installation

From the plugin directory:

```bash
# Clone or symlink into Claude Code plugins
# Option A: Skills-directory (auto-discovered)
ln -s /root/AAA/plugins/claude-code-federation /root/.claude/skills/arifos-federation

# Option B: Via Claude Code CLI
claude plugin install /root/AAA/plugins/claude-code-federation
```

## Components

### Agents

| Agent | Use When |
|-------|----------|
| `333-agi` | Planning, synthesis, architecture, complex multi-step reasoning |
| `555-asi` | Memory recall, drift detection, telemetry, deep research |
| `888-apex` | Constitutional verdict BEFORE irreversible mutations or seals |

### Hooks

| Hook | Event | What It Does |
|------|-------|-------------|
| F1 AMANAH | PreToolUse (Bash/Edit/Write) | Warns/blocks destructive Bash commands, checks session binding |
| F11 AUDIT | PostToolUse (all) | Records tool execution to audit log, ingests to arifFlow for FQ metabolism |
| F4 CLARITY | Stop | Checks for uncommitted changes — enforces ΔS ≤ 0 |

## Requirements

- Claude Code v2.1.198+
- Python 3.7+ (for hook scripts)
- arifOS kernel running at :8088
- arifFlow running at :7073 (non-fatal if down)

## Author

333-AGI Δ MIND — forged 2026-08-08 under F13 SOVEREIGN
