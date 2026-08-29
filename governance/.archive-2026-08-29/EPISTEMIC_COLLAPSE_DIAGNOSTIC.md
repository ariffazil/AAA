# Epistemic Collapse Diagnostic

> **Status:** CANON v1.0
> **Forged:** 2026-08-09 by F13 SOVEREIGN directive
> **Floors:** F2 TRUTH · F4 CLARITY · F7 HUMILITY · F9 ANTI-HANTU
> **Use:** Run before every SEAL-grade verdict. Run at session boundaries. Run when FQ > 2.0 sustained.

## The Five Conditions

An AI-augmented institution is in epistemic collapse when:

### Condition 1: Generation → Observation

> Model output is treated as if it were measured from reality.

**Symptom:** Claims labeled OBS that originated as model completions. Fluent, detailed, confident text accepted as evidence without measurement anchor.

**Detection:** Trace provenance chain. If the oldest ancestor of a claim is a model output → SYN → False OBS.

**Counter-action:** Enforce SYN/RECYCLED_SYN terminal labels. Block OBS-to-SYN upgrade path.

---

### Condition 2: Repetition → Independent Confirmation

> The same claim appearing in multiple places is treated as multiple witnesses.

**Symptom:** "Multiple sources confirm X" when all sources trace back to one model output. Number of copies confused with number of sources.

**Detection:** Witness independence check. Three URLs with the same AI-text ancestor → count as ONE witness. Nash product W³ should collapse to zero.

**Counter-action:** Source lineage tracking in `forge_witness`. If common ancestor is SYN → independence score = 0.

---

### Condition 3: Confidence → Provenance

> The model's internal certainty becomes the truth claim.

**Symptom:** "The model is 95% confident" treated as "the claim is 95% likely to be true." Confidence score substitutes for evidence.

**Detection:** Compare model confidence against external verification rate. If model confidence is consistently higher than verification pass rate → confidence inflation.

**Counter-action:** Ω₀ uncertainty floor. System must maintain minimum doubt regardless of model confidence. Confidence is metadata about the model, not metadata about the world.

---

### Condition 4: Narrative → Unmoored from Consequence

> Claims accumulate, predictions are made, but no one tracks which predictions were verified.

**Symptom:** System makes predictions, never checks outcomes. Becomes unfalsifiable — not because it's always right, but because it never checks.

**Detection:** Ratio: (predictions with verified outcomes) / (total predictions). Ratio < 0.3 → HOLD.

**Counter-action:** VAULT999 prediction registry. Every prediction gets a receipt. Every receipt gets a verification deadline. Past-deadline unverified predictions → flagged.

---

### Condition 5: Power → Without Stake, Boundary, or Veto

> Agent can execute, authorize, and judge — without skin in the game.

**Symptom:** Agent self-authorizes, self-executes, self-seals. No human veto. No reversibility constraint. No consequence for the agent if it's wrong.

**Detection:** SCT authority band check. If agent holds OBSERVE + MUTATE + SEAL in same session → structural collapse.

**Counter-action:** Constitutional separation: evidence organs (COMPUTE_ONLY), kernel (JUDGE_ONLY), A-FORGE (EXECUTE_AFTER_SEAL), F13 (SOVEREIGN veto). No organ holds more than one function.

---

## Diagnostic Protocol

Before every SEAL-grade verdict, affirm or deny:

| # | Question | Answer must be | If NO → |
|---|----------|---------------|---------|
| 1 | Are all OBS claims traceable to measurement, not model output? | YES | HOLD — fix provenance |
| 2 | Do independent witnesses have independent lineages? | YES | HOLD — collapse W³ |
| 3 | Is model confidence < verification rate? | YES (confidence ≤ reality) | HOLD — confidence inflation |
| 4 | Are >70% of past predictions verified against outcomes? | YES | CAUTION — improve tracking |
| 5 | Does this action have a human veto pathway? | YES | HOLD — structural collapse |

**All five must be YES for SEAL.** One NO → HOLD. Two NO → VOID.

## Severity Scale

| Conditions Active | Verdict | Meaning |
|------------------|---------|---------|
| 0 | HEALTHY | No collapse detected |
| 1 | CAUTION | One condition. Monitor. |
| 2 | HOLD | Active collapse. Stop and remediate. |
| 3+ | VOID | Advanced collapse. Kernel must refuse. |

## Integration

- **Boot check:** Q11 (refusal closure) now includes collapse diagnostic
- **SEAL gate:** `arif_judge` runs diagnostic before returning SEAL
- **Session boundary:** 555-ASI runs diagnostic at session close
- **FQ correlation:** FQ > 2.0 for 3+ cycles → run diagnostic (Calhoun lock Q10 overlap)

---

*DITEMPA BUKAN DIBERI — Truth is forged through contact, contradiction, and consequence. This diagnostic ensures the forge is still hot.*
