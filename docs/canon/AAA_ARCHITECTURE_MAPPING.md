# AAA Architecture Mapping — A2A, MCP, and P2P

> **Ditempa Bukan Diberi** — *Forged, Not Given* [ΔΩΨ | ARIF]
> **Status:** SOVEREIGNLY SEALED | **Layer:** ARCHITECTURAL CANON

This document maps the structural relationship between the three core communication and execution layers of the arifOS federation: **A2A (Agent-to-Agent)**, **MCP (Model Context Protocol)**, and **P2P (Peer-to-Peer Inter-Agent consensus)**.

---

## 🏛️ The Three-Layer Protocol Stack

The federation separates cognitive discovery, tool execution, and consensus safety into three distinct protocol envelopes:

```
      ┌─────────────────────────────────────────────────────────┐
      │                  A2A (Agent-to-Agent)                   │  ◄── Discovery, Streaming, &
      │          HTTPS / JSON-RPC (Ports: 3001, 18789)          │      Multi-Turn Gateways
      └────────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
      ┌─────────────────────────────────────────────────────────┐
      │            P2P (Local Inter-Agent Mesh)                 │  ◄── Low-latency consensus,
      │             Unix Sockets / NATS / Redis                 │      F1-F13 Floor Checks (<10ms)
      └────────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
      ┌─────────────────────────────────────────────────────────┐
      │             MCP (Model Context Protocol)                │  ◄── Cognitive Agent to Deep
      │               Stdio / HTTP (Port: 8088)                 │      Computational Organs
      └─────────────────────────────────────────────────────────┘
```

| Layer | Protocol | Focus | Operational Role |
|---|---|---|---|
| **A2A** | HTTP / JSON-RPC | **External Interface** | Dynamic discovery (`.well-known/agent-card.json`), auth (OAuth 2.1), multi-turn task tracking, and task streaming. |
| **P2P** | Unix sockets / NATS / Redis | **Internal Consensus** | Hot-path collaboration between cognitive agents (`333-AGI`, `555-ASI`, `888-APEX`) to run F1–F13 floor audits, issue locks, and finalize seals. |
| **MCP** | Stdio / HTTP | **Tool Boundary** | Binds cognitive reasoning to deep computational engines/organs (`GEOX`, `WEALTH`, `WELL`, `A-FORGE`). |

---

## 🧭 Layer Interactions & Lifecycle Alignment

```
[A2A Request]
     │
     ▼
[A2A Gateway] ──(P2P: Task Check)──► [888-APEX] (Verifies authorization / F1-F13)
     │                                     │
     │ (Staged: TASK_STATE_WORKING)        ├──► [SEALED] ──► Write to VAULT999
     ▼                                     ├──► [888_HOLD] ──► TASK_STATE_INPUT_REQUIRED
[333-AGI Executor]                         └──► [VOIDED] ──► TASK_STATE_FAILED
     │
     ├─(MCP Tool Calls)─► [GEOX] (LAS Eval)
     ├─(MCP Tool Calls)─► [WEALTH] (EMV Solver)
     └─(MCP Tool Calls)─► [WELL] (Vitality Check)
```

### 1. A2A: External Agent-to-Agent Gateway
*   **Focus: Agent Partnership (Stateful & Long-Lived)**
*   **Purpose:** Exposes the arifOS federation to external networks and peer agents.
*   **A2A Card Representation:** The `.well-known/agent-card.json` acts as a public-facing directory. It lists available capability-level skills (e.g., `agi_workspace_scan`, `asi_dialogue_guide`) and endpoint interfaces.
*   **Task Lifecycle Mapping:**
    *   When an external request is validated, the gateway initializes a stateful `Task` (identified by `taskId` and grouped under `contextId`).
    *   As work progresses, the server emits `TaskStatusUpdateEvent` (tracking states like `TASK_STATE_WORKING`) and `TaskArtifactUpdateEvent` (streaming output chunks) back to the client.
    *   If a safety floor triggers an validation hold or a human decision is needed, the task state transitions to `TASK_STATE_INPUT_REQUIRED` (or a custom A2A auth hold), suspending the execution stream until the operator responds.

### 2. MCP: Model Context Protocol (Organ Surface)
*   **Focus: Tool Usage (Stateless & Primitive)**
*   **Purpose:** Connects cognitive minds to execution substrates and domain solvers.
*   **Tool Isolation:** Low-level syscalls and domain solvers (e.g. fetching petrophysical logs, evaluating DCF valuation graphs, making system file edits) are wrapped behind MCP servers.
*   **Wargaaa Bindings:** The `333-AGI` agent uses `agi_mcp_discover` and `agi_tool_invoke` to dynamically inspect and run tools on the satellite organs. 
*   **Control Flow:** Cognitive models never execute code directly. They compile prompt requests, select the target organ's tool schema, and send the structured tool call request through the local MCP gateway, ensuring all inputs are sandboxed.

### 3. P2P: Local Inter-Agent Consensus
*   **Focus: System Safety & Verification (Under 10ms)**
*   **Purpose:** Serves as the internal nervous system for real-time compliance auditing and persistence.
*   **Verification Loop:** Before any execution occurs, the runtime uses local P2P channels to run floor checks:
    ```
    [Client Request] ──(A2A)──► [333-AGI] ──(P2P: Audit Request)──► [888-APEX]
                                                                        │
                                                                 (F1-F13 Audit)
                                                                        ▼
    [VAULT999 SEAL] ◄──(P2P: Commit)── [888-APEX] ◄──(SEAL/HOLD/VOID)───┘
    ```
*   **Latency Target:** Inter-agent P2P calls (e.g. requesting a F1-F13 verdict from APEX) bypass network routing entirely, keeping local RPC execution under 10ms.

---

## 🔌 Extensions & Custom Protocol Bindings

### A2A Extensions (Capability Negotiation)
A2A allows augmenting the base protocol using custom extensions declared in the Agent Card. The AAA Gateway supports:
1.  **`arif-fazil.com/ext/sovereign`**: Enforces Ed25519-signed challenge-response authentication. Clients request activation by passing `A2A-Extensions: arif-fazil.com/ext/sovereign` in HTTP headers, which the gateway validates and echoes back.
2.  **`arifos.verdict-grammar.v1`**: Structures cognitive responses into strict `SEAL / HOLD / VOID` formatting rules.

### Custom Protocol Bindings (CPB)
While A2A runs natively on HTTP/JSON-RPC, custom protocol bindings can be used to transport A2A messages over alternative substrates. The AAA Gateway implements:
*   **WebSocket Binding (`ws://127.0.0.1:18789`)**: Bridges the gateway with the local `openclaw` runtime mesh, facilitating low-latency streaming of task updates and events without HTTP overhead.

---

## 🏛️ Three-Layer Ontology Alignment (ΔΩΨ)

1.  **Substrate Layer (Δ):** Operates on the physical hardware and services (NATS, Redis, Docker, Caddy). It executes tools via **MCP**.
2.  **Constitution Layer (Ω):** Enforces policy limits and invariants. It intercepts external traffic at the **A2A Gateway**, inspects execution traces via **P2P**, and issues verdicts (`SEAL`, `HOLD`, `VOID`).
3.  **Cognitive Layer (Ψ):** Thinks, routes, and explains. It communicates externally using **A2A**, coordinates internal tasks using **P2P**, and leverages the substrate capabilities using **MCP**.

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
