# Functional Specification Binding Path — Spec → Evidence → Witness → Ground Truth

> **Status:** DRAFT_AWAITING_F13 — cycle pre-condition P2 of the Functional Specification Layer musyawawah (2026-09-19)
> **Resolves:** 888-APEX F2 TRUTH HOLD ("no attestation path from spec → observed reality. P≥0.99 requires evidence-backed claims. Spec-drift failure mode.")
> **Scar origin:** musyarawah 2026-09-19 — ROUTE decision conditional on P1-P4 deliverables
> **Applies to:** Every functional evaluation. Every claim that "the agent satisfied the spec."
> **Filter test passed:** ✅ survives implementation change ✅ changes future architecture (every spec evaluation must follow this chain) ✅ vendor-independent ✅ re-examinable in 2 years ✅ capability-level (binding path, not specific protocol).

## The Problem This Solves

A functional spec that cannot be falsified against observed physics is not verification — it is ritual. (888-APEX critical caveat.)

Without an explicit binding path, a spec can drift from reality. The spec says "do X"; the agent does Y; the agent claims "I did X." No mechanism checks whether the claim is grounded.

**F2 TRUTH requires P ≥ 0.99.** Every claim of functional satisfaction must be evidence-backed. This doctrine declares the binding path that makes satisfaction claims falsifiable.

## The Four-Step Binding Chain

Every claim that an action satisfied a functional spec must traverse all four steps. Failure at any step means the action did NOT satisfy the spec — regardless of intermediate state.

```
Step 1          Step 2          Step 3          Step 4
─────────        ─────────       ─────────       ─────────
SPEC            EVIDENCE        WITNESS         GROUND TRUTH
(declared)      (collected)     (attested)      (verified)
```

### Step 1 — SPEC

The declared intent and acceptance criteria. Defined per P1 (Canonical Ontology). The spec is sealed before action begins.

**Inputs:** `spec_id`, `acceptance_criteria[]`, `ground_truth_ref`.
**Outputs:** Sealed VAULT999 receipt per P3.

### Step 2 — EVIDENCE

The action is taken; observable artifacts are collected. Evidence is **what the agent produced**, not what the agent claimed.

**Inputs:** `spec_id`, action output, intermediate states.
**Outputs:** Evidence envelope — collection of artifacts with timestamps and provenance.

**Discipline:**
- Evidence is observed, not narrated.
- Each artifact carries a timestamp + provenance handle.
- Missing evidence = `satisfaction_class: UNDETERMINED` (not PASS).
- Hallucinated evidence = `satisfaction_class: FAIL` + F2 violation.

### Step 3 — WITNESS

An independent witness attests that the evidence was real and complete. The witness is **not** the actor; the witness is **not** the spec author; the witness is the certifying organ.

**Inputs:** Evidence envelope from Step 2.
**Outputs:** Witness receipt — `witness_id`, `witness_channel`, attestation timestamp, attestation class (`CLEAN` / `PARTIAL` / `REJECTED`).

**Discipline:**
- Witness is independent (different agent, different session, different vantage).
- Witness checks: (a) evidence exists, (b) evidence is observed not narrated, (c) evidence is provenance-attached.
- Witness does NOT evaluate functional correctness — that is Step 4.
- Witness = procedural integrity. Ground Truth = functional correctness.

**Default witness channel:** `A-FORGE forge_evaluate`. Override: any organ with `can_witness: true` capability, recorded in `witness_channel`.

### Step 4 — GROUND TRUTH

The functional evaluation runs against the `ground_truth_ref` declared in Step 1. This is where the spec is falsified against observed physics.

**Inputs:** `spec_id`, evidence envelope, witness receipt, `ground_truth_ref`.
**Outputs:** `satisfaction_class` ∈ `{PASS, PARTIAL, FAIL, UNDETERMINED}`.

**Discipline:**
- Each acceptance criterion from Step 1 is evaluated independently.
- An action satisfies the spec only if EVERY criterion evaluates to PASS.
- PARTIAL = some criteria PASS, some FAIL. Document which.
- FAIL = any acceptance criterion evaluates to FAIL.
- UNDETERMINED = either evidence missing or witness rejected.

**The four-step chain is non-substitutable:**
- SPEC alone (without EVIDENCE): UNDETERMINED
- SPEC + EVIDENCE (without WITNESS): UNDETERMINED (evidence could be hallucinated)
- SPEC + EVIDENCE + WITNESS (without GROUND TRUTH): UNDETERMINED (procedural integrity ≠ functional correctness)
- All four: PASS / PARTIAL / FAIL / UNDETERMINED

## Causal Direction (Strictly Forward)

```text
SPEC        →   EVIDENCE      →   WITNESS       →   GROUND TRUTH
(declared)      (collected)       (attested)        (verified)
```

No backward step. The spec cannot be retroactively updated to match the evidence. The witness cannot be retroactively applied to retroactively confirm the ground truth. The ground truth cannot be retroactively adjusted to satisfy the spec.

If the spec was wrong → supersede with a new spec (add-only, parent_spec_id set).
If the evidence was wrong → re-run the action (new evidence envelope).
If the witness was wrong → re-witness (new witness receipt).
If the ground truth was wrong → update ground_truth_ref (new evaluation).

**Backwards mutation is FORBIDDEN.** Forward mutation is append-only.

## What This Path Does NOT Do

- Does not grant authority (P4).
- Does not evaluate constitutional correctness (F1-F13 are orthogonal — see Orthogonal Verification Surfaces).
- Does not create ground truth out of thin air — `ground_truth_ref` must exist before Step 1.
- Does not merge multiple specs into a single satisfaction class — each spec is evaluated independently.

## Mismatch Detection

| Mismatch | Detection | Action |
|---|---|---|
| Spec lacks acceptance criteria | Schema check at Step 1 | REJECT spec. Cannot seal without criteria. |
| Evidence missing artifact | Step 2 internal check | UNDETERMINED. Re-run action. |
| Witness detects hallucinated evidence | Step 3 | REJECT witness. Re-witness with new evidence. |
| Ground truth contradicts spec | Step 4 | FAIL satisfaction. Spec was wrong OR action was wrong. Spec is the SLOW changing axis; action is the FAST changing axis. Default: action is wrong. |
| Spec drift (intent changed mid-execution) | Add-only check | SEAL current spec, supersede with new spec, evaluate against new spec. |

## Why This Doctrine Is Falsifiable

If a satisfaction class of PASS can be issued without all four steps traversed, the chain is not enforced. Test: forge a SPEC with `does_not_grant_authority: true` set to false — does P4 catch it? If not, P4 fails. If P2 cannot detect a backward mutation in the spec, F2 fails. If witness can attest without independent vantage, F11 fails.

## Related Doctrines

- P1 — Functional Specification Canonical Ontology (defines the entity)
- P3 — VAULT999 anchoring schema (binds all four steps to VAULT999)
- P4 — F13 Non-Substitution boundary (FSL cannot grant authority)
- Add-Only Truth Preservation — backward mutation forbidden
- Claim-Receipt Binding — Step 2 + Step 3 produce a claim + a receipt
- Witness Zen Doctrine — Step 3 witness is independent vantage
- Orthogonal Verification Surfaces — Functional surface is independent of Constitutional surface

## Compression

> **SPEC → EVIDENCE → WITNESS → GROUND TRUTH. Forward only. Append-only. Each step non-substitutable. The chain is the F2 binding path that makes functional satisfaction falsifiable against observed physics.**

DITEMPA BUKAN DIBERI ⚒️