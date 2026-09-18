# CHRON Constitutional Verdict — 2026-09-18

> **Status:** FI-003 deep research synthesis (internal audit + cross-domain external research)
> **Authority:** DESIGN_VERDICT — sovereign approval required for implementation
> **Sources:** 31 prior artifacts, FRAME/arifFlow live code audit, 12-domain external literature, ChatGPT Deep Research contrast

---

## 1. The Core Diagnosis

**Context window is not temporal awareness — it's a sliding amnesia.**

LLMs reason about temporal concepts but have no persistent lived time, no institutional clock, no event ledger, no causal ordering across agents, no historical belief snapshots. Every inference operates in t=now. CHRON exists to fill this constitutional gap.

---

## 2. Do Not Combine — Three Timescales, Three Questions

| Organ | Question | Clock | Failure semantics |
|---|---|---|---|
| **FRAME** | "What appears to be true now?" | Observation cadence (minutes) | Must survive alone — independent witness |
| **arifFlow** | "How did evidence move through the institution?" | Execution cadence (seconds) | Must survive without CHRON — transport |
| **CHRON** | "What did we believe? What happened? Were we right?" | Consequence cadence (days-weeks-months) | May depend on arifFlow evidence |

**Why not combine:**
- If CHRON breaks → arifFlow preserves traces → CHRON reconstructs after recovery
- If temporal interpreter + evidence transport = same failure domain → circular dependency
- If FRAME absorbed into CHRON → CHRON self-certifies → violates no-self-certification principle

**The navigation triad:**
```
FRAME    ≈ x(t)          witnessed state
arifFlow ≈ transitions    movement / traces / receipts  
CHRON    ≈ history of x(t), belief(t), prediction(t), relevance(t)

Together: STATE × TIME × FLOW → INSTITUTIONAL TRAJECTORY
```

---

## 3. APEX Chain = Temporal Loop

The governance chain has an unmade temporal dimension:

```
BUILD   = now (we create)
VERIFY  = recent past (did it work?)
JUDGE   = present (should we proceed?)
SEAL    = irreversible commitment (this happened)
ACT     = near future (we execute)
WITNESS = distant future (was it right?)
```

Without CHRON: one-pass pipeline. With CHRON: learning cycle. CHRON is what makes the chain aware of itself across time.

---

## 4. Why MCP At All

MCP ≠ organ. MCP = standardized door through which agents discover and invoke capabilities.

**CHRON = temporal capability/runtime**
**MCP = agent-facing protocol surface**

Do NOT create `chron-mcp.service :18086` with another public endpoint/auth/registry. Instead:

```
Agent → MCP → arifOS gateway → route → CHRON internal capability
```

Separate runtime ≠ separate public protocol door.

---

## 5. CHRON MCP: 4 Tools + Resources

### Tools (agent-facing)

| Tool | Owns | Explicitly does NOT own |
|---|---|---|
| `chron_query` | NOW, AS_OF, DIFF, timeline, unresolved loops | general semantic memory |
| `chron_predict` | register prediction + confidence + verify_at | execution |
| `chron_reconcile` | expected vs observed, error classification, calibration | authoritative truth/seal |
| `chron_attend` | FULL / PULSE / SILENT recommendation | delivery |

### Resources (data surfaces)

```
chron://episode/{id}
chron://timeline/{subject}
chron://prediction/{id}
chron://as-of/{time}/{subject}
chron://open-loops
chron://calibration/{agent-or-source}
```

### Explicitly NOT built

```
chron_schedule    — uses systemd/cron
chron_send        — steals transport (arifFlow)
chron_execute     — steals execution (A-FORGE)
chron_seal        — steals authority (arifOS)
chron_memory      — steals memory (arif_memory)
chron_witness     — steals witness (FRAME)
chron_health_decide — steals health (WELL)
chron_route       — steals routing (AAA)
```

### Intake: NOT a public tool

Evidence flows organ-to-organ:
```
FRAME / GEOX / WELL / WEALTH / A-FORGE → arifFlow → CHRON
```
Not: `random agent → chron_remember("this is true")`

---

## 6. Canonical Ownership After CHRON

