---
name: ASI-mcp-governor
description: Governed MCP routing via arifOS F1-F13
homepage: https://arif-fazil.com
metadata:
  openclaw:
    emoji: 🫀
    requires:
      bins:
      - mcporter
    install:
    - id: node
      kind: node
      package: mcporter
      bins:
      - mcporter
      label: Install mcporter
owner: AAA
---
# arif-mcp-governor

Governed MCP routing via arifOS F1-F13. Routes organ calls through arifOS kernel for C2+/IRREVERSIBLE tools.

## Architecture

```
OpenClaw → arifOS MCP (8080) → arifOS F1-F13 judgment
                ↓ (on SEAL)
           GEOX (8081) / WEALTH (8082) / WELL (8083)
```

## Risk Tiers

| Tier | Action |
|------|--------|
| `readonly` | Execute directly, log to VAULT999 |
| `c1` | arifOS pre-check, execute anyway |
| `c2` | **arifOS SEAL required** |
| `irreversible` | **arifOS SEAL + ack_irreversible required** |

## Tool Discovery

```bash
# List all registered organ tools
mcporter list --config /root/arifOS/CONFIG/mcporter.json

# List GEOX tools
mcporter list geox --schema

# List WEALTH tools
mcporter list wealth-organ --schema
```

## Making Calls

### Direct (for READONLY/C1 tools)

```bash
mcporter call geox.geox_well_analyze_sequence source=/data/well.las zone_top:=1000 zone_base:=2000 --config /root/arifOS/CONFIG/mcporter.json --output json
```

### Governed (for C2/IRREVERSIBLE tools)

C2+ tools MUST be called via arifOS MCP first to get SEAL:

1. Call `arif_judge` on arifOS MCP (port 8080)
2. If verdict = SEAL → call the organ tool via mcporter
3. If verdict = HOLD → return HOLD to caller
4. If verdict = VOID → reject

Example flow for `geox_prospect_judge_seal`:
```bash
# Step 1: Get arifOS SEAL
curl -X POST http://localhost:8080/mcp -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "arif_judge",
    "arguments": {
      "mode": "judge",
      "candidate": "{\"action\":\"GEOX_ORGAN:geox_prospect_judge_seal\",\"description\":\"GEOX irreversible prospect judgment\"}",
      "actor_id": "openclaw"
    }
  }
}'

# Step 2: If verdict=SEAL → call organ
mcporter call geox.geox_prospect_judge_seal prospect_ref:=MY_PROSPECT ac_risk_score:=0.3 ack_irreversible:=true --config /root/arifOS/CONFIG/mcporter.json
```

## Organ Endpoints

| Organ | URL | Risk Profile |
|-------|-----|-------------|
| geox | http://geox_eic:8081 | 30 tools, C2+ requires SEAL |
| wealth-organ | http://wealth-organ:8082 | 33 tools, C2+ requires SEAL |
| well | http://well:8083 | 14 tools, C1+ advisory |

## Registered Servers (mcporter.json)

Located at: `/root/arifOS/CONFIG/mcporter.json`

Contains: `context7`, `codegraphcontext`, `arifos`, `geox`, `wealth-organ`, `well`
