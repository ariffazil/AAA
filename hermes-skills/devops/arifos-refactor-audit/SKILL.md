---
name: arifos-refactor-audit
description: arifOS constitutional diff verification — trace removed code, verify floor enforcement still exists, identify gaps after refactors
triggers:
  - dirty files in arifOS with large line-count changes
  - refactor involving server.py, runtime/, or core/ layers
  - user asks what was removed / if enforcement is missing
  - git diff shows architectural simplification
  - user asks "drift or compression?" or "regression or progression?"
---

# arifOS Refactor Audit — Constitutional Diff Verification

## Trigger

When asked to review git diffs or assess what a refactor removed from arifOS codebase. Use when:
- Dirty files in arifOS repo with large line-count changes
- Refactor involving `server.py`, `runtime/`, or `core/` layers
- Need to verify constitutional enforcement still exists after changes
- User asks to classify changes as drift/compression/progression/regression

## Classification Framework

When analyzing a diff, classify each removal into one of four buckets:

| Class | Meaning | Signal |
|-------|---------|--------|
| **DRIFT** | Something that worked/gated is now gone | Enforcement hole created |
| **COMPRESSION** | Legitimate simplification, no enforcement lost | Same outcome, less code |
| **PROGRESSION** | Genuine improvement — new capability or better approach | Adds value |
| **REGRESSION** | Was broken, now fixed | Bug was present, now gone |

**Key diagnostic question:** Was the removed code *actually being called*, or was it dead code?
- Dead code removal = COMPRESSION (good)
- Live enforcement removal = DRIFT (bad)
- Was broken/stubbed = REGRESSION → fix it

## Audit Protocol

### Step 1 — Git Diff Overview
```bash
cd /root/arifOS
git status                      # what branches are dirty
git diff --stat                 # high-level: which files, how big
git diff <file>                 # full per-file diff
git stash list                  # check for WIP commits sitting locally
```

**Always run `git diff --stat` BEFORE committing** — a 3rd dirty file can appear that wasn't part of the discussed changes.

### Step 2 — Trace the Critical Path

**For removed functions, was it actually wired?**
```bash
# Was the function definition removed?
grep -n "FUNCTION_NAME" server.py

# Was the wiring block (that applied the function) also removed?
grep -n "HARDENED_HANDLERS\|_CANONICAL_HANDLERS.update\|_CANONICAL_HANDLERS.clear" server.py
# If function exists but wiring block doesn't → dead code = COMPRESSION (not DRIFT)
```

**For import path changes** (e.g. `core.floors` → `runtime.floors`):
```bash
# Check both paths exist
ls -la arifosmcp/runtime/floors.py arifosmcp/core/floors.py
cat arifosmcp/runtime/floors.py   # check if shim or real implementation
```

### Step 3 — Constitutional Enforcement Check

**Floor enforcement verification — 3 patterns exist:**

1. **Central dispatch** (removed in 2026-04 refactor): `_wrap_hardened_dispatch` in `server.py` wrapping ALL tools
2. **Per-tool call** (current): `check_floors()` called explicitly inside each tool handler
3. **Kernel evaluation** (vault/forge): `_KERNEL.evaluate_intent()` in `runtime/tools.py`

**To check which tools call `check_floors`:**
```bash
grep -l "check_floors" arifosmcp/tools/*.py | wc -l   # count protected tools
grep -L "check_floors" arifosmcp/tools/*.py           # tools with ZERO floor enforcement
```

**To check real implementation path:**
```bash
grep -n "def check_floors" arifosmcp/runtime/floor.py arifosmcp/core/floors.py
# runtime/floor.py = real enforcer; runtime/floors.py = shim (DeprecationWarning)
```

### Step 4 — Stub/Lie Detection

Endpoints that return hardcoded lies about system state:
```python
# IS a regression — lies about what tools are registered:
return JSONResponse({"tools": [], "count": 0})

# IS a regression — lies about full system state:
return JSONResponse({"status": "ok"})  # when real probe was doing real work
```

### Step 5 — Runtime Verification

If changes are on VPS, verify live container matches committed state:
```bash
curl -s http://localhost:8080/health | python -m json.tool  # check startup
docker exec <container> git -C /app status --short          # verify committed state
docker ps --format "{{.Names}} {{.Status}}"                # check container health
```

## Patch Protocol

When regressions found, apply surgical patches — **no new tools, no new logic**:

### Regression 1: Stub endpoints lying about state
```python
# BEFORE (broken):
async def tools_with_meta(request: Request) -> JSONResponse:
    return JSONResponse({"tools": [], "count": 0})

# AFTER (truthful):
async def tools_with_meta(request: Request) -> JSONResponse:
    return JSONResponse({
        "tools": v2_tools_registered,
        "count": len(v2_tools_registered),
        "version": _DEPLOY_VERSION,
    })
```

### Regression 2: Dead code left behind
After removing dead functions that used `inspect` or `asyncio`:
```bash
# Check if imports are still used
grep -n "^import inspect\|^import asyncio" server.py
# Remove both if unused — prevents false confidence in future audits
```

### Verification after patching
```bash
python -m py_compile arifosmcp/server.py && echo "SYNTAX OK"
git diff --stat   # should be minimal: only the regressions fixed
```

## Key Findings from 2026-04-30 Audit

| Pattern | Classification | Notes |
|---------|---------------|-------|
| `check_floors` in `runtime/floor.py` | ✅ Real impl | 36-line enforcer, F1-F13 interceptors |
| `check_floors` in `runtime/floors.py` | ⚠️ Shim | DeprecationWarning → re-exports from `floor.py` |
| Per-tool floor calls | ✅ ~13 tools | session, sense, kernel, gateway, forge, etc. |
| Tools with ZERO floor checks | ❌ 25+ files | judge, heart, architect, lsp, reality, agentzero_tools, etc. |
| Central `_wrap_hardened_dispatch` | **COMPRESSION** | Defined but NEVER wired; dead code removal |
| Federation probe `/status.json` | **COMPRESSION** | Was 200 lines of httpx AsyncClient; caused 502s, removal is legitimate simplification |
| `/tools` endpoint hardcoded empty | **REGRESSION** | Was stubbed to return `{"tools": [], "count": 0}` — lies about registered tools → patched to truth |
| `rest_routes.py` +26 lines | **PROGRESSION** | `/runtime_fingerprint` endpoint — genuine drift detection improvement |

## Lessons Learned

1. **Import path changes** (`core.floors` → `runtime.floors`) must be verified — shims hide real impl location
2. **Deprecation shims** in `runtime/` directory can mask whether real logic exists
3. **Per-tool `check_floors` opt-in** is weaker than central dispatch — any new tool that doesn't call it runs naked
4. **`git stash list`** — always check; 6 WIP stashes were sitting unnoticed
5. **Dead code vs removed enforcement** — trace whether the function was actually wired before classifying removal as DRIFT. `grep -n "HARDENED_HANDLERS"` tells you if it was applied.
6. **Stub endpoints are regressions** — returning `[]` or `{"status": "ok"}` when the real state is different is a lie, not cleanup
7. **COMPRESSION doesn't mean benign** — removing cross-cutting enforcement (even if buggy) is still weaker than having it
8. **Large diffs** (−645 lines) often mean architectural simplification — verify *actual* enforcement impact
9. **Always `git diff --stat` before committing** — surprise dirty files appear that weren't discussed
10. **`asyncio` and `inspect` imports** — check if still used after removing dead code; remove if orphaned
