---
name: arifos-mcp-three-surface-debug
description: Debug why arifOS MCP resources and prompts are not exposed — FastMCP registered but custom stdio loop unreachable
tags: [arifOS, MCP, FastMCP, debugging]
last_verified: 2026-05-06
---

# arifOS MCP Three-Surface Debug

## Trigger
Debugging MCP endpoint on arifOS when `tools/list` works but `resources/list` or `prompts/list` return nothing or errors.

## Symptom
```
curl -sf http://localhost:8080/mcp -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"resources/list","params":{}}'
# Returns error or empty — but FastMCP resources are registered in arifosmcp/resources/
```

## Root Cause
arifOS uses a **custom stdio JSON-RPC loop** in `arifosmcp/runtime/__main__.py` that only handles:
- `initialize`
- `tools/list`
- `tools/call`

It does NOT handle:
- `resources/list`
- `resources/read`
- `prompts/list`
- `prompts/get`

FastMCP resources and prompts ARE registered via `register_resources(mcp)` and `register_prompts(mcp)` in `server.py`, but they are unreachable because the custom loop short-circuits before FastMCP's transport layer processes them.

## Diagnostic Steps

### 1. Verify MCP spec — 3 separate capability surfaces

| Surface | Protocol Methods | MCP Capability Field |
|---------|-----------------|---------------------|
| Tools | `tools/list`, `tools/call` | `capabilities.tools` |
| Resources | `resources/list`, `resources/read`, `resources/subscribe` | `capabilities.resources` |
| Prompts | `prompts/list`, `prompts/get` | `capabilities.prompts` |

### 2. Check initialize response
```bash
curl -sf http://localhost:8080/mcp -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```
If `capabilities` only has `tools`, resources and prompts are not exposed.

### 3. Check what the stdio transport handles
```bash
grep -n "resources\|prompts" /root/arifOS/arifosmcp/runtime/__main__.py
```
Expected: should find `resources/list` and `prompts/list` handlers. If zero matches — found the gap.

### 4. Check FastMCP registration in server.py
```bash
grep -n "register_resources\|register_prompts" /root/arifOS/arifosmcp/server.py
```
Should show both are called.

### 5. Verify resources/prompts actually exist
```bash
ls /root/arifOS/arifosmcp/resources/
ls /root/arifOS/arifosmcp/prompts/
```

## Fix Options

### Option A — FastMCP Native Transport (recommended)
Replace the custom `__main__.py` stdio loop with `mcp.run()` which handles all three surfaces natively.

### Option B — Extend Custom Transport
Add missing handlers to `__main__.py` AND update the initialize capability:
```python
"capabilities": {
    "tools": {"listChanged": True},
    "resources": {"subscribe": True, "listChanged": True},
    "prompts": {"listChanged": True}
}
```

## arifOS Specific Locations
- Custom stdio loop: `/root/arifOS/arifosmcp/runtime/__main__.py`
- FastMCP server: `/root/arifOS/arifosmcp/server.py` (lines 151-212)
- Resources: `/root/arifOS/arifosmcp/resources/` (5 canonical + F-WEB evidence)
- Prompts: `/root/arifOS/arifosmcp/prompts/` (system, judge, init, meta-skills)
- MCP spec: https://modelcontextprotocol.io/specification/2025-11-25/server/

## Key Insight
FastMCP registers resources/prompts at the Python object level, but if a custom transport loop handles JSON-RPC directly (bypassing FastMCP's transport), those handlers are unreachable. The registration (`register_*()` calls) is NOT the same as exposure (protocol method handlers).
