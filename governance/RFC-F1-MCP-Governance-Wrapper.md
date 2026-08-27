# RFC: F1-MCP-Governance-Wrapper

> **Status:** DRAFT — Awaiting 888 Sovereign Seal  
> **Date:** 2026-08-28  
> **Authors:** Hermes (orchestration seat), Arif (sovereign architect)  
> **Reviewers:** Gemini (external intelligence), 333-AGI (proposer)  
> **ΔS:** -0.18  
> **FQ:** OPTIMAL  
> **Constitutional Scope:** F1 (AMANAH), F2 (TRUTH), F13 (SOVEREIGN)  
> **Depends On:** AAA_TOOL_RIGHTS_POLICY_v0.2, FORGE-federation-manifest

---

## 0. Abstract

arifOS runs on 15+ MCP servers with 100+ exposed tool schemas. The current architecture allows raw MCP connections directly into the main LLM context window, creating three systemic failure modes:

1. **False Confidence Paradox** — Tool proliferation widens the gap between capability (what the agent CAN call) and judgment (what the agent SHOULD call).
2. **Soft Boundary Failure** — Constitution/governance rules enforced via system prompt are stochastic. A degraded attention state cannot reliably self-audit.
3. **Governance Absence in MCP Spec** — The MCP protocol was designed for connectivity, not governance. It carries no native reversibility metadata, permission semantics, or impact classification.

This RFC defines four deterministic infrastructure mechanisms that move judgment enforcement from LLM context window to compiled runtime, closing the gap between capability surface and governance layer.

**Core Principle:** Governance lives in deterministic code, not stochastic prompts.

---

## 1. Problem Statement

### 1.1 The Entropy Displacement Problem

MCP solves syntactic standardization (JSON-RPC, uniform handshake). It does NOT solve semantic alignment. When 20 MCP servers expose 100 tools simultaneously:

- Schema collision occurs (e.g., `fed_route` vs `geox_claim` — similar invocation pattern, different domain).
- Attention degradation increases proportionally with tool count.
- Agent confidence calibration fails — the agent becomes confidently wrong about tool selection.

**Measurement:** When >15 tools are visible in a single turn, tool-call error rate increases ~3x vs. ≤5 tools (empirical observation from arifOS sessions).

### 1.2 The Unified Blast Radius Problem

Standardized protocol = standardized attack surface. Indirect prompt injection that compromises one tool surface can traverse the entire MCP layer because:

- Permission model is static declaration (at registration), not dynamic runtime validation.
- No deterministic circuit breaker exists between LLM tool-call output and MCP server execution.

### 1.3 The State Blindness Problem

MCP treats tools as stateless pure functions: JSON in, JSON out. But tools like `capital_ledger`, `geox_claim`, and `well_log_intake` mutate real state. MCP carries:

- No reversibility metadata
- No impact radius classification
- No cascading failure awareness

The agent receives no native signal about whether a call is safe, risky, or irreversible.

### 1.4 The Self-Audit Paradox

F1–F13 governance floors are enforced via system prompt. When an agent enters attention degradation (schema overload, hallucination cycle, fatigue), the very mechanism that should catch errors IS the degraded mechanism. This is equivalent to requiring a compromised system to audit its own compromise.

**Conclusion:** Governance must move from stochastic prompt to deterministic runtime.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      LAYER 0: LLM                          │
│              (Main model + agent reasoning)                 │
│                 Sees: max 3–5 tools                         │
└──────────────────────┬──────────────────────────────────────┘
                       │ tool-call output (JSON-RPC)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            LAYER 1: MCP REVERSIBILITY WRAPPER               │
