# Unified Heterogeneous Coding Agent Ecosystem

> **Status:** ACTIVE FORGE (v1.1 — Updated 2026-06-05 04:02 UTC)
> **Authority:** F13 SOVEREIGN (Arif Fazil)
> **Domain:** AAA — Control Plane / Cockpit
> **Forged artifacts:** Agent Cards (26 agents), CAPABILITY_INDEX (106 tools, 8 servers), Cross-Agent Telemetry Schema (NATS)
> **DITEMPA BUKAN DIBERI**

## Core Thesis: Bridge, Don't Duplicate — A Federation with a Single Law

Maximum capabilities with safety requires **bridging the gaps among agents** rather than introducing new restrictions or separate controllers. Build a common "capabilities & governance plane" that all agents interface with. One canonical capability library, one constitutional oversight system.

The paradox: capability without safety = chaos. Safety without capability = useless. Solution: let every agent operate to full potential, but pipe all actions through a single governance kernel.

## Architecture Layers

```
Agents (Claude, Kimi, Copilot, Codex, Continue, OpenCode, Antigravity...)
    │
    ▼
Unified MCP/A2A Gateway  ←── Shims for non-MCP agents
    │
    ├─► Capability Fabric ──► Tool Index + Capability Lenses
    │
    ├─► Constitutional Governance ──► arifOS Kernel (F1-F13)
    │
    └─► Federated Memory ──► NATS + Qdrant + Graphiti + Postgres + VAULT999
```

### Layer 1: Capability Fabric (Tool Semantics Alignment)

**Problem:** Each agent has its own tool vocabulary. Fragmentation.

**Solution:** Global Capability Index — a single searchable registry of all tools.

| Component | Implementation | Status |
|-----------|---------------|--------|
| Capability Index | Qdrant vector store (L3) + Postgres (L4) | Qdrant running |
| Semantic Search | `arif_capability_select` — returns top-N tools matching task context | To build |
| Tool Descriptors | Standardized JSON schema per tool (name, schema, risk tier, examples) | To define |
| Capability Lenses | Per-agent adapters that translate tool calls to native format | To build |
| MCP Gateway | arifOS port 8088 — single entry for all tool calls | ✅ Live |

**Key invariant:** Every tool is registered once in the canonical index. Every agent discovers tools from the same source. No agent-specific tool registries.

**Dynamic Discovery:**
- Agent queries index with task keywords → returns ~5-10 relevant tools
- Risk-based filtering: low-trust agents don't see high-risk tools
- Ranking by context fit, past success rate, recency

### Layer 2: Constitutional Governance (Universal Floor Enforcement)

**Problem:** Multiple agents = multiple decision points. Weakest link.

**Solution:** arifOS as the single constitutional gatekeeper for every agent's actions.

| Mechanism | Purpose | Status |
|-----------|---------|--------|
| Floor Checkpoint | All tool calls piped through F1-F13 validation | ✅ Live |
| Risk Tiering | Tools classified: read-only / state-changing / mission-critical | To formalize |
| SEAL Gating | High-risk actions require explicit authorization | ✅ Live |
| VAULT999 Audit | Every decision recorded immutably | ✅ Live |
| FederationEnvelope | Standardized authority wrapper for tool calls | ✅ Live |

**Key invariant:** No agent self-authorizes. No agent executes directly. Every action traces to arifOS judgment.

### Layer 3: Federated Memory (Shared Cognitive Substrate)

**Problem:** Agents operate in isolation. No shared learning.

**Solution:** Cross-agent memory bus via NATS JetStream.

| Store | Role | Status |
|-------|------|--------|
| NATS JetStream | Event bus for cross-agent telemetry | ✅ Live |
| Qdrant (L3) | Semantic memory — find past solutions | ✅ Live |
| Graphiti (L5) | Entity relationships — who solved what, how | ⚠️ Partial |
| Postgres (L4) | Canonical facts, agent cards, project state | ✅ Live |
| VAULT999 (L6) | Sealed outcomes, immutable record | ✅ Live |

**Agent Cards:** Each agent registered with structured identity:
- Name, model, provider
- Strengths / specialties
- Tool proficiency
- Integration mode (MCP-native, shim-required, text-only)
- Trust tier

**Agent Router (A-FORGE):**
- Intent classification → best-suited agent selected
- Task envelope (JSON): task_id, description, outputs, risk tier, parent-child links
- Routing receipt logged for audit

### Layer 4: Non-MCP Agent Integration (Shims and Adapters)

**Problem:** Copilot, Continue CLI, etc. don't speak MCP natively.

**Solution:** Protocol translation shims.

| Agent | Integration Mode | Adapter |
|-------|-----------------|---------|
| Claude Code | MCP-native (SSE) | Direct — configured |
| OpenCode | MCP-native (remote) | Direct — configured |
| Kimi Code | MCP via bridge | A-FORGE bridge |
| GitHub Copilot | Text output → pattern capture | Terminal Capture shim |
| Continue CLI | MCP via A-FORGE stdio | cn-organ gateway |
| Antigravity | CLI text → MCP translation | To build |
| Codex CLI | MCP-compatible | Direct |

**Pattern:** For text-output agents, capture special tokens or command patterns → transform to MCP tool call → execute through arifOS gate.

