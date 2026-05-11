---
name: arifos-python-parser-crash-recovery
description: Fix Python 3.13 dataclass syntax crashes in archived/deprecated arifOS modules — when importlib.util fails because the target file itself crashes Python's parser at load time.
tags: [python, arifos, python3.13, dataclass, import, debugging, archived]
last_updated: 2026-05-07
---

# arifos-python-parser-crash-recovery

## Problem

An archived Python module (e.g. `_archived/capability_map_deprecated.py`) contains syntax valid in earlier Python versions but broken in Python 3.13 (typically: `dataclass` with `slots=True` combined with `field(default=...)` — these are mutually exclusive in Python 3.13).

When you try to import it directly:
```python
import importlib.util
spec = importlib.util.spec_from_file_location("mod", "/path/to/mod.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # 💥 Python parser crashes here
```

The crash is at **parse time**, not runtime. Even `py_compile` fails. Standard import debugging tools don't work because the file can't even be loaded into Python.

## Diagnosis

1. Confirm it's a parser crash (not ImportError):
```python
python3 -c "import py_compile; py_compile.compile('/path/to/file.py')"
# If this fails with SyntaxError → parser crash
```

2. Read the file directly (bypass Python's import mechanism):
```python
with open('/path/to/file.py') as f:
    content = f.read()
```

3. Find the Python 3.13 incompatibilities — common patterns:
   - `dataclass(slots=True)` + `field(default=...)` in same class
   - `dataclass(slots=True)` + mutable default in field()
   - Other dataclass + slotting combinations

## Solution: Manual Symbol Extraction + Shim

Do NOT try to fix the archived file. Instead:

1. **Read the archived file directly** with `read_file` or Python's `open()`
2. **Identify only the symbols actually needed** by calling code (look for `ImportError` or `from x import y` failures in test output)
3. **Copy just those symbols** into a new `capability_map.py` shim
4. **Re-define them standalone** — no import from the archived module

```python
# capability_map.py — self-contained shim
# Do NOT: importlib.util.load_module_from_archived(...)
# DO: manually define only the symbols that callers actually need

LEGACY_TOOL_MAP = {...}   # copy from archived file
CANONICAL_TOOL_HANDLERS = {...}  # copy from archived file

def build_llm_context_map() -> dict[str, object]:
    """Return the canonical discovery payload."""
    return {
        "schema": "arifos-llm-context/v1",
        "canonical_tools": {...},
        "tool_aliases": dict(LEGACY_TOOL_MAP),
        ...
    }
```

## Real Example

**File:** `/root/arifOS/arifosmcp/capability_map.py`
**Archived source:** `/root/arifOS/arifosmcp/_archived/capability_map_deprecated.py`

The archived file crashed Python 3.13's parser due to:
```python
@dataclass(slots=True)
class SomeClass:
    field: str = field(default="value")  # 💥 mutual exclusion
```

**Fix:** Read the archived file, extract `build_llm_context_map()` function body (lines 132-191), `LEGACY_TOOL_MAP`, `CANONICAL_TOOL_HANDLERS`, `ALIGNED_STAGES`, `CAPABILITY_MAP`, `LEGACY_TOOLS` — copy each standalone definition into `capability_map.py`. Do NOT import the archived module.

## Why Not Fix the Archived File?

1. Archived files are snapshots — fixing them creates a fork that won't match git history
2. The crash is Python 3.13-specific — older Python versions won't see it
3. The archived file is intentionally frozen — we only need select symbols

## Verification

After creating the shim:
```bash
python3 -c "from arifosmcp.capability_map import build_llm_context_map; print(build_llm_context_map())"
# Should return dict without crashing

python3 -m pytest tests/ -q --tb=line 2>&1 | tail -3
# Should have fewer import-error failures
```

## Related

- `arifos-python-circular-import-pattern` — for circular ImportError problems (different from parser crash)
- `python-indentation-fix` — for indentation-only bugs in patches
