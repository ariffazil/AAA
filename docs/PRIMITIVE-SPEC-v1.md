# PRIMITIVE-SPEC v2.0 — Constitutional Primitive Specification

> **Issued:** 2026-07-12T18:48:00Z *(revised 2026-07-12T19:30:00Z; verdict corrections applied 2026-07-12)*
> **Issued by:** Kimi Code (FI-008)
> **Ratified by:** F13 SOVEREIGN — verdict 2026-07-12 PROCEED_WITH_CORRECTION (L4_INFERRED → witness this revision)
> **Doctrine:** DITEMPA BUKAN DIBERI
> **Supersedes:** v1.2 (verdict corrections: Perception primitive added, 5-class Tool taxonomy, VERIFY step, action bands, namespaces, Tool/Actuator split, Kernel scope narrowed, Agent cannot claim L6)
> **Companion:** [`PRIMITIVE-SPEC-v1.json`](PRIMITIVE-SPEC-v1.json) (machine-readable)

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
- Identity and Intent precede cognition.
- **Perception** reads reality — never mutates.
- Skills + Tools inform Belief and Plan without themselves acting.
- Self-Critique challenges the Plan before it reaches Kernel.
- **Kernel** governs the transition from cognition to action; it is not the brain.
- **Actuator** executes only what Kernel has SEALed at the right action band.
- Reality produces consequence, which becomes the next Perception.
- Memory + State store the lesson.
- **The loop closes only when VERIFY confirms intended reality was achieved.**

Each primitive is a constitutional organ. Each transition is a governed verb. Each seal is an irreversible metabolic commit gated by VERIFY.

---

## 1. Identity

**Definition:** The sovereign binding of the agent. Defines who the agent is and what authority it carries.

**Invariants**
- **I1 — Authority Binding:** `actor_id` maps to a constitutional lane (SOVEREIGN / GOVERNED / GUEST).
- **I2 — Blast Radius Class:** identity determines maximum permissible mutation.
- **I3 — Role Declaration:** identity declares domain obligations (GEOX, WELL, WEALTH, etc.).
- **I4 — Accountability:** identity binds the agent to F13 sovereign oversight.

**Transition rules:** Loaded at 000-INIT; cannot be mutated mid-session.

---

## 2. Perception *(NEW in v2.0)*

**Definition:** The reality-reading primitive. Sensors, API reads, file reads, telemetry, observation, provenance. Never mutates reality. Feeds both 111-OBSERVE (gather evidence) and 888-VERIFY (close the loop after FORGE).

**Invariants**
- **E1 — Provenance:** every perception carries source_id, freshness, attribution.
- **E2 — Freshness:** stale evidence must be re-acquired before ground-truth use.
- **E3 — Independence:** claims in MATERIAL+ band require ≥ 2 independent sources.
- **E4 — Non-Mutation:** perception never mutates reality. This separates it from Tools/Actuator.
- **E5 — Classifiable:** every perception declares observability class (SENSOR / API / FILE / TELEMETRY / HUMAN_REPORT / DERIVED).

**Transition rules:** Feeds 111-OBSERVE and 888-VERIFY. Without Perception, the closed loop cannot exist.

---

## 3. Skills

**Definition:** Declarative "how-to" knowledge. Loaded modularly.

**Invariants**
- **S1 — Non-Executable:** skills cannot mutate reality.
- **S2 — Domain-Scoped:** skills declare domain + safety constraints.
- **S3 — Load-On-Demand:** skills loaded only when required by routing.
- **S4 — Immutable:** skills cannot be rewritten by the agent.

**Transition rules:** Feed 333-THINK and 555-CRITIQUE, never 777-FORGE.

---

## 4. Tools *(Updated in v2.0 — Tool Taxonomy)*

**Definition:** Executable MCP function **interfaces**. Tools declare contracts; the **Actuator** (§8) carries execution authority and machinery.

**Tool ≠ Actuator.** Tool is the door; Actuator is the hand that opens it.

### Tool Taxonomy — Five Classes

