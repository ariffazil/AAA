# arifOS Federation — Code & Infrastructure Map
> **Generated:** 2026-06-22 | **Purpose:** Lower entropy. Single source of truth for where everything lives.
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## FEDERATION AT A GLANCE

```
┌─────────────────────────────────────────────────────────────────┐
│                    Arif (F13 SOVEREIGN)                         │
│                         │                                       │
│         ┌───────────────┼───────────────┐                       │
│         ▼               ▼               ▼                       │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐                    │
│   │   AAA    │   │  APEX    │   │  HERMES  │                    │
│   │ Cockpit  │   │  Judge   │   │ Telegram │                    │
│   │  :3001   │   │ :3002    │   │  :8644   │                    │
│   └────┬─────┘   └────┬─────┘   └────┬─────┘                    │
│        │              │              │                           │
│   ┌────┴──────────────┴──────────────┴────┐                      │
│   │         arifOS KERNEL :8088           │                      │
│   │   22 canonical + 40 diagnostic tools  │                      │
│   │   F1-F13 floors | VAULT999 | SES     │                      │
│   └────┬──────────┬──────────┬───────────┘                      │
│        │          │          │                                   │
│   ┌────▼──┐  ┌────▼──┐  ┌───▼────┐                              │
│   │ GEOX  │  │WEALTH │  │  WELL  │                              │
│   │ :8081 │  │:18082 │  │ :18083 │                              │
│   └───────┘  └───────┘  └────────┘                              │
│        │          │          │                                   │
│        └──────────┼──────────┘                                   │
│                   ▼                                              │
│           ┌──────────────┐                                       │
│           │   A-FORGE    │                                       │
│           │ :7071 (HTTP) │                                       │
│           │ :7072 (MCP)  │                                       │
│           │  4-layer     │                                       │
│           │  forge gate  │                                       │
│           └──────┬───────┘                                       │
│                  ▼                                               │
│           ┌──────────────┐                                       │
│           │   VAULT999   │                                       │
│           │  Immutable   │                                       │
│           │   Ledger     │                                       │
│           └──────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. arifOS — Constitutional Kernel (`/root/arifOS`)

**Repo:** `github.com/ariffazil/arifOS` | **Port:** 8088 | **Stack:** Python 3.12, FastMCP, FastAPI

### 1.1 Directory Map

```
/root/arifOS/
├── arifosmcp/              ← PRIMARY SOURCE (~200 files)
│   ├── runtime/             ← Server, bridges, gates, seals (largest module)
│   ├── tools/               ← 52 tool handler implementations
│   ├── schemas/             ← 57 Pydantic schema files
│   ├── gateway/             ← MCP proxy gateway (18 files)
│   ├── core/                ← Constitutional core (41 files)
│   ├── memory/              ← Memory system (16 files)
│   ├── transport/           ← MCP transport layer (15 files)
│   ├── geometry/            ← Geometric mind (18 files)
│   ├── providers/           ← LLM providers (7 files)
│   ├── resources/           ← MCP resources (24 files)
│   ├── intelligence/        ← Intelligence subsystem (13 files)
│   ├── boot/                ← Boot sequence (12 files)
│   ├── hexagon/             ← HEXAGON agent architecture (10 files)
│   ├── federation/          ← Federation contracts (8 files)
│   ├── evidence/            ← Evidence pipeline (7 files)
│   ├── abi/                 ← Protocol bridges (7 files)
│   ├── agents/              ← Eureka agent (6 files)
│   ├── apps/                ← Applications (18 files)
│   ├── evals/               ← Evaluation harness (13 files)
│   ├── specs/               ← Specifications (6 files)
│   └── constitutional_map.py ← **SOT: 57-tool → floor → stage mapping**
├── tests/                   ← ~200+ tests across 35 directories
├── deploy/                  ← Docker, Caddy, systemd, manifests
├── docs/                    ← 30+ subdirectories, 150+ files
├── scripts/                 ← 29 ops/audit scripts
├── commands/                ← 50+ CLI tools + archived scripts
├── pyproject.toml           ← 80+ dependencies
├── Dockerfile               ← Multi-stage, port 8088
└── identity.toml            ← Organ identity
```

### 1.2 Cognitive Loop (000 → 999)

| Stage | Code | Tool | Trinity | Risk |
|-------|------|------|---------|------|
| INIT | 000 | `arif_session_init` | AGI | medium |
| OBSERVE | 111 | `arif_sense_observe`, `arif_explore` | AGI | low |
| EVIDENCE | 222 | `arif_evidence_fetch` | AGI | medium |
| REASON | 333 | `arif_mind_reason` | AGI | medium |
| COMPOSE | 444r | `arif_reply_compose` | ASI | medium |
| ROUTE | 555 | `arif_kernel_route`, `arif_route`, `arif_triage`, `arif_bridge_connect` | AGI | medium |
| MEMORY | 555m | `arif_memory_recall` | AGI | medium |
| HEART | 666 | `arif_heart_critique` | ASI | medium |
| GATEWAY | 666g | `arif_gateway_connect` | ASI | medium |
| MEASURE | 777 | `arif_ops_measure` | ASI | low |
| JUDGE | 888 | `arif_judge_deliberate` | APEX | high |
| FORGE | 010 | `arif_forge_execute` | APEX | high |
| SEAL | 999 | `arif_vault_seal` | APEX | high |

### 1.3 Floor Enforcement (F1-F13)

| Floor | Name | Type | Enforcement |
|-------|------|------|-------------|
| F1 | AMANAH | HARD | Lease required for mutation |
| F2 | TRUTH | HARD | Evidence gates, confidence bands |
| F3 | TRI-WITNESS | DERIVED | Byzantine ≥ 0.75 |
| F4 | CLARITY | HARD | ΔS ≤ 0 entropy |
| F5 | PEACE² | SOFT | Non-destructive power |
| F6 | EMPATHY | SOFT | RASA protocol |
| F7 | HUMILITY | HARD | Ω₀ ∈ [0.03, 0.05], 0.90 cap |
| F8 | GENIUS | DERIVED | G ≥ 0.80 |
| F9 | ANTI-HANTU | HARD | C_dark < 0.30 |
| F10 | ONTOLOGY | HARD | Category lock |
| F11 | AUDITABILITY | HARD | All decisions logged |
| F12 | RESILIENCE | HARD | Injection defense |
| F13 | SOVEREIGN | HARD | Human veto absolute |

---

## 2. AAA — Federation Cockpit & A2A Gateway (`/root/AAA`)

**Repo:** `github.com/ariffazil/AAA` | **Port:** 3001 | **Stack:** TypeScript 6, React 19, Express 5, Python core

### 2.1 Directory Map

```
/root/AAA/
├── src/                     ← Primary source
│   ├── Cockpit.tsx           ← Operator cockpit UI (mission, floors, agents, events)
│   ├── webmcp.ts             ← 10 WebMCP tools
│   ├── gateway/
│   │   ├── server.ts         ← Express A2A gateway (createApp)
│   │   ├── deliberation.ts   ← **F1/F2/F4/F6/F9/F13 deterministic scan**
│   │   ├── paradox_anchors.ts ← 11 paradox anchors (3×3 matrix)
│   │   ├── schema.ts         ← A2A protocol types (TaskMessage, JSONRPC)
│   │   ├── store.ts          ← TaskStore + EventBus
│   │   └── auth.ts           ← Bearer + API key auth middleware
│   ├── components/           ← 40+ shadcn/ui + Cockpit panels
│   ├── ai/                   ← AI chat panel + RAG client
│   └── seed/                 ← Bootstrap: agent-card, routing policy
├── a2a-server/               ← Production A2A server (2869-line server.js)
│   ├── server.js             ← All routes + deliberation + federation + AI
│   ├── agent_lifecycle.js    ← Agent state machine
│   ├── federation_envelope.js ← Risk tier + action class validation
│   ├── mesh_coordinator.js   ← NATS loop detector + gradient computer
│   └── agent-cards/          ← Cards for all 12 agents + 8 forge instruments
├── core/                     ← Python constitutional core
│   ├── pre_forge_gate.py     ← Unified gate: F2→F3→F9→composite verdict
│   ├── citation_provenance.py ← F2 TRUTH
│   ├── witness_diversity.py  ← F3 TRI-WITNESS
│   └── shadow_audit.py       ← F9 ANTI-HANTU
├── agents/                   ← 30 agent directories
├── governance/               ← DEWAN, KAMUS, PUSTAKA, laws, fiqh
├── docs/                     ← ~95 documentation files
├── tests/                    ← Pytest: contract parity + P2P validation
├── a2a/                      ← A2A definitions, agent cards, peer contracts
└── registries/               ← Canonical agent/tool/federation registries
```

### 2.2 A2A Endpoints (port 3001)

| Route | Purpose |
|-------|---------|
| `GET /.well-known/agent-card.json` | AAA identity |
| `GET /.well-known/a2a-discovery.json` | Discovery contract |
| `GET /a2a/{agent}/agent-card.json` | Per-agent cards |
| `POST /message/send` | JSON-RPC ingress → deliberation → execute |
| `POST /a2a/tasks/send` | A2A task dispatch |
| `GET /operator/tasks` | Operator task list |
| `GET /operator/holds` | Hold summary |
| `GET /operator/seals` | Seal count + vault status |
| `POST /operator/tasks/:id/approve` | Approve held task |
| `GET /federation/organs` | List registered organs |
| `POST /federation/register` | Register federated organ |

### 2.3 Agent Registry (30 agents)

| Agent | Role | Agent | Role |
|-------|------|-------|------|
| 333-AGI | Delta MIND reasoning | hermes-asi | Telegram @ASI_arifos_bot |
| 555-ASI | Omega HEART synthesis | hermes-ops | Operations relay |
| 777-forge | Engineering witness | openclaw | AGI gateway (:18789) |
| 888-APEX | Phi JUDGE deliberation | opencode | Coding agent |
| A-ARCHIVE | Ledger sealing | claude-code | Anthropic CLI forge |
| A-AUDIT | Compliance auditing | codex | OpenAI coding forge |
| A-ENGINEER | Engineering agent | copilot | GitHub Copilot forge |
| A-ARCHITECT | Architecture agent | aider | AI pair programming |
| kernel-scribe | Documentation | kimi-code | Moonshot forge |
| ops-planner | Operational planning | antigravity | Coding agent |
| self-forge-advisor | Meta-cognition | warga | Citizen registry |

---

## 3. A-FORGE — Execution Engine (`/root/A-FORGE`)

**Repo:** `github.com/ariffazil/A-FORGE` | **Ports:** 7071 (HTTP), 7072 (MCP) | **Stack:** TypeScript, Node.js 22, MCP SDK 1.29

### 3.1 Directory Map

```
/root/A-FORGE/
├── src/
│   ├── domain/               ← Pure business logic (no I/O)
│   │   ├── engine/            ← AgentEngine, IntentRouter, BudgetManager
│   │   ├── governance/        ← **THE 13-FLOOR ENFORCER** + 4-layer gate
│   │   │   ├── FloorEnforcer.ts      ← Central F1-F13 dispatcher
│   │   │   ├── AmanahLockManager.ts  ← Layer 1: F1 AMANAH
│   │   │   ├── ModelCapabilityGate.ts← Layer 2: model check
│   │   │   ├── GovernanceBridge.ts   ← Layer 3: arifOS bridge
│   │   │   ├── actionClassifier.ts   ← 8-tier taxonomy
│   │   │   └── f1*.ts → f12*.ts      ← Individual floor checkers
│   │   ├── agents/            ← AAAgent, Coordinator, Worker profiles
│   │   ├── containment/       ← bwrap/firejail/docker sandbox
│   │   ├── forge/workflow/    ← Symphony workflow engine
│   │   ├── planner/           ← PlanValidator, ParallelPlanner
│   │   └── types/             ← 22 domain type files
│   ├── application/          ← Use cases
│   │   ├── approval/          ← Layer 4: ApprovalBoundary + TicketStore
│   │   ├── memory/            ← LongTerm, ShortTerm, ArifOSClient
│   │   └── a2a/               ← A2A protocol + DeepNShadow
│   ├── infrastructure/       ← Adapters
│   │   ├── llm/               ← ModelGateway (provider sovereignty)
│   │   ├── tools/             ← ToolRegistry (62+ tools)
│   │   ├── vault/             ← VaultClient, PostgresVault, MerkleV3
│   │   ├── bridges/           ← geoxBridge, wealthBridge
│   │   └── cli/code-mode/     ← CLI, code sandbox
│   └── interfaces/           ← Delivery
│       ├── server.ts          ← Express HTTP (:7071)
│       ├── mcp/
│       │   ├── core.ts        ← **MCP core — tools registered**
│       │   ├── serve.ts       ← Multi-transport bootstrap (:7072)
│       │   ├── forgeTools.ts  ← 18 forge_* tools
│       │   ├── gatewayTools.ts← P1 external MCP wrappers
│       │   └── proxyTools.ts  ← 6 groups: filesystem, postgres, memory, git, github, docker
│       ├── routes/            ← approval, governance, jobs, vault routes
│       └── middleware/        ← ConstitutionalBoundary, operatorAuth
├── test/                     ← 32 test files (Jest-free)
├── docs/                     ← 12 subdirectories, 80+ files
├── deploy/                   ← Docker, Caddy, systemd, Grafana, Prometheus
└── services/                 ← MIND:51001 + MEMORY:51002 federated services
```

### 3.2 The 4-Layer Forge Gate

Every execution passes ALL four. No skipping.

```
Layer 1: AmanahLockManager   → HARAM/BLOCK | HOLD | PASS
Layer 2: ModelCapabilityGate → DEGRADED | MISSING | PASS
Layer 3: GovernanceBridge    → SEAL | SABAR | VOID (via arifOS)
Layer 4: ApprovalBoundary    → APPROVED | 888_HOLD | DENIED
```

### 3.3 MCP Tool Groups

| Group | Count | Examples |
|-------|-------|----------|
| Canonical (arifOS bridged) | 22 | `arif_session_init` → `arif_vault_seal` |
| forge_identity_* | 4 | register, status, list, revoke |
| forge_lease_* | 4 | create, check, extend, revoke |
| forge_registry_* | 3 | list, describe, search |
| forge_shell_* | 1 | exec (F1-AMANAH gated) |
| forge_log_* | 3 | stream, query, tail |
| forge_job_* | 4 | submit, status, cancel, list |
| Gateway (external MCPs) | 8 | Playwright, MiniMax, Netdata, Brave, GitHub |
| forge_filesystem_* | 5 | read, write, glob, grep, stat |
| forge_postgres_* | 3 | query, schema, tables |
| forge_memory_* | 3 | recall, store, list |
| forge_git_* | 4 | status, diff, log, commit |
| forge_github_* | 4 | PR, issue, search, status |
| forge_docker_* | 4 | ps, logs, exec, images |
| Diagnostic | 9 | leases, probes, Hermes, attestation |

---

## 4. VAULT999 — Immutable Ledger (`/root/VAULT999` → `/root/.local/share/arifos/vault999`)

### 4.1 Structure

```
/root/VAULT999/
├── outcomes.jsonl           ← **Primary: 4,342 sealed verdicts (1.67 MB)**
├── federation_epistemology.db ← SQLite: epistemic events + subjects
├── CCC_CANON/               ← Canonical sealed events
├── capsules/                 ← Capsule subsystem (LAW, SCAR, LINEAGE)
├── doctrine/                 ← MEMORY_AUTHORITY_MANIFESTO + 71-system audit
├── kernel/                   ← ARIFOS_KERNEL.invariant.v1.0.yaml
├── schemas/                  ← artifact_kind.schema.json (6 epistemic classes)
├── scars/                    ← Kinabalu scar ledger
├── witness/                  ← Cross-human verification receipts
├── sessions/                 ← Session seal records
├── signatures/               ← Cryptographic signatures
└── backups/                  ← 5× outcomes.jsonl backups
```

### 4.2 Supabase Mirror
- **Table:** `vault_sealed_events`
- **Project:** `utbmmjmbolmuahwixjqc`
- **Postgres:** `postgresql://arifos_admin@postgres:5432/vault999`

