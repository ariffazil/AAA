# PHASE 3 · STEP 2+3 — Generator Seam & First Patch (333-AGI, 2026-09-18)

## STEP 2 — the seam, in writing

**Where the public schema is produced:** `register_tools()` (`arifosmcp/runtime/tools.py` ~27625). For each name in `public_tool_names_for_mode()`: handler ← `_CANONICAL_HANDLERS[name]`; description ← `public_registry`; then the **enum injection block** (~27744) patches the registered tool's JSON Schema: `_modes = constitutional_map[name]["modes"]` → written into `properties.mode.enum`.

**Where dispatch happens:** `_CANONICAL_HANDLERS[name]` → handler internals. For `arif_memory`: `_arif_memory_v5_router` → routes known v5 modes to `megaTools/tool_13_arif_memory` (whose `ARIF_MEMORY_MODES` tuple is the v5 dispatch table) and everything else to legacy `_arif_memory_recall`.

**The seam defect (exhibit A, measured):** three declarations, joined by hand —
1. `constitutional_map` `modes` (advertised intent — 8 modes)
2. router `v5_native_modes` (hand-copied literal — **missing `audit`**)
3. `ARIF_MEMORY_MODES` + legacy branches (actual capability — 13 + 19 legacy)

`audit` existed in (1) and (3), absent in (2) → advertised, implemented, never routed = **phantom mode**. Measured before-fix: legacy direct call → `RETAK`; source probe: `router literal has audit: False`.

**Can one be derived from the other? Yes — prefer deriving:**
- routing **derives** from the dispatch table: `v5_native_modes = frozenset(ARIF_MEMORY_MODES)`.
- advertisement stays a **governance subset** (`constitutional_map`) but is **filtered at registration** to ⊆ the handler's declared universe (`__dispatch_modes__`).
- no third definition needed: capability declares its universe; governance declares the public subset; the guard enforces `advertised ⊆ claimed ⊄universe`.

## STEP 3 — first patch (local only, NOT deployed)

File: `/root/arifOS/arifosmcp/runtime/tools.py` (commit `local`, +41/−8)

| # | Change |
|---|---|
| A | router derives v5 triage set from `ARIF_MEMORY_MODES` (single source of truth) |
| B | `_arif_memory_v5_router.__dispatch_modes__` = frozenset(13 modes) declared |
| C | `register_tools` guard: advertised enum filtered ⊆ declared universe; logs `MODE ENUM GUARD` on any drop; undeclared handlers unchanged (extension point for other tools) |

**Evidence (in-process vs repo copy):** `audit → v5 routed` ✓ · `recall → v5` (control) ✓ · `banana → legacy fallthrough` ✓ · advertised 8/8 kept (audit now dispatchable) ✓ · py_compile clean ✓.

**NOT deployed:** live venv copy + app copy untouched; restart + wire re-measure + baseline v0.2 enum pass await F13.

**Collateral findings for reconciliation:**
1. `/opt/arifos/arifosmcp/runtime/tools.py` is a **skewed lineage** (~80 diff lines; carries a "C1 FIX 2026-09-17 · Tool degradation ≠ substrate degradation" variant the live copy lacks) — flag for deploy-line reconciliation.
2. `federation_query` / `federation_sync` / `score_prediction` / `metabolize` / `reconcile` are implemented in v5 and become callable-by-name after deploy, but remain **unadvertised** (map subset unchanged) — consistent with "resolve server-side, never appear in discovery".