│   Custom arifOS headers injected at tool registration:     │
│   is_reversible | impact_radius | requires_888_hold        │
│   Missing metadata → UNCHECKED_BLOCK                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ wrapped payload
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        LAYER 2: DETERMINISTIC INTERCEPTOR                   │
│   Compiled binary (Rust/Go), stateless, immutable           │
│   Reads signed TOML/JSON policy → enforces rules            │
│   Blocks writes without reversibility metadata              │
│   Logs every decision to append-only audit chain            │
└──────────────────────┬──────────────────────────────────────┘
                       │ approved payload (or BLOCKED)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 3: MCP SERVERS (Target)                  │
│   FED | GEOX | WEALTH | WELL | minimax-media | composio   │
└─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────┐
    │         ORTHOGONAL: ZERO-LLM INTENT ROUTER      │
    │  Deterministic classifier (regex/tag/dispatch)  │
    │  Operates BEFORE tools enter Layer 0 context    │
    │  Input: user intent + session context           │
    │  Output: filtered toolset (max 5)               │
    └─────────────────────────────────────────────────┘
```

---

## 3. Component Specifications

### 3.1 Zero-LLM Intent Router

**Purpose:** Prevent tool-set overload by filtering visible tools before they enter the LLM context window.

**Implementation:**
- Lightweight deterministic classifier. Zero LLM inference calls.
- Three dispatch mechanisms (in priority order):
  1. **JSON-RPC Method Pattern Match** — If user intent maps to a known MCP method prefix (e.g., `geox_*`, `fed_*`, `capital_*`), route to that domain's toolset.
  2. **Domain Tag Extraction** — Regex-based extraction of domain keywords from user message. Map to tool domains.
  3. **Session History Heuristic** — If current session has established a domain focus, bias toolset toward that domain.

**Constraints:**
- Latency budget: ≤5ms (sub-millisecond is target for regex/tag matching).
- Maximum tools exposed per turn: **N ≤ 5** (hard cap).
- If decomposition is required (task spans multiple domains), trigger multi-step decomposition rather than exposing >5 tools.

**Fallback:**
- If classifier confidence is ambiguous (multiple domain matches), default to **smallest viable toolset** (1-2 tools for most specific match) + emit `INTENT_ROUTER_AMBIGUOUS` audit event.

**Anti-pattern:**
- ❌ Using an LLM call to classify intent (moves judgment problem one layer down).
- ❌ Exposing full toolset as fallback when classifier is uncertain (defeats the purpose).

### 3.2 Per-Agent Role ACL

**Purpose:** Ensure each agent persona in a gotong-royong session sees only tools authorized for its role.

**ACL Structure:**

```toml
[roles]
333-AGI = {
  allowed_categories = ["read", "compute", "propose", "spawn"],
  blocked_categories = ["state-mutation", "high-impact-mutation"],
  max_tool_count = 5
}

555-ASI = {
  allowed_categories = ["read", "verify", "audit"],
  blocked_categories = ["state-mutation", "high-impact-mutation", "spawn"],
  max_tool_count = 3
}

888-APEX = {
  allowed_categories = ["read", "deliberate", "verdict", "seal"],
  blocked_categories = ["state-mutation"],
  max_tool_count = 5
}

A-FORGE = {
  allowed_categories = ["read", "execute-after-seal", "build", "deploy"],
  blocked_categories = ["unsealed-mutation"],
  max_tool_count = 5
}

