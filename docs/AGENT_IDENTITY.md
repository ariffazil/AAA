# AGENT IDENTITY MAP — The Three-Dimensional Identity Model

> **DITEMPA BUKAN DIBERI** — Identity is forged, not given.
> **Canonical source:** This file + `agents/*/agent-card.json` (v2.2.0 schema)
> **Last updated:** 2026-07-04

---

## 1. The Problem This Solves

The federation has **three identity systems** that must be reconciled:

| System | Schema | Path | Consumer |
|--------|--------|------|----------|
| arifOS Agent Card | `arifOS/agent-card/v2.2.0` | `agents/*/agent-card.json` | Federation organs |
| A2A Agent Card | A2A v1.0 `AgentCard` | `/.well-known/agent-card.json` | External A2A agents |
| A2A Registry | A2A agents.json | `/.well-known/agents.json` | Discovery clients |

**The invariant: ONE agent card → THREE views derived from it.**

---

## 2. The Three-Dimensional Identity Model

```
Identity = A2A Public Card ∪ arifOS Constitutional Profile ∪ Runtime Binding
```

| Dimension | A2A Field | arifOS Extension | Where It Lives |
|-----------|-----------|-----------------|----------------|
| **Capability** | skills[].id, name, description, tags, examples | mcp_surface, floor_scope per skill | `agent-card.json` skills[] |
| **Constitutional** | extensions[] | principal_agent, hexagon_warga, charter | `agent-card.json` root |
| **Relational** | provider | bound_to, trinity layer, organ_host | `agent-card.json` root |
| **Metaphysical** | — | apexMasterSeal (cognitive ring, JITU gate) | `agent-card.json` (extended card only) |

---

## 3. Identity Sources — Canonical vs Derived

```
agents/<id>/agent-card.json
    └── arifOS v2.2.0 (SINGLE SOURCE OF TRUTH)
         │
         ├── a2a-server/agent-cards/<id>.json  → SYMLINK to agents/<id>/agent-card.json
         │
         ├── public/.well-known/agent-card.json  → GENERATED (A2A-compatible view)
         │
         ├── .well-known/agent-card-extended.json  → GENERATED (full arifOS + auth)
         │
         └── .well-known/agents.json  → GENERATED at runtime from agent-card-registry
```

### Source Locations

| Path | Schema | Mutability | Auth |
|------|--------|-----------|------|
| `agents/<id>/agent-card.json` | arifOS v2.2.0 | Canonical — edit here | Write: F13 |
| `a2a-server/agent-cards/<id>.json` | Symlink to agents/ | Read-only (via symlink) | Read: any |
| `a2a-server/agent-cards/aaa-*.json` | arifOS v2.2.0 (infra) | Unique infra cards | Read: any |
| `a2a-server/agent-cards/forge/*.json` | arifOS v2.2.0 (forge) | Unique forge instrument cards | Read: any |
| `a2a-server/agent-cards/organs/*.json` | arifOS v2.2.0 (organs) | Unique organ descriptor cards | Read: any |
| `public/.well-known/agent-card.json` | A2A v1.0 | Generated — do not edit | Read: any |
| `/.well-known/agents.json` (at :3001) | A2A registry | Generated at runtime | Read: any |

---

## 4. Agent Taxonomy

### 4.1 HEXAGON Warga (Constitutional Citizens)

| ID | Class | Ring | Stage | Skills | Source Card |
|----|-------|------|-------|--------|-------------|
| 333-AGI | AGI | Δ MIND | 333 | 33 | `agents/_lanes/333-AGI/` |
| 555-ASI | ASI | Ω HEART | 555 | 33 | `agents/_lanes/555-ASI/` |
| 888-APEX | APEX | ΦΙ JUDGE | 888 | 33 | `agents/_lanes/888-APEX/` |
| A-AUDIT | Collapsed | (observer) | N/A | Collapsed | `agents/_lanes/A-AUDIT/` (embedded in 888-APEX) |
| A-ARCHIVE | Collapsed | (vault) | N/A | Collapsed | `agents/_lanes/A-ARCHIVE/` (embedded in 888-APEX) |

### 4.2 Runtime Agents (Operational)

| ID | Role | Host | Source Card |
|----|------|------|-------------|
| hermes-asi | Telegram relay | Hermes | `agents/hermes-asi/` |
| openclaw | OpenClaw gateway | Local | `agents/openclaw/` |
| opencode | CLI forge instrument | VPS | `agents/opencode/` |
| main | Operator assistant | OpenClaw | `agents/main/` |

### 4.3 A-Role Cards (Infrastructure)

| ID | Role | Source Card |
|----|------|-------------|
| aaa-gateway | AAA gateway card | `a2a-server/agent-cards/aaa-gateway.json` |
| aaa-architect | AAA architect persona | `a2a-server/agent-cards/aaa-architect.json` |
| aaa-engineer | AAA engineer persona | `a2a-server/agent-cards/aaa-engineer.json` |
| aaa-auditor | AAA auditor persona | `a2a-server/agent-cards/aaa-auditor.json` |

### 4.4 External CLI Tools (Connected)

| ID | Vendor | Source Card |
|----|--------|-------------|
| aider | Aider | `agents/_external/aider/` |
| claude-code | Anthropic | `agents/_external/claude-code/` |
| codex | OpenAI | `agents/_external/codex/` |
| continue-cli | Continue | `agents/_external/continue-cli/` |
| copilot | GitHub/Microsoft | `agents/_external/copilot/` |
| gemini-cli | Google | `agents/_external/gemini-cli/` |
| grok-build | xAI | `agents/_external/grok-build/` |
| kimi-code | Moonshot | `agents/_external/kimi-code/` |
| qwen-code | Alibaba | `agents/_external/qwen-code/` |

---

## 5. A2A Endpoint Map (AAA Gateway, port 3001)

| Path | Purpose | Auth | Data Source |
|------|---------|------|-------------|
| `/.well-known/agent-card.json` | A2A canonical agent card | No | `src/seed/agent-card-official.json` |
| `/.well-known/agent-card-extended.json` | Extended card with federation topology | Yes (bearer) | Same + `_extended` fields |
| `/.well-known/agents.json` | Agent registry (generated) | No | `agent-card-registry` `getAll()` |
| `/.well-known/a2a-discovery.json` | Discovery contract | No | Dynamic |
| `/.well-known/a2a-routing-policy.json` | Routing policy | No | Static config |
| `/.well-known/arifos-federation.json` | Federation manifest | No | Static config |
| `/.well-known/peer-federation-contract.json` | Peer contract | No | Static config |

---

## 6. How to Add a New Agent

1. Create `agents/<id>/agent-card.json` (arifOS v2.2.0 schema)
2. If the agent is a warga: add to HEXAGON registry in server.js
3. If the agent needs A2A discovery: add symlink or card to `a2a-server/agent-cards/`
4. Restart `aaa-a2a.service` → registry auto-loads → `/.well-known/agents.json` updates

---

## 7. Invariants

1. **One card = one agent.** No duplicate files for the same agent.
2. **agents/*/agent-card.json is canonical.** Edit there. The a2a-server/agent-cards/ dir contains symlinks or infra-only cards.
3. **protocolVersion must be 1.0.0** (current A2A v1.0 spec).
4. **`/.well-known/agents.json` is generated, not hand-maintained.** The `public/a2a/agents.json` file is deprecated.
5. **Part discriminator uses `type` (v1.0), not `kind` (legacy).** Validation accepts both for backward compat.

---

*DITEMPA BUKAN DIBERI — Identity is constitutional, not configurable.*
