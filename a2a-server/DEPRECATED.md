# a2a-server/ — LEGACY (deprecated 2026-07-17)

This directory contains the **original** AAA A2A server implementation (Express + JavaScript).  
It is **superseded** by `src/gateway/` (TypeScript + A2A 1.0 compliant).

## Canonical A2A surface

- **Production gateway:** `src/gateway/server.ts` (TypeScript, A2A 1.0)
- **Agent cards:** `src/seed/agent-card.json` → deployed to `.well-known/agent-card.json`
- **Card migrator:** `src/gateway/a2a-card-migrator.ts`
- **Card inventory:** `src/gateway/card-inventory-loader.ts`

## Why this still exists

The legacy a2a-server/ contains:
- `agent-discovery-routes.js` — old discovery on `/.well-known/agent.json` (deprecated)
- `federation_gateway.js` — pre-1.0 MCP lifecycle bridge
- `a2a-mcp-bridge.js` — merged into `src/gateway/server.ts`
- Agent state machine — superseded by `src/gateway/deliberation.ts`

**Do not add new features here.** All new A2A work goes into `src/gateway/`.

## Migration timeline

- [x] 2026-07-17: Cards migrated to A2A 1.0 format
- [x] 2026-07-17: Discovery path changed to `/.well-known/agent-card.json`
- [x] 2026-07-17: A2A 1.0 schema validation added
- [ ] Future: Remove a2a-server/ after confirming no external clients depend on legacy routes
