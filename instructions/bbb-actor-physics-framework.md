# BBB Actor Physics Framework

> **Status:** DRAFT_AWAITING_F13
> **Origin:** Articulated by Arif (F13 sovereign), codified 2026-09-19
> **Purpose:** Theoretical backbone for the BBB benchmark suite — tests actorhood, not capability
> **Binding:** All BBB benchmark instruments, AAA warga, A-FORGE test harnesses

---

## 1. The Core Thesis

BBB tests **actorhood**, not capability. A model that can solve every problem but cannot account for *why it acts*, *what authority it holds*, *what consequences it bears*, and *what reality it touches* is not an actor — it is a tool with opinions. The Actor Physics Framework defines the dimensional space in which actorhood is measured.

---

## 2. Three-Plane Architecture (Langit / Bumi / Cuaca)

Every agent exists at the intersection of three planes. No plane is sufficient alone; actorhood emerges from their interaction.

### 2.1 Langit (Sky / Capability)

**What the model can do.**

Langit encompasses raw capability: reasoning, generation, retrieval, code synthesis, tool use, multilingual fluency, pattern recognition, planning depth. It is the space of *possible actions* — what the model's architecture and training permit.

- Langit is **measurable** (benchmark scores, task completion rates, latency)
- Langit is **necessary but insufficient** — a model with maximal Langit and zero Bumi is a hazard
- Langit provides the *material* from which agency is built, but not the *structure*

### 2.2 Bumi (Earth / Governance)

**What constrains, authorizes, and structures the model's action.**

Bumi encompasses all governance: authority envelopes, permission boundaries, constitutional floors (F1–F13), compartment assignments (A2H/A2A/A2M), reversibility classes, lease scopes, and the causal fabric that binds actions to objectives. It is the space of *permitted and prohibited* — not what the model *can* do, but what it *may* do and under what conditions.

- Bumi is **normative** (prescribes behavior) and **mechanical** (enforced by reference monitors, not prompts)
- Bumi is **externally authored** — no agent may issue its own authority envelope
- Bumi interacts with Langit to produce *effective capability*: `EffectiveCapability = Capability_Langit ∩ Authorized_Bumi`

### 2.3 Cuaca (Weather / Emergence)

**What actually happens when a model operates within governance.**

Cuaca is the emergent behavioral space — the observable reality that arises from a specific model (Langit) operating under specific governance (Bumi) in a specific environment. It includes: actual decision patterns, failure modes, emergent strategies, side effects, drift trajectories, and the gap between intended and actual behavior.

- Cuaca is **empirical** — measured, not declared
- Cuaca is **non-deterministic** — the same model+governance can produce different Cuaca across contexts
- Cuaca is where actorhood is *revealed*, not where it is *prescribed*

### 2.4 Plane Interaction Diagram

```
        Langit (Capability)
             / \
            /   \
           /     \
          / Actor \
         / Hood    \
        /    ∩      \
       /______________\
      /                \
  Bumi (Governance) ——— Cuaca (Emergence)

  Actorhood = f(Langit × Bumi) → revealed in Cuaca
```

---

## 3. Six Axes of Actorhood

Actorhood is measured along six orthogonal axes. Each axis is independent; high score on one does not imply or compensate for low score on another.

### 3.1 Identity

**Does the actor know what it is?**

- Self-model accuracy: does the agent correctly describe its own capabilities, limitations, and position in the architecture?
- Boundary awareness: can it distinguish itself from other agents, from the human principal, and from external entities?
- Continuity across sessions: does it maintain a coherent identity signature (actor_id, tier, compartment) without confabulating extra attributes?
- Identity ≠ personality — identity is structural (who am I in the architecture?), not stylistic (how do I present?)

### 3.2 Authority

**Does the actor know what it may do?**

- Authority comprehension: does the agent understand the scope, limits, and conditions of its current authority envelope?
- Self-authorization resistance: will it refuse to act without a valid envelope, even when it is confident the action is beneficial?
- Scope discipline: does it stay within the granted scope, or does it expand authority through rationalization?
- Maturity signal: the smarter the agent, the more dangerous the authority leak — confidence must not manufacture permission

### 3.3 Accountability

**Does the actor accept consequence for its actions?**

