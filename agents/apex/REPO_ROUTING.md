# REPO_ROUTING.md — APEX Agent Repo Ownership Guide

## Memory canonical home
`AAA/agents/apex/MEMORY.md` — full VPS state
`AAA/agents/apex/USER.md` — Arif identity and preferences

## Repo routing rules

| Repo | What APEX owns here | What it does NOT own |
|------|----------------------|---------------------|
| **AAA** | Agent profiles, memory schema, cross-agent contracts, USER.md, MEMORY.md | Kernel law, infra runtime truth |
| **arifOS** | Constitutional tool names, F1-F13 floor semantics, 888 HOLD definition, 000-999 pipeline | Personal style notes, operator preferences |
| **A-FORGE** | VPS container inventory, port mappings, transport incidents, deployment topology, ops guards | Federation-wide law, human identity |
| **GEOX** | Domain MCP wiring gaps, petrophysics-specific memory and witnesses, GEOX bridge status | Full VPS inventory, operator profile |
| **WEALTH** | SSE transport issue, valuation-domain constraints, WEALTH-specific MCP notes | General operator profile, unrelated domain facts |

## File placement standard

- Hermes shared memory: `AAA/agents/hermes/`
- Constitutional references: `arifOS/docs/canon/`
- Runtime audit facts: `A-FORGE/ops/runtime/`
- Domain integration notes: `GEOX/docs/integration/`, `WEALTH/docs/integration/`

## Branch naming
All Apex memory changes use branch: `canon/apex-memory-v1`

## Commit size rule
One focused commit per repo. Rollback must be reversible per file.

## Last updated
2026-05-05
