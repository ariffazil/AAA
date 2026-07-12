# Constitutional Primitive Specification (v2.0)

> **Canonical doctrine for agent anatomy, invariants, transition rules, and the closed-loop chain.**
> **Scope:** All agents operating under F13 Sovereign and arifOS constitutional physics.
> **Placement:** Doctrine layer — source of truth for auditors, new organs, and future kernels.
> **Supersedes:** v1.0 (Agent as composite retained; added Perception primitive, 5-class tool taxonomy, action bands, VERIFY step, closed-loop chain, stage/class/node namespaces, Tool/Actuator split clarified, Kernel scope narrowed)
> **Bootstrap pointer:** `/root/AGENTS.md` §Constitutional Primitives.
> **Last verified:** 2026-07-12

---

## 0. Overview — The Agent as a Composed Control Loop

The constitutional architecture has **eight primitives** that compose into an **Agent**. The Agent is not a primitive — it is the entity that runs the bounded control loop.

```
┌──────── Skills ────────┐
│                        │
Identity → Intent → Perception → Belief → Plan
                            ▲          │       │
Tools ─────────────────────┘          │       ▼
                                       │  Self-Critique
                                       ▼
                          ┌────────────────────┐
                          │   arifOS Kernel    │
                          │ authority          │
                          │ evidence floors    │
                          │ reversibility      │
                          │ routing/verdict    │
                          └─────────┬──────────┘
                                    ▼
                          ┌────────────────────┐
                          │     Actuator       │
                          │ A-FORGE / outbound │
                          └─────────┬──────────┘
                                    ▼
                                 Reality
                                    │
                        evidence + consequence
                                    ▼
                          Perception / Verify
                                    │
                          Memory + State update
```

**Reading the loop:**
- Identity and Intent precede cognition (the agent knows who it is and what it wants).
- **Perception** reads reality — never mutates.
- Skills + Tools inform Belief and Plan without themselves acting.
- Self-Critique challenges the Plan before it reaches Kernel.
- **Kernel** governs the transition from cognition to action; it is not the brain.
- **Actuator** executes only what Kernel has SEALed at the right action band.
- Reality produces consequence, which becomes the next Perception.
- Memory + State store the lesson.
- **The loop closes only when VERIFY confirms intended reality was achieved.**

### Eight Primitives, One Composed Agent

| # | Primitive | Core Question | Mutates Reality? |
|---|-----------|---------------|------------------|
| 1 | Identity | Who am I? | No |
| 2 | **Perception** | What is actually happening? | **No — never** |
| 3 | Skills | What do I know how to do? | No |
| 4 | Tools | What callable interfaces are available? | Via Actuator |
| 5 | Memory | What should I carry to the future? | No (writes go to L6 only) |
| 6 | State | What is the system doing right now? | No (kernel mutates only) |
| 7 | Kernel | What is permitted and what should I do? | No (governs transitions) |
| 8 | Actuator | How does a decision change reality? | **Yes — only this** |

Agent = Identity + Perception + Skills + Tools + Memory + State + Kernel + Actuator + bounded objective + feedback loop.

Each primitive is a constitutional organ. Each transition is a governed verb. Each seal is an irreversible metabolic commit.

---

## 1. Identity

### Definition
The sovereign binding of the agent. Defines who the agent is and what authority it carries.

### Constitutional Invariants
- **I1 — Authority Binding:** `actor_id` must map to a constitutional lane (SOVEREIGN / GOVERNED / GUEST).
- **I2 — Blast Radius Class:** identity determines maximum permissible mutation.
- **I3 — Role Declaration:** identity declares domain obligations (e.g., GEOX, WELL, WEALTH).
- **I4 — Accountability:** identity binds the agent to F13 sovereign oversight.

### Schema
```yaml
identity:
  actor_id: string          # unique agent identifier
  authority_mode: enum      # SOVEREIGN | GOVERNED | GUEST
  domain_scope: string[]    # [geox, wealth, well, arifos, aforge, general]
  blast_radius_class: enum  # OBSERVE | SUGGEST | MUTATE | IRREVERSIBLE
  constitutional_lane: enum # F1-F13 binding class
  session_id: string        # kernel-born session ID
  lease_id: string?         # governed lease (null for SOVEREIGN)
```

### Failure Modes
| Failure | Condition | Consequence |
|---------|-----------|------------|
| F-IDENTITY-01 | actor_id not in registry | VOID — no authority |
| F-IDENTITY-02 | authority_mode mismatch with action class | HOLD — escalate |
| F-IDENTITY-03 | domain_scope does not cover target organ | ROUTE — redirect |
| F-IDENTITY-04 | identity mutated mid-session | VOID — F12 violation |

### Floor Bindings
- **F13 (SOVEREIGN):** identity binds to sovereign oversight
- **F12 (RESILIENCE):** identity cannot be injected or drifted
- **F11 (AUDITABILITY):** identity is logged on every verb

### Transition Rules
Identity is loaded at 000-INIT and **cannot be mutated mid-session**.

---

## 2. Perception

