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