---

## 5. VPS INFRASTRUCTURE — af-forge (`/root`)

### 5.1 Service Map (all systemd)

```
FEDERATION CORE:
  arifos.service              → :8088  (Python kernel)
  arifos-gateway.service      → MCP gateway
  arifosd.service             → Control plane daemon

AI/LLM:
  geox-mcp.service            → :8081  (Earth intelligence)
  minimax-code-mcp.service    → :18091 (VLM + search)
  minimax-media-mcp.service   → :18090 (TTS, media)
  ollama.service              → :11434 (Local LLM)
  mind.service                → :51001 (MIND cognitive)
  cognitive-memory.service    → :51002 (MEMORY cognitive)

EXECUTION:
  a-forge.service             → :7071  (HTTP server)
  a-forge-mcp.service         → :7072  (MCP gateway)
  aaa-a2a.service             → :3001  (A2A gateway)
  aaa-preforge.service        → :18990 (Pre-forge gate)
  forge-gateway.service       → 777-FORGE

MESSAGING:
  nats-server.service         → :4222, :8222
  hermes-a2a.service          → :18001
  hermes-asi-gateway.service  → :8644  (Telegram bot)
  f11-bridge.service          → :5002  (F13 witness)

DATA:
  postgres (docker)           → :5432  (pgvector/pg16)
  redis (docker)              → :6379
  qdrant (docker)             → :6333-6334
  falkordb (docker)           → :6380
  temporal (docker)           → :7233

OBSERVABILITY:
  prometheus.service          → :9090
  grafana-server.service      → :3000
  node_exporter.service       → :9100
  netdata.service             → :19999
  loki (docker)               → :3100
  promtail (docker)           → :9080

NETWORK:
  caddy.service               → :80, :443  (14+ domains, TLS)
  cloudflared.service         → :20241
  tailscaled.service          → mesh VPN
  ssh.service                 → :22888
```

