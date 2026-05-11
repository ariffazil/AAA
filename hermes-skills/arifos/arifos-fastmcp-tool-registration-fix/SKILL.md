---
name: arifos-fastmcp-tool-registration-fix
description: Fix KeyError 'mode' in arifOS FastMCP tool registration caused by _wrap_handler() overwriting __annotations__
tags: [arifOS, FastMCP, debugging, tool-registration]
last_updated: 2026-04-27
---

# arifOS FastMCP Tool Registration Debug

## Symptom
After fixing circular imports, `arifOS MCP` starts but fails tool registration with:
```
KeyError: 'mode'
```
on the first tool call (e.g. `arif_session_init`).

## Root Cause
`_wrap_handler()` in `arifosmcp/runtime/tools.py` wraps canonical handlers with a generic signature:
```python
def _wrap_handler(handler, name):
    async def wrapper(args: Any = None, kwargs: Any = None) -> Any:
        ...
    wrapper.__wrapped__ = handler
    wrapper.__annotations__ = {"args": "Any", "kwargs": "Any", "return": "Any"}
    return wrapper
```

FastMCP's `ParsedFunction.from_function` reads `__annotations__` directly from the function object — NOT from `__wrapped__`. So when it looks up `mode` (the first parameter of `arif_session_init`), it's searching the wrapper's `{"args", "kwargs", "return"}` annotation dict and raises `KeyError`.

## Fix
The `_wrap_handler()` function should NOT overwrite `__annotations__` with generic types. Instead, preserve the original function's annotations:

```python
def _wrap_handler(handler, name):
    async def wrapper(args: Any = None, kwargs: Any = None) -> Any:
        ...
    wrapper.__wrapped__ = handler
    # Do NOT override __annotations__ — FastMCP reads them from the wrapper directly
    # If you must set annotations, preserve the original's:
    # wrapper.__annotations__ = {**handler.__annotations__}
    return wrapper
```

The `__wrapped__` attribute is used elsewhere (e.g. by `inspect.signature`) but NOT by FastMCP's `ParsedFunction` when it resolves parameter names.

## Verification
```bash
docker run --rm arifos:local python3 -c "
import sys; sys.path.insert(0, '/app/arifosmcp')
from arifosmcp.runtime.tools import _CANONICAL_HANDLERS, _wrap_handler
import inspect

h = _CANONICAL_HANDLERS['arif_session_init']
w = _wrap_handler(h, 'arif_session_init')
print('Wrapped annotations:', w.__annotations__)  # Must include mode, actor_id, etc.
print('Wrapped signature:', inspect.signature(w))  # Must show (mode, actor_id, ...)
"
```

## Related
- Circular import fix for `core.judgment`: sys.path prepend + explicit `sys.modules["core"].floors = floors` attachment
- Sys.path bug: `arifosmcp/core/__init__.py` had `sys.path.insert(0, '/app')` which duplicated the path since `/app/arifosmcp` was already at position 0