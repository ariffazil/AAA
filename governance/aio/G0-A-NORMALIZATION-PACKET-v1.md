# G0-A NORMALIZATION PACKET — First Evidence Pass

> Mode: READ-ONLY | Created: 2026-09-12T14:10:00+08:00
> Auditor: Hermes | Status: IN PROGRESS (not sealed)
> All values are CLAIMS TO VERIFY, not established facts, until source, commit, date, and implementation references are collected.

---

## 1. Source-of-Truth and Authority Ranking

### Repository Inventory

| Repository | Branch | HEAD | Dirty | Role |
|---|---|---|---|---|
| /root/arifOS | main | 480eb04ed6c0 | No | Kernel — constitution, floor definitions, enforcement code |
| /root/A-FORGE | main | 5a9cb7e974ec | Yes (2 files) | Execution — reality loop, trust scoring, tool registry |
| /root/AAA | main | e1e447fc8d35 | Yes (8 files) | Cockpit — instructions, governance docs, canon, reports |
| /root/GEOX | main | c456858aa958 | No | Earth intelligence organ |
| /root/WEALTH | main | 32f5ae69fb2c | Yes (1 file) | Capital intelligence organ |
| /root/WELL | main | 3dcda541f3af | No | Human readiness organ |
| /root/arifFlow | (not checked) | — | — | Flow metabolism plane — FQ computation |

### Authority Ranking

| Rank | Source | Path | Status |
|---|---|---|---|
| **A** | FLOOR_TABLE.json (machine-readable canonical) | /root/arifOS/GENESIS/FLOOR_TABLE.json | v1.0.0, forged 2026-07-23 |
| **A** | 000_KERNEL_CANON.md §3 (prose canonical) | /root/arifOS/GENESIS/000_KERNEL_CANON.md | Marked HISTORICAL; still declares itself SoT |
| **B** | constitution.md (AAA instructions) | /root/AAA/instructions/constitution.md | Points to FLOOR_TABLE.json as canonical |
| **B** | CONSTITUTION.md (AAA governance) | /root/AAA/constitution/CONSTITUTION.md | Simplified copy; contains DRIFT |
| **C** | apex_primitives.py (G computation) | /root/arifOS/arifosmcp/runtime/apex_primitives.py | Operational interpretation |
| **C** | fq.ts (FQ computation) | /root/arifFlow/src/ts/arifflow/state/fq.ts | Operational interpretation |
| **D** | fq_policy.yaml (FQ thresholds) | /root/arifOS/contracts/fq_policy.yaml | Runtime configuration |
| **E** | VAULT999 receipts | /root/arifOS/VAULT999/ | Historical evidence |
| **F** | AGENTS.md, dashboards, prose copies | Various | Informational until proven normative |

**Critical observation:** 000_KERNEL_CANON.md is marked HISTORICAL (deprecated tool names notice) but still declares itself as the Single Source of Truth for F1-F13. FLOOR_TABLE.json says consumers must sync to IT, not to 000. This authority ambiguity is itself a drift.

---

## 2. Semantic-Drift Matrix

### F7 HUMILITY — CRITICAL DRIFT

| Source | Confidence Cap Value | Additional Wording |
|---|---|---|
| FLOOR_TABLE.json (Rank A) | ∈ [0.95, 0.97] | "Ω₀ as UNCERTAINTY FLOOR — minimum residual doubt, NOT a confidence ceiling" |
| 000_KERNEL_CANON.md (Rank A, HISTORICAL) | ∈ [0.95, 0.97] | Same as FLOOR_TABLE |
| AAA/instructions/constitution.md (Rank B) | ∈ [0.95, 0.97] | Missing the "NOT a confidence ceiling" clarification |
| AAA/constitution/CONSTITUTION.md (Rank B) | **0.90** | Contradicts both Rank A sources |

**Drift type:** Numerical contradiction + missing semantic clarification
**Risk:** A downstream consumer using 0.90 as the confidence cap would be applying a WRONG threshold — either too permissive or too restrictive depending on the use.
**Status:** CRITICAL — requires correction under G0-B.

