# Federation Orthogonality — Future State Model

> **Generated:** 2026-09-16 | **Status:** Working artifact, not sealed
> **Purpose:** What the federation looks like after Phase 0–4 complete
> **Companion to:** federation-orthogonality.md · federation-orthogonality-invariant-floor-mapping.md

## Current State (2026-09-16)

```
Runtime services:     45 active systemd units + 7 Docker containers
Skill inventory:      ~195 distinct (451 with mirrors)
Invariants (I-01–24): 8 LIVE / 13 CANON / 3 PROPOSED
EUREKA ledger:        19 entries (2 new this session)
Constitutional floors: F1–F13 all RATIFIED in code
Canon fragments:      2 new (orthogonality + invariant-floor-mapping)
```

## Target State (after Phase 4)

### Dimension 1: Interaction Planes (where work happens)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HUMAN PLANE                                 │
│  HERMES gateway + MCP + bridge + SOUL.md + RASA + Shadow           │
│  Primary: make reality legible to Arif                             │
│  Runtime: LIVE                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                      WORKSHOP PLANE                                 │
│  OpenClaw session runtime + subagent lifecycle + artifact synth     │
│  Primary: coordinate bounded agentic work                          │
│  Runtime: LIVE (role card pending disposition)                     │
├─────────────────────────────────────────────────────────────────────┤
│                       PROTOCOL PLANE                                │
│  A2A gateway (aaa-a2a.service) + agent cards + trace propagation   │
│  Primary: typed inter-organ task exchange                          │
│  Runtime: LIVE                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                    IMPLEMENTATION PLANE                              │
│  FI-001..FI-009 coding agents + change contracts + branch/PR/test  │
│  Primary: reversible machine changes under bounded authority        │
│  Runtime: LIVE                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Dimension 2: Governance Institutions (who authorises)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AAA                                         │
│  Cross-plane institution: consent verification, lease issuance,    │
│  progress witnessing, artifact validation, evidence disclosure,    │
│  intent routing, capability registry, surface guard                │
│  Touches: ALL FOUR PLANES                                          │
│  Port: :3001 | Service: aaa-mcp.service + aaa-a2a.service         │
├─────────────────────────────────────────────────────────────────────┤
│                       arifOS                                        │
│  Constitutional kernel: judgment, admissibility, verdict, seal gate│
│  Touches: ALL FOUR PLANES (admissibility check on every plane)    │
│  Port: :8088 | Service: arifos.service                             │
├─────────────────────────────────────────────────────────────────────┤
│                       VAULT999                                      │
│  Immutable witness: receipt chain, Merkle anchors, append-only     │
│  Touches: ALL FOUR PLANE outcomes (records what happened)          │
│  Storage: /root/VAULT999/ | chattr +i filesystem immutability     │
└─────────────────────────────────────────────────────────────────────┘
```

### Dimension 3: Execution Instruments (how work happens)

```
arifOS kernel   → judgment and seal
A-FORGE         → authorized execution after seal
WELL            → readiness/vitality constraints
GEOX            → physical/resource constraints
WEALTH          → consequence computation
HERMES gateway  → Telegram bridge + human interface
arifFLOW        → metabolism plane (observation, never judge/exec)
FED router      → federation routing
FRAME           → independent observer
```

## Phase-by-Phase Transition

### Phase 0 — Discover (current)

**What exists:**
- 2 canon fragments written (orthogonality + invariant-floor-mapping)
- 2 EUREKA entries recorded (AAA-as-institution + three-axis model)
- 122 skills inventoried on disk

**What's pending:**
- OpenClaw: dual-column capability mapping (their deliverable)
- Hermes: capability-to-existing-skill mapping (depends on OpenClaw data)
- Full skills_inventory.json generation
- Semantic duplicate cluster identification

**Exit criteria:** Every active skill has: owner, category, plane alignment, runtime status (LIVE/TARGET/PROPOSED), and canonical successor (if superseded).

### Phase 1 — Establish Common Primitives

**Targets (from contract §7.1):**

| Primitive | Current skill | Status |
|---|---|---|
| core/governance/constitutional-reflex | constitutional-floors skill | LIVE |
| core/primitives/action-classification | FED router action classes | PARTIAL |
| core/primitives/evidence-contract | evidence-contract references in AGENTS.md | CANON only |
| core/primitives/receipt-witness | vault999-writer + MerkleReceiptAnchor | LIVE |
| core/routing/intent-routing | FED router + FLAME | LIVE |
| core/routing/attention-budget | skill trigger system | PARTIAL |

**Gap:** evidence-contract and attention-budget are canon-only. Phase 1 wires them to runtime gates.

### Phase 2 — Orthogonalize Agent Packs

**Targets:**

| Pack | Target skills | Current state |
|---|---|---|
| HERMES pack | bridge-protocol + governed-uncertainty + relationship-kernel + hermes-rasa + human-meaning-membrane | ALL LIVE |
| OpenClaw pack | task-decomposition + subagent-lease + artifact-synth + reality-probing + escalation | PROPOSED (no skills exist) |
| A2A pack | agent-card-governance + a2a-task-contract + artifact-exchange + trace-propagation | PARTIAL (forge-mcp-a2a-agentic exists) |
| Coding-agent pack | change-contract + repo-context + implementation-tests + fault-injection + pr-migration | PARTIAL (forge-repo-intelligence + FORGE-ci-diagnose exist) |

**Key action:** OpenClaw pack is entirely new. Either create from scratch or identify existing skills that serve the same function under different names.

### Phase 3 — Archive Safely

**Targets:**
- Add alias redirects for superseded skills
- Run routing regression tests
- Archive 451→195 mirror deduplication
- Preserve rollback paths

### Phase 4 — Validate Emergent Behavior

**Tests:**

| Test | What it proves |
|---|---|
| Adversarial authority-bypass | No agent can mutate without going through the gate |
| Cross-agent trace propagation | trace_id survives handoffs across planes |
| Duplicate-skill routing | Two skills with same trigger don't create authority collision |
| Failure receipt tests | UNMEASURED/VOID/HOLD actually block downstream |
| Human-consent binding | Irreversible actions require explicit F13 approval |
| Attention load measurement | Agents load fewer skills after orthogonalization |

## What Success Looks Like

```
BEFORE (flat model):
  "Where does AAA fit?" → ambiguous, competes with planes
  "Which agent owns this?" → unclear, multiple overlap
  "Is this skill loaded?" → 451 skills, mirrors, no dedup

AFTER (three-axis model):
  "Where does AAA fit?" → institution axis, crosses all planes
  "Which agent owns this?" → plane + institution + instrument = exact coordinate
  "Is this skill loaded?" → 195 distinct, one canonical per capability
```

## Open Debt

| Debt | Owner | Status |
|---|---|---|
| OpenClaw role card disposition | OpenClaw | IN PROGRESS |
| Capability-to-skill mapping table | Hermes | BLOCKED on OpenClaw deliverable |
| 13 canon-only invariants not runtime-gated | AAA | Phase 1 target |
| 4 duplicate-owner skills (human merge decision) | Arif (F13) | PENDING |
| 451→195 mirror deduplication | Phase 3 | NOT STARTED |

DITEMPA BUKAN DIBERI ⚒️