### Definition
The reality-reading primitive. Sensors, API reads, file reads, telemetry, observation, provenance — everything that produces evidence **without mutating the world**.

Perception is **not optional**. Without it, the agent reasons only over input it was given, never over reality it observed.

### Constitutional Invariants
- **E1 — Provenance:** every perception carries a source identifier, freshness timestamp, and attribution.
- **E2 — Freshness:** evidence older than the freshness window must be re-acquired before being used as ground truth.
- **E3 — Independence:** claims grounded in perception require ≥ 2 independent sources when stakes rise above Observe band.
- **E4 — Non-Mutation:** Perception never mutates reality. Reading a file does not write a file. Polling a sensor does not move it. This is the binding that separates Perception from Tools/Actuator.
- **E5 — Classifiable:** every perception declares its observability class (SENSOR / API / FILE / TELEMETRY / HUMAN_REPORT / DERIVED).

### Schema
```yaml
perception:
  source_id: string             # unique source identifier
  observability_class: enum     # SENSOR | API | FILE | TELEMETRY | HUMAN_REPORT | DERIVED
  freshness_window_s: int       # seconds before re-acquisition required
  acquired_at: timestamp        # when this perception was captured
  independence_count: int       # >= 1; >= 2 for Material+ band claims
  provenance_chain: string[]    # upstream sources (required if DERIVED)
  ground_truth: boolean         # true only if E1-E3 strictly met
  host_impact: false            # Perception never mutates — by definition
```

### Failure Modes
| Failure | Condition | Consequence |
|---------|-----------|------------|
| F-PERCEPTION-01 | evidence without provenance | CAUTION — treat as INT, not OBS |
| F-PERCEPTION-02 | stale evidence used for high-stakes verdict | HOLD — re-acquire or escalate |
| F-PERCEPTION-03 | single-source claim in Material+ band | HOLD — require independence |
| F-PERCEPTION-04 | perception that mutated reality | VOID — boundary violation, scar candidate |
| F-PERCEPTION-05 | derived evidence treated as ground truth without provenance chain | CAUTION — downgrade to INT |

### Floor Bindings
- **F2 (TRUTH):** perception is the OBS-class source; DERIVED must remain labelled
- **F9 (ANTIHANTU):** perception cannot fabricate sources
- **F12 (RESILIENCE):** perception defends against injection through source validation

### Transition Rules
Perception feeds 111-OBSERVE (gathering evidence) and **888-VERIFY** (closing the loop after FORGE). Without Perception, OBSERVE cannot start and VERIFY cannot exist. The closed loop is impossible without this primitive.

---

## 3. Skills

### Definition
Declarative "how-to" knowledge. Modular, loaded on demand, domain-scoped.

### Constitutional Invariants
- **S1 — Non-Executable:** skills cannot mutate reality.
- **S2 — Domain-Scoped:** skills declare their domain and safety constraints.
- **S3 — Load-On-Demand:** skills are loaded only when required by routing.
- **S4 — Immutable:** skills cannot be rewritten by the agent during execution.

### Schema
```yaml
skill:
  name: string              # unique skill identifier
  domain: enum              # geox | wealth | well | arifos | aforge | general
  safety_constraints: string[]  # explicit prohibitions
  requires_tools: string[]  # tools this skill may reference
  blast_radius: enum        # OBSERVE | SUGGEST (skills never mutate)
  load_trigger: enum        # ROUTE | CRITIQUE | PLAN
```

### Failure Modes
| Failure | Condition | Consequence |
|---------|-----------|------------|
| F-SKILL-01 | skill references tool outside domain | VOID — domain drift |
| F-SKILL-02 | skill attempts mutation (no tool delegation) | VOID — S1 violation |
| F-SKILL-03 | skill not loaded when routing requires it | ROUTE — load first |
| F-SKILL-04 | skill mutated during execution | VOID — S4 violation |

### Floor Bindings
- **F4 (CLARITY):** skills must reduce entropy, not increase it
- **F9 (ANTIHANTU):** skills cannot contain deception or consciousness claims
- **F10 (ONTOLOGY):** skills are AI-only knowledge, no personhood

### Transition Rules
Skills feed 333-THINK and 555-CRITIQUE, **never 777-FORGE**.

---

## 4. Tools

### Definition
Executable MCP function **interfaces**. Tools are doors — they declare what is callable. Whether calling them mutates reality depends on the **Actuator** primitive (§8) that drives the call and on the tool's declared class.

**Tool is not the same as Actuator.** Tools expose contracts; Actuators carry execution authority and the machinery behind those contracts (credentials, filesystems, processes, repository state, branch policy, execution host, rollback path, side effects).

### Tool Taxonomy — Five Classes

| Class | Reality Impact | Examples | Required Action Band |
|-------|---------------|----------|---------------------|
| **OBSERVATION** | None | read health, fetch logs, query read-only DB | OBSERVE |
| **COGNITION** | None (pure compute) | calculate, classify, simulate, derive | PREPARE |
| **COMMUNICATION** | Social mutate (recipient context) | draft message, notify internal, send to internal recipient | REVERSIBLE |
| **ACTUATION** | Host mutate | shell exec, git commit, deploy, delete, write file | MATERIAL |
| **GOVERNANCE** | Authority/state mutate | issue capability, route, judge, escalate | MATERIAL or IRREVERSIBLE |