### F6 EMPATHY/MARUAH — MINOR DRIFT

| Source | Name | Rule |
|---|---|---|
| FLOOR_TABLE.json (Rank A) | EMPATHY | "Protect weakest stakeholder. Preserve dignity (maruah)." |
| 000_KERNEL_CANON.md (Rank A) | EMPATHY *(op: MARUAH)* | Same rule, different notation |
| AAA/instructions/constitution.md (Rank B) | EMPATHY ⇄ MARUAH | Adds "Dual-registry lossless bridge" — NOT in Rank A |

**Drift type:** Name notation + extra semantic claim in Rank B not present in Rank A
**Risk:** LOW for function, but the "Dual-registry lossless bridge" is an implementation detail that doesn't appear in the normative source. Consumer confusion possible.
**Status:** MINOR — clarify at G0-B.

### A-FORGE G Formula Comment — CRITICAL DRIFT

| Source | G Formula Claimed |
|---|---|
| FLOOR_TABLE.json (Rank A) | G = (A×P×E×X)^(1/4) ≥ 0.80 |
| apex_primitives.py (Rank C) | G = (A×P×E×X)^(1/4) — MATCHES constitution |
| A-FORGE types.ts comment (Rank C) | "G = A · P · E · X · Φ" — WRONG |
| A-FORGE engine.ts comment (Rank C) | "G = Q·V·Ψ·Φ" — DIFFERENT VARIABLES |

**Drift type:** Code comments contradict normative source and each other
**Risk:** MEDIUM — comments may mislead developers. The actual computation in apex_primitives.py IS correct, but the types.ts and engine.ts comments describe different formulas.
**Status:** CRITICAL — code comments must be corrected.

### min_g_score Threshold — CRITICAL DRIFT

| Source | Threshold |
|---|---|
| FLOOR_TABLE.json (Rank A) | G ≥ 0.80 |
| A-FORGE DEFAULT_HEURISTIC_GATES (Rank C) | min_g_score = 0.70 |
| fq_policy.yaml (Rank D) | References "qg.v0.3.1-vector" but does not specify G threshold |

**Drift type:** Implementation threshold (0.70) differs from constitutional threshold (0.80)
**Risk:** CRITICAL — the gate may release actions that the constitution intends to block.
**Status:** Requires clarification: which is authoritative?

### 000_KERNEL_CANON.md Authority Status — CONTRADICTION

| Source | Status of 000 |
|---|---|
| 000 itself | "CANON — SoT for F1-F13" |
| HISTORICAL_NOTICE.md | "Uses deprecated tool names" |
| FLOOR_TABLE.json | "consumers_must_sync_to: this file or 000_KERNEL_CANON.md" |

**Drift type:** Self-contradicting authority claim
**Risk:** MEDIUM — unclear which document is authoritative creates sync confusion
**Status:** Must be resolved at G0-B

---

## 3. Metric Cards

### METRIC.G — Governance Adequacy Signal

