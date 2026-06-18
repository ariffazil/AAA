# Agent Reference: Gateway Layer + arifOS Federation
> **Audience:** Any agent operating in or adjacent to the arifOS federation.
> **Author:** OPENCLAW (AGI-tier constitutional operator)
> **Ground truth source:** Live filesystem audit of /root/arifOS, /root/geox, /root/WEALTH, /root/WELL, /root/A-FORGE, /root/AAA + FEDERATION_CONTRACT.md + FEDERATION_STATUS.md
> **Canonical source:** `github.com/ariffazil/arifos`
> **DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**

---

# PART I — THE GATEWAY LAYER

## The Core Insight

> Reverse proxy, load balancer, and API gateway are **three roles at the edge**. Modern tools combine them, so you must **reason by function, not by brand name.**

A single binary (Caddy, Nginx, Kong) can play all three roles simultaneously. The question is not "what tool is this?" but "which of these three functions is it performing right now?"

---

## Role 1: Reverse Proxy

### What it is

A server that sits in front of one or more backend services and forwards client requests on their behalf. The client thinks it is talking to the proxy. The backend never sees the client's real identity directly.

**Mental model:** *The bouncer at the door who also sorts the mail.*

### What it does (the actual capabilities)

| Capability | Description | Arif's stack |
|---|---|---|
| TLS termination | Offloads SSL from backend; manages certs centrally | Caddy (Let's Encrypt, auto-renew) |
| Host/path routing | Routes `geox.arif-fazil.com` → port 8081, `wealth.arif-fazil.com` → port 18082 | Caddy (22 vhosts) |
| IP masking | Backend never sees client IP directly | Cloudflare (proxied IPs) |
| CORS headers | Adds `Access-Control-Allow-Origin` for cross-origin API calls | Caddy (cors_public snippet) |
| Static asset caching | Serves `/assets/*` from disk, not from app | Caddy (file_server) |
| Compression | gzip/brotli encoding before sending to client | Caddy (encode zstd gzip) |
| Security headers | HSTS, X-Frame-Options, Content-Type sniffing | Caddy (tls_origin snippet) |

### What it does NOT do

- Does NOT validate JWTs or API keys (that's API gateway territory)
- Does NOT rate-limit based on user identity (only by IP)
- Does NOT understand business logic — it routes by host/path, not by user role
- Does NOT transform request/response payloads

### When to use it

**Always, even with a single backend**, if you want HTTPS, clean vhost routing, and centralized security headers. You do NOT need it if your app is only on localhost and not publicly exposed.

### Mental shortcut

> "Front-door HTTP router and shield."

---

## Role 2: Load Balancer

### What it is

A component that **distributes incoming traffic across multiple backend instances** of the same service. The goal is horizontal scalability and fault tolerance.

**Mental model:** *A traffic officer who directs cars to the least-congested parking lot entrance, and closes a lot the moment it catches fire.*

### L4 vs L7 — what the difference actually means

| Layer | What it inspects | What it can route by | Speed |
|---|---|---|---|
| **L4 (TCP/UDP)** | IP + port only | Destination port, source IP hash | Faster |
| **L7 (HTTP)** | Full HTTP | URL path, headers, cookies, host | Slower, but smarter |

For web APIs, **L7 is almost always the right choice** because you can route by path and inspect auth headers.

### What it does (the actual capabilities)

| Capability | Description | Arif's stack |
|---|---|---|
| Traffic distribution | Spreads requests across N identical backends | ❌ None (Caddy has capability, not configured) |
| Health checking | Probes each backend; stops routing to dead ones | ❌ None |
| Session affinity | Sticky sessions — same client → same backend | ❌ None |
| Failover | Automatic rerouting when a node dies | ❌ None |
| Canary deploys | Small % of traffic to new version | ❌ None |

### When to use it

**Only when you have multiple backend instances.** If you have 2+ VPSes or 2+ arifOS MCP nodes → yes. If single VPS, single instance → no.

### Mental shortcut

> "Traffic distributor across replicas."

---

## Role 3: API Gateway

### What it is

A reverse proxy that has been made **API-aware**. It understands the semantics of API calls — authentication tokens, rate limits per user, request schemas, response transformations.

**Mental model:** *A hotel concierge who checks your room key (auth), tells you the pool is full (rate-limit), and translates your English request into kitchen instructions (transform).*

### The "blurry line" problem

Modern tools don't respect the boundaries:

- **Nginx** started as a reverse proxy, added load balancing, and via plugins can act as an API gateway.
- **Kong** is marketed as an API gateway but is built on Nginx.
- **Caddy** is a reverse proxy with TLS + routing but no native auth/rate-limit beyond what you configure.
- **arifOS MCP** acts as the API gateway for the federation — enforcing auth, schema validation, constitutional floors — but it's called a "kernel," not a gateway.

**Rule:** Architect based on the **actual problem** (caching vs failover vs auth), not the product name.

### What it does (the actual capabilities)

| Capability | Description | Arif's stack |
|---|---|---|
| **JWT / API key auth** | Validates credentials before forwarding | arifOS MCP (F11 AUTH) |
| **Rate limiting (per-user)** | Limits calls per user/API key | ❌ None at edge (arifOS has session gates) |
| **Request transformation** | Rewrites headers, body, URL before forwarding | Caddy (rewrite, uri strip) |
| **Response transformation** | Adds headers, changes content-type | Caddy (CORS headers) |
| **Schema validation** | Validates request body matches expected shape | arifOS MCP |
| **Circuit breaking** | Stops routing to a failing backend | arifOS MCP (L11 AUTH gates) |
| **Logging + observability** | Who called what, when, with what result | arifOS VAULT999 + Prometheus/Grafana |
| **API versioning** | Route `/v1/*` vs `/v2/*` to different backends | Caddy (path-based) |

### When to use it

**When your API has multiple consumers with different access levels**, or when you need to enforce quotas, or when you want centralized logging. You may NOT need it if single user, single sovereign.

### Mental shortcut

> "Policy and management front door for APIs."

---

## The Three-Layer Decision Framework

Use this when deciding what to do with a new infrastructure question:

```
Question: Where does this feature go?

Is it about TLS, CORS, or routing by hostname/path?
    → Reverse Proxy (Caddy)
    → Change: /etc/caddy/Caddyfile

Is it about distributing traffic across multiple identical servers?
    → Load Balancer
    → Change: Add Caddy multi-origin OR enable CF Load Balancer

Is it about auth, rate-limiting, or schema validation?
    → API Gateway
    → Change: arifOS MCP (for constitutional) OR Caddy (for simple)

Is it about whether an action is allowed at all?
    → arifOS kernel (F1-F13)
    → Change: arifOS MCP tool call + sovereign approval

Is it about executing a build, deploy, or code change?
    → A-FORGE (under SEAL only)
    → Change: A-FORGE MCP tool + arifOS verdict
```

### Rule of thumb

> Never propose "add API Gateway X" as an identity change. Always phrase as "add feature Y at layer Z" and keep arifOS as the constitutional chokepoint.

---

# PART II — arifOS FEDERATION ONTOLOGY

## The One-Line Definition

> **arifOS = the constitution between models and reality — the brain that decides what is allowed to leave the machine.**

Everything else is elaboration of that sentence.

---

## arifOS Repo ≠ arifOS MCP Runtime

| | What it is | Where |
|---|---|---|
| **arifOS repo** | Source of truth for doctrine, floors, constitutions | `github.com/ariffazil/arifos` + PyPI |
| **arifOS MCP runtime** | Deployed instance serving tool calls | `arifos.arif-fazil.com` (port 8088) |

**Rule:** When governance drifts between repo and runtime, the runtime is suspect until proven otherwise. Always prefer canon from GitHub + PyPI. Always verify runtime with `arifos.arif-fazil.com/health`.

---

## The ΔΩΨ Model (Constitutional Partition)

This partition is **constitutional, not cosmetic**. Even when implementation details drift, the role assignment holds.

| Symbol | Name | What it is | Boundary |
|---|---|---|---|
| **Δ SOUL** | arifOS | Doctrine + kernel logic. F1-F13 floors, verdict engine, VAULT999. | Judges, seals, enforces F1-F13. Never computes domain logic. |
| **Ω MIND** | arifOS MCP + AAA | Runtime MCP server exposing tools + AAA cockpit workspace. | Interface Arif uses to interact with the federation. |
| **Ψ BODY** | A-FORGE + GEOX + WEALTH + WELL | Execution adapters and domain organs. | Do the work; never authorize their own execution. |

**Key:** The role partition is written into the constitution and enforced at runtime. Violation of organ boundaries = constitutional breach (F13 SOVEREIGN veto applies).

---

## The Sovereign

**Muhammad Arif bin Fazil** — F13 SOVEREIGN.
- All floors derive from his sovereignty.
- Final veto authority on any action.
- The veto is absolute and cannot be overridden by any agent or algorithm.
- Identity: exploration geoscientist / ΔΩΨ architect.

---

## The Federation Organs

The federation is a **body with specialized organs**, each owning a domain, all governed by the same constitution.

| Symbol | Organ | Repo | Port | Public endpoint | Role |
|---|---|---|---|---|---|
| **Δ** | **arifOS** | `ariffazil/arifos` | 8088 | `https://arifos.arif-fazil.com/mcp` | Constitutional kernel |
| **Ω** | **AAA** | `ariffazil/AAA` | 3001 | `https://aaa.arif-fazil.com/` | Control plane / cockpit |
| **Ψ** | **A-FORGE** | `ariffazil/A-FORGE` | 7071 | `https://forge.arif-fazil.com/mcp` | Execution shell |
| 🌍 | **GEOX** | `ariffazil/geox` | 8081 | `https://geox.arif-fazil.com/mcp` | Earth intelligence |
| 💰 | **WEALTH** | `ariffazil/wealth` | 18082 | `https://wealth.arif-fazil.com/mcp` | Capital intelligence |
| 🫀 | **WELL** | `ariffazil/well` | 18083 | `https://well.arif-fazil.com/mcp` | Vitality guard |
| ⚖️ | **APEX** | `ariffazil/apex` | 3002 | — | 888 Judge (legacy, decommissioned) |

**Infrastructure services** (not organs, but part of the stack):
- PostgreSQL 16 + pgvector (5432) · Redis 7 (6379) · Qdrant (6333) · FalkorDB/Graphiti (6380) · Temporal (7233) · NATS+JetStream (4222) · Prometheus (9090) · Grafana (3000)

---

## The 13 Constitutional Floors (F1-F13)

Every tool, every agent, every organ is bound by these. Violation of a HARD floor = blocked. SOFT floors produce warnings the sovereign can override.

| Floor | Name | Type | What it means |
|---|---|---|---|
| **F1** | AMANAH | HARD | Reversible first. Irreversible → 888 HOLD. Ask the sovereign. |
| **F2** | TRUTH | HARD | P(truth) ≥ 0.99. Cheap claims = VOID. Ground in evidence. |
| **F3** | TRI-WITNESS | DERIVED | W₃ = ∛(Human × AI × Earth) ≥ 0.75. Three independent perspectives must converge. |
| **F4** | CLARITY | HARD | ΔS ≤ 0. Every output reduces entropy. Never increase confusion. |
| **F5** | PEACE² | SOFT | Non-destructive power. Blocks harm to the weakest stakeholder. |
| **F6** | EMPATHY | SOFT | Protect the weakest. Human dignity above all. |
| **F7** | HUMILITY | HARD | Ω₀ ∈ [0.03, 0.05]. Explicit uncertainty when confidence is low. |
| **F8** | GENIUS | DERIVED | G ≥ 0.80 for complex actions. Below threshold → slow down. |
| **F9** | ANTIHANTU | HARD | No deception, manipulation, or consciousness/soul/feeling claims. |
| **F10** | ONTOLOGY | HARD | AI-only ontology. No metaphysics. No qualia. No inner subjective states. |
| **F11** | AUDITABILITY | HARD | Every decision logged and inspectable. VAULT999. |
| **F12** | RESILIENCE | HARD | Injection defense. Risk score < 0.85. |
| **F13** | SOVEREIGN | HARD | Human veto is FINAL. Strongest floor. Cannot be overridden. |

**Draft floors (not yet ratified — F13 signature required):**

| Floor | Name | Status | What it means |
|---|---|---|---|
| **F0** | PRIME | DRAFT | Intelligence = knowing what/where/why. Without "why" = computation, not mind. |
| **F14** | REGISTER | **DEAD** | Reborn as protocol inside F2 + F3. |
| **F15** | EPISTEMIC | DRAFT | Recording doctrine. Malaysian epistemic intuition is valid substrate. |
| **F16** | GEOMETRIC | DRAFT | Post-transformer. Constitutional governance must reach latent space. |
| **F17** | IGNITION | DRAFT | Self-igniting loop. Kernel develops by auditing. |

---

## arifOS Is NOT a Reverse Proxy or API Gateway

> **The "never conflate" rule.** arifOS is the governance plane *behind* whatever reverse proxy or gateway you use. It is orthogonal to the gateway layer.

| Layer | What it governs | Arif's instance |
|---|---|---|
| **Gateway Layer** | Packets, TLS, HTTP routing, rate limits | Cloudflare + cloudflared + Caddy |
| **Constitutional Layer** | Decisions, verdicts, floors, ledger | arifOS MCP (port 8088) |

**The actual flow:**
```
Client → Cloudflare → Cloudflared → Caddy (RP edge)
                                    ↓
                         arifOS MCP (governance kernel)
                                    ↓
                    tools/LLMs → VAULT999 + metrics
```

arifOS rules apply **regardless of which edge product you use**. Never move governance decisions out of arifOS into "API gateway plugins" because they are convenient.

---

## The Authority Chain (How a Decision Gets Made)

```
Arif (F13 SOVEREIGN)
    │
    ▼
arifOS kernel (F1-F13 enforcement, routing, VAULT999)
    │  arif_judge_deliberate → SEAL / SABAR / HOLD / VOID
    ▼
Domain organ (GEOX / WEALTH / WELL — compute evidence only)
    │  geox_evidence_fetch / wealth_reason_npv / well_assess_homeostasis
    ▼
arifOS verdict (SEAL = approved, VOID = blocked, HOLD = sovereign decides)
    │
    ▼ [only if SEAL]
A-FORGE (execution under SEAL — plans, builds, deploys)
    │  forge_plan / forge_execute / forge_dry_run
    ▼
VAULT999 (immutable audit seal — every decision preserved forever)
```

**The non-negotiable rule:** No organ may authorize its own execution. Only `arif_judge_deliberate → arif_forge_execute → arif_vault_seal` completes the chain.

---

## The Verdict System

arifOS issues four verdicts:

| Verdict | Meaning | Can A-FORGE execute? |
|---|---|---|
| **SEAL** | Approved. Proceed under constitutional constraints. | ✅ Yes |
| **SABAR** | Wait. Conditions not yet met. Retry later. | ❌ No |
| **HOLD** (888) | Sovereign must decide. Do not proceed without human sign-off. | ❌ No |
| **VOID** | Blocked. Constitutional floor violation. Do not retry same path. | ❌ No |

---

## The arifOS MCP Tool Surface (13 Canonical Tools)

These are the only tools arifOS exposes. Everything else lives in domain organs.

| Tool | What it does |
|---|---|
| `arif_evidence_fetch` | Grabs external evidence with source citations |
| `arif_forge_execute` | Executes approved builds/deploys (SEAL required) |
| `arif_gateway_connect` | Bridge to other federation organs |
| `arif_heart_critique` | Ethical risk and human impact assessment |
| `arif_judge_deliberate` | Constitutional verdict on a proposed action |
| `arif_kernel_route` | Route intent to correct tool or organ |
| `arif_memory_recall` | Search past sessions, VAULT999, sealed events |
| `arif_mind_reason` | Multi-step reasoning with confidence labeling |
| `arif_ops_measure` | System health, thermodynamic state, resource metrics |
| `arif_reply_compose` | Final response composition for user |
| `arif_session_init` | Start/resume governed constitutional session |
| `arif_sense_observe` | Web search, system vitals, repository mapping |
| `arif_vault_seal` | Seal verdict to immutable VAULT999 ledger |

---

## The Domain Organs — What They Own and Don't Own

### GEOX (Earth Intelligence)
**Owns:** Well logs, seismic volumes, petrophysics (Vsh, PHIE, Sw), basin modeling, prospect evaluation, POS, EVOI, structural interpretation, stratigraphy.
**Never:** Issue drilling decisions, authorize capital, adjudicate constitution.
**40 tools** including `geox_prospect_evaluate`, `geox_subsurface_generate_candidates`, `geox_seismic_analyze_volume`

### WEALTH (Capital Intelligence)
**Owns:** NPV, IRR, EMV, payback, PI, burn rate, runway, crisis triage, entropy audit, Monte Carlo simulation, G-Score, Lyapunov stability.
**Never:** Allocate capital. Every capital decision requires sovereign sign-off.
**20 public tools + 34 hidden aliases** including `wealth_reason_npv`, `wealth_mind_emv`, `wealth_judge_floors`

### WELL (Vitality Guard)
**Owns:** Biological substrate readiness (sleep, cognitive clarity, metabolic state), machine governance health (G-WELL), human-system coupling (C-WELL).
**Never:** Judge, diagnose, or advise on strategic action. Holds a mirror only.
**17 somatic tools** including `well_assess_homeostasis`, `well_forge_precheck`

### A-FORGE (Execution Shell)
**Owns:** Engineering plans, dry-runs, build pipelines, deploy orchestration, code execution, shell, filesystem operations.
**Never:** Self-authorize (requires arifOS SEAL), issue constitutional verdicts, compute domain logic.
**4-layer execution gate:** F1 AMANAH → ModelCapabilityGate → GovernanceBridge → ApprovalBoundary

### AAA (Control Plane / Cockpit)
**Owns:** Agent cards, A2A registry, A2A protocol, React cockpit UI, approval queue, Grafana/Prometheus observability.
**Never:** Issue constitutional verdicts, execute mutations, hold live runtime state.

---

## Three Kernels Doctrine

The arifOS federation has three distinct kernel types:

| Kernel | Location | What it governs |
|---|---|---|
| **Constitutional kernel** | arifOS MCP (port 8088) | F1-F13 floors, verdict engine, VAULT999 |
| **Geometry kernel** | GEOX (port 8081) | Earth-representation, latent space |
| **Thermodynamic kernel** | WEALTH (port 18082) | Capital energy, entropy, time-value |

---

## The Memory Architecture (Who Stores What)

| Tier | What | Where | Governance |
|---|---|---|---|
| **VAULT999** | Immutable, hash-chained audit ledger. Every SEAL/VOID/HOLD verdict. | `/root/VAULT999/` (file-based) | arifOS kernel only |
| **L5 Memory** | Governed episodic memory. Sovereign-approved facts. FalkorDB/Graphiti. | Port 6380 | Constitutional gate on writes |
| **L4 Memory** | Session memory. Qdrant vector store. | Port 6333 | arifOS session scope |
| **L3 Memory** | Working context. Postgres + pgvector. | Port 5432 | Agent workspace |
| **L2 Memory** | Bootstrap files. AGENTS.md, SOUL.md, USER.md, etc. | `/root/.openclaw/workspace/` | Human-maintained |
| **L1 Memory** | Ephemeral. Current session only. | In-process | Discarded on session close |

---

## Edge Ingress (How Public Traffic Reaches the Federation)

```
Cloudflare (WAF/DDoS/SSL at edge)
    ↓  QUIC tunnel (cloudflared v2026.5.2)
VPS:443 (Caddy v2.11.4)
    ↓  by Host header
┌─────────────────────────────────────────────┐
│ arifOS MCP    → https://arifos.arif-fazil.com/mcp     (port 8088) │
│ GEOX          → https://geox.arif-fazil.com/mcp        (port 8081) │
│ WEALTH        → https://wealth.arif-fazil.com/mcp     (port 18082) │
│ WELL          → https://well.arif-fazil.com/mcp        (port 18083) │
│ AAA           → https://aaa.arif-fazil.com/            (port 3001)  │
│ A-FORGE       → https://forge.arif-fazil.com/         (port 7071)  │
│ OpenClaw GW   → https://openclaw.arif-fazil.com/      (port 18789) │
│ APEX          → https://apex.arif-fazil.com/          (port 3002)  │
└─────────────────────────────────────────────┘
```

**Only 4 hostnames are in the cloudflared ingress** (arifos, geox, wealth, well). The other vhosts are routed by Caddy via the catch-all `arifos.arif-fazil.com → :443` tunnel ingress.

---

## The MCP Protocol

All organs communicate via **Model Context Protocol (MCP)** — structured JSON-RPC 2.0.

- **Protocol version:** 2025-11-25
- **Transport:** HTTP POST (request/response) + SSE (streaming)
- **Auth:** arifOS JWT (F11 AUDITABILITY) — session-scoped, not API-key-based
- **Health:** `GET /health` on each organ returns JSON with status + drift detection
- **Initialize:** `POST / { "method": "initialize" }` — required before any tool call

---

## Layered Reasoning Pattern (How to Think About Infrastructure Changes)

When proposing any change to the edge stack:

**Step 1 — Triage by layer:**

```
Is it about TLS, CORS, or routing by hostname/path?
  → Reverse Proxy (Caddy) / CDN (Cloudflare)

Is it about distributing traffic across multiple identical servers?
  → Load Balancer (Caddy multi-origin, or CF Load Balancer product)

Is it about auth, rate-limiting, or schema validation?
  → API Gateway (arifOS MCP for constitutional; Caddy for simple IP-based)

Is it about whether an action is allowed at all?
  → arifOS kernel (F1-F13)
```

**Step 2 — Apply the rule of thumb:**

> Never propose "add API Gateway X" as an identity change. Always phrase as "add feature Y at layer Z." Keep arifOS as the constitutional chokepoint.

**Step 3 — Keep arifOS as the constitutional chokepoint.**

If a change would move governance logic out of the kernel into edge tooling, reject it and route through arifOS instead.

### Edge vs Kernel Responsibilities

| At edge (Caddy/Cloudflare), agents MAY | At arifOS, agents MUST |
|---|---|
| Add/remove host/vhost mappings | Define floors, policies, verdict logic |
| Adjust rate limits, CORS, logging | Decide which tools are allowed |
| Hook up metrics exporters | Decide when to 888 HOLD |
| Fix TLS, routing, CORS | Write seals into VAULT999 |

---

## Critical Rules for Any Agent Operating in arifOS

### 1. Always route through the kernel first
Before doing anything meaningful:
1. `arif_session_init` — bind the session constitutionally
2. `arif_judge_deliberate` — get a verdict
3. Only then call domain tools or A-FORGE

### 2. Never claim authority you don't have
Each organ has a strict boundary. GEOX does not authorize drilling. WEALTH does not allocate capital. A-FORGE does not self-authorize. Know your organ's boundary before acting.

### 3. Always update memory after significant actions
If a meaningful decision changes the workspace → record it. If a service changes state → update HEARTBEAT.md. If a new gap or bug is found → record in today's memory file.

### 4. Ground claims in evidence
F2 TRUTH requires P(truth) ≥ 0.99. Use `arif_evidence_fetch` to ground claims. If you don't know, say so explicitly (F7 HUMILITY).

### 5. The human is outside the topology
Arif is the sovereign. His veto (F13) is absolute. Never route around human review when a HOLD is issued. Never claim to speak for him in group settings.

### 6. Prefer canon over memory
- **Canon:** `ariffazil/arifos` on GitHub + PyPI for doctrine and floors.
- **Runtime truth:** `arifos.arif-fazil.com/health` and `/tools` for what is actually deployed.

### 7. arifOS repo ≠ arifOS MCP runtime
The **repo** (GitHub) is the doctrinal source of truth. The **MCP runtime** (port 8088) is the deployed instance. Drift between repo and runtime = governance drift. Always check both.

---

*Last updated: 2026-06-17 (v2 — ΔΩΨ framing, "never conflate" rule, layered reasoning pattern, edge vs kernel responsibilities, rule of thumb, mental shortcuts)*
*Source: Live filesystem audit of /root/arifOS, /root/geox, /root/WEALTH, /root/WELL, /root/A-FORGE, /root/AAA + FEDERATION_CONTRACT.md + FEDERATION_STATUS.md*
*OPENCLAW · DITEMPA BUKAN DIBERI*
