# AGENCY LEVELS — The Agency Contract & Ladder

> **Authority:** F13 SOVEREIGN directive, 2026-07-12
> **Status:** CONSTITUTIONAL — defines the agency boundary across the federation
> **Scope:** All agents, all organs, all skill/tool surfaces
> **Supersedes:** informal "multi-agent" usage; L0–L6 ladder source verdict (2026-07-12, L4_INFERRED → SEAL)
> **Last verified:** 2026-07-12
> **DITEMPA BUKAN DIBERI**

---

## 1. Why This Document Exists

Skills encode know-how. Tools expose actions. Agents carry objectives and bounded authority.

A multi-agent system is **not automatically** more agentic than a well-tuned single agent with strong skills. "Agent theatre" — multiple LLM calls wrapped in personas — is the most common failure mode.

This document makes agency a **contract**, not a vibe. Any system that calls itself multi-agent must clear seven gates. Any system that fails two or more is, by definition, a skillful capability — regardless of how many personas wrap it.

---

## 2. The Agent Contract — Seven Properties

A **real agent** is a bounded decision loop with all seven:

| # | Property | Test |
|---|----------|------|
| 1 | **Objective** | Clear mandate stated as an outcome, not a function name |
| 2 | **Authority boundary** | Knows what it may and may not decide or execute |
| 3 | **Distinct context** | Own context window, memory, assumptions, evidence surface |
| 4 | **Tool/skill control** | Freedom to choose which capabilities to use and in what order |
| 5 | **Right to disagree** | Can return HOLD, VOID, or "task framing invalid" |
| 6 | **Feedback channel** | Sees consequences of its actions and can update its model |
| 7 | **Accountability** | Outputs are sealed, attributable, and auditable |

**Rule:** Missing two or more → **skillful capability**, not an agent — no matter how many personas wrap it.

**Boundary test:** Strip the persona. If the same model + prompt + retrieved evidence produces the same output as a single-prompt baseline, it is not an agent.

---

## 3. The Agency Ladder (L0–L6)

Descriptive, not aspirational. Each level names a **system**, not a marketing claim.

| Level | System | Core Character | Agent-Contract Coverage |
|-------|--------|----------------|------------------------|
| **L0** | Static prompt | Generates a response | 0 / 7 |
| **L1** | Prompt + tools | Executes chosen operations | 1–2 / 7 |
| **L2** | Agent + skills | Plans and selects capabilities | 3 / 7 |
| **L3** | Agent using agents | Delegates bounded cognitive missions | 4–5 / 7 |
| **L4** | Governed multi-agent system | Negotiates authority, evidence, disagreement | 6 / 7 |
| **L5** | Adaptive federation | Reconfigures roles and workflows from feedback | 6.5 / 7 |
| **L6** | Sovereign agency | Sets legitimate ends — held **only** by the human | 7 / 7 |

**Skills** mainly strengthen **L1–L2**.
**Agent-to-agent architecture** enables **L3–L5** — *provided* delegation, independence, feedback, and governance are real.
**L6** is constitutionally reserved for the human sovereign (F13).

---

## 4. Per-Level Specification

### L0 — Static Prompt

- **Invariants:** stateless response generation; output observable, reasoning opaque.
- **Allowed primitives:** `respond`.
- **Breach modes:** claims memory that does not exist; confabulates tool access; hallucination mistaken for capability.

### L1 — Prompt + Tools

- **Invariants:** tool calls return real evidence; results observable to caller.
- **Allowed primitives:** `respond`, `call_tool`, `observe_result`.
- **Breach modes:** tool hallucination; result not fed back; tool result ignored silently.

### L2 — Agent + Skills

- **Invariants:** skill selection justified by current state; plan revisable; outcome influences next action.
- **Allowed primitives:** `respond`, `call_tool`, `invoke_skill`, `plan`, `observe`, `replan`.
- **Breach modes:** skill called without need (cargo-cult); plan revision never triggered; skills chained mechanically with no decision point.