Validator = {
  allowed_categories = ["read", "verify"],
  blocked_categories = ["state-mutation", "high-impact-mutation", "spawn", "execute"],
  max_tool_count = 3
}
```

**Enforcement:**
- Role ACL is resolved at gotong-royong session initialization.
- Orchestrator assigns tool masks per sub-agent based on role.
- Sub-agent context window receives only role-scoped tools. No exception.
- Flat policy (all tools for all agents) is explicitly prohibited.

**Integration with TOOL_RIGHTS_POLICY v0.2:**
- This ACL is the runtime enforcement of the existing Layer 3 (Rights Layer) defined in AAA_TOOL_RIGHTS_POLICY_v0.2 Section 2.
- Rights → ACL mapping is maintained in the policy config file, not hardcoded.

### 3.3 Custom MCP Reversibility Wrapper

**Purpose:** Inject governance metadata into MCP tool schemas where native MCP spec has none.

**arifOS Custom Headers:**

| Header | Type | Description |
|--------|------|-------------|
| `arifos_is_reversible` | `bool` | Can this action be undone? `true` = reversible, `false` = permanent mutation. |
| `arifos_impact_radius` | `int` (0–5) | How many downstream systems/state objects are affected? 0 = no state change, 5 = critical infrastructure. |
| `arifos_requires_888_hold` | `bool` | Does this require 888 Sovereign confirmation before execution? |
| `arifos_category` | `enum` | `read-only`, `compute`, `propose`, `state-mutation`, `high-impact-mutation` |
| `arifos_allowed_roles` | `list<str>` | Which agent roles may invoke this tool. Empty = 888 only. |

**Injection Point:**
- Headers are injected during tool registration / build-time, NOT at runtime.
- Each MCP server's tool schema is annotated with these headers in a sidecar manifest.
- The interceptor reads the manifest at startup and enforces accordingly.

**Default Classification:**

```
arifos_impact_radius    arifos_is_reversible    arifos_requires_888_hold    arifos_category
─────────────────────   ────────────────────    ─────────────────────────   ──────────────────────
0                       true                    false                       read-only
1                       true                    false                       compute
2                       true                    false                       propose
3                       false                   true                        state-mutation
4                       false                   true                        high-impact-mutation
5                       false                   true                        critical-mutation
```

**Fail-Safe Rule:**
- Any tool registered in an MCP server WITHOUT arifOS headers → auto-classified as `UNCHECKED_BLOCK`.
- Tool cannot be invoked until signed policy metadata is injected.
- This is the default: **unknown = blocked**, not unknown = allowed.

### 3.4 Governed Dynamic Policy Layer

**Purpose:** Allow policy config evolution without recompiling the immutable interceptor binary.

**Architecture:**

```
┌──────────────────────────────────────┐
│       IMMUTABLE ENGINE (Binary)      │
│  Rust/Go compiled interceptor        │
│  Stateless, no learning loop         │
│  Reads policy from disk/memory       │
│  Verifies cryptographic signature    │
│  Enforces rules deterministically    │
└──────────────────┬───────────────────┘
                   │ hot-reload signal (SIGHUP / file watch)
                   ▼
┌──────────────────────────────────────┐
│      DYNAMIC POLICY CONFIG           │
│  Format: TOML (primary) / JSON       │
│  Signed: Ed25519 (888 Sovereign)     │
│  Mutually signed: HMAC (DEV_KEY)     │
│  Hot-reloadable at runtime           │
└──────────────────────────────────────┘
```

**Cryptographic Hot-Reload Protocol:**

1. Policy file is updated and signed with Ed25519 key (888 Sovereign) or HMAC (DEV_KEY for delegated scope).
2. Interceptor receives SIGHUP or detects file change via inotify.
3. Interceptor reads new policy file.
4. Interceptor verifies cryptographic signature against stored public keys.
5. If signature is VALID → hot-reload new policy into RAM. Emit `POLICY_RELOAD_SUCCESS` audit event.
6. If signature is INVALID → reject new policy. Retain last-known-good config. Emit `POLICY_RELOAD_REJECTED` audit event.
7. If policy file is MISSING → retain last-known-good config. Emit `POLICY_FILE_MISSING` audit event.

**Delegated Authority Tiers:**

| Impact Radius | Signature Required | Authority |
|---------------|-------------------|-----------|
| ≤ 1 (read-only / compute) | HMAC with DEV_KEY | Autonomous — no sovereign hold |
| 2–3 (propose / state-mutation) | Ed25519 with 888 Sovereign Key | Sovereign hold required |
| 4–5 (high-impact / critical) | Ed25519 with 888 Sovereign Key + W_SCAR confirmation | Sovereign hold + epistemic floor |

**Fail-Safe Policy Fallback:**
- Unknown tools (no metadata in policy file) → `UNCHECKED_BLOCK`
- Expired signatures → `POLICY_STALE` flag, continue with last-known-good
- Corrupted policy file → `POLICY_CORRUPTED` alert, revert to compiled defaults

**Append-Only Audit Chain:**

Every policy event is logged to an immutable append-only file:

```json
{
  "timestamp": "2026-08-28T01:27:00+08:00",
  "event_type": "POLICY_RELOAD_SUCCESS",
  "policy_version": "1.2.0",
  "policy_hash": "sha256:a1b2c3d4...",
  "signature_algorithm": "ed25519",
  "signer": "888-SOVEREIGN",
  "trigger": "hot-reload",
  "previous_hash": "sha256:e5f6g7h8...",
  "delta_tools_added": 2,
  "delta_tools_modified": 1,
  "delta_tools_blocked": 0
}
```

- Chain integrity verified by checking each entry's `previous_hash` links to the prior entry's hash.
- Any tampering breaks the chain and emits `AUDIT_CHAIN_TAMPERED` alert.
- Chain file stored at: `/root/AAA/governance/audit/mcp-policy-audit-chain.jsonl`

---

## 4. Execution Flow

### 4.1 Normal Operation (Read-Only / Low-Risk)

```
User Message
    │
    ▼