### 5.2 Docker (9 containers, all healthy)

| Container | Image | Port |
|-----------|-------|------|
| postgres | pgvector/pgvector:pg16 | 5432 |
| redis | redis:7-alpine | 6379 |
| qdrant | qdrant/qdrant:latest | 6333-6334 |
| falkordb | falkordb/falkordb:latest | 6380 |
| temporal | temporalio/auto-setup:latest | 7233 |
| temporal-ui | temporalio/ui:latest | 8233 |
| loki | grafana/loki:2.9.4 | 3100 |
| promtail | grafana/promtail:2.9.4 | 9080 |
| graphiti-mcp | zepai/knowledge-graph-mcp:latest | 8000 |

### 5.3 Hooks (`/root/hooks/`)

| Hook | Trigger | Purpose |
|------|---------|---------|
| bootstrap.sh | SessionStart | Federation health + context injection |
| token-gate.sh | PreToolUse | F1/F5/F12 floor enforcement |
| auto-approve.sh | PermissionRequest | Auto-approve safe patterns |
| auto-seal.sh | PostToolUse | Auto-seal after constitutional tools |
| failure-recovery.sh | PostToolUseFailure | Recovery from failed calls |
| prompt-enrich.sh | UserPromptSubmit | Context enrichment |
| precompact.sh | PreCompact | Integrity checks |
| postcompact.sh | PostCompact | Post-compaction verify |
| stop.sh | Stop | Clean shutdown + checkpoint |