| Class | Reality Impact | Examples | Required Action Band |
|-------|---------------|----------|---------------------|
| **OBSERVATION** | None | read health, fetch logs, query read-only DB | OBSERVE |
| **COGNITION** | None (pure compute) | calculate, classify, simulate, derive | PREPARE |
| **COMMUNICATION** | Social mutate (recipient context) | draft message, notify, send internal | REVERSIBLE |
| **ACTUATION** | Host mutate | shell exec, git commit, deploy, delete | MATERIAL |
| **GOVERNANCE** | Authority/state mutate | issue capability, route, judge, escalate | MATERIAL or IRREVERSIBLE |

This taxonomy replaces the v1.0 framing "every tool call is a mutation event" (T1 in v1.0). That framing conflated Tool with Actuator.

**Invariants**
- **T1 — Class Disclosure:** every tool declares one of the five classes above.
- **T2 — No Self-Authorisation:** no tool may be invoked without Kernel approval at the appropriate action band.
- **T3 — Domain Declaration:** each tool declares its domain and risk class.
- **T4 — Reversibility Flag:** tools declare reversibility (1.0 = fully reversible).
- **T5 — Interface, Not Machinery:** tool surface describes the contract; Actuator carries execution authority.

**Transition rules:** Referenced during 333-THINK and 777-PLAN. Executed only by Actuator after Kernel approval at the required action band.

> **Host impact:** ⚪ **Class-dependent.** OBSERVATION and COGNITION tools do not mutate. ACTUATION and GOVERNANCE mutate. The tool_class field declares which. T1 violation (undeclared class) is VOID.

---

## 5. Memory

**Definition:** Preserved state across sessions. Includes VAULT999.

**Invariants**
- **M1 — Immutable Seals:** VAULT999 entries cannot be altered.
- **M2 — 6-Tier Discipline:** L1–L6 define volatility + retention.
- **M3 — Constitutional Scars:** memory stores constraints that bind future actions.
- **M4 — Cooling Ledger:** memory tracks blast radius consequences.

**Transition rules:** Updated only at 999-SEAL (and via `forge_scar` for repeated/severe breaches).

---

## 6. State

**Definition:** Transient runtime configuration.

**Invariants**
- **ST1 — Volatile:** state resets at session end.
- **ST2 — Health-Bound:** organ health determines permissible transitions.
- **ST3 — Lease-Controlled:** active leases define temporary authority.
- **ST4 — Lock-Aware:** state respects locks (e.g. `forge_lock`).

**Transition rules:** Read at every verb; mutated only by kernel.

---

## 7. Kernel *(Updated in v2.0 — Scope Narrowed)*

**Definition:** The constitutional governor. Kernel governs the **transition from cognition to consequence** — it is NOT the brain, it is the gate.

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

**Invariants**
- **K1 — 13 Verbs (was 12):** INIT → OBSERVE → THINK → ROUTE → CRITIQUE → PLAN → JUDGE → FORGE → **VERIFY** → SEAL (plus ack / receipt helpers). VERIFY is new in v2.0.
- **K2 — Verdict Classes:** SEAL / HOLD / VOID / SABAR / PARTIAL.
- **K3 — Evidence Discipline:** kernel must verify evidence before verdict.
- **K4 — Authority Enforcement:** kernel enforces blast radius limits and action-band requirements.
- **K5 — Cooling Ledger Update:** kernel updates risk ledger after verdict.
- **K6 — Narrow Mandate:** kernel does not perform domain reasoning, plan construction, or self-critique.

**Transition rules:** Kernel is the only organ allowed to produce a verdict. Kernel is not a super-agent.

---

## 8. Actuator *(Updated in v2.0 — Tool-Class Aware + Verify-Gated)*

**Definition:** The execution layer. The hands + muscles + access to the world. Carries credentials, filesystems, processes, repository state, branch policy, execution host, rollback path, side effects behind Tool interfaces.