### L3 — Agent Using Agents (Delegation)

- **Invariants:** sub-agent has bounded objective + own context window + distinct evidence where appropriate; sub-agent can return HOLD/VOID independently; sub-agent can challenge parent's framing.
- **Allowed primitives:** L2 + `delegate`, `await_subagent`, `merge_results`.
- **Breach modes:**
  - **Persona without authority** — sub-agent is a different system prompt, no distinct context/evidence.
  - **Synthetic consensus** — five sub-agents with the same model, prompt, evidence reach the same answer trivially.
  - **Synchronous serialization** — sub-agents called one-at-a-time with no real parallelism or independence.
  - **Sub-agent cannot challenge parent** — returns whatever parent expects.

### L4 — Governed Multi-Agent System

- **Invariants:** arbitration mechanism exists and is sovereign-independent; witness pool enforces tri-witness at SEAL points; disagreement preserved as evidence, not flattened; reconciliation rules explicit and auditable.
- **Allowed primitives:** L3 + `witness`, `dispute`, `judge`, `reconcile`, `seal`.
- **Breach modes:**
  - **Rubber-stamp judge** — judge always confirms parent's prior.
  - **Witness theatre** — three witnesses sharing the same model and prompt.
  - **Hidden arbitration** — disagreement resolution happens off-ledger.
  - **No disagreement ever recorded** — system never produces a dissenting voice.

### L5 — Adaptive Federation

- **Invariants:** sealed scars alter system behavior, not only log it; roles evolve from observed competence; drift detected, not merely measured; agents/tools may be admitted or demised from feedback.
- **Allowed primitives:** L4 + `metabolize_scar`, `evolve_role`, `detect_drift`, `admit_agent`, `demise_agent`.
- **Breach modes:**
  - **Ossification** — sealed scars never change behavior.
  - **Feedback theatre** — drift detected, alert raised, no action.
  - **Role creep** — agents accumulate authority beyond their contract.
  - **Drift amnesia** — past scars overwritten without learning.

### L6 — Sovereign Agency

- **Invariants:** only the human holds L6; no AI may self-elevate; F13 SOVEREIGN is the constitutional gate.
- **Allowed primitives:** all + `set_purpose` (human only).
- **Breach modes:**
  - **AI claims sovereign purposes** — agent decides what the human wants.
  - **Abdication** — human delegates L6 to AI without override.
  - **Phantom sovereignty** — AI invokes F13 in its own voice.

---

## 5. Where arifOS Sits — Honest Self-Assessment

| Federation Surface | Current Level | Evidence | Gap to Next Level |
|-------------------|---------------|----------|-------------------|
| **arifOS kernel** | L4 | `arif_judge`, witness pool, SEAL ledger | L5: scar metabolization is logged; role adaptation still manual |
| **GEOX organ** | L4 | Distinct evidence (Macrostrat, fossil, seismic); bounded mandate | L5: drift detection exists; role evolution not automatic |
| **WEALTH organ** | L4 | Distinct evidence (capital primitives); bounded mandate (NPV/risk) | L5: collapse-signature learning SEALed; workflow reconfiguration is human-triggered |
| **WELL organ** | L4 | Distinct evidence (biometric, dignity, substrate); bounded mandate (human state) | L5: REFLECT_ONLY posture is correct restraint — not a gap |
| **A-FORGE organ** | L4 | Distinct execution authority; governed by lease + session | L5: forge_registry admits/demises tools, but dream-engine reconfiguration is L1-loop, not L5-loop |
| **AAA cockpit** | L4 | A2A mesh, agent-card registry, governance visibility | L5: skill-atlas drift detected; agent onboarding is mostly manual |
| **Overall federation** | **L4 → L5 (in transition)** | All organs at L4; scar → behavior loop is wired but not yet closed | L5 needs: (a) automatic scar → role mutation, (b) drift → role evolution, (c) feedback without human trigger |