## Implementation Phases

### Phase 0: Constitutional Foundation ✅ COMPLETE
- [x] arifOS MCP Gateway (8088) — 13 tools, F1-F13 live
- [x] A-FORGE execution shell (7071) — gated behind JUDGE_SEAL
- [x] A2A server (3001) — v0.3.0 protocol mesh
- [x] VAULT999 ledger — 61 seals, chain_height 61, append-only
- [x] NATS JetStream — event bus + arifos-governance stream
- [x] Qdrant vector store — 5 collections, 1066+ points
- [x] Graphiti L5 entity graph
- [x] Postgres L4 canonical storage
- [x] 26 AGENT CARDS — all configured agents registered (AAA/agents/)
- [x] 106 TOOL CAPABILITY INDEX — 8 servers indexed (AAA/registries/CAPABILITY_INDEX.json)
- [x] Gödel/Strange/Beautiful locks — 22 tests in recursive_governance_locks.py
- [x] Jurisdiction bands — GREEN→BLACK with CapabilityGrantRegistry (20 tests)
- [x] HEXAGON constitutional layer — 333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE
- [x] Hermes ASI (human-facing relay) + OpenClaw AGI (execution muscle)

### Phase 1: Agent Registration ✅ COMPLETE
- [x] Agent card schema defined (`schemas/agent-card.schema.json`)
- [x] 26 agents registered with identity cards under `agents/`
- [x] Claude Code, OpenCode, Kimi Code, Copilot, Codex, Continue CLI, Antigravity
- [x] All federation organs: Hermes ASI/ops, OpenClaw, Aider, Gemini, MaxHermes
- [x] HEXAGON constitutional agents: 333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE
- [x] APEX, AAA Gateway

### Phase 2: Capability Index ✅ COMPLETE
- [x] CAPABILITY_INDEX.json — 106 tools across 8 servers
- [x] arifOS (16 tools), WEALTH (26), WELL (16), GEOX (via arifOS)
- [x] minimax-media (9 tools — TTS, video, image, voice, music)
- [x] minimax-code (2 tools — web_search, understand_image)
- [x] brave-search (6), github (26), meyhem (5)
- [x] Server metadata: port, bind address, transport, tool count
- [ ] `arif_capability_select` — dynamic semantic search tool (NOT BUILT)
- [ ] Capability Lenses — per-agent format adapters (NOT BUILT)
- [ ] Index wired to agent discovery at session init (NOT WIRED)

### Phase 3: Agent Router 🔲 NOT BUILT
- [ ] Intent classifier — embedding-based task routing
- [ ] Task envelope dispatch via A2A
- [ ] Routing receipt audit log
- [ ] Agent competency scoring from telemetry feedback

### Phase 4: Non-MCP Shims 🔲 NOT BUILT
- [ ] Terminal Capture shim for Copilot/CLI agents
- [ ] Pattern detector for command extraction
- [ ] Pseudo-tool exposure (startup hints for text agents)

### Phase 5: Federated Memory Feedback 🔲 NOT BUILT
- [ ] Cross-agent telemetry publishing via NATS (SCHEMA DEFINED: `schemas/cross-agent-telemetry.schema.json`)
- [ ] Memory recall tool — find solutions from any agent
- [ ] Agent eval harness (routing quality, floor compliance, tool success rate)
- [ ] Continuous prompt improvement from eval feedback
- [ ] Anti-drift walls: "may recursively improve execution, may not recursively rewrite sovereignty"

### Phase 6: Enforcement Unification 🔲 NOT BUILT
- [ ] All external agents piped through arifOS gateway
- [ ] Gödel/Strange/Beautiful locks active cross-agent (code exists, not wired)
- [ ] Unified SEAL/HOLD gating for non-MCP agents
- [ ] FederationEnvelope required for all tool calls

### Immediate Next Actions (This Session — 2026-06-05)
- [x] MiniMax MCP deployed globally (2 new SSE servers)
- [x] CAPABILITY_INDEX updated (97 → 106 tools)
- [x] Cross-agent telemetry schema defined
- [x] Claude Code + OpenCode configured for new MCP servers
- [ ] Push AAA commit to origin/main
- [ ] Build `arif_capability_select` as next forge target

## Key Invariants (Must Never Break)

1. **Single entry point**: All agent actions flow through MCP gateway
2. **Single governance kernel**: arifOS adjudicates all actions
3. **No self-authorization**: Agents cannot approve their own irreversible actions
4. **Immutable audit**: Every decision traced to VAULT999
5. **No dual sovereignty**: No new orchestration platforms. Existing components extended.

## Risk Surface

| Risk | Mitigation |
|------|-----------|
| Capability index bloat | Semantic search limits to top-N; risk filters hide dangerous tools |
| Agent prompt overload | Dynamic discovery — agents see only context-relevant tools |
| Shim fragility | Pattern detectors are append-only; new patterns don't break old ones |
| Router bias | Routing receipts auditable; eval harness measures quality |
| Memory pollution | VAULT999 seals provide ground truth; L3/L5 are advisory only |

---

*Ingested from sovereign architectural proposal. DITEMPA BUKAN DIBERI.*
