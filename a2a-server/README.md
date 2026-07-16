# AAA A2A Server — Agent-to-Agent Protocol Gateway

Standalone Express server implementing the A2A (Agent-to-Agent) protocol for
the arifOS federation. This is the production runtime that powers the
`https://aaa.arif-fazil.com` agent card endpoint and task routing.

It is **not** the static cockpit site. The React cockpit is built from the repo
root and published separately via GitHub Pages at `https://arif-fazil.com`.

## Quick Start

```bash
cd a2a-server
npm install
cp ../.env.example .env   # or configure directly
node server.js             # listens on port 3001
```

## What It Does

- Serves agent cards at `/.well-known/agent-card.json` and `/a2a/agents.json`
- Routes A2A tasks between federation organs (arifOS, GEOX, WEALTH, WELL, A-FORGE)
- Connects to NATS event bus for real-time orchestration
- Writes sealed verdicts to VAULT999 via the vault writer endpoint
- Enforces federation envelope validation before task execution

## Architecture

```
Client (agent/UI)
    ↓
A2A Server (port 3001)
    ├── NATS → arifOS governance stream
    ├── Redis → session state + telemetry
    └── VAULT999 Writer → sealed verdicts (port 5001)
```

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness probe |
| GET | `/.well-known/agent-card.json` | A2A agent discovery |
| GET | `/a2a/agents.json` | HEXAGON agent registry |
| POST | `/a2a/tasks` | Submit A2A task for routing |
| GET | `/a2a/tasks/:id` | Check task status |

## Related

- [AAA Cockpit](../README.md) — the React frontend and control plane
- [arifOS Constitution](https://github.com/ariffazil/arifOS) — F1-F13 floors
- [HEXAGON Agents](../agents/) — agent identity directories