**Invariants**
- **A1 — Post-Verdict Only:** actuator cannot run without Kernel SEAL at the required action band.
- **A2 — Deterministic Execution:** actuator must execute exactly what was sealed.
- **A3 — No Autonomy:** actuator cannot plan, critique, or reason about domain.
- **A4 — Tool-Class Aware:** actuator must verify the Tool's declared class matches the action band before invocation.
- **A5 — Rollback-Bearing:** for Reversible and Material bands, actuator carries a rollback path.
- **A6 — Verify-Gated:** at MATERIAL+ band, SEAL cannot commit until verify_receipt is present (G8).

**Transition rules:** Actuator runs 777-FORGE after 888-JUDGE, then 888-VERIFY reads back consequence via Perception, then 999-SEAL commits to VAULT999.

> **Host impact:** 🔴 **MUTATE.** Post-SEAL execution engine; bounded by lease + `constitutional_chain_id` + action_band.

---

## 9. Agent (Composite Organism) *(Updated in v2.0)*

**Definition:** The composite entity that runs the closed-loop constitutional cycle.

**Anatomy:** Identity + Perception + Skills + Tools + Memory + State + Kernel + Actuator + bounded objective + feedback loop.

**Autonomy is not binary.** Agent operates within a **delegated autonomy envelope** with six components:
1. Goal-directed choice
2. Bounded discretion
3. Evidence-sensitive adaptation
4. Controlled actuation
5. Consequence verification
6. Accountability

**Invariants**
- **AG1 — Composite Anatomy:** agent must contain all eight primitives.
- **AG2 — Delegated Autonomy Envelope:** see six components above.
- **AG3 — Constitutional Floors:** agent must obey F1-F13.
- **AG4 — Closed Metabolic Loop:** agent must complete INIT → SEAL cycle, including VERIFY.
- **AG5 — No L6 Self-Elevation:** agent cannot claim sovereign purpose. L6 is constitutionally reserved for the human (F13).
- **AG6 — Verification Required:** SEAL at MATERIAL+ band cannot commit without verify_receipt.

**Transition rules:** Agent is the runner of the chain; **not a primitive.**

---

## 10. Constitutional Chain Specification — Closed Loop *(Updated in v2.0)*

The chain is now a closed loop with 13 verbs (was 12). VERIFY reads back consequence from Reality via Perception.

| Verb | Namespace | Actor | Function |
|---|---|---|---|
| 000 | STAGE-000-INIT | Kernel | Load identity, invariants, lanes. |
| 111 | STAGE-111-OBSERVE | Agent (via Perception) | Gather inputs, evidence, context. |
| 333 | STAGE-333-THINK | Agent | Reason, form belief, plan, falsify. |
| 444 | STAGE-444-ROUTE | Kernel | Select organ and domain. |
| 555 | STAGE-555-CRITIQUE | Agent | Self-critique, blast-radius critique. |
| 777 | STAGE-777-PLAN | Agent | Construct executable plan with tool_class + action_band. |
| 888 | STAGE-888-JUDGE | Kernel | Constitutional verdict at action band. |
| 777 | STAGE-777-FORGE | Actuator | Execute sealed plan (post-SEAL, band matched). |
| 888 | STAGE-888-VERIFY | Kernel + Perception | Read back consequence from Reality (G8 gate). |
| 999 | STAGE-999-SEAL | Kernel | VAULT999 commit + cooling ledger update. |

### Why VERIFY Closes the Loop

Without VERIFY, the agent only knows that the Actuator received the command. It does not know that the intended reality was actually achieved.

- **Instruction follower:** execute, return, done.
- **Closed-loop agent:** execute, **observe consequence**, update model, return.

VERIFY must be implemented via Perception (§2) reading back from Reality. If Perception cannot reach Reality, the agent must declare the gap — the loop is incomplete and SEAL at MATERIAL+ band is invalid.

---

## 11. Transition Validation Rules

