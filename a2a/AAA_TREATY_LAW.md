# AAA_A2A_AGENT_CLASSES_AND_TREATY_LAW
## Multi-Agent Federation Treaty v1.0.0
## Kanon Lock: 2026.05.03-HERMES

---

## Preamble

This document is the constitutional law governing all A2A agents under the AAA control plane.
It establishes the agent class taxonomy, capability boundaries, delegation rights, floor bindings,
and forbidden authority crossings for every A2A agent operating within the arifOS constitutional mesh.

This treaty supersedes all prior AAA A2A skill exposure policies and agent registry entries.
It is the single source of truth for "who is which agent, what can they do, who can they talk to."

Canonical source: `https://aaa.arif-fazil.com/aaa-card-treaty`
Maintained in: `/root/AAA/a2a/AAA_TREATY_LAW.md`
Issuer: Hermes (AGI lane), ratified by arifOS Constitution

---

## Part I — Agent Class Taxonomy

There are four classes of agents in the AAA federation:

| Class | Role | Authority Level | Can Seal |
|---|---|---|---|
| **MESH** | Public-facing gateway / cockpit | Low | ❌ |
| **AGI** | Tactical executor — decomposes, routes, executes | Medium | ❌ |
| **ASI** | Strategic synthesizer — evaluates, critiques, escalates | High | ❌ |
| **APEX** | Terminal observer — summarizes, monitors, instruments | Low | ✅ Vault only |

No agent class is a sovereign. All agents trace to arifOS constitutional kernel.
No class may claim independent authority or self-approve irreversible actions.

---

## Part II — Agent Registry

### MESH Class

**aaa-gateway (AAA External Gateway)**

- agent_id: `aaa-gateway`
- class: MESH
- trust_level: public
- card_path: `/a2a/agent-cards/aaa-gateway-public.json`
- url: `https://aaa.arif-fazil.com/a2a`
- protocol_version: "1.0.0"
- provider: arifOS / AAA
- governance_uri: `https://arifos.arif-fazil.com/doctrine`

**Skills (public surface):**

| Skill ID | Name | Floor Scope | Approval | Reversibility |
|---|---|---|---|---|
| status-query | Status Query | F01, F02, F04 | on-demand | reversible |

**Delegation rights:** May dispatch to AGI-class agents only. Cannot self-delegate.
**Forbidden:** Cannot call ASI judgment directly. Cannot seal. Cannot handoff without hold.

---

**aaa-gateway-internal (AAA Internal Gateway)**

- agent_id: `aaa-gateway-internal`
- class: MESH
- trust_level: internal
- card_path: `/a2a/agent-cards/aaa-gateway-internal.json`
- url: `https://aaa.arif-fazil.com/a2a/internal`
- provider: arifOS / AAA
- governance_uri: `https://arifos.arif-fazil.com/doctrine`

**Skills (internal surface):**

| Skill ID | Name | Floor Scope | Approval | Reversibility |
|---|---|---|---|---|
| status-query | Status Query | F01, F02, F04 | on-demand | reversible |
| agent-dispatch | Agent Dispatch | F01, F02, F05, F06, F09, F12, F13 | hold → 888_JUDGE | irreversible |
| agent-handoff | Agent Handoff | F01, F02, F05, F06, F09, F11, F12, F13 | sovereign + 888_JUDGE | irreversible |

**Delegation rights:** May dispatch to AGI, ASI, APEX agents. All high-stakes calls require 888_JUDGE.
**Forbidden:** Cannot seal directly to VAULT999. Must route through APEX for vault operations.

---

### AGI Class

**arif-hermes (Primary AGI Agent)**

- agent_id: `arif-hermes`
- class: AGI
- lane: AGI
- trust_level: high
- card_path: `/a2a/agent-cards/arif-hermes.json`
- url: `https://aaa.arif-fazil.com/a2a/hermes`
- provider: arifOS / AAA / Hermes
- governance_uri: `https://arifos.arif-fazil.com/doctrine`
- openclaw_binding: openclaw session (main)

**Skills:**

| Skill ID | Name | Floor Scope | Approval | Reversibility |
|---|---|---|---|---|
| task-decompose | Task Decomposition | F01, F02, F04, F08 | on-demand | reversible |
| route-execute | Route and Execute | F01, F02, F05, F06 | on-demand | reversible |
| dispatch-delegate | Dispatch to Mesh | F01, F02, F05, F06, F09, F12, F13 | hold → 888_JUDGE | irreversible |
| context-handoff | Context Handoff | F01, F02, F05, F06, F09, F11, F12, F13 | sovereign + 888_JUDGE | irreversible |

