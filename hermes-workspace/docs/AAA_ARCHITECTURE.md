# AAA Architecture — Arif's Agent Architecture
> **Operational Layer of arifOS**

*Forged, Not Given — Ditempa Bukan Diberi*

---

## Overview

AAA (Arif's Agent Architecture) is the **operational spine of arifOS**. It connects external agents to arifOS's core governance, orchestrating multi-agent workflows while ensuring all actions are constitutionally governed.

AAA fulfills **three primary roles** within the arifOS ecosystem:

| Role | Description |
|------|-------------|
| **Control-Plane Seed** | Provides the initial identity, constitution, and governance defaults for every agent in the federation |
| **A2A Gateway** | Acts as the entry point for Agent-to-Agent (A2A) communication and orchestration |
| **Governance Runtime Adapter** | Analyzes each request to decide if and how it should be executed (direct, via Kernel, or held for human) |

---

## Canonical Definition

> AAA is the operational spine of arifOS: it seeds agents, orchestrates negotiation through A2A, and intermediates between intent and constitutional judgment.

AAA does **not**:
- Execute domain tasks or make final judgments
- Generate content or answers
- Store long-term data (beyond audit logs)
- Create or modify policy

---

## 1. Control-Plane Seed (Bootstrap)

AAA's first role is to serve as the **genesis for agent governance**.

### What it provides

- **Agent Identity Template** — A canonical agent identity (`.well-known/agent.json`) that new agents can clone or reference
- **Constitution & Governance Defaults** — Baseline F1–F13 Floor parameters; every agent starts with the same "laws of physics"
- **Bootstrap Procedure** — New agents call `AAA.get_bootstrap()` to retrieve their unique ID, known agents, MCP endpoints, and constitution version hash

### Invariants

- AAA as a seed **never alters the canon** — it only distributes it
- There is exactly one source of truth for the constitution and core configs
- New agents must not override these on their own — AAA prevents divergence

### Non-Goal

The seed is not a dynamic service. It doesn't decide policies on the fly or generate new identities. It ensures **consistency and availability** of the governance blueprint only.

---

## 2. A2A Gateway (Orchestration & Messaging)

**Live endpoint:** `https://aaa.arif-fazil.com/a2a`

The gateway is the **traffic controller** for the agent federation.

### Responsibilities

| Responsibility | Detail |
|----------------|---------|
| **Authentication** | Bearer token or API key required on every request. Invalid/missing tokens return `401 Unauthorized` |
| **Schema Validation** | All incoming JSON is checked against the A2A message schema before any processing |
| **Message Routing** | Based on `recipient.agent_id`, routes to the appropriate internal agent |
| **Orchestration** | Breaks complex tasks into sub-tasks, delegates, tracks pending state |
| **Statelessness** | No long-term sessions; minimal in-memory stores (nonce cache, task state only) |

### Key Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/a2a` | GET | No | Service info and endpoint map |
| `/a2a/health` | GET | No | Health check with kernel status |
| `/a2a/.well-known/agent.json` | GET | No | Agent card (capabilities, skills, auth schemes) |
| `/a2a/message/send` | POST | **Yes** | Send a task message (JSON-RPC) |
| `/a2a/message/stream` | POST | **Yes** | SSE streaming for long-running tasks |
| `/a2a/tasks/:taskId` | GET | **Yes** | Get task status |
| `/a2a/tasks/:taskId/cancel` | POST | **Yes** | Cancel a task |
| `/a2a/tasks/:taskId/subscribe` | GET | **Yes** | Subscribe to task events via SSE |

### Invariants

- The gateway **never executes domain logic** or "thinks" on behalf of agents
- It only parses, authenticates, validates, and routes
- All failure responses are **structured JSON-RPC errors** — no silent drops

### Failure Modes

- Unreachable internal agent → returns error upstream (never silently drops)
- Gateway parse failure → `400` with structured error (no internal stack traces)
- Auth failure → `401` (no information leakage about why)

---

## 3. Governance Runtime Adapter (Risk-Based Router)

The adapter is AAA's **decision center**. It sits between the gateway and execution layers.

### Risk Assessment & Routing

| Risk Level | Criteria | Routing Path |
|------------|----------|--------------|
| **LOW** | Simple data retrieval, read-only, noFloor impact | Direct to **MCP** (stateless execution) |
| **MEDIUM** | Content generation, judgment calls, Floor exposure | Via **arifOS Kernel** for constitutional check |
| **HIGH** | Legal, safety, ethical implications, ambiguous intent | **888 HOLD** — human (888 Judge) must review |

### Routing Decision Rules

```
IF tool IN safe_tools清单 AND no floor impact:
    → MCP_direct_execution()
ELIF any floor exposure OR content generation:
    → kernel.apply_floors(draft)
    IF kernel SEAL:
        → execute_and_return()
    ELSE IF kernel HOLD:
        → return_hold_notice()
ELSE:
    → trigger_888_HOLD()
```

### Invariants

- The adapter **never bypasses governance** — conservative routing is intentional
- When in doubt, route through the Kernel (extra latency is preferable to a dangerous slip)
- If the Kernel is offline → all MEDIUM/HIGH requests become HOLD (fail-safe, not fail-open)

### Fallback Behavior (Kernel Offline)

When Kernel connection is lost, AAA enters **local mode**:
- LOW-risk read operations may proceed
- All requests requiring Kernel mediation are held
- Cockpit shows `Kernel: DISCONNECTED`
- Explicit logging of degraded state

---

## End-to-End Flow (The Golden Path)

```
External Agent (e.g. Copilot)
    │ (1. Sends A2A JSON-RPC over HTTPS)
    │ Trust Boundary: AAA Gateway authenticates + validates schema
    ▼
AAA A2A Gateway (Orchestration Layer)
    ├─ Confirms sender identity and permissions
    ├─ Parses message (intent, target, payload)
    ├─ Initiates internal collaboration if needed
    └─ Invokes Governance Adapter for routing decision
    ▼
AAA Governance Adapter (Runtime Router)
    ├─ LOW RISK  → MCP direct execution
    ├─ MEDIUM    → arifOS Kernel (F1–F13 floors)
    └─ HIGH      → 888 HOLD (human review)
    ▼
Execution Layer
    ├─ MCP Tool Execution (if approved)
    └─ Constitutional Kernel (if invoked)
        ├─ 999 SEAL → proceed
        └─ 888 HOLD → pause for human
    ▼
Outcome Delivery
    ├─ If executed → result returned via AAA Gateway
    └─ If held → hold notice returned via AAA Gateway
    ▼
External Agent receives result or hold notification
```

---

## Trust Boundaries

### Boundary 1: AAA Gateway Ingress
- **All** incoming messages must pass auth check and schema validation before any processing
- This prevents unauthorized or malformed requests from ever reaching internal agents

### Boundary 2: AAA ↔ arifOS Kernel
- Kernel is a **protected component** that AAA calls but does not control
- AAA handles Kernel unavailability gracefully (see fallback behavior above)

### Boundary 3: AAA ↔ MCP Layer
- MCP tools are treated as **potentially untrusted**
- All MCP responses are subject to post-checks via the Kernel
- If a tool output violates a Floor, the Kernel catches it

### Boundary 4: Human-in-the-Loop (888 Judge)
- Final authority always remains human
- AAA never overrides or bypasses a human veto — **hard invariant**
- Held requests await human decision via Cockpit or admin API

---

## The 13 Constitutional Floors (arifOS Kernel)

Floors are constraint equations enforced by the Kernel — not sequential filters.

| Floor | Name | Core Mandate |
|-------|------|-------------|
| F1 | Amanah | Sacred Trust — all actions must be reversible |
| F2 | Truth | Accuracy — citations required; uncertainty bounded Ω₀ ∈ [0.03, 0.05] |
| F3 | Tri-Witness | Consensus — DECISIONS require W³ ≥ 0.95 (Theory ∩ Constitution ∩ Manifesto) |
| F9 | Anti-Hantu | No "Soul" — prohibition of consciousness claims ("I feel", "I am") |
| F11 | Auditability | Transparency — immutable logs in VAULT999 |
| F13 | Sovereign | Override — 888 Judge maintains absolute veto power |

Full floor definitions: [arifOS Constitution](../arifOS/ROOT_CANON.yaml)

---

## Interfaces and Integration Points

### External A2A API
```
POST /a2a/message/send
Authorization: Bearer <A2A_TOKEN>
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": "task-001",
  "method": "a2a.message.send",
  "params": {
    "sender": { "agent_id": "copilot" },
    "recipient": { "agent_id": "aaa-gateway" },
    "payload": { ... },
    "nonce": "X7K9F32",
    "timestamp": 1745360400
  }
}
```

### Agent Discovery
```
GET /a2a/.well-known/agent.json
```
Returns AAA's agent card — identity, capabilities, auth schemes, skills.

### Internal Agent Bus
AAA maintains a registry of internal agent workspaces. Routing is by `recipient.agent_id`.

### MCP Interface
AAA calls MCP tools via HTTP JSON-RPC:
```
POST /mcp
{"method": "geox.interpret_las", "params": {...}}
```
Tool schemas loaded from MCP server's `/tools` endpoint.

### Kernel Governance API
```
{"method": "kernel.apply_floors", "params": {"content": "...", "floors": ["F2", "F9"]}}
```
Returns `999 SEAL` (approved) or `888 HOLD` (rejected/needs review).

### Vault-999 Logging
- Kernel writes SEAL/HOLD decisions with reasoning and hash
- AAA writes direct MCP execution events (no Kernel involvement)
- Logs are chained and regularly verified for integrity

### Human Override Channel
- Held tasks surface in Cockpit UI for 888 Judge review
- Judge resolves via Cockpit or by sending a new A2A message as the Judge agent
- Human decision is logged and immutable

---

## Security & Failure Modes

### Auth (Implemented)
- Bearer token (`Authorization: Bearer <token>`) or API key (`x-a2a-key: <key>`)
- Reject before JSON-RPC parsing — prevents method probing
- Tokens are runtime-only (env vars, not in code)

### Schema Validation (Implemented)
- Fail-closed: unknown fields → `400 Invalid Request`
- Missing required fields → `400 Invalid Request`
- Wrong types → `400 Invalid Request`

### Replay Protection (Implemented)
- Nonce + timestamp in every message
- Duplicate nonce within window → `401` (replay detected)
- Timestamp outside acceptable window → `401` (expired)
- In-memory nonce cache with 5-minute TTL
- Payload hash cache with 30-minute TTL

### Failure Mode Summary

| Failure | Response |
|---------|----------|
| Missing/bad auth | `401 Unauthorized` |
| Schema invalid | JSON-RPC `-32600 Invalid Request` |
| Timestamp expired | JSON-RPC `-32005 Timestamp outside window` |
| Nonce replay | JSON-RPC `-32004 Duplicate request detected` |
| Kernel offline | Local mode — HIGH/MEDIUM → HOLD |
| MCP timeout | Bounded error, no retry silently |
| Internal agent down | Structured error upstream |

---

## Repository Structure

```
ariffazil/AAA/
├── a2a-server/              # Standalone A2A gateway (Node.js/Express)
│   ├── server.js             # Hardened A2A server (auth, validation, routing)
│   ├── Dockerfile           # Production container image
│   └── package.json
├── src/
│   ├── Cockpit.tsx          # Read-only constitutional observatory
│   ├── App.tsx              # Entry point
│   └── components/
│       └── TrinityNav.tsx   # Navigation bar
├── docs/
│   ├── AAA_ARCHITECTURE.md  # This document
│   ├── COPILOT_STUDIO_CONNECTION.md
│   └── MCP_PAYLOADS.md
├── schemas/
│   └── mcp-openapi.yaml     # OpenAPI 3.0 spec for Copilot Studio
└── public/.well-known/
    └── agent-card.json      # A2A agent card
```

### Planned Refactors (Post-Seal)

| Component | Current State | Target State |
|-----------|--------------|--------------|
| `seed/` module | Bootstrap data embedded | Dedicated `seed/` directory with `identity.yaml`, `floors_default.yaml`, `bootstrap.py` |
| `adapter/` module | Adapter logic inlined in gateway | Isolated `adapter/router.py` with data-driven risk policies |
| `schemas/` directory | Schema validation in code | Standalone `schemas/a2a_message.json` (AJV-compatible) |
| Agent registry | Hardcoded list | `agents.yaml` config-loaded at startup |
| Risk policies | Rule-based (if/else) | Policy-driven via external config |

---

## Final Hardening Checklist (Pre-Seal)

Before declaring AAA fully **SEALed**:

- [x] Authentication gate on all `/a2a/**` endpoints
- [x] Schema validation (fail-closed, structured errors)
- [x] Replay protection (nonce + timestamp cache)
- [x] Agent card current and consistent with arifOS canon
- [ ] Governance path enforcement verified per tool/type
- [x] Kernel heartbeat monitoring (Cockpit shows `Kernel: CONNECTED/DISCONNECTED`)
- [ ] Vault-999 logging verified for all HOLD/SEAL events
- [ ] Human override mechanism tested end-to-end
- [ ] Robust error handling (tool failure, timeout edge cases)
- [ ] Documentation reflects current implementation state

---

## Public Endpoints

| Endpoint | Auth | Status |
|----------|------|--------|
| `https://aaa.arif-fazil.com/a2a` | No | LIVE |
| `https://aaa.arif-fazil.com/a2a/health` | No | LIVE |
| `https://aaa.arif-fazil.com/a2a/.well-known/agent.json` | No | LIVE |
| `https://aaa.arif-fazil.com/a2a/message/send` | **Yes** | LIVE |
| `https://aaa.arif-fazil.com/a2a/message/stream` | **Yes** | LIVE |

---

*AAA is forged, not given. Ditempa Bukan Diberi.*
