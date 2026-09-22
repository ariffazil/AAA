---
id: forge-mcp-governance-wrapper
name: forge-mcp-governance-wrapper
version: 1.0.0-2026.08.28
description: "Use when building MCP governance interception layers."
owner: A-FORGE
risk_tier: high
floor_scope: ['F1', 'F2', 'F4', 'F11', 'F13']
autonomy_tier: T2
ecology_state: WARM
capability_tier: fed-agent-subagent
---
# ⚒️ MCP Governance Wrapper — Deterministic Interception Architecture

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose

Build and operate deterministic governance layers on top of MCP (Model Context Protocol) that enforce tool-call safety, reversibility checking, intent routing, and audit logging — WITHOUT relying on LLM judgment for enforcement.

## When to Use

- Adding a new MCP server to the federation and need governance metadata
- Building tool-call interception/proxy layers for arifOS
- Designing intent routing for agent tool selection
- Creating policy configs for tool classification (reversibility, impact, role ACL)
- Building append-only audit chains for governance events
- Reviewing MCP governance architecture for correctness

## When NOT to Use

- MCP server health probes — use `FORGE-mcp-lifeguard`
- MCP server testing/conformance — use `mcp-testing`
- MCP server operations — use `mcp-ops`
- Agent-level governance (constitution, floors) — use `ASI-agentic-governance`

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Policy file signed. Unsigned mutations blocked. Interceptor immutable — no silent drift. |
| F2 TRUTH | Tool declarations must match live tools/list. Drift = F2 violation. |
| F4 CLARITY | One policy file, one audit chain, one interceptor binary. No stale copies. |
| F11 AUDIT | Append-only audit chain with cryptographic hash linking. Every reload logged. |
| F13 SOVEREIGN | Impact radius ≥ 3 tools require 888 Sovereign Key. No self-authorization. |

---

## Core Problem: The False Confidence Paradox

When MCP exposes 100+ tools simultaneously:
- **Schema collision** occurs (similar tool names, different domains)
- **Attention degradation** increases proportionally with tool count
- **Capability-judgment gap widens** — agent feels more capable but judgment doesn't scale

**Measurement:** When >15 tools visible in a single turn, tool-call error rate increases ~3x vs ≤5 tools.

**Root cause:** MCP was designed for connectivity, not governance. It carries no native reversibility metadata, permission semantics, or impact classification.

---

## Architecture: 4 Deterministic Mechanisms

### Mechanism 1: Zero-LLM Intent Router

**Rule:** Intent classification is deterministic (regex, JSON-RPC method dispatch, domain tag mapping). ZERO LLM inference calls.

**Why:** LLM-based routing moves judgment problem one layer down. Router miscategorize → wrong tools exposed → same False Confidence Paradox at smaller scope.

**Implementation:**
- Three dispatch mechanisms (priority order): JSON-RPC method pattern → domain tag extraction → session history heuristic
- Latency budget: ≤5ms
- Maximum tools per turn: N ≤ 5 (hard cap)
- If multi-domain task → trigger decomposition, NOT broader toolset

**Pitfall:** Using an LLM call to classify intent. This is the most common anti-pattern. It looks elegant but recurses the problem.

### Mechanism 2: Per-Agent Role ACL

**Rule:** Each agent persona in a gotong-royong session sees only tools authorized for its role. Flat policy (all tools for all agents) is explicitly prohibited.

**Role Definitions:**
- `333-AGI`: read, compute, propose, spawn (NO state-mutation)
- `555-ASI`: read, verify, audit only (NO mutation, NO spawn)
- `888-APEX`: read, deliberate, verdict, seal
- `A-FORGE`: read, execute-after-seal, build, deploy
- `Validator`: read, verify only (ZERO mutation tools)

**Implementation:**
- ACL resolved at gotong-royong session initialization
- Orchestrator assigns tool masks per sub-agent
- Sub-agent context receives ONLY role-scoped tools — no exception

### Mechanism 3: Custom MCP Reversibility Wrapper

**Rule:** Native MCP spec has no governance metadata. Inject arifOS custom headers at tool registration/build-time.

