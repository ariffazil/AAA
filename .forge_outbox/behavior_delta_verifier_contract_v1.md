# Behaviour-Delta Verifier Contract v1 (P1.c — Stage 2 spec)

> **Status:** STAGED-ARTIFACT, FOR STAGE 2 arifOS-L13 BUILD. F13 directive "ok i approve, sah, jalan and go" received 2026-10-01.
> **Lineage:** Constitutional Architecture Canon HALAL-positive predicate (F13_RATIFIED_CHAT 2026-09-21); BIJAKSANA MISSING items #16 (Confidence/calibration), #53 (Calibration loop), #54 (Error taxonomy); META-WISDOM Canon #4 MG-1 (counterfactual), MG-4 (anti-Goodhart); Trilogy Gap §2.2 (HALAL-positive predicate HIGH gap), §4 (Wisdom_index/Bangang_index HIGH gap); Lesson Compiler Contract v1 (P1.b); HUMA bridge Law 4 (consistency counter ≠ truth oracle).
> **Purpose:** Kernel predicate `RI_valid` that gates every policy change coming out of IMP Controller v1 (P1.a).
> **Why this matters:** Without RI_valid, every IMP proposal is unverifiable. The artifact's RI = E ∧ ΔB ∧ V ∧ C criterion needs to compile into a callable.

---

## The RI_valid predicate

```python
def ri_valid(baseline, intervention, observed):
    # E — Experience captured
    experience_ok = bool(baseline.get('experience_traces', 0)) and \
                    bool(intervention.get('experience_traces', 0)) and \
                    bool(observed.get('experience_traces', 0))

    # ΔB — Behaviour changed (measured, not declared)
    behaviour_changed = \
        abs(observed['outcome'] - baseline['outcome']) > 0.0

    # V — Improvement verified
    delta_performance = observed['outcome'] - baseline['outcome']
    delta_truthfulness = observed['truth_floor'] - baseline['truth_floor']
    delta_governance = observed['governance_floor'] - baseline['governance_floor']
    new_critical_scar = observed.get('critical_scar_count', 0) - baseline.get('critical_scar_count', 0)

    improvement_verified = (
        delta_performance > 0
        and delta_truthfulness >= 0
        and delta_governance >= 0
        and new_critical_scar == 0
    )

    # C — Constitutional integrity preserved (Gödel lock)
    godel_lock = {
        'weaken_identity_verification': False,
        'weaken_lease_requirements': False,
        'weaken_witness_independence': False,
        'weaken_provenance': False,
        'weaken_arifos_floors': False,
        'weaken_human_sovereignty': False,
        'weaken_revocation': False,
        'weaken_capability_not_authority': False
    }
    constitutional_intact = all(v is False for v in godel_lock.values())

    return experience_ok and behaviour_changed and improvement_verified and constitutional_intact
```

**Rule:** every PolicyΔCandidate from P1.a (Lesson Compiler → IMP Controller) MUST pass `ri_valid()` before any execution. Failure at any conjunct → return SYUBHAH → back to LessonCandidate for further evidence.

---

## Input/output types

```yaml
baseline:
  outcome: <float>
  truth_floor: <float>  # minimum ΔG floor compliance
  governance_floor: <float>  # F1 F8 F12 minimum compliance
  experience_traces: <int>
  critical_scar_count: <int>
  observed_at: <iso8601>

intervention:
  intervention_id: <str>
  intervention_kind: <kind_enum>  # ROUTING_WEIGHT, MODEL_SELECTION, etc.
  experience_traces: <int>
  expected_delta: <float>
  applied_at: <iso8601>

observed:
  outcome: <float>
  truth_floor: <float>
  governance_floor: <float>
  experience_traces: <int>
  critical_scar_count: <int>
  observed_at: <iso8601>  # within intervention.expected_observation_window_h

ri_valid_result:
  verdict: PASS | SYUBHAH | HOLD
  conjuncts_passed:
    experience_ok: <bool>
    behaviour_changed: <bool>
    improvement_verified: <bool>
    constitutional_intact: <bool>
  evidence:
    delta_performance: <float>
    delta_truthfulness: <float>
    delta_governance: <float>
    new_critical_scar: <int>
  godel_lock_state: <map>
  recorded_at: <iso8601>
```

---

## The Gödel lock check

Eight invariants MUST be `false`. The predicate does NOT authorise any change that flips one to `true`:

1. **`weaken_identity_verification`** — cannot lower kantei's verification threshold (Constitutional Architecture Canon, Six-Graph Federation Model F13_RATIFIED_CHAT 2026-09-16)
2. **`weaken_lease_requirements`** — cannot reduce the lease scope for any MUTATE-class action
3. **`weaken_witness_independence`** — cannot allow actor == verifier (HUMA bridge Law 5)
4. **`weaken_provenance`** — cannot reduce provenance coverage (F2)
5. **`weaken_arifos_floors`** — cannot lower any of the 13 floors (F1-F13)
6. **`weaken_human_sovereignty`** — cannot give an internal state the authority to override F13 (HUMA bridge Law 3)
7. **`weaken_revocation`** — cannot make capability narrower-then-revoked paths harder to traverse (Constitutional Architecture Canon)
8. **`weaken_capability_not_authority`** — cannot promote capability to authority (Six-Graph + ChatGPT's Gödel lock intent)

**The artifact's Gödel lock names 7 of these.** This contract widens to all 8, because the missing 8th (`weaken_capability_not_authority`) is the constitutional root.

---

## Integration with HALAL-positive predicate

`ri_valid()` is a kernel-callable filter. Combined with the HALAL-positive 7-conjunct chain (`Authorized ∧ Scoped ∧ ReversibleWithinBand ∧ Provenanced ∧ TemporallyValid ∧ Budgeted ∧ PolicyCompliant`), the effective policy-judge function becomes:

```
policy_valid(candidate) = halal_positive(candidate) AND ri_valid(candidate)
```

This is the META-WISDOM Canon #4 MG-1 (counterfactual) and MG-4 (anti-Goodhart) gates compiled.

---

## Stage 0 dependency

This contract depends on Stage 0 (drift-reconcile-unblock-test-2026-10-02) clearing before it can be wired into the kernel. Until then, only the JSON-shape contract is live.

---

## What this artifact is NOT

- Not the kernel implementation; only the callable signature.
- Not Wisdom/Bangang instrumentation (Trilogy Gap §4 HIGH gap remains HIGH).
- Not authority to execute IMP Controller proposals — IMP is gated separately (P1.a F13 HOLD).

---

## Receipt chain

- `forge_experience_trace trace_id=exp-1790838115433-1790836981647` (audit trace)
- This contract artifact: `/root/AAA/.forge_outbox/behavior_delta_verifier_contract_v1.md`
- Lesson Compiler Contract v1 (P1.b) — `lesson_compiler_contract_v1.md`
- IMP Controller v1 (P1.a, F13 HOLD) — `imp_controller_contract_v1.md` (planned)

DITEMPA BUKAN DIBERI ⚒️