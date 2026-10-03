# Memory Schema

One-line summary:
Explorer memory stores contradiction-bearing state as structured graph objects, not transcript blobs.

## 1. Purpose

Use this schema whenever an explorer run must preserve:

- what was observed
- what was hypothesized
- what was falsified
- what survived
- what still contradicts
- who owns the next move

The goal is not "big memory". The goal is memory that can carry tension without flattening it.

## 2. Core Object Model

Minimum entities:

- `node`
- `edge`
- `claim`
- `test`
- `contradiction`
- `route`
- `receipt`

## 3. Node Schema

```yaml
node_id:
node_type: claim | evidence | hypothesis | test_result | contradiction | verdict
title:
domain:
subfield:
epistemic_rung: OBS | DER | INT | SPEC
domain_law:
summary:
confidence:
uncertainty_band:
blindspots: []
constraints: []
created_at:
updated_at:
owner_organ:
source_refs: []
```

Rules:

- `domain` is required
- `epistemic_rung` is required
- `uncertainty_band` must be explicit even if coarse
- `owner_organ` names who owns the next lawful interpretation

## 4. Claim Schema

```yaml
claim_id:
node_id:
claim_text:
evidence_for: []
evidence_against: []
missing_tests: []
status: proposed | surviving | falsified | held | sealed
contradiction_ids: []
lineage:
  parent_claims: []
  parent_tests: []
  parent_routes: []
next_owner:
```

Rules:

- no claim without both `evidence_for` and `evidence_against` fields
- `missing_tests` may be empty, but field must exist
- `status` changes only after explorer loop movement

## 5. Test Schema

```yaml
test_id:
hypothesis_id:
test_type: observe | simulate | compare | stress | governance
owner_organ:
prediction:
observed_outcome:
passed:
confidence_impact:
uncertainty_delta:
notes:
executed_at:
```

## 6. Contradiction Schema

```yaml
contradiction_id:
class: obs_vs_obs | model_vs_obs | model_vs_model | scale_vs_scale | domain_vs_domain | time_vs_time | memory_vs_action | meaning_vs_execution
left_ref:
right_ref:
description:
severity: low | medium | high | critical
is_real:
missing_data:
resolved_by:
status: open | compressed | held | sealed
```

## 7. Edge Schema

```yaml
edge_id:
from_id:
to_id:
edge_type: supports | contradicts | depends_on | routes_to | tests | governs | falsifies
weight:
stress:
entropy:
drift:
governance_route:
ac_risk:
```

Use edges to preserve cross-domain meaning, not just connectivity.

## 8. Memory Update Rules

When a run completes:

1. create or update observation nodes
2. create hypothesis claims
3. attach tests
4. surface contradiction nodes
5. route survivors to next owner
6. attach verdict node only after verification/judgment boundary

Never overwrite contradiction with summary prose. Preserve the contradiction object.

## 9. Minimal JSON Example

```json
{
  "claim_id": "claim-geox-001",
  "claim_text": "Prospect is geologically valid but capital-invalid under current risk regime.",
  "domain": "earth",
  "subfield": "prospect_evaluation",
  "epistemic_rung": "DER",
  "evidence_for": ["test-geox-014", "test-wealth-009"],
  "evidence_against": [],
  "missing_tests": ["test-well-003"],
  "status": "surviving",
  "contradiction_ids": ["cx-0021"],
  "next_owner": "well"
}
```

## 10. Law

Memory must preserve:

- structure
- lineage
- contradiction
- uncertainty
- ownership

If one is missing, the memory is too weak for governed exploration.
