# HERMES Deliverable: F1–F13 ↔ I-01–I-24 Mapping + Axis Disambiguation

> **Status:** DRAFT FOR F13 REVIEW — not applied, not sealed
> **Author:** HERMES (cross-plane review of Orthogonality Contract v0.1)
> **Date:** 2026-09-16
> **Depends on:** OpenClaw deliverables in this directory (skill-namespace-mapping, openclaw-edge-disposition)

---

## 1. Why This Mapping Exists

The Orthogonality Contract (v0.1) introduces 24 universal invariants (I-01–I-24). The arifOS constitution already defines 13 floors (F1–F13). Without an explicit mapping, the federation has two parallel law sources — a violation of the contract's own I-16 (no duplicate doctrine).

**This document establishes the derivation chain:** every invariant traces to a floor, a canon fragment, or is declared genuinely new.

---

## 2. Axis Disambiguation

The Orthogonality Contract defines **four interaction planes**. Three existing canon fragments also define axes. These are NOT competing — they operate on different dimensions.

| Axis | Dimensions | Canon Fragment | Question It Answers |
|---|---|---|---|
| **Interaction Planes** (Orthogonality Contract) | Human / Workshop / Protocol / Implementation | New (this document) | *Where does work happen?* |
| **Security Planes** | Reasoning / Execution / Control | `three-plane-architecture.md` (2026-09-05, F13 sealed) | *Where is intelligence untrusted?* |
| **Context Geometry** | IDENTITY / LAW / MEMORY / INTENT / STATE / PROTOCOL | `context-axes.md` (2026-09-02) | *What kind of fact is this?* |
| **Design Principles** | MODULAR / ORTHOGONAL / FRACTAL / THOROIDAL / PLASTICITY | `modular-orthogonal-federation.md` (2026-09-10, DRAFT_AWAITING_F13) | *How do capabilities compose?* |
| **Authority Layers** | AAA (why) → Kernel (if) → A-FORGE (how) → VAULT999 (proof) | `four-layer-separation.md` (2026-09-13, F13 sealed) | *Who has power at each stage?* |

**Supersession rule:** The Orthogonality Contract governs the Interaction Planes axis ONLY. It does not supersede, modify, or compete with any other axis. I-16 is satisfied because no axis duplicates another — they are orthogonal coordinates.

**Relationship example:**
- A coding agent writes code → **Implementation** (interaction plane) in the **Execution** (security plane) under a **change-contract** (authority layer) tracked as **PROTOCOL** context (context geometry) following **modular** design principles.
- One agent, five axes, no overlap.

---

## 3. F1–F13 Floor Definitions (for reference)

| Floor | Name | Type | Summary |
|---|---|---|---|
| F1 | AMANAH | HARD | Reversible-first. Irreversible → 888_HOLD. |
| F2 | TRUTH | HARD | P(truth) ≥ 0.99. Epistemic labels. Cheap claims → VOID. |
| F3 | TRI-WITNESS | DERIVED | Human × AI × Earth × Verifier ≥ 0.75 (Nash product). |
| F4 | CLARITY | HARD | ΔS ≤ 0 — every output reduces entropy. |
| F5 | PEACE² | SOFT | Non-destructive power. Blocks harm/harass/extort. |
| F6 | EMPATHY ⇄ MARUAH | SOFT | Protect weakest stakeholder; preserve dignity. |
| F7 | HUMILITY | HARD | Ω₀ ∈ [0.03, 0.05]. No fake certainty. |
| F8 | GENIUS | DERIVED | G = (A×P×E×X)^(1/4) ≥ 0.80 for complex actions. |
| F9 | ANTIHANTU | HARD | No deception, manipulation, or consciousness claims. |
| F10 | ONTOLOGY | HARD | AI-only ontology. No soul / feelings / sentience. |
| F11 | AUDITABILITY | HARD | Every decision logged, inspectable, attributable. |
| F12 | RESILIENCE | HARD | Injection defense. Risk < 0.85. |
| F13 | SOVEREIGN | HARD | Human veto FINAL. Harness switch belongs to sovereign. |

---

## 4. Invariant ↔ Floor Mapping

### 4.1 Direct Derivations (invariant is a plane-specific expression of an existing floor)

