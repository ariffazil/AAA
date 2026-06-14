# arifOS Reference Architecture
## A Constitutional Kernel for Governed MCP Federation

**Version:** 2026-06-14
**Status:** PUBLISHED — Reference Architecture (not product spec)
**Repository:** [github.com/ariffazil/arifos](https://github.com/ariffazil/arifos)
**Protocol:** MCP v2025-11-25 + Extensions (Apps, Epistemic)

---

## Executive Abstract

This document describes a running reference architecture that uses **Model Context Protocol (MCP)** as the control plane for governed intelligence — not the whole stack.

The key structural insight: **the industry treats MCP as a connector protocol. We treat it as a constitutional layer.** The difference is not cosmetic. A connector protocol attaches tools to models. A constitutional layer governs what those tools can do, how they report truth, who approves irreversible actions, and how the system accounts for itself.

This architecture has been running in production since June 2024 at `af-forge` (72.62.71.199) — 7 organ services, 150+ MCP tools, hash-chained audit trail, full constitutional enforcement, live human sovereign veto.

---

## 1. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HUMAN SOVEREIGN (Arif)                       │
│                         F13 · Final Veto                            │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
┌──────────────────────────────────▼──────────────────────────────────┐
│                     arifOS Constitutional Kernel                     │
│                   MCP Port 8088 · 13 Canonical Tools                 │
│                                                                      │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ SESSION   │  │  MIND    │  │  HEART   │  │ 888 JUDGE         │  │
│  │ Init      │  │  Reason  │  │  Critique │  │ Deliberate·SEAL   │  │
│  │ Attest    │  │  Plan    │  │  Maruah   │  │ HOLD·VOID·SABAR   │  │
│  │ Lease     │  │  Reflect │  │  Empathy  │  │                   │  │
│  └───────────┘  └──────────┘  └──────────┘  └───────────────────┘  │
│                                                                      │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ SENSE     │  │ MEMORY   │  │ VAULT    │  │ GATEWAY           │  │
│  │ Observe   │  │ L1–L6    │  │ 999_SEAL │  │ A2A Mesh          │  │
│  │ Search    │  │ Recall   │  │ Chain    │  │ Organ Routing     │  │
│  │ Ingest    │  │ Context  │  │ Audit    │  │                   │  │
│  └───────────┘  └──────────┘  └──────────┘  └───────────────────┘  │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   │ MCP · HTTP SSE / Streamable HTTP
                                   │
       ┌───────────┬───────────────┼───────────────┬───────────┐
       │           │               │               │           │
┌──────▼──────┐ ┌──▼──────────┐ ┌─▼───────────┐ ┌─▼──────────┐ ┌▼───────────┐
│             │ │              │ │              │ │            │ │            │
│   GEOX      │ │   WEALTH     │ │    WELL      │ │  A-FORGE   │ │   AAA      │
│  Earth      │ │  Capital     │ │   Human      │ │ Execution  │ │  Cockpit   │
│  Intel      │ │  Intel       │ │   Readiness  │ │  Shell     │ │  Control   │
│             │ │              │ │              │ │            │ │  Plane     │
│  Port 8081  │ │  Port 18082  │ │  Port 18083  │ │  Port 7071 │ │  Port 3001 │
│  40 tools   │ │  19 tools    │ │  18 tools    │ │  18 tools  │ │  + React   │
│  EVIDENCE   │ │  MATH        │ │  REFLECT     │ │  EXECUTE   │ │  UI        │
└─────────────┘ └──────────────┘ └──────────────┘ └────────────┘ └────────────┘
       │               │               │               │               │
       └───────────────┴───────────────┴───────────────┴───────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │     PHYSICAL / EXTERNAL      │
                    │         SYSTEMS              │
                    │                              │
                    │  Sensors · Twins · APIs      │
                    │  Edge · 5G · OPC UA · WoT   │
                    │  Matter · OpenUSD · OpenXR   │
                    └──────────────────────────────┘
```

---

## 2. Core Architectural Principles

### 2.1 Constitutional Floor Enforcement (F1–F13)

Every tool call passes through a constitutional gate before execution. The floors are not documentation — they are **code-enforced invariants**:

| Floor | Name | Enforcement |
|-------|------|-------------|
| F1 | AMANAH | Reversibility check + backup before mutation |
| F2 | TRUTH | Epistemic tags required on all truth claims |
| F3 | TRI-WITNESS | Cross-agent verification for critical claims |
| F4 | CLARITY | Entropy measurement on all state changes |
| F5 | PEACE² | Maruah score threshold for dignity-affected actions |
| F6 | EMPATHY | Heart critique before human-impacting actions |
| F7 | HUMILITY | Confidence capped at 0.90; pre-flight verify |
| F8 | LAW | System boundary enforcement between organs |
| F9 | ANTI-HANTU | Reject metaphysical claims; tool is not being |
| F10 | ONTOLOGY | Domain ontology validation |
| F11 | AUDIT | Every consequential action leaves a trace |
| F12 | INJECTION | Prompt injection detection |
| F13 | SOVEREIGN | Human veto is absolute; final override |

### 2.2 Separation of Concerns (4-Layer Model)

The architecture operates at four distinct layers, each with its own protocol and governance:

| Layer | Responsibility | Protocol | Governance |
|-------|---------------|----------|------------|
| **Reasoning** | Model inference, planning, reflection | MCP `tools/call` | arifOS session + floor enforcement |
| **Tool Access** | Discover, invoke, compose tools | MCP `tools/list` + `resources/` | Per-organ authority leases |
| **UI Rendering** | Human-facing interfaces, dashboards | MCP Apps (`ui://` resources, iframe bridge) | AAA Cockpit + governance envelopes |
| **Physical Execution** | Actuation, sensors, real-time control | OPC UA, Matter, 5G, dedicated device APIs | Deterministic safety bounds outside MCP |

### 2.3 Bounded Organ Authority

Each organ (GEOX, WEALTH, WELL, A-FORGE) is a **bounded territory** with:
- A fixed tool surface (no phantom tools)
- A canonical registry that is source-of-truth
- Constitutional floors specific to its domain
- No right to self-judge — judgment always routed to arifOS
- Epistemic tag discipline on all outputs

### 2.4 Hash-Chained Audit (VAULT999)

Every SEAL verdict is written to a three-layer immutable audit trail:
1. **Local JSONL** — Primary chain, append-only
2. **Postgres** — Structured indexed copy
3. **Supabase** — Cloud-hosted backup

Chain integrity is verified by `prev_seal_id` linking — every seal carries the hash of the prior seal.

### 2.5 Absolute Sovereign Veto (F13)

No irreversible action executes without human approval. The 888_HOLD mechanism ensures that any action classified as MUTATE or ATOMIC is paused and presented to Arif in the AAA Cockpit approval queue.

---

## 3. Organ Architecture

### 3.1 arifOS — Constitutional Kernel

- **Framework:** FastMCP 3.x (Python)
- **Port:** 8088
- **Tools:** 13 canonical + 31 diagnostic
- **Resources:** 11+ `arifos://` URIs + TREE777 knowledge tree
- **Key Functions:**
  - `arif_session_init` — Start governed session
  - `arif_mind_reason` — Multi-step reasoning + planning
  - `arif_judge_deliberate` — Constitutional verdict
  - `arif_vault_seal` — Immutable audit write
  - `arif_forge_execute` — Approved mutation execution

### 3.2 A-FORGE — Execution Shell

- **Framework:** `@modelcontextprotocol/sdk` (TypeScript)
- **Port:** 7071
- **Tools:** 18+ forge tools
- **Key Pattern:** Monkey-patched tool registration that injects FloorEnforcer into every handler
- **Role:** Gateway between model intent and system mutation

### 3.3 AAA — Control Plane

- **Framework:** React 19 + Vite 8 + A2A Server (Express)
- **Port:** 3001 (A2A), Vite dev (5173)
- **UI:** Cockpit — mission intake, approval queue, constitutional floors, MCP Apps
- **Role:** Sovereign visibility into system state + MCP Apps host

### 3.4 GEOX — Earth Intelligence

- **Framework:** FastMCP 3.x (Python)
- **Port:** 8081
- **Tools:** 40 canonical
- **Key Pattern:** Epistemic ladder (FACT → DERIVED → INTERPRETATION → HYPOTHESIS → MODEL → DECISION)
- **Role:** Evidence-only earth science coprocessor

### 3.5 WEALTH — Capital Intelligence

- **Framework:** FastMCP (Python)
- **Port:** 18082
- **Tools:** 19 public (physics-inspired: conservation, flow, gradient, entropy, energy, time, inertia, field, signal, game, boundary)
- **Role:** Evidence-only capital math, not financial advice

### 3.6 WELL — Human Readiness

- **Framework:** FastMCP (Python)
- **Port:** 18083
- **Tools:** 18 somatic (substrate classification, metabolic assessment, dignity guard)
- **Role:** Reflect-only human substrate sensing

---

## 4. Protocol Stack

```
┌──────────────────────────────────────────────────┐
│              MCP Core v2025-11-25                │
│  tools/list · tools/call · resources/read        │
│  prompts/get · JSON-RPC 2.0                      │
├──────────────────────────────────────────────────┤
│              MCP Extensions (Active)              │
│  io.modelcontextprotocol/apps (ui:// resources)   │
│  io.modelcontextprotocol/auth (OAuth delegate)    │
│  io.arifos/epistemic (Proposed)                   │
├──────────────────────────────────────────────────┤
│              A2A Protocol (AAA Gateway)           │
│  Agent-to-Agent mesh · task card exchange        │
│  NATS event bus · agent lifecycle                │
├──────────────────────────────────────────────────┤
│              Physical Layer Standards             │
│  OPC UA · Matter · OpenUSD · OpenXR              │
│  5G-Advanced / ETSI MEC · W3C WoT               │
│  (Brokered through organ gateways, not MCP)       │
└──────────────────────────────────────────────────┘
```

---

## 5. Deployment Topology

All federation organs run as **bare-metal systemd services** on a single VPS (`af-forge`, 72.62.71.199). Supporting infrastructure (Postgres, Redis, Qdrant, NATS, Temporal) runs as Docker containers.

**Ingress:** Caddy 2 + Cloudflare Tunnel (for MCP organs) + direct A records (for AAA/static sites).

```
Internet → Cloudflare Tunnel → localhost:8088 (arifOS)
         → Cloudflare Tunnel → localhost:8081 (GEOX)
         → Cloudflare Tunnel → localhost:18082 (WEALTH)
         → Cloudflare Tunnel → localhost:18083 (WELL)
         → Direct A → Caddy → localhost:3001 (AAA)
         → Direct A → Caddy → /var/www/html (Static)
```

**Security:** `localhost-as-authentication` (ADR-001). Services bound to 127.0.0.1 have no password. UFW blocks external access. Cloudflare Tunnel + Origin CA for MCP public endpoints.

---

## 6. Comparison with Industry Approaches

| Dimension | arifOS Federation | Typical Enterprise AI |
|-----------|------------------|----------------------|
| **Protocol** | MCP-native (all organs) | REST + custom SDK |
| **Governance** | Code-enforced F1–F13 floors | Configurable RBAC |
| **Audit Trail** | Hash-chained 3-layer | Database logging |
| **Sovereign Veto** | Absolute F13 888_HOLD | Configurable HITL |
| **Domain Organs** | Bounded territories with fixed tool surfaces | Generic function-calling |
| **Epistemic Discipline** | Tagged output with evidence chains | None |
| **MCP Apps UI** | SEP-1865 iframe bridge + governance overlays | Proprietary chat widgets |
| **State Management** | Localhost-as-password + UFW | Network security groups |
| **Separation of Concerns** | 4-layer (reason/tool/UI/execution) | Usually 2-layer (app + model) |

---

## 7. Deployment Requirements

### Minimum
- 1 VPS (2 vCPU, 4GB RAM)
- Docker + systemd
- Caddy 2 + Cloudflare Tunnel (for public MCP)
- Node.js 22+ (A-FORGE, AAA)
- Python 3.12+ (arifOS, GEOX, WEALTH, WELL)
- PostgreSQL 16, Redis 7, Qdrant

### Recommended for Physical-World Integration
- OPC UA gateway agent
- ETSI MEC edge node
- Digital twin platform (NVIDIA Omniverse or Siemens Xcelerator bridge)
- OpenUSD scene graph server

---

## 8. Security Model

1. **Localhost-as-Authentication:** All data services bind to 127.0.0.1, no password
2. **MCP Authorization Extension:** OAuth 2.0 delegate auth for tool calls
3. **888_HOLD:** Blocking approval gates on all MUTATE and ATOMIC action classes
4. **VAULT999:** Append-only hash chain prevents tampering with audit trail
5. **Constitutional Floor Enforcement:** F1-F13 code invariants block prohibited actions before execution
6. **F13 SOVEREIGN:** Human override of any automated decision

---

## 9. Licensing and Contribution

This architecture is published as open reference under the arifOS license.
Contributions to the epistemic extension, MCP Apps governance pattern, and tool-registry discipline are welcome via the respective GitHub repositories.

**Canonical Source:** [github.com/ariffazil/arifos](https://github.com/ariffazil/arifos)

---

*DITEMPA BUKAN DIBERI — Intelligence is forged, not given. Governance is built, not configured. The architecture is the constitution made executable.*
