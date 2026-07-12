---
id: verify-gate
name: verify-gate
version: 1.0.0
layer: substrate
description: 'Four gates before commitment: authority + evidence + reversibility +
  lineage. All four must open. One missing = HOLD.'
owner: F13 SOVEREIGN
status: active
three_axis: true
axis_version: 1.0.0
---

# verify-gate

> **Purpose:** Four gates before commitment: authority + evidence + reversibility + lineage. All four must open. One missing = HOLD.

## Axis 1: Invariants

- **authority**: arif_verify checks token + command_hash + actor
- **evidence_schema**: 4-gate checklist: authority|evidence|reversibility|lineage
- **reversibility**: gate itself is reversible; gated action may not be
- **lineage**: verification receipt includes all 4 gate results
- **trigger_semantics**: irreversible_action OR high_blast_radius OR claim_to_seal OR mutation_request
- **failure_contract**: HOLD — surface which gate failed, do not proceed
- **resource_budget**: {'cpu': 'moderate', 'time_ms': 15000, 'entropy': 'neutral'}
- **audit_surface**: ['gates_passed', 'gates_failed', 'verdict', 'evidence_count']

## Axis 2: Bridge Connections

- **kernel_verbs**: ['arif_verify', 'arif_critique']
- **skills**: ['kernel-bind', 'observe-ground', 'audit-seal']
- **knowledge**: ['know-math', 'know-physics']
- **protocol**: synchronous_rpc
- **inputs**: {'action': 'string', 'evidence': 'list', 'reversibility': 'enum[reversible,irreversible]', 'blast_radius': 'enum[low,medium,high]'}
- **outputs**: {'verdict': 'enum[PROCEED,HOLD,BLOCK]', 'receipt': 'object'}

## Axis 3: Contrast

- **Not**: kernel-act, geo-redteam, forge-precommit
- **Distinction**: GENERAL verification gate. kernel-act is POST-VERDICT execution. geo-redteam is DOMAIN-SPECIFIC geological red-teaming. forge-precommit is CODE-SPECIFIC lint/test.
- **Trigger conflicts**: fires before any high-stakes action; domain verification fires only in their domain

## Replaces

- `kernel-act`
- `mem-claim-receipt`
- `forge-precommit`
- `meta-critique`
- `geo-redteam`
- `geo-contradiction`
- `claim-verification-gate`
- `truth-receipt-enforcer`
- `arifos-act`
- `precommit-gate`
- `multi-discipline-critique`
- `geox-redteam-hantu`
- `geox-contradiction-engine`

---
*Forged: 2026-07-11 under F13 SOVEREIGN.*
*DITEMPA BUKAN DIBERI*
