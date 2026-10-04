# Vault Reader — Dual-File Precedence Trap (2026-08-07)

## What it is

Two VAULT999 ledger files exist side-by-side on arifOS:

| Path | Schema | Last entry observed | Status |
|---|---|---|---|
| `/root/.local/share/arifos/vault999/seal_chain.jsonl` | `{"seq", "timestamp", "session_id", "actor", ...}` (uses `timestamp`) | `2026-08-03T08:53:06Z` | **STALE** (frozen since 2026-08-03) |
| `/root/arifOS/VAULT999/outcomes.jsonl` | `{"schema", "record_class", "record_id", "ts", ...}` (uses `ts`) | `2026-08-07T03:02:08.310367+00:00` | **ACTIVE** (appended each session close) |

## The bug

`runtime/webmcp/live_metrics.py:get_governance_metrics()` had this fallback (lines 316-326, pre-fix):

```python
if not vault_last:
    vault_path = Path("/root/.local/share/arifos/vault999/seal_chain.jsonl")
    if not vault_path.exists():
        vault_path = Path("/root/arifOS/VAULT999/outcomes.jsonl")
    if vault_path.exists():
        with open(vault_path) as f:
            lines = f.readlines()
            if lines:
                last = json.loads(lines[-1])
                vault_last = last.get("timestamp", "") or last.get("created_at", "")
```

**Two compounding problems:**

1. **First-existing wins, not newest.** The code reads whichever file exists first. With both existing, `seal_chain.jsonl` wins because it's listed first. The active `outcomes.jsonl` is never consulted. `/health.last_seal_timestamp` always reports 2026-08-03 even though seals are happening daily.

2. **Field-name mismatch.** `seal_chain.jsonl` uses `timestamp` (read works). `outcomes.jsonl` uses `ts` (read fails). Adding `or last.get("ts", "")` to the lookup chain only works if the file is actually read — and it isn't, because of problem #1.

## Symptom (what users see)

- `/health.governance.last_seal_timestamp` reports a date from weeks ago
- `tail outcomes.jsonl` shows fresh seals (yesterday, today)
- The kernel looks like its "arrow of time" is broken — but it's actually a read-path bug

## How to diagnose

```bash
# 1. Check both files exist and their last-entry timestamps
ls -la /root/.local/share/arifos/vault999/seal_chain.jsonl /root/arifOS/VAULT999/outcomes.jsonl
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl | python3 -c "import json,sys; print('seal_chain ts:', json.loads(sys.stdin.read()).get('timestamp'))"
tail -1 /root/arifOS/VAULT999/outcomes.jsonl | python3 -c "import json,sys; print('outcomes   ts:', json.loads(sys.stdin.read()).get('ts'))"

# 2. Check what /health reports
curl -sf http://127.0.0.1:8088/health | python3 -c "import json,sys; print(json.load(sys.stdin).get('governance',{}).get('last_seal_timestamp'))"

# 3. If vault timestamp is weeks old but /health reports today → working
#    If vault is fresh but /health reports old → BUG (you're in this doc)
```

## The fix (canonical, applied 2026-08-07)

```python
if not vault_last:
    # Read BOTH vault files and pick the newest timestamp.
    vault_candidates = [
        Path("/root/.local/share/arifos/vault999/seal_chain.jsonl"),
        Path("/root/arifOS/VAULT999/outcomes.jsonl"),
    ]
    all_lines: list[str] = []
    for candidate in vault_candidates:
        if candidate.exists():
            with candidate.open() as fh:
                candidate_lines = fh.readlines()
                all_lines.extend(candidate_lines)

    if all_lines:
        def _parse_ts(line: str) -> str:
            try:
                obj = json.loads(line)
            except Exception:
                return ""
            if not isinstance(obj, dict):
                return ""
            return (
                obj.get("timestamp", "")
                or obj.get("created_at", "")
                or obj.get("ts", "")
                or ""
            )
        all_lines.sort(key=_parse_ts, reverse=True)
        newest_raw = all_lines[0]
        try:
            newest = json.loads(newest_raw)
        except Exception:
            newest = {}
        if not isinstance(newext, dict):  # noqa — see full patch
            newest = {}
        vault_last = (
            newest.get("timestamp", "")
            or newest.get("created_at", "")
            or newest.get("ts", "")
        )
```

Three things to make robust:
- `isinstance(obj, dict)` guard (seal_chain.jsonl has stray string lines)
- Sort by timestamp key, descending — pick newest
- Three-tier field fallback: `timestamp` → `created_at` → `ts`

## Verification after deploy

```bash
# Compare vault truth vs /health truth
VAULT_TS=$(tail -1 /root/arifOS/VAULT999/outcomes.jsonl | python3 -c "import json,sys; print(json.load(sys.stdin).get('ts'))")
HEALTH_TS=$(curl -sf http://127.0.0.1:8088/health | python3 -c "import json,sys; print(json.load(sys.stdin).get('governance',{}).get('last_seal_timestamp'))")
[ "$VAULT_TS" = "$HEALTH_TS" ] && echo "PASS" || echo "FAIL: vault=$VAULT_TS health=$HEALTH_TS"
```

## Why the read-source bug class matters

This is the same hazard class as `_FLOOR_DEFAULTS` substitution (silent default masks unmeasured) and the dual `/health` endpoints (`/health` reads from `thermo.get("floors")` directly, `/api/governance-status` reads from `_build_governance_status_payload()` — different code paths, different outputs).

**Three diagnostic rules for any "data missing from health surface" complaint:**

1. **Both files exist?** Check both. The system may have multiple persistence paths and the reader picks one.
2. **Field names match?** Check the actual record schema. `timestamp` vs `created_at` vs `ts` are all live in arifOS. Don't guess.
3. **Endpoint duality** — `/health` vs `/api/governance-status` vs `/metrics/json` are three different routes through the kernel. They may not agree. Query all three when in doubt.

## Broader principle

When a system has multiple persistence paths for the same logical data (vault files, in-memory caches, aggregate metrics), the *fastest path* tends to win. The fastest path is rarely the most current. When in doubt, read **all paths** and reconcile by timestamp.

This same pattern bit the SC4 floor fix: `runtime_floors` in `/health` was fed by an older code path than `governance.floors` in `/api/governance-status`. Different paths = different realities.