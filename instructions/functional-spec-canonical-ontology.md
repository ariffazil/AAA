# Functional Specification Canonical Ontology (FSO)

> **Status:** DRAFT_AWAITING_F13 — cycle pre-condition P1 of the Functional Specification Layer musyawawah (2026-09-19)
> **Resolves:** 888-APEX F10 ONTOLOGY VOID ("Functional Specification Layer has no canonical entity definition in federation ontology. Who owns it? How is it versioned? Ghost-entity risk.")
> **Scar origin:** musyarawah 2026-09-19 — ROUTE decision conditional on P1-P4 deliverables
> **Applies to:** Every functional spec authored, stored, bound, or consumed in the federation.
> **Filter test passed:** ✅ survives implementation change ✅ changes future architecture (defines canonical class for all FSL artifacts) ✅ vendor-independent ✅ re-examinable in 2 years ✅ capability-level (entity class, not specific format).

## The Problem This Solves

Before FSO, "functional spec" was a noun with no definition. Federation agents could not distinguish a functional spec from a claim, an artifact, a docket, a receipt, or an arbitrary text file. Every downstream system (Spec-Receipt Binding, F12 Spec-Injection Gate, Golden-Dataset Registry) was undefined to a class.

**F10 ONTOLOGY explicitly forbids ghost-entity references.** A layer that has no canonical entity is the canonical violation of F10.

This doctrine declares the entity class.

## The Entity Class

A `FunctionalSpec` is a sealed, append-only, versioned declaration of **intent + acceptance criteria + ground-truth binding** authored by a permitted authority and consumable by functional evaluators.

### Required Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `spec_id` | UUIDv7 | YES | Globally unique. Format: `fso:<ulid>`. |
| `spec_version` | SemVer | YES | MAJOR.MINOR.PATCH. Changes to intent/ground-truth → MAJOR. Acceptance criteria refinement → MINOR. Editorial → PATCH. |
| `intent` | string | YES | Plain-language declaration of what the action intends to accomplish. ≤ 256 chars. Must be human-readable. |
| `acceptance_criteria` | array<Predicate> | YES | Ordered list of measurable predicates. Each predicate is `(name, measurement, threshold, source)`. Empty list is FORBIDDEN — would render the spec UNMEASURABLE. |
| `ground_truth_ref` | URI | YES | Reference to the ground-truth artifact against which satisfaction is measured. Required for F2 binding (see P2). |
| `witness_channel` | string | YES | Which organ attests the satisfaction. Default: A-FORGE `forge_evaluate`. |
| `author` | actor_id | YES | Who wrote the spec. Must have `can_author_spec: true` capability. |
| `authoring_session_id` | UUID | YES | The session under which the spec was authored. Must be sealed. |
| `vaul999_anchor` | UUID | YES | The VAULT999 receipt_id under which the spec is sealed. See P3. |
| `parent_spec_id` | UUID | NO | If supersession, the spec_id this one replaces. None for origin. |
| `feder_domain` | enum | YES | `GEOX` / `WEALTH` / `WELL` / `AAA` / `A-FORGE` / `arifOS` / `CROSS`. Specifies owning organ. |
| `satisfaction_class` | enum | YES (after action) | `UNSPECIFIED` / `PASS` / `PARTIAL` / `FAIL` / `UNDETERMINED`. Default before action: `UNSPECIFIED`. |
| `does_not_grant_authority` | bool: true | YES (mandatory) | Fixed-true flag. FSL receipt cannot grant authority. See P4. |
| `f12_scan_status` | enum | YES | `CLEAN` / `FLAGGED` / `BLOCKED`. Result of pre-binding F12 scan. |
| `expiry` | timestamp | NO | Optional spec obsolescence date. Supersession is preferred over expiry. |
| `created_at` | ISO8601 | YES | UTC. |
| `created_by_session_id` | UUID | YES | Session that sealed this spec. |

### Forbidden Fields

| Field | Why forbidden |
|---|---|
| `authority_token` | FSL cannot grant authority. (P4) |
| `bypass_floor_check` | FSL cannot override F1-F13. |
| `execution_priority` | Priority flows through arifOS lane routing, not FSL. |
| `expected_pass` | Bias forbidden; the spec must be measurable AND falsifiable. |