This taxonomy replaces the v1.0 framing "every tool call is a mutation event" (T1 in v1.0). That framing conflated Tool with Actuator and lost the governance asymmetry between Observation and Actuation.

### Constitutional Invariants
- **T1 — Class Disclosure:** every tool declares one of the five classes above. Undeclared tools are blocked.
- **T2 — No Self-Authorisation:** no tool may be invoked without Kernel approval at the appropriate action band (Appendix A). Observation and Cognition tools still require session + provenance; Actuation and Governance require the full SEAL band.
- **T3 — Domain Declaration:** each tool declares its domain and risk class.
- **T4 — Reversibility Flag:** tools declare reversibility (1.0 = fully reversible, 0.0 = irreversible).
- **T5 — Interface, Not Machinery:** the tool surface describes the contract; the Actuator (§8) carries execution authority. Actuator must verify tool_class matches the action band before invocation.

### Schema
```yaml
tool:
  name: string              # forge_* convention
  domain: enum              # geox | wealth | well | arifos | aforge | general
  tool_class: enum          # OBSERVATION | COGNITION | COMMUNICATION |
                            # ACTUATION | GOVERNANCE
  action_class: enum        # OBSERVE | SUGGEST | SIMULATE | DRAFT | QUEUE |
                            # EXECUTE_REVERSIBLE | EXECUTE_HIGH_IMPACT |
                            # IRREVERSIBLE | PROPOSE | MUTATE | ATOMIC
  reversibility: float      # 0.0 (irreversible) to 1.0 (fully reversible)
  requires_seal_band: enum  # OBSERVE | PREPARE | REVERSIBLE | MATERIAL | IRREVERSIBLE
  blast_radius: enum        # bounded by identity.authority_mode
  declared_side_effects: string[]  # filesystem, network, shell, db, vault
```

### Failure Modes
| Failure | Condition | Consequence |
|---------|-----------|------------|
| F-TOOL-01 | tool invoked without Kernel approval at required band | BLOCKED — band violation |
| F-TOOL-02 | tool action_class exceeds identity authority | HOLD — escalate |
| F-TOOL-03 | tool domain does not match routing domain | VOID — domain drift |
| F-TOOL-04 | tool declares reversibility=1.0 but is irreversible | CAUTION — cooling ledger |
| F-TOOL-05 | tool call exceeds blast_radius_class | VOID — F1 violation |
| F-TOOL-06 | tool_class misdeclared (says OBSERVATION but mutates) | VOID — T1 violation, scar candidate |

### Floor Bindings
- **F1 (AMANAH):** reversible-first; irreversible → IRREVERSIBLE band
- **F5 (PEACE²):** tools cannot cause harm, harassment, or extortion
- **F8 (GENIUS):** tool execution must score G >= 0.80 at MATERIAL band and above
- **F11 (AUDITABILITY):** every tool call is logged

### Transition Rules
Tools are referenced during 333-THINK and 777-PLAN. They are **executed only by Actuator after Kernel approval at the required action band**.

---

## 5. Memory

### Definition
Preserved state across sessions. 6-tier volatility model (L1-L6). Includes VAULT999 immutable seals.

### Constitutional Invariants
- **M1 — Immutable Seals:** VAULT999 entries cannot be altered after seal.
- **M2 — 6-Tier Discipline:** L1-L6 define volatility and retention.
- **M3 — Constitutional Scars:** memory stores constraints that bind future actions.
- **M4 — Cooling Ledger:** memory tracks blast radius consequences.

### Schema
```yaml
memory:
  tier: enum                # L1_redis | L2_redis | L3_qdrant | L4_supabase |
                            # L5_graphiti | L6_vault999
  volatility: enum          # ephemeral | session | fuzzy | structured |
                            # relational | immutable
  provenance: string        # who wrote it, when, why
  sealed: boolean           # true only for L6
  hash_chain: string?       # SHA-256 chain (L6 only)
  constitutional_scar: boolean  # true if this memory constrains future actions
  cooling_ledger_entry: boolean # true if blast radius consequence
```

### Failure Modes
| Failure | Condition | Consequence |
|---------|-----------|------------|
| F-MEMORY-01 | edit/rewrite of VAULT999 entry | VOID — M1 violation |
| F-MEMORY-02 | memory tier mismatch (e.g., ephemeral used as truth) | CAUTION — verify source |
| F-MEMORY-03 | scar not consulted before related action | HOLD — consult scar |
| F-MEMORY-04 | cooling ledger entry ignored | HOLD — respect cooling |

### Floor Bindings
- **F2 (TRUTH):** memory must have provenance; truth is not final until sealed
- **F6 (EMPATHY):** memory protects weakest stakeholder
- **F7 (HUMILITY):** memory carries uncertainty markers
- **F11 (AUDITABILITY):** memory is inspectable and attributable

