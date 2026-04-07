# WAW — arifOS Website & Documentation Portal

> **DITEMPA BUKAN DIBERI** — *Intelligence is forged, not given.*

> **⚠️ THIS IS THE WEBSITE / PRESENTATION LAYER**
> 
> **Canonical Source of Truth for arifOS:** [`ariffazil/arifOS`](https://github.com/ariffazil/arifOS)
> 
> **TypeScript Runtime Shell:** [`ariffazil/af-forge`](https://github.com/ariffazil/af-forge)

```
WEBSITE_VERSION: 55.2.0
ARIFOS_VERSION: 2026.04.07
STATUS: OPERATIONAL
AUTHORITY: 888_JUDGE
```

---

## What is WAW?

WAW (World Agent Web) is the **frontend presentation layer** for arifOS — the website, documentation portal, and user interface that civilization interacts with.

**Live Site:** https://arif-fazil.com  
**MCP Runtime:** https://arifosmcp.arif-fazil.com

## Repository Structure

| Directory | Purpose |
|-----------|---------|
| `src/` | React/Vite source code |
| `memory/` | Long-term curated memory |
| `.well-known/` | Discovery endpoints |
| `AGENTS.md` | Agent behavior rules for this codebase |

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
│  PRESENTATION (THIS REPO)                                    │
│  └── ariffazil/waw — Website, docs portal, UI               │
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