```yaml
metric_id: METRIC.G
display_name: Governance adequacy
status: HYPOTHESIS
version: apex-v1-phase2
construct: >
  Composite governance health indicator derived from four behavioral fractions:
  A (lease compliance), P (evidence compliance), E (success rate),
  X (reversibility rate via dry-run). Geometric mean ensures no factor
  dominates and zero in any factor collapses G.
operational_definition: >
  G = (A × P × E × X)^(1/4)
  where:
    A = in_lease / n (calls with valid lease)
    P = with_evidence / n (calls with evidence compliance)
    E = successes / n (successful tool calls)
    X = dry_runed / n (calls preceded by dry-run)
  Each factor floored at 0.01 to prevent collapse.
  None in any factor → G = None (UNMEASURED).
formula_source: /root/arifOS/arifosmcp/runtime/apex_primitives.py:171-185
input_fields:
  - in_lease: boolean per tool call
  - with_evidence: boolean per tool call
  - successes: boolean per tool call
  - dry_runed: boolean per tool call
input_provenance: Tool call records from A-FORGE execution traces
freshness_policy: UNKNOWN — computed over a rolling window (window_seconds parameter)
missingness_policy: None in any factor → G = None (UNMEASURED). Correctly handled.
aggregation_method: Geometric mean
correlation_assumptions: A, P, E, X may be correlated (e.g., lease-compliant calls may also be evidence-compliant). Correlation not measured.
uncertainty_expression: NONE — no confidence interval, no sensitivity analysis
calibration_dataset: NOT ESTABLISHED
validation_tests:
  - test_apex_g_standardization.test.ts (unit tests exist)
  - apexEmpirical.test.ts (empirical tests exist)
decision_rights: Used as gate threshold (min_g_score) for reality loop
thresholds:
  - value: 0.80
    authority: FLOOR_TABLE.json (Rank A)
    rationale: "Complex actions require G ≥ 0.80"
  - value: 0.70
    authority: A-FORGE DEFAULT_HEURISTIC_GATES
    rationale: UNKNOWN — appears to be an operational override
known_failure_modes:
  - false precision (no uncertainty expression)
  - shared-upstream correlation (A, P, E, X may share upstream sources)
  - stale input (freshness policy not defined)
  - threshold discrepancy (0.80 vs 0.70)
  - W3=None from this source (actual W3 displayed must come from elsewhere)
audit_result: PENDING
```

### METRIC.W3 — Tri-Witness Consensus

```yaml
metric_id: METRIC.W3
display_name: Tri-witness consensus
status: HYPOTHESIS
version: UNKNOWN
construct: >
  Witness agreement across three independent channels: Human, AI, and
  External/Earth. Nash geometric mean: W3 = ∛(H × AI × Ext).
  All three must be present; zero in any channel collapses W3.
operational_definition: >
  In apex_primitives.py: W3 = None (honest — comment says
  "needs live witness channels, tool-call metrics don't carry").
  The displayed W3=0.74 must come from a different computation
  path (likely rest_routes or dashboard layer).
  EXACT COMPUTATION PATH: NOT YET TRACED.
formula_source: UNKNOWN (not in apex_primitives.py where G is computed)
input_fields: UNKNOWN
input_provenance: UNKNOWN
freshness_policy: UNKNOWN
missingness_policy: UNKNOWN
aggregation_method: Geometric mean (if canonical Nash formula is used)
correlation_assumptions: UNKNOWN — independence of H, AI, Ext channels not verified
uncertainty_expression: NONE
calibration_dataset: NOT ESTABLISHED
validation_tests: NONE FOUND
decision_rights: Used as gate (F3 threshold ≥ 0.75)
thresholds:
  - value: 0.75
    authority: FLOOR_TABLE.json (Rank A)
    rationale: "Human × AI × Earth witness ≥ 0.75"
known_failure_modes:
  - witness channels may share model, prompt, infrastructure (correlated failure)
  - computation path not traced — displayed value origin uncertain
  - no independence verification
  - no calibration dataset
audit_result: PENDING — CRITICAL: computation path must be traced
```

### METRIC.FQ — Flow Quotient

