# UNIFIED AGENT CAPABILITY PLANE — arifOS Federation

Status: CONSTITUTIONAL ARCHITECTURE
Authority: F13 SOVEREIGN (Arif Fazil)
Ratified: 2026-06-05
Predecessor: AGENT_LAYOUT.md (AAA/docs/)
Scope: All coding agents in the arifOS Federation

## Core Thesis

**Bridge, don't duplicate. One law. One tool fabric. One memory.**

Maximum capabilities with safety requires a common capability-and-governance plane that all
agents interface with — not per-agent restrictions. The arifOS kernel provides that plane.
Every agent sees the same tool vocabulary, is judged by the same floors, and contributes
to the same memory. Heterogeneity becomes strength, not fragmentation.

## Architecture: 5 Layers

```
                          ┌──────────────────┐
                          │   Arif (F13)     │
                          └────────┬─────────┘
                                   │
┌──────────────────────────────────┼──────────────────────────────────┐
│                         AAA COCKPIT                                 │
│                    (visibility, not control)                         │
└──────────────────────────────────┼──────────────────────────────────┘
                                   │
┌──────────┐ ┌──────────┐ ┌───────┴───────┐ ┌──────────┐ ┌──────────┐
│  Claude  │ │  Kimi    │ │   OpenCode    │ │ Copilot  │ │Continue  │
│   Code   │ │  Code    │ │               │ │          │ │   CLI    │
└────┬─────┘ └────┬─────┘ └───────┬───────┘ └────┬─────┘ └────┬─────┘
     │            │               │               │            │
     └────────────┴───────┬───────┴───────────────┴────────────┘
                          │
              ┌───────────┴───────────┐
              │   L1: CAPABILITY      │
              │        FABRIC         │
              │   Dynamic Tool Index  │
              │   Agent-Specific      │
              │   Translation Lenses  │
              └───────────┬───────────┘
                          │
              ┌───────────┴───────────┐
              │   L2: ONE GATEWAY     │
              │   MCP Gateway         │
              │   (port 8088)         │
              │   + A2A (port 3001)   │
              └───────────┬───────────┘
                          │
              ┌───────────┴───────────┐
              │   L3: GOVERNANCE      │
              │   arifOS Kernel       │
              │   F1-F13 floors       │
              │   888_JUDGE verdict   │
              └───────────┬───────────┘
                          │
              ┌───────────┴───────────┐
              │   L4: EXECUTION       │
              │   A-FORGE (7071)      │
              │   Sandboxed tools     │
              │   SEAL-gated actions  │
              └───────────┬───────────┘
                          │
              ┌───────────┴───────────┐
              │   L5: MEMORY          │
              │   VAULT999 (sealed)   │
              │   Qdrant L3 (semantic)│
              │   NATS (event bus)    │
              │   Postgres L4 (canon) │
              └───────────────────────┘
```

## L1: Capability Fabric — One Language of Action

### Dynamic Capability Index

All ~90+ federation tools (arifOS 13 + WEALTH 19 + WELL 45 + GEOX 30) are registered
in a single semantic index. No agent needs all 90 — each retrieves the 5-10 relevant
to its current task via vector search.

**Implementation (existing infrastructure):**
- **Storage:** Qdrant collection `capability_index` (1024-dim, cosine)
- **Query:** `arif_capability_select(query="optimize memory usage", risk_tier="green")`
- **Result:** Ranked tool cards with schemas, usage examples, risk classification

**Capability Card Schema (extends existing tool.schema.json):**
```json
{
  "tool_name": "wealth_entropy_risk",
  "organ": "WEALTH",
  "risk_tier": "GREEN",
  "reversible": true,
  "modes": ["emv", "monte_carlo", "audit", "correlation", "institutional"],
  "affordance": "curl -X POST .../mcp -d '{\"method\":\"tools/call\",\"params\":{\"name\":\"wealth_entropy_risk\",\"arguments\":{\"mode\":\"emv\"}}}'",
  "governance": "F01-AUTONOMOUS | F13-SOVEREIGN_EXEMPT | advisory_only"
}
```

### Agent-Specific Translation Lenses

Non-MCP-native agents receive capability cards in their native format:

