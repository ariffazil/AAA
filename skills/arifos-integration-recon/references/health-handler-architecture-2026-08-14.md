# arifOS /health Handler Architecture — Two-Route Split & Umbrella Degraded

Verified 2026-08-14 by reading deployed source at `/opt/arifos/app/`.

## The Two /health Implementations

There are TWO `/health` handlers in the codebase. Only ONE actually serves requests.

### 1. `horizon_health()` — server.py:2465 (NOT SERVING)

```python
async def horizon_health(request: Request) -> JSONResponse:
    """GET /health — Three-signal honest health (transport/kernel/floors)."""
```

Clean design: returns `status` (worst-of-three) + `signals{transport, kernel, floors, thread_pool}`.
~7 fields total. Well-documented with honesty notes.

**This function exists but is NOT registered as the /health route.** It is defined in
`server.py` but `register_rest_routes()` in `rest_routes.py` registers a DIFFERENT handler
at `/health` that takes precedence.

### 2. `health()` — rest_routes.py:3114 (ACTUALLY SERVING)

```python
@route("/health", methods=["GET"])
async def health(request: Request) -> Response:
```

This is the handler that actually serves `GET /health`. It is registered inside
`register_rest_routes()` (rest_routes.py:2925). It produces the 80+ key enriched response.

**How to confirm which handler serves:**
```bash
# The rest_routes registration wins because it runs AFTER server.py routes
grep -n 'register_rest_routes' /opt/arifos/app/arifosmcp/server.py
# Line ~3906: register_rest_routes(app, CANONICAL_TOOL_HANDLERS, mcp)
```

## The Umbrella Degraded Problem

### How `status: degraded` is computed (rest_routes.py:~3247)

```python
runtime_drift_val = bool(_drift.get("runtime_drift", False))    # from _compute_runtime_drift()
contract_drift_val = contracts.get("contract_drift", True)      # from contract_status_summary()

# Also OR'd with software_release attestation drift:
_sr_drift = bool(_attest.get("drift"))
runtime_drift_val = runtime_drift_val or _sr_drift

_degraded = runtime_drift_val or contract_drift_val
payload = {"status": "degraded" if _degraded else "healthy", ...}
```

**Problem:** Multiple independent issues collapse into one opaque boolean. Agents reading
`status: degraded` cannot tell WHICH cause triggered it without reading individual fields.
No `degraded_reasons[]` array exists in the top-level payload.

### What `registry_truth` actually means (rest_routes.py:~3340)

```python
"registry_truth": "VERIFIED" if not contract_drift_val and not runtime_drift_val else "DRIFT_DETECTED",
```

`registry_truth` is DERIVED from drift flags, NOT from tool count comparison.
It has nothing to do with the 62/48/8 numbers.

### The 62/48/8 Tool Counts — BY DESIGN

| Field | Value | Meaning |
|---|---|---|
| `tools_registry_size` | 62 | Internal registry callables (canonical + aliases) |
| `total_declared_tools` | 48 | Public wire (8) + diagnostic (40) |
| `tools_exposed_via_mcp` | 8 | Public MCP tools/list facade |

These numbers are NOT a mismatch. The `tool_count_semantics` dict in the payload explains
each field. 62 > 48 > 8 because aliases inflate registry and diagnostic tools aren't on
the public wire. **Do not report this as drift.**

## Cache Behavior

The `/health` handler has a **5-minute TTL cache** (`_health_cache`):

```python
# rest_routes.py:~3136
if not _nocache and not _want_detail and _health_cache["payload"] is not None:
    if _now - _health_cache["ts"] < 300.0:  # 5min TTL
        return JSONResponse(_health_cache["payload"])
```

Bypass with: `curl localhost:8088/health?nocache=1` or `?detail=1`

## Key Code Locations (deployed /opt/arifos/app/)

| What | File | Line |
|---|---|---|
| Actual /health handler | `arifosmcp/runtime/rest_routes/rest_routes.py` | ~3114 |
| _degraded computation | same | ~3247 |
| registry_truth derivation | same | ~3340 |
| _build_governance_status_payload | same | ~868 |
| _compute_runtime_drift | same | ~2521 |
| register_rest_routes | same | ~2925 |
| horizon_health (NOT serving) | `arifosmcp/server.py` | ~2465 |
| Health cache TTL | `rest_routes.py` | ~3136 |

## Init Token Staleness

The `arif_init` response includes a `software_release` block with `built_commit` from
install time. This can differ from the live `/health` endpoint's `source_commit` because
the init token caches the wheel metadata from when the package was installed.

**Symptom:** Agent reads init token → sees `built_commit: 8077223`. Agent reads /health →
sees `source_commit: b1d14ff`. Agent reports drift. But `runtime_matches_build: true` in
/health means the running code IS correct — only the metadata label is stale.

**Fix:** Rebuild wheel from current source: `cd /opt/arifos/app && pip install -e .`

## Proposed Fix: degraded_reasons[] + layer_health{}

The architectural fix (additive, no logic change):

1. **`degraded_reasons: []`** — after computing `_degraded`, build an array listing
   exact causes: `["runtime_drift: source=X != built=Y", "contract_drift: ..."]`

2. **`layer_health: {}`** — separate the four layers explicitly:
   - `constitutional`: floors + vault999
   - `runtime`: drift + commit match
   - `registry`: tool counts (always healthy — 62/48/8 by design)
   - `infra`: pointer to /ready for load/swap

3. **Init token freshness warning** — when `built_commit != source_commit`, add
   `_freshness_warning` to the init token's software_release block.

SPEC for this fix: `/root/forge_work/health-degraded-reasons/SPEC.md`
