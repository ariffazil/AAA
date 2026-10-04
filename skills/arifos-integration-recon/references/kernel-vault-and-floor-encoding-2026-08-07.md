# Kernel Vault & Floor Encoding — Live Bugs (2026-08-07)

Two durable kernel bugs surfaced in the 2026-08-07 contradiction map. Both have known fix recipes but are NOT yet patched (awaiting Arif's authorization per "stabilize, don't add").

## Bug 1: `last_seal_timestamp` always null despite wiring

### Symptom

`curl http://127.0.0.1:8088/health | jq .governance.last_seal_timestamp` → `null` (always)

### Root cause

File: `/opt/arifos/app/arifosmcp/runtime/webmcp/live_metrics.py`
Function: `get_governance_metrics()`
Lines: 325-326

```python
                    if lines:
                        last = json.loads(lines[-1])
                        vault_last = last.get("timestamp", "") or last.get("created_at", "")
```

### The mismatch

The vault record schema (verified on disk, `/root/.local/share/arifos/vault999/outcomes.jsonl`) uses field name `ts`:

```jsonl
{"schema":"arifos.record.v1","record_class":"SESSION_RECEIPT","record_id":"RECEIPT-2026-08-06-wealth-sprint1-2","ts":"2026-08-06T07:47:11.197975+00:00","actor":{...}}
```

The reader checks `"timestamp"` then `"created_at"`. Neither exists. `vault_last` is always empty string → falsy → returns null.

### Two health endpoints affected

Both `/health` and `/metrics/json` delegate to `get_live_metrics()` via `live.get("governance", {}).get("vault_last_seal")`:

| Endpoint | Line | Key path |
|---|---|---|
| `/health` | `rest_routes.py:3349` | `"last_seal_timestamp": vault_last_seal` inside `governance` |
| `/metrics/json` | `rest_routes.py:3923` | same path |

Fixing the reader fixes both.

### Fix recipe (single-line, one word)

```diff
-                        vault_last = last.get("timestamp", "") or last.get("created_at", "")
+                        vault_last = last.get("timestamp", "") or last.get("created_at", "") or last.get("ts", "")
```

Three-tier fallback covers all known vault schemas. After deploy:
```bash
curl -sf http://127.0.0.1:8088/health | python3 -c "import json,sys; d=json.load(sys.stdin); print('last_seal_timestamp:', repr(d['governance'].get('last_seal_timestamp')))"
```

Expected: a real ISO-8601 timestamp string.

### Why this is durable

The schema `arifos.record.v1` (see top of file) is canonical. Future record creators will use `ts`. The reader should match. This is a 1-character bug with 1-character fix.

## Bug 2: Unmeasured floors render as PASSING values, not null

### Symptom

`runtime_floors` shows `F9: 0.0`, `F7: 0.04`, `F12: 0.43` in `/health`. The system cannot tell whether these are real failed measurements or "no measurement engine running."

`execution_readiness: "held"` is set with no diagnostic for *which* floor caused the hold.

### Root cause

File: `/opt/arifos/app/arifosmcp/runtime/rest_routes/rest_routes.py`
Function: `_build_governance_status_payload()`

**Line 907** (default seed):
```python
    resolved_floors = {k: floors.get(k, v) for k, v in _FLOOR_DEFAULTS.items()}
```

`_FLOOR_DEFAULTS` is built by `_canonical_floor_defaults()` (line 306-307), which calls `_representative_floor_score(fid)` for every `LAW_SPEC_KEYS` entry. For F9, this returns a **PASSING value** (the threshold itself), not `None`.

**Line 922-925** (failure mask):
```python
    for fid in LAW_SPEC_KEYS:
        val = resolved_floors.get(fid)
        if val is not None and not _floor_passes(fid, float(val)):
            resolved_floors[fid] = _FLOOR_DEFAULTS[fid]
```

This replaces ANY failing score with the passing default. So a genuinely-failed floor becomes "passing." Unmeasured becomes "passing." The system cannot distinguish three states:
1. Measured and passing
2. Measured and failing (silently upgraded to passing)
3. Unmeasured (silently upgraded to passing)

### `_floor_passes` already has the right discipline

Lines 705-735: `_floor_passes` (FLR-001, 2026-08-03) gates missing source as NOT PASS. But this discipline is **NOT applied** at the fallback path in lines 907/922.

### Fix recipe (3 surgical edits, ~15 lines)

**Edit A** — line 907, after the seed, add unmeasured-aware default:
```diff
     resolved_floors = {k: floors.get(k, v) for k, v in _FLOOR_DEFAULTS.items()}
+
+    # SC4 FIX (2026-08-07): Unmeasured floors must be null, not false zeros.
+    measured_keys = set(floors.keys())
+    for fid in LAW_SPEC_KEYS:
+        if fid not in measured_keys:
+            resolved_floors[fid] = None
+
```

**Edit B** — lines 922-925, don't hide unmeasured as passing:
```diff
     for fid in LAW_SPEC_KEYS:
-        val = resolved_floors.get(fid)
-        if val is not None and not _floor_passes(fid, float(val)):
-            resolved_floors[fid] = _FLOOR_DEFAULTS[fid]
+        val = resolved_floors.get(fid)
+        if val is None:
+            continue
+        if not _floor_passes(fid, float(val)):
+            resolved_floors[fid] = _FLOOR_DEFAULTS[fid]
```

**Edit C** — in the final payload construction (around line 3131), expose unmeasured list:
```diff
             "runtime_floors": thermo.get("floors", {}),
+            "unmeasured_floors": [fid for fid in LAW_SPEC_KEYS if resolved_floors.get(fid) is None],
```

### Verification after deploy

```bash
curl -sf http://127.0.0.1:8088/health | python3 -c "
import json,sys
d = json.load(sys.stdin)
floors = d['runtime_floors']
print('null floors:', [k for k,v in floors.items() if v is None])
print('unmeasured list:', d.get('unmeasured_floors'))
print('F9:', repr(floors.get('F9')))
"
```

Expected: `F9` is `null`, `unmeasured_floors` includes `["F9"]` (and any other floor with no measurement).

### Risk

Low. Consumers already accept `float | None` in several places. Where consumers DON'T accept null, the fix exposes their bugs — which is correct behavior, not new risk.

### Why this is durable

The pattern (defaults mask measurement state) is the same pattern that made `last_seal_timestamp` always null. Both are: "the system cannot tell the truth about its own state." Until both are fixed, the constitution is grounded but the constitutional *reporting* is not.

## Related (not bugs, but durable kernel semantics)

### `_FLOOR_DEFAULTS` returns passing values, not "default unmeasured"

`_representative_floor_score()` at line 285-303:
```python
    if law_id == "F7" and "range" in spec:
        return float(low) + 0.01  # in-band humility
    if comparator in {">", ">="}:
        return threshold  # passing value
    if comparator == "<=":
        return threshold  # passing value
```

The function's name says "representative" but its behavior is "default PASSING." If you call this expecting "what does a neutral floor look like," you get a misleading answer.

This is by design (calibrated to pass) but should be renamed `_representative_passing_floor_score()` to match behavior.

### `runtime_floors` mixes F-prefix and L-prefix keys

Live observation: `{"F1": 0.5, "F2": 1.0, ..., "F9": 0.0, "L10": 1.0, "L11": 1.0, "L12": 0.43, "L13": 1.0}`.

Two encodings for the same constitutional surface, mixed in one dict. `judge.py:8421` has `_identity_floors = {"L11", "F11", "L13", "F13"}` — explicit dual-encoding accommodation.

**Out of scope for "stabilize, don't add."** The contradiction is real but unifying the IDs is a `SC1` patch requiring coord across `constitutional_map.py`, `runtime/law.py`, and ~50 callers. Multi-day blast radius. Don't do it without explicit sovereign direction.