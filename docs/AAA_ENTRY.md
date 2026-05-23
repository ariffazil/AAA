# AAA — Entry Point
**Status:** OPERATIONAL | **Organ:** BODY (Ω) | **Authority:** arifOS

## Quick Start
```bash
npm install && npm run dev
```

## Critical Files
| File | Purpose |
|------|---------|
| `src/App.tsx` | Root React component |
| `src/Cockpit.tsx` | Operator dashboard |
| `services/a2a-gateway/server.js` | A2A gateway (port 3001) |
| `a2a/registry/agent-cards.json` | Agent registry |

## Health Check
```bash
curl http://localhost:3001/health
curl https://aaa.arif-fazil.com/health
```

## Build Commands
```bash
npm install          # Install deps
npm run dev         # Dev server (http://localhost:5173)
npm run build       # Production build
npm run a2a:server # Start A2A gateway
```

## Federation
```
AAA (Body) ←→ arifOS (Kernel) ←→ A-FORGE (Forge)
```

See `.AGENTS.md` for full agent onboarding context.
**999 SEAL ALIVE**