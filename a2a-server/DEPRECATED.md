# a2a-server/ — LIVE, MISLABELLED

> **Correction 2026-09-13 (FI-008).** This file previously declared this
> directory *"LEGACY (deprecated 2026-07-17)"*. That declaration was never
> carried out. **This directory IS the production A2A gateway.** The original
> notice is preserved verbatim at the bottom for audit.

## Verified reality — 2026-09-13

| Fact | Evidence |
|---|---|
| Live gateway runs from here | `systemctl cat aaa-a2a.service` → `ExecStart=/usr/bin/node /root/AAA/a2a-server/server.js` |
| Service is up | `aaa-a2a.service` active/running · `curl 127.0.0.1:3001/` → 200 |
| Protocol | `{"service":"AAA A2A Gateway","version":"1.2","protocol_version":"1.2","auth":"required"}` |
| Live discovery surface | `/.well-known/a2a-discovery.json` · `/.well-known/agent-card.json` · `/.well-known/arifos-federation.json` |
| Live task surface | `POST /tasks` · `GET /tasks/{taskId}` · `GET /tasks/{taskId}/stream` |
| Declared successor runs nowhere | `/root/AAA/src/gateway/server.ts` exists; **no TS gateway process is running** |
| Legacy `/a2a/*` path | absent from the live Caddyfile (only in `Caddyfile.bak.*`) · public `/a2a` → **404** |

Modules added to this directory **after** the deprecation notice, through 2026-08-10:
`fq_gate.js` · `witness_gate.js` · `art_gate.js` · `predict_gate.js` ·
`membrane_middleware.js` · `seal_chain.js` · `cognitive_hierarchy.js` ·
`federation_envelope.js` · `mesh_coordinator.js` · `agent-card-registry.js` (+more)

`server.js` requires exactly those post-deprecation modules. The notice was
ignored for three weeks while this directory became the production system.

## Genuinely retired modules — do NOT add features to these

- **`a2a-mcp-bridge.js`** — retired; merged into `src/gateway/server.ts`.
  Imported **only** by `tests/test_a2a_dependencies.js` and
  `tests/e2e-cross-organ-flow.js`. Nothing in the production require chain
  loads it.
  ⚠️ *Observed 2026-09-13:* an APEX-ZEN MUTATE gate was written into this file.
  It has never executed — it was placed in the single truly-dead module of a
  live directory. 0 `apex_zen_blocked` events exist in VAULT999.
- `agent-discovery-routes.js` — old discovery on `/.well-known/agent.json`
- `federation_gateway.js` — pre-1.0 MCP lifecycle bridge
- Agent state machine — superseded by a deliberation module

## Open decision — F13, not for agents to settle

Two coherent futures; pick one:

- **A. Declare the truth.** This directory is production. Scope/retire this
  notice, and route new A2A work through `server.js`'s require chain.
- **B. Complete the migration.** Finish the move to `src/gateway/server.ts`,
  then retire this tree properly.

Until one is chosen, agents will keep re-deriving work that cannot run here.
This contradiction produced three separate false conclusions on 2026-09-13
alone (a gate reported "live", a "405" chased on a dead path, "dual cards").

---

## Original notice — retained for audit (superseded, inaccurate)

# a2a-server/ — LEGACY (deprecated 2026-07-17)

This directory contains the **original** AAA A2A server implementation (Express + JavaScript).
It is **superseded** by `src/gateway/` (TypeScript + A2A 1.0 compliant).

## Canonical A2A surface

- **Production gateway:** `src/gateway/server.ts` (TypeScript, A2A 1.0)
- **Agent cards:** `src/seed/agent-card.json` → deployed to `.well-known/agent-card.json`
- **Card migrator:** `src/gateway/a2a-card-migrator.ts`
- **Card inventory:** `src/gateway/card-inventory-loader.ts`

## Migration timeline

- [x] 2026-07-17: Cards migrated to A2A 1.0 format
- [x] 2026-07-17: Discovery path changed to `/.well-known/agent-card.json`
- [x] 2026-07-17: A2A 1.0 schema validation added
- [ ] Future: Remove a2a-server/ after confirming no external clients depend on legacy routes