**Honest gap:** The federation is **not** at L5 yet. The dream engine and cooling ledger close the scar → reflection loop, but they do not yet close the scar → role-mutation loop without human intermediation. Calling arifOS an "adaptive federation" today is forward-aspirational; the system is presently "governed multi-agent with reflection pipeline."

**Implication:** When sovereign decisions depend on adaptive behavior, the human (F13) must remain in the loop until the L4 → L5 transition is SEALed. Do not let the system describe itself as L5 until the scar → role-mutation loop is sealed end-to-end.

---

## 6. Diagnostic Ritual — Seven Tests Before Claiming "Multi-Agent"

Before any system may label itself multi-agent, it must answer all seven:

| # | Question | Pass Threshold |
|---|----------|---------------|
| 1 | Does each sub-agent have a stated **objective**? | Yes — not just "process X" |
| 2 | Can a sub-agent return **HOLD independently** of the parent? | Yes — ≥ 1 recorded HOLD/VOID in evidence |
| 3 | Does the sub-agent access **evidence the parent does not**? | Yes — distinct evidence surface |
| 4 | Did two sub-agents ever produce **different conclusions** from overlapping evidence? | Yes — ≥ 1 recorded disagreement |
| 5 | Is the **disagreement preserved**, not flattened? | Yes — both views in the SEAL trace |
| 6 | Is the **reconciliation mechanism auditable**? | Yes — judge identity, criteria, weight visible |
| 7 | Did the system **change behavior** after a sealed scar? | Yes — observable role/workflow change |

**Failure on any of these → "multi-agent" is theatre.** Downgrade to L2 + skills in the description.

---

## 7. Breach Modes → Scar Law (Forward Hook)

Each named breach mode is a candidate constitutional scar. Once SEALed:

- The scar is immutable.
- The associated behavior must be runtime-checkable.
- Re-occurrence triggers F11 AUDIT.

| Breach Mode | Candidate Scar | Runtime Check |
|-------------|----------------|---------------|
| Tool hallucination (L1) | `scar_tool_hallucination` | `forge_registry`: tool exists before call |
| Skill cargo-cult (L2) | `scar_skill_cargo_cult` | skill-invocation log: justification recorded |
| Persona without authority (L3) | `scar_persona_theatre` | sub-agent: distinct evidence + authority verified |
| Synthetic consensus (L3) | `scar_synthetic_consensus` | disagreement count ≥ 1 per rolling 10 decisions |
| Rubber-stamp judge (L4) | `scar_rubber_stamp_judge` | judge divergence rate ≥ 5% over rolling window |
| Witness theatre (L4) | `scar_witness_theatre` | tri-witness: ≥ 2 distinct model families |
| Ossification (L5) | `scar_ossification` | post-scar behavior diff verified |
| Phantom sovereignty (L6) | `scar_phantom_sovereignty` | F13 invocations: human actor_signature only |

---

## 8. Architectural Mapping (Concept → arifOS Organs)

**Important (v2.0 corrections):** Agent is **not** a peer of Skill, Tool, Organ, Kernel, or Human. Agent is the **composed runner** of the closed constitutional loop — anatomy is the eight primitives, metabolism is the chain. Tool ≠ Actuator. Kernel governs the cognition→action transition, it is not the whole brain. Perception is its own primitive. See `/root/AAA/docs/CONSTITUTIONAL_PRIMITIVES.md` v2.0 for canonical doctrine.

