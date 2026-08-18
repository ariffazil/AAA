# handover.log — clerk death certificates

**Path:** `/root/AAA/telemetry/handover.log`  
**Kind:** append-only JSONL. Not SOT. Not `state.json`.  
**Writer:** clerks via `handover-append.sh`  
**Reader:** `arifos-hero.sh` (last 5 `ACTIVE`)

`terminal/` = mutable runtime (`state.json`).  
`telemetry/` = event stream. Do not merge them.

## 8 fields + 2 extensions

| Field | Type | Notes |
|---|---|---|
| ts | ISO-8601 UTC | |
| actor | string | clerk / harness / 888 |
| session_id | string | F11 |
| category | enum (8) | see below |
| summary | string ≤100 | |
| sots_touched | string[] | |
| delta_s | float | ≤ 0 preferred |
| status | ACTIVE · RESOLVED · SEALED · SUPERSEDED | |
| prev_hash | sha256 hex | hash of previous **line** including `\\n`. First line = 64 zeros |
| floor_impact | string[] | e.g. `["F2","F11"]`. Empty if none |

## 8 categories

`collision_fix` · `blueprint_map` · `config_patch` · `port_shift` · `drift_alert` · `seal_record` · `handover_intake` · `sot_mutation` · `constitutional_pivot`

`constitutional_pivot` registered 2026-08-18 (first instance: runtime inherits reality).  
Deferred: `witness_received`.

## LAW (two sources, one field)

| Use | File |
|---|---|
| Floor-anchored / constitution | `/root/arifOS/GENESIS/000_KERNEL_CANON.md` **primary** |
| Federation bootstrap / protocol | `/root/AAA/prompts/INIT.md` |

ATLAS `LAW` points at GENESIS. INIT is federation bootstrap, not the constitution.

## Concurrency

Append uses `fcntl.flock` + `O_APPEND` + `fsync`. Safe for multi-clerk writes.