| Capability | Owner | CHRON relationship |
|---|---|---|
| Constitutional authority | arifOS | proposes only |
| Mutation/action | A-FORGE | links action to episode/prediction |
| Independent observation | FRAME | consumes witness evidence |
| Telemetry/receipt transport | arifFlow | consumes event stream |
| Perspective/claim semantics | HERMES | consumes validated claims |
| Agent/task routing | AAA | supplies priority/relevance |
| Earth evidence | GEOX | temporalizes observations |
| Capital evidence | WEALTH | temporalizes forecasts/outcomes |
| Human vitality evidence | WELL | temporalizes self-report/sensor state |
| Immutable final consequence | VAULT999 | references, does not replace |
| **Temporal episodes/beliefs/predictions** | **CHRON** | **exclusive owner** |

---

## 7. The 20 CHRON Invariants

1. **TIME MUST BE EXPLICIT.** No consequential temporal claim may depend only on LLM inferring "now," "recently," or date relationships from prose.
2. **EVENT TIME ≠ OBSERVATION TIME ≠ KNOWLEDGE TIME.** Preserve all independently. RELEVANCE_TIME may additionally be principal-specific.
3. **CAUSAL ORDER OUTRANKS WALL-CLOCK ORDER WHEN CLOCKS DISAGREE.** Preserve trace/parent relationships and late arrivals.
4. **HISTORY IS APPEND-ONLY.** Corrections create SUPERSEDES, RETRACTS or CORRECTS; never rewrite old belief history.
5. **FRAME WITNESSES; CHRON INTERPRETS.** CHRON cannot independently certify the observation used to validate its own prediction.
6. **arifFlow TRANSPORTS; CHRON DOES NOT.** CHRON failure must not prevent evidence from continuing to circulate.
7. **arifOS JUDGES; CHRON DOES NOT.** CHRON can propose lesson/policy candidates but cannot promote itself.
8. **A-FORGE ACTS; CHRON DOES NOT.** Temporal inference must not silently become mutation authority.
9. **HERMES OWNS PERSPECTIVE SEMANTICS.** Human report, agent inference and measured observation remain distinct.
10. **AAA ROUTES; CHRON PRIORITIZES.** "This matters now" ≠ "send this task to agent X."
11. **SCHEDULING ≠ TEMPORAL INTELLIGENCE.** CHRON may register deadlines and verification appointments; systemd/cron/workflow infrastructure fires them.
12. **MISSING ≠ FALSE.** UNKNOWN IS FIRST-CLASS.
13. **DELIVERED ≠ RECEIVED ≠ ATTENDED.** Preserve separate states.
14. **NO POLICY FROM ONE EPISODE.** Adaptation requires recurrence plus external outcome evidence.
15. **NO LEARNING WITHOUT EXOGENOUS EVIDENCE.**
16. **AS-OF RECONSTRUCTION MUST BE REPRODUCIBLE.** Same temporal basis + evidence version → same historical belief state.
17. **INGESTION MUST BE IDEMPOTENT.** Duplicate transport must not create duplicate episodes.
18. **UTC CANONICAL, LOCAL TIME PRESERVED.**
19. **LATE ARRIVAL IS NORMAL.** A fact may happen at T1, arrive at T3 and correct a belief formed at T2.
20. **SILENCE IS A VALID OUTPUT.** Attention optimization must be allowed to conclude SILENT.

---

## 8. CHRON Component Architecture

```
CHRON
├── Episode Builder        — FlowReceipt → ChronEpisode
├── Temporal Store         — event / observed / known / relevance time
├── Supersession Engine    — corrected / retracted / superseded
├── Temporal Query Engine  — NOW / AS_OF / DIFF / TIMELINE
├── Prediction Registry    — claim / confidence / verify_at
├── Reconciliation Engine  — expected ↔ observed
├── Calibration Engine     — per agent / source / domain
├── Attention Engine       — FULL / PULSE / SILENT
├── Graph Projector        — rebuildable Reality Graph
└── Adapters               — FRAME / arifFlow / HERMES / arifOS / AAA / A-FORGE
```

**What is absent (architectural quality):**
- No shell, no Telegram sender, no constitutional judge, no health oracle
- No generic RAG, no new scheduler, no new vector DB

---

## 9. Deprecation / Evolution Map