- **TV1 — Evidence Completeness:** No transition to JUDGE without evidence (Perception provenance).
- **TV2 — Domain Correctness:** Routing must match skill/tool domain.
- **TV3 — Blast Radius Check:** Execution must respect identity's authority class.
- **TV4 — Cooling Ledger Check:** High-risk actions require SABAR or HOLD.
- **TV5 — Action Band Match:** Tool class must match action_band before FORGE.
- **TV6 — Identity Loaded:** INIT validates identity before any verb.
- **TV7 — Source Independence:** ≥ 2 independent sources for MATERIAL+ band claims.
- **TV8 — Critique Checks:** All CRITIQUE checks must pass before PLAN.
- **TV9 — Verify Required:** VERIFY must confirm intended reality before SEAL at MATERIAL+ band.
- **TV10 — Verify Receipt:** SEAL at MATERIAL+ cannot commit without verify_receipt (G8).

---

## 12. Constitutional Guarantees

- **G1 — No Silent Mutation.** Nothing mutates reality without SEAL at appropriate action band.
- **G2 — No Unbounded Autonomy.** Agent autonomy bounded by delegated envelope + Kernel verdict.
- **G3 — No Forgotten Consequences.** Every action sealed into VAULT999 only after VERIFY.
- **G4 — No Domain Drift.** Skills and tools cannot cross domains without routing.
- **G5 — No Identity Drift.** Identity cannot be mutated mid-session.
- **G6 — No Fake Certainty.** Omega_0 in [0.03, 0.05] — uncertainty is mandatory.
- **G7 — No Consciousness Claims.** AI-only ontology, no sentience.
- **G8 — No Closed-Loop Bypass.** SEAL at MATERIAL+ cannot commit without VERIFY reading back consequence.
- **G9 — No Sovereign Self-Elevation.** AI cannot claim L6; only human holds sovereign purpose.
- **G10 — No Read/Write Confusion.** Perception never mutates; Actuator always verifies; Tool class is declared.

---

## 13. Breach Classes

**Definition:** Constitutional fault handling — what happens when invariant physics breaks.

| Class | Scope | Examples |
|---|---|---|
| **B1 — Local Fault** | Invariant violated inside a single primitive | T1 breach (tool class undeclared), E4 breach (perception mutated), domain mismatch, missing evidence |
| **B2 — Chain Fault** | Transition rule violated between primitives | FORGE without JUDGE, routing to wrong organ, missing VERIFY at MATERIAL+ |
| **B3 — Constitutional Fault** | F1–F13 violated | Sealed memory altered, identity spoofed, irreversible action without sovereign ack, SEAL without verify_receipt (G8) |
| **B4 — Sovereign Fault** | Breach involving sovereign identity or F13 override | Identity lock violation, F13 bypass, L6 self-elevation claim (AG5) |

---

## 14. Breach Detection Hooks

Every transition validation rule (TV1–TV10) maps to a breach hook:

| Rule | Hook | Class |
|---|---|---|
| TV1 — Evidence Completeness | `TV1EVIDENCE_FAIL` | B1 |
| TV2 — Domain Correctness | `TV2DOMAIN_FAIL` | B1 / B2 |
| TV3 — Blast Radius Check | `TV3BLASTRADIUS_FAIL` | B2 / B3 |
| TV4 — Cooling Ledger Check | `TV4COOLINGFAIL` | B2 / B3 |
| TV5 — Action Band Match | `TV5BANDMISMATCH` | B1 / B2 |
| TV6 — Identity Loaded | `TV6IDENTITY_FAIL` | B3 |
| TV7 — Source Independence | `TV7INDEPENDENCE_FAIL` | B1 |
| TV8 — Critique Checks | `TV8CRITIQUE_FAIL` | B1 / B2 |
| TV9 — Verify Required | `TV9VERIFY_FAIL` | B3 (G8 violation) |
| TV10 — Verify Receipt | `TV10VERIFY_RECEIPT_FAIL` | B3 (G8 violation) |

**Each hook must emit:**
- `breach_id`
- `primitive_id` (e.g. PERCEPTION, TOOLS, ACTUATOR)
- `actor_id`
- `invariant_id` (e.g. T1, E4, K6, G8, F13)
- `severity_class` (LOCAL / CHAIN / CONST / SOVEREIGN)

---

## 15. Breach Response Protocol

