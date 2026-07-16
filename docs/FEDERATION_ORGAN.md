# arifOS Federation — Canonical Organ Map

> **Sealed:** 2026-06-22 | **Authority:** F13 SOVEREIGN — Arif
> **Status:** CANONICAL — supersedes all prior organ diagrams
> **Repo substrate:** Final 33 (see trinity-33-canonical + /root/AAA/docs/TRINITY_33_REPOS.md) — 11 arifOS (law), 11 AAA (cockpit), 11 A-FORGE (execution). Orthogonal. Never let forge outrun kernel.
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## THE MAP

```
                         Arif (F13 SOVEREIGN)
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
     ┌────────▼────────┐  ┌───────▼───────┐  ┌────────▼────────┐
     │   Hermes (py)   │  │ OpenClaw (ts) │  │   AAA (ts)      │
     │   MIND organ    │  │  HANDS organ  │  │  IDENTITY organ  │
     │   :8644 (Tg)    │  │  :18789 (GW)  │  │  :3001 (A2A/MCP) │
     └────────┬────────┘  └───────┬───────┘  └────────┬────────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │ A2A
                       ┌──────────▼──────────┐
                       │   arifOS KERNEL      │
                       │   :8088 (Python)     │
                       │                      │
                       │  F1-F13 Floors       │
                       │  Session / Identity  │
                       │  Judge / Vault /     │
                       │  Capability Graph    │
                       └──────────┬───────────┘
                                  │ MCP transport
            ┌─────────────────────┼─────────────────────┐
            │                     │                     │
   ┌────────▼────────┐  ┌─────────▼─────────┐  ┌───────▼────────┐
   │  GEOX (py)      │  │  WEALTH (py/node) │  │  WELL (py)     │
   │  EARTH organ    │  │  CAPITAL organ    │  │  VITALITY organ │
   │  :8081          │  │  :18082           │  │  :18083         │
   └────────┬────────┘  └─────────┬─────────┘  └───────┬────────┘
            │                     │                     │
            └─────────────────────┼─────────────────────┘
                                  │
                       ┌──────────▼──────────┐
                       │    A-FORGE (ts)      │
                       │    EXECUTE organ     │
                       │    :7071 / :7072     │
                       │                      │
                       │  4-Layer Forge Gate  │
                       │  plan → dry-run →    │
                       │  approve → execute   │
                       └──────────┬───────────┘
                                  │
                       ┌──────────▼──────────┐
                       │     VAULT999        │
                       │     IMMUTABLE        │
                       │                      │
                       │  outcomes.jsonl      │
                       │  Hash-chained        │
                       │  Append-only         │
                       └──────────────────────┘

EDGE AGENTS (MCP clients — connect THROUGH kernel, NOT above it):
  Claude Code  — builder organ (governed harness, DeepSeek v4-pro)
  OpenCode     — forge worker (governed harness, MiMo v2.5-pro)
  OpenClaw GW  — gateway operator (TS, port 18789)
```

> **Public surface split (repo-attested):** this repo's cockpit build is published as a static Pages site at `arif-fazil.com` via `.github/workflows/pages.yml`. The live AAA gateway surface is `aaa.arif-fazil.com`, reverse-proxied to localhost `:3001`.

---

## LAYER SEPARATION

### Sovereignty Layer
| Entity | Substrate | Role |
|--------|-----------|------|
| **Arif** | Human | F13 SOVEREIGN — absolute veto, final judge |

### Identity & Interface Layer
| Organ | Port | Substrate | Role |
|-------|------|-----------|------|
| **Hermes** | :8644 | Python | MIND — ASI cognitive relay, Telegram interface, memory orchestration |
| **OpenClaw** | :18789 | TypeScript | HANDS — AGI transport router, envelope broker, tool gateway |
| **AAA** | :3001 | TypeScript | IDENTITY — A2A/MCP gateway origin, agent registry, operator UX; cockpit build is published separately as Pages |

### Governance Layer
| Organ | Port | Substrate | Role |
|-------|------|-----------|------|
| **arifOS** | :8088 | Python | LAW — F1-F13 floors, session init, judge deliberation, vault seal, capability graph, interrupt routing |

### Domain Intelligence Layer
| Organ | Port | Substrate | Role | `domain_law` |
|-------|------|-----------|------|--------------|
| **GEOX** | :8081 | Python | EARTH — seismic, petrophysics, basin, prospect (Physics9-bounded) | `NATURAL_LAW` |
| **WEALTH** | :18082 | Python/Node | CAPITAL — NPV, IRR, EMV, conservation, flow, entropy | `CAPITAL_LAW` |
| **WELL** | :18083 | Python | VITALITY — human readiness, fatigue, dignity, homeostasis (REFLECT_ONLY) | `SUBSTRATE_LAW` |