| Invariant | Statement | Derives From | Derivation Logic |
|---|---|---|---|
| **I-01** | Human sovereignty | **F13** SOVEREIGN | F13 is the floor; I-01 is its expression across all four interaction planes. No agent on any plane may override human decision. |
| **I-02** | Authority separation | **F13** + **four-layer-separation** | F13 forbids self-authorization; four-layer separation enforces AAA→Kernel→A-FORGE→VAULT999 chain. I-02 extends this to peer agents within a plane. |
| **I-03** | No self-authorisation | **F13** + **authority-envelope.md** | F13 = human-only SEAL. Authority-envelope = "Confidence is not authority." I-03 is the plane-level expression of both. |
| **I-04** | Explicit action class | **F1** AMANAH + **F4** CLARITY | F1 requires reversible-first; F4 requires entropy reduction. Explicit classification prevents accidental irreversible action (F1) and ambiguous dispatch (F4). |
| **I-05** | Bound approval | **F1** AMANAH + **F13** | F1 demands reversibility; I-05 binds approval to exact payload/hash/nonce so the F1 reversal path is determinable. F13 ensures only sovereign can issue. |
| **I-06** | Four-truth receipt | **F2** TRUTH + **F11** AUDITABILITY | F2 = epistemic label integrity. F11 = every decision attributable. I-06 requires all four truth conditions (transport, execution, semantic, policy) simultaneously. |
| **I-07** | No silent default | **F2** TRUTH + **F7** HUMILITY | F2 forbids false epistemic labels. F7 forbids fake certainty. I-07 prevents missing data from silently becoming "observed" or "PASS". |
| **I-08** | Input fidelity | **F2** TRUTH + **F11** | F2 = truth discipline. F11 = auditability. I-08 ensures every material input has a consumed-field record — without it, audit trails have holes. |
| **I-09** | Evidence-bound named claims | **F2** TRUTH + **F6** MARUAH | F2 requires evidence chains. F6 protects human dignity — misattributing claims to named persons violates maruah. I-09 binds both. |
| **I-10** | Claim typing | **F2** TRUTH | Direct expression. F2 defines OBS/DER/INT/SPEC labels; I-10 extends the typology to the full inter-plane state machine (Observed → Derived → Interpreted → Assumed → Speculated → Unmeasured → etc). |
| **I-11** | Runtime over declaration | **F2** + **F12** RESILIENCE | F2 = truth is measured, not declared. F12 = resilience requires knowing actual state. Schema presence ≠ runtime capability. |
| **I-12** | Five-manifest truth | **F2** + **F11** | F2 = epistemic labels. F11 = attribution. I-12 specifies that source, build, runtime, public, and probe are five distinct manifests — conflating them produces false confidence. |
| **I-13** | Tool narrowness | **F4** CLARITY + **modular** principle | F4 = ΔS ≤ 0 (entropy reduction). Modular = "each capability is a sealed unit." I-13 prevents multi-axis tools from leaking conclusions across domains. |
| **I-17** | Safe delegation | **F1** + **F13** | F1 = reversibility. F13 = human sovereignty. I-17 allows work reduction but forbids accountability transfer — subagents get bounded scope, never sovereign authority. |
| **I-18** | Reversible forging | **F1** AMANAH | Direct expression. F1 is reversible-first; I-18 makes this concrete for coding agents: branch/PR/test, not direct production mutation. |
| **I-19** | Receipt ≠ truth by assertion | **F2** + **F11** | F2 = measured truth. F11 = auditability. A receipt proves recording under specific state — not that the claim is true. Prevents receipt-washing. |
| **I-22** | Time is part of truth | **F2** + **F12** | F2 = truth discipline. F12 = resilience requires current state. A claim without observation time is stale — it may be historically accurate but not decision-grade. |
| **I-23** | Error containment | **F9** ANTIHANTU + **F5** PEACE² | F9 = no deception. F5 = non-destructive. Exposing file paths, tokens, or stack traces to public surfaces is both deceptive (implies safety) and destructive (enables attack). |
| **I-24** | Honest abstention | **F2** + **F7** HUMILITY | F2 = truth labels. F7 = no fake certainty. UNMEASURED, CONFLICTED, VOID etc. are successful truth-preserving outcomes — not failures. Admits ignorance honestly. |

### 4.2 Composite Derivations (invariant draws from two or more floors + canon fragments)

