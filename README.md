<!-- SOT-MANIFEST
federation_release: v2026.09.13
last_verified: 2026-09-14T08:30:00Z
live_commit: 8a2c373dc
a2a_port: 3001
a2a_status: loopback JSON-RPC healthy; public POST /a2a exact path 405 (Caddy /a2a/* HOLD)
protocol: A2A v1.0 (wire Major.Minor; GitHub tag v1.0.1 is spec patch — never stamp 1.2)
canonical_surface: a2a/CANONICAL_SURFACE.md
apex_zen: A2A delegates ⊥ MCP equips ⊥ ACT mutates ⊥ arifOS governs ⊥ F13 decides
godel_lock: ACTIVE federation-wide
role: ATTENTION PLANE — Federation State, A2A Gateway, Skill Catalog, Intent Routing, Verification
authority: DISPLAY_ONLY — never judges (arifOS), never metabolizes (arifFlow), never executes (A-FORGE)
agent_lanes: 3 (333-AGI, 555-ASI, 888-APEX; FORGE is adat agentic substrate)
truth_rule: /health + live Agent Card + POST /a2a/ beat any static count in prose
vault: CONNECTED
seal_chain: append-only (chattr +a) + Merkle anchor every 100 receipts
holds: Caddy exact /a2a · JWS card keys · medical purge (Pilihan A) · WELL biometrics
-->

# AAA — Attention Plane & Federation Registry

## The attention plane of the arifOS federation — compressing reality into sovereign attention.

AAA converts federated reality into actionable sovereign attention through observation, verification, registration, and routing. It does not judge (arifOS), execute (A-FORGE), or witness (arifFlow). It makes reality visible, trustworthy, and actionable.

In a world where intelligence is abundant, attention is the scarce resource. AAA exists to ensure the right reality reaches the right authority at the right time.

**Licensed under AGPL-3.0.**

| Audience | What you get |
|---|---|
| **Human** | One switchboard. Intent in, the right organ out. No terminal dump in your pocket |
| **Agent / A2A** | Public card `/.well-known/agent-card.json`. JSON-RPC at `/a2a/` with `A2A-Version: 1.0`. Extended card is authenticated, not a topology dump |
| **Institution** | DISPLAY_ONLY edge: routes and shows state. Judgment is [arifOS](https://github.com/ariffazil/arifOS). Hands are [A-FORGE](https://github.com/ariffazil/A-FORGE) |

Canonical live surface: [`a2a/CANONICAL_SURFACE.md`](./a2a/CANONICAL_SURFACE.md)

---

## The Problem

As federations grow, intelligence becomes abundant but human attention becomes scarce. The challenge is no longer generating answers — it is determining what matters, what requires attention now, and what can safely wait. Without an attention layer, operators drown in logs, dashboards, metrics, and agent chatter.

AAA solves this by providing:

- **Attention compression** — converts complex federated reality into actionable sovereign attention
- **Federation state** — canonical `federation_state()` object with organ health, FQ, holds, bottlenecks
- **Verification** — cross-checks observed state against live federation reality
- **Intent routing** — deterministic classification that maps intent to the correct organ
- **Skill catalog** — 200+ skills discoverable and composable across organs

---

## Architecture

```
                    ┌─────────────────┐
                    │    Sovereign    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  AAA Attention  │
                    │     Plane       │
                    │   Port :3001    │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐      ┌─────────────┐     ┌─────────────┐
    │ Observe │      │   Verify    │     │    Route    │
    │ (State) │      │ (aaastate   │     │ (Intent     │
    │         │      │  verify)    │     │  Classify)  │
    └────┬────┘      └──────┬──────┘     └──────┬──────┘
         │                  │                    │
         └──────────────────┼────────────────────┘
                            ▼
                   ┌─────────────────┐
                   │ Federation State │
                   │  (canonical)    │
                   └────────┬────────┘
                            │
    ┌──────────┬────────────┼────────────┬──────────┐
    │          │            │            │          │
    ▼          ▼            ▼            ▼          ▼
 arifOS     A-FORGE     arifFlow     WEALTH    GEOX/WELL
 Authority  Execution   Witness     Capital   Domain
  Plane      Plane       Plane      Plane      Organs
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
curl http://localhost:4000/health/liveliness
```

### Local Development

```bash
cd AAA
npm install
npm run dev

# Or with Docker Compose for full stack (AAA + FED)
docker compose up -d
```

---

## Key Components

### A2A Mesh Gateway
Agent-to-agent communication broker using the Agent-to-Agent (A2A) protocol v1.0.0. Handles message routing, session management, and inter-organ communication.

### FED Gateway (Multi-Model Inference)
Federation model gateway with fallback chains across providers (FLAME Router retired 2026-09-04):
- **FED** `:4000` — HAProxy intake into the federation model lanes (LiteLLM)
- **Fallback chains** — retry with backoff; position 3+ on a different provider/route
- **Local fallback** — Ollama, zero-cost

When a model fails, FED routes to the next provider — no interruption.

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

### Federation State & Attention Plane
Canonical `federation_state()` object — the keystone. Every surface projects from the same state:

- **Organ health** — 8 organs, latency, failure reasons
- **Flow Quotient (FQ)** — per-actor metabolism, diagnosis, stuck actors
- **Authority debt** — holds, seals, oldest hold, held actors
- **Bottleneck detection** — infrastructure, authority, metabolism, or none
- **Verification** — `aaa_state_verify.py` cross-checks state against live sources

Surfaces: [Web Cockpit](https://aaa.arif-fazil.com) · [Static API](https://aaa.arif-fazil.com/state.json) · Terminal (`python3 federation_state.py crf`) · Verification (`python3 aaa_state_verify.py`)

---

## Federation Role

AAA sits between reality and the sovereign:

```
Reality → AAA (observe + verify + compress) → Sovereign Attention
```

### Division of Constitutional Labor

| Organ | Constitutional Role | Scarcity | Does NOT |
|-------|---------------------|----------|----------|
| **arifOS** | **Authority Plane** — constitutional judgment | Authority | Never executes, never witnesses |
| **AAA** | **Attention Plane** — reality compression + routing | Attention | Never judges, never executes, never mutates |
| **arifFlow** | **Witness Plane** — metabolic recording | Reality | Never judges, never executes |
| **A-FORGE** | **Execution Plane** — bounded mutation | Execution | Never adjudicates, never witnesses |
| **GEOX** | **Earth Intelligence** | Domain | Never judges, never routes |
| **WEALTH** | **Capital Intelligence** | Capital | Never judges, never executes |
| **WELL** | **Human Readiness** | Substrate | Never judges, never executes |

AAA **observes, verifies, compresses, and routes — but never judges, executes, or mutates.** Verdicts belong to arifOS. Mutations belong to A-FORGE. Reality recording belongs to arifFlow.

### What AAA Is Not

AAA is not an orchestrator. AAA is not a workflow engine. AAA is not a judge. AAA is not an executor. AAA is not an agent manager.

AAA does not decide truth. AAA does not mutate reality. AAA only ensures that reality reaches attention.

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
| `GET /health/liveliness` | FED gateway liveliness (no auth) | None |
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
