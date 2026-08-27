---
id: FORGE-call-map
name: FORGE-call-map
description: "Use when mapping every callable in the federation or planning boot-time call contracts between FI harnesses. Use when mapping every callable in the federation or planning boot-time call contracts between FI harnesses. Boot-time call contract: how to invoke every FI harness, organ MCP, A2A target, and FED socket. AAA 3-layer cards = directory (who). This skill = telephone (how). Load on session start."
version: 1.0.0
risk_tier: low
autonomy_tier: T0
owner: AAA
triggers:
  - "how do I call"
  - "invoke opencode"
  - "spawn coder"
  - "call map"
  - "macam mana nak call"
  - session boot / init when dispatching to another agent
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# FORGE-call-map

## Load first when

- Dispatching work to OpenCode / Claude / Kimi / Grok / Codex
- Hermes or OpenClaw needs to spawn a coder
- Agent says "I don't know how to call X"

## Canonical paths

| Form | Path |
|------|------|
| Human | `/root/AAA/docs/CALL_MAP.md` |
| Machine | `/root/AAA/federation/call_map.yaml` |

## Rule

1. Read CALL_MAP (or yaml twin).
2. Probe target health.
3. Prefer **local CLI** on same VPS; A2A when cross-process/mesh; MCP for organs.
4. Respect boundary column (T3 HOLD / organ ceiling).
5. Do **not** treat FED as a person — FED is model transport.

## Quick coding path

```bash
opencode run "<task>"
```

## Related

- Directory: AAA agent cards / `AGENTS_UNIFIED.yaml`
- Route intent: skill `route-dispatch` + `arif_route`
- Handoff packet: `FORGE-cross-agent-handoff`
