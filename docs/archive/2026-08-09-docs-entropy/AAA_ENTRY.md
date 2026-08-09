<!-- SATELLITE | tier:satellite | sot:STATE.md | 2026-08-09 -->
> **Satellite** — historical elaboration / design note / prior draft.  
> **Canonical SOT:** [`STATE.md`](./STATE.md) (§1–16).  
> If this file conflicts with STATE.md, **STATE wins**. Do not fork law here.  
> *One truth · Many projections · 0 contradictions* · DITEMPA BUKAN DIBERI.

# AAA — Entry Point

**Status:** OPERATIONAL | **Organ:** BODY (Ω) | **Authority:** arifOS

## Quick Start
```bash
npm install && npm run dev
```

## MCP Server (A2A Gateway)
```bash
# Start A2A MCP gateway (port 3001)
npm run a2a:server

# Health check
curl http://localhost:3001/health
curl https://aaa.arif-fazil.com/health
```

## Critical Files
| File | Purpose |
|------|---------|
| `src/App.tsx` | Root React component |
| `src/Cockpit.tsx` | Operator dashboard |
| `services/a2a-gateway/server.js` | A2A gateway (port 3001) |
| `registries/agents.yaml` | Canonical agent registry (15 agents, HEXAGON 4.1) |

## Build Commands
| Command | Purpose |
|---------|---------|
| `npm install` | Install dependencies |
| `npm run dev` | Dev server (http://localhost:5173) |
| `npm run build` | Production build |
| `npm run a2a:server` | Start A2A MCP gateway |

## Federation
```
AAA (Body) ←→ arifOS (Kernel) ←→ A-FORGE (Forge)
```

See `.AGENTS.md` for full agent onboarding context.

**999 SEAL ALIVE**
