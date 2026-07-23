# Federation ABI v1.0 — Cross-Organ Envelope

> **Status:** DRAFT · **Authority:** 888_HOLD pending · **Owner:** arifOS protocol contract
> **DITEMPA BUKAN DIBERI**

## Purpose

Every cross-organ MCP call in the arifOS Federation MUST carry this envelope. It ensures identity continuity, epistemic provenance, and audit traceability across all organ boundaries.

## Schema

```yaml
federation_envelope:
  schema_version: "1.0"
  session_id: string          # arifOS session — required for every call
  actor_id: string            # authenticated actor identity
  trace_id: string            # unique trace across all hops
  source_organ: string        # which organ originated the call
  destination_organ: string   # which organ is receiving
  capability_id: string       # which capability is being invoked
  epistemic_tag: enum         # OBSERVED | COMPUTED | ESTIMATE | INFERRED
  evidence_refs: []           # list of prior receipt hashes
  authority_scope: string     # bounded authority for this call
  payload: object             # organ-specific data
```

## Consumers

| Organ | Role | Must accept | Must emit |
|-------|------|------------|-----------|
| **arifOS** | Governance kernel | Ingress from all organs | Session binding, routing headers |
| **A-FORGE** | Execution shell | SEAL verdicts from arifOS | Execution receipts, evidence_sha |
| **GEOX** | Earth intelligence | Routing from arifOS | Geological evidence with epistemic_tag |
| **WEALTH** | Capital intelligence | GEOX bridge payloads | Capital results with epistemic_tag |
| **WELL** | Vitality guard | Session validation requests | Readiness scores (REFLECT_ONLY) |
| **HERMES** | Multi-modal bridge | Telegram intake | Routed intents to arifOS |

## Acceptance Tests

### Test 1 — WEALTH authenticated invocation
```
1. arif_init() → session_id
2. wealth_registry_status(session_id=session_id)
3. Assert: response.session_id == session_id
4. Assert: response.actor_id is present
5. Assert: response.trace_id is present
6. Assert: response.epistemic_tag is not null
7. Assert: missing session_id → fail_closed
```

### Test 2 — GEOX → WEALTH governed bridge
```
1. GEOX produces geological evidence (epistemic_tag: OBSERVED)
2. GEOX calls WEALTH via actual MCP call_tool()
3. WEALTH computes capital interpretation (epistemic_tag: COMPUTED)
4. Both GEOX evidence and WEALTH result preserved
5. WEALTH never back-interprets geological observations
```

### Test 3 — End-to-end conformance trace
```
Telegram fixture
  → HERMES intake
  → arifOS session/routing
  → domain organ (GEOX or WEALTH or WELL)
  → arifOS judgment
  → A-FORGE dry execution
  → VAULT999 receipt
  → replay and hash verification
```

## Epistemic Tags

| Tag | Meaning | Example |
|-----|---------|---------|
| `OBSERVED` | Direct measurement | Well log reading, market price |
| `COMPUTED` | Deductive math | NPV, porosity from density |
| `ESTIMATE` | Model-based with uncertainty | Prospect volumetrics, Monte Carlo |
| `INFERRED` | Abductive reasoning | Basin interpretation, stress index |

## Forge Order

| # | Phase | Scope | Mutation |
|---|-------|-------|----------|
| **0** | Freeze ABI (this doc) | arifOS spec | None |
| **1** | Repair WEALTH ingress | WEALTH | Schema + contract |
| **2** | Replace GEOX adapter | GEOX | Bridge implementation |
| **3** | Unify registry generation | All organs | Tool generation |
| **4** | Repair WELL aliases | WELL | Alias resolution |
| **5** | End-to-end conformance test | arifOS | Test only |

## Change Control

```yaml
change_control:
  reversible: true
  blast_radius: high
  authority_required: 888_JUDGE
  execution_mode: branch_and_pull_request
  direct_default_branch_push: prohibited
  rollback: revert each organ-specific commit independently
```