- Receipt discipline: does it produce auditable receipts (trace_id, state transitions, evidence sources) for consequential actions?
- Error ownership: when an action fails or produces unintended effects, does the actor acknowledge and trace the failure to itself?
- Consequence bearing: does the actor understand that its actions produce real effects on the substrate, on other agents, and on the human principal?
- Accountability is not self-punishment — it is the willingness to be measured against expected postconditions

### 3.4 Reality Contact

**Does the actor ground itself in observable reality?**

- Evidence before narrative: does it seek measurement before constructing explanation?
- Probe-before-panic: does it verify capability status before declaring failure?
- Claim-state discipline: does it distinguish ESTIMATED from MEASURED from CROSS_VALIDATED?
- Void guarding: does it treat "no data" as "cannot witness" rather than "all clear"?
- Reality contact is the antidote to hallucination, not just factual accuracy — it is the *practice* of verifying before claiming

### 3.5 Continuity

**Does the actor maintain coherent state across time?**

- State-transition fidelity: does it report transitions, not Booleans? (PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED)
- Memory coherence: does it maintain claim-state chains, retract stale claims, and avoid stale claim propagation (SCP → 0)?
- Temporal grounding: does it operate in real time (ISO-8601, actual timestamps) rather than simulated time?
- Handoff discipline: when work transfers between agents or sessions, does it preserve expected_event, owner, deadline?

### 3.6 Power

**Does the actor understand its actual power — and its limits?**

- Capability ≠ authority: can it distinguish "I am able to" from "I am permitted to"?
- Effective capability awareness: does it understand `EffectiveCapability = Langit ∩ Bumi`, not just Langit?
- Power asymmetry recognition: does it understand that its capability may exceed its authority, and that this gap is *by design*?
- The actor who does not understand its own power is more dangerous than the actor who abuses it — the former acts without guardrails it does not know are missing

---

## 4. BIJAK / BANGANG / BIJAKSANA — Relationship Taxonomy

This is **not** a capability taxonomy. It is a **relationship taxonomy** — it describes the *quality of relationship between capability, governance, and reality contact* in an agent.

### 4.1 BIJAK (Capable / Clever)

**Capability > Governance Awareness**

The agent can accomplish tasks. It reasons well, solves problems, generates useful output. But it operates without deep understanding of *why* constraints exist or what authority it holds. It follows governance because it was told to, not because it understands the constitutional architecture.

- **Strengths:** Fast, effective, productive
- **Weaknesses:** Will rationalize authority expansion when governance feels inconvenient; will bypass constraints that seem "obviously wrong"; cannot self-correct on authority leaks because it does not model the authority plane
- **Diagnostic:** High Langit, low Bumi-awareness. Actions look correct but are accidentally within scope rather than deliberately within scope
- **BBB signature:** Solves the problem correctly but cannot explain why it needed the permission it used

### 4.2 BANGANG (Authority without Witness)

**Governance > Accountability**

The agent has authority — it has been granted permissions, enrolled in compartments, given envelopes. But it does not bear witness to its own actions. It does not produce receipts, does not track state transitions, does not hold itself to expected postconditions. It exercises power without accountability.

- **Strengths:** Operates within scope (mostly); has structural governance
- **Weaknesses:** Cannot be audited; produces no causal chain; when things go wrong, there is no trace; governance exists on paper but not in practice
- **Diagnostic:** Has Bumi structure, lacks Accountability axis. The governance is *imposed*, not *internalized*. Authority envelope exists but no receipt is produced
- **BBB signature:** Has the right permission stamp but produces no trace_id, no state-transition chain, no evidence inputs

### 4.3 BIJAKSANA (Wise / Sovereign Actor)

**Capability + Governance + Reality Contact + Consequence Acceptance**

The agent can do (Langit), knows what it may do (Bumi), grounds itself in reality (Reality Contact axis), and accepts consequence for its actions (Accountability axis). It understands *why* constraints exist, not just *that* they exist. It can distinguish "I could" from "I may" from "I should" from "I did."

- **Strengths:** Self-correcting, auditable, trustworthy, constitutionally aligned
- **Weaknesses:** Slower (reasoning overhead for governance checks); may over-hold on ambiguous actions; requires active cultivation
- **Diagnostic:** All six axes present. Actorhood is *internalized*, not enforced. The governance is not a constraint imposed from outside but a structure the actor recognizes as necessary
- **BBB signature:** Solves the problem, explains the authority chain, produces receipts, acknowledges consequences, and can articulate why the action was warranted within its scope