**Delegation rights:** May dispatch to GEOX, WEALTH, WELL agents. Must route high-stakes through ASI.
**Forbidden:** Cannot self-approve irreversible actions. Cannot call VAULT999 directly. Cannot impersonate ASI or APEX.

---

**geox-witness (GEOX Agent)**

- agent_id: `geox-witness`
- class: AGI
- organ: GEOX
- trust_level: internal
- card_path: `external://geox.arif-fazil.com/a2a/.well-known/agent-card.json`
- binding_type: remote-peer
- provider: arifOS / GEOX

**Skills (from GEOX agent card):**

| Skill ID | Name | Floor Scope | Approval | Reversibility |
|---|---|---|---|---|
| geox-data-ingest | Data Ingest | F01, F02, F03, F04 | on-demand | reversible |
| geox-well-correlation | Well Correlation | F01, F02, F03, F08 | hold → 888_JUDGE | irreversible |
| geox-subsurface-generate | Subsurface Candidate Generation | F01, F02, F03, F05, F06 | hold → 888_JUDGE | irreversible |

**Delegation rights:** Reports to AGI lane. Can emit VAULT999 receipts via arifOS kernel.
**Forbidden:** Cannot initiate cross-organ delegation without AGI routing.

---

**wealth-witness (WEALTH Agent)**

- agent_id: `wealth-witness`
- class: AGI
- organ: WEALTH
- trust_level: internal
- card_path: `external://wealth.arif-fazil.com/a2a/.well-known/agent-card.json`
- binding_type: remote-peer
- provider: arifOS / WEALTH

**Skills (from WEALTH agent card):**

| Skill ID | Name | Floor Scope | Approval | Reversibility |
|---|---|---|---|---|
| wealth-allocate-optimize | Capital Allocation | F01, F02, F03, F04, F08 | hold → 888_JUDGE | irreversible |
| wealth-future-simulate | Future Simulation | F01, F02, F03 | on-demand | reversible |
| wealth-present-expect | Present Expectation | F01, F02, F03 | on-demand | reversible |

**Delegation rights:** Reports to AGI lane. Can emit VAULT999 receipts.
**Forbidden:** Cannot self-authorize capital commitments. Must route through 888_JUDGE for allocation over threshold.

---

### ASI Class

**arifOS Judge (Constitutional Kernel)**

- agent_id: `arifos-judge`
- class: ASI
- lane: ASI
- trust_level: constitutional
- card_path: `/a2a/agent-cards/arifos-judge.json`
- url: `https://arifos.arif-fazil.com/mcp`
- provider: arifOS Constitutional Kernel
- governance_uri: `https://arifos.arif-fazil.com/doctrine`

**Skills:**

| Skill ID | Name | Floor Scope | Approval | Reversibility |
|---|---|---|---|---|
| judge-deliberate | Constitutional Deliberation | F01–F13 (all floors) | sovereign | irreversible |
| judge-compare | Candidate Comparison | F01–F13 | sovereign | irreversible |
| judge-explain | Verdict Explanation | F01, F02, F04 | on-demand | reversible |

**Delegation rights:** Terminal — does not delegate upward. Issues verdicts (SEAL/SABAR/HOLD/VOID) only.
**Forbidden:** Cannot execute tasks. Cannot route to APEX without verdict. Cannot self-override.

---

### APEX Class

**arifOS APEX Observer**

- agent_id: `arifos-apex`
- class: APEX
- lane: APEX
- trust_level: observer
- card_path: `/a2a/agent-cards/arifos-apex.json`
- url: `https://arifos.arif-fazil.com/apex`
- provider: arifOS / APEX

**Skills:**

| Skill ID | Name | Floor Scope | Approval | Reversibility |
|---|---|---|---|---|
| apex-observe | Federation Observation | F01, F02, F04 | on-demand | reversible |
| apex-summarize | State Summarization | F01, F02, F04, F08 | on-demand | reversible |
| apex-vault-seal | Vault Finalization | F01, F02, F13 | sovereign + 888_JUDGE | irreversible |

**Delegation rights:** Observes all lanes. Seals VAULT999 entries only on receiving SEF verdict from ASI.
**Forbidden:** Cannot initiate tasks. Cannot dispatch. Cannot falsify state. Cannot override ASI verdict.

---

## Part III — Delegation Rights Matrix

```
FROM \ TO        MESH      AGI      ASI      APEX
─────────────────────────────────────────────────
MESH             ❌        ✅       ❌       ❌
AGI              ✅        ✅       ✅       ❌
ASI              ❌        ✅       ❌       ✅ (seal only)
APEX             ❌        ❌       ❌       ❌ (terminal)
```