**arifOS Headers:**
```
arifos_is_reversible: bool
arifos_impact_radius: int (0–5)
arifos_requires_888_hold: bool
arifos_category: enum (read-only|compute|propose|state-mutation|high-impact-mutation|critical-mutation)
arifos_allowed_roles: list[str]  // empty = 888 only
```

**Fail-Safe Default:** Unknown/unregistered tools → UNCHECKED_BLOCK. Tool cannot be invoked until signed metadata is injected.

**Impact Radius Mapping:**
- 0: No state change (read-only)
- 1: Trivial compute, no mutation
- 2: Propose action, reversible
- 3: State mutation, requires 888 hold
- 4: High-impact mutation, requires 888 hold
- 5: Critical infrastructure, requires 888 + W_SCAR confirmation

### Mechanism 4: Governed Dynamic Policy Layer

**Rule:** Immutable binary (Rust) + cryptographically signed dynamic config (TOML). Decouples runtime enforcement from policy evolution.

**Architecture:**
- **Immutable Engine:** Rust compiled interceptor. Stateless, no learning loop. Reads policy from disk. Verifies signature. Enforces deterministically.
- **Dynamic Policy:** TOML/JSON config. Hot-reloadable. Every update signed with Ed25519 (888 Sovereign) or HMAC (DEV_KEY for delegated scope).
- **Delegated Authority:** Impact ≤1 + reversible → DEV_KEY. Impact >1 or irreversible → 888 Sovereign Key only.
- **Fail-Safe:** Invalid signature → retain last-known-good. Missing file → retain last-known-good. Corrupted → alert + revert.
- **Append-Only Audit Chain:** Every policy reload logged with SHA256 hash linking. Tamper-evident.

**Pitfall:** Making the interceptor binary mutable (with learning/retraining loops). The interceptor MUST be immutable. Policy evolves via signed config, not binary changes.

---

## Musyawarah Execution Rules (3-Tier Runtime Governance)

Runtime decision framework for when to escalate:

### Tier 1: Trivial Task = Solo Fast-Path
- Low-risk, routine work
- Agent runs solo, no deliberation
- Cuts latency, saves tokens, ΔS < 0

### Tier 2: High-Risk / Ambiguous = Trigger Musyawarah
- P(truth) < 0.99 OR risk present
- Tri-witnessing 2-3 agents
- Capped at max 2 turns
- No consensus after 2 turns → declare Ω₀ (Uncertainty), stop deliberating

### Tier 3: State Mutation = Gotong Royong + F1 Gate
- Sub-agents can split for parallel sub-tasks
- Write/execute actions MUST pass F1 (Reversibility check)
- If irreversible → HOLD for 888 confirmation

**Key principle:** Musyawarah is a safety gate triggered by need, NOT a default chatting protocol for everything.

**Pitfall:** Infinite musyawarah loops. Always enforce the 2-turn cap. Ω₀ is a valid outcome.

---

## Reference Files

- `references/rfc-summary.md` — RFC spec decisions, locked architecture, phase roadmap
- `references/musyawarah-execution-rules.md` — 3-tier runtime governance + 3 hard mechanisms
- `references/rust-crate-pattern.md` — Standard pattern for arifOS Rust infrastructure crates
- `templates/mcp-governance-policy.toml` — Starter policy config with all tool categories

---

## Anti-Patterns

1. **LLM-based intent routing** — Recurses the judgment problem. Always use deterministic classifier.
2. **Flat tool ACL in multi-agent sessions** — All agents seeing all tools = False Confidence Paradox at agent level.
3. **Mutable interceptor binary** — If the interceptor can learn/drift, it's not deterministic. Immutable binary + signed config only.
4. **UNKNOWN = ALLOWED** — Unregistered tools must default to UNCHECKED_BLOCK, never allowed.
5. **Soft-only governance** — Constitution/prompt rules without deterministic enforcement = drunk driver reading safety manual while driving.
6. **Tool count as capability metric** — More tools ≠ better judgment. Track capability-to-judgment ratio, not tool count.