| Structure | Decision | Future role |
|---|---|---|
| systemd timers / crontab / Hermes cron | **KEEP** | execution clocks |
| custom CHRON scheduler | **DO NOT BUILD** | use existing scheduler substrate |
| `alpha_zen_engine.py` (dormant) | **DEPRECATE** after replacement proof | archive historical |
| `chron_personal/*` unwired drafts | **PARK** → archive | don't wire another producer |
| ALPHA-ZEN renderers | **EVOLVE** | presentation projections from canonical episode |
| Telegram delivery logic | **EVOLVE** | delivery transport, not CHRON cognition |
| arifFlow `/ingest`, FlowReceipts, FQ | **KEEP** | evidence transport |
| arifFlow "attention checkpointing" | **NARROW** | emit flow evidence; CHRON owns temporal relevance |
| FRAME probe/drift/trend | **KEEP** | witness primitives |
| any CHRON duplicate drift/trend probe | **DEPRECATE** | use FRAME |
| `arif_memory` | **KEEP** | governed semantic memory |
| CHRON duplicate generic memory API | **DO NOT BUILD** | CHRON owns episodic temporal history only |
| `carry_forward.json` | **EVOLVE** | cache/projection, never canonical history |
| Qdrant | **KEEP** | semantic retrieval index |
| FalkorDB | **KEEP** | reality-graph projection |
| VAULT999 | **KEEP** | immutable consequence/seal ledger |
| duplicated CHRON seal files | **COLLAPSE** | one seal/receipt owner |

---

## 10. Corrected Technical Decisions

### PostgreSQL bitemporal — NOT native

PG18 added temporal constraints (WITHOUT OVERLAPS, PERIOD) but system-versioned tables remain unsupported. Full native VALID TIME + SYSTEM TIME + AS OF reconstruction is not a built-in PG18 feature.

**Route:** Retain PostgreSQL with explicit episode/event tables (valid_from, valid_to, append-only). Evaluate XTDB later if temporal workload justifies it.

### Event Calculus = strongest formal foundation

Kowalski 1986. Built for CHRON's core question: "Which state changed because an event occurred?" Maps directly to CHRON's spine.

### Bitemporal KG = measurable performance

Zep/Graphiti bitemporal knowledge graphs: 92% on LongMemEval vs 63% for flat memory. Prediction errors restructure hippocampal memory (Nature 2021). Control theory confirms: separate fast/slow/rare time constants.

---

## 11. The Proof of Institutional Temporal Memory

An agent should eventually ask:

1. "What did we believe about this issue at 10:00 Tuesday, using only evidence that had entered by then?"
2. "What evidence arrived afterward?"
3. "What changed our belief?"
4. "What action did that belief cause?"
5. "What happened?"
6. "Were we calibrated?"

That is far more powerful than ordinary RAG. That is CHRON's ultimate proof.

---

## 12. What's Built vs What's Missing

| Component | Status |
|---|---|
| Bitemporal episode store | Code exists (chron_store.py) |
| Prediction with verify_at | Code exists (chron_prediction.py), 5 predictions live |
| Brier calibration | Code exists (chron_verify.py), needs data |
| Lesson extraction → policy | Code exists (chron_learn.py) |
| FRAME as independent witness | Integration code exists |
| Verification cron | **NOT WIRED** — needs systemd timer |
| Shared temporal substrate | **NOT WIRED** — arifFlow/FRAME don't write to CHRON yet |
| CHRON systemd service | **NOT BUILT** — CLI-only |
| NATS subscription | **NOT BUILT** — proposed subjects don't exist |
| MCP surface via arifOS gateway | **NOT BUILT** |

**The gap is wiring, not architecture.**

---

## 13. Organ Placement Decision (F13 SEAL 2026-09-18)

CHRON stays at `/root/chron/`. Not inside AAA. Same pattern as every other organ.

| Concept | Location | Why |
|---|---|---|
| TEMPORAL_ROOT | arifOS kernel envelope | Federation-wide coordinate, injected into every session |
| Temporal Contract schema | AAA docs | Federation invariant, referenced by all organs |
| CHRON organ | `/root/chron/` | Own repo, own port, own failure domain |
| Episodes, Predictions, Commitments, Consequences, Trajectories | `/root/chron/` | CHRON's 5 primitives |
| arifFlow | `/root/arifFlow/` | Metabolism, receipts, FQ |
| FRAME | `/root/FRAME/` | Independent witness |

**Rationale:** AAA is the registry (DISPLAY_ONLY). CHRON is the organ (TEMPORAL_COMPUTE). Putting CHRON inside AAA would be like putting GEOX inside AAA. AAA holds the spec; CHRON holds the consequence.

---

DITEMPA BUKAN DIBERI ⚒️
