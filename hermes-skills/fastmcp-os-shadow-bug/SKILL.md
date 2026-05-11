---
name: fastmcp-os-shadow-bug
description: "FastMCP 3.2.4 async tool shadowing bug — `import os` at module level gets undefined inside async tool wrappers. Use when FastMCP tool throws 'cannot access local variable os where it is not associated with a value' or similar NameError for stdlib modules imported at module top-level."
category: devops
tags: [fastmcp, python, bug, async, shadowing]
---

# FastMCP 3.2.4 `os` Variable Shadow Bug

## Symptom

Tool works when called from Python directly:
```python
from geox.engines.correlation_panel import build_correlation_panel
build_correlation_panel(...)  # ✅ OK
```

But fails via FastMCP HTTP endpoint:
```
Error calling tool 'geox_well_correlation_panel': cannot access local variable 'os' 
where it is not associated with a value
```

## Root Cause

FastMCP 3.2.4 wraps async tools in an instrumentation/context layer that creates a new local scope for the function body. The module-level `import os` at the top of the **calling** module (`unified_13.py`) gets shadowed — Python sees `os` as a local name that was never assigned in the async wrapper's scope.

## Fix

Replace `os.path.exists(path)` with `Path(path).exists()` using `pathlib`:

```python
# Before (breaks in FastMCP async wrapper):
import os
if os.path.exists(path):
    ...

# After (always works):
from pathlib import Path
if Path(path).exists():
    ...
```

`pathlib.Path` is imported at module level in most files and is never shadowed because it's accessed as `Path(...)` (a call, not a name reference).

## Affected Functions

Any function in `unified_13.py` or similar FastMCP tool files that calls `os.path.exists`, `os.path.join`, etc. from within an async tool function.

## Verification

Test both ways:
1. Direct Python import (bypasses FastMCP)
2. Via HTTP MCP endpoint (exercises FastMCP wrapper)

If (1) works but (2) fails → this bug.