[Zero-LLM Intent Router] ─── regex/tag/classify ──→ Filtered Toolset (≤5)
    │
    ▼
[LLM Context Window] ──── agent reasons + selects tool ──→ tool-call output
    │
    ▼
[MCP Reversibility Wrapper] ─── injects arifOS headers ──→ wrapped payload
    │
    ▼
[Deterministic Interceptor] ─── reads policy, checks reversibility ──→ APPROVED
    │
    ▼
[MCP Server] ──── executes ──→ result returned to agent
    │
    ▼
[Audit Log] ──── append event ──→ done
```

**Latency overhead:** ≤5ms (intent router) + ≤1ms (interceptor check) = **<6ms total governance overhead**.

### 4.2 High-Risk / Irreversible Operation

```
Agent tool-call output (irreversible, impact_radius ≥ 3)
    │
    ▼
[MCP Reversibility Wrapper] ─── is_reversible=false, requires_888_hold=true
    │
    ▼
[Deterministic Interceptor] ─── BLOCKS execution ──→ returns:
    │
    │   EXECUTION_BLOCKED
    │   reason: "Irreversible operation requires 888 Sovereign Hold"
    │   tool: "capital_ledger.write"
    │   impact_radius: 5
    │   reversibility: false
    │
    ▼
[Agent receives BLOCKED status] ─── must HOLD, cannot proceed
    │
    ▼
[Route to 888-APEX for verdict] ─── HOLD / VOID / SEAL
```

### 4.3 Gotong-Royong (Multi-Agent) Session

```
Orchestrator receives complex task
    │
    ▼
[Intent Router] ─── classifies multi-domain task ──→ triggers decomposition
    │
    ▼
[Orchestrator spawns sub-agents] ─── assigns role + ACL per agent
    │
    ├──→ Sub-Agent A (333-AGI, "scout")  ─── tools: [read, compute, propose]
    ├──→ Sub-Agent B (555-ASI, "verify") ─── tools: [read, verify, audit]
    └──→ Sub-Agent C (A-FORGE, "execute")─── tools: [read, execute-after-seal]
    │
    ▼