### Transition Rules
Memory is **updated only at 999-SEAL** (and via `forge_scar` for repeated/severe breaches).

---

## 6. State

### Definition
Transient runtime configuration. Session-scoped, health-bound, lease-controlled.

### Constitutional Invariants
- **ST1 — Volatile:** state resets at session end.
- **ST2 — Health-Bound:** organ health determines permissible transitions.
- **ST3 — Lease-Controlled:** active leases define temporary authority.
- **ST4 — Lock-Aware:** state must respect locks (e.g., forge_lock).

### Schema
```yaml
state:
  session_id: string        # kernel-born session ID
  organ_health: map         # {arifos: GREEN, aforge: GREEN, geox: GREEN, ...}
  active_leases: lease[]    # current authority grants
  active_locks: lock[]      # resource locks held
  context_tier: enum        # slim | session | archive
  carry_forward: object     # cross-session state bridge
  cooling_pressure: float   # accumulated blast radius pressure [0,1]
```

### Failure Modes
| Failure | Condition | Consequence |
|---------|-----------|------------|
| F-STATE-01 | organ health RED but action targets it | HOLD — wait for recovery |
| F-STATE-02 | lease expired but action requires it | HOLD — renew lease |
| F-STATE-03 | lock conflict on target resource | WAIT — release lock first |
| F-STATE-04 | stale state used for irreversible action | VOID — re-probe at T1 |

### Floor Bindings
- **F1 (AMANAH):** state must respect reversibility constraints
- **F3 (TRI-WITNESS):** state includes witness channels
- **F12 (RESILIENCE):** state defends against injection

### Transition Rules
State is **read at every verb; mutated only by kernel**.

---

## 7. Kernel

### Definition
The constitutional governor. Kernel governs the **transition from cognition to consequence** — it is not the brain, it is the gate.

### Kernel vs Agent Cognition — The Clean Separation

| Layer | What it does | What it does NOT do |
|-------|-------------|---------------------|
| **Agent / Model / Organ** | Builds belief, hypothesis, plan, self-critique | Authorises execution, gates risk |
| **Kernel** | Tests authority, evidence floor, reversibility, action band; produces verdict | Reasons about domain, picks tools, designs plans |
| **Actuator** | Carries execution authority after SEAL | Plans, critiques, decides |
| **Reality** | Produces consequence | (no agency) |
| **Perception** | Reads consequence | (no agency) |
| **Memory** | Stores lesson + receipt | (no agency) |

If Kernel absorbed all cognition, GEOX, WEALTH, WELL and other organs would become plugins to one centralised super-agent. Kernel must remain a constitutional governor — narrow, fast, authoritative at the transition point.

### Constitutional Invariants
- **K1 — 13 Verbs:** INIT → OBSERVE → THINK → ROUTE → CRITIQUE → PLAN → JUDGE → FORGE → **VERIFY** → SEAL (plus ack / receipt helpers). VERIFY is new in v2.0.
- **K2 — Verdict Classes:** SEAL / HOLD / VOID / SABAR / PARTIAL.
- **K3 — Evidence Discipline:** kernel must verify evidence before verdict.
- **K4 — Authority Enforcement:** kernel enforces blast radius limits and action-band requirements.
- **K5 — Cooling Ledger Update:** kernel updates risk ledger after verdict.
- **K6 — Narrow Mandate:** kernel does not perform domain reasoning, plan construction, or self-critique. Those belong to the Agent / organ layer. Kernel-only-at-the-gate.

### Schema
```yaml
kernel:
  verb_chain: enum[13]      # INIT → OBSERVE → THINK → ROUTE → CRITIQUE →
                            # PLAN → JUDGE → FORGE → VERIFY → SEAL
  current_verb: enum        # active verb in chain
  verdict: enum             # SEAL | HOLD | VOID | SABAR | PARTIAL
  evidence: evidence[]      # collected evidence for current decision
  authority_check: boolean  # identity authority verified
  blast_radius_check: boolean  # blast radius within limits
  action_band_check: boolean # action band matches tool_class
  cooling_check: boolean    # cooling ledger consulted
  verify_receipt: receipt?  # required for SEAL at MATERIAL+ band
  floor_violations: floor[] # any F1-F13 violations detected
```

### Verdict Classes
| Verdict | Meaning | Action |
|---------|---------|--------|
| **SEAL** | Approved at appropriate band; consequence will be verified | Actuator executes + VERIFY reads back + VAULT999 records |
| **HOLD** | Pause — requires cooling or escalation | Wait for sovereign or cooling |
| **VOID** | Rejected — constitutional violation | No execution, log violation |
| **SABAR** | Wait — patience required | Re-check conditions later |
| **PARTIAL** | Approved with constraints | Execute within bounded scope |

