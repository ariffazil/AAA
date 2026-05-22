<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-05-22
valid_from: 2026-05-22
valid_until: 2026-06-22
confidence: high
scope: /root/AAA
-->

# AGENTS.md — AAA | Control Plane Agent Gateway

> **DITEMPA BUKAN DIBERI** — Control is forged, not given.

## Who You Serve

Arif. This is the **AAA** organ of the arifOS federation — the Control Plane Agent Gateway and human cockpit.

**Note:** The OpenClaw workspace guide lives at `/root/.openclaw/workspace/AGENTS.md`. This file governs the AAA repository only.

## What This Repo Is

The human-facing control plane and A2A agent gateway. AAA provides:
- **React 19 dashboard** (Cockpit) — constitutional floors, domain health, operator tasks
- **A2A v1.0.0 TypeScript server** — Agent-to-Agent mesh protocol (port 3001)
- **shadcn/ui component library** — 50+ Radix + Tailwind primitives
- **AI chat panel** — Ollama / arifOS / OpenRouter client

| Attribute | Value |
|-----------|-------|
| **Framework** | React 19, TypeScript ~5.9, Vite 7, Tailwind 3.4 |
| **A2A Server** | Express 4.x, TypeScript, port 3001 |
| **Build** | `npm run build` → `dist/` |
| **Path Alias** | `@/` → `src/` |
| **Strict TS** | `false` |

## Repository Structure

```
AAA/
├── src/
│   ├── main.tsx          # React entry point (+ webmcp init)
│   ├── App.tsx           # Root component (hash router)
│   ├── Cockpit.tsx       # Main dashboard
│   ├── ai/               # AI chat panel + client
│   ├── gateway/          # A2A v1.0.0 TypeScript server
│   ├── components/ui/    # shadcn/ui primitives (50+)
│   ├── adapter/          # GovernanceAdapter → A-FORGE /sense
│   ├── seed/             # Control-plane seed data
│   ├── lib/              # Utilities (cn() helper)
│   └── hooks/            # React hooks
├── public/               # Static assets, .well-known/, a2a/
├── contracts/            # YAML governance contracts
├── schemas/              # JSON/YAML schemas
├── skills/               # Agent skills library
├── agents/               # Per-agent identity directories
├── a2a-server/           # Standalone Express A2A gateway (Docker)
├── observability/        # Prometheus + Grafana config
└── components.json       # shadcn/ui config
```

## Authority & Autonomy

### Autonomous
- Modify React components, add UI features, refactor TypeScript
- Run `npm run build`, `npm run lint`
- Update contracts/schemas
- Work in `a2a-server/` standalone gateway

### Requires 888_HOLD
- Production deployment without verified build pass
- Changes to A2A auth schema or agent card format
- Cross-repo API contract changes

## Build & Test

```bash
cd /root/AAA

# Install
npm install

# Dev server
npm run dev      # Vite dev server

# Build
npm run build

# Lint
npm run lint

# Validate AAA contracts
npm run validate:aaa
npm run export:aaa

# A2A standalone production server
cd a2a-server && npm install && node server.js
```

## Federation Position

```
arifOS (Ω Law) → AAA (Control Plane + A2A Mesh) → A-FORGE / GEOX / WEALTH / WELL
                     ↑
                Human operator (Arif)
```

AAA is the **interface layer**, not the law layer. It routes intent to A-FORGE, displays federation health, and hosts the A2A mesh gateway. Constitutional judgment remains in arifOS.

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