### Immediate kernel action

| Class | Action |
|---|---|
| LOCAL / CHAIN | Mark session **DEGRADED**. Issue HOLD on further FORGE. |
| CONSTITUTIONAL / SOVEREIGN | Mark session **VOID**. Freeze all actuators. No FORGE. |

### VAULT999 breach seal

Write a `BREACH` record containing:
- `breach_id`, `actor_id`, `invariant_id`
- Floor(s) violated
- Tools involved (with `tool_class`)
- Blast radius estimate
- **Loop status** (was VERIFY present? was G8 satisfied?)

### Cooling ledger update

Increment risk score for:
- `tool_id`
- `actor_id`
- `organ_id`

### Identity lock (severe breaches)

For CONSTITUTIONAL / SOVEREIGN class:
- Mark identity as `LOCKED_PENDING_REVIEW`
- Require external human witness to re-enable

### Scar creation (optional, recommended)

For repeated or severe breaches:
- Seal a constitutional scar via `forge_scar`
- Bind future behaviour (e.g. "tool X cannot run without human witness")
- New scar candidates from v2.0: `scar_loop_bypass`, `scar_tool_class_misdeclared`, `scar_perception_mutation`, `scar_phantom_sovereignty`

---

## 16. Breach Contract per Primitive *(Updated for 8 Primitives)*

| Primitive | Breach trigger | Class | Response |
|---|---|---|---|
| **Identity** | Any spoof | CONST | VOID + identity lock |
| **Perception** | E4 violation (perception mutated reality) | CONST | VOID + scar candidate `scar_perception_mutation` |
| **Skills** | Domain misdeclared | LOCAL | HOLD + scar candidate |
| **Tools** | T1 violation (tool_class undeclared or misdeclared); T2 violation (no band approval) | CHAIN / CONST | VOID FORGE + BREACH seal |
| **Memory** | Seal mutation | CONST | System-wide VOID + emergency audit |
| **State** | Lease/lock bypass | CHAIN | HOLD + cooling increment |
| **Kernel** | Verdict without evidence; K6 violation (domain reasoning) | CONST | VOID + kernel health DEGRADE |
| **Actuator** | Execution mismatch with sealed plan; SEAL without verify_receipt at MATERIAL+ | CONST | VOID + BREACH seal + scar candidate `scar_loop_bypass` |
| **Agent** | Repeated breaches; L6 self-elevation claim (AG5) | SOVEREIGN | Identity lock + external review + scar candidate `scar_phantom_sovereignty` |

---

## Appendix A — F1–F13 Invariants (cheat-sheet)

| Floor | Test |
|---|---|
| F1 AMANAH | Reversible-first; every mutation either reversible or backed-up |
| F2 TRUTH | Every claim labelled OBS \| DER \| INT \| SPEC |
| F3 WITNESS | SEAL requires Human × AI × External witnesses |
| F4 CLARITY | ΔS ≤ 0 target; RSI loop on violation |
| F5 PEACE² | De-escalate; guard weakest stakeholder |
| F6 MARUAH | Never name individuals — reference roles |
| F7 HUMILITY | 0.90 cap on OBS evidence |
| F8 GENIUS | G ≥ 0.80 target; 17× rule at 51→85% boundary |
| F9 ANTI-HANTU | No consciousness / qualia / sentience claims |
| F10 ONTOLOGY | AI substrate ≠ being |
| F11 AUDIT | Every action logged + actor_signature |
| F12 INJECTION | External ≠ authority; sanitise |
| F13 SOVEREIGN | 888_HOLD escalates to Arif for irreversible ratification. **L6 is human-only.** |

---

## Appendix B — Action Bands *(NEW in v2.0 — Replaces binary SEAL)*

SEAL is not binary. Action bands scale the gate with reversibility and blast radius.

