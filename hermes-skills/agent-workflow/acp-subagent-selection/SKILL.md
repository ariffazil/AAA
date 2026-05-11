---
name: acp-subagent-selection
description: Choose the right subagent for ACP tasks — Kimi vs OpenCode vs direct execution
category: agent-workflow
---

# ACP Subagent Selection Strategy

## Core Rule
ACP background tasks cannot handle interactive permission prompts. Select the right agent based on the task type.

## Agent Capabilities

| Agent | ACP Mode | Best For | Limitation |
|-------|----------|----------|------------|
| **Kimi** | ✅ Background capable | Reasoning, research, multi-step analysis | ❌ Blocked by interactive permission prompts in background mode |
| **OpenCode** | ✅ Full file access | File operations, code refactoring, writing | ⚠️ May produce thin output in long sessions — verify results |
| **Direct (Hermes)** | n/a | Small-medium additive changes, auditing, verification | ❌ 4300+ line mechanical refactors = slow for human |

## Decision Tree

```
Task type?
├── Read-only / research / reasoning
│   └── Kimi ACP (background OK if task is self-contained)
├── File write / refactor / multi-file changes
│   └── OpenCode OR direct execution
│       ├── Small (<100 lines, additive): OpenCode OK
│       └── Large (1000+ lines, mechanical): Arif direct
└── Verification / auditing
    └── Hermes directly (no subagent needed)
```

## WEALTH Refactor Case Study

**Task:** Decompose 4300-line `monolith.py` into 36 atomic tools + 12 prompts + 21 resources

**What happened:**
1. Kimi spawned → hit permission prompt wall in ACP mode → failed ✅
2. OpenCode spawned → completed Phase 0 (handshake fix) but Phases 1-4 not done → partial ✅
3. Arif switched to direct execution → completed ✅

**Lesson:** Large mechanical refactors (adding `@mcp.tool()` decorators + async wrappers around existing logic) are additive and low-break-risk. Better done directly by Arif or chunked into <100 line pieces per OpenCode run.

## Workflow

1. Spawn subagent for task
2. If task produces thin/threshold output → verify what actually landed
3. If subagent fails → pivot to appropriate alternative (see decision tree)
4. For large refactors: offer Arif direct execution as option

## Verification Steps

After any subagent completes:
```
git -C ~/WEALTH diff --stat
git -C ~/WEALTH log --oneline -3
```
Check: expected files modified? Commit message accurate? Output matches actual changes?
