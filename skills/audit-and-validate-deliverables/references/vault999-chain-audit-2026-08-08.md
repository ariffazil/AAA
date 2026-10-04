# VAULT999 Chain Integrity — Audit Reference (2026-08-08)

## Context

Session SEAL-e7cde4b28b7b4cb2 + Hermes audit pass. 9-ATLAS upgrade + chaos reduction + full system audit.

## Canonical Verifier

- **Script:** `/root/arifOS/scripts/verify_vault_chain.py` (20,928 bytes)
- **Usage:** `python3 scripts/verify_vault_chain.py --input VAULT999/outcomes.jsonl` (or default: VAULT999/vault999.jsonl)
- **Makefile target:** `vault999-verify` — **WAS miswired to `vault999_status.py` (a reporter), not `verify_vault_chain.py` (the canonical checker)**
- **Fix:** one-line Makefile change (line 182 in `/root/arifOS/Makefile`)

## Live Verification Results (2026-08-08 ~05:23Z)

| Ledger | Status | Chain Length | Strict Breaks | Legacy Flat | Notes |
|---|---|---|---|---|---|
| `SEALED_EVENTS.jsonl` (v1) | **BROKEN** | 1333 | 958 | 0 | Frozen historical |
| `SEALED_EVENTS_v2.jsonl` (v2) | **BROKEN** | 1754 | 1731 | 0 | Active canonical |
| `vault999.jsonl` (v3 live) | INTACT | 5 | 1 | 5 | Mixed nested/flat |
| **Overall** | **DEGRADED** | — | — | — | — |

## outcomes.jsonl (42K entries) — NOT in canonical verifier

The canonical verifier's `CHAIN_LEDGERS` array only includes `SEALED_EVENTS.jsonl`, `SEALED_EVENTS_v2.jsonl`, and `vault999.jsonl`. It does NOT check `outcomes.jsonl`.

`outcomes.jsonl` is a **decision ledger**, not a chain ledger. It has its own canonical schema:
- `decision_id` + `session_id` + `verdict_issued` + `floor_attribution` (decision ledger)
- `event` + `ts` + `verdict` (tool-call telemetry)
- `chain_hash` + `prev_hash` + `ts` (chain-linked seal entries — only ~2,700 of 42K)

## Schema Distribution (outcomes.jsonl)

```
30,329  {} (actually: decision ledger entries — field set {decision_id, session_id, ...})
 7,397  (event, ts, verdict)             ← tool-call schema
 2,742  (chain_hash, event, ...)         ← chain-linked
   754  (prev_hash, timestamp)           ← old schema
   282  (event, timestamp)               ← old schema
```

**Key trap:** these 30,329 entries are NOT empty — they are decision-ledger records with a different field set. Naive "count missing chain_hash" = 38,947 entries, but most are in other schemas by design.

## JUDGE_SEAT_DEPUTY_ACTIVATED (the actual bug)

- **Total:** 18 entries (14 on 2026-08-07, 4 on 2026-08-08)
- **All 18:** missing `chain_hash`, using `timestamp` not `ts`
- **Location:** in `outcomes.jsonl` (decision ledger)
- **Root cause:** the JUDGE_SEAT_DEPUTY_ACTIVATED write path in arifOS uses old schema (`timestamp` not `ts`, no `chain_hash`)

## Broken link classification (from canonical verifier)

| kind | Meaning |
|---|---|
| `MISSING_CHAIN_HASH` | chain_hash field missing or empty — structural break |
| `PREV_MISMATCH` | prev_hash does not match prior entry's chain_hash |
| `PARSE_ERROR` | line fails JSON parse (malformed line) |
| `LEGACY_FLAT_ROW` | row uses flat schema without chain pointer (intentionally non-chain) |

## Auditor's tiering (corroborated)

| Tier | Finding | Status |
|---|---|---|
| 1 — Constitutional | 46 JUDGE_SEAT_DEPUTY entries + canonical verifier unwired | CRITICAL (bounded) |
| 2 — Governance | 666-AUDITOR-GODEL-LOCK named, not solved | unchanged |
| 3 — Measurement | FRAME chambers live, W-vectors unmeasured | unchanged |
| 4 — Operational | opencode_render.py, arif_seal gap, qwen-code | unchanged |

## Lessons for future audits

1. Always enumerate JSONL schemas before counting failures
2. Verify Makefile targets actually invoke the canonical checker
3. `outcomes.jsonl` is decision ledger (no chain), `vault999.jsonl` + `SEALED_EVENTS*.jsonl` are chain ledgers (different scope)
4. "Chain healthy" from a status reporter ≠ chain verified from canonical checker