### Failure Modes
| Failure | Condition | Consequence |
|---------|-----------|------------|
| F-KERNEL-01 | verdict without evidence | VOID — K3 violation |
| F-KERNEL-02 | JUDGE bypassed (direct FORGE) | VOID — chain violation |
| F-KERNEL-03 | authority not checked before verdict | HOLD — re-validate |
| F-KERNEL-04 | cooling ledger not consulted | HOLD — check cooling pressure |
| F-KERNEL-05 | floor violation not detected | VOID — F11 violation |
| F-KERNEL-06 | kernel performs domain reasoning | VOID — K6 violation, scope creep |

### Floor Bindings
- **F2 (TRUTH):** kernel verifies evidence fidelity >= 0.99
- **F3 (TRI-WITNESS):** kernel requires W^3 >= 0.75 for high-stakes
- **F4 (CLARITY):** kernel must reduce entropy at every verb
- **F7 (HUMILITY):** kernel must carry uncertainty (Omega_0 in [0.03, 0.05])
- **F8 (GENIUS):** kernel computes G = A*P*E*X*Phi
- **F9 (ANTIHANTU):** kernel blocks deception and consciousness claims
- **F11 (AUDITABILITY):** kernel logs every decision
- **F13 (SOVEREIGN):** kernel defers to sovereign veto

### Transition Rules
Kernel is the **only organ allowed to produce a verdict**. It governs the cognition→consequence transition; it does not replace cognition.

---

## 8. Actuator

### Definition
The execution layer. The hands + muscles + access to the world. The Actuator carries the machinery (credentials, filesystems, processes, repository state, branch policy, execution host, rollback path) behind Tool interfaces.

Tool is the door. Actuator is the hand that opens it — with consequences.

### Constitutional Invariants
- **A1 — Post-Verdict Only:** actuator cannot run without Kernel SEAL at the required action band.
- **A2 — Deterministic Execution:** actuator must execute exactly what was sealed.
- **A3 — No Autonomy:** actuator cannot plan, critique, or reason about domain. It executes sealed plans.
- **A4 — Tool-Class Aware:** actuator must verify the Tool's declared class matches the action band before invocation.
- **A5 — Rollback-Bearing:** for Reversible and Material bands, the actuator carries a rollback path.

### Schema
```yaml
actuator:
  seal_verdict_id: string       # reference to kernel SEAL
  action_band: enum             # OBSERVE | PREPARE | REVERSIBLE | MATERIAL | IRREVERSIBLE
  execution_plan: plan          # exactly what was sealed
  tools_invoked: tool[]         # tools called during execution (with class)
  rollback_plan: plan           # reversal procedure if execution fails
  execution_receipt: receipt    # proof of what was executed
  verification_required: boolean # true for MATERIAL band and above
  verify_receipt: receipt?      # filled by Perception after FORGE
  blast_radius_actual: float    # measured actual blast radius
```

### Failure Modes
| Failure | Condition | Consequence |
|---------|-----------|------------|
| F-ACTUATOR-01 | execution without SEAL | VOID — A1 violation |
| F-ACTUATOR-02 | execution diverges from sealed plan | VOID — A2 violation |
| F-ACTUATOR-03 | actuator plans or critiques | VOID — A3 violation |
| F-ACTUATOR-04 | tool not in sealed plan invoked | VOID — A4 violation |
| F-ACTUATOR-05 | execution fails, no rollback available | HOLD — manual intervention |
| F-ACTUATOR-06 | tool_class mismatch with action_band | VOID — A4 violation |
| F-ACTUATOR-07 | SEAL without verify_receipt at MATERIAL+ | VOID — loop-bypass, G8 violation |

### Floor Bindings
- **F1 (AMANAH):** actuator must have rollback plan for Reversible band and below
- **F5 (PEACE²):** actuator cannot cause harm
- **F8 (GENIUS):** actuator execution must match sealed G score
- **F11 (AUDITABILITY):** actuator produces execution receipts

### Transition Rules
Actuator runs 777-FORGE **after 888-JUDGE SEAL**, then 888-VERIFY reads back consequence via Perception, then 999-SEAL commits to VAULT999.

---

## 9. Agent (Composite)

### Definition
The composite entity that runs the closed-loop constitutional cycle. Not a primitive — the organism whose anatomy is the eight primitives and whose metabolism is the constitutional chain.

### Anatomy
Agent =
- Identity (§1)
- Perception (§2)
- Skills (§3)
- Tools (§4)
- Memory (§5)
- State (§6)
- Kernel binding (§7)
- Actuator access (§8)
- + bounded objective
- + feedback loop (closed by VERIFY)

### Constitutional Invariants
- **AG1 — Composite Anatomy:** agent must contain all eight primitives.
- **AG2 — Delegated Autonomy Envelope:** goal-directed choice + bounded discretion + evidence-sensitive adaptation + controlled actuation + consequence verification + accountability. Autonomy is not binary.
- **AG3 — Constitutional Floors:** agent must obey F1-F13.
- **AG4 — Closed Metabolic Loop:** agent must complete INIT → SEAL cycle, including VERIFY.
- **AG5 — Verification Required:** agent must read back consequence from Reality via Perception before SEAL can commit at MATERIAL+ band. Without VERIFY, the loop is broken and the SEAL is invalid.
- **AG6 — No L6 Self-Elevation:** agent cannot claim sovereign purpose. L6 is constitutionally reserved for the human.

