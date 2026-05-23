# AAA² — Agent-Agnostic Architecture (Target State Roadmap)

> **Analyst:** Kimi (Moonshot AI)
> **Classification:** AAA Technical Architecture Review — Level F13 Sovereign
> **Epoch:** 2026-05-23
> **Status:** TARGET_STATE (Roadmap) — Not yet implemented.

---

## 1. CURRENT_STATE (The Agent Trap)

Currently, the federation operates as an L3 (Multi-Agent) system bound by the **arifOS 13-tool Constitutional Kernel** (F1-F13) and the **Nine-Signal Hub**.

However, the architecture suffers from the "Agent Trap" — N×M hardcoded integration:
- `arifOS/.claude/`, `arifOS/.gemini/`, `arifOS/.opencode/`
- `AAA/agents/openclaw/`, `AAA/agents/hermes-*`

This requires per-agent custom integration for identity, state, and governance, which breaks true A2A interoperability. Governance is currently enforced via HTTP round-trips to the Python arifOS kernel, preventing opaque boundary enforcement for external agents.

---

## 2. TARGET_STATE (AAA² Agent-Agnostic Substrate)

The target state shifts the philosophy from *"integrating agents into our system"* to *"any agent that speaks A2A+MCP is automatically a citizen of our federation."*

### The New Four-Layer Topology
1. **SOVEREIGN INTENT (Δ):** Human-only layer (Arif, 888 Judge).
2. **CONSTITUTIONAL KERNEL (Ω):** arifOS (13 Floors, Verdict Engine) + **Universal Agent Adapter (UAA)**.
3. **AGENT-AGNOSTIC PLANE (Ψ²):** The AAA² Mesh. Identity Registry, Capability Negotiator, Portable State Protocol, Cross-Agent Memory.
4. **EXECUTION SUBSTRATE (Ξ):** A-FORGE Runtime Abstraction (Docker/WASM/Process).

### The Seven Pillars of AAA²

1. **Universal Agent Adapter (UAA):** Standardized interface for any agent (Codex, Claude, OpenCode, Gemini) to connect to the federation without custom hardcoding.
2. **Agent Identity & Binding Protocol:** A2A Agent Cards subjected to constitutional binding ceremonies before receiving federation JWTs.
3. **Portable State Protocol (PSP):** Agent-agnostic state representations stored in VAULT999. Allows context handoff (e.g., Claude starts, Kimi continues, OpenClaw finishes).
4. **Federation Mesh (FMesh):** Peer-to-peer gossip discovery replacing the centralized A2A gateway.
5. **Unified Skill Ontology:** A single, federated registry mapping skills to constitutional thresholds (e.g., F11 required to judge).
6. **Cross-Agent Memory (CAM):** Shared epistemic state transfer with constitutional access control.
7. **Governance Compiler (gWasm):** Compiling F1-F13 into executable WebAssembly (WASM) modules so any agent runtime enforces policy locally.

---

## 3. ALIGNMENT TO CANON

- **13-Tool Alignment:** The 13 canonical arifOS tools remain the SOT for all interactions. The AAA² Universal Agent Adapters will marshal external agents through this exact 13-tool pipeline (000 INIT -> 999 SEAL).
- **Nine-Signal Alignment:** The Cross-Agent Memory (CAM) and Federation Mesh (FMesh) will broadcast along the Nine-Signal ontological frequencies.
- **W_scar Consequence Surface:** The gWasm compiler ensures that irrespective of the agent's internal architecture, the physical execution consequence (W_scar) remains governed by the physical invariants (Earth/GEOX) and the Sovereign Veto (Human/888).

*DITEMPA BUKAN DIBERI — AAA² is the Forge for L5 ASI.*
