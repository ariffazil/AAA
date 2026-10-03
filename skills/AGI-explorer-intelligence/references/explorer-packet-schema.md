# Explorer Packet Schema

One-line summary:
The explorer packet is the canonical handoff object for one governed exploration cycle.

## 1. Purpose

Use this packet when handing results between:

- Hermes and domain organs
- OpenCode and OpenClaw
- explorers and AAA
- explorers and arifOS
- explorers and A-FORGE

It is the portable unit of governed exploration.

## 2. JSON Schema Shape

```json
{
  "packet_id": "string",
  "query": "string",
  "mode_sequence": ["observe", "hypothesize", "falsify", "verify"],
  "observations": [],
  "hypotheses": [],
  "tests": [],
  "contradictions": [],
  "survivors": [],
  "uncertainty_band": 0.0,
  "owning_organs": [],
  "next_route": null,
  "verdict_candidate": "SEAL | SABAR | HOLD | VOID | null",
  "memory_update": {},
  "receipts": [],
  "timestamps": {
    "started_at": "ISO-8601",
    "completed_at": "ISO-8601"
  }
}
```

## 3. YAML Form

```yaml
packet_id:
query:
mode_sequence:
  - observe
  - hypothesize
  - falsify
  - verify
observations: []
hypotheses: []
tests: []
contradictions: []
survivors: []
uncertainty_band:
owning_organs: []
next_route:
verdict_candidate:
memory_update: {}
receipts: []
timestamps:
  started_at:
  completed_at:
```

## 4. Field Definitions

### `observations`

List of raw or normalized observation objects.

Minimum observation object:

```yaml
observation_id:
source:
domain:
epistemic_rung: OBS
summary:
confidence:
freshness:
```

### `hypotheses`

List of ranked candidate explanations.

Minimum hypothesis object:

```yaml
hypothesis_id:
rank:
claim:
owning_domain:
falsifiers: []
confidence:
```

### `tests`

List of attempted falsification or verification actions.

```yaml
test_id:
hypothesis_id:
test_type:
owner_organ:
passed:
notes:
```

### `contradictions`

List of contradiction records surfaced during the loop.

```yaml
contradiction_id:
class:
description:
severity:
status:
```

### `survivors`

The surviving claims or hypotheses after falsification.

```yaml
survivor_id:
claim_ref:
reason_survived:
residual_uncertainty:
```

### `next_route`

Inline route object or route reference using the route contract.

### `memory_update`

Compact instruction telling memory what to persist.

```yaml
create_nodes: []
update_nodes: []
create_edges: []
attach_receipts: []
```

## 5. Validation Rules

1. `mode_sequence` must preserve order.
2. `observations` must not be empty unless the packet is a routing-only stub.
3. `hypotheses` must exist before `tests`.
4. `survivors` cannot exist without `tests`.
5. `verdict_candidate` cannot be `SEAL` if `uncertainty_band > 0.20`.
6. `next_route` is required when the owning organ changes.

## 6. Minimal JSON Example

```json
{
  "packet_id": "xp-20260706-001",
  "query": "Is this prospect ready for capital screening?",
  "mode_sequence": ["observe", "hypothesize", "falsify", "verify"],
  "observations": [
    {
      "observation_id": "obs-01",
      "source": "geox",
      "domain": "earth",
      "epistemic_rung": "OBS",
      "summary": "Structure closes and tie quality is acceptable.",
      "confidence": 0.82,
      "freshness": "fresh"
    }
  ],
  "hypotheses": [
    {
      "hypothesis_id": "hyp-01",
      "rank": 1,
      "claim": "Prospect is geologically valid.",
      "owning_domain": "earth",
      "falsifiers": ["seal_failure", "age_mismatch"],
      "confidence": 0.73
    }
  ],
  "tests": [
    {
      "test_id": "test-01",
      "hypothesis_id": "hyp-01",
      "test_type": "falsify",
      "owner_organ": "geox",
      "passed": true,
      "notes": "No fatal geological contradiction found."
    }
  ],
  "contradictions": [],
  "survivors": [
    {
      "survivor_id": "surv-01",
      "claim_ref": "hyp-01",
      "reason_survived": "Primary geological falsification gates passed.",
      "residual_uncertainty": 0.18
    }
  ],
  "uncertainty_band": 0.18,
  "owning_organs": ["geox", "wealth"],
  "next_route": {
    "to_organ": "wealth",
    "trigger": "surviving_contradiction"
  },
  "verdict_candidate": "SABAR",
  "memory_update": {
    "create_nodes": ["claim-geox-001"],
    "update_nodes": [],
    "create_edges": ["edge-route-001"],
    "attach_receipts": ["receipt-geox-88"]
  },
  "receipts": ["receipt-geox-88"],
  "timestamps": {
    "started_at": "2026-07-06T14:30:00Z",
    "completed_at": "2026-07-06T14:33:00Z"
  }
}
```

## 7. Law

Explorer packets must be:

- compact
- auditable
- routable
- memory-safe
- contradiction-preserving

If the packet reads like prose instead of state, it is too weak.