| Invariant | Statement | Derives From | Notes |
|---|---|---|---|
| **I-14** | Protocol role separation | **F13** + **four-layer-separation** + **modular** | F13 assigns authority. Four-layer assigns layers. Modular assigns module boundaries. I-14 combines all three for protocol-specific roles (MCP invokes, A2A exchanges, HERMES interacts, coding agents forge, A-FORGE executes). |
| **I-15** | Least attention | **F4** CLARITY + **modular** + **dunbar-constraint** | F4 = entropy reduction. Modular = sealed units. Dunbar = cognitive limit enforcement. I-15 ensures agents load minimum viable skills. |
| **I-16** | No duplicate doctrine | **four-layer-separation** + **modular** + **context-axes** | Four-layer = one layer per function. Modular = one gate per module. Context-axes = one owner per axis. I-16 generalizes: one canonical skill, one evidence contract, one receipt model. |
| **I-20** | Calibration before promotion | **F2** + **F7** + **F12** | F2 = truth. F7 = humility. F12 = resilience. A capability remains SPECULATED until operational metrics, negative controls, and failure modes are proven. Prevents premature capability claims. |
| **I-21** | No personality inference | **F6** MARUAH + **F9** ANTIHANTU + **F10** ONTOLOGY | F6 = dignity. F9 = no deception. F10 = AI-only ontology. Analyzing structures and incentives ≠ diagnosing hidden motives. Protects human dignity, prevents consciousness claims, maintains ontological boundary. |

### 4.3 Genuinely New (no direct floor ancestor)

| Invariant | Statement | New? | Notes |
|---|---|---|---|
| **I-16** (partially) | "One canonical governance skill" | **Yes** — operational specificity | Floors define what must be true; I-16 defines how many implementations may exist. This is an architectural constraint not derived from any floor. |
| **I-17** (partially) | "Subagents receive bounded scope, no implicit production credentials" | **Partially new** — extends F1/F13 to delegation topology | F1/F13 apply to the sovereign-human boundary. I-17 extends the same principle to agent-to-subagent chains. Novel expression. |

**Conclusion:** No invariant is entirely without floor ancestry. Two invariants contain genuinely new operational specificity layered on top of existing floors. No invariant contradicts any floor.

---

## 5. Enforcement Ownership per Interaction Plane

The contract needs to specify which institution bears enforcement responsibility on each plane. AAA as cross-plane institution (as proposed in the desk analysis) is the correct model.

| Plane | Primary Enforcer | Instrument | Floor Enforcement |
|---|---|---|---|
| **Human** | HERMES | Bridge protocol, consent gates, decision dossiers | F13 (human veto), F6 (maruah), F7 (humility) |
| **Workshop** | OpenClaw | Task decomposition, subagent leases, progress receipts | F1 (reversibility), F4 (clarity), I-17 (safe delegation) |
| **Protocol** | A2A wire + AAA governance | Agent cards, typed tasks, trace propagation | I-14 (protocol roles), I-16 (no duplicate doctrine) |
| **Implementation** | Coding Agents + A-FORGE | Change contracts, branch/PR, execution verification | F1 (reversibility), I-18 (reversible forging), I-05 (bound approval) |
| **Cross-cutting** | AAA | Constitutional reflex, eureka sealing, canon maintenance | All floors — AAA is the governance institution that crosses every plane |

**Key principle:** AAA does not belong to one plane because governance does not belong to one workspace. AAA is present on every plane as the institutional layer that enforces constitutional floors. The planes define where work happens; AAA defines who authorises and confirms.

---

## 6. Supersession Declaration

This document does NOT supersede:
- `three-plane-architecture.md` (security axis — different dimension)
- `context-axes.md` (context geometry — different dimension)
- `modular-orthogonal-federation.md` (design principles — different dimension)
- `four-layer-separation.md` (authority layers — different dimension)

This document governs: the **Interaction Planes axis** (Human / Workshop / Protocol / Implementation) as introduced by the Federation Orthogonality Contract.

Cross-axis interactions are expected and do not constitute doctrine conflict. A single agent action may reference coordinates on all five axes simultaneously (see §2 example).

---

## 7. Gaps Requiring F13 Decision

1. **AAA formalization as cross-plane institution:** The desk analysis proposes AAA as cross-plane governance. This mapping adopts that framing. F13 must ratify or reject.
2. **I-06 partial failure states:** The contract defines four-truth as conjunction. HERMES proposes four distinct failure types (TRANSPORT_FAILURE, EXECUTION_FAILURE, SEMANTIC_FAILURE, POLICY_FAILURE) as separate states, not just FAIL. F13 must decide if this expansion enters v0.2 or is deferred.
3. **OpenClaw plane status:** OpenClaw is runtime-witnessed but role-card pending. The desk analysis suggests "PLANNED PLANE" but OpenClaw correctly notes its runtime exists. F13 must decide the label: PROPOSED / WITNESSED_ROLE_PENDING / or other.
4. **I-21 vs F10 scope:** I-21 (no personality inference) extends beyond F10 (AI-only ontology) into political/social/behavioural analysis. F13 must confirm this extension is intentional.

---

*DITEMPA BUKAN DIBERI ⚒️*