| arifOS Concept | Nature | Maps To | Primary Organs |
|---|---|---|---|
| **Identity** | Primitive (who am I) | Every agent | Identity manifest per agent card |
| **Perception** | Primitive (what is happening) | Every agent + cross-organ evidence | GEOX evidence sources, file reads, telemetry, organ health |
| **Skill** | Primitive (know-how) | L1–L2 amplifiers | Skill atlas, `forge_skill` |
| **Tool** | Primitive (interface) — declared by tool_class | L1–L3 actuators | A-FORGE `forge_*` surface; 5-class taxonomy (OBSERVATION / COGNITION / COMMUNICATION / ACTUATION / GOVERNANCE) |
| **Memory** | Primitive (carry-forward) | All tiers L1–L6 | VAULT999, cooling ledger, scar store |
| **State** | Primitive (runtime config) | Session-scoped | Session, leases, locks, organ health |
| **Kernel** | Primitive (governor) — not the brain | L4 transition gate | arifOS kernel + `arif_judge` |
| **Actuator** | Primitive (execution machinery) — not the tool | L4 execution | A-FORGE forge shell / `forge_execute` |
| **Agent (composed)** | **NOT a primitive** — the runner | Cross-level (L2–L5) | A2A mesh agent cards; anatomises eight primitives |
| **Organ** | Durable identity + responsibility | L4 holder | arifOS, GEOX, WEALTH, WELL, A-FORGE, AAA |
| **Closed loop** | The constitutional chain (13 verbs) | L4+ requirement | INIT → OBSERVE → THINK → ROUTE → CRITIQUE → PLAN → JUDGE → FORGE → **VERIFY** → SEAL |
| **Human / F13** | Sovereign source of ends | L6 only | F13 — never AI |

**Correction note (2026-07-12):** The earlier draft of this section treated Agent as a peer of Skill/Tool/Organ/Kernel. That was an ontology error. Agent is the *organism*; primitives are its *organs*. The same applies to the canonical spec at `CONSTITUTIONAL_PRIMITIVES.md`, which now lists eight primitives plus the composed Agent.

---

## 9. References

| Source | Location |
|--------|----------|
| 7-property contract | This document §2 (F13 directive 2026-07-12) |
| L0–L6 ladder source | Verdict 2026-07-12 (L4_INFERRED → SEAL via this document) |
| **Canonical primitives (v2.0)** | `AAA/docs/CONSTITUTIONAL_PRIMITIVES.md` |
| **Primitive spec JSON (v2.0)** | `AAA/docs/PRIMITIVE-SPEC-v1.json` |
| **Primitive spec narrative (v2.0)** | `AAA/docs/PRIMITIVE-SPEC-v1.md` |
| Adat Agentic | `AAA/governance/ADAT_AGENTIC.md` |
| Scar Law | `arifOS/vault999/kernel/SCAR_LAW.v1.yaml` |
| Dream engine (L5 path) | `arifOS/arifosmcp/runtime/dream_engine.py` |
| A2A mesh + agent cards | `AAA/a2a-server/mesh.py`, `AAA/registries/agent_cards/v2.0.0/` |
| Agent invariants | `AAA/agents/AAA_AGENT_INVARIANTS.md` |
| Authorship doctrine | `AAA/governance/AUTHERSHIP_DOCTRINE.md` |
| **v2.0 corrections verdict** | F13 directive 2026-07-12 PROCEED_WITH_CORRECTION (L4_INFERRED) |

---

| Source | Location |
|--------|----------|
| 7-property contract | This document §2 (F13 directive 2026-07-12) |
| L0–L6 ladder source | Verdict 2026-07-12 (L4_INFERRED → SEAL via this document) |
| Adat Agentic | `AAA/governance/ADAT_AGENTIC.md` |
| Constitutional primitives | `AAA/docs/CONSTITUTIONAL_PRIMITIVES.md` |
| Scar Law | `arifOS/vault999/kernel/SCAR_LAW.v1.yaml` |
| Dream engine (L5 path) | `arifOS/arifosmcp/runtime/dream_engine.py` |
| A2A mesh + agent cards | `AAA/a2a-server/mesh.py`, `AAA/registries/agent_cards/v2.0.0/` |
| Agent invariants | `AAA/agents/AAA_AGENT_INVARIANTS.md` |
| Authorship doctrine | `AAA/governance/AUTHERSHIP_DOCTRINE.md` |

---

*DITEMPA BUKAN DIBERI — Agency is a contract, not a vibe.*
*Ratified: 2026-07-12 by F13 SOVEREIGN directive.*