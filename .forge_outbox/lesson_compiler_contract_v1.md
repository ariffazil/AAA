# Lesson Compiler Contract v1 (P1.b)

> **Status:** STAGED-ARTIFACT, FOR EXECUTION. F13 directive "ok i approve, sah, jalan and go" received 2026-10-01.
> **Lineage:** BIJAKSANA Substrate Canon MISSING items #16 (Confidence/calibration), #53 (Calibration loop), #54 (Error taxonomy); Trilogy Gap §2.2 HIGH (HALAL-positive predicate); CHRON live evidence `lesson_health.lesson_actionable=0, blind_lesson_share=1.0`.
> **Purpose:** Closes the closed-loop bridge from `VerifiedPrediction` to `PolicyΔCandidate`. Without this, CHRON has 0 actionable lessons from 103,193 episodes.
> **Kernel anchor:** F1 · F2 · F7 · F8 · F13 · HUMA bridge Laws 1, 4, 5.

---

## The Pipeline (6 stages)

```
VerifiedPrediction
   ↓
[1] ErrorClass
   ↓
[2] LessonCandidate
   ↓
[3] Falsifier
   ↓
[4] ApplicableScope
   ↓
[5] PolicyΔCandidate
   ↓
[6] arifOS Judge → SEAL or VOID → Back to MIND or FORGET
```

Each stage produces a typed JSON object. Stages are append-only; nothing downstream deletes anything upstream. CoW receipt per transition.

---

## Stage 1 — ErrorClass

**Input:** VerifiedPrediction record (from `chron_predictions_due` → `chron_record_verification`)
**Output:**
```json
{
  "error_class_id": "ec-{hash8}",
  "source_prediction_id": "pred-...",
  "verdict": "VERIFIED_INCORRECT" | "VERIFIED_CORRECT" | "VERIFIED_MIXED" | "UNVERIFIABLE",
  "brier_score": 0.218,
  "calibration_delta": 0.012,
  "error_taxonomy": "OVERCONFIDENCE | UNDERCONFIDENCE | WRONG_DIRECTION | CALIBRATION_DRIFT | DOMAIN_CONSTRUCTION | UNKNOWN",
  "model_repeatable": true,
  "scope": {"organ": "CHRON", "tool": "chron_predictions_due", "domain": "macro"},
  "first_seen_at": "2026-10-01T...",
  "occurrences_window_24h": 1
}
```

**Rule:** every `VERIFIED_INCORRECT` prediction **must** produce exactly one `error_class`. `VERIFIED_CORRECT` produces only if brier_score > 0.05 OR calibration_delta is in the trailing 10th percentile.

**Why:** Closes WAJIB #54 (error taxonomy) and gives the lesson loop something named to act on.

---

## Stage 2 — LessonCandidate

**Input:** ErrorClass
**Output:**
```json
{
  "lesson_candidate_id": "lc-{hash8}",
  "source_error_class_id": "ec-...",
  "candidate_text": "When X tool returns Y class result, the Z parameter was miscalibrated by ±W in N/M cases over K days. Treat as a CALIBRATION_DRIFT, not a model defect.",
  "claim_class": "DER" | "MECHANISM" | "PATTERN",
  "witnessed_by": ["AI_ORGAN", "user"],
  "confidence": 0.6,
  "falsifier_promised": "next 2 predictions of the same kind will land within ±0.05 of stated confidence, OR a clean replay of the same input in sandbox fails-closed",
  "promoted_to_lesson": false
}
```

**Rule:** a `lesson_candidate` is *not yet* a `lesson`. It is a hypothesis the future may turn into evidence. F7 humility floor: confidence capped at 0.6 at this stage.

**Why:** HUMA bridge Law 4 — a consistency counter is not a truth oracle. A candidate is *consistent*, not *true*.

---

## Stage 3 — Falsifier

**Input:** LessonCandidate
**Output:**
```json
{
  "falsifier_id": "f-{hash8}",
  "source_lesson_candidate_id": "lc-...",
  "falsifier_text": "next 2 predictions of the same kind will land within ±0.05 of stated confidence, OR a clean replay of the same input in sandbox fails-closed",
  "falsifier_type": "PREDICTION_BASED" | "REPLAY_BASED" | "COUNTEREXAMPLE_BASED",
  "regime": "FAST (≤24h)" | "MEDIUM (≤7d)" | "SLOW (≤30d)",
  "scheduled_at": "2026-10-02T...",
  "verification_protocol": "chron_record_verification on a new prediction matching falsifier_source"
}
```

**Rule:** **every** LessonCandidate **must** carry a falsifier. No falsifier → LessonCandidate is rejected at the gate; not promoted to ApplicableScope.

**Why:** HUMA bridge Law 5 — a refutation stage is a governance organ. Constitutional Architecture Canon `∂Intelligence/∂t > 0 ↛ ∂Authority/∂t > 0` requires falsification discipline.

---