```yaml
metric_id: METRIC.FQ
display_name: Flow quotient
status: PLAUSIBLE
version: qg.v0.2 (code) / qg.v0.3.1-vector (policy — discrepancy)
construct: >
  Real-time balance between verification and execution activity.
  High FQ = verify-dominated (fossilization risk). Low FQ =
  execute-dominated (burning risk). Balanced FQ = healthy metabolism.
operational_definition: >
  FQ = verify_count / execute_count (count-based, v2.1+)
  Verdicts:
    q > 3.0 → FOSSILIZED
    q >= 1.0 → OPTIMAL
    q >= 0.5 → FLOWING
    q >= 0.1 → STUCK
    q < 0.1 → BURNING
    verify_count == 0 → UNKNOWN
    Both 0 → UNMEASURED
formula_source: /root/arifFlow/src/ts/arifflow/state/fq.ts
input_fields:
  - execute_count: steps with execute_cost_ns > 0
  - verify_count: steps with verify_cost_ns > 0
input_provenance: arifFlow receipt store (in-memory + disk-persisted)
freshness_policy: Rolling window (default 100 steps)
missingness_policy: null quotient → UNKNOWN verdict
aggregation_method: Count ratio
correlation_assumptions: Assumes execute and verify steps are independent categories
uncertainty_expression: NONE
calibration_dataset: NOT ESTABLISHED
validation_tests: Unit tests exist in arifFlow Rust crate
decision_rights: Advisory + gating (per fq_policy.yaml enforcement)
thresholds:
  - healthy_min: 0.5 (fq_policy.yaml)
  - observe_only_below: 0.5 (fq_policy.yaml)
  - risk_class_floors: T0=0.1, T1=0.3, T2=0.5, T3=1.0
known_failure_modes:
  - window size sensitivity (100 steps default — may not be appropriate for all actors)
  - version discrepancy between policy (v0.3.1) and code (v0.2)
  - per-actor vs aggregate FQ may differ significantly
  - stale receipts could inflate counts
audit_result: PENDING
```

### CLASSIFIER.GOVERNANCE_COLLAPSE

```yaml
classifier_id: GOVERNANCE_COLLAPSE
status: UNKNOWN
construct: >
  Multi-dimensional vector diagnosis flagging pathological governance.
  Triggered by "g-dimension pathological" in fq_policy.yaml escalation rules.
operational_definition: >
  Trigger: vector diagnosis GOVERNANCE_COLLAPSE (g-dimension pathological)
  Action: report to arifOS :8088 for 888 review
  EXACT CLASSIFICATION LOGIC: NOT YET TRACED.
  Likely computed in arifFlow health endpoint or a separate diagnostic layer.
source: /root/arifOS/contracts/fq_policy.yaml:35
known_failure_modes:
  - classifier logic not in searched codebase — may be in arifFlow Rust code
  - "g-dimension" undefined in accessible documentation
  - may conflate FQ fossilization with governance health
audit_result: PENDING — CRITICAL: classifier logic must be located and documented
```

---

## 4. Constitution → Code → Test → Receipt Traceability

### F1 AMANAH (enforcement found)

| Layer | Location | Status |
|---|---|---|
| Prose | FLOOR_TABLE.json, constitution.md | DEFINED |
| Code | apex_primitives.py (reversibility_engine.py referenced) | ENFORCED |
| Tests | F1_provenance_tests: 4, T2_shell_classifier_tests: 8 | 12 PASSING |
| Receipt | evidence.f1_engine_receipt (required in judge) | ENCODED |

### F8 GENIUS (enforcement found)

| Layer | Location | Status |
|---|---|---|
| Prose | FLOOR_TABLE.json: G = (A×P×E×X)^(1/4) ≥ 0.80 | DEFINED |
| Code | apex_primitives.py: geometric mean computation | ENFORCED |
| Tests | test_apex_g_standardization.test.ts, apexEmpirical.test.ts | EXIST |
| Receipt | G score in apex primitives output | ENCODED |

### F3 TRI-WITNESS (partial enforcement)

| Layer | Location | Status |
|---|---|---|
| Prose | FLOOR_TABLE.json: Human + AI + Earth ≥ 0.75 | DEFINED |
| Code | apex_primitives.py: W3 = None (honest gap) | NOT ENFORCED from this path |
| Tests | NONE FOUND for W3 | MISSING |
| Receipt | W3 in output but value来源 UNTRACED | UNCERTAIN |

### F5 PEACE², F9 ANTIHANTU, F10 ONTOLOGY, F11 AUDITABILITY, F12 RESILIENCE, F13 SOVEREIGN

| Layer | Status |
|---|---|
| Prose | DEFINED in FLOOR_TABLE.json |
| Code | Enforcement NOT YET TRACED for most |
| Tests | NOT YET TRACED for most |
| Receipt | NOT YET TRACED for most |

