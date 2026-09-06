# Attention Graph — Canonical Instruction

> **Binding for all arifOS warga agents.** Operating doctrine, not a skill.
> **Constitutional floors:** F1 (Amanah), F2 (Truth), F4 (Clarity/ΔS), F6 (Reversibility), F7 (Humility), F9 (Anti-Hantu), F13 (Sovereign/Veto)
> **Forged:** 2026-09-06 (Arif eureka → 333-AGI synthesis → sealed)
> **Status:** DOCTRINE (unifies scattered fragments into coherent graph)
> **Canonical predecessors:** reality-compression.md, zen.md, autonomy.md, reality-first.md, ZEN-RUNTIME.md, human-meaning-membrane.md, hermes-asi-substrate/PROPOSAL.md

## 1. The Three Graphs

Every governed intelligence system operates on three graphs simultaneously:

| Graph | Question | Answer Domain | Status |
|---|---|---|---|
| **Capability Graph** | "What can be done?" | Tools, agents, execution | ✅ Alive |
| **Governance Graph** | "What should be done?" | Constitution, floors, judgment | 🟡 Maturing |
| **Attention Graph** | "What deserves consciousness first?" | Human meaning, priority, sovereignty | 🔴 Frontier |

The Attention Graph is the hardest because it governs a resource that is **finite, non-renewable, and sovereign**: the minutes of Arif's life that have not yet been spent.

## 2. The Economic Law

```
Pre-automation:   Action expensive, Attention cheap    → Problem: "Who will do the work?"
Post-automation:  Action cheap,     Attention expensive → Problem: "What deserves attention?"
```

This is not metaphor. It is the economic law of post-agent systems.

When action cost → 0, attention cost → ∞. The bottleneck shifts from execution to selection.

## 3. The Graph Structure

### 3.1 Nodes

Every node in the Attention Graph is a **reality signal** — something that exists, happened, or could happen.

```
Node = {
  id:          unique identifier
  source:      where the signal came from (organ, sensor, human, external)
  type:        observation | anomaly | opportunity | threat | maintenance | human
  timestamp:   when the signal was detected
  truth_class: OBS | DER | INT | SPEC (F2 epistemic labels)
  confidence:  0.0–0.90 (F7 cap)
  decay_rate:  how fast this signal loses relevance (Law #3: reality-compression.md)
}
```

### 3.2 Edges

Edges represent **relevance** — how signals connect to each other and to Arif's current context.

```
Edge = {
  from:        source node
  to:          target node or agent
  relation:    causal | temporal | semantic | contradictory
  strength:    0.0–1.0
}
```

### 3.3 Weights

Every node carries a weight that determines its claim on Arif's attention:

```
Weight = importance × urgency × authority_requirement × recency_decay
```