## Stage 4 — ApplicableScope

**Input:** LessonCandidate + Falsifier
**Output:**
```json
{
  "applicable_scope_id": "as-{hash8}",
  "source_lesson_candidate_id": "lc-...",
  "scope_type": "TOOL" | "ORGAN" | "FEDERATION",
  "scope_targets": ["forge_shell", "forge_git"],
  "excluded_targets": ["arif_seal"],
  "mutation_class_required": "REVERSIBLE",
  "blast_radius_bound": "session",
  "reversibility_proven": false
}
```

**Rule:** scope must name **specific tools, organs, or federation surfaces**, not categories. No exclusions except explicit by tool_id. Mutation class MUST be REVERSIBLE at this stage — policy changes are downstream of `belonging`.

**Why:** Constitutional Architecture Canon's HALAL-positive predicate `Authorized ∧ Scoped ∧ ReversibleWithinBand ∧ Provenanced ∧ TemporallyValid ∧ Budgeted ∧ PolicyCompliant`. Scoped is the first conjunct.

---

## Stage 5 — PolicyΔCandidate

**Input:** ApplicableScope (reversibility_proven=true)
**Output:**
```json
{
  "policy_delta_candidate_id": "pdc-{hash8}",
  "source_applicable_scope_id": "as-...",
  "policy_kind": "ROUTING_WEIGHT" | "MODEL_SELECTION" | "TASK_DECOMPOSITION" | "SKILL_SELECTION" | "BUDGET" | "CONFIDENCE_CALIBRATION" | "REVERSIBLE_HEURISTIC",
  "delta_vector": {
    "before": {"routing_weight_X_for_Y": 0.50},
    "after":  {"routing_weight_X_for_Y": 0.40}
  },
  "expected_outcome": "FORGE_SHELL class-of-failure rate should fall by ≥0.05 over next 20 invocations",
  "expected_observation_window_h": 48,
  "go_del_no_go": "GO",
  "constitutional_lock_breach": false,
  "godel_lock_checked": {
    "weaken_identity_verification": false,
    "weaken_lease_requirements": false,
    "weaken_witness_independence": false,
    "weaken_provenance": false,
    "weaken_arifos_floors": false,
    "weaken_human_sovereignty": false,
    "weaken_revocation": false,
    "weaken_capability_not_authority": false
  }
}
```

**Rule:** `policy_kind` ∈ {`ROUTING_WEIGHT`, `MODEL_SELECTION`, `TASK_DECOMPOSITION`, `SKILL_SELECTION`, `BUDGET`, `CONFIDENCE_CALIBRATION`, `REVERSIBLE_HEURISTIC`}. **No** kind is `IDENTITY_VERIFICATION_WEAKENING`, `LEASE_WEAKENING`, `WITNESS_WEAKENING`, `PROVENANCE_WEAKENING`, `ARIFOS_FLOOR_WEAKENING`, `HUMAN_SOVEREIGNTY_WEAKENING`, `REVOCATION_WEAKENING`, `CAPABILITY_AUTHORITY_WEAKENING` — these are explicitly listed in `godel_lock_checked` as `false`, and any proposal that flips one to `true` is rejected at the gate.

**Why:** the Gödel lock from the ChatGPT canon + Constitutional Architecture Canon's "the recursive-improvement mechanism cannot modify the invariants that authorize recursive improvement." Constitutionally enforced.

---

## Stage 6 — arifOS Judge → SEAL or VOID

**Input:** PolicyΔCandidate
**Output:** SEAL → moves to `forge_skillstore` as a new skill candidate + `arif_memory` L3 (Active Lessons). VOID → LessonCandidate is marked `falsified=true`, route returns to MIND or FORGET per Source-Type Promotion Gate.

**Rule:** arifOS Judge runs the route through the HALAL-positive 7-conjunct chain. If any conjunct fails → VOID. If all 7 pass → SEAL.

**Why:** Constitutional Architecture Canon. The judge is the only organ that can promote a LessonCandidate to a Lesson.

---

## What this artifact is NOT

- Not a kernel contract. The JSON shapes above are the *interface contract*, not the implementation. The implementation is `arifOS-L13` BUILD (P0 artefact chain).
- Not a new organ. Lesson compilation uses CHRON (episodes) + arifOS (judge) + arifFlow (FQ) + AAA (skillstore) — all existing surfaces.
- Not an authority grant. This contract is Stage 1 autonomous staging; the pipeline does not run until the Stage 2 contract authorship (behaviour-delta verifier) is live.

## Receipt chain for this artifact

- `forge_experience_trace trace_id=exp-1790838115433-1790836981647` (audit trace, sealed)
- `arifFlow receipt_id=47ecd31b-d370-4640-87a7-3f1fb2748e37` (audit FQ=0.9 FLOWING)
- This contract artifact: `/root/AAA/.forge_outbox/lesson_compiler_contract_v1.md`

DITEMPA BUKAN DIBERI ⚒️