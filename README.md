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