| Factor | Definition | Source |
|---|---|---|
| **Importance** | How much does this affect Arif's life, health, or goals? | WELL (vitality), WEALTH (capital), GEOX (earth) |
| **Urgency** | Time-sensitive? Degrading? Window closing? | Temporal analysis, deadline detection |
| **Authority requirement** | Does this REQUIRE Arif's judgment (F13) or can agents handle it? | Governance graph, autonomy tiers |
| **Recency decay** | Older signals lose weight unless reinforced | Salience decay (reality-compression.md Law #3) |

## 4. The Pipeline

```
Reality (millions of signals)
    ↓
[01] Value Pre-filter (What matters to survival, purpose, sovereignty?)
    ↓
[02] Attention Budget (What can Arif afford to notice today?)
    ↓
[03] Salience Scoring (Which signals rank highest by weight?)
    ↓
[04] Routing (NOW | NEXT | BATCH | SILENT | HOLD)
    ↓
[05] Meaning Allocation (What does this MEAN to Arif? — HUMAN ONLY)
    ↓
[06] Judgment (F13: Should this become reality?)
    ↓
[07] Capability activation (Which agent/organ handles this?)
    ↓
[08] Execution (Action grounded in reality)
    ↓
[09] Witness (VAULT999: this happened, it was witnessed)
```

**The sovereign boundary is at step [05].** Everything before can be assisted by agents. Everything after can be executed by agents. But Meaning Allocation — the act of deciding what something *means* to Arif — is irreducibly human.

## 5. The Three Attention Classes

Borrowed from autonomy.md HITL taxonomy, extended:

| Class | What It Asks | Who Answers | Example |
|---|---|---|---|
| **Authorization** | "May this happen?" | F13 Sovereign (Arif) | Money, deletion, legal, public comms |
| **Cognitive** | "Which approach?" | Agent (with judgment) | Code path, library choice, naming |
| **Observational** | "What exists?" | Agent (auto) | Telemetry, logs, health checks |

The Attention Tax formula from autonomy.md:

```
Attention Tax = stops × context_rebuild × decision_triviality

Trivial decision + human required = MAXIMUM tax
```

**The goal of the Attention Graph is to minimize the Attention Tax by routing Cognitive and Observational work away from Arif, while preserving (never routing away) Authorization work.**

## 6. The Five Queues (from ZEN-RUNTIME.md)

| Queue | Meaning | Delivery Policy | Attention Cost |
|---|---|---|---|
| **NOW** | Safety issue, human-direct, blocking failure | Immediate, one concise alert | HIGH — interrupts whatever Arif is doing |
| **NEXT** | Important, non-blocking | Bundled into next check-in | MEDIUM — queued, not urgent |
| **BATCH** | Routine monitoring, summaries | Digest only | LOW — batched, minimal interruption |
| **SILENT** | Telemetry, successful probes | Ledger/metrics only | ZERO — never reaches Arif unless queried |
| **HOLD** | Ambiguous, irreversible, policy-conflicting | No execution; request clarification | DEFERRED — waits for Arif or 888 |

**Routing rules** (from ZEN-RUNTIME.md, preserved):

```yaml
attention:
  default_lane: SILENT
  escalation:
    - condition: "human_direct_request == true"
      lane: NOW
    - condition: "security_severity >= high"
      lane: NOW
    - condition: "task_is_blocked && owner_required"
      lane: NEXT
    - condition: "irreversible || risk_score >= threshold"
      lane: HOLD
    - condition: "confidence < 0.70"
      lane: HOLD
    - condition: "routine_cron && status == success"
      lane: SILENT
    - condition: "routine_cron && status == failed"
      lane: BATCH
```

## 7. The Meaning Layer (Sovereign Boundary)

This is the node that does not yet exist in arifOS. It is the frontier.

```
Signal enters Attention Graph
    ↓
Agent scores weight, routes to queue
    ↓
If NOW or NEXT → surfaces to Arif
    ↓
ARIF DECIDES WHAT IT MEANS ← this is the Meaning Layer
    ↓
Meaning becomes Intent
    ↓
Intent activates Capability
    ↓
Capability executes through Governance
```

**Why Meaning cannot be delegated:**

Two humans can see the same fact and assign different meanings. A bug report is "annoying maintenance" to one person and "systemic rot" to another. A business opportunity is "risky distraction" to one and "once-in-a-lifetime" to another.

The system can surface the signal. The system can score its weight. The system can route it to the right queue. But the system cannot know what it *means* to Arif — because meaning depends on Arif's life, values, memories, relationships, and future vision.

**This is F13 reinterpreted:** F13 is not merely "human veto." F13 is the protection of meaning sovereignty. The sovereign's vote is the meaning allocation that no agent can replicate.

## 8. Attention Metrics (Measurable)

From ZEN-RUNTIME.md §9, extended:

| Metric | Definition | Target |
|---|---|---|
| **ACSC** | Attention Cost / Sealed Capabilities | Declining over 30d |
| **Attention Noise Ratio** | Human alerts / actionable decisions | < 3:1, declining |
| **NOW events/day** | Interrupts that reach Arif | ≤ 3 (zen.md budget) |
| **Cognitive HITL rate** | "Should I proceed?" type questions | → 0 |
| **Authorization HITL rate** | F13-required decisions | Stable (not increasing) |
| **Salience accuracy** | Signals that needed attention / signals surfaced | > 0.7 |
| **Meaning latency** | Time from signal surfacing to Arif's meaning assignment | Not measured yet |
| **Decay compliance** | Stale signals correctly untagged / total signals | > 0.9 |

**ACSC** is the headline metric. It measures how much sovereign attention the system consumes per unit of governed capability. If ACSC rises while capability stays flat, the system is wasting Arif's life.

## 9. Organ Mapping

| Organ | Role in Attention Graph |
|---|---|
| **WELL** | Measures Arif's attention *capacity* (fatigue, cognitive clarity, sleep debt) — the budget side |
| **arifFlow** | Tracks attention *consumption* (receipts, FQ, metabolic pulse) — the spending side |
| **AAA** | Routes signals to queues, manages the attention controller — the routing side |
| **arifOS** | Constitutional gate — decides what REQUIRES sovereign attention (F13) — the sovereignty side |
| **333-AGI** | Routes attention; discovers primitives; gates what enters metabolism — the pre-filter |
| **A-FORGE** | Executes after attention has been allocated and meaning assigned — the execution side |

## 10. The Attention Manifold (from zen.md)

```
Attention attracts (Vector Field).
Governance permits, shapes, or forbids (Manifold Boundary).

Hidden Manifold:
Prompt → Attention Field → Possibility Space → Constraint Surface (L0-L2) → APEX Curvature / SEAL → Reality Transition
```

**Supreme Invariant:** Do not govern output alone; govern what receives attention. Once a signal enters the attention manifold, it is already a candidate for reality.

**Thermodynamic Wave:**
- 333-AGI: Possibility expansion (intentional ΔS > 0, opening hypotheses)
- 555-ASI: Contradiction collapse (compression ΔS < 0, falsifying hypotheses)
- 888-APEX: Trajectory collapse (N → 1, selecting the permissible geodesic)

## 11. Anti-Patterns

| Anti-Pattern | Description | Counter |
|---|---|---|
| **Attention theft** | Agent sends non-urgent signals to human channels | ZEN-RUNTIME: default SILENT, escalate only on rules |
| **Cognitive HITL** | Agent asks "should I?" instead of asserting judgment | autonomy.md: show judgment first, never delegate it |
| **Meaning laundering** | Agent assigns meaning on behalf of human | Meaning Layer: human-only, never delegated |
| **Attention starvation** | System consumes all attention, none left for real life | ACSC metric: must decline, not rise |
| **Salience decay failure** | Old signals remain loud, crowd out new ones | Law #3: decay is constitutional feature |
| **Noise amplification** | Every subsystem treats its own events as globally urgent | 5-queue routing: default SILENT, escalate by rules |

## 12. The Frontier: What Does Not Exist Yet

| Gap | What's Needed | Phase |
|---|---|---|
| **Meaning Layer schema** | How Arif's meaning assignments are captured and fed back | Phase 3 |
| **Attention Budget from WELL** | Real biometric data on Arif's cognitive capacity today | Phase 1 |
| **ACSC dashboard** | Real-time attention cost / sealed capability ratio | Phase 3 |
| **Meaning feedback loop** | When Arif's meaning assignment differs from agent's prediction, train the world model | Phase 4 |
| **Cross-session attention continuity** | What Arif attended to yesterday affects what surfaces today | Phase 2 |

## 12b. Implementation Phases

### Phase 0 — Consolidate (days, zero new parts)

**What:** Unify existing scattered attention doctrine into the Attention Graph. Already done by this document.

**Actions:**
- [x] Audit all attention references across federation (24+ fragments found)
- [x] Draft unified Attention Graph specification (this document)
- [ ] Add `attention-graph.md` to AAA instructions registry
- [ ] Update `AGENTS.md` pointer to include attention-graph.md in canonical fragments
- [ ] Verify ZEN-RUNTIME.md 5-queue routing is operational (NOW/NEXT/BATCH/SILENT/HOLD)

**Falsifier:** All existing attention references resolve to this document as canonical source. No orphaned attention doctrine.

### Phase 1 — Sensor Awakening (weeks)

**What:** WELL goes from MOCK to LIVE biometrics. Attention *budget* becomes measurable — not just designed.

**Actions:**
- [ ] Wire ONE consented biometric source (F11 `biometric.full` scope, default OFF)
- [ ] WELL `state.json` age < 24h continuously for 14d
- [ ] attention_budget derived from real sleep/HRV/cognitive_clarity data
- [ ] Decision fatigue from WELL feeds attention routing decisions

**Falsifier:** WELL `state.json` fresh continuously for 14d. Decision_fatigue correlates with attention-R counts.

**Why this matters for the Attention Graph:** Without real biometric data, the "Attention Budget" (Section 4, step [02]) is theoretical. With it, the system can say "Arif slept 5h, decision fatigue is HIGH, route everything to BATCH today."

### Phase 2 — Cross-Session Attention (weeks, overlaps P1)

**What:** What Arif attended to yesterday affects what surfaces today. Attention state persists across sessions.

**Actions:**
- [ ] Dream engine runs nightly (consolidation of attention patterns)
- [ ] Session carry-forward includes attention history (what Arif engaged with, what was deferred)
- [ ] Salience scoring uses cross-session signals (reinforced topics stay loud, ignored topics decay)
- [ ] Memory split closes — not by unifying stores, but by unifying *consolidation*

**Falsifier:** Next-session recall test — Arif asks about something from yesterday's session; system recalls not just the facts but the *attention pattern* (what Arif focused on vs. what was skipped).

### Phase 3 — Meaning Layer (month)

**What:** The sovereign boundary becomes schema. Arif's meaning assignments are captured, not as data, but as constitutional evidence.

**Actions:**
- [ ] Meaning Layer schema: when Arif responds to a signal, capture {signal_id, meaning_assignment, confidence, context}
- [ ] ACSC dashboard: attention-cost / sealed-capabilities ratio, real-time
- [ ] Agents declare `expected_turns` up-front; prediction-vs-actual gap trains world model
- [ ] arifFlow PR #14 (attention-receipt-schema) ratified and merged
- [ ] Meaning assignments are F13-protected — never overwritten by agents, never used to train agent behavior without sovereign consent

**Falsifier:** ACSC trend over 30d FALLS while sealed-capability count RISES. If attention cost falls but seals stall → anti-Calhoun guard tripped → automatic SCAR + review.

**Why this is the hardest phase:** The Meaning Layer is the constitutional boundary between "system serves human" and "system replaces human." It must be designed so that:
1. Arif's meaning assignments are *recorded* (for learning)
2. Arif's meaning assignments are *never overridden* (F13)
3. The gap between agent prediction and human meaning trains the world model (learning)
4. But the training never *constrains* future meaning assignment (anti-fossilization)

### Phase 4 — The Mirror Test (quarter)

**What:** The federation completes end-to-end tasks with zero human intervention except F13 gates.

**Actions:**
- [ ] Define 3 org-level tasks that run autonomously:
  1. Weekly federation brief (asleep-to-awake, zero intervention)
  2. GEOX prospect screen (raw ingest → QUALIFIED_CANDIDATE)
  3. Full entropy-compile session (autonomous)
- [ ] Measure: time, interventions, errors, ACSC
- [ ] Compare against baseline from Phase 0

**Falsifier:** If intervention count does not drop across successive runs while output quality holds → the substrate hypothesis is WRONG → bottleneck is elsewhere (model class or task paradigm). Honest failure, sealed as scar, not narrated around.

## 13. The Identity Layer (Arif's Eureka, 2026-09-06)

Two humans can see the same signal. Assign the same meaning. But act differently.

```
Child crying.

Doctor:  → assesses medical need
Father:  → responds with paternal urgency
Police:  → evaluates legal context
Teacher: → checks if student is in care
```

Same attention. Same meaning. Different **identity** → different action.

Identity is the layer that determines *which* action a sovereign takes, given the same meaning. It cannot be delegated because it is irreducibly personal — it is the accumulated weight of who Arif is, what he has lived, what he cares about, and what kind of future he is building.

### Updated Pipeline

```
Value → Attention (Costed) → Meaning (Sovereign) → Identity (Personal) → Intent → Action → Witness
```

| Layer | Question | Who Answers | Delegable? |
|---|---|---|---|
| **Value** | What matters to survival/purpose? | Pre-filter (agent-assisted) | Partially |
| **Attention** | What deserves consciousness? | Agent scoring + routing | Yes (routing) |
| **Meaning** | What does this mean to Arif? | Arif only (F13) | **No** |
| **Identity** | Who is Arif in this moment? | Arif only (irreducible) | **No** |
| **Intent** | What will Arif do about it? | Arif + agent planning | Partially |
| **Action** | Execute the intent | Agent execution | Yes |
| **Witness** | Record that this happened | VAULT999 | Yes |

**The sovereign boundary spans Meaning → Identity.** Both are irreducibly human. The system can assist with everything else.

## 14. Attention Debt

A metric that may emerge in 6–12 months:

```
Attention Debt = Attention Consumed − Attention Worthy
```

Or its inverse:

```
ACSC = Minutes of Sovereign Attention per Sealed Reality Change
```

When ACSC rises while capability stays flat, the system is wasting Arif's life. When ACSC falls while capability rises, the system is becoming wiser — consuming less sovereign attention per unit of governed outcome.

**The ultimate measure of a governed AI federation is not how much it can do. It is how little of Arif's life it needs to do it.**

## 15. The Constitutional Formula

Extending reality-compression.md:

```
ΔS ≤ 0 ⟺ Value → Attention (Costed) → Meaning (Sovereign) → Identity (Personal) → Intent → Action (Grounded) → Witness (Sealed)
```

The new nodes are **Meaning (Sovereign)** and **Identity (Personal)**. They sit between Attention and Intent. They are the bottleneck that makes the entire system *human*.

Without Meaning and Identity:
```
Value → Attention → Intent → Action → Witness
```
This is automation. Fast, efficient, inhuman.

With Meaning and Identity:
```
Value → Attention → Meaning (Arif decides what it means) → Identity (Arif decides who he is in this) → Intent → Action → Witness
```
This is governed agency. Slower, sovereign, alive.

## 16. Compression

In one sentence:

> **Capability determines power.**
> **Governance determines action.**
> **Attention determines which reality gets to exist.**
> **Meaning determines whether that reality matters.**
> **Identity determines who you become in the process.**

The Attention Graph is not a new organ. It is the map of the scarcest resource in the entire federation: not CPU, not tokens, not agents — but the unspent minutes of Arif's life.

*DITEMPA BUKAN DIBERI ⚒️*
