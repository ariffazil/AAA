# Federation ABI v1.0 — Cross-Organ Envelope

> **Status:** HARDENED DRAFT · **Authority:** 888_HOLD (not ratified)  
> **Owner:** arifOS (`contracts/schemas/`) — canonical  
> **AAA role:** byte-identical mirror at `schemas/federation/` + `SHA256SUMS`  
> **session_id:** `SEAL-<16hex>` (live kernel) · **session_token:** `sct_v1.*` (optional)  
> **payload_hash:** FCJ-v1 (see `schemas/federation/CANONICAL_JSON.md`) — not full RFC 8785  
> **DITEMPA BUKAN DIBERI**

## 1. Purpose

The Federation ABI defines a transport-neutral contract for cross-organ invocation. Every organ-to-organ call carries this envelope. The contract is independent of MCP, REST, A2A, or any future transport — each transport profile implements the same semantic contract.

**This document does not claim F13 ratification, VAULT999 seal, or live end-to-end conformance.**

## 2. Schema Inventory

| Schema | Canonical (arifOS) | AAA mirror |
|--------|--------------------|------------|
| Request | `contracts/schemas/federation-request.v1.schema.json` | `schemas/federation/federation-request.v1.schema.json` |
| Response | `contracts/schemas/federation-response.v1.schema.json` | `schemas/federation/federation-response.v1.schema.json` |
| Error | `contracts/schemas/federation-error.v1.schema.json` | `schemas/federation/federation-error.v1.schema.json` |
| Receipt | `contracts/schemas/federation-receipt.v1.schema.json` | `schemas/federation/federation-receipt.v1.schema.json` |

Mirrors MUST be byte-identical. Verify: `sha256sum --check schemas/federation/SHA256SUMS`.

There is **no second schema tree** under `docs/schemas/` for federation request/response.

## 3. Session fields

| Field | Format | Meaning |
|-------|--------|---------|
| `session_id` | `SEAL-[a-f0-9]{16}` | Live arifOS session identifier |
| `session_token` | `sct_v1.*` (optional) | Session Capability Token — **not** interchangeable with `session_id` |

## 4. Authority conditionals

- `action_class=EXECUTE` → requires `authority.judge_receipt_ref`
- `mutation=true` AND `reversible=false` → requires `authority.human_ack_ref`

## 5. Semantic honesty (validator)

| Check | What it actually does |
|-------|------------------------|
| `session_identifier_present` | Non-empty `session_id` only — **not** liveness |
| `check_deadline` | `deadline_at` not in the past |
| `check_payload_hash` | FCJ-v1 hash match |
| `check_retry_bound` | `attempt <= max_attempts` — **not** idempotency |
| `check_idempotency_stateful` | Store lookup: unseen / same-hash replay / different-hash conflict |

Live session attestation (existence, expiry, actor binding, SCT verify, revocation) is **out of scope** for this structural ABI pack and remains a kernel concern.

## 6. Fixtures

Under `fixtures/federation/`:

| File | Expectation |
|------|-------------|
| `valid-request.json` | PASS — `SEAL-bee1b3fd3ebd4ae4` |
| `valid-response.json` | PASS |
| `missing-session-invalid.json` | FAIL |
| `sess-format-invalid.json` | FAIL — rejects `sess-xyz` |
| `expired-deadline-invalid.json` | FAIL |
| `execute-without-judge-invalid.json` | FAIL |
| `irreversible-without-ack-invalid.json` | FAIL |
| `retry-bound-invalid.json` | FAIL |
| `idempotency-conflict-invalid.json` | FAIL against seeded store |

## 7. Change Control

```yaml
owner: arifOS (canonical schema)
mirror: AAA (byte-identical, hash-pinned)
branch_arifos: fix/abi-hardening-0a
branch_aaa: forge/abi-v1-hardening
status: HARDENED DRAFT
authority_required: 888_JUDGE + F13 for ratification
direct_default_branch_push: forbidden until ratified
```

## 8. Forge Order

| # | Phase | Status |
|---|-------|--------|
| **0A.2** | Unify schema root, live session format, honest semantics | 🔨 DRAFT PR |
| **0B** | Ratify + pin + independent review | HOLD |
| **1** | WEALTH ingress | HOLD |
| **2** | GEOX bridge | HOLD |
| **3–4** | Empty / not implemented | HOLD |

## 9. Explicit non-claims

- Not merged
- Not sealed in VAULT999
- Not system-done
- Dedicated ABI CI green ≠ repository-wide gate green
- Connector/runtime drift (judge modes, 502s) is separate from schema drafting