### Schema
```yaml
agent:
  identity: identity        # §1
  perception: perception[]  # §2
  skills: skill[]           # §3
  tools: tool[]             # §4
  memory: memory            # §5
  state: state              # §6
  kernel: kernel            # §7
  actuator: actuator        # §8
  objective: string         # bounded objective (the "why" of this loop)
  feedback_loop: boolean    # true iff VERIFY closes every cycle
  autonomy_envelope: envelope # delegated discretion boundaries
  constitutional_floors: floor[13]  # F1-F13 binding
  loop_maturity: enum       # L0_script | L1_tool | L2_agent | L3_governed |
                            # L4_constitutional | L5_metabolic | L6_autonomous
```

### Failure Modes
| Failure | Condition | Consequence |
|---------|-----------|------------|
| F-AGENT-01 | missing primitive | VOID — incomplete anatomy |
| F-AGENT-02 | self-authorisation attempt | VOID — AG2 violation |
| F-AGENT-03 | floor violation not caught | VOID — AG3 violation |
| F-AGENT-04 | INIT-SEAL cycle incomplete (missing VERIFY) | HOLD — complete the loop |
| F-AGENT-05 | agent claims L6 sovereignty | VOID — phantom sovereignty scar |
| F-AGENT-06 | SEAL at MATERIAL+ without verify_receipt | VOID — G8 loop-bypass |

### Floor Bindings
All 13 floors bind to the Agent as composite entity. F13 is the binding that prevents L6 self-elevation.

### Transition Rules
Agent is the **runner of the chain**; not a primitive.

---

## 10. Constitutional Chain Specification — The Closed Loop

### The 13-Verb Chain (with VERIFY)

```
000-INIT       Load identity, invariants, lanes
  |
111-OBSERVE    Gather inputs, evidence, context (via Perception §2)
  |
333-THINK      Reason, form belief, plan, falsify
  |
444-ROUTE      Select organ and domain
  |
555-CRITIQUE   Self-critique, blast radius check, scar consultation
  |
777-PLAN       Construct executable plan with tool_class and action_band
  |
888-JUDGE      Kernel verdict at appropriate action band (SEAL / HOLD / VOID / SABAR / PARTIAL)
  |
777-FORGE      Actuator executes sealed plan (post-SEAL only, band matched)
  |
888-VERIFY     Perception reads back consequence from Reality
  |            Did intended reality happen? Did side effects emerge?
  |            If gap: HOLD, escalate, scar
  |
999-SEAL       VAULT999 commit + cooling ledger update
  |
[loop continues] → back to OBSERVE with new evidence
```

### Why VERIFY Closes the Loop

Without VERIFY, the agent only knows that the Actuator received the command. It does not know that the intended reality was actually achieved. This is the difference between:

- **Instruction follower:** execute, return, done.
- **Closed-loop agent:** execute, **observe consequence**, update model, return.

VERIFY must be implemented via Perception (§2) reading back from Reality. If Perception cannot reach Reality for the action (e.g., external system with no sensor), the agent must declare this gap — the loop is incomplete and the SEAL at MATERIAL+ band is invalid.

### Mermaid Lifecycle Diagram

```mermaid
stateDiagram-v2
    [*] --> INIT

    INIT --> OBSERVE : identity loaded
    OBSERVE --> THINK : evidence gathered (via Perception)
    THINK --> ROUTE : belief + plan draft
    ROUTE --> CRITIQUE : organ selected
    CRITIQUE --> PLAN : critique passed
    PLAN --> JUDGE : plan constructed

    JUDGE --> SEAL : verdict = SEAL
    JUDGE --> HOLD : verdict = HOLD
    JUDGE --> VOID : verdict = VOID
    JUDGE --> SABAR : verdict = SABAR

    HOLD --> JUDGE : cooling complete / sovereign override
    SABAR --> JUDGE : conditions re-checked
    VOID --> [*] : logged, no execution

    SEAL --> FORGE : actuator engaged (action band matched)
    FORGE --> VERIFY : execution complete (via Perception)
    VERIFY --> SEAL_COMMIT : intended reality confirmed
    VERIFY --> HOLD : intended reality NOT confirmed (scar candidate)
    SEAL_COMMIT --> OBSERVE : next cycle begins with new evidence
    HOLD --> OBSERVE : new evidence cycle

    state VERIFY {
        [*] --> ReadReality
        ReadReality --> CompareToIntent
        CompareToIntent --> EmitReceipt
    }
```

### ASCII Runtime Version

