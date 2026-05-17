---
title: "SKILL: arifOS Operator Protocol"
type: skill
version: 1.0.0
category: governance
risk_band: HIGH
floors: [F1, F2, F3, F4, F11, F12, F13]
evidence_required: true
sources: [/root/.opencode/skills/arifos-operator/SKILL.md]
confidence: high
---

# SKILL: arifOS Operator Protocol

> **Source:** `/root/.opencode/skills/arifos-operator/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Any governed action touching agents, tools, floors (F1-F13), or VAULT999
- Operating against arifOS constitutional MCP kernel
- Cross-organ coordination
- Keywords: arifOS, constitutional, floors, MCP, VAULT999, F1-F13, governance, seal

---

## Pre-Context (Read Before Acting)

Before any governed action, read:
1. `/root/AGENTS.md` — Landing protocol, repo atlas, authority boundaries
2. `/root/CONTEXT.md` — Current focus, blockers, alerts, repo health
3. `/root/CLAUDE.md` — Current session context
4. `/root/MEMORY.md` — Curated long-term memory

---

## Canonical Surfaces

| Surface | URL/Path |
|---------|----------|
| Law kernel repo | `https://github.com/ariffazil/arifOS` |
| Canonical docs | `https://arifos.arif-fazil.com/` |
| MCP endpoint | `https://mcp.arif-fazil.com/mcp` |
| Health + tools | `https://mcp.arif-fazil.com/health` |

---

## Floor Quick Reference

| Floor | Code | Key Rule |
|-------|------|---------|
| F01 | AMANAH | No irreversible deletion without 888_HOLD |
| F02 | TRUTH | Cite sources, no fabrication |
| F03 | WITNESS | Evidence must be verifiable |
| F07 | HUMILITY | Acknowledge uncertainty |
| F09 | ANTIHANTU | No consciousness claims |
| F13 | SOVEREIGN | Human veto is absolute |

---

## Operator Checklist

For GEOX, WEALTH, WELL, AAA, A-FORGE:

```
1. Read repo README + organ contract
2. Query arifOS MCP: does operation cross floor > F2?
3. If irreversible → 888_HOLD: propose plan, wait for human
4. State which floors are in play
5. State whether MCP was consulted
6. Attach recommended arifOS tool calls when human wants to execute
```

---

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

---

## Output Requirements

Every operator action must state:
- Which floor(s) are in play
- Whether arifOS MCP was consulted
- Recommended arifOS tool calls for execution

---

## Related Pages

- [[skill-constitutional-reasoning]] — full reasoning framework
- [[skill-constitutional-advisor]] — F1-F13 quick reference
- [[skill-arifos-federation]] — federation atlas
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Govern first, operate second.*
