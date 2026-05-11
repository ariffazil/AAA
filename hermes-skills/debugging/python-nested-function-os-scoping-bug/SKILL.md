---
name: python-nested-function-os-scoping-bug
description: Python nested function scoping bug — os.close() in outer scope breaks os.path in nested functions
tags: [python, scoping, bug, fastmcp, nested-function]
last_updated: 2026-05-01
---

# Python Nested Function `os` Scoping Bug

## Trigger
A nested function (`def inner()`) defined **later** inside an outer function (`def outer():`) uses `os.path` or `os.listdir()` or similar — but the outer function previously assigned to `os` via `os.close(fd)` or any other `os.X()` call in a conditional/try block.

## Symptom
```
TypeError: cannot access local variable 'os': it is not found in scope
```
or
```
TypeError: cannot access local variable 'os': it is referenced before assignment
```

## Root Cause
Python's scoping rules: once `os.close(fd)` executes in the outer function, Python treats `os` as a **local variable of the entire enclosing function** for the purposes of name resolution. When `inner()` later tries to access `os.path`, Python looks up the local `os` — which hasn't been assigned yet at that point in code execution.

## Pattern (BAD)
```python
def outer():
    if condition:
        os.close(fd)      # ← makes `os` local to outer()'s scope
    def inner():
        os.path.exists(x)  # ← TypeError: local variable 'os' referenced before assignment
```

## Pattern (GOOD)
```python
def outer():
    import os as _os     # use a DIFFERENT local name
    if condition:
        _os.close(fd)    # ← safe, _os is local
    def inner():
        os.path.exists(x)  # ← still refers to module-level os, not polluted
```

## Where This Hit arifOS
- `unified_13.py` — `os.close(fd)` in the URL-download branch of `geox_data_ingest_bundle` broke **all** nested tool functions
- Every tool call returned `TypeError: cannot access local variable 'os'` until fixed

## Verification
```python
# Quick test inside container:
docker exec <container> python3 -c "
from contracts.tools.unified_13 import geox_well_correlation_panel
# If this raises TypeError about 'os', the bug is still present
"
```

## Prevention
- Prefer module-level imports and keep all `os.*` calls at module level
- If you must use `os` inside an outer function with nested functions, use `import os as _os` with a different local name