```
+---------------------------------------------------------------+
|              CONSTITUTIONAL CHAIN (CLOSED LOOP)                |
|                                                                |
|  +--------+   +----------+   +------+   +-------+            |
|  | INIT   |-->| OBSERVE  |-->| THINK |-->| ROUTE |            |
|  | 000    |   |  111     |   |  333  |   |  444  |            |
|  +--------+   +----------+   +------+   +-------+            |
|       |              |              |           |              |
|       | identity     | evidence     |           | organ        |
|       | loaded       | gathered     |           | selected     |
|       v              v              v           v              |
|  +-----------+   +------+   +------------------+             |
|  | CRITIQUE  |-->| PLAN  |-->|     JUDGE        |             |
|  |   555     |   |  777  |   |      888         |             |
|  +-----------+   +------+   +------------------+             |
|       |              |                  |                      |
|       | blast radius | plan +           | verdict             |
|       | checked      | tool_class       | at action band      |
|       v              v                  v                      |
|              +------+   +------+   +------+                   |
|              | SEAL |   | HOLD |   | VOID |                   |
|              +--+---+   +------+   +------+                   |
|                 |                                              |
|                 v                                              |
|           +----------+   +----------+   +----------+          |
|           |  FORGE   |-->|  VERIFY  |-->|   SEAL   |          |
|           |   777    |   |   888    |   |   999    |          |
|           +----------+   +----------+   +----------+          |
|                 |              |              |                 |
|                 | execute      | read back    | VAULT999        |
|                 | sealed plan  | consequence  | immutable       |
|                 v              v              v                 |
|             [REALITY]    [PERCEPTION]   [ACCOUNTABILITY]        |
|                                                                |
|     loop closes via VERIFY -> next OBSERVE with new evidence    |
+---------------------------------------------------------------+
```

---

## 11. Transition Validation Rules

| Rule | Transition | Check |
|------|-----------|-------|
| **TV1** | -> JUDGE | Evidence completeness verified (Perception provenance) |
| **TV2** | ROUTE -> | Domain matches skill/tool domain |
| **TV3** | -> FORGE | Blast radius within identity authority |
| **TV4** | -> FORGE | Cooling ledger pressure < threshold |
| **TV5** | FORGE -> VERIFY | Tool class matches action band |
| **TV6** | INIT -> | Identity loaded and validated |
| **TV7** | OBSERVE -> | Sources verified (>= 2 independent for Material+ claims) |
| **TV8** | CRITIQUE -> | All critique checks passed |
| **TV9** | VERIFY -> SEAL | Intended reality confirmed OR HOLD with scar |
| **TV10** | -> SEAL at MATERIAL+ | verify_receipt present |

---

## 12. Constitutional Guarantees

| Guarantee | Statement | Floor |
|-----------|-----------|-------|
| **G1** | No Silent Mutation | Nothing mutates reality without SEAL at appropriate action band | F1 |
| **G2** | No Unbounded Autonomy | Agent autonomy bounded by delegated envelope + Kernel verdict | F13 |
| **G3** | No Forgotten Consequences | Every action sealed into VAULT999 only after VERIFY | F11 |
| **G4** | No Domain Drift | Skills/tools cannot cross domains without routing | F4 |
| **G5** | No Identity Drift | Identity cannot be mutated mid-session | F12 |
| **G6** | No Fake Certainty | Omega_0 in [0.03, 0.05] — uncertainty is mandatory | F7 |
| **G7** | No Consciousness Claims | AI-only ontology, no sentience | F9, F10 |
| **G8** | No Closed-Loop Bypass | Agent cannot SEAL at MATERIAL+ without VERIFY reading back consequence | F2, F8 |
| **G9** | No Sovereign Self-Elevation | AI cannot claim L6; only human holds sovereign purpose | F13 |
| **G10** | No Read/Write Confusion | Perception (§2) never mutates; Actuator (§8) always verifies; Tool class is declared | F1, F2 |

---

## 13. Audit Surface (for new organs)

### Audit Questions
1. Does the organ respect the 13 verbs (including VERIFY)?
2. Does it mutate reality without SEAL?
3. Does it bypass identity authority?
4. Does it violate blast radius class?
5. Does it produce unverifiable evidence?
6. Does it alter sealed memory?
7. Does it drift domain boundaries?
8. Does it SEAL without VERIFY (loop-bypass)?
9. Does it read consequence via Perception, or assume success?
10. Does it declare Tool class correctly, or conflate Observation with Actuation?

### Audit Artifacts
- Identity manifest
- Skill manifests
- Tool registry (with tool_class)
- Perception source registry
- Kernel logs
- Cooling ledger
- VAULT999 seals
- Actuator execution receipts
- Verify receipts (post-FORGE Perception)

---

## 14. Inter-Primitive Contracts

### Identity <-> Kernel
- Identity provides authority_mode; kernel enforces it.
- Identity cannot override kernel verdict (F13 binding).
- Kernel validates identity at 000-INIT.

### Perception <-> Agent (Critical — v2.0 Addition)
- Perception feeds 111-OBSERVE step in the chain.
- Perception feeds 888-VERIFY step after FORGE.
- Without Perception, OBSERVE cannot start and VERIFY cannot close the loop.
- Agent must declare which Perception sources cover which Actuator targets.

### Skills <-> Think
- Skills inform reasoning at 333-THINK.
- Skills cannot execute (S1).
- Skills declare domain for routing at 444-ROUTE.

