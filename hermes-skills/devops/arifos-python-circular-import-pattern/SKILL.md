---
name: arifos-python-circular-import-pattern
description: Break circular Python imports in arifOS runtime modules by duplicating small stateless helpers locally. Triggered by ImportError involving floors.py/floor.py.
tags: [python, arifos, import, dependency]
last_updated: 2026-05-01
---

# arifos-python-circular-import-pattern

## Problem
Python circular import when two runtime modules both need to reference each other at import time.

## Known Cycle in arifOS
```
floor.py (needs _nine_signal_from_status from tools.py)
  → tools.py (imports check_floors from floors.py at module load)
    → floors.py (deprecated alias that re-imports from floor.py)
```

## Solution: Local Helper Duplication
When the shared utility is small (≤10 lines) and stateless, duplicate it locally in the requesting module rather than importing. This breaks the cycle without changing the dependency graph.

```python
# In arifosmcp/runtime/floor.py — duplicate instead of import:

def _nine_signal_from_status(status: str) -> dict[str, str]:
    """Build Nine-Signal block from response status field."""
    if status == "OK":
        return {"delta": "KUKUH", "psi": "DITERIMA", "omega": "BIJAK", "overall": "SELAMAT"}
    if status in ("HOLD", "VOID"):
        return {"delta": "GANTUNG", "psi": "GANTUNG", "omega": "DIAMBIL", "overall": "HENTI"}
    return {"delta": "GANTUNG", "psi": "GANTUNG", "omega": "GANTUNG", "overall": "HENTI"}
```

## When NOT to Use This Pattern
- Utility is >20 lines or has external dependencies → refactor into a third shared module
- Utility is frequently updated → duplication causes divergence bugs
- Utility is tested independently → import and test it once in its canonical location

## Alternative: Lazy Import
For larger utilities, use lazy import inside the function body:
```python
def some_function():
    from arifosmcp.runtime.tools import _nine_signal_from_status
    return _nine_signal_from_status("OK")
```
This delays the import to call time, not module-load time, breaking the cycle.

## arifOS Specific Notes
- `floors.py` is deprecated alias. Always import from `floor.py`.
- `tools.py` has the canonical `_nine_signal_from_status` but also imports from `floors.py`.
- `floor.py` is the correct place for the duplicated helper since it's the law kernel.

## Trigger
When you see: `ImportError: cannot import name 'check_floors' from 'arifosmcp.runtime.floors'`
