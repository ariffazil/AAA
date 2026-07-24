# Federation Agent Card Registry

> **SOT:** 2026-07-24 | **seal_seq:** fed-phase-5
> **Canonical path:** `/root/AAA/registries/AAA_AGENTS_REGISTRY.json`
> **Total cards:** 25+ across 7 organs

## Core Organs (7)

| Card ID | Organ | Path | Principal |
|---------|-------|------|-----------|
| arifOS | arifOS | `.well-known/agent-card.json` | architect |
| A-FORGE | A-FORGE | `.well-known/agent-card.json` | agent |
| AAA | AAA | `.well-known/agent-card.json` | architect |
| GEOX | GEOX | `.well-known/agent-card.json` | earth |
| WEALTH | WEALTH | `.well-known/agent-card.json` | agent |
| WELL | WELL | `.well-known/agent-card.json` | institution |
| HERMES | HERMES | `.well-known/agent-card.json` | agent |

## AAA Governance Agents (4)

| Card ID | Directory | Role |
|---------|-----------|------|
| 333-AGI | `AAA/agents/333-AGI/` | Reasoner — multi-domain evidence synthesis |
| 555-ASI | `AAA/agents/555-ASI/` | Memory keeper — institutional continuity |
| 777-forge | `AAA/agents/777-forge/` | Executor — governed execution |
| 888-APEX | `AAA/agents/888-APEX/` | Judge — constitutional verdicts |

## AAA Edge Agents (7)

| Card ID | Directory | Type |
|---------|-----------|------|
| hermes-asi | `AAA/agents/hermes-asi/` | Telegram bridge |
| main | `AAA/agents/main/` | Primary operator |
| makcikgpt | `AAA/agents/makcikgpt/` | Malaysian AI chat |
| openclaw | `AAA/agents/openclaw/` | Gateway operator |
| opencode | `AAA/agents/opencode/` | Forge worker |
| prospect-maturation | `AAA/agents/prospect-maturation/` | GEOX pipeline |
| agent-zero | `AAA/agents/agent-zero/` | Experimental agent |

## GEOX Skill Agents (11)

| Card ID | Path | Domain |
|---------|------|--------|
| atmosphere | `GEOX/skills/atmosphere/` | Climate |
| geodesy | `GEOX/skills/geodesy/` | Positioning |
| governance | `GEOX/skills/governance/` | Policy |
| hazards | `GEOX/skills/hazards/` | Risk |
| infrastructure | `GEOX/skills/infrastructure/` | Systems |
| mobility | `GEOX/skills/mobility/` | Transport |
| orchestration | `GEOX/skills/orchestration/` | Pipeline |
| planner | `GEOX/skills/planner/` | Strategy |
| sensing | `GEOX/skills/sensing/` | Observation |
| terrain | `GEOX/skills/terrain/` | Geomorphology |
| water | `GEOX/skills/water/` | Hydrology |

## Verification

```bash
# Count all agent cards
find /root/{AAA,arifOS,A-FORGE,GEOX,WEALTH,WELL,HERMES} \
  -name "agent-card.json" | wc -l

# Validate all cards are valid JSON
find /root/{AAA,arifOS,A-FORGE,GEOX,WEALTH,WELL,HERMES} \
  -name "agent-card.json" -exec python3 -c \
  "import json; json.load(open('{}')); print('✅ {}')" \;
```
