# FastMCP 4 Breaking Changes (Reference)

Forged: 2026-08-11 | Source: WELL staging migration run on FastMCP 4.0.0b2 + mcp SDK 2.0.0

## Change 1: `_check_accept_headers` → `_validate_accept_header` (async, 4 args)

**Old (FastMCP 3.x):**
```python
def _check_accept_headers(self, request):
    if request.headers.get("accept") != "application/json":
        raise ValueError("Only JSON accepted")
```

**New (FastMCP 4.x):**
```python
async def _validate_accept_header(self, request, scope, send):
    if request.headers.get("accept") != "application/json":
        await send({"type": "http.response.start", "status": 406, "headers": [(b"content-type", b"text/plain")]})
        await send({"type": "http.response.body", "body": b"Not acceptable"})
```

**Symptom of monkey-patch mismatch:** `TypeError: _patched() takes 2 positional arguments but 4 were given`

**Fix pattern (if you must monkey-patch):**
```python
# WRONG (old-style sync patch)
def _patched(self, request):
    ...
(server as any)._validate_accept_header = _patched

# RIGHT (new-style async patch matching the 4-arg signature)
async def _patched(self, request, scope, send):
    # do your check
    return await original(self, request, scope, send)
(server as any)._validate_accept_header = _patched
```

**Detection:** grep for `_check_accept_headers` in your source. If found, update to `_validate_accept_header`.

## Change 2: TasksExtension separated from core

**Old (FastMCP 3.x):** `@mcp.tool(task=True)` worked out of the box.

**New (FastMCP 4.x):** TasksExtension must be explicitly imported and registered.

```python
# FastMCP 4.x requires this block (place near server startup)
try:
    from fastmcp_tasks import TasksExtension  # type: ignore
    mcp.add_extension(TasksExtension())
except ImportError:
    pass  # fastmcp-tasks not installed, task=True tools will fail silently
```

**Install command (in staging venv):**
```bash
pip install --pre "fastmcp-tasks==4.0.0b2"
```

**Symptom of missing TasksExtension:** tools decorated with `task=True` are registered but fail at runtime with no clear error. Add the extension block, restart, verify.

## Change 3: Strict `clientCapabilities` enforcement

**Old (FastMCP 3.x):** `clientCapabilities` in `_meta` was optional. Missing fields → ignored.

**New (FastMCP 4.x):** `clientCapabilities` is required for stateless 2026-07-28 clients. Missing → error code `-32602`.

```python
# Required for stateless clients (curl, MCPJam modern, 2026-07-28 spec)
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": "2026-07-28",
    "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {
            "roots": {},
            "sampling": {},
        }
    }
}
```

**Detection:** If stateless clients (curl, MCPJam) receive `-32602 Invalid Request` but sessioned clients work, you're missing `clientCapabilities`.

**Workaround for legacy clients:** FastMCP 4 will negotiate back to 2025-11-25 if 2026-07-28 isn't fully supported. Test #1 in the 8-receipt matrix checks this.

## Detection Cheat Sheet

| Error | Likely cause | Fix |
|-------|--------------|-----|
| `TypeError: takes 2 positional arguments but 4 were given` | Old-style monkey-patch on `_validate_accept_header` | Rewrite as `async def _patched(self, request, scope, send)` |
| `@mcp.tool(task=True)` tool registered but fails at runtime | Missing TasksExtension | Add the `mcp.add_extension(TasksExtension())` block |
| `-32602 Invalid Request` from stateless client | Missing `clientCapabilities` | Add to `_meta` per snippet above |
| Server returns `2025-11-25` when client requested `2026-07-28` | Expected fallback (dual-era) | NOT a bug — FastMCP 4 supports both, server negotiates down |

## Reference Run: WELL Staging (2026-08-11)

All 3 breaking changes were encountered and fixed in the WELL staging run:

```
1. Accept-headers: Patched from `_check_accept_headers` (sync, 2 args)
   to `_validate_accept_header` (async, 4 args) → fixed TypeError

2. TasksExtension: Added `mcp.add_extension(TasksExtension())` block
   after fastmcp-tasks==4.0.0b2 install → tasks now work

3. clientCapabilities: All curl test commands include
   `clientCapabilities` in `_meta` → no -32602 errors
```

Receipt: `/root/forge_work/2026-08-11-well-staging/WELL-STAGING-RECEIPT.md`

## What to Check BEFORE Migration

```bash
# In your source code, grep for patterns that will break
grep -rn "_check_accept_headers" /root/<ORGAN>/src/  # should be empty for 4.x
grep -rn "@mcp.tool(task=True)" /root/<ORGAN>/src/  # needs TasksExtension block
grep -rn "_meta" /root/<ORGAN>/src/  # check clientCapabilities presence
```

If any of these returns hits, budget time to fix them before the 8-receipt test matrix.
