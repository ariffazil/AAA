<!-- SOT-MANIFEST
federation_release: v2026.09.13
last_verified: 2026-09-13T06:32:00Z
live_commit: 8a2c373dc
a2a_port: 3001
a2a_status: loopback JSON-RPC healthy; public POST /a2a exact path 405 (Caddy /a2a/* HOLD)
protocol: A2A v1.0 (wire Major.Minor; GitHub tag v1.0.1 is spec patch — never stamp 1.2)
canonical_surface: a2a/CANONICAL_SURFACE.md
apex_zen: A2A delegates ⊥ MCP equips ⊥ ACT mutates ⊥ arifOS governs ⊥ F13 decides
godel_lock: ACTIVE federation-wide
role: REGISTER & DISPLAY — A2A Gateway, State Plane, Skill Catalog, Intent Routing
authority: DISPLAY_ONLY — never judges (arifOS), never metabolizes (arifFlow), never executes (A-FORGE)
agent_lanes: 3 (333-AGI, 555-ASI, 888-APEX; FORGE is adat agentic substrate)
truth_rule: /health + live Agent Card + POST /a2a/ beat any static count in prose
vault: CONNECTED
seal_chain: append-only (chattr +a) + Merkle anchor every 100 receipts
holds: Caddy exact /a2a · JWS card keys · medical purge (Pilihan A) · WELL biometrics
-->

# AAA — Intelligence Routing & State Plane

## The sovereign intelligence layer for the arifOS federation — routing intent to the right organ, every time.

AAA is the cognitive nervous system and registry of the arifOS federation. It classifies human and agent intent, routes tasks to the correct organ (kernel, execution, earth science, capital, health), manages the federation state plane, and provides the A2A gateway mesh.

**Licensed under AGPL-3.0.**

| Audience | What you get |
|---|---|
| **Human** | One switchboard. Intent in, the right organ out. No terminal dump in your pocket |
| **Agent / A2A** | Public card `/.well-known/agent-card.json`. JSON-RPC at `/a2a/` with `A2A-Version: 1.0`. Extended card is authenticated, not a topology dump |
| **Institution** | DISPLAY_ONLY edge: routes and shows state. Judgment is [arifOS](https://github.com/ariffazil/arifOS). Hands are [A-FORGE](https://github.com/ariffazil/A-FORGE) |

Canonical live surface: [`a2a/CANONICAL_SURFACE.md`](./a2a/CANONICAL_SURFACE.md)

---

## The Problem

Multi-agent AI systems fail at orchestration. Without a central routing layer, agents call the wrong tools, models degrade silently, and state becomes inconsistent across organs. AAA solves this by providing:

- **Deterministic intent classification** — maps user language to organ capability
- **Multi-model routing (FLAME)** — automatic fallback across providers when models fail
- **State plane management** — single source of truth for federation health
- **Skill catalog** — 200+ skills discoverable and composable across organs

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    AAA Intelligence Layer                     │
│  Port :3001  ·  A2A Gateway  ·  State Plane                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐ │
│  │   Intent     │  │   State      │  │   Skill Catalog    │ │
│  │ Classifier   │  │   Plane      │  │   (200+ skills)    │ │
│  └──────┬───────┘  └──────┬───────┘  └─────────┬──────────┘ │
│         │                 │                     │           │
│  ┌──────▼─────────────────▼─────────────────────▼──────────┐│
│  │              A2A Mesh Gateway                            ││
│  │  Agent-to-agent message broker · Express 5.x            ││
│  └──────────────────────────┬──────────────────────────────┘│
│                             │                               │
│  ┌──────────────┐  ┌───────▼───────┐  ┌──────────────────┐ │
│  │  Agent       │  │ Amanah Board  │  │ Operator Cockpit │ │
│  │  Registry    │  │ (Work Queue)  │  │ (Health/HOLDs)   │ │
│  └──────────────┘  └───────────────┘  └──────────────────┘ │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ FLAME Router │
                    │  :18901      │
                    └──────────────┘
```

---

## Quick Start

### Docker

```bash
git clone https://github.com/arif-fazil/AAA.git
cd AAA
docker compose up -d

# Verify
curl http://localhost:3001/health
curl http://localhost:18901/health/liveliness
```

### Local Development

```bash
cd AAA
npm install
npm run dev

# Or with Docker Compose for full stack (AAA + FLAME)
docker compose up -d
```

---

## Key Components

### A2A Mesh Gateway
Agent-to-agent communication broker using the Agent-to-Agent (A2A) protocol v1.0.0. Handles message routing, session management, and inter-organ communication.

### FLAME Router (Multi-Model Inference)
Automatic model routing with fallback chains across providers:
- **MuleRouter** (80%) — primary, multi-model with fixed pricing
- **OpenRouter** (15%) — secondary, broad model availability
- **Ollama** (5%) — local fallback, zero-cost

When a model fails, FLAME automatically routes to the next provider — no interruption.

### Intent Classification
Deterministic mission routing that maps human language to machine states:
- Six stable mission states (no seventh — ambiguous → HOLD)
- Works even when the ML classifier is down
- Phase 2: optional model-assisted intent parsing

### Skill Catalog
200+ skills across 11 categories:
- **333-AGI** — General intelligence, web, research, epistemic discovery
- **555-ASI** — Causal reasoning, structural intelligence, vision analysis
- **888-APEX** — Sovereign adjudicative, constitutional audit
- **FORGE (adat)** — Code, infrastructure, deployment (inherited capability substrate)
- **warga** — Citizen agent skills
- And more (productivity, media, smart home, social)

### State Plane
Real-time federation state monitoring:
- Organ health across all 7 organs
- HOLD queue management
- Seal chain verification (append-only with Merkle anchors)
- Deployment drift detection

---

## Federation Role

AAA sits between the user and all other organs:

```
User → AAA (intent classification + routing) → Target Organ
```

### Division of Constitutional Labor

| Organ | Constitutional Role | Authority Ceiling | Does NOT |
|-------|---------------------|-------------------|----------|
| **arifOS** | **JUDGE** | F1–F13 Constitutional Kernel | Never executes (mutates nothing) |
| **AAA** | **REGISTER & DISPLAY** | A2A Mesh, State Plane, Skill Catalog | Never judges, never metabolizes, never executes |
| **arifFlow** | **METABOLIZE** | Attention Pulse, Flow Quotient (FQ) | Never judges, never executes |
| **A-FORGE** | **EXECUTE** | Actuator, MCP Tools, System Mutations | Never adjudicates |

AAA **registers identities and displays state, but never judges, metabolizes, or executes**. Verdicts belong solely to arifOS. Metabolisms belong to arifFlow. Mutations belong to A-FORGE.

---

## Federation Repository Taxonomy (5-Tier)

The arifOS Federation organizes its 35 repositories into five distinct operational tiers:

- **Tier 1 — Core Runtime:** `arifOS`, `A-FORGE`, `arifFlow`, `AAA`, `GEOX`, `WEALTH`, `WELL`. The living spine of the federation.
- **Tier 2 — Governance Infrastructure:** `scripts`, `FRAME`, `web-canon`, `arifOS-model-registry`. Rulebooks, tools, schemas, and operational scripts.
- **Tier 3 — Federation Interfaces:** `arif-fazil.com`, `ariffazil`, `HERMES`. Human and sovereign public boundaries.
- **Tier 4 — Infrastructure Attachments:** `compose`, `searxng`, `syedos`, `A2B`, `awesome-mcp-servers`, `macrostrat`. Auxiliary configurations and benchmarks without runtime authority.
- **Tier 5 — Archives:** 15 retired historical repositories under zero execution rights (`[L4 ARCHIVE]`).

---

## Health Checks

| Endpoint | Description | Auth |
|----------|-------------|------|
| `GET /health` | AAA organ liveness | None |
| `GET /health/skills` | Skill catalog status | None |
| `GET /health/liveliness` | FLAME router (no auth) | None |
| `GET /health/agents` | Agent registry | None |

---

## Documentation

- [Full Technical README](docs/README-FULL.md)
- [Federation Architecture](docs/FEDERATION.md)
- [A2A Protocol Spec](docs/A2A_ORGAN_REGISTRY.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Changelog](CHANGELOG.md)
- [Security Policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

---

## License

**GNU Affero General Public License v3.0 (AGPL-3.0)**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU AGPL v3.0. See [LICENSE](LICENSE) for the full text.

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.

Built by Muhammad Arif bin Fazil.