## Ownership

| Domain | Owner organ | Authority ceiling |
|---|---|---|
| `GEOX` | GEOX | COMPUTE_ONLY |
| `WEALTH` | WEALTH | COMPUTE_ONLY |
| `WELL` | WELL | REFLECT_ONLY |
| `AAA` | AAA | DISPLAY_ONLY |
| `A-FORGE` | A-FORGE | EXECUTE_AFTER_SEAL |
| `arifOS` | arifOS | JUDGE_ONLY |
| `CROSS` | Joint — signature of all relevant organs | (multi-organ SEAL required) |

**No organ may author a spec outside its domain.** A WEALTH functional spec for "compute Kelly fraction" is allowed; a WEALTH functional spec for "evaluate geological horizon" is **NOT** — the GEOX domain owns that.

**CROSS specs require multi-organ seal** — a SPEC that spans multiple domains is sealed only when every relevant organ has signed.

## Versioning Rules

- **MAJOR change** (intent or ground-truth changes): New spec, parent_spec_id set. Old spec superseded.
- **MINOR change** (acceptance criteria refinement): Same spec, new spec_version (MINOR+1). parent_spec_id NOT set (add-only, no overwrite).
- **PATCH change** (editorial, typos): Same spec_version (no version bump), new VAULT999 receipt with `is_correction: true`.

Specs are append-only. Never edit. Supersede to change.

## Tiering

Functional specs follow the same L1-L6 tier system as `arif_memory`:

| Tier | Description | Example |
|---|---|---|
| L1 | Raw observation spec | "I observed this input" |
| L2 | Derived spec | "Spec derived from observation X" |
| L3 | Interpreted spec | "Spec for a domain-specific task" |
| L4 | Promoted spec | "Spec ratified by organ owner" |
| L5 | Canon-level spec | "Spec bound to constitutional doctrine" |
| L6 | Immutable spec | "Spec sealed into VAULT999, never re-opened" |

Default authoring tier: **L4** (organ owner must ratify). Promotion to L5-L6 requires explicit constitutional path.

## Authoring Rights

`can_author_spec: true` capability is granted by:

- A-FORGE organ owner for `A-FORGE` domain
- GEOX organ owner for `GEOX` domain
- WEALTH organ owner for `WEALTH` domain
- WELL organ owner for `WELL` domain
- AAA organ owner for `AAA` domain
- arifOS for `arifOS` and `CROSS` domains
- **arifOS authority envelope** (F13 SOVEREIGN) for any override

A 333-AGI agent cannot author a Functional Spec directly. They draft, the owning organ ratifies, the spec is sealed. **Separation of authoring from execution.** (F1 AMANAH: drafting never implies authority.)

## Three Anti-Patterns This Doctrine Forbids

1. **Self-referential specs**: A spec that measures itself. Forbidden. `ground_truth_ref` must point to an artifact outside the spec.
2. **Authority-bearing specs**: A spec that includes language like "this action is authorized." Forbidden. `does_not_grant_authority: true` is mandatory.
3. **Vague specs**: A spec with empty `acceptance_criteria`. Forbidden. Empty criteria renders the spec UNMEASURABLE.

## Why This Doctrine Is Falsifiable

If a spec can be authored without all required fields, FSO is not enforced — implement and check. If `does_not_grant_authority: false` can ever be set, P4 has been violated — flag. If an organ authors a spec outside its domain, ownership rules are broken — revoke.

## Related Doctrines

- P2 — Spec → Evidence → Witness → Ground Truth binding path (F2 TRUTH resolution)
- P3 — VAULT999 anchoring schema (F11 AUDIT resolution)
- P4 — F13 Non-Substitution boundary (F13 SOVEREIGN preservation)
- F10 ONTOLOGY — explicit grounding for the entity class
- Add-Only Truth Preservation — supersession is append-only, never overwrite
- Memory Promotion Gate — L1-L6 tiering inherited from there

## Compression

> **A Functional Spec is a sealed, append-only, versioned declaration of intent + acceptance criteria + ground-truth binding — owned by domain, authored under separation, marked `does_not_grant_authority: true`. F10 is the load-bearing floor.**

DITEMPA BUKAN DIBERI ⚒️