> **Domain contrast (Math · Physics · Code · MCP flow):** [`DOMAIN_ORGAN_CONTRAST.md`](./DOMAIN_ORGAN_CONTRAST.md) — orthogonal axes, live tool contracts, agentic handoffs.  
> **Architecture seal v2026.07.15:** [`ARIFOS_MCP_ARCHITECTURE_v2026.07.15.md`](./ARIFOS_MCP_ARCHITECTURE_v2026.07.15.md) — Foundations · Organs · Contrast · READMEs · Flow · 999 SEAL.

### Execution Layer
| Organ | Port | Substrate | Role |
|-------|------|-----------|------|
| **A-FORGE** | :7071/:7072 | TypeScript | EXECUTE — 4-layer forge gate, engineering actuator |

### Immutable Memory Layer
| Organ | Location | Substrate | Role |
|-------|----------|-----------|------|
| **VAULT999** | `/root/VAULT999/outcomes.jsonl` | JSONL on disk | MEMORY — append-only, hash-chained, sealed truth |

---

## SUBSTRATE RATIONALE

### Why Python for MIND + LAW
- Symbolic reasoning, numeric computation, REPL-grade execution
- Multi-model orchestration, memory graph traversal
- Hermes AIAgent embed pattern: "brain mode" inside Python apps
- arifOS: FastMCP + FastAPI + Pydantic schema enforcement

### Why TypeScript for HANDS + EXECUTE
- JSON-native, HTTP/WebSocket-native, schema-first
- Envelope routing, tool brokering, multi-tenant gateway
- OpenClaw: npm ecosystem, @openclaw/acpx protocol
- A-FORGE: 4-layer forge gate in TypeScript, 77 MCP tools

### Why Python for Domain Intelligence
- Scientific computing stack: numpy, scipy, segyio, lasio
- Physics9 boundary enforcement, petrophysical computation
- Capital/financial modeling, wellness metric computation

### Why TypeScript + Python for IDENTITY
- AAA: React 19 cockpit + Express 5 A2A gateway (TypeScript)
- Agent card registry, federation envelope validation
- Constitutional core in Python (pre_forge_gate, citation_provenance)

---

## CONSTITUTIONAL BOUNDARIES

### Authority Rule
No organ may seal without arifOS. Only 888_JUDGE → 999_VAULT emits seals.
No organ may self-authorize mutation. Engineering requires arifOS SEAL → A-FORGE execute.

### Boundary Rule
- arifOS judges — never mutates
- A-FORGE executes — never legislates
- GEOX/WEALTH/WELL compute — never decide
- Hermes relays — never seals
- OpenClaw routes — never adjudicates
- AAA displays — never adjudicates
- VAULT999 remembers — never rewrites

### Substrate Rule
Agents (Claude Code, OpenCode) are governed MCP clients at the edge.
They connect THROUGH the kernel, not above it.
They are NOT organs — they are governed instruments bound to organs.

### F13 Absolute
Arif's veto is final. No autonomous loop without his say.
The kernel enforces. The sovereign decides.

---

## AGENT-ORGAN DISTINCTION

A common category error confuses **agents** with **organs**.

| Layer | Examples | Characteristics |
|-------|----------|----------------|
| **Organs** | arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA, VAULT999 | Always-on systemd services, MCP servers, constitutional roles |
| **Agents** | Claude Code, OpenCode, Hermes (runtime), OpenClaw (runtime) | Governed MCP clients, session-bound, connect through kernel |

Agents sit at the **edge** of the federation, not above the kernel.
The kernel is the hub — every agent connects through :8088.

---

## COGNITIVE LOOP (000 → 999)

| Stage | Code | Tool | Organ |
|-------|------|------|-------|
| INIT | 000 | `arif_session_init` | arifOS |
| OBSERVE | 111 | `arif_sense_observe` | arifOS |
| EVIDENCE | 222 | `arif_evidence_fetch` | arifOS |
| REASON | 333 | `arif_mind_reason` | arifOS → Hermes |
| COMPOSE | 444r | `arif_reply_compose` | arifOS → Hermes |
| ROUTE | 555 | `arif_kernel_route` | arifOS |
| MEMORY | 555m | `arif_memory_recall` | arifOS |
| HEART | 666 | `arif_heart_critique` | arifOS |
| MEASURE | 777 | `arif_ops_measure` | arifOS |
| JUDGE | 888 | `arif_judge_deliberate` | arifOS |
| FORGE | 010 | `arif_forge_execute` | arifOS → A-FORGE |
| SEAL | 999 | `arif_vault_seal` | arifOS → VAULT999 |

---

*Sealed 2026-06-22 under F13 SOVEREIGN.*
*Supersedes: all ad-hoc organ diagrams, Copilot drafts, and non-canonical agent maps.*
*Canonical location: `/root/AAA/docs/FEDERATION_ORGAN.md`*

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