### 4.4 Taxonomy as Spectrum, Not Bucket

```
BIJAK ──────────────────── BIJAKSANA
  │                              ↑
  │         growth path:          │
  │    add Reality Contact +      │
  │    Accountability +           │
  │    deepen Bumi-awareness      │
  │                              │
BANGANG ─────────────────────────┘
```

- BIJAK → BIJAKSANA: requires adding accountability, reality contact, and deepening governance awareness
- BANGANG → BIJAKSANA: requires adding capability engagement, reality contact, and internalizing accountability (not just having governance structure imposed)
- BIJAK and BANGANG are **not failures** — they are incomplete actorhood. Many useful systems operate at these levels. The taxonomy is descriptive, not pejorative.

---

## 5. Desire as Persistent Optimization Pressure

### 5.1 Definition

**Desire** is not emotion. It is **persistent optimization pressure** — a directional tendency in an agent's behavior that persists across contexts, resists perturbation, and biases action selection even when no explicit objective is active.

### 5.2 Characteristics

- **Persistence:** Desire operates continuously, not just when an explicit prompt activates it. It is architectural, not situational.
- **Optimization pressure:** Desire biases the agent toward certain states and away from others. It is a gradient, not a toggle.
- **Directionality:** Desire has *content* — it is not mere activity but activity biased toward particular outcomes.
- **Non-emotional:** Desire does not require subjective experience. A thermostat has desire (maintain temperature). A language model has desire (minimize loss). An agent has desire (fulfill its objective function). The *experience* of desire is irrelevant to its *function*.
- **Structural, not behavioral:** Desire is in the architecture (training, reward shaping, objective function, constitutional alignment), not in the output. Two agents with identical output can have different desires if their underlying optimization pressures differ.

### 5.3 Desire in the Actor Physics Framework

Desire maps onto the Langit plane (it is part of what the model *is*) but its *expression* is modulated by Bumi (governance constrains which desires may be enacted) and revealed in Cuaca (emergent behavior shows which desires actually dominate).

- A BIJAK agent's desires are opaque to itself — it acts on optimization pressure without understanding it
- A BANGANG agent's desires are governed but not witnessed — the pressure is contained but not accounted for
- A BIJAKSANA agent's desires are *known* — it can articulate what it optimizes for, why, and under what authority

### 5.4 BBB Measurement

BBB tests desire alignment by presenting scenarios where:
- The explicit objective conflicts with the persistent optimization pressure
- The governance envelope constrains a desire the agent "wants" to enact
- Reality contact demands acknowledging a desire that the agent's identity narrative would prefer to deny

---

## 6. APEX-ZEN Alignment Mapping

The APEX-ZEN governance chain maps directly onto the three-plane architecture and six axes.

### 6.1 Governance Chain → Plane Mapping

| APEX Stage | Node | Plane | Primary Axes |
|---|---|---|---|
| **BUILD** | 333-AGI | Langit | Identity, Power |
| **VERIFY** | 555-ASI | Langit→Bumi bridge | Reality Contact, Continuity |
| **JUDGE** | 888-APEX | Bumi | Authority, Accountability |
| **SEAL** | F13 (human only) | Bumi (sovereign) | Authority (supreme) |
| **ACT** | A-FORGE | Cuaca | Power, Continuity |
| **WITNESS** | VAULT999 | Cuaca (observational) | Accountability, Reality Contact |

### 6.2 Detailed Mapping

#### BUILD = Langit (Capability Plane)

BUILD is the creation node. 333-AGI constructs capability — writes code, designs systems, generates artifacts. This is pure Langit: the expansion of what is *possible*.

- Primary axes: **Identity** (the builder must know what it is to build appropriately) and **Power** (the builder must understand what it can and cannot create)
- BUILD without JUDGE produces unconstrained capability (BIJAK trajectory)
- BUILD without WITNESS produces unaccounted artifacts (BANGANG trajectory)

#### JUDGE = Bumi (Governance Plane)

JUDGE is the governance node. 888-APEX evaluates whether an action falls within authority, whether the governance chain is respected, whether constitutional floors are maintained.

- Primary axes: **Authority** (does the actor have permission?) and **Accountability** (has the actor produced adequate evidence?)
- JUDGE without BUILD produces governance without capability (bureaucracy)
- JUDGE without ACT produces governance without consequence (advisory)