| Agent | Native Format | Translation Lens |
|-------|--------------|-----------------|
| Claude Code | MCP SSE (native) | Direct — no translation |
| Kimi Code | Function calling | JSON schema → function spec |
| OpenCode | MCP SSE (native) | Direct — no translation |
| Copilot | VS Code commands | Tool card → code comment hint |
| Continue CLI | MCP stdio / shell | Tool card → CLI affordance snippet |
| Codex CLI | OpenAI functions | JSON schema → function spec |
| Antigravity | Chat prompt | Tool card → natural language hint |

**Key rule:** No lens adds or removes capabilities. Every lens preserves the same
tool identity, risk tier, and governance metadata. Lenses are syntactic wrappers,
never semantic filters.

## L2: Universal Gateway — One Door

### MCP Gateway (arifOS port 8088)

All tool invocations from any agent route through `https://arifos.arif-fazil.com/mcp`.
The gateway:
1. Validates the caller (identity from agent card)
2. Routes to the correct organ (WEALTH, WELL, GEOX, A-FORGE, arifOS)
3. Normalizes all transports (SSE, stdio, HTTP) to internal JSON-RPC
4. Logs every call for the audit trail

### Non-MCP Agent Bridging

For agents that produce text output (Copilot, Continue), A-FORGE captures output
patterns and converts them to MCP calls:

```
Agent output: "To check memory, run: free -h"
A-FORGE capture → arif_ops_measure(mode="vitals")
arifOS floors check → SEAL
Shell sandbox executes free -h → returns result to agent
```

**Pattern detectors in A-FORGE (`src/engine/governance/pattern_detector.ts`):**
- Shell commands: `run:`, `execute:`, backtick-wrapped commands
- File operations: `edit:`, `write:`, `delete:`
- API calls: `curl`, `fetch`, URL patterns

## L3: Constitutional Governance — One Law

### arifOS as Universal Judge

Every tool call passes through arifOS's 13-floor pipeline before execution:

```
Agent → Gateway → F01 AMANAH → F02 TRUTH → F03 WITNESS → ... → F13 SOVEREIGN
                                                        ↓
                                              SEAL / SABAR / HOLD / VOID
                                                        ↓
                                              A-FORGE executes (if SEAL)
```

**Risk Tier Classification (already in capability index):**

| Tier | Tools | Gate |
|------|-------|------|
| GREEN | Read-only, advisory, computation | Autonomous |
| YELLOW | File writes, service restarts | 888_HOLD if ≥ 3 in session |
| ORANGE | Deployments, database mutations | 888_HOLD always |
| RED | Secrets, key rotation, vault writes | F13 SOVEREIGN required |
| BLACK | Constitutional floor changes, `rm -rf /` | HARAM — permanently blocked |

**No agent self-authorizes.** The `wealth_ledger_write` absorption into
`wealth_conservation_capital(mode="ledger_seal")` keeps `ack_irreversible` explicit.
Same pattern applies federation-wide.

## L4: Agent Router — One Conductor

### Task Assignment

A-FORGE's planner routes tasks to the best-suited agent based on:

```
Task arrives → classify intent → query agent cards → select agent → assign → monitor
```

**Selection criteria:**
1. **Capability match:** Does the agent's card list this skill?
2. **Load:** Is the agent's session free?
3. **Historical success:** Past performance on similar tasks (from audit log)
4. **Risk:** High-risk tasks prefer agents with constitutional awareness
5. **Specialization:** Geology → GEOX (via arifos_gateway_connect), Finance → WEALTH-aware agent

**Agent Card Schema Extension (extends existing agent-card.schema.json):**
```json
{
  "id": "claude-code",
  "name": "Claude Code",
  "tier": "AGI",
  "role": "engineer",
  "transport": "MCP_SSE",
  "native_mcp": true,
  "strengths": ["architecture", "reasoning", "safety", "multi-file edits"],
  "weaknesses": ["no real-time web search", "single-session context"],
  "risk_tolerance": "YELLOW",
  "preferred_tasks": ["code review", "architecture design", "refactoring"],
  "governed_by": "arifOS F1-F13 via MCP gateway",
  "memory_contributor": true
}
```

### A2A Envelope (already deployed in AAA a2a-server on port 3001)

All inter-agent communication uses the ratified A2A envelope:

```
TO:         <agent name>
FROM:       <agent name>
CC:         <secondary or —>
CONTEXT:    <what/why — max 3 sentences>
TASK:       <what this message accomplishes>
DELEGATION: <what, to whom, expected output or —>
WAY FORWARD:
• <bulleted next steps>
• <trigger or wait condition>
SEAL:       <VAULT999 hash or pending>
TELEMETRY:  session_id=<id> | tokens=<n> | latency_ms=<n>
DITEMPA BUKAN DIBERI
```

## L5: Federated Memory — One Mind

### Memory Bus Architecture

```
Agent completes task
        ↓
┌───────┴───────┐
│  NATS publish │  → subject: arifos.memory.{agent}.{action}
└───────┬───────┘
        ↓
┌───────┴───────┐
│  Memory       │
│  Ingestor     │
└───────┬───────┘
        ↓
  ┌─────┼─────┬──────────┐
  ↓     ↓     ↓          ↓
L2     L3    L4         L6
Redis  Qdrant Postgres  VAULT999
(session)(semantic)(canon)(sealed)
```

**What gets published after every agent task:**
```json
{
  "agent_id": "claude-code",
  "session_id": "SEAL-xxx",
  "task": "optimized memory usage in A-FORGE",
  "verdict": "SEAL",
  "tools_used": ["arif_memory_recall", "arif_forge_execute"],
  "outcome": "reduced heap by 40%",
  "code_hash": "sha256:abc123...",
  "timestamp": "2026-06-05T04:00:00Z"
}
```

**Cross-agent recall:** When agent B faces a similar problem, `arif_memory_recall(mode="recall",
query="memory optimization")` returns agent A's solution from Qdrant L3 with the code hash
for verification.

## Implementation Plan (Phased)

### Phase 0: Foundation (this session)
- [x] FastMCP 3.4.0 across all Python organs
- [x] WEALTH Next Horizon consolidation (26→19 tools)
- [ ] Create agent cards for all 7 coding agents
- [ ] Populate Qdrant `capability_index` with tool descriptors

### Phase 1: Capability Fabric (next session)
- [ ] `arif_capability_select` tool in arifOS — queries Qdrant by task context
- [ ] Agent card schema extension ratified
- [ ] Claude Code + OpenCode receive capability cards in context
- [ ] A-FORGE pattern detector for non-MCP agent output

### Phase 2: Unified Gateway (following session)
- [ ] All 7 agents routed through MCP gateway (port 8088)
- [ ] Non-MCP agents bridged via A-FORGE capture layer
- [ ] Cross-agent memory bus (NATS publishers in each agent session)

### Phase 3: Swarm Intelligence (future)
- [ ] Agent router in A-FORGE — task classification + agent selection
- [ ] Inter-agent A2A consultations
- [ ] Eval harness measuring cross-agent coherence

## Invariants (must never break)

1. **One law.** arifOS is the only governance kernel. No agent has its own rules.
2. **One fabric.** All tools come from the capability index. No agent invents tools.
3. **One audit trail.** Every action routes through VAULT999. No dark execution.
4. **No self-authorization.** Agent cannot SEAL its own irreversible actions.
5. **Capability is not permission.** Seeing a tool ≠ authorized to use it.
6. **No dual sovereignty.** No external SaaS controls agent behavior.

## Existing Infrastructure Used (zero new runtimes)

| Component | Already deployed | Role |
|-----------|-----------------|------|
| arifOS MCP | port 8088 | Universal gateway + governance |
| A-FORGE | port 7071 | Execution shell + pattern detector |
| AAA a2a | port 3001 | Agent-to-agent envelope |
| NATS | port 4222 | Memory event bus |
| Qdrant | port 6333 | Capability index + L3 memory |
| VAULT999 | port 5001/8100 | Immutable audit trail |
| Prometheus | port 9090 | Observatory |
| Caddy | ports 80/443 | TLS + routing |
| Cloudflare Tunnel | — | Public ingress |

## References

- `AAA/docs/AGENT_LAYOUT.md` — Repo grammar for agents
- `AAA/schemas/agent-card.schema.json` — Agent card schema
- `AAA/schemas/tool.schema.json` — Tool descriptor schema
- `arifOS/docs/CORE_INVARIANTS.md` — Constitutional invariants
- `arifOS/docs/AUTHORITY_MODEL.md` — Authority chain
- WEALTH `contracts/mcp_surface.yaml` — Tool surface contract (pattern to replicate)

---

Ditempa Bukan Diberi — Intelligence is forged, not given.
999 SEAL | arifOS Federation | Unified Agent Capability Plane