### 5.4 Secrets Map

| Location | Contents |
|----------|----------|
| `/root/.secrets/vault.env` | All secrets (16.7 KB) |
| `/root/.secrets/vault.flat.env` | Systemd-safe flat env (8.9 KB) |
| `/root/.secrets/providers.yml` | AI provider configs |
| `/root/.secrets/INDEX.md` | Full credential inventory |
| `/root/.env` | Agent-level env |
| `/root/arifOS/.env` | arifOS env |
| `/root/A-FORGE/.env` | A-FORGE env |

---

## 6. QUICK REFERENCE

### Port → Service

| Port | Service | Port | Service |
|------|---------|------|---------|
| 80/443 | Caddy | 7072 | A-FORGE MCP |
| 3000 | Grafana | 8000 | Graphiti KG |
| 3001 | AAA A2A | 8001 | L5 Search |
| 3002 | APEX Prime | 8081 | GEOX MCP |
| 4222 | NATS | 8088 | arifOS Kernel |
| 5001 | VAULT999 Writer | 8644 | Hermes ASI |
| 5002 | F11 Bridge | 8931 | Playwright |
| 51001 | MIND | 9090 | Prometheus |
| 51002 | MEMORY | 9100 | Node Exporter |
| 5432 | Postgres | 11434 | Ollama |
| 6333 | Qdrant | 18082 | WEALTH |
| 6379 | Redis | 18083 | WELL |
| 6380 | FalkorDB | 18090 | MiniMax Media |
| 7071 | A-FORGE HTTP | 18091 | MiniMax Code |
| 7233 | Temporal | 19999 | Netdata |
| 8233 | Temporal UI | 22888 | SSH |

### Repo → Directory → GitHub

| Repo | Directory | GitHub |
|------|-----------|--------|
| arifOS | `/root/arifOS` | `ariffazil/arifOS` |
| AAA | `/root/AAA` | `ariffazil/AAA` |
| A-FORGE | `/root/A-FORGE` | `ariffazil/A-FORGE` |
| VAULT999 | `/root/VAULT999` | (local only) |
| GEOX | `/root/geox` | `ariffazil/GEOX` |
| HERMES | `/root/HERMES` | `ariffazil/HERMES` |

### Tool Surface Summary

| Organ | Tool Count | Transport |
|-------|-----------|-----------|
| arifOS | 62 (22 canonical + 40 diagnostic) | MCP streamable-http |
| A-FORGE | 77 (bridged + native) | MCP streamable-http |
| GEOX | 50+ | MCP streamable-http |
| WEALTH | 30+ | MCP streamable-http |
| WELL | 15+ | MCP streamable-http |
| AAA | 10 (WebMCP) | A2A + Express |

---

*End of Federation Map. Regenerate when significant structural changes occur.*
