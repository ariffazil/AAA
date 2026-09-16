# Musyawarah Execution Rules — 3-Tier Runtime Governance

> Locked: 2026-08-28 by 888 Sovereign

## Core Principle

Musyawarah is a safety gate triggered by need, NOT a default chatting protocol for everything.

## Tier 1: Trivial Task = Solo Fast-Path

- Low-risk, routine work
- Agent runs solo, no deliberation
- Cuts latency, saves tokens, ΔS < 0
- **Trigger:** Default for all tasks unless risk detected

## Tier 2: High-Risk / Ambiguous = Trigger Musyawarah

- **Trigger:** P(truth) < 0.99 OR any risk present
- Tri-witnessing: 2-3 agents deliberate
- **Hard cap:** Max 2 turns
- No consensus after 2 turns → declare **Ω₀ (Uncertainty)** and stop
- **Pitfall:** Infinite deliberation loops. Always enforce the 2-turn cap.

## Tier 3: State Mutation = Gotong Royong + F1 Gate

- **Trigger:** Any write/execute action that mutates state
- Sub-agents can split for parallel sub-tasks
- ALL write/execute actions MUST pass F1 (Reversibility check)
- **If irreversible:** HOLD for 888 confirmation. No exceptions.
- **If reversible:** Execute with audit trail.

## 3 Hard Infrastructure Mechanisms

### 1. Zero-LLM Intent Router
Deterministic classifier (regex, JSON-RPC method dispatch, domain tag mapping).
Zero LLM inference. Latency ≤5ms. Max 5 tools per turn.

### 2. Per-Agent Role ACL
Each agent persona sees only authorized tools. Flat policy prohibited.
Resolved at gotong-royong session initialization.

### 3. MCP Proxy Interceptor (Hard F1 Gate)
Tool payloads pass through deterministic interceptor before reaching MCP servers.
Irreversible operations blocked at OS layer. EXECUTION_BLOCKED returned to agent.