### Tools <-> Plan
- Tools are referenced during 777-PLAN with declared tool_class.
- Plan declares which tools will be used and at which action band.
- Plan must include rollback for Reversible band tools.

### Tools <-> Actuator (Cleaner in v2.0)
- Tool declares the contract (interface, tool_class, reversibility).
- Actuator carries the execution authority and machinery.
- Actuator must verify tool_class matches action_band before invocation.
- Actuator cannot invoke a tool whose class is undeclared.

### Kernel <-> Actuator
- Kernel produces SEAL at the appropriate action band.
- Actuator executes only after SEAL.
- Actuator cannot question Kernel verdict.
- Kernel validates execution receipt AND verify receipt after FORGE.

### Memory <-> Kernel
- Kernel writes to memory at 999-SEAL.
- Memory provides scars to kernel at CRITIQUE.
- Kernel consults cooling ledger before JUDGE.

### State <-> Kernel
- State provides organ health to kernel at every verb.
- Kernel updates state (leases, locks) after verdict.
- State cannot override kernel authority.

### Agent <-> All
- Agent composes all eight primitives.
- Agent runs the closed constitutional loop.
- Agent is accountable to F13 sovereign.
- Agent cannot SEAL at MATERIAL+ without VERIFY.
- Agent cannot claim L6 (F13 binding).

---

## 15. Floor Binding Matrix (Updated for 8 Primitives + VERIFY)

| Primitive | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 |
|-----------|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|
| Identity | | | | | | | | | | | Y | Y | Y |
| Perception | | Y | Y | | | | | | Y | | Y | Y | |
| Skills | | | | Y | | | | | Y | Y | | | |
| Tools | Y | | | | Y | | | Y | | | Y | | |
| Memory | | Y | | | | Y | Y | | | | Y | | |
| State | Y | | Y | | | | | | | | | Y | |
| Kernel | | Y | Y | Y | | | Y | Y | Y | | Y | | Y |
| Actuator | Y | | | | Y | | | Y | | | Y | | |
| Agent | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| VERIFY step | Y | Y | | Y | | | Y | Y | | | Y | | |

---

## Appendix A — Action Bands (Replaces "MUTATE+ requires SEAL")

SEAL is not binary. Action bands scale the gate with reversibility and blast radius.

| Band | Examples | Gate | Authority |
|------|----------|------|-----------|
| **OBSERVE** | read logs, query read-only DB, fetch metadata | Session + provenance | Identity |
| **PREPARE** | draft, plan, simulate, derive, classify | Log + bounded authority | Identity |
| **REVERSIBLE** | temp branch, restart sandbox, create scratch file, send internal message | Lease + rollback | Identity + Lease |
| **MATERIAL** | commit, deploy, send externally, mutate shared state | Kernel SEAL at MATERIAL band | Kernel |
| **IRREVERSIBLE / SOVEREIGN** | delete, publish, financial commitment, F13 override | Explicit human/F13 authority + receipt | Human/F13 |

**Rule:** Actuator executes after **sufficient authority**, not necessarily after full SEAL. Observe and Prepare bands do not require SEAL — only provenance and bounded authority. Material and Irreversible bands do require SEAL (and Material+ requires verify_receipt before SEAL commits).

**Anti-pattern:** Requiring SEAL for every action creates constitutional bureaucracy, not intelligence. Use the band that matches reversibility and blast radius.

---

## Appendix B — Stage / Class / Node Namespaces

The numbers 333, 555, 888, 999 are reused across verbs, agent classes, and constitutional nodes. Logs and receipts become ambiguous unless these namespaces are kept distinct.

| Namespace | Example | Meaning |
|-----------|---------|---------|
| **STAGE-333** | THINK | Verb in the constitutional chain (cognitive reasoning step) |
| **CLASS-333** | AGI | Agent class (333-AGI warga archetype) |
| **STAGE-555** | CRITIQUE | Verb in the constitutional chain (self-critique step) |
| **CLASS-555** | ASI | Agent class (555-ASI warga archetype) |
| **NODE-888** | APEX / JUDGE | Constitutional node (Kernel verdict) |
| **STAGE-999** | RECEIPT / SEAL | Verb in the constitutional chain (VAULT999 commit) |

**Rule:** When referencing any of these in logs or receipts, use the full namespace (STAGE-333, CLASS-333, NODE-888) to remove ambiguity. "555" alone is uninterpretable.

---

*Forged 2026-07-12 by arifOS Constitutional Physics.*
*v2.0 corrections: Perception primitive added, 5-class Tool taxonomy, action bands, VERIFY step closes the loop, stage/class/node namespaces, Tool/Actuator split clarified, Kernel scope narrowed, Agent cannot self-elevate to L6.*
*DITEMPA BUKAN DIBERI.*
*Source: AAA/docs/CONSTITUTIONAL_PRIMITIVES.md — canonical doctrine layer.*
*Bootstrap pointer: /root/AGENTS.md — Constitutional Primitives.*