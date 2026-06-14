<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-06-14
valid_from: 2026-05-19
valid_until: 2026-07-14
confidence: high
scope: /
-->

# BOUNDARY.md — AAA Agent Workspace & Control Plane

> **DITEMPA BUKAN DIBERI** — Forged, not given.

## Owns

- **Operator Cockpit UX** — React 19 + Vite dashboard, constitutional floors display, operator task queue
- **Agent Identity & Workflows** — Per-agent identity directories, skills library, workflow definitions
- **Agent Runtime Homes** — Hermes/OpenClaw/Codex/Kimi/OpenCode/Copilot runtime mirrors, ignored secrets, sessions, skills, and workspace state
- **A2A Gateway (TypeScript)** — Standalone Express A2A server (port 3001), agent-to-agent mesh protocol
- **Host Adapters** — GovernanceAdapter routing intent to A-FORGE / arifOS /sense endpoints
- **Session Surfaces** — WebMCP init, client-side session management, operator visibility
- **Control-Plane Seed Data** — SOUL.md, IDENTITY.md, canonical agent personas
- **Static Sites (subsidiary)** — Static HTML subsites under `sites/` (hosted on Cloudflare Pages + VPS)

## Does Not Own

- **Constitutional Law** — F1–F13 enforcement, verdict engine, vault sealing (owned by arifOS)
- **Deep Domain Engines** — Geospatial reasoning, subsurface modeling (owned by GEOX)
- **Capital Logic** — NPV/IRR, portfolio optimization, economic scoring (owned by WEALTH)
- **Deployment Orchestration** — Docker compose, release assembly, infrastructure (owned by A-FORGE)
- **MCP Server Runtime** — FastMCP server, tool registry, schema authority (owned by arifOS)
- **Vault / Seal Authority** — Append-only ledger, cryptographic seals (owned by arifOS)
- **APEX Verdict Service Source** — CommonJS Express verdict service source (owned by `/root/APEX`; AAA only references it)

## Imports From

| Source | What | Interface |
|--------|------|-----------|
| **arifOS** | Tool registry, floor status, session tokens, governance verdicts | MCP streamable-http (port 8080), `/api/status`, `/api/federation-probe` |
| **A-FORGE** | Build artifacts, deploy status, release metadata | HTTP bridge (port 7071), GitHub releases |
| **GEOX** | Earth-truth artifacts, prospect cards, spatial evidence | MCP mesh via A2A gateway |
| **WEALTH** | Capital scores, decision memos, viability ratings | MCP mesh via A2A gateway |
| **WELL** | Human readiness signals, substrate health | Health endpoint (port 8083) |
| **APEX** | Verdict envelopes and service health | HTTP service (port 3002), A2A bridge |

## Exports To

| Consumer | What | Interface |
|----------|------|-----------|
| **arifOS** | Operator intent, session assertions, identity packs | A2A v1.0.0 mesh protocol |
| **A-FORGE** | Deploy triggers, release approval signals, operator commands | Webhook, A2A relay |
| **All agents** | Agent identity schemas, skill manifests, workflow templates | A2A mesh, static JSON |
| **Hermes ASI** | Runtime home, session archive, skills, memory mirror | `/root/AAA/agents/hermes-asi/runtime/` (ignored by git) |

## Known Boundary Violations (888 HOLD Queue)

1. **A2A authority overlap** — AAA runs `a2a-server/` (port 3001) while arifOS also has A2A routes in `runtime/rest_routes.py`. One must be canonical.
2. **GovernanceAdapter depth** — `src/adapter/router.ts` routes to A-FORGE `/sense` but also interprets floor results. Risk of duplicating arifOS judgment logic.
3. **Static site estate** — `sites/` directory contains both AAA-branded and non-AAA sites (arif-fazil.com flagship). Consider moving non-AAA sites to `arif-sites`.

## Canonical Surfaces

- **Frontend:** React 19 + Vite dev server (`npm run dev`)
- **A2A Server:** Express on port 3001 (`node a2a-server/server.js`)
- **Export:** AAA contract validation (`npm run validate:aaa`, `npm run export:aaa`)
