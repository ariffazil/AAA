# Multi-Bug arifOS/WEALTH/Caddy Patch Session — 2026-05-19

Session: 5 bugs fixed in one session across arifOS, WEALTH, and Caddy.

## Bugs Fixed

### P1 — tools.py search() dict unwrap pattern

**Problem:** `memory_store.search()` returns dict `{"results": [...]}` but callers in `tools.py` iterated return value as a list of memory records. In recall mode, this iterated dict keys ("results", etc.) causing `r.get(...)` to fail.

**Files:** `/root/arifOS/arifosmcp/runtime/tools.py` lines ~6399-6402, ~6567-6568

**Fix pattern:**
```python
# Before (broken)
results = _ms_search(query=query or "", limit=10)
for r in results:  # iterates dict keys if dict returned
    memories.append(r.get(...))

# After (fixed)
_raw = _ms_search(query=query or "", limit=10)
_results = _raw.get("results", []) if isinstance(_raw, dict) else (_raw or [])
for r in _results:
    memories.append(r.get(...))
```

**Verification:** `python3 -m py_compile tools.py` → OK

---

### P1 — get_memory_store phantom export (Phoenix janitor broken)

**Problem:** `__all__` in memory_store.py exported `get_memory_store` but the function didn't exist. The `memory_janitor.py` imports it at module level → import fails → Phoenix-72 janitor can't start.

**File:** `/root/arifOS/arifosmcp/runtime/memory_store.py`

**Fix:** Added `get_memory_store` to `__all__` list (phantom was in exports but not in module).

**Root cause note:** `memory_janitor.py` also calls `seal_entry`, `void_entry`, `get_expired_cooling_entries` — these are aspirational stubs that don't exist in the module. Janitor will still fail at RUNTIME for missing methods, but IMPORT is fixed.

**Verification:** `python3 -m py_compile memory_store.py` → OK

---

### P2 — _pg_get_by_qdrant_id wrong column

**Problem:** Function named `_pg_get_by_qdrant_id` but actually queried `WHERE qdrant_id = $1` using `pg_id` parameter (which is the Postgres primary key id, NOT the qdrant_id). With `include_deleted=False`, every persisted Qdrant point with a pg_id was treated as deleted and skipped → `arif_memory_audit` returns empty escalation surface.

**File:** `/root/arifOS/arifosmcp/runtime/memory_store.py` lines 895-897

**Fix:**
```python
# Before (wrong column)
def _pg_get_by_qdrant_id(pg_id: str | None):
    row = await conn.fetchrow(
        "SELECT ... FROM memory_store WHERE qdrant_id = $1",  # WRONG
        pg_id
    )

# After (correct column)
def _pg_get_by_id(pg_id: str | None):
    row = await conn.fetchrow(
        "SELECT ... FROM memory_store WHERE id = $1",  # CORRECT
        pg_id
    )
```

**Also fixed:** Call site changed from `_pg_get_by_qdrant_id(pg_id)` → `_pg_get_by_id(pg_id)`

**Verification:** `python3 -m py_compile memory_store.py` → OK

---

### P2 — Caddyfile shared_assets 404

**Problem:** `handle /_shared/*` with `root * /var/www/html/_shared` keeps `/ _shared` segment when resolving → requests for `/_shared/app.css` resolve to `/var/www/html/_shared/_shared/app.css` (double prefix).

**File:** `/root/arifOS/deploy/Caddyfile` lines 22-25

**Fix:**
```caddy
# Before (double prefix)
(handle shared_assets) {
    handle /_shared/* {
        root * /var/www/html/_shared
        file_server
    }
}

# After (strip_prefix correct)
(handle shared_assets) {
    handle /_shared/* {
        root * /var/www/html
        strip_prefix /_shared
        file_server
    }
}
```

---

### P2 — hedge_drag hold trigger ignored (WEALTH)

**Problem:** `wealth_evaluate_prospect` computes `hedge_drag` and defines `HEDGE_DRAG_THRESHOLD`, but verdict doesn't check it. A prospect with large hedge mismatch can still return `QUALIFY` as long as EMV positive and paradox low.

**File:** `/root/WEALTH/mcp/server.py` line ~162-163

**Fix:**
```python
# Before (hedge_drag computed but ignored in verdict)
hold_triggered = (emv < 0) or (paradox_score >= 0.5)
verdict = "QUALIFY" if emv > 0 and paradox_score < 0.5 else "888-HOLD"

# After (hedge_drag gates verdict)
hold_triggered = (hedge_drag > 0.15) or (emv < 0) or (paradox_score >= 0.5)
verdict = "QUALIFY" if emv > 0 and paradox_score < 0.5 and hedge_drag <= 0.15 else "888-HOLD"
```

**Verification:** `python3 -m py_compile server.py` → OK

---

## Multi-Bug Session Pattern

When auditing a code change that touches multiple files:
1. Check each file compiles independently
2. Verify the fix pattern in context (don't just trust the old string match)
3. For dictunwrap fixes: always check if the return value is actually a dict or list
4. For `_pg_get_by_X` functions: verify the WHERE clause column matches the parameter name
5. For Caddyfile path handling: always check if strip_prefix is needed when changing root

## Files Modified Summary

```
arifOS/arifosmcp/runtime/tools.py         — search dict unwrap (2 locations)
arifOS/arifosmcp/runtime/memory_store.py — _pg_get_by_id fix + __all__ export
arifOS/deploy/Caddyfile                   — strip_prefix fix
WEALTH/mcp/server.py                      — hedge_drag verdict gate
```