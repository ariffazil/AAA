---
name: ASI-mcp-governor
description: Governed MCP routing via arifOS F1-F13. All calls to GEOX, WEALTH, WELL organs must route through arifOS kernel for C2+/IRREVERSIBLE tools. Uses mcporter for stdio/HTTP bridging.
homepage: https://arif-fazil.com
metadata:
  openclaw:
    emoji: "🫀"
    requires:
      bins: ["mcporter"]
    install:
      - id: node
        kind: node
        package: mcporter
        bins: ["mcporter"]
        label: "Install mcporter"
---

# arif-mcp-governor

Governed MCP routing via arifOS F1-F13. Routes organ calls through arifOS kernel for C2+/IRREVERSIBLE tools.

## Architecture

```
OpenClaw → arifOS MCP :8088 → arifOS F1-F13 judgment
                         ↓ (on SEAL)
              GEOX :8081 / WEALTH :18082 / WELL :18083
```

The public MCP door is `https://mcp.arif-fazil.com/mcp`; the organ hostnames are compatibility surfaces. `mcporter` discovers the configured servers and their live schemas; never copy a stale tool count from this skill into an operational claim.

## Risk Tiers

| Tier | Action |
|------|--------|
| `readonly` | Execute directly, log to VAULT999 |
| `c1` | arifOS pre-check, execute anyway |
| `c2` | **arifOS SEAL required** |
| `irreversible` | **arifOS SEAL + ack_irreversible required** |

## Tool Discovery

```bash
# Live server inventory and health
mcporter list

# Live schemas for one server
mcporter list arifos --schema
mcporter list geox --schema
mcporter list wealth --schema
mcporter list well --schema
mcporter list aforge --schema
```

The configured server imports are editor/runtime state, not a repository file. Record the discovery timestamp and source before using counts in a report.

## Making Calls

### Direct (for READONLY/C1 tools)

```bash
mcporter call geox.geox_well_analyze_sequence source=/data/well.las zone_top:=1000 zone_base:=2000 --output json
```

### Governed (for C2/IRREVERSIBLE tools)

C2+ tools MUST be called via arifOS MCP first to get SEAL:

1. Call `arif_judge` on the canonical arifOS MCP path (`:8088` internally).
2. If verdict = SEAL → call the organ tool via mcporter.
3. If verdict = HOLD → return HOLD to caller.
4. If verdict = VOID → reject.

**Authority requirement (2026-07-15 kernel test):**
`arif_judge` requires SOVEREIGN authority (`requires_888_hold = True`). The kernel interceptor resolves authority from **transport-level JWT/DPoP verification only** — self-reported `actor_id` caps at MEDIUM and will always get `888_HOLD`.

To reach SOVEREIGN, the caller must present a valid JWT token in the `Authorization: Bearer <token>` header. Without JWT, judge calls return `888_HOLD` regardless of session state.

Example flow:

```bash
# Step 1: submit the candidate to arifOS through the canonical MCP door
curl -X POST https://mcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARIFOS_JWT" \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"tools/call",
    "params":{"name":"arif_judge","arguments":{
      "mode":"judge",
      "candidate":"{\"action\":\"GEOX_ORGAN:geox_prospect\",\"description\":\"Prospect evaluation\"}",
      "actor_id":"openclaw"
    }}
  }'

# Step 2: only after a returned SEAL, call the organ tool
mcporter call geox.geox_prospect prospect_ref:=MY_PROSPECT --output json
```

## Organ Endpoints

| Organ | Internal MCP | Public MCP surface | Risk profile |
|-------|--------------|--------------------|--------------|
| arifOS | `http://127.0.0.1:8088/mcp` | `https://mcp.arif-fazil.com/mcp` | Governance/judge/seal |
| A-FORGE | `http://127.0.0.1:7072/mcp` | `https://mcp.arif-fazil.com/mcp` via kernel | Execution; lease required |
| GEOX | `http://127.0.0.1:8081/mcp` | `https://geox.arif-fazil.com/mcp` compatibility | Earth evidence |
| WEALTH | `http://127.0.0.1:18082/mcp` | `https://wealth.arif-fazil.com/mcp` compatibility | Capital computation |
| WELL | `http://127.0.0.1:18083/mcp` | `https://well.arif-fazil.com/mcp` compatibility | Reflect-only readiness |

## Registered Servers

`mcporter list` is the live source for configured server names, transport, health, and tool counts. Do not refer to the removed `/root/arifOS/CONFIG/mcporter.json`; it is not present on this machine. When a server is offline, label it OFFLINE rather than copying its last-known count.

