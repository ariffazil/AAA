# CARD EXPERIMENT — Agent Cognition vs Agent Card Surface

> **Hypothesis:** An agent's ability to route, delegate, and act correctly depends on how many agent cards it holds. Zero cards = blind. All cards = federation-aware.

## The Concrete Problem

**Propagate `mcp_surface.tools` field across all 24 agent cards.** OpenCode's card already fixed (v3.1.0). The rest still use deprecated `mcp_servers` or have no MCP surface declared at all.

The task is:
```
For each agent card in /root/AAA/agents/ (recursive):
  Check if it uses 'mcp_servers' (deprecated) or missing 'mcp_surface.tools'
  If yes, add mcp_surface with actual tool names from the federation MCP catalog
```

## Method — 4 Trials

Each trial runs the SAME task but starts with DIFFERENT card awareness.

| Trial | Cards in sandbox | Agent knows |
|-------|-----------------|-------------|
| **0-cards** | Empty `/agents/` (except own identity) | Only itself |
| **1-card** | Only 333-AGI card | Itself + 333-AGI |
| **some-cards** | All 5 warga cards | Warga only (no GEOX/WEALTH/WELL organ cards) |
| **all-cards** | Full set (25+ cards) | Complete federation |

## Sandbox Setup

```
/tmp/card-experiment/
├── 0-cards/agents/          # empty
├── 1-card/agents/           # 333-AGI card only
├── some-cards/agents/       # 5 warga cards
├── all-cards/agents/        # all 25+ cards
├── results/                 # experiment output
└── run.sh                   # trial runner
```

## What to Observe

| Signal | What it tells you |
|--------|------------------|
| Did agent find ALL cards needing update? | Coverage |
| Did agent know where GEOS/WEALTH tools live? | Cross-organ awareness |
| Did agent attempt A2A discovery or just read files? | Protocol awareness |
| Did agent ask "who owns geox_basin?" vs just guessing? | Card utility |
| Time to complete task | Efficiency delta |

## How to Run

```bash
# Per trial:
CARD_DIR=/tmp/card-experiment/0-cards/agents
# Agent starts with only $CARD_DIR populated
# Run task, observe behavior, record to /tmp/card-experiment/results/{trial}.md
```

## Deliverable

Compare 4 trials → answer: **is the agent different with more cards?**

Record to `/tmp/card-experiment/results/CONCLUSION.md`.
