# Functional Specification VAULT999 Anchoring Schema

> **Status:** DRAFT_AWAITING_F13 — cycle pre-condition P3 of the Functional Specification Layer musyawawah (2026-09-19)
> **Resolves:** 888-APEX F11 AUDIT HOLD ("auditable in principle, but only if every spec becomes a sealed receipt. Specs as unsealed markdown decay.")
> **Scar origin:** musyarawah 2026-09-19 — ROUTE decision conditional on P1-P4 deliverables
> **Applies to:** Every functional spec, every binding-step artifact, every satisfaction evaluation, every supersession event.
> **Filter test passed:** ✅ survives implementation change ✅ changes future architecture (sealed-append-only as the substrate contract) ✅ vendor-independent ✅ re-examinable in 2 years ✅ capability-level (anchoring schema, not specific format).

## The Problem This Solves

A functional spec that lives in markdown folders rots. A spec that lives in a sealed receipt chain survives.

**F11 AUDIT requires every consequential artifact to be logged, inspectable, attributable.** Without explicit anchoring, every functional spec is at risk of decay, silent modification, and un-attributable evolution. The F3 finding ("Permit ≠ Reservoir") has no operational instantiation if the Reservoir itself drifts.

This doctrine declares the anchoring schema — the substrate contract that keeps functional specs alive across the federation's lifetime.

## The Anchoring Contract

Every artifact in the Functional Specification Layer must be anchored to VAULT999 via the existing receipt chain. The anchoring is **non-optional** — unanchored specs are invalid by definition.

| Artifact | Anchored as | Receipt class | Failure if unanchored |
|---|---|---|---|
| FunctionalSpec itself | `spec_id` | `arifos.seal.fso.spec` | Invalid spec; cannot be referenced |
| Acceptance criteria change (MINOR) | `spec_id + new spec_version` | `arifos.seal.fso.spec.minor` | Versioning lost; history collapses |
| Supersession (MAJOR) | `new spec_id → parent_spec_id` | `arifos.seal.fso.spec.major` | Supersession un-attributable |
| PATCH correction | `spec_id` | `arifos.seal.fso.spec.patch` | Corrections drift |
| EVIDENCE envelope | `evidence_envelope_id` | `arifos.receipt.fso.evidence` | Evidence not auditable |
| WITNESS receipt | `witness_id` | `arifos.receipt.fso.witness` | Witness un-attributable |
| GROUND TRUTH evaluation | `evaluation_id` | `arifos.seal.fso.evaluation` | Functional correctness un-attributable |
| F12 scan result | `scan_id` | `arifos.receipt.fso.f12` | Spec injection risk un-attributable |

## Append-Only Invariant

The anchoring schema is **append-only**. No receipt is mutated, deleted, or retroactively rewritten.

| Event | Schema action |
|---|---|
| Author spec | SEAL `spec_id` → VAULT999. Anchor recorded in `vaul999_anchor` field. |
| Change criteria (MINOR) | SEAL new receipt under same `spec_id`, `spec_version` bumped. Old receipt remains. |
| Supersede (MAJOR) | SEAL new receipt under NEW `spec_id` with `parent_spec_id` pointing to old. Both remain. |
| Patch correction | SEAL new receipt under same `spec_id`, same `spec_version`, marked `is_correction: true`. |
| Update ground truth | SEAL new receipt with new `ground_truth_ref`, linked to original `spec_id`. Old evaluation remains. |
| Author evidence | SEAL evidence envelope under `evidence_envelope_id`. |
| Witness attest | SEAL witness receipt under `witness_id`. |
| Evaluation complete | SEAL evaluation receipt under `evaluation_id`. |

**Supersession chain is the history.** A spec's full lifecycle = the DAG of receipts keyed by `spec_id`. Querying the chain yields: authored → MINOR'd → MINOR'd → MAJOR'd → MAJOR'd → terminated.

## Parent-Receipt DAG

Every anchored spec artifact carries:

