# SC4 Floor-Defaulting Trap — runtime_floors silent substitution

The arifOS `/health` payload reports `runtime_floors` as a dict of floor ID → numeric score. The kernel uses these scores to compute `execution_readiness`, `service_health`, and the OWNER_SUMMARY COLOR (green/yellow/red). If a floor lacks a real measurement, the system needs to emit `null` + `reason: "no_measurement"` so downstream consumers can distinguish "floor at zero" from "floor never measured."

The current code (as of commit `ef5ee9bba`) has an SC4 half-fix: the helper exists but the silent default substitution happens BEFORE the helper runs.

## Where the trap lives

**File:** `/root/arifOS/arifosmcp/runtime/rest_routes/rest_routes.py`

### Line 907 — silent substitution (the defect)

```python
resolved_floors = {k: floors.get(k, v) for k, v in _FLOOR_DEFAULTS.items()}
```

`_FLOOR_DEFAULTS` is the dictionary of calibrated fallback values (e.g., `F7: 0.04`, `F8: 0.80`). When `floors.get("F9")` returns `None`, the substitution silently inserts `0.04` (or whatever the default is). The downstream `_floor_status_strict` helper receives a real number and labels it "pass" or "fail" — never "unmeasured".

### Line 761 — the helper (correct, but unreachable)

```python
def _floor_status_strict(law_id: str, score: Any) -> str:
    """Return one of 'unmeasured' | 'pass' | 'fail' for a floor.

    Additive sibling of _floor_passes that exposes the unmeasured state
    instead of silently substituting default values (F13 constraint 2026-08-03:
    'no missing source may render PASS').
    """
    if score is None:
        return _FLOOR_STATUS_UNMEASURED
    try:
        fscore = float(score)
    except (TypeError, ValueError):
        return _FLOOR_STATUS_UNMEASURED
    # ...
```

The helper correctly handles `None` → "unmeasured". But because `_FLOOR_DEFAULTS` substitution happens upstream, `score` is never `None` by the time the helper sees it.

### Line 3131 — the emission site

```python
"runtime_floors": thermo.get("floors", {}),
"runtime_floors_status": {
    fid: {
        "score": score,
        "status": _floor_status_strict(fid, score),
        "measured": _floor_status_strict(fid, score) != "unmeasured",
    }
    for fid, score in thermo.get("floors", {}).items()
},
```

`runtime_floors_status` IS emitted with `measured: bool` and `status: "pass"|"fail"|"unmeasured"`. But `thermo.get("floors", {})` is the source dict, which has its own resolution path inside `_build_governance_status_payload`. The `measured: true/false` field is honest — IF the source dict's `floors` has the floor key as `None` rather than defaulted.

## The honest floor values live in `thermo["floors"]`

`_build_governance_status_payload()` (around line 870) reads `floors = state.get("floors", {})` from the live kernel state. If `state["floors"]["F9"]` is `None` (shadow never measured), then `thermo["floors"]["F9"]` is `None`, and the emission site correctly emits `"measured": false, "status": "unmeasured", "score": null`. So the SC4 half-fix DOES work end-to-end — IF the live kernel state honestly reports `None` for unmeasured floors.

The remaining ambiguity: the live `/health` shows `F9: 0.0`. Either:
- (a) `shadow` telemetry was actually measured and equals 0.0 (which is possible — low deception signal = good)
- (b) `shadow` was never measured and 0.0 is the default

You cannot distinguish (a) from (b) from the `/health` output alone. You have to look at the live telemetry pipeline (`state.get("telemetry", {})`) to see whether `shadow` was actually populated.

## Why this matters

Three downstream consumers depend on `runtime_floors`:

1. **`service_health`** (line 1044) → "green"/"yellow"/"red". Computed from `substrate_degraded` (substrate liveness), NOT from floor values directly. Safe.
2. **`execution_readiness`** → "void"/"held"/"ready". Also derived from substrate, not floors. Safe.
3. **`owner_summary.color`** → "GREEN"/"YELLOW"/"RED" badge. This is what Arif sees on first glance. The color comes from `runtime_drift` + `vault_health`, not floor values directly. Safe.

So the immediate blast radius of the SC4 trap is **display honesty**, not floor enforcement. The numbers in `runtime_floors` are decoration; the gates in the verdict path are what actually blocks execution.

## The fix (geometry brief from 2026-08-07, awaiting ratification)

Phase 3 of the zero-risk bundle:

```diff
--- a//root/arifOS/arifosmcp/runtime/rest_routes/rest_routes.py
+++ b//root/arifOS/arifosmcp/runtime/rest_routes/rest_routes.py
@@ -907,7 +907,9 @@ def _build_governance_status_payload() -> dict[str, Any]:
-    resolved_floors = {k: floors.get(k, v) for k, v in _FLOOR_DEFAULTS.items()}
+    resolved_floors = {k: None for k in _FLOOR_DEFAULTS}
+    for fid in resolved_floors:
+        v = floors.get(fid)
+        if v is not None:
+            resolved_floors[fid] = float(v)
```

And at the emission site:

```diff
-            "runtime_floors": thermo.get("floors", {}),
+            "runtime_floors": resolved_floors,  # null-safe (SC4)
```

The helper `_floor_status_strict` already handles `None` correctly. No other changes needed.

## Smoke test recipe

After applying the patch, verify end-to-end with:

```python
from arifosmcp.runtime.rest_routes.rest_routes import (
    _floor_status_strict,
    _FLOOR_DEFAULTS,
)

# Floor with no source measurement → unmeasured
assert _floor_status_strict("F9", None) == "unmeasured"

# Floor with real source measurement → pass or fail based on threshold
assert _floor_status_strict("F9", 0.04) in ("pass", "fail")  # depends on threshold

# Floor with NaN → unmeasured
import math
assert _floor_status_strict("F9", math.nan) == "unmeasured"

# Floor with non-numeric → unmeasured
assert _floor_status_strict("F9", "not a number") == "unmeasured"
```

Then check the live `/health` endpoint:

```bash
curl -sf http://127.0.0.1:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
status = d.get('runtime_floors_status', {})
for fid in ('F9', 'F8', 'F7'):
    entry = status.get(fid, {})
    print(f'{fid}: score={entry.get(\"score\")}, status={entry.get(\"status\")}, measured={entry.get(\"measured\")}, reason={entry.get(\"reason\")}')"
```

Expected: every floor shows `measured: true/false` honestly. Floors that were never measured show `score: null, status: "unmeasured"`.

## Related references

- `references/dual-verdict-paths.md` — the wrapper-vs-judge path divergence (separate but related gate-omission class)
- `references/deployment-drift-markers.md` — the `.git_commit` lying about code state (related to floor display, since deployment_drift_status reports on this)
- `references/kernel-floor-id-duality-and-judge-paths.md` — F1–F13 vs L01–L13 dual-encoding

## Provenance

Captured from arifOS session 2026-08-07, investigating the "9 floor values look fine but execution_readiness=held" pattern. The trapped state is real but currently cosmetic — execution_readiness comes from substrate, not floors. The honest fix is still warranted: a future sovereign-grade consumer (or I-ARIF judge-ML) needs to read floors as truth, not as defaults.