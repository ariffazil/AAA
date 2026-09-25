# AAA EvidenceQuality × ActionRisk — Refactor Spec v0

> **Status:** SPEC_RATIFIED (text-level) on 2026-09-25 07:18 MYT. Awaiting F13 sovereign ratification to canon.
> **Closes:** Loop L12 from `/root/AAA/blueprints/HOOK-FEDERATION-STANDARD-DRAFT-v0.md` §7.
> **Source audit:** AAA EvidenceQuality formula `(1-Uncertainty) × Reversibility` + `irreversibility_floor: P ≥ 0.85` — same factor counted in two places.
> **Author:** FI-005 (Codex CLI, warga-aaa).

---

## 1. The detected double-count

Current AAA formula (paraphrased from `AAA_FEDERATION_ENFORCEMENT_MATRIX.md`):

```
EvidenceQuality = (1 - Uncertainty) × Reversibility
irreversibility_floor: P(action | proceed) ≥ 0.85
```

Here `Reversibility` enters EvidenceQuality **multiplicatively** AND again enters the
irreversibility floor as a probability threshold. Two flaws:

1. **One factor two jobs.** A low-reversibility decision *automatically* lowers
   EvidenceQuality even when uncertainty is independently small. That is a category
   confusion — knowing how reversible a thing is is not knowing how sure we are.
2. **Floor depends on uncertainty, but uncertainty is implicit.** `P(action | proceed) ≥ 0.85`
   names a probability threshold without naming whether it's `P(success)` or `P(safe)`. If
   they coincide, the floor double-counts again.

---

## 2. The refactor (binding after F13 ratify)

Split into **two independent quantities**, with one as an override gate.

### 2.1 EvidenceQuality

```
EvidenceQuality := (1 - Uncertainty)              ∈ [0, 1]
```

A pure epistemic measure. How sure are we, holding everything else fixed.
This is **what we know** about the world.

### 2.2 ActionRisk

```
ActionRisk := (Impact × Urgency × (1 - Uncertainty)) / AttentionCost
```

A composite of **consequence-side** + **epistemic-side** + **attention-budget**.
Multiplier form, normalised per action context:

- `Impact` ∈ [0, 1]: blast radius + irreversibility character.
- `Urgency` ∈ [0, 1]: pressure to act — time-critical signals set this above 0.
- `(1 - Uncertainty)`: same epistemic guard used in EvidenceQuality. **Single source.**
- `AttentionCost` ∈ [0, 1, ε]: human-attention units required.

### 2.3 Reversibility — an override gate, not a multiplier

```
ReversibilityClass := REVERSIBLE  |  CONSTRAINED  |  IRREVERSIBLE
```

**Not multiplied into the score.** Instead it gates the *admissibility* of the action:

| ReversibilityClass | Rule |
|---|---|
| REVERSIBLE       | proceed unless EvidenceQuality < 0.40 OR ActionRisk > 0.70 |
| CONSTRAINED      | proceed iff EvidenceQuality ≥ 0.60 AND ActionRisk ≤ 0.55 AND F13 SOVEREIGN or delegated envelope present |
| IRREVERSIBLE     | proceed iff EvidenceQuality ≥ 0.85 AND ActionRisk ≤ 0.30 AND F13 SOVEREIGN receipt + independent witness signature |

Numbers are heuristic phase-1 defaults (cite this surface as `calibration_required: true`).

### 2.4 Naming

- `ActionRisk` is **higher-is-riskier**. Distinguished from older "risk_class C0..C5" by being
  a continuous measure and admitting calibration to real outcomes (Phase 2).
- `ReversibilityClass` replaces "action_class T0..T4" for the *override* role, but T0..T4
  classes remain for hooking/audit metadata.

---

## 3. Migration map (smallest patch first)

1. Add `EvidenceQuality := (1 - Uncertainty)` to AAA canonical formulas as the **new** definition.
2. Deprecate `EvidenceQuality = (1-Uncertainty) × Reversibility` (keep in glossary as legacy_formula).
3. Add `ActionRisk := (Impact × Urgency × (1 - Uncertainty)) / AttentionCost`.
4. Add `ReversibilityClass` enum and the override-gate table above.
5. Update enforcement matrix C-class to route `CONSTRAINED` and `IRREVERSIBLE` through the same
   `arif_judge` flow, not through the old multiplicative path.
6. Mark `calibration_required: true` until outcome-coupled thresholds are measured (Phase 2).

---

## 4. Failure modes this avoids

- **Phantom caution:** multiplying by Reversibility made every low-reversibility action read as
  low-quality evidence. After the refactor, even irreversible bad-news can have high
  EvidenceQuality (we know it well) while being correctly gated at the override.
- **Floor double-count:** the 0.85 irreversibility floor has only one semantic now (EvidenceQuality ≥ 0.85).
- **Stealth weight drift:** without a separate AttentionCost denominator, urgent + uncertain situations
  produce artificially low ActionRisk. After the refactor, attention starvation is explicit.

---

## 5. Out of scope (next-spec, not this one)

- Coupling `ActionRisk` to realised outcomes (Phase 2 calibration: empirical `prediction_rate`).
- Per-organ `ActionRisk` baselines (separate spec, depends on outcome coherence L13 receipt instrumentation).
- Reversibility self-attestation vs independent-witness classification (L14+ work, future).

---

## 6. Ratification gate

This spec requires F13 SOVEREIGN vote before it becomes binding. Until then, treat the contents
as a working draft. The migration map in §3 is non-executable absent that vote.

DITEMPA BUKAN DIBERI ⚒️
