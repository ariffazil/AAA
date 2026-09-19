---
id: FORGE-call-map
name: forge-call-map
description: "Use when mapping every callable in the federation or planning boot-time call contracts between FI harnesses."
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

## NEW — 2026-09-18 (canonical13 ↔ legacy argument-translation table)

arifOS exposes a public surface (`arif_*`) AND internal canonical13 (`arif_init`, `arif_observe`, etc.). Probe 2026-09-18T06:38Z showed 5/8 public names resolve+execute; 3 contract drifts remain:

| Public name | Internal | Status | Drift |
|---|---|---|---|
| `arif_sense_observe` | `arif_observe` | ✅ works | — |
| `arif_mind_reason` | `arif_think` | ✅ works | — |
| `arif_ops_measure` | `arif_measure` | ✅ works | — |
| `arif_heart_critique` | `arif_judge` | ⚠️ executes, degraded_fallback | verdict geometry drift |
| `arif_kernel_route` | `arif_route` | ⚠️ works without `mode` | `mode='status'` rejected |
| `arif_gateway_connect` | `arif_bridge_connect` | ❌ schema mismatch | `mode` arg not translated to `organ`+`tool_name` |
| `arif_session_budget` | unknown | ❌ Unknown tool | not registered |

**Adapter translation rule:** When public tool requires `mode=` arg, internal handler expects positional or different-keyword. ALWAYS probe with no-arg first, then escalate. Never assume advertised schema matches callable schema.

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
