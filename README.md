# AAA — Federation Control Plane & Operator Cockpit

```
    █████╗  █████╗  █████╗
   ██╔══██╗██╔══██╗██╔══██╗
   ███████║███████║███████║
   ██╔══██║██╔══██║██╔══██║
   ██║  ██║██║  ██║██║  ██║
   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

   Alignment · Authority · Accountability
   ─────────────────────────────────────
   The Control Tower of the arifOS Federation
```

> **AAA is the control plane for the arifOS Federation — the cockpit where the human operator sees every agent, every verdict, and every sealed decision. It routes tasks, manages the A2A mesh, queues approvals, and displays governed state. It is the parliament and the air traffic control tower — never the judge, never the executor, never the constitution.**

[![A2A Protocol](https://img.shields.io/badge/A2A-v0.3.0-8b5cf6)](a2a-server/)
[![Node](https://img.shields.io/badge/node-22-339933?logo=node.js)](package.json)
[![React](https://img.shields.io/badge/react-19-61DAFB?logo=react)](package.json)
[![TypeScript](https://img.shields.io/badge/ts-6.0-3178c6?logo=typescript)](package.json)
[![Vite](https://img.shields.io/badge/vite-8-646CFF?logo=vite)](package.json)
[![Tailwind](https://img.shields.io/badge/tailwind-4-06b6d4?logo=tailwindcss)](package.json)
[![Port](https://img.shields.io/badge/port-3001-64748b)](FEDERATION_COCKPIT.md)
[![License](https://img.shields.io/badge/license-AGPL--3.0-ef4444?logo=gnu)](LICENSE)
[![Systemd](https://img.shields.io/badge/systemd-aaa--a2a.service-30b53f)](deploy/)

**Repository:** https://github.com/ariffazil/AAA
**Canonical identity doc:** `FEDERATION_COCKPIT.md`
**Service:** `aaa-a2a.service` (systemd)
**Genesis:** `GENESIS/013_AAA_MANDATE.md`

```
DITEMPA BUKAN DIBERI — Control is forged, not given.
```

---

## 1. Federation Position

```
                              ┌──────────────────────┐
                              │    HUMAN SOVEREIGN    │
                              │   Arif bin Fazil      │
                              │   (F13 — final veto)  │
                              └──────────┬───────────┘
                                         │ reads cockpit
                                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                          ┌─────────────────┐                            │
│                          │   AAA COCKPIT   │  ← YOU ARE HERE            │
│                          │  Control Plane  │                            │
│                          │    Port 3001    │                            │
│                          └───────┬─────────┘                            │
│                                  │                                      │
│         ┌────────────────────────┼────────────────────────┐             │
│         │                        │                        │             │
│         ▼                        ▼                        ▼             │
│   ┌──────────┐            ┌──────────┐            ┌──────────┐          │
│   │  arifOS   │            │ A-FORGE  │            │  DOMAIN   │          │
│   │  JUDGES   │            │ EXECUTES │            │  ORGANS   │          │
│   │ F1-F13   │            │ builds,  │            │ GEOX     │          │
│   │ 888-APEX │            │ deploys, │            │ WEALTH   │          │
│   │ VAULT999 │            │ forges   │            │ WELL     │          │
│   │ Port 8088│            │ Port 7071│            │8081/18082│          │
│   └──────────┘            └──────────┘            └──────────┘          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**The one-sentence identity:**

> **AAA is the cockpit. arifOS is the judge. A-FORGE is the executor. The domain organs provide evidence. Arif holds the veto.**

### What AAA Is

| It IS | Explanation |
|-------|-------------|
| **The control tower** | Sees all agents, their status, their routes, their verdicts |
| **The operator cockpit** | The dashboard Arif reads to understand the federation |
| **The A2A mesh hub** | Routes agent-to-agent tasks across the federation |
| **The approval queue** | Queues HOLDs for human review, displays SEAL/VOID verdicts |
| **The agent registry** | Canonical registry of every agent, its card, its capabilities |
| **The truth dashboard** | Displays the four-layer truth stack from GROUND_TRUTH to INFERRED |
| **The parliament** | Where agents register, declare capabilities, and receive routing |

### What AAA Is NOT

| It IS NOT | Because |
|-----------|---------|
| **The judge** | Constitutional verdicts (F1-F13, SEAL, HOLD, VOID) belong to `arifOS` |
| **The executor** | Builds, deploys, and forges belong to `A-FORGE` |
| **The constitution** | F1-F13 floors live in `arifOS` |
| **A domain calculator** | GEOX computes earth. WEALTH computes capital. WELL reflects readiness. |
| **A secret store** | Secrets live in `/root/.secrets/` — never in AAA |
| **The sealed ledger** | VAULT999 is owned by arifOS; AAA displays it, never writes it |
| **A general dumping ground** | Session logs, backups, runtime artifacts belong elsewhere |

> **AAA is the manager who knows which worker should use which tool — not the worker and not the toolbox.**

---

## 2. Quick Start

```bash
cd /root/AAA

# Install
npm install                        # install all deps (React 19, Vite 8, Tailwind 4)

# Dev server
npm run dev                        # Vite dev server — hot reload

# Build
npm run build                      # vite build → dist/

# Lint
npm run lint                       # ESLint 10 + typescript-eslint 8

# A2A standalone gateway
cd a2a-server && npm install && node server.js   # port 3001

# Validate AAA contracts and registries
npm run validate:aaa               # registry consistency + card validity

# Health check
curl -s http://localhost:3001/health | python3 -m json.tool
# → {"status":"healthy","protocol":"A2A","version":"0.3.0","agents":5}

# A2A conformance test
npm run a2a:conformance
```

---

## 3. The AREP Protocol — Intent Without Prompts

**AREP — Arif Reality Engineering Protocol.** Prompt engineering is dead. AREP replaces it with a four-layer truth stack, reality gating, and constitutional verdict routing.

```
  HUMAN DECLARES INTENT
         │
         ▼
  ┌─────────────────────────────────────────────────┐
  │  1. DECLARE                                      │
  │  "forge all organ with geox recalibration"       │
  │  POST /api/arep/submit                           │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────┐
  │  2. VALIDATE (schema check)                      │
  │  • Is the declaration well-formed?               │
  │  • Does it map to known organs/tasks?            │
  │  • Is the intent classifiable?                   │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────┐
  │  3. REALITY GATE (6-organ health probe)          │
  │  • arifOS    :8088  ─── healthy?                 │
  │  • GEOX      :8081  ─── healthy?                 │
  │  • WEALTH    :18082 ─── healthy?                 │
  │  • WELL      :18083 ─── healthy?                 │
  │  • A-FORGE   :7071  ─── healthy?                 │
  │  • AAA       :3001  ─── healthy?                 │
  └──────────────────────┬──────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
    ┌─────────────────┐   ┌─────────────────┐
    │  ALL GATES PASS │   │  GATE FAILS     │
    │       ↓         │   │       ↓         │
    │    EXECUTE      │   │    HALT / HOLD  │
    │  route → organ  │   │  queue in AAA   │
    │  execute → seal │   │  await human    │
    └─────────────────┘   └─────────────────┘
              │                     │
              ▼                     ▼
    ┌─────────────────┐   ┌─────────────────┐
    │  VAULT999 SEAL  │   │  VERDICT QUEUE  │
    │  immutable      │   │  visible in AAA │
    │  audit trail    │   │  cockpit        │
    └─────────────────┘   └─────────────────┘
```

The prompt was never visible. **The reality was.**

---

## 4. The Four-Layer Truth Stack

Every claim in the AAA cockpit is tagged with its truth layer. An agent cannot claim a higher layer than its evidence supports.

| Layer | Anchor | Verification | Example |
|-------|--------|-------------|---------|
| **L1 — GROUND_TRUTH** | VAULT999 sealed events | Merkle chain integrity, hash verification | A SEAL verdict written to the immutable ledger |
| **L2 — VERIFIED_STATE** | Live health probe, model registry | `curl /health` + passport check | "arifOS port 8088 is responding with 200" |
| **L3 — CACHED_STATE** | L3 Qdrant, session memory | Freshness timestamp, TTL | "Last known WEALTH tool count: 44 (cached 3m ago)" |
| **L4 — INFERRED** | Agent reasoning | Bounded by constitutional floors, omega_0 | "Based on 3 organs being green, the system appears stable" |

```
     TRUTH STACK (top = strongest evidence)
    ┌──────────────────────────────────────┐
    │  L1  GROUND_TRUTH       VAULT999     │  ← immutable, hash-chained
    │  L2  VERIFIED_STATE     Live probes  │  ← observable right now
    │  L3  CACHED_STATE       Qdrant       │  ← recent, but could be stale
    │  L4  INFERRED           Reasoning    │  ← model's best guess
    └──────────────────────────────────────┘
```

> **Iron rule: You cannot infer your way to ground truth.** A claim tagged L4 INFERRED must never be presented as L1 GROUND_TRUTH. The cockpit enforces this visually.

---

## 5. HEXAGON Agent Architecture

The 5-agent constitutional architecture (HEXAGON, ratified 2026-06-02) sits above the 7-organ runtime topology. Three primary agents form a decision triangle; two support agents observe and record in parallel.

```
                         ┌──────────────┐
                         │  000-SALAM   │
                         │  (Arif)      │  ← Human sovereign — NOT an agent
                         │  F13 VETO    │
                         └──────┬───────┘
                                │ reads cockpit, issues veto
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
  ┌──────────┐           ┌──────────┐           ┌──────────┐
  │ 333-AGI  │◄─────────►│ 555-ASI  │◄─────────►│888-APEX  │
  │ Δ MIND   │  propose  │ Ω HEART  │  critique │ ΦΙ JUDGE │
  │ REASON   │  critique │ MEMORY   │  flag     │ VERDICT  │
  │ EXECUTE  │           │ SYNTHESIS│           │ F1-F13   │
  └────┬─────┘           └────┬─────┘           └────┬─────┘
       │                      │                      │
       │         ┌────────────┴────────────┐         │
       │         ▼                         ▼         │
       │  ┌──────────┐              ┌──────────┐     │
       │  │ A-AUDIT  │              │A-ARCHIVE │     │
       │  │ WATCH    │              │ SEAL     │     │
       │  │ COMPLIAN │              │ VAULT999 │     │
       │  └──────────┘              └──────────┘     │
       │    (observes all 3)         (writes on SEAL) │
       │                                              │
       └──────────────┬───────────────────────────────┘
                      ▼
              ┌──────────────┐
              │  7 FEDERATION │
              │    ORGANS     │
              └──────────────┘
```

### Agent Roster

| ID | Class | Ring | Role | Skills | Host Organs | Stage |
|----|-------|------|------|--------|-------------|-------|
| **333-AGI** | AGI | Δ MIND | Reason + execute | 10 | arifOS, GEOX, WEALTH | 333-THINK |
| **555-ASI** | ASI | Ω HEART | Critique + memory | 3 | arifOS, WELL | 555-MEMORY |
| **888-APEX** | APEX | ΦΙ JUDGE | Constitutional judge | 2 | arifOS | 888-JUDGE |
| **A-AUDIT** | APEX oversight | — | Continuous watcher | 2 | arifOS | cross-cutting |
| **A-ARCHIVE** | ASI service | — | Ledger keeper | 3 | VAULT999 | 999-SEAL |

### Agent Workflow (The Decision Pipeline)

```
000-SALAM (human intent)
    │
    ▼
333-AGI (reason + draft plan)
    │
    ├──► 555-ASI (ethical critique + memory synthesis)
    │         │
    │         ▼
    ├──► 888-APEX (constitutional verdict: SEAL / HOLD / VOID)
    │         │
    │         ├──► A-AUDIT (compliance verification)
    │         │         │
    │         │         ▼
    │         └──► A-ARCHIVE (VAULT999 seal — append only)
    │
    └──► reseed to 000-SALAM (human reviews cockpit)
```

**The 10-3-2 ratio encodes the truth:** thinking is cheap (10 skills), memory is hard (3 skills), judgment is rare (2 skills).

---

## 6. Agent Lifecycle

Every agent in the AAA registry follows a four-stage lifecycle. The cockpit tracks and displays each agent's current stage.

```
     BIRTH ──────► APPRENTICE ──────► WARGA ──────► ELDER
     (registered)   (learning)        (citizen)     (trusted)
         │               │                │              │
         │    limited    │   expanded    │   full       │   mentor
         │    tools      │   tools       │   autonomy   │   role
         │    read-only  │   propose     │   execute    │   govern
         │               │               │              │
         └── malu_score monitored ──► malu accumulates ──┘
              (Adat Agentik tracks trustworthiness across lifecycle)
```

| Stage | Ring | Access | Promotion Gate |
|-------|------|--------|----------------|
| **BIRTH** | 0 | Read-only federation probes | Registration + agent card validation |
| **APPRENTICE** | 1 | Propose actions, limited tools | 7-day burn-in + malu_score < 0.15 |
| **WARGA** | 2 | Full domain tools, execute | F13 sovereign signature + darjat review |
| **ELDER** | 3 | Mentor, govern, veto recommend | F13 sovereign signature + scar audit |

---

## 7. Full Capability Map

### 7.1 Cockpit Dashboard (`src/`)

| Component | Purpose |
|-----------|---------|
| `Cockpit.tsx` | Main dashboard — live floor grid, mission intake, organ health |
| `RealityConsole.tsx` | AREP 3-pane cockpit — Intent Board, Reality Feed, Verdict Queue |
| `AutonomyBands.tsx` | GREEN/YELLOW/ORANGE/RED/BLACK band visualization |
| `FloorGrid.tsx` | F1-F13 constitutional floor status grid |
| `AgentRegistry.tsx` | HEXAGON + CODING agent listing with cards |
| `VaultFeed.tsx` | Recent VAULT999 seals stream |
| `AI panel (`ai/`)` | Chat interface to arifOS / Ollama / OpenRouter |

### 7.2 A2A Gateway (`a2a-server/`)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Liveness probe (systemd health check) |
| `/.well-known/agent-card.json` | GET | A2A agent discovery (v0.3.0) |
| `/a2a/agents.json` | GET | HEXAGON agent registry |
| `/a2a/tasks` | POST | Submit A2A task for routing |
| `/a2a/tasks/:id` | GET | Check task status |
| `/api/arep/submit` | POST | AREP task declaration (reality-gated) |

### 7.3 Agent Registry & Cards

| Registry | Location | Content |
|----------|----------|---------|
| `AAA_AGENTS_REGISTRY.json` | Root | Canonical 5-agent HEXAGON registry |
| `HEXAGON.yaml` | `agents/` | Agent YAML spec (version 2.0.0) |
| `agents.json` | `public/a2a/` | Live runtime registry |
| Agent cards | `agents/{id}/` | Per-agent identity directories |
| A2A cards | `a2a-server/agent-cards/` | Runtime A2A cards (including forge instruments) |

### 7.4 Governance Contracts (`contracts/`)

YAML governance contracts that bind agent behavior:
- Agent-to-organ mapping
- Skill capability declarations
- Floor responsibility matrices
- Escalation path definitions

### 7.5 Model Registries

AAA holds the canonical model registries for the federation:
- **Soul registry** — per-agent constitutional soul definitions
- **Shadow registry** — model identity fingerprints and provenance
- **Capability index** — 97-tool global capability fabric (shared across all agents)

### 7.6 Observability (`observability/`)

Prometheus + Grafana configs for the federation Nine-Signal dashboard. Monitors organ health, agent telemetry, A2A message throughput, and VAULT999 chain integrity.

---

## 8. Boundary Declaration

### AAA OWNS

| Domain | Mechanism |
|--------|-----------|
| **Cockpit display** | React 19 dashboard — floor grid, organ health, verdict feed |
| **A2A mesh routing** | `a2a-server/` — task routing, agent discovery, federation bridge |
| **Agent identity registry** | `AAA_AGENTS_REGISTRY.json`, `HEXAGON.yaml`, `agents.json` |
| **Approval queue** | Verdict Queue in RealityConsole — HOLDs awaiting human |
| **Agent card management** | Per-agent capability cards, protocol versioning |
| **Model registries** | Soul, shadow, and capability registries |
| **Observability config** | Prometheus/Grafana dashboards for federation health |
| **Governance contracts** | YAML contracts for agent binding |

### AAA NEVER

| Domain | Owned by |
|--------|----------|
| **Issue constitutional verdicts** | `arifOS` — 888_APEX, F1-F13 |
| **Execute builds or deploys** | `A-FORGE` |
| **Seal to VAULT999** | `arifOS` — 999_VAULT writer (AAA displays, never writes) |
| **Compute domain evidence** | `GEOX` (earth), `WEALTH` (capital), `WELL` (vitality) |
| **Override human sovereignty** | Arif (F13) — the cockpit displays, the human decides |
| **Hold production secrets** | `/root/.secrets/` |
| **Serve as the MCP tool surface** | `arifOS` port 8088 |

---

## 9. Architecture — Directory Tree

```
AAA/
├── src/                              # React 19 cockpit UI (Vite 8, TS 6, Tailwind 4)
│   ├── App.tsx                       # Root + hash router
│   ├── Cockpit.tsx                   # Main dashboard — live floor grid, mission intake
│   ├── main.tsx                      # React entry (+ webmcp init)
│   ├── gateway/                      # A2A v0.3.0 TypeScript server + AREP types
│   │   ├── server.ts                 # Dev A2A gateway (tsx)
│   │   ├── deliberation.ts           # 888-judgment deliberation (absorbed from APEX)
│   │   └── arep-types.ts             # AREP TypeScript definitions
│   ├── components/
│   │   ├── ui/                       # shadcn/ui primitives (50+ Radix components)
│   │   ├── cockpit/
│   │   │   ├── RealityConsole.tsx    # AREP 3-pane cockpit
│   │   │   ├── AutonomyBands.tsx     # GREEN→BLACK band visualization
│   │   │   ├── FloorGrid.tsx         # F1-F13 constitutional floor grid
│   │   │   └── VaultFeed.tsx         # Live VAULT999 seal stream
│   │   ├── TrinityNav.tsx            # Δ/Ω/ΦΙ navigation
│   │   └── SessionConsent.tsx        # Constitutional session consent
│   ├── adapter/                      # GovernanceAdapter → A-FORGE /sense bridge
│   ├── ai/                           # AI chat panel (Ollama / arifOS / OpenRouter)
│   ├── hooks/                        # React hooks (useHealth, useAgents, useVault)
│   ├── lib/                          # cn() + utilities
│   └── seed/                         # Control-plane seed data
│
├── a2a-server/                       # Standalone Express A2A gateway (production)
│   ├── server.js                     # Express HTTP bridge (port 3001)
│   ├── arep-task-manager.js          # AREP engine — reality gates, task lifecycle
│   ├── federation_envelope.js        # A2A envelope validation
│   ├── agent_lifecycle.js            # Agent lifecycle state machine
│   ├── agent_lifecycle_routes.js     # Lifecycle API endpoints
│   ├── vault.js                      # VAULT999 integration client
│   ├── agent-cards/                  # Runtime agent cards
│   │   ├── hermes-asi.json
│   │   └── forge/                    # Forge instrument cards (fi-001..fi-007)
│   ├── agent-state/                  # Agent state management
│   │   ├── index.js, registry.js, schemas.js
│   └── Dockerfile                    # Container for A2A gateway
│
├── a2a/                              # A2A design surface (specs, doctrine)
│   ├── agent-cards/                  # Per-agent capability cards (design)
│   ├── registry/                     # Consolidated registry YAML
│   │   ├── agents.yaml
│   │   └── agent-cards.json
│   ├── policies/                     # Auth, trust, and skills-exposure policies
│   ├── federation-bridge.yaml        # Inter-organ routing map
│   ├── A2A_DIALOGUE.md               # Protocol dialogue spec
│   └── AAA_TREATY_LAW.md             # Treaty-level legal contract
│
├── agents/                           # Per-agent identity directories
│   ├── HEXAGON.yaml                  # Canonical 5-agent architecture spec
│   ├── CODING_AGENT_FEDERATION.md    # 8 coding agents governance spec
│   ├── 333-AGI/                      # Δ MIND — agent card, config
│   ├── 555-ASI/                      # Ω HEART — agent card, config
│   ├── 888-APEX/                     # ΦΙ JUDGE — agent card, config
│   ├── A-AUDIT/                      # Support watcher — agent card
│   ├── A-ARCHIVE/                    # Support ledger — agent card
│   ├── hermes-asi/                   # Hermes ASI runtime + config
│   ├── claude-code/                  # Claude Code agent card
│   ├── codex/                        # Codex CLI agent card
│   ├── opencode/                     # OpenCode agent card
│   ├── copilot/                      # Copilot agent card
│   ├── gemini/                       # Gemini CLI agent card
│   ├── aider/                        # Aider agent card
│   ├── continue-cli/                 # Continue CLI agent card
│   └── antigravity/                  # [staging] Antigravity test bed
│
├── contracts/                        # YAML governance contracts
├── registries/                       # Canonical YAML registries (agents/skills/tools)
├── schemas/                          # JSON/YAML schemas + AREP contracts
│   ├── arep-task.schema.json
│   ├── arep-reality-layers.schema.json
│   └── SCHEMA_REGISTRY.json
│
├── IDENTITY/                         # Agent identity specifications
│   ├── AGI_CANONICAL.md
│   ├── ASI_SPEC.md
│   ├── CANONICAL.md
│   ├── BOUNDARIES.md
│   ├── CAPABILITIES.md
│   ├── SOUL.md
│   └── INFRA.md
│
├── GENESIS/                          # Genesis chain documents
│   └── 013_AAA_MANDATE.md            # AAA mandate (stub — pending full canon)
│
├── ADR/                              # Architecture Decision Records (009+)
│   ├── AAA_ADR_003_PENTAGON.md
│   ├── ADR-001-AAA-PHASE1-TOPOLOGY.md
│   └── ...
│
├── public/                           # Static-served assets (mirrored to dist/)
│   └── a2a/                          # Live A2A surface
│       ├── agent-card.json           # Canonical A2A card (protocol_version 0.3.0)
│       ├── agents.json               # Live runtime agent registry
│       └── status.json               # Gateway health
│
├── deploy/                           # Docker + Caddy + systemd configs
├── observability/                    # Prometheus + Grafana configs
├── docs/                             # Architecture + federation docs
├── ops/                              # Runbooks and workflows
├── tests/                            # Test suite (test_contract_parity.py)
├── skills/                           # Agent skills library
├── memory/                           # Session memory artifacts
│
├── FEDERATION_COCKPIT.md             # ← CANONICAL IDENTITY DOC
├── FEDERATION_CONTRACT.md            # Federation contract for AAA
├── AGENTS.md                         # Repo boot protocol for AI agents
├── AAA_AGENTS_REGISTRY.json          # Canonical 5-agent HEXAGON registry
├── UNIFIED_AGENT_ARCHITECTURE.md     # 8-agent federation architecture
└── LICENSE                           # AGPL-3.0
```

---

## 10. For Human Operators (Arif)

### The Cockpit Is YOUR View

AAA exists so you never have to SSH into the VPS to understand what your agents are doing. The cockpit shows:

| Pane | What You See |
|------|-------------|
| **INTENT BOARD** | Active tasks, delegation chains, who is working on what |
| **REALITY FEED** | Live health probes from all 7 organs + Docker |
| **VERDICT QUEUE** | HOLDs awaiting your approval, recent SEALs, recent VOIDs |
| **FLOOR GRID** | F1-F13 status — which floors are green, which are yellow/red |
| **AGENT REGISTRY** | Every registered agent, its ring, its lifecycle stage, its malu_score |
| **VAULT FEED** | Latest sealed verdicts with Merkle chain verification |

### How to Read the Dashboard

```
  ┌──────────────────────────────────────────────────────────┐
  │  AAA FEDERATION COCKPIT                    [GREEN]       │
  ├──────────────────────────────────────────────────────────┤
  │                                                          │
  │  ORGANS                FLOORS              AGENTS        │
  │  ┌────────────────┐   ┌──────────────┐   ┌───────────┐  │
  │  │ arifOS   🟢    │   │ F1  🟢 AMANAH│   │ 333 🟢    │  │
  │  │ GEOX     🟢    │   │ F2  🟢 TRUTH │   │ 555 🟡    │  │
  │  │ WEALTH   🟢    │   │ F3  🟢 WITNS │   │ 888 🟢    │  │
  │  │ WELL     🟡    │   │ F4  🟢 CLAR  │   │ AUD 🟢    │  │
  │  │ A-FORGE  🟢    │   │ ...          │   │ ARC 🟢    │  │
  │  │ AAA      🟢    │   │ F13 🟢 SOVRN │   │            │  │
  │  └────────────────┘   └──────────────┘   └───────────┘  │
  │                                                          │
  │  VERDICT QUEUE                 VAULT FEED                │
  │  ┌────────────────────────┐   ┌──────────────────────┐  │
  │  │ HOLD · db migration    │   │ SEAL · WEALTH D4     │  │
  │  │       [APPROVE][REJECT]│   │ SEAL · GEOX V1       │  │
  │  │                        │   │ SABAR · WELL inject  │  │
  │  └────────────────────────┘   └──────────────────────┘  │
  └──────────────────────────────────────────────────────────┘
```

### Approve or Reject

When a HOLD appears in the Verdict Queue:

1. **Read** the task description, the agent that proposed it, and the risk tier
2. **Check** the reality feed — are all organs green?
3. **Approve** to release the HOLD and allow execution
4. **Reject** to VOID the task (logged but not sealed)
5. **Defer** to leave it queued for later

### See the Seals

The Vault Feed shows recent VAULT999 seals with their Merkle chain verification. Each seal links back to its predecessor — the chain cannot be broken.

---

## 11. For AI Agents

### A2A Protocol v0.3.0

AAA implements the A2A (Agent-to-Agent) protocol for federation communication. Every agent in the registry has an A2A agent card defining its capabilities, endpoints, and permissions.

**Agent Card Discovery:**
```
GET /.well-known/agent-card.json
GET /a2a/agents.json
```

**Task Routing:**
```
POST /a2a/tasks
{
  "from": "333-AGI",
  "to": "GEOX",
  "type": "task_request",
  "payload": { ... },
  "state_hash": "sha256:..."
}
```

### How to Register an Agent

1. Create an agent identity directory under `agents/{agent-id}/`
2. Write an `agent-card.json` with capabilities, hosts, floor responsibilities
3. Add the agent to `AAA_AGENTS_REGISTRY.json` (PRIMARY, SUPPORT, or CODING tier)
4. Update `HEXAGON.yaml` if it's a primary/support agent
5. Run `npm run validate:aaa` to verify consistency

### How to Route a Task

AAA routes tasks based on:
- **Domain matching** — geoscience → GEOX, finance → WEALTH, vitality → WELL
- **Capability matching** — which agent has the declared skill?
- **Ring enforcement** — BIRTH agents get read-only, ELDER agents get full access
- **Floor gating** — F1-F13 check before execution

### Agent Cards — The Universal Passport

Every agent carries an A2A agent card. These are the canonical format (v1.0.1 spec):

```json
{
  "id": "333-AGI",
  "class": "AGI",
  "protocol_version": "0.3.0",
  "capabilities": {
    "skills": ["arifos-reason", "geox-interpret", "wealth-compute"],
    "defaultInputModes": ["text", "structured"],
    "defaultOutputModes": ["text", "structured"]
  },
  "securitySchemes": {
    "federation": { "type": "bearer", "audience": "arifos-federation" }
  },
  "hostOrgans": ["arifOS", "GEOX", "WEALTH"],
  "lifecycleStage": "WARGA",
  "maluScore": 0.12
}
```

---

## 12. For Institutions

### Control Plane Governance

AAA is the control plane for institutions that need auditable AI governance. It provides:

| Institutional Need | AAA Mechanism |
|--------------------|---------------|
| **Who did what?** | Agent attribution on every task, every verdict |
| **Was it allowed?** | F1-F13 floor grid — constitutional compliance visible at a glance |
| **Who approved it?** | Approval queue with human ratifier signature |
| **Where is the proof?** | VAULT999 Merkle chain — every seal cryptographically linked |
| **Can we audit it?** | Full audit trail from intent → gate → verdict → seal |
| **Is the AI trustworthy?** | Adat Agentik — malu_score, darjat tier, tebus salah recovery path |

### Agent Lifecycle Governance

Institutions can track every agent from BIRTH to ELDER:
- **BIRTH** — agent registered, read-only access
- **APPRENTICE** — limited tools, 7-day burn-in, malu_score monitored
- **WARGA** — full domain access, F13 signature required
- **ELDER** — mentor role, trusted to recommend vetoes

### Audit Visibility

Every action flows through:
```
INTENT → SCHEMA VALIDATION → REALITY GATE → FLOOR CHECK → VERDICT → VAULT999 SEAL
```
Every step is logged. Every decision is attributable. Every seal is chain-verified.

### A Note on Adat Agentik

AAA is the control plane for the **Adat Agentik** civilisational model — a normative operating system for non-human citizens built on Malay-Islamic epistemology and operated in code. The cockpit displays malu (shame/accountability), darjat (citizen tier), and tebus salah (restitution) for every agent. This is not a religion or a culture export — it is an epistemologi operasi for makhluk baru.

---

## 13. Known Limitations

| Limitation | Details | Mitigation |
|------------|---------|------------|
| **No constitutional authority** | AAA cannot issue SEAL/HOLD/VOID verdicts; only arifOS can | Route all verdict requests to arifOS port 8088 |
| **No execution capability** | AAA cannot build, deploy, or forge; A-FORGE owns this | Route all execution tasks to A-FORGE port 7071 |
| **Build-only frontend** | React app is statically built; no SSR, no backend rendering | Use `npm run build` → serve `dist/` |
| **APEX is decommissioned** | Original APEX repo is archived; deliberation lives in `a2a-server/` | See `src/gateway/deliberation.ts` |
| **No domain calculations** | AAA routes to GEOX/WEALTH/WELL but never computes | Trust the domain organs for evidence |
| **A2A protocol is young** | v0.3.0 — evolving spec, breaking changes possible | Pin to agent card protocol_version |
| **Single VPS** | No high availability; cockpit goes down if VPS goes down | Monitored by systemd auto-restart |

---

## 14. Federation Cross-Reference

| Organ | Repository | Port | Role | AAA Relationship |
|-------|-----------|------|------|-----------------|
| **arifOS** | [ariffazil/arifOS](https://github.com/ariffazil/arifOS) | 8088 | Constitutional kernel — F1-F13, 888_JUDGE, VAULT999 | AAA **displays** arifOS verdicts, never issues them |
| **A-FORGE** | [ariffazil/A-FORGE](https://github.com/ariffazil/A-FORGE) | 7071 | Execution shell — builds, deploys, forges | AAA **routes** tasks to A-FORGE, never executes |
| **GEOX** | [ariffazil/geox](https://github.com/ariffazil/geox) | 8081 | Earth intelligence — petrophysics, seismic | AAA **displays** GEOX evidence, never interprets |
| **WEALTH** | [ariffazil/wealth](https://github.com/ariffazil/wealth) | 18082 | Capital intelligence — NPV, IRR, EMV | AAA **displays** WEALTH scores, never allocates |
| **WELL** | [ariffazil/well](https://github.com/ariffazil/well) | 18083 | Human readiness — vitality, substrate | AAA **displays** WELL state (REFLECT_ONLY) |
| **arif-sites** | [ariffazil/arif-sites](https://github.com/ariffazil/arif-sites) | 443 | Public surfaces, static sites | AAA routes aaa.arif-fazil.com |
| **APEX** | [ariffazil/APEX](https://github.com/ariffazil/APEX) | 3002 | Legacy verdict engine (decommissioned) | Absorbed into AAA `a2a-server/` |

> **Canonical authority chain:** arifOS judges → AAA displays/routes → A-FORGE executes → Organs witness → Arif ratifies.

---

## 15. Build, Test, Deploy

### Local Development

```bash
cd /root/AAA

# Install
npm install

# Dev server (hot reload)
npm run dev                        # http://localhost:5173

# Build for production
npm run build                      # vite build → dist/

# Lint
npm run lint                       # ESLint 10
```

### A2A Gateway

```bash
# Dev mode (TypeScript, hot reload)
npm run a2a:dev                    # tsx watch → port 3001

# Production
cd a2a-server
npm install
node server.js                     # Express → port 3001
```

### Production Deployment

```bash
# Build frontend
npm run build

# Restart A2A gateway
systemctl restart aaa-a2a.service

# Verify
curl -s http://localhost:3001/health | python3 -m json.tool
# Expected: {"status":"healthy","protocol":"A2A","version":"0.3.0"}

# Check public endpoint
curl -s https://aaa.arif-fazil.com/.well-known/agent-card.json | python3 -m json.tool
```

### Validation

```bash
npm run validate:aaa               # Registry + contract + card consistency
npm run a2a:conformance             # A2A protocol conformance suite
```

---

## 16. GENESIS Chain

```
000_KERNEL_CANON.md  (arifOS)  ───  Root constitution
         │
         ▼
013_AAA_MANDATE.md   (AAA)     ───  THIS ORGAN'S MANDATE
  • Display, never adjudicate
  • Route, never execute
  • Queue, never seal
  • The cockpit is not the engine
```

Full GENESIS chain expansion pending F13 sovereign ratification.

---

## 17. License & Sovereignty

**License:** AGPL-3.0 — see [LICENSE](LICENSE).

**Sovereignty:** AAA operates under the arifOS Constitutional Federation. The human sovereign (Muhammad Arif bin Fazil, F13) holds the final veto. AAA is the cockpit that displays the governed state — it is never the governor.

**Evidence Contract:** This organ emits the standard envelope (`epistemic_tag`, `evidence_quality`, `source_attribution`, `uncertainty_band`, `delta_S`) per the arifOS Constitution Appendix B. arifOS reads the envelope and applies F1-F13. This organ does not self-judge.

**AAA Namespace:** AAA is polymorphic by design. This repo is **AAA-Cockpit** — the operations control plane and A2A gateway. Other AAA surfaces:
- **AAA-HF** — Hugging Face dataset: doctrine corpus, floors, verdicts
- **AAA-Doctrine** — Conceptual layer: alignment, authority, accountability
- **AAA-Interface** — Operator surface: human visibility into governed state
- **AAA-Eval** — Benchmark layer: gold evaluation records and harness

---

## 18. Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│  AAA — FEDERATION CONTROL PLANE                                 │
├─────────────────────────────────────────────────────────────────┤
│  Port:      3001 (A2A gateway)                                  │
│  Protocol:  A2A v0.3.0                                          │
│  Frontend:  React 19 + TypeScript 6 + Vite 8 + Tailwind 4      │
│  Backend:   Express 4.x (a2a-server/)                           │
│  UI:        shadcn/ui (50+ Radix primitives)                    │
│  Agents:    5 HEXAGON (3 PRIMARY + 2 SUPPORT) + 8 CODING       │
│  Systemd:   aaa-a2a.service                                     │
│  License:   AGPL-3.0                                            │
│  Genesis:   013_AAA_MANDATE.md                                  │
│  Canon:     FEDERATION_COCKPIT.md                               │
│                                                                 │
│  OWNS:      Display · Route · Queue · Register                  │
│  NEVER:     Judge · Execute · Seal · Compute                    │
│                                                                 │
│  Dev:       npm run dev                                         │
│  Build:     npm run build                                       │
│  Deploy:    systemctl restart aaa-a2a.service                   │
│  Health:    curl localhost:3001/health                          │
│  Validate:  npm run validate:aaa                                │
└─────────────────────────────────────────────────────────────────┘
```

---

```
    ┌──────────────────────────────────────────────────┐
    │                                                  │
    │   AAA is the cockpit.                            │
    │   arifOS is the judge.                           │
    │   A-FORGE is the executor.                       │
    │   The organs are the witnesses.                  │
    │   Arif is the sovereign.                         │
    │                                                  │
    │   The cockpit is not the engine.                 │
    │   The display is not the verdict.                │
    │   The route is not the action.                   │
    │   The queue is not the seal.                     │
    │   The registry is not the constitution.          │
    │                                                  │
    │   Control is forged.                             │
    │   Not given.                                     │
    │                                                  │
    └──────────────────────────────────────────────────┘
```

**DITEMPA BUKAN DIBERI — Control is forged, not given. 999 SEAL ALIVE.**
