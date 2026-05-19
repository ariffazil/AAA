<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-05-19
valid_from: 2026-05-19
valid_until: 2026-06-19
confidence: high
scope: /root/AAA
epistemic_status: CLAIM
-->

# AAA — Agent Interface & Session Cockpit

> **Status:** OPERATIONAL | **Organ:** BODY (Ω) | **Authority:** arifOS
> **Domain:** `aaa.arif-fazil.com`

## 🏛️ What this repo is

The primary interface surface for agentic sessions within the arifOS federation. It manages context, session identity, and the human-in-the-loop veto layer via a React 19 cockpit UI and an A2A gateway enabling agent-to-agent communication.

**AAA owns the BODY — the observable surface through which agents interact with the federation.**

## 📦 Ownership

- **Owns**: React cockpit UI, A2A gateway service (`services/a2a-gateway/`), session state management, agent SDK components.
- **Does NOT own**: Execution orchestration (A-FORGE), Constitutional judgment (arifOS).

## 🏗️ Current Structure

```
AAA/
├── src/                        # React 19 + TypeScript source
│   ├── App.tsx                 # Root component
│   ├── Cockpit.tsx            # Main dashboard
│   ├── gateway/               # A2A v1.0.0 server and agent card endpoints
│   ├── adapter/               # Router adapters
│   ├── components/ui/         # Radix + Tailwind UI primitives (shadcn/ui)
│   ├── hooks/                 # React hooks
│   ├── lib/                   # Utilities
│   └── seed/                  # Control-plane seed data (SOUL.md, IDENTITY.md)
├── services/
│   └── a2a-gateway/          # Standalone Express A2A gateway (port 3001)
│       ├── Dockerfile
│       ├── docker-compose.a2a.yml
│       ├── server.js
│       └── package.json
├── specs/contracts/            # Governance contracts (renamed from contracts/)
│   ├── federation/
│   ├── decisions/
│   └── workflows/
├── docs/
│   ├── AGENT_LAYOUT_CONTRACT.md
│   └── RELEASE_NOTES_2026.05.16.md
└── a2a-server/               # Standalone A2A gateway (legacy)
```

## 🚀 Verified Commands

```bash
# Install
npm install

# Development
npm run dev                  # Vite dev server

# Production build
npm run build               # Outputs to dist/

# Lint
npm run lint

# A2A gateway
npm run a2a:server         # Start A2A gateway on port 3001

# Validate AAA contracts
npm run validate:aaa
npm run export:aaa
```

## 🔗 Federation Loop

- [arifOS](https://github.com/ariffazil/arifOS) — Kernel (constitutional judgment, VAULT999)
- [A-FORGE](https://github.com/ariffazil/A-FORGE) — Forge (deployment, infrastructure)

---

*Last Verified: 2026.05.16 | 999 SEAL ALIVE*
