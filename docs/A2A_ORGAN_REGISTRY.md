# A2A Organ Registry — Federation Agent Cards

> **SOT:** 2026-07-24 | **seal_seq:** fed-phase-4
> **Canonical:** `/root/AAA/registries/AAA_AGENTS_REGISTRY.json`

## Federation Organs (A2A Agents)

| Agent ID | Organ | Card Path | Status |
|----------|-------|-----------|--------|
| 888-APEX | arifOS | `arifos.arif-fazil.com/.well-known/agent-card.json` | ✅ ACTIVE |
| 777-forge | A-FORGE | `forge.arif-fazil.com/.well-known/agent-card.json` | ✅ ACTIVE |
| 333-AGI | AAA | `aaa.arif-fazil.com/agents/333-AGI/agent-card.json` | ✅ ACTIVE |
| 555-ASI | AAA | `aaa.arif-fazil.com/agents/555-ASI/agent-card.json` | ✅ ACTIVE |
| GEOX | GEOX | `geox.arif-fazil.com/.well-known/agent-card.json` | ✅ ACTIVE |
| WEALTH | WEALTH | `wealth.arif-fazil.com/.well-known/agent-card.json` | ✅ ACTIVE |
| WELL | WELL | `well.arif-fazil.com/.well-known/agent-card.json` | ✅ ACTIVE |
| HERMES | HERMES | `t.me/arifos` | ✅ ACTIVE |

## A2A Protocol Version: 1.0

All agents communicate via A2A protocol through `aaa.arif-fazil.com:3001` gateway.

## Card Schema

All agent cards follow `arifOS/agent-card/v2.2.0` schema with:
- `principal_agent` — type (human/architect/agent/institution/earth/void/liar/llm/model)
- `capabilities` — streaming, pushNotifications, stateTransitionHistory
- `skills` — array of capability declarations
- `security` — authentication methods

## Verification

```bash
# Probe all agent cards
for domain in arifos aaa geox wealth well forge; do
  curl -sf "https://$domain.arif-fazil.com/.well-known/agent-card.json" | jq '.name'
done
```