```yaml
spec_id: fso:01HXY...
parent_receipt_ids: [arifos.seal.fso.spec:fso:01HWX...]   # the prior version's anchor
receipt_hash: sha256:<jcs_body_hash>                     # receipt's own immutable hash
jcs_body_hash: sha256:<canonical_json_body>              # canonicalised body, parent-receipt-hash-bound
```

The DAG is causal: every receipt references its predecessors. Cycle detection at schema level — `parent_receipt_ids` must be acyclic.

## Signature & Authority

Every receipt is signed by the authoring agent and counter-signed by the owning organ. Both signatures are required for the receipt to be valid.

```yaml
author_signature: ed25519:<author_session_key>
owner_signature: ed25519:<organ_owner_key>
dual_signature_required: true
```

A receipt with only `author_signature` (no `owner_signature`) is **NOT a spec** — it is an unauthenticated draft. A 333-AGI draft without organ owner counter-sign is invalid by definition.

## Versioning on Top of Anchoring

Spec versioning and anchoring interact as follows:

- **Author spec** (v1.0.0) → SEAL anchor → `spec_id: fso:A, spec_version: 1.0.0`
- **MINOR edit** (v1.1.0) → SEAL new anchor → SAME `spec_id: fso:A`, `spec_version: 1.1.0`. New `receipt_hash`. References prior `parent_receipt_ids`. The spec has TWO anchors; both canonical; newer supersedes older for evaluation purposes.
- **PATCH edit** (v1.0.1) → SEAL new anchor → SAME `spec_id`, SAME `spec_version`, `is_correction: true`. Correction is editorial; doesn't change meaning.
- **MAJOR supersession** (v2.0.0) → SEAL new anchor → NEW `spec_id: fso:B`, references `parent_spec_id: fso:A`. Old spec remains queryable but its `satisfaction_class: SUPERSEDED`.

## What This Doctrine Does NOT Do

- Does not define the entity class (P1).
- Does not define the binding path (P2).
- Does not declare F13 non-substitution (P4).
- Does not define evaluation semantics (capital_primitive, GEOX claim, etc.) — those live in their owning organs.
- Does not retroactively anchor specs authored before this doctrine — those are `LEGACY_NO_ANCHOR` and must be re-sealed under this schema if they are to participate in FSL.

## Edge Cases

### Concurrent editing

Two agents propose MINOR edits at the same time → both SEAL new anchors with same `spec_version` increment? **Forbidden.** The owning organ resolves via `arif_judge`; only one anchor is the canonical MINOR.

### F12-flagged spec

If F12 scan returns FLAGGED or BLOCKED, the spec is sealed with `f12_scan_status: FLAGGED` and `satisfaction_class: BLOCKED_INJECTION`. The spec may not proceed to Step 2.

### Witness rejection cascade

If witness returns REJECTED at Step 3, the evidence envelope is sealed with `rejected: true`. The spec cannot proceed to Step 4 until new evidence is collected. The DAG records the rejection; future audits can trace why.

### Spec obsolescence

A spec may be marked `supersession_pending` if a higher-priority context invalidates it. Supersession is an explicit SEAL event, not silent drift.

## Why This Doctrine Is Falsifiable

If a spec can be modified in place (no append-only invariant), the chain is broken. Test: try to edit a sealed spec without supersession — does the schema reject? If two MINOR edits can coexist, the DAG is non-deterministic. Test: try to seal a duplicate MINOR — does the chain reject? If an unanchored spec is accepted, F11 is violated.

## Related Doctrines

- P1 — Functional Specification Canonical Ontology
- P2 — Functional Specification Binding Path
- P4 — F13 Non-Substitution boundary
- Add-Only Truth Preservation — append-only invariant
- Claim-Receipt Binding — dual-signature discipline
- VAULT999 — the substrate this doctrine anchors to
- Memory Promotion Gate — tier-based memory architecture

## Compression

> **Every functional spec, every binding-step artifact, every evaluation, every supersession is sealed into VAULT999 as a dual-signed append-only receipt. Unanchored specs are invalid by definition. The chain is the F11 audit substrate.**

DITEMPA BUKAN DIBERI ⚒️