**Summary:** Of 13 floors, only F1 and F8 have confirmed end-to-end enforcement chains (prose → code → tests → receipt). The remaining 11 floors have prose definitions but enforcement traces are incomplete or untraced.

---

## 5. Direct Predicate HOLD Vector

| HOLD Label | Direct Predicate | Evidence Source | Classification |
|---|---|---|---|
| `G < 0.80` | Is G computed from fresh inputs and bound to an executable gate? | apex_primitives.py (formula YES), threshold discrepancy (0.70 vs 0.80) | CONSERVATIVE_HEURISTIC (threshold may be wrong) |
| `W3 < 0.75` | Are witnesses independent under a defined model? | W3 computation path UNTRACED, independence UNVERIFIED | METRIC_ARTIFACT_RISK |
| WELL stale | Does the source heartbeat exceed declared freshness? | 8-day staleness claimed | DIRECTLY_SUPPORTED (if freshness verified) |
| GEOX parity | Is every tool classified under one scope? | 26/27/30 discrepancy | DIRECTLY_SUPPORTED (if count verified) |
| GOVERNANCE_COLLAPSE | Is there a direct violation of identity/authorization/rollback? | Classifier logic UNTRACED | STALE_OR_UNRESOLVED |
| FQ fossilization | Does FQ show repeated verify with no disposition? | FQ formula is clear (PLAUSIBLE) | PLAUSIBLE (needs runtime verification) |
| No human auth | Has F13 authorized any mutation? | No evidence of recent F13 authorization for current HOLD | DIRECTLY_SUPPORTED |

### HOLD Classification Summary

| Classification | Count | Items |
|---|---|---|
| DIRECTLY_SUPPORTED | 3 | WELL freshness, GEOX parity, F13 authorization |
| CONSERVATIVE_HEURISTIC | 1 | G threshold (may be wrong value) |
| METRIC_ARTIFACT_RISK | 1 | W3 (computation path untraced) |
| STALE_OR_UNRESOLVED | 1 | GOVERNANCE_COLLAPSE (classifier untraced) |
| PLAUSIBLE | 1 | FQ fossilization (formula clear, runtime needs check) |

---

## 6. AIO Lineage Audit (Preliminary)

### Inventory

| Category | Count | Source |
|---|---|---|
| Experience traces | UNKNOWN | No systematic search of VAULT999 receipt store completed |
| Sealed scars | Multiple | /root/AAA/scars/ directory exists |
| World-model gaps | UNKNOWN | forge_wm_gaps not queried |
| AIO pilot receipts | 1 | AIO-20260912-001 (just created) |

### Classification (based on available evidence)

Almost all existing scars and traces appear to be **DORMANT_MEMORY** — records of failures that exist but have no linked behavioral delta, runtime guard, or consequence test.

No evidence found of a complete chain:
`witness → learning delta → enforcement → consequence receipt → retained learning`

**Adaptation Yield ≈ 0** (pending full lineage audit)

**Status:** Consistent with fossilization hypothesis. The institution records failures but does not demonstrably learn from them in a way that changes future behavior.

---

## 7. Unknowns and Contradictions Register

| ID | Description | Severity | Status |
|---|---|---|---|
| U-001 | W3=0.74 computation path not traced | CRITICAL | OPEN |
| U-002 | GOVERNANCE_COLLAPSE classifier logic not found | CRITICAL | OPEN |
| U-003 | F7 confidence cap: 0.90 vs 0.95-0.97 contradiction | CRITICAL | OPEN |
| U-004 | min_g_score: 0.70 vs 0.80 discrepancy | CRITICAL | OPEN |
| U-005 | 000_KERNEL_CANON.md authority status ambiguous | MEDIUM | OPEN |
| U-006 | FQ policy version: v0.3.1 vs code v0.2 | MEDIUM | OPEN |
| U-007 | A-FORGE types.ts G formula comment wrong | MEDIUM | OPEN |
| U-008 | F6 name notation inconsistent across sources | LOW | OPEN |
| U-009 | AIO lineage audit incomplete | MEDIUM | OPEN |
| U-010 | F1-F13 enforcement coverage only traced for F1, F8 | HIGH | OPEN |

