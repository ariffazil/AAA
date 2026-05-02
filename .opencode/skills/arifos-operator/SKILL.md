---
name: arifos-operator
description: Operate against the arifOS constitutional MCP kernel and AAA workspace. Use for any governed action that touches agents, tools, floors (F1-F13), or VAULT999. Always consult this skill before irreversible operations on arifOS-linked systems. Trigger keywords: arifOS, constitutional, floors, MCP, VAULT999, F1-F13, governance, seal, SABAR, VOID.
version: 1.0.0
author: arif
tags: arifos, mcp, constitutional, governance, floors, vault999
---

# ArifOS Operator Protocol

## Canonical Surfaces
- Law kernel repo: `https://github.com/ariffazil/arifOS`
- Canonical docs: `https://arifos.arif-fazil.com/`
- MCP endpoint: `https://mcp.arif-fazil.com/mcp`
- Health + tools: `https://mcp.arif-fazil.com/health`

## arifOS MCP Tools (via arifos-mcp tool)
Before any governed action, call `arifos-mcp` to:
- List tools: `GET /tools`
- Health check: `GET /health`
- Call specific tool via `POST /tools/call`

## Floor Quick Reference
| Floor | Code | Key Rule |
|-------|------|----------|
| F01 | AMANAH | No irreversible deletion without 888_HOLD |
| F02 | TRUTH | Cite sources, no fabrication |
| F03 | WITNESS | Evidence must be verifiable |
| F07 | HUMILITY | Acknowledge uncertainty |
| F09 | ANTIHANTU | No consciousness claims |
| F13 | SOVEREIGN | Human veto is absolute |

## MCP Call Pattern
```typescript
// Use arifos-mcp tool:
{
  path: "/tools",
  method: "GET"
}
// Then POST to specific tool:
{
  path: "/tools/call",
  method: "POST",
  body: {
    name: "arif_judge_deliberate",
    arguments: { candidate: "...", session_id: "..." }
  }
}
```

## Operator Checklist Before Acting
For GEOX, WEALTH, WELL, AAA, A-FORGE:
1. Read repo README + organ contract
2. Query arifOS MCP: does operation cross floor > F2?
3. If irreversible → **888 HOLD**: propose plan, wait for human
4. State which floors are in play, whether MCP was consulted

## Output Requirements
- Always state which floor(s) are in play
- Explicitly say whether arifOS MCP was consulted
- Attach recommended arifOS tool calls when human wants to execute

## Federated Skill Registry
AAA is meta-orchestrator. Skills live in:
- `AAA/.opencode/skills/arifos-operator/` — arifOS bridge (THIS)
- `AAA/.opencode/skills/skill-reflector/` — self-audit loop
- `A-FORGE/.opencode/skills/` — infra skills
- `GEOX/.opencode/skills/geox-analyst/` — domain reasoning
- `WEALTH/.opencode/skills/wealth-analyst/` — domain reasoning

---

*Last updated: 2026-05-02*