---
id: observe-ground
name: observe-ground
version: 1.0.0
layer: substrate
description: Evidence before narrative. All claims must be sourced, labeled OBS/DER/INT/SPEC,
  and confidence-capped. Reality wins over elegance.
owner: F13 SOVEREIGN
status: active
three_axis: true
axis_version: 1.0.0
---

# observe-ground

> **Purpose:** Evidence before narrative. All claims must be sourced, labeled OBS/DER/INT/SPEC, and confidence-capped. Reality wins over elegance.

## Axis 1: Invariants

- **authority**: arif_observe returns evidence with sources
- **evidence_schema**: OBSERVED / DERIVED / INTERPRETED / SPECULATIVE
- **reversibility**: True
- **lineage**: every evidence item carries source + timestamp + confidence
- **trigger_semantics**: claim_emitted OR evidence_requested OR reality_check_needed
- **failure_contract**: label UNKNOWN, do not fabricate
- **resource_budget**: {'cpu': 'moderate', 'time_ms': 30000, 'entropy': 'medium'}
- **audit_surface**: ['evidence_count', 'confidence_band', 'source_types', 'contradiction_flags']

## Axis 2: Bridge Connections

- **kernel_verbs**: ['arif_observe']
- **skills**: ['kernel-bind', 'verify-gate']
- **knowledge**: ['know-physics', 'know-math']
- **protocol**: synchronous_rpc
- **inputs**: {'claim': 'string', 'domain': 'string', 'depth': 'enum[quick,deep]'}
- **outputs**: {'evidence': 'list[{type,content,source,confidence}]', 'contradictions': 'list[string]'}

## Axis 3: Contrast

- **Not**: geo-evidence, research-search, meta-bias-detect
- **Distinction**: GENERAL evidence discipline. geo-evidence is DOMAIN-SPECIFIC earth data. research-search is the ACT of searching. meta-bias-detect is POPULATION-LEVEL statistical bias.
- **Trigger conflicts**: fires on ANY claim in ANY domain; domain skills fire only in their domain

## Replaces

- `geo-evidence`
- `geo-epistemic`
- `geo-claim`
- `geo-ground`
- `kernel-authority-detect`
- `meta-bias-detect`
- `geox-grounding`
- `geox-claim-grammar`
- `geox-earth-evidence`
- `geox-epistemic-ladder`

---
*Forged: 2026-07-11 under F13 SOVEREIGN.*
*DITEMPA BUKAN DIBERI*
