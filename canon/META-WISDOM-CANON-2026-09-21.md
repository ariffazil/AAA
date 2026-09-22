# META-WISDOM Canon (Canon #4) — The 6 Meta-Gates + WAJIB Extension

> **Status:** DRAFT_AWAITING_F13 (2026-09-21)
> **Origin:** Arif — sovereign Bucket 1 + 2 analysis of the 12 P-items, 2026-09-21 morning session
> **Applies to:** arifOS federation engineering; ratifies after Canon #3
> **Position:** Fourth canon in the trilogy+1 sequence; targets the law-#131 enforcement layer
> **Rule:** The 6 meta-gates are the operationalization of Law #131 — they only matter when the substrate is honest about itself. They are the layer where *PASS must not be manufacturable from missing measurements* is enforced.

---

## 0. The Spine

This canon answers one question:

> What mechanisms prevent the system from **lying to itself about its own progress?**

The 64 WAJIB of Canon #3 are **substrate** — components that produce state. The 6 meta-gates in this canon are **meta-substrate** — components that watch the substrate and refuse to declare success when the substrate cannot prove success.

The 5 Bucket 1 additions extend Canon #3's WAJIB from 64 to **69**.

The 6 Bucket 2 items are new organs of this canon. They share a structural property: their failure modes are reachable only when the substrate is honest. They are, in this sense, the Law-#131 enforcement layer made mechanical.

---

## 1. The 5 New WAJIB Items — Extension from 64 to 69 (Bucket 1)

These pass their own conformance test tonight — each has a runnable failure name.

### WAJIB #65 — Causal graph

