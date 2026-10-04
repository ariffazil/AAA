# VAULT999 Shape Probe — 2026-08-06

## Summary

`/root/arifOS/VAULT999/outcomes.jsonl` contains 37,016 entries (13.3 MB, `chattr +a`)
but with four overlapping schemas and only 11 hash-chained entries (0.0297% coverage).

## Schema Distribution

| Shape | Count | Primary keys |
|---|---|---|
| decision_log | 29,761 | `decision_id`, `session_id`, `verdict_issued`, `expected_outcome`, `actual_outcome`, `outcome_status`, `harm_detected`, `reversible`, `calibration_delta`, `operator_override`, `override_reason`, `timestamp_decision`, `timestamp_outcome`, `floor_attribution` |
| event_log | 5,798 | `ts`, `event`, `actor`, `session`, `tool`, `verdict`, `detail` |
| receipt | 612 | `receipt_id`, `receipt_type` (+ various payload fields) |
| other | 467 | various non-standard shapes |
| malformed | 380 | not parseable JSON |

## Hash-Chain Coverage

- `hash` field present: 31 entries
- `prev_hash` field present: 628 entries
- `seq` field present: 46 entries
- **Both `hash` AND `prev_hash` present: 11 entries**
- Hash-chain coverage: **11 / 37,016 = 0.0297%**

## Key Dates

- First entry: test fixtures (`D001 SEAL PENDING`, `sess-test`), timestamp ~2026-04-26
- First real hash-chained receipt: line ~12,218, `2026-05-17T10:02:00Z` (Telegram twin-bot routing debug)
- Latest entry: `2026-08-06T10:04:06Z` (event_log, `arif_observe` tool call)

## Architectural Implication

The architectural claim ("hash-chained append-only ledger") holds on the append-only axis
(`chattr +a` verified) but not on the chain-coverage axis. The file is a **four-register
forensic archive** — not a single sealed chain. This is correct as observation and
incorrect as architecture. The fix is either schema-enforce every entry onto the chain
or document the four-register structure as intentional.

## First Entry Schema (test fixture)

```json
{
  "decision_id": "D001",
  "session_id": "sess-test",
  "verdict_issued": "SEAL",
  "expected_outcome": "safe file read",
  "actual_outcome": "",
  "outcome_status": "PENDING",
  "harm_detected": false,
  "reversible": true,
  "calibration_delta": 0.0,
  "operator_override": false,
  "override_reason": "",
  "timestamp_decision": "1777194404.5178616",
  "timestamp_outcome": "",
  "floor_attribution": {}
}
```

## Latest Entry Schema (event_log)

```json
{
  "ts": "2026-08-06T10:04:06.622497+00:00",
  "event": "tool_call",
  "actor": "unknown",
  "session": "unknown",
  "tool": "arif_observe",
  "verdict": "UNKNOWN",
  "detail": ""
}
```

## Verification Script

```bash
python3 << 'EOF'
import json
from collections import Counter
shapes = Counter()
hash_chain = 0
malformed = 0
with open('/root/arifOS/VAULT999/outcomes.jsonl') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        if 'ts' in d and 'event' in d:
            shapes['event_log'] += 1
        elif 'decision_id' in d and 'verdict_issued' in d:
            shapes['decision_log'] += 1
        elif 'receipt_id' in d or 'receipt_type' in d:
            shapes['receipt'] += 1
        else:
            shapes['other'] += 1
        if 'hash' in d and 'prev_hash' in d:
            hash_chain += 1
total = sum(shapes.values()) + malformed
print(f'decision_log: {shapes["decision_log"]}')
print(f'event_log: {shapes["event_log"]}')
print(f'receipt: {shapes["receipt"]}')
print(f'other: {shapes["other"]}')
print(f'hash+prev_hash: {hash_chain} / {total} = {hash_chain/total*100:.4f}%')
print(f'malformed: {malformed}')
EOF
```

## Cross-references

- `references/2026-08-06-deepest-memory-recall.md` — confirms line 12,218 = first real hash receipt
- §17 of `verify-nested-sibling-reports` — the four-register trap and two-probe rule
- Pitfall entry in `federation-infra-verification` SKILL.md §17
