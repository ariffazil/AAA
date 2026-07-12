# Route Contract

One-line summary:
The route contract defines when an explorer stays local, when it crosses organs, and when it must stop for constitutional judgment.

## 1. Purpose

Use this contract whenever:

- an explorer packet needs a `next_route`
- multiple organs could own the same contradiction
- a result is strong enough to affect execution or judgment

Routing is not preference. Routing is law-bound ownership transfer.

## 2. Canonical Organs

- `geox`
- `wealth`
- `well`
- `aaa`
- `arifos`
- `aforge`

## 3. Route Fields

```yaml
route_id:
from_organ:
to_organ:
reason:
trigger:
required_inputs: []
expected_outputs: []
authority_class: evidence | state | judgment | execution
risk_tier:
blocking_conditions: []
handoff_receipts: []
```

## 4. Default Routing Law

1. route to the organ whose law most directly governs the contradiction
2. do not escalate cross-domain if local falsification can still resolve it
3. route to `aaa` when identity, lease, agent state, or coordination ambiguity appears
4. route to `arifos` when authority, irreversible consequence, or verdict ambiguity appears
5. route to `aforge` only when the task is ready for build, test, execution, or tool evolution

## 5. Organ Ownership Rules

### GEOX

Owns routes where the central uncertainty is:

- physical reality
- seismic/well/stratigraphic evidence
- subsurface contradiction

### WEALTH

Owns routes where the central uncertainty is:

- economic viability
- risk asymmetry
- portfolio consequence

### WELL

Owns routes where the central uncertainty is:

- vitality
- fatigue
- substrate stability
- human/system readiness

### AAA

Owns routes where the central uncertainty is:

- identity
- lease
- capability graph
- multi-agent coordination

### arifOS

Owns routes where the central uncertainty is:

- judgment
- authority
- floor conflict
- irreversible consequence

### A-FORGE

Owns routes where the central uncertainty is:

- execution method
- tool mutation
- build/test/deploy path

## 6. Allowed Route Patterns

Common lawful patterns:

- `geox -> wealth`
- `geox -> well`
- `wealth -> well`
- `well -> aaa`
- `aaa -> arifos`
- `arifos -> aforge`

Possible but higher-burden patterns:

- `geox -> aaa`
- `wealth -> arifos`
- `well -> aforge`

Any skip over `arifos` is illegal when the route crosses into authority or irreversible execution.

## 7. Route Triggers

Use these trigger classes:

- `missing_domain_law`
- `surviving_contradiction`
- `failed_local_falsification`
- `identity_ambiguity`
- `authority_boundary`
- `execution_readiness`
- `human_vitality_risk`

## 8. Blocking Conditions

Typical blockers:

- missing required evidence
- stale state
- unresolved contradiction at lower layer
- no lease or identity continuity
- WELL red / degraded substrate
- arifOS `HOLD` or `VOID`

## 9. Minimal YAML Example

```yaml
route_id: route-014
from_organ: geox
to_organ: wealth
reason: "Physical prospect survives falsification but capital validity remains unresolved."
trigger: surviving_contradiction
required_inputs:
  - claim-geox-001
  - test-geox-014
expected_outputs:
  - capital_validity_assessment
  - risk_asymmetry
authority_class: evidence
risk_tier: T1
blocking_conditions:
  - missing_portfolio_context
handoff_receipts:
  - receipt-geox-88
```

## 10. Law

Every route must answer:

- why this organ
- why now
- why not stay local
- what must arrive with the handoff

If those answers are absent, the route is narrative, not contract.
