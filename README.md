# AAA — Canonical Repo Identity

**DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**

> **⚠️ LEGACY IDENTITY NOTICE**
>
> This repository previously operated under the **WAW** legacy name.
> Its canonical identity is now **AAA** — the agent workspace and control-plane seed.

- **AAA charter:** [`AAA_CHARTER.md`](./AAA_CHARTER.md)
- **OpenClaw seed extraction:** [`AAA_OPENCLAW_SEED.md`](./AAA_OPENCLAW_SEED.md)
- **Canonical source of governance truth:** [`ariffazil/arifOS`](https://github.com/ariffazil/arifOS)
- **Execution shell:** [`ariffazil/A-FORGE`](https://github.com/ariffazil/A-FORGE)

```
WEBSITE_VERSION: 55.2.0
ARIFOS_VERSION:  2026.04.07
STATUS:          OPERATIONAL
AUTHORITY:       888_JUDGE
```

---

## What this repo is now

Historically, `waw` was treated as the frontend presentation layer for arifOS. That framing is now **legacy only**.

This repo is now **AAA**:

- The future **agent workspace**
- The future **control-plane seed**
- The home of **agent identity, contracts, skills, workflows, host adapters, and governance surfaces**
- A migration bridge while public website concerns move toward **`arif-sites`** over time

- **Live site:** [https://arif-fazil.com](https://arif-fazil.com)
- **Canonical MCP runtime:** [https://mcp.arif-fazil.com](https://mcp.arif-fazil.com)
- **Canonical MCP health:** [https://mcp.arif-fazil.com/health](https://mcp.arif-fazil.com/health)
- **Canonical MCP endpoint:** [https://mcp.arif-fazil.com/mcp](https://mcp.arif-fazil.com/mcp)

---

## Repository structure

| Directory / File | Purpose |
|---|---|
| `src/` | Legacy React/Vite surface still present during migration |
| `memory/` | Long-term curated memory |
| `.well-known/` | Discovery endpoints |
| `openclaw/` | OpenClaw authority plane: gateway, ACP, MCP, plugins, A2A, exports |
| `schemas/` | Contract schemas for AAA and OpenClaw runtime artifacts |
| `AGENTS.md` | Agent behavior rules for this codebase |
| `ROOT_CANON.yaml` | Root file precedence and status manifest |
| `AAA_CHARTER.md` | Canonical future direction and ownership boundaries |
| `AAA_OPENCLAW_SEED.md` | Extracted OpenClaw seed for AAA bootstrap |

---

## Ecosystem hierarchy

```text
┌─────────────────────────────────────────────────────────────┐
│  CANONICAL SOURCE OF TRUTH                                  │
│  ├── ariffazil/arifOS                                       │
│  │   Constitutional kernel, doctrine, Floors F1–F13        │
│  └── Runtime truth verified at deployed MCP gateway        │
├─────────────────────────────────────────────────────────────┤
│  RUNTIME SHELL                                              │
│  └── ariffazil/A-FORGE                                      │
│      Metabolic shell, agent runtime, orchestration          │
├─────────────────────────────────────────────────────────────┤
│  CONTROL-PLANE SEED (THIS REPO)                             │
│  ├── ariffazil/AAA                                          │
│  │   Agent workspace, contracts, skills, workflows          │
│  │   host adapters, governance surfaces                     │
│  └── Legacy website/frontend content pending migration      │
├─────────────────────────────────────────────────────────────┤
│  PUBLIC SURFACES                                            │
│  └── ariffazil/arif-sites                                   │
│      Sites, docs portals, rendering surfaces                │
└─────────────────────────────────────────────────────────────┘
```

| Layer | Repo / Surface | Role |
|---|---|---|
| **Kernel** | `ariffazil/arifOS` | Constitutional law, Floors, doctrine, MCP governance kernel |
| **Execution shell** | `ariffazil/A-FORGE` | Metabolic shell, agent runtime, orchestration, observability |
| **Control-plane seed** | `ariffazil/AAA` | Agent workspace, contracts, skills, workflows, host adapters |
| **Public sites** | `ariffazil/arif-sites` | Websites, docs portals, rendering surfaces |

---

## AAA agents

AAA owns the **control-plane agents** — not constitutional judgment (arifOS) and not runtime execution (A-FORGE).

| Agent | Role | Must not own |
|---|---|---|
| **AAA-Agent** | Intent router, workspace conductor | Final verdict authority |
| **ARCHIVIST-Agent** | Canon + memory curator (L1→L2→L3 promotion) | Runtime execution decisions |
| **NOTIFIER-Agent** | Human-loop escalation, HOLD queues, alerts | Adjudication |
| **CONTRACTOR-Agent** | Goals, org, governance, decision schema formalization | Freeform ops execution |
| **BRIDGE-Agent** | OpenClaw / A2A / MCP interop, host adapters | Constitutional overrides |

AAA **thinks about the workspace.**
A-FORGE **runs the workspace.**
arifOS **judges the workspace.**

---

## Technology stack

- **Build tool:** Vite
- **Framework:** React
- **Styling:** Tailwind CSS + Radix UI primitives
- **Deployment:** Cloudflare Pages / VPS

---

## Quick start

```bash
npm install
npm run dev
npm run build
npm run preview
```

---

## Federation status

- **111 Discovery:** live as publishable static assets under `/a2a/` and `/.well-known/`
- **Message ingress:** `888_HOLD` in this repo until a server runtime exposes `/a2a/message`

## A2A Server (FULLY IMPLEMENTED)

AAA now has a production-ready A2A server implementing the Linux Foundation Agent2Agent protocol v0.3.0.

```bash
# Start A2A server
npm run a2a:server

# Development mode with watch
npm run a2a:dev

# Run tests
npm run a2a:test

# Run demo client
npm run a2a:demo
```

### Full Endpoint List

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/.well-known/agent.json` | Public | Agent Card discovery |
| GET | `/agent.json` | Public | Agent Card alias |
| GET | `/a2a/agent/authenticatedExtendedCard` | Required | Extended capabilities card |
| POST | `/message/send` | Optional | Submit task (blocking) |
| POST | `/message/stream` | Optional | Submit task (SSE streaming) |
| GET | `/tasks/:taskId` | Optional | Get task status |
| GET | `/tasks` | Optional | List tasks with filters |
| POST | `/tasks/:taskId/cancel` | Optional | Cancel a task |
| POST | `/tasks/:taskId/pushNotificationConfig/set` | Optional | Configure push notifications |
| GET | `/tasks/:taskId/pushNotificationConfig/get` | Optional | Get push notification config |
| GET | `/tasks/:taskId/subscribe` | Optional | SSE subscribe to task updates |
| GET | `/health` | Public | Health check |

### Authentication

- **Bearer Token**: `Authorization: Bearer <token>`
- **API Key**: `X-API-Key: <key>`
- **OAuth 2.0**: Via authorization flow
- **None**: Development mode

### Skills

| Skill ID | Triggers | Description |
|----------|----------|-------------|
| `agent-dispatch` | "dispatch", "send", "task" | Task dispatch to specialists |
| `agent-handoff` | "handoff", "transfer", "delegate" | Context handoff |
| `status-query` | "status", "check", "query" | Read-only status |

### Example Request

```bash
curl -X POST http://localhost:3001/message/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "dispatch a task to planner"}],
        "messageId": "test-123"
      }
    }
  }'
```

### Example Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "aaa-abc123def456",
    "contextId": "550e8400-e29b-41d4-a716-446655440000",
    "status": {
      "state": "completed",
      "message": {
        "role": "agent",
        "parts": [{"kind": "text", "text": "[AAA Gateway] Task dispatched..."}],
        "messageId": "resp-456"
      },
      "timestamp": "2026-04-22T12:00:00.000Z"
    },
    "kind": "task"
  }
}
```

### Deploy with Docker

```bash
# Build and run
docker build -f src/lib/a2a/Dockerfile -t aaa-a2a-server .
docker run -p 3001:3001 aaa-a2a-server

# Or use docker-compose
docker-compose -f src/lib/a2a/docker-compose.yml up -d
```

See [`src/lib/a2a/README.md`](./src/lib/a2a/README.md) for full documentation.

---

## Institutional model

- **222:** canonical Goal → Task → Verdict chain lives under `contracts/goals/`
- **333:** canonical OrgUnit + topology graph lives under `contracts/org/`

---

## Governance trail

- **666 / 777:** governance gates and budget policies live under `contracts/governance/`
- **888 / 999:** decision objects and vault export mapping live under `contracts/decisions/` and `vault/decisions/`

---

## Constitutional alignment

This codebase follows the same constitutional direction as arifOS, while **constitutional authority remains in arifOS**.

- **F1 Amanah** — Reversible changes, git-first discipline
- **F2 Truth** — Accurate documentation and clear contracts
- **F9 Anti-Hantu** — No dark patterns, no shadow behavior
- **F13 Sovereign** — Human authority remains final

AAA may model and surface governance.
It does not replace the kernel.

---

## Links

| Resource | URL |
|---|---|
| arifOS (SoT) | [https://github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS) |
| A-FORGE | [https://github.com/ariffazil/A-FORGE](https://github.com/ariffazil/A-FORGE) |
| Runtime gateway | [https://mcp.arif-fazil.com](https://mcp.arif-fazil.com) |
| Runtime health | [https://mcp.arif-fazil.com/health](https://mcp.arif-fazil.com/health) |
| MCP endpoint | [https://mcp.arif-fazil.com/mcp](https://mcp.arif-fazil.com/mcp) |
| Main site | [https://arif-fazil.com](https://arif-fazil.com) |

---

**License:** AGPL-3.0-only
**Authority:** 888_JUDGE — Muhammad Arif bin Fazil
**Website:** [https://arif-fazil.com](https://arif-fazil.com)

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