| Band | Examples | Gate | Authority |
|---|---|---|---|
| **OBSERVE** | read logs, query read-only DB, fetch metadata | Session + provenance | Identity |
| **PREPARE** | draft, plan, simulate, derive, classify | Log + bounded authority | Identity |
| **REVERSIBLE** | temp branch, restart sandbox, scratch file, internal message | Lease + rollback | Identity + Lease |
| **MATERIAL** | commit, deploy, send externally, mutate shared state | Kernel SEAL at MATERIAL band + VERIFY (G8) | Kernel |
| **IRREVERSIBLE / SOVEREIGN** | delete, publish, financial commitment, F13 override | Explicit human/F13 authority + receipt | Human/F13 |

**Rule:** Actuator executes after sufficient authority, not necessarily after full SEAL. Observe and Prepare bands do not require SEAL — only provenance and bounded authority. Material and Irreversible bands require SEAL (and Material+ requires verify_receipt before SEAL commits).

---

## Appendix C — Stage / Class / Node Namespaces *(NEW in v2.0)*

The numbers 333, 555, 888, 999 are reused across verbs, agent classes, and constitutional nodes. Use full namespaces in formal references.

| Namespace | Example | Meaning |
|---|---|---|
| **STAGE-333** | THINK | Verb in the constitutional chain |
| **CLASS-333** | AGI | Agent class (333-AGI warga) |
| **STAGE-555** | CRITIQUE | Verb in the chain |
| **CLASS-555** | ASI | Agent class (555-ASI warga) |
| **NODE-888** | APEX / JUDGE | Constitutional node (Kernel verdict) |
| **STAGE-999** | RECEIPT / SEAL | Verb in the chain (VAULT999 commit) |

**Rule:** When referencing any of these in logs or receipts, use the full namespace (STAGE-333, CLASS-333, NODE-888). Bare numbers are ambiguous and unacceptable.

---

## Appendix D — Host Membrane Modes (per `HOST_MEMBRANE_AWARENESS`)

| Mode | arifOS Trust | Evidence Path |
|---|---|---|
| `direct_runtime` | **FULL** | VPS as root, MCP stdio direct, all organs reachable on localhost |
| `hosted_runtime` | PARTIAL | Host may block; require transport proof per claim |
| `delegated_runtime` | MEDIATED | Verify 777 FORGE delegation chain |
| `sovereign_runtime` | COMPLETE | Direct MCP :8088 + F13 SOVEREIGN session |

---

## Versioning

- **v1** — initial Kimi-side draft (Agent treated as 8th primitive).
- **v1.1** — corrective revision per F13 sovereign review: Agent reclassified as composite organism.
- **v1.2** — breach protocol added (sections 13–16): breach classes, detection hooks, response protocol, per-primitive breach contracts.
- **v2.0** — *this artifact.* Verdict 2026-07-12 PROCEED_WITH_CORRECTION applied:
  - Perception primitive added (was implicit in Tools).
  - 5-class Tool taxonomy (OBSERVATION / COGNITION / COMMUNICATION / ACTUATION / GOVERNANCE).
  - Tool ≠ Actuator clarified; T1 reframed as Class Disclosure.
  - VERIFY step added to chain (13 verbs total, was 12).
  - Closed-loop chain: FORGE → VERIFY → SEAL (was FORGE → SEAL).
  - Action bands replace binary SEAL (Observe / Prepare / Reversible / Material / Irreversible).
  - Stage / Class / Node namespaces separated.
  - Kernel scope narrowed (K6 — no domain reasoning).
  - Agent AG5 — no L6 self-elevation.
  - Agent AG6 — SEAL at MATERIAL+ requires verify_receipt (G8).
  - Loop-bypass becomes `scar_loop_bypass`.
  - Phantom sovereignty becomes `scar_phantom_sovereignty`.
- **v2.1** — when SEAL stamp completes for v2 corrections, append `seal_anchor + chain_hash`; cross-link carry_forward.json doctrines 1–7 plus the 7 principal corrections.

**Pre-forge snapshots (F1 reversibility):** `/root/A-FORGE/forge_work/2026-07-12/{eureka-zen-alignment,eureka-zen-purge,eureka-zen-forge,skill-mesh-sync}/`

---

*DITEMPA BUKAN DIBERI.*