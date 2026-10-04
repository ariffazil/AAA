# VAULT999 Mixed Schemas — Field-Name Drift in `outcomes.jsonl`

Discovered 2026-08-08. Two record types in the same file with incompatible field names.

## The two shapes

**Type A — tool_call / seal / COMMIT_RECEIPT (hash-chained):**
```json
{
  "ts": "2026-08-08T05:14:37.790149+00:00",
  "event": "tool_call",
  "actor": "kimi-code/FI-008",
  "tool": "arif_init",
  "verdict": "UNKNOWN",
  "payload_hash": "791775d8beaa2e92",
  "prev_hash": "GENESIS",
  "chain_hash": "a724288a12b676ad"
}
```

**Type B — AGENT_MODEL_MAP deputy-failover (NOT in the hash chain):**
```json
{
  "channel": "deepseek_direct",
  "decision": "PROCEED",
  "event": "JUDGE_SEAT_DEPUTY_ACTIVATED",
  "primary_seat": "deepseek/deepseek-v4-pro",
  "deputy_seat": "deepseek/deepseek-v4-pro",
  "role": "666_JUDGE",
  "reason": "Primary seat failed; serving role via map-allowed deputy.",
  "registry_path": "/root/AAA/registries/models/AGENT_MODEL_MAP.json",
  "tool_origin": "333_REASON",
  "timestamp": "2026-08-08T05:15:34.058624+00:00",
  "chain_hash": null
}
```

Key field-name differences:
- `ts` (Type A) vs `timestamp` (Type B) — same semantic, different key
- `chain_hash` present (Type A) vs `null` (Type B)
- `actor`, `tool`, `verdict` present (Type A) vs absent (Type B)
- Type B carries governance metadata (`deputy_seat`, `primary_seat`, `reason`)

## Scale

- ~43 Type B records in a 41821-line file (as of 2026-08-08)
- Type B records are written by AGENT_MODEL_MAP deputy-failover logic, not the kernel seal chain
- The records are NOT corrupt — they are a different writer that doesn't participate in the hash chain

## Impact

`make vault999-verify` and chain-hash verification scripts break on Type B records because `chain_hash` is null and the timestamp field name is different. Fix: filter before verification.

## Filter patterns

```bash
# Only verify hash-chained records (Type A)
cat outcomes.jsonl | jq -c 'select(.chain_hash != null)' | jq -c '{ts, chain_hash}'

# Find only deputy-failover entries
grep "JUDGE_SEAT_DEPUTY" outcomes.jsonl | jq -c '{event, timestamp, role}'

# Chain-hash verifier (safe across both shapes)
cat outcomes.jsonl | jq -c '
  select(.chain_hash != null)
  | {ts: .ts, hash: .chain_hash, event: .event}
' | head -20
```

## Recommended fix path (non-urgent)

Normalize the two types to a shared envelope:
```json
{
  "ts": "...",              // always "ts", never "timestamp"
  "chain_hash": "...",     // always present (null if non-chain)
  "record_class": "tool_call | deputy_failover | commit_receipt",
  "event": "...",
  ...                      // type-specific fields
}
```

A one-time normalization pass can be written as a Python script over `outcomes.jsonl` → `outcomes.normalized.jsonl` → rename. Do NOT do this without F13 authorization — the file is append-only (`chattr +a`).

## FQ with `verify_count > execute_count` is HEALTHY

The degenerate FQ case is `verify_count == 0` with `execute_count > 0` — quotient f64::MAX, verdict OPTIMAL, meaning zero verification happened. The mirror case where `verify_count > execute_count` (e.g. 9 > 6 → quotient 1.5) is legitimate high-verification coverage — genuinely OPTIMAL. Always read both counts alongside the quotient to avoid false alarms.

Live example (2026-08-08):
```json
{"fq": {"execute_count": 6, "verify_count": 9, "quotient": 1.5, "verdict": "OPTIMAL"}}
```
This means verification outpaces execution — good governance, not a bug.