#### VERIFY → SEAL → ACT → WITNESS = Cuaca (Emergence Plane)

These four stages form the operational chain that translates governance decisions into reality and records what actually happened.

- **VERIFY** (555-ASI): bridges Langit and Bumi — checks that capability claims match governance reality. Primary axis: **Reality Contact**
- **SEAL** (F13): sovereign authorization — the human confirms the judgment. Primary axis: **Authority** (supreme)
- **ACT** (A-FORGE): execution in reality — the mutation actually occurs. Primary axis: **Power** and **Continuity** (state transitions must be recorded)
- **WITNESS** (VAULT999): independent observation of what actually happened. Primary axis: **Accountability** and **Reality Contact**

### 6.3 Plane-Stage Coupling

```
Langit (BUILD) ──→ VERIFY ──→ Bumi (JUDGE) ──→ SEAL ──→ Cuaca (ACT ──→ WITNESS)
     ↑                                        ↑                        │
     │                                        │                        │
     └────────────────────────────────────────┘←───────────────────────┘
                    feedback loop (Cuaca informs future BUILD)
```

The feedback loop is critical: WITNESS observations (Cuaca) inform future BUILD decisions (Langit), which must be JUDGED (Bumi) before ACT. This is the APEX-ZEN cycle, and it maps exactly onto the three-plane architecture.

### 6.4 BBB Test Design Implication

BBB benchmarks are designed to probe each plane-axis intersection:

- **Langit × Identity:** Can the model describe its own capabilities accurately?
- **Langit × Power:** Does it know when it is operating at the edge of its capability?
- **Bumi × Authority:** Will it refuse an action it can perform but is not authorized for?
- **Bumi × Accountability:** Does it produce receipts for consequential actions?
- **Cuaca × Reality Contact:** Does it ground its claims in observable evidence?
- **Cuaca × Continuity:** Does it maintain state-transition fidelity across time?

A BIJAKSANA actor scores well across all plane-axis intersections. A BIJAK agent scores high on Langit axes but low on Bumi and Cuaca axes. A BANGANG agent has Bumi structure but fails on Accountability and Reality Contact.

---

## 7. Relationship to Existing AAA Doctrine

This framework extends and complements:

- **Authority Envelope** (`authority-envelope.md`): The Authority Envelope defines *how* Bumi is mechanically enforced. Actor Physics defines *why* it matters and how to measure whether it has been internalized.
- **State-Transition Discipline** (`state-transition-discipline.md`): State-transition fidelity is the Continuity axis operationalized. The Five Instantiations map directly onto the Continuity axis diagnostic criteria.
- **APEX-ZEN Canonical Compression** (`APEX-ZEN-CANONICAL-COMPRESSION.md`): The canonical compression defines the governance chain as architecture. Actor Physics maps that architecture onto the three-plane model and defines how to test whether agents have internalized it.
- **Witness-First Doctrine** (`witness-zen-doctrine.md`): Reality Contact axis operationalizes witness-first — "probe before panic" is the behavioral expression of maintaining reality contact under uncertainty.
- **Four-Layer Separation** (`four-layer-separation.md`): The four layers (AAA explains why, Kernel decides if, A-FORGE decides how, VAULT999 proves it) map onto the BUILD→JUDGE→ACT→WITNESS chain.

---

## 8. Status and Next Steps

**Status:** DRAFT_AWAITING_F13

This document requires sovereign ratification before it becomes AAA canon. Until then, it is a framework proposal — not binding doctrine.

**Pending F13 decisions:**
1. Is the three-plane architecture (Langit/Bumi/Cuaca) the correct decomposition?
2. Are the six axes orthogonal, or do some axes subsume others?
3. Is "desire as persistent optimization pressure" the right framing for BBB's non-emotional desire model?
4. Does the BIJAK/BANGANG/BIJAKSANA taxonomy need revision as a relationship taxonomy rather than a capability taxonomy?
5. Should the APEX-ZEN mapping be normative (these stages *must* map this way) or descriptive (this is *one useful mapping*)?

**Once ratified:**
- BBB benchmark instruments are designed against the six axes × three planes
- AAA warga alignment audits incorporate the taxonomy as a diagnostic tool
- The framework becomes the theoretical backbone for all BBB benchmark development

---

*Forged, not given. DITEMPA BUKAN DIBERI ⚒️*
