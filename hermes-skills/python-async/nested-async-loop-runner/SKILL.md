---
name: nested-async-loop-runner
description: Run async coroutines safely from sync code in any event loop context — handles nested loops in Python 3.10+.
tags: [python, asyncio, fastmcp, runtime]
sources:
  - arifOS MCP audit (arif_memory_recall asyncio.run() crash, 2026-04-29)
---

# nested-async-loop-runner

## When to use

A sync tool/wrapper function needs to call an `async` coroutine, but it may be invoked either:
1. From a pure sync context (no event loop running), OR
2. From inside a running event loop (e.g. FastMCP sync tool wrapper called by an async handler)

Using `asyncio.run()` directly fails with `RuntimeError: This event loop is already running` in Python 3.10+ when path #2 applies.

## The wrong approaches (what most people try first)

```python
# ❌ WRONG — crashes in nested async context
result = asyncio.run(coro())

# ❌ WRONG — loop.run_until_complete() raises in Python 3.11+ when loop is already running
loop = asyncio.get_running_loop()
return loop.run_until_complete(coro)

# ❌ WRONG — result() called before future resolves (can't await in sync context)
loop = asyncio.get_running_loop()
future = loop.run_in_executor(pool, lambda: asyncio.run(coro))
return asyncio.wrap_future(future).result()  # InvalidStateError: Result is not set
```

## The correct solution

```python
import asyncio
import concurrent.futures

def _run_async(coro):
    """Run an async coroutine from a sync context safely, in any context."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop — safe to create one
        return asyncio.run(coro)
    
    # Already inside an async context — run in separate thread with its own loop.
    # Cannot use run_until_complete on a running loop (Python 3.11+ raises).
    def _thread_target():
        return asyncio.run(coro)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_thread_target)
        return future.result()  # Blocks this thread; executor thread has its own loop
```

## Verification

```python
# Test both contexts
async def dummy():
    return "ok"

# Pure sync context
result = _run_async(dummy())   # → "ok"

# Nested async context (simulates FastMCP sync wrapper in async handler)
async def simulate_fastmcp_handler():
    result = _run_async(dummy())  # NO await — _run_async is sync
    return result

assert asyncio.run(simulate_fastmcp_handler()) == "ok"  # → passes
```

## Why it works

- Path 1 (no loop): `asyncio.run()` creates its own loop, runs the coroutine, loop is destroyed after. Clean.
- Path 2 (running loop): `ThreadPoolExecutor` gives us a separate OS thread with its own event loop. `future.result()` blocks the calling thread until the executor thread completes. No loop conflict.

## Key insight

Python 3.11+ tightened `run_until_complete()` — it now raises `RuntimeError('This event loop is already running')` instead of silently creating a nested loop. The only safe way to bridge sync→async from inside a running loop is a separate thread with its own loop.

## Applies to

- FastMCP sync tool wrappers calling async memory/database operations
- Any sync callback invoked by an async framework (aiohttp, FastAPI, Starlette)
- Jupyter notebook environments (always have a running loop)