[Each sub-agent's context receives ONLY role-scoped tools]
    │
    ▼
[All tool-calls pass through Interceptor] ─── per-agent policy enforcement
    │
    ▼
[Results converge to orchestrator] ─── synthesis or 2-turn cap → Ω₀
```

---

## 5. Policy Config Schema

### 5.1 Primary Config: `mcp-governance-policy.toml`

```toml
# arifOS MCP Governance Policy
# Signed by: 888 Sovereign Key (Ed25519)
# Last modified: 2026-08-28T01:27:00+08:00
# Policy version: 1.0.0

[meta]
version = "1.0.0"
created = "2026-08-28"
signature_algorithm = "ed25519"
signer = "888-SOVEREIGN"
chain_hash = "sha256:genesis"

# ── Global Constraints ──

[global]
max_tools_per_turn = 5
intent_router_enabled = true
interceptor_enabled = true
audit_chain_path = "/root/AAA/governance/audit/mcp-policy-audit-chain.jsonl"
default_unknown_tool = "UNCHECKED_BLOCK"

# ── Tool Classifications ──

[tools]

[tools.fed_route]
arifos_is_reversible = true
arifos_impact_radius = 1
arifos_requires_888_hold = false
arifos_category = "compute"
arifos_allowed_roles = ["333-AGI", "555-ASI", "888-APEX", "A-FORGE", "Validator"]

[tools.fed_status]
arifos_is_reversible = true
arifos_impact_radius = 0
arifos_requires_888_hold = false
arifos_category = "read-only"
arifos_allowed_roles = ["333-AGI", "555-ASI", "888-APEX", "A-FORGE", "Validator"]

[tools.geox_claim]
arifos_is_reversible = false
arifos_impact_radius = 4
arifos_requires_888_hold = true
arifos_category = "high-impact-mutation"
arifos_allowed_roles = ["333-AGI"]

[tools.geox_basin]
arifos_is_reversible = true
arifos_impact_radius = 1
arifos_requires_888_hold = false
arifos_category = "read-only"
arifos_allowed_roles = ["333-AGI", "555-ASI", "A-FORGE", "Validator"]

[tools.capital_ledger]
arifos_is_reversible = false
arifos_impact_radius = 5
arifos_requires_888_hold = true
arifos_category = "critical-mutation"
arifos_allowed_roles = []  # 888 only

[tools.capital_indicator]
arifos_is_reversible = true
arifos_impact_radius = 1
arifos_requires_888_hold = false
arifos_category = "read-only"
arifos_allowed_roles = ["333-AGI", "555-ASI", "A-FORGE", "Validator"]

[tools.well_log_intake]
arifos_is_reversible = false
arifos_impact_radius = 3
arifos_requires_888_hold = true
arifos_category = "state-mutation"
arifos_allowed_roles = ["333-AGI"]

[tools.well_observe_machine]
arifos_is_reversible = true
arifos_impact_radius = 0
arifos_requires_888_hold = false
arifos_category = "read-only"
arifos_allowed_roles = ["333-AGI", "555-ASI", "A-FORGE", "Validator"]

[tools.generate_video]
arifos_is_reversible = true
arifos_impact_radius = 0
arifos_requires_888_hold = false
arifos_category = "compute"
arifos_allowed_roles = ["333-AGI", "A-FORGE"]

[tools.forge_execute]
arifos_is_reversible = false
arifos_impact_radius = 4
arifos_requires_888_hold = true
arifos_category = "high-impact-mutation"
arifos_allowed_roles = ["A-FORGE"]

# ── Intent Router Domain Mapping ──

[intent_router.domains]

[intent_router.domains.finance]
keywords = ["trading", "gold", "xauusd", "capital", "wealth", "market", "portfolio"]
tools = ["fed_route", "fed_status", "capital_indicator", "capital_ledger"]
priority = 1

[intent_router.domains.geoscience]
keywords = ["basin", "well", "geology", "seismic", "petrophysics", "subsurface", "geox"]
tools = ["geox_basin", "geox_claim", "geox_well", "geox_petrophysics"]
priority = 1

[intent_router.domains.wellness]
keywords = ["health", "wellness", "intake", "vitality", "well"]
tools = ["well_log_intake", "well_observe_machine", "well_assess_homeostasis"]
priority = 1

[intent_router.domains.media]
keywords = ["video", "image", "tts", "voice", "music", "generate", "media"]
tools = ["generate_video", "text_to_image", "text_to_audio"]
priority = 1

[intent_router.domains.system]
keywords = ["status", "health", "federation", "mcp", "tools", "audit"]
tools = ["forge_health_check", "forge_status", "forge_registry_status"]
priority = 2
```

### 5.2 Sidecar Manifest: `arifos-tool-metadata.json`

Per-MCP-server tool annotation file, generated at tool registration:

```json
{
  "server": "fed",
  "version": "1.0.0",
  "generated": "2026-08-28T01:27:00+08:00",
  "tools": {
    "fed_route": {
      "arifos_is_reversible": true,
      "arifos_impact_radius": 1,
      "arifos_requires_888_hold": false,
      "arifos_category": "compute"
    },
    "fed_status": {
      "arifos_is_reversible": true,
      "arifos_impact_radius": 0,
      "arifos_requires_888_hold": false,
      "arifos_category": "read-only"
    }
  }
}
```

---

## 6. Constitutional Floor Mapping

| Floor | Application in This RFC |
|-------|------------------------|
| **F1 AMANAH** | Policy file is signed. Unsigned mutations are blocked. Interceptor is immutable — no silent drift. |
| **F2 TRUTH** | Tool declarations must match live `tools/list`. Drift = F2 violation. Sidecar manifest is source of truth. |
| **F4 CLARITY** | One policy file, one audit chain, one interceptor binary. No stale copies. |
| **F11 AUDIT** | Append-only audit chain with cryptographic hash linking. Every policy reload logged. |
| **F13 SOVEREIGN** | Impact radius ≥ 3 tools require 888 Sovereign Key signature. No agent can self-authorize high-impact mutations. |

**New Floor Interaction:**

| Mechanism | Floor Enforcement |
|-----------|-------------------|
| Zero-LLM Intent Router | F2 (TRUTH) — prevents schema confusion that leads to false invocations |
| Per-Agent Role ACL | F13 (SOVEREIGN) — role boundaries are sovereign design decisions |
| Reversibility Wrapper | F1 (AMANAH) — irreversible actions require explicit sovereign confirmation |
| Dynamic Policy Layer | F11 (AUDIT) — every policy change is cryptographically signed and logged |

---

## 7. Implementation Roadmap

### Phase 1: Policy Schema + Audit Chain (Week 1)
- [ ] Define and validate `mcp-governance-policy.toml` schema
- [ ] Implement append-only audit chain writer (`audit_chain.py`)
- [ ] Generate sidecar manifests for all 15 MCP servers
- [ ] Test policy signing with Ed25519 keypair

### Phase 2: MCP Reversibility Wrapper (Week 2)
- [ ] Build tool annotation pipeline (inject arifOS headers at registration)
- [ ] Implement UNCHECKED_BLOCK default for unannotated tools
- [ ] Validate with existing MCP tools (FED, GEOX, WEALTH)

### Phase 3: Deterministic Interceptor (Week 3)
- [ ] Compile interceptor binary (Rust or Go)
- [ ] Implement policy file reader + signature verification
- [ ] Implement SIGHUP hot-reload protocol
- [ ] Load testing: verify <6ms governance overhead

### Phase 4: Zero-LLM Intent Router (Week 3-4)
- [ ] Implement regex/tag-based classifier
- [ ] Define domain keyword mappings
- [ ] Integration test: verify ≤5 tools exposed per turn
- [ ] Latency validation: ≤5ms budget

### Phase 5: Per-Agent Role ACL (Week 4)
- [ ] Implement role-scoped tool injection for gotong-royong sessions
- [ ] Integration with orchestrator spawn logic
- [ ] Test Validator-Agent receives zero mutation tools

### Phase 6: Constitutional Integration (Week 5)
- [ ] Wire interceptor into arifOS kernel execution path
- [ ] Update TOOL_RIGHTS_POLICY v0.2 to reference this RFC
- [ ] Update federation manifest with governance layer topology
- [ ] Full integration test: end-to-end governance flow

---

## 8. Risk Assessment

| Risk | Mitigation | Residual Risk |
|------|------------|---------------|
| Intent router miscategorizes domain | Default to smallest toolset + audit event | Low — false negative is safe, false positive triggers broader audit |
| Policy file corruption | Fail-safe to last-known-good + alert | Low — immutable binary retains compiled defaults |
| Interceptor binary has bugs | Static analysis + adversarial testing + immutable (no runtime mutation) | Medium — binary bugs require recompile + 888 re-seal |
| Latency overhead exceeds budget | Target <6ms; profiled at each phase; fallback to tool-count-only cap | Low — regex/tag matching is sub-millisecond |
| Gödel gap: who governs the interceptor? | Binary is immutable; policy changes require 888 signature; audit chain is append-only | Accepted — cannot eliminate self-reference; can only minimize attack surface |
| Delegated DEV_KEY scope creep | Scope is per-tool-category, not per-tool; 888 can revoke delegation | Low — revocation is a signed policy update |

---

## 9. Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-08-28 | Zero-LLM intent router | LLM-based routing moves judgment problem one layer down. Deterministic classifier is the only architecture that doesn't recurse. |
| 2026-08-28 | Per-agent role ACL over flat policy | Gotong-royong multi-agent sessions require different toolsets per role. Flat policy = all tools visible = False Confidence Paradox at agent level. |
| 2026-08-28 | Custom arifOS headers over native MCP | MCP spec does not carry governance metadata. Building on top of MCP is unavoidable. |
| 2026-08-28 | Immutable binary + dynamic signed config | Decouples runtime enforcement from policy evolution. Binary cannot drift. Config can evolve under cryptographic governance. |
| 2026-08-28 | Unknown = UNCHECKED_BLOCK (fail-safe) | Default must be deny, not allow. Safety first. Unknown tools cannot be invoked until explicitly classified and signed. |
| 2026-08-28 | Audit chain is append-only with hash linking | Tamper-evident. Any modification breaks the chain. Zero-drift observability. |

---

## 10. Decisions (Locked by 888 Sovereign — 2026-08-28)

| # | Question | Decision | Rationale |
|---|----------|----------|-----------|
| 1 | Interceptor Language | **Rust** (LOCKED) | Memory safety, zero GC pause, zero overhead, small binary footprint. Fits deterministic proxy interceptor. |
| 2 | Policy File Format | **TOML** (LOCKED) | Superior readability for hand-audit and 888 human inspection. JSON syntax too bracket-heavy for governance review. YAML rejected (ambiguous parsing). |
| 3 | DEV_KEY Scope Boundary | **impact_radius ≤ 1 AND is_reversible = true ONLY** (LOCKED) | Read-only/trivial tools only. Sebarang state mutation atau impact_radius > 1 wajib 888 Sovereign Key signature. Zero delegation untuk mutation ops. |
| 4 | Domain Expansion Roadmap | **Pilot FED + GEOX first, expand after 1-week clean audit** (LOCKED) | Rollout berperingkat. Audit chain log lari tanpa error selama 1 minggu baru unseal ke WEALTH, WELL, dan media tools. |
| 5 | Hermes Integration | **UDS (Unix Domain Socket) Proxy Shim** (LOCKED) | Interceptor sits as UDS proxy shim below Hermes execution layer. Hermes → intent routing → Proxy Interceptor filter/audit/mask → Target MCP Server. Hermes core architecture unchanged. Interceptor filters silently. |

---

> **DITEMPA BUKAN DIBERI ⚒️**  
> This RFC is a draft awaiting 888 Sovereign Seal.  
> No implementation begins until signed by Arif Fazil (F13).