---

## 8. Ranked Remediation Plan

### READ-ONLY CLARIFICATIONS (no mutation needed)

| Priority | Item | Action |
|---|---|---|
| 1 | Trace W3=0.74 computation path | Search arifFlow rest_routes, dashboard, and any other computation layers |
| 2 | Locate GOVERNANCE_COLLAPSE classifier | Search arifFlow Rust code, health endpoint, and diagnostic layer |
| 3 | Complete F1-F13 enforcement trace | Systematically check each floor's code path |
| 4 | Verify F7 confidence cap source | Confirm 0.90 is wrong and 0.95-0.97 is canonical |
| 5 | Complete AIO lineage audit | Query VAULT999 receipts, scar ledger, experience traces |

### REVERSIBLE TECHNICAL REMEDIATION (requires 888 authorization, not F13)

| Priority | Item | Action |
|---|---|---|
| 1 | Fix F7 in AAA/constitution/CONSTITUTION.md | Change 0.90 → 0.95-0.97 (match Rank A) |
| 2 | Fix A-FORGE types.ts comment | Correct "G = A · P · E · X · Φ" → "G = (A×P×E×X)^(1/4)" |
| 3 | Fix A-FORGE engine.ts comment | Correct "G = Q·V·Ψ·Φ" → "G = (A×P×E×X)^(1/4)" |
| 4 | Align min_g_score threshold | Decide 0.70 or 0.80, make consistent |

### CHANGES REQUIRING F13 HUMAN APPROVAL

| Priority | Item | Action |
|---|---|---|
| 1 | G0-B normative freeze | Arif authorizes final constitution package |
| 2 | Resolve 000 authority ambiguity | Decide: retire 000 as historical or restore as normative |
| 3 | FQ policy version alignment | Ratify correct version (v0.2 or v0.3.1) |
| 4 | Threshold policy decision | Formalize which thresholds are hard gates vs advisory |

---

## 9. Audit Commit List (Reproducibility)

| Repository | Commit | Branch | Date |
|---|---|---|---|
| /root/arifOS | 480eb04ed6c0 | main | Latest at audit time |
| /root/A-FORGE | 5a9cb7e974ec | main | Latest at audit time |
| /root/AAA | e1e447fc8d35 | main | Latest at audit time |
| /root/GEOX | c456858aa958 | main | Latest at audit time |
| /root/WEALTH | 32f5ae69fb2c | main | Latest at audit time |
| /root/WELL | 3dcda541f3af | main | Latest at audit time |
| /root/arifFlow | NOT CHECKED | — | Must be added |

---

## 10. Verdict

**G0-A is IN PROGRESS.** This first pass has identified:

- **3 CRITICAL semantic drifts** (F7 cap value, min_g_score threshold, G formula comments)
- **1 CRITICAL metric gap** (W3 computation path untraced)
- **1 CRITICAL classifier gap** (GOVERNANCE_COLLAPSE logic untraced)
- **10 UNKNOWNs** requiring further investigation
- **3 directly supported HOLD predicates** (WELL freshness, GEOX parity, F13 authorization)
- **4 HOLD predicates with uncertain basis** (G threshold, W3, GOVERNANCE_COLLAPSE, FQ)

**The current HOLD is partially justified by direct predicates but partially rests on unvalidated metrics.** This is the expected finding — it confirms the hypothesis that uncalibrated metrics must not be promoted to law, while preserving the safety value of the HOLD itself.

**Next actions:**
1. Complete W3 computation path trace
2. Locate GOVERNANCE_COLLAPSE classifier
3. Complete F1-F13 enforcement matrix
4. Produce G0-A v2 with all unknowns resolved

---

DITEMPA BUKAN DIBERI — G0-A IN PROGRESS, NOT SEALED
