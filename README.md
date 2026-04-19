# AAA — Canonical Repo Identity

> **DITEMPA BUKAN DIBERI** — *Intelligence is forged, not given.*

> **⚠️ LEGACY IDENTITY NOTICE**
> 
> This repository previously operated under the **WAW** legacy name, but its canonical identity is now **AAA**, the agent workspace and control plane.
> 
> - **AAA charter:** [`AAA_CHARTER.md`](./AAA_CHARTER.md)
> - **OpenClaw seed extraction:** [`AAA_OPENCLAW_SEED.md`](./AAA_OPENCLAW_SEED.md)
> - **Canonical source of truth for governance:** [`ariffazil/arifOS`](https://github.com/ariffazil/arifOS)
> - **Execution shell:** [`ariffazil/af-forge`](https://github.com/ariffazil/af-forge)

```
WEBSITE_VERSION: 55.2.0
ARIFOS_VERSION: 2026.04.07
STATUS: OPERATIONAL
AUTHORITY: 888_JUDGE
```

---

## What is this repo now?

Historically, `waw` was treated as the frontend presentation layer for arifOS.

That is now legacy framing only.

This repo is now **AAA**:

- the future **agent workspace**
- the future **control plane**
- the home of agent identity, contracts, skills, workflows, host adapters, and governance surfaces

Public website concerns are expected to migrate toward **`arif-sites`** over time.

**Live Site:** https://arif-fazil.com  
**MCP Runtime:** https://arifosmcp.arif-fazil.com

## Repository Structure

| Directory | Purpose |
|-----------|---------|
| `src/` | Legacy React/Vite surface still present during migration |
| `memory/` | Long-term curated memory |
| `.well-known/` | Discovery endpoints |
| `openclaw/` | OpenClaw authority plane: gateway, ACP, MCP, plugins, A2A, exports |
| `schemas/` | Contract schemas for AAA and OpenClaw runtime artifacts |
| `AGENTS.md` | Agent behavior rules for this codebase |
| `ROOT_CANON.yaml` | Root file precedence and status manifest |
| `AAA_CHARTER.md` | Canonical future direction and ownership boundaries |
| `AAA_OPENCLAW_SEED.md` | Extracted OpenClaw seed for AAA bootstrap |

## Ecosystem Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│  CANONICAL SOURCE OF TRUTH                                   │
│  ├── ariffazil/arifOS (kernel, doctrine, Floors F1-F13)     │
│  └── Runtime: /health + /tools on deployed server           │
├─────────────────────────────────────────────────────────────┤
│  RUNTIME SHELLS                                              │
│  ├── ariffazil/af-forge (TypeScript agent workbench)        │
│  └── arifosmcp/ (MCP server, HTTP transport)                │
├─────────────────────────────────────────────────────────────┤
│  CONTROL-PLANE SEED (THIS REPO)                              │
│  ├── ariffazil/waw (legacy alias) → AAA                     │
│  │   (canonical agent workspace + control plane)            │
│  └── legacy website/frontend content pending migration       │
├─────────────────────────────────────────────────────────────┤
│  PUBLIC SURFACES                                             │
│  └── ariffazil/arif-sites (sites, rendering, docs portals)  │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

- **Build Tool:** Vite
- **Framework:** React
- **Styling:** Tailwind CSS + Radix UI primitives
- **Deployment:** Cloudflare Pages / VPS

## Quick Start

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 111 Federation Status

- **Discovery:** live as publishable static assets under `/a2a/` and `/.well-known/`
- **Message ingress:** **888_HOLD** in this repo until a server runtime exposes `/a2a/message`

## 222 / 333 Institutional Model

- **222:** canonical Goal -> Task -> Verdict chain lives under `contracts/goals/`
- **333:** canonical OrgUnit + topology graph lives under `contracts/org/`

## 666 / 777 / 888 / 999 Governance Trail

- **666 / 777:** governance gates and budget policies live under `contracts/governance/`
- **888 / 999:** decision objects and vault export mapping live under `contracts/decisions/` and `vault/decisions/`

## Constitutional Alignment

This codebase follows the same 13 Floors (F1-F13) as arifOS:

- **F1 Amanah** — Reversible changes (git history)
- **F2 Truth** — Accurate documentation
- **F9 Anti-Hantu** — No dark patterns in UI
- **F13 Sovereign** — Human (Arif) holds final design authority

## Links

| Resource | URL |
|----------|-----|
| arifOS (SoT) | https://github.com/ariffazil/arifOS |
| AF-FORGE | https://github.com/ariffazil/af-forge |
| Runtime Health | https://arifosmcp.arif-fazil.com/health |
| Canonical Index | https://arifosmcp.arif-fazil.com/.well-known/arifos-index.json |

---

**License:** AGPL-3.0-only  
**Authority:** 888_JUDGE — Muhammad Arif bin Fazil  
**Website:** https://arif-fazil.com