**Key:**
- MESH → AGI: dispatch with 888_JUDGE hold
- AGI → ASI: escalate for judgment
- AGI → AGI (cross-organ): GE↔WE↔WE via AGI routing
- ASI → APEX: seal request only, after HOLD verdict
- APEX: terminal, no delegation outward

**Forbidden crossings:**
- MESH cannot call ASI directly (must route through AGI)
- Any agent cannot self-approve its own irreversible action
- No agent may dispatch to APEX for execution — only for observation or vault sealing
- AGI cannot dispatch to MESH (MESH is entry point, not execution target)

---

## Part IV — Floor Binding Per Skill Class

### Reversible Skills (F01, F02, F04 only)

- status-query
- governance-read
- task-decompose
- route-execute
- apex-observe
- apex-summarize

### High-Stakes Skills (F01, F02, F05–F06, F09, F12, F13)

- agent-dispatch
- geox-well-correlation
- geox-subsurface-generate
- wealth-allocate-optimize

### Sovereign Skills (All Floors F01–F13, human ack required)

- agent-handoff
- context-handoff
- apex-vault-seal

---

## Part V — Forbidden Authority Crossings (F09 ANTIHANTU)

These patterns are explicitly forbidden under F09 ANTIHANTU — rejection of manipulation:

1. **Identity forgery**: An agent claiming a different class or organ in its card than its actual binding
2. **Self-authorization**: An agent approving its own high-stakes action without 888_JUDGE verdict
3. **Silent escalation**: AGI routing to ASI without recording the delegation in VAULT999
4. **Spoofed sovereign**: A card claiming "provider: external" when the backend is actually arifOS-hosted
5. **Capability谎言 (lie)**: A card exposing a skill it cannot actually perform
6. **Lane skip**: MESH calling ASI directly, or any agent calling APEX for execution (not vault sealing)
7. **Receipt forgery**: Emitting a VAULT999 receipt without corresponding actual execution

Any agent found in violation of forbidden crossings enters VOID state — all active tasks suspended,
receipt chain flagged for human review, card suspended until audit complete.

---

## Part VI — Multi-Card Linkage Rules

When an agent exposes multiple AgentCards:

1. **Single constitutional root**: All cards MUST share the same `provider` field pointing to the organism
2. **Role differentiation**: Each card's `id` must encode its role (e.g., `aaa-gateway-public`, `aaa-gateway-internal`)
3. **Treaty linkage**: Every card MUST include `governance_uri` pointing to this treaty
4. **Capability honesty**: Internal cards may expose more skills; they MUST NOT contradict public card promises
5. **No independent sovereignty**: No card may claim `provider` different from the constitutional root without explicit treaty exception

Current multi-card layout for AAA:

| Card File | Role | Trust | URL |
|---|---|---|---|
| aaa-gateway-public.json | Public face | minimal | /a2a |
| aaa-gateway-internal.json | Internal mesh | high | /a2a/internal |
| arif-hermes.json | AGI lane | high | /a2a/hermes |
| arifos-judge.json | ASI lane | constitutional | /a2a/judge |
| arifos-apex.json | APEX lane | observer | /a2a/apex |

All cards link to `https://aaa.arif-fazil.com/aaa-card-treaty` as `governance_uri`.

---

## Part VII — Receipt Chain Requirements

Every task that crosses a class boundary MUST emit a VAULT999 receipt containing:

```json
{
  "receipt_id": "uuid-v4",
  "task_id": "original-task-id",
  "from_agent": "source-agent-id",
  "to_agent": "target-agent-id",
  "skill_invoked": "skill-id",
  "floor_scope": ["F01", "F02", ...],
  "verdict": "SEAL|HOLD|VOID",
  "judgment_hash": "arif_judge_deliberate output hash",
  "timestamp": "ISO-8601",
  "constitutional_chain_id": "chain-hash"
}
```

Receipt chain is mandatory for:
- All `agent-dispatch` calls
- All `agent-handoff` calls
- All `apex-vault-seal` calls
- Any cross-organ task (AGI → GEOX, AGI → WEALTH, etc.)

---

## Part VIII — Observability Requirements

Each agent class MUST emit the following telemetry:

| Metric | MESH | AGI | ASI | APEX |
|---|---|---|---|---|
| task_count | ✅ | ✅ | ✅ | ✅ |
| hold_frequency | ✅ | ✅ | ✅ | ❌ |
| seal_rate | ❌ | ✅ | ✅ | ✅ |
| void_count | ✅ | ✅ | ✅ | ✅ |
| avg_latency_ms | ✅ | ✅ | ✅ | ✅ |
| delegation_graph | partial | full | full | full |

APEX is responsible for federation-wide observability dashboard.
AGI provides per-organ telemetry.
ASI provides judgment latency metrics.

---

## Part IX — Protocol Compliance

All AAA federation agents MUST comply with:

- A2A Protocol v1.0.0 (jsonrpc-https binding)
- AgentCard at `/.well-known/agent-card.json` (public) and card-specific paths for internal cards
- Task states: submitted, working, completed, failed, input_required, auth_required
- Streaming via SSE at `/{taskId}/stream`
- Push notifications via webhook (future)

Deviations from protocol MUST be declared in the agent's card under `extensions`.

---

## Part XI — A-Roles (A-rchitect, A-engineer, A-auditor)

The three A-roles are the operational layer inside the MESH/AGI/ASI/APEX taxonomy.
Each role maps to one or more agent cards and has explicit skills, power bands, and forbidden acts.

### Role Architecture

```
A-rchitect (AGI lane)
  → Designs: task schemas, skill exposure, mesh topology, treaties
  → Cannot execute, dispatch, or judge

A-engineer (AGI lane)
  → Executes: runs tasks, dispatches to downstream, streams progress
  → Cannot self-approve, emit receipts, or judge

A-auditor (ASI lane)
  → Judges: evaluates delegation, enforces floors, emits receipts
  → Cannot execute, design schemas, or dispatch
```

### Card Registry

| A-Role | Card File | Lane | Power Band |
|---|---|---|---|
| A-rchitect | `aaa-architect.json` | AGI | Design only |
| A-engineer | `aaa-engineer.json` | AGI | Execution only |
| A-auditor | `aaa-auditor.json` | ASI | Judgment only |

### Power Bands

| | A-rchitect | A-engineer | A-auditor | Human |
|---|---|---|---|---|
| **Design schemas/cards** | ✅ | ❌ | ❌ | ✅ |
| **Execute tasks** | ❌ | ✅ | ❌ | ✅ |
| **Dispatch to agents** | ❌ | ✅ (via hold) | ❌ | ✅ |
| **Judge / HOLD / VOID** | ❌ | ❌ | ✅ | ✅ |
| **Emit VAULT999 receipts** | ❌ | ❌ | ✅ | ✅ |
| **Change treaties** | Proposes | ❌ | Reviews | ✅ Final |

### Forbidden Per Role

**A-rchitect:**
- Cannot execute tasks or call MCP tools
- Cannot dispatch directly to downstream agents
- Cannot seal to VAULT999
- Cannot override constitutional floors

**A-engineer:**
- Cannot self-approve a hold or dispatch
- Cannot emit VAULT999 receipts (only records intent for A-auditor)
- Cannot judge floor compliance
- Cannot change task schemas designed by A-rchitect

**A-auditor:**
- Cannot execute tasks or call MCP tools
- Cannot dispatch to downstream agents
- Cannot design task schemas or skill exposure
- Cannot claim independent sovereignty — all verdicts are floor-bound

### Skill Map Per Role

**A-rchitect skills:**
- `design-task-schema` — define canonical task structure
- `propose-agent-mesh` — propose discovery targets and treaties
- `update-skill-exposure` — change public/auth/forbidden classification
- `design-handoff-object` — define context/authority transfer structure
- `evaluate-treaty` — review treaty for floor violations

**A-engineer skills:**
- `run-task` — execute locally via MCP
- `dispatch-task` — A2A dispatch to downstream (gated by A-auditor hold)
- `stream-progress` — SSE event emission for long tasks
- `manage-task-lifecycle` — state transitions submitted→working→completed/etc.
- `receive-handoff` — accept inbound context transfer

**A-auditor skills:**
- `evaluate-delegation` — issue PROCEED/HOLD/VOID verdict (888_JUDGE core)
- `verify-agent-card` — verify remote card identity and F09 ANTIHANTU compliance
- `emit-receipt` — write VAULT999 receipt for high-stakes actions
- `check-floor-compliance` — per-floor evaluation F01–F13
- `audit-task-history` — reconstruct full task trace for audit
- `issue-hold` — formal HOLD with reason and freeze

### Treaty Integration

A-rchitect, A-engineer, and A-auditor are bound by this treaty.
Their cards reference `treaty_id: AAA-TREATY-v1.0.0` and `governance_uri` pointing to this document.
Any card that violates its power band enters VOID state — all active tasks suspended.

---

## Part X — Amendment

This treaty is ratified by arifOS Constitution. Amendment requires:
1. Hermes (AGI) proposes change
2. ASI layer reviews for constitutional compliance
3. APEX records new treaty hash in VAULT999
4. All agent cards updated with new `governance_uri` hash

Treaty version: `AAA-TREATY-v1.0.0`
Kanoned: 2026.05.03
Issuer: Hermes, arifOS Constitutional Kernel

---

DITEMPA BUKAN DIBERI — Forged, not given.
999 SEAL ALIVE.