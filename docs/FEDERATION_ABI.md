# Federation ABI v1.0 — Cross-Organ Envelope

> **Status:** HARDENED DRAFT · **Authority:** 888_HOLD pending ratification
> **Owner:** arifOS (canonical schema); AAA (display mirror, hash-pinned)
> **Schema root:** `aaa/schemas/federation/`
> **DITEMPA BUKAN DIBERI**

## 1. Purpose

The Federation ABI defines a transport-neutral contract for cross-organ invocation. Every organ-to-organ call carries this envelope. The contract is independent of MCP, REST, A2A, or any future transport — each transport profile implements the same semantic contract.

```
Federation capability invocation
    ├── MCP implementation (streamable-http, current)
    ├── REST implementation
    ├── A2A implementation
    └── future transport
```

## 2. Schema Inventory

| Schema | File | Purpose |
|--------|------|---------|
| Request | `schemas/federation/federation-request.v1.schema.json` | Cross-organ invocation |
| Response | `schemas/federation/federation-response.v1.schema.json` | Organ response |
| Error | `schemas/federation/federation-error.v1.schema.json` | Fail-closed error |
| Receipt | `schemas/federation/federation-receipt.v1.schema.json` | VAULT999 recording |

## 3. Key Design Decisions

### 3.1 Transport Neutrality
The ABI defines semantic fields (`source_organ`, `capability_id`, `action_class`), not transport headers. Each transport profile maps these fields to its native mechanism:
- **MCP**: `Mcp-Session-Id` header for session; JSON-RPC params for envelope fields
- **A2A**: Agent card metadata for organ identity; task context for trace
- **Direct**: HTTP headers for session; JSON body for envelope

### 3.2 Trace Continuity
Every invocation carries three identifiers:
- `trace_id`: constant across all hops in a workflow
- `invocation_id`: unique per hop
- `parent_invocation_id`: links to prior hop (null for origin)

Plus `hop_index` for ordinal position and `issued_at`/`deadline_at` for timing.

### 3.3 Integrity Verification
`payload_hash`, `schema_hash`, `source_manifest_hash`, and `evidence_hashes` enable cryptographic verification that the payload, schema, and evidence chain are unaltered across transport boundaries.

### 3.4 Authority Classification
`action_class` (OBSERVE | COMPUTE | JUDGE | EXECUTE) combined with `mutation`, `reversible`, and `authority_band` enable destination organs to fail closed when required authority fields (`judge_receipt_ref`, `human_ack_ref`) are absent.

### 3.5 Idempotency
`idempotency_key` + `attempt` + `max_attempts` prevent duplicate execution. Same key = same effect. Destination organ must detect and reject attempts beyond `max_attempts`.

## 4. Consumers

| Organ | Accepts | Emits | Action Class |
|-------|---------|-------|-------------|
| **arifOS** | Ingress from all organs | Session binding, routing, verdicts | JUDGE |
| **A-FORGE** | SEAL verdicts, leases | Execution receipts, evidence_sha | EXECUTE |
| **GEOX** | Routing from arifOS | Geological evidence | OBSERVE |
| **WEALTH** | Routing from arifOS, GEOX bridge | Capital computation | COMPUTE |
| **WELL** | Session validation requests | Readiness scores | OBSERVE |
| **HERMES** | Telegram intake | Routed intents | OBSERVE |
| **VAULT999** | Sealed consequence + evidence | Immutable receipt, chain ref, replay | — |
| **AAA** | Display-only mirror | Hash-pinned schema copies | — |

## 5. Error Classes

| Code | Meaning | Retry |
|------|---------|-------|
| `SESSION_MISSING` | No session provided | No |
| `SESSION_INVALID` | Session expired or unknown | No |
| `AUTHORITY_INSUFFICIENT` | `authority_band` too low for `action_class` | No |
| `JUDGE_RECEIPT_MISSING` | `action_class=EXECUTE` without `judge_receipt_ref` | No |
| `HUMAN_ACK_REQUIRED` | IRREVERSIBLE without `human_ack_ref` | No |
| `SCHEMA_INCOMPATIBLE` | Schema version mismatch | No |
| `ORGAN_UNREACHABLE` | Destination organ not responding | Yes |
| `DEADLINE_EXCEEDED` | `deadline_at` passed | No |
| `PAYLOAD_INTEGRITY_FAILED` | `payload_hash` mismatch | No |

## 6. Compatibility Rules

| Change | Version | Rule |
|--------|---------|------|
| Add optional field | Patch | Accept unknown, ignore |
| Add required field | Minor | New field defaults to null for old callers |
| Remove field | Major | Reject unknown fields in strict mode |
| Change field type | Major | Reject, return SCHEMA_INCOMPATIBLE |
| Deprecation | Minor | 90-day window, warn on use |
| Minimum supported version | — | N-1 (current and previous minor) |

## 7. Acceptance Tests

### T1 — Valid request passes schema validation
```
$ python3 -c "import json; from jsonschema import validate; ..."
→ PASS: valid-request.json validates against federation-request.v1.schema.json
```

### T2 — Missing session fails closed
```
→ FAIL: missing-session-invalid.json rejected — SESSION_MISSING
```

### T3 — WEALTH authenticated invocation
```
1. arif_init() → session_id
2. WEALTH tool with federation envelope → OK
3. Response carries: session_id, actor_id, trace_id, epistemic_tag
4. Missing session → SESSION_MISSING error
```

### T4 — End-to-end conformance
```
Telegram fixture → HERMES → arifOS → organ → judge → A-FORGE → VAULT999
→ replay verified: trace continuity, hash integrity, hop_index sequential
```

## 8. Fixtures

| File | Purpose |
|------|---------|
| `fixtures/federation/valid-request.json` | Nominal cross-organ request |
| `fixtures/federation/missing-session-invalid.json` | Session absent — must fail |

## 9. Change Control

```yaml
owner: arifOS (canonical schema)
mirror: AAA (hash-pinned display copy)
branch: forge/abi-v1-hardening
status: HARDENED DRAFT
authority_required: 888_JUDGE ratification
execution_mode: pull_request_review
direct_default_branch_push: not yet ratified
rollback: revert branch
```

## 10. Forge Order

| # | Phase | Status |
|---|-------|--------|
| **0A** | Harden ABI (this branch) | 🔨 IN PROGRESS |
| **0B** | Ratify + pin schema hash | HOLD |
| **1** | Repair WEALTH ingress | HOLD |
| **2** | Replace GEOX adapter | HOLD |
| **3** | Unify registry generation | HOLD |
| **4** | Repair WELL aliases | HOLD |
| **5** | End-to-end conformance test | HOLD |