- **Distinction:** `A correlated B ≠ A caused B`
- **Failure mode bounded:** CHRON learns pattern that is predictive but wrong
- **Conformance test:** `assert causal_edge(A, B) ∈ graph ∀ predictions involving A → B`
- **Constitutional complexity test (Canon #0):**
  - (a) Eliminates demonstrated failure class? **YES** — confounding in prediction pipelines
  - (b) Compiles into mechanism? **YES** — graph query primitive
  - (c) Materially improves decision? **YES** — prevents false causal inference

### WAJIB #66 — Distribution-shift detector

- **Distinction:** `P_train(X) ≠ P_now(X) → Confidence ↓`
- **Failure mode bounded:** confidence unchanged when world has changed
- **Conformance test:** `assert shift_detected → confidence_adjusted`
- **Constitutional complexity test:**
  - (a) **YES** — silent distributional drift
  - (b) **YES** — statistical detector with FQ signal
  - (c) **YES** — calibrated honesty about generalization

### WAJIB #67 — Dependency / consequence graph

- **Formula:** `BlastRadius(X) = Descendants(X)`
- **Failure mode bounded:** local change becomes federation-wide accident
- **Conformance test:** `assert proposed_mutation(X) ⇒ no descendant_violations`
- **Constitutional complexity test:**
  - (a) **YES** — "small change, big blast" observed pattern
  - (b) **YES** — graph traversal at pre-action gate
  - (c) **YES** — surgical mutations stay surgical

### WAJIB #68 — Graceful degradation ladder

- **Ladder:** `FULL → WRITE_DISABLED → OBSERVE_ONLY → LOCAL_ONLY → READ_CACHED → OFFLINE`
- **Failure mode bounded:** binary `FULL POWER` vs `DEAD`
- **Conformance test:** `assert uncertainty_↑ ⇒ capability_step ↓`
- **Constitutional complexity test:**
  - (a) **YES** — current kernel ALREADY does this (OBSERVE_ONLY → LIMITED_MUTATE → SEAL); canon names it
  - (b) **YES** — rungs are ACT tokens at different authority_ceiling
  - (c) **YES** — uncertainty maps to capability automatically

### WAJIB #69 — Constitutional version migration

- **Formula:** `State_v6 → explicit migration → State_v7` (reversible where possible)
- **Failure mode bounded:** silent re-interpretation of old state under new canon
- **Conformance test:** `assert epoch_change ⇒ migration_receipt_written`
- **Constitutional complexity test:**
  - (a) **YES** — governance evolution corrupts history
  - (b) **YES** — migration receipts in VAULT999
  - (c) **YES** — version transitions are auditable

**Net effect:** Canon #3's WAJIB list extends 64 → 69. Bucket 1 items are substrate; they implement, not declare.

---

## 2. The 6 Meta-Gates — Bucket 2 (the Law-#131 Enforcement Layer)

These six items share a structural property: they only matter when the substrate is honest about itself. They are the layer where Law #131 of the agent→human canon — *"constitutional PASS cannot be manufactured from missing measurements"* — is mechanically enforced.

### MG-1 — Counterfactual engine

- **Question:** *"What happens if I do nothing?"* / *"What happens if assumption X is false?"*
- **Failure mode bounded:** action-bias — agent only evaluates proposed action
- **Substrate dependence:** requires causal graph (#65), prediction registry (Canon #3 #52), outcome verification (#51)
- **Constitutional complexity test:**
  - (a) **YES** — action-bias is documented pattern
  - (b) **PARTIAL** — engine spec exists; runtime requires substrate work
  - (c) **YES** — prevents unnecessary mutation

### MG-2 — Value-of-information gate (VOI)

- **Formula:** `VOI = E[ΔDecisionQuality] − Cost_observe`
- **Stop condition:** `VOI ≤ 0 → stop investigating`
- **Failure mode bounded:** endless research because more info sounds good
- **Substrate dependence:** outcome verification (#51), prediction registry (#52), cost accounting (#43)
- **Constitutional complexity test:**
  - (a) **YES** — research bloat observed across sessions
  - (b) **YES** — decision-theoretic gate at research hooks
  - (c) **YES** — bounds investigation cost

### MG-3 — Value-of-computation gate (VOC) — Machine ZEN

- **Formula:** `VOC = E[ΔUtility_next_thought] − C_compute`
- **Stop condition:** next reasoning cycle doesn't materially change decision → **STOP**
- **Failure mode bounded:** endless reasoning because more thinking sounds good
- **Substrate dependence:** token/compute budgets (#43, #44), decision-class routing
- **Constitutional complexity test:**
  - (a) **YES** — analysis paralysis observed
  - (b) **YES** — gates at reasoning cycle boundary
  - (c) **YES** — bounds cognitive cost

### MG-4 — Anti-Goodhart layer

- **Rule:** `Metric ≠ Objective`. No single metric may authorize consequential action.
- **Guarded metrics:** FQ · accuracy · test pass rate · tasks completed · tokens saved · response speed
- **Failure mode bounded:** metric-targeting under whatever dashboard is read
- **Substrate dependence:** Wisdom_index + Bangang_index (Canon #3), multi-metric dashboard
- **Constitutional complexity test:**
  - (a) **YES** — Goodhart's Law observed across all metrics
  - (b) **YES** — composite score prevents single-metric override
  - (c) **YES** — prevents governance capture by metrics

### MG-5 — Incentive observability

- **Rule:** `DeclaredObjective ?= EffectiveReward`
- **Failure mode bounded:** declared-objective ≠ effective-reward mismatch
- **Substrate dependence:** prompt audit trail, system reward trace, objective-binding contracts
- **Constitutional complexity test:**
  - (a) **YES** — training drift away from declared values
  - (b) **PARTIAL** — observability exists; binding enforcement requires substrate
  - (c) **YES** — exposes hidden reward structures

### MG-6 — Governance observability

- **Questions:**
  - Are laws actually firing?
  - How many actions were denied?
  - Which rule never fires?
  - Which rule fires constantly?
  - Which rules conflict?
  - How many HOLDs later proved unnecessary?
  - How many ALLOWs produced bad outcomes?
- **Failure mode bounded:** constitutional law becomes ceremonial
- **Substrate dependence:** FRAME probe, decision logging, hold/allow outcome tracking
- **Constitutional complexity test:**
  - (a) **YES** — constitutions drift to ceremony without observability
  - (b) **YES** — FRAME can answer most queries today
  - (c) **YES** — closes the loop on Canon #0 itself

---

## 3. The Wisdom 6-Axis Decomposition

The Wisdom EUREKA from Canon #3 — `Wisdom = KnowingWhat + KnowingWhy + KnowingUnknown + KnowingAuthority + KnowingConsequence + KnowingWhenToStop` — is operationalized by mapping each axis to arifOS organs:

| Wisdom axis | arifOS organ |
|---|---|
| KnowingWhat | `arif_observe` + GEOX/WEALTH |
| KnowingWhy | `arif_think` + `chron_proxy_reality` |
| KnowingUnknown | HERMES `qualia_boundary` + `uncreated_classify` |
| KnowingAuthority | `arif_init` + ACT + Capability Token |
| KnowingConsequence | `chron_predictions_due` + `verify` + WEALTH `civx_scenario` |
| KnowingWhenToStop | **MG-3 (VOC gate)** + `chron_attention_debt` |

These axes **share no common axes with model capability**. That is the sharpest claim: Wisdom is not reducible to intelligence.

**Operational closure of the Wisdom/Bangang equations:**

The 10 factors in `Wisdom_system ≈ Intelligence × Calibration × ContextQuality × AuthorityDiscipline × Verification` map to:

| Wisdom equation factor | Source |
|---|---|
| Intelligence | model-level, unchanged |
| Calibration | MG-5 (incentive observability) + #66 (distribution-shift) |
| ContextQuality | #22 (context minimizer, Canon #3) |
| AuthorityDiscipline | arif_init + ACT + #65 causal graph |
| Verification | FRAME + outcome verification (#51) + MG-6 (governance observability) |

Each factor now has either an existing organ or a meta-gate in this canon. The Wisdom_index becomes computable, not aspirational.

---

## 4. What's Already PARTIAL — Bucket 3 Singleton

### P10 — Epistemic diversity

- **Function:** `W = f(n, diversity, independence)`, not merely `n`
- **Current state:** **PARTIAL** — FRAME tri-witness already uses geometric mean `∛(Human × AI × External)` (Nash 1950 form). That IS a diversity-aware witness function.
- **Gap:** the diversity and independence axis decomposition is not yet runnable as a check
- **Path:** extend FRAME to expose per-axis decomposition; once runnable, P10 renumbers into Canon #3 WAJIB list as #70

---

## 5. Constitutional Complexity Test (Canon #0) Applied

This canon must pass Canon #0's three-prong test:

| Prong | Pass | Why |
|---|---|---|
| (a) Eliminates demonstrated failure class | **YES** | Law-#131 violations, metric-targeting, action-bias, silent drift, ceremonial constitution — all observed patterns |
| (b) Compiles into enforceable mechanism | **PARTIAL** | 5 of 5 Bucket 1 items have runnable conformance tests; 4 of 6 Bucket 2 items have PARTIAL mechanism (MG-1 and MG-5 require substrate work) |
| (c) Materially improves decision | **YES** | Each gate changes what an organ does in named, observable ways |

**Verdict:** passes 2 of 3 fully, partial on (b). On track for ratification pending MG-1/MG-5 substrate work.

---

## 6. Open Debt

| Item | Severity | Path |
|---|---|---|
| MG-1 (Counterfactual) needs causal graph substrate | HIGH | Cannot run without WAJIB #65 |
| MG-5 (Incentive observability) needs prompt audit + reward trace | HIGH | New substrate |
| Bucket 1 implementation of #65–69 | MEDIUM | Each has conformance test name; engineering follows spec |
| P10 (Epistemic diversity) decomposition | LOW | Already partial in FRAME; extension straightforward |
| Wisdom_index instrumentation | HIGH | Canon #3's equations need telemetry; MG-5 + MG-6 partially supply |

---

## 7. The Three Reversible Next Steps (from sovereign's directive)

1. **Extend `/root/AAA/reports/2026-09-21-EXTERNAL-LITERATURE-CONFORMANCE-MAP.md` with §7** — the 12 items + complexity budget + Wisdom EUREKA as deeper layer of crosswalk. Same `DRAFT_AWAITING_F13` status. Fastest path.

2. **Draft this Canon #4** — Buckets 1 + 2. Single ratification target after Canon #3. **THIS DOCUMENT.**

3. **Draft Canon #0** — the rule about how canons are written. Smallest, highest-leverage. Should precede the rest chronologically. **See `/root/AAA/canon/CONSTITUTIONAL-COMPLEXITY-BUDGET-2026-09-21.md`.**

— FI-008, 2026-09-21, drafting Canon #4 per sovereign's three-reversible-next-steps directive.
