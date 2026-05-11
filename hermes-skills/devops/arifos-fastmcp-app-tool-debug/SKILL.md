---
name: arifos-fastmcp-app-tool-debug
description: Debug why FastMCPApp tools don't appear in tools/list — visibility=["app"] filter in FastMCP 3.2.0
tags: [fastmcp, arifos, mcp, debugging]
version: 1.0.0
---

# Skill: Debug FastMCP App Tool Visibility in arifOS

## Symptom
`add_provider(fastmcp_app)` succeeds silently, provider shows in `mcp.providers`, but `mcp.list_tools()` returns zero tools from that provider.

## Root Cause
FastMCP 3.2.0 `server.py:185` — `_is_model_visible()` filters out any tool whose `meta.ui.visibility == ["app"]`.  
`FastMCPApp` registers all its tools with `visibility=["app"]` so they appear in app UIs but are stripped from MCP `tools/list` responses to clients.

```python
def _is_model_visible(tool: Tool) -> bool:
    visibility = tool.meta.get("ui", {}).get("visibility", [])
    if not isinstance(visibility, list):
        return True
    return "model" in visibility  # ["app"] → returns False
```

## Diagnostic Steps
1. `mcp.list_tools()` — count tools from the app
2. `mcp.providers` — confirm app is registered
3. Read `fastmcp/server/server.py:185` — check `_is_model_visible()`
4. Import and call `await fastmcp_app_instance.list_tools()` directly — if it returns tools, the issue IS visibility filtering

## Solution
Do NOT use `add_provider()` for tools that must be visible to MCP clients. Instead wire them directly:

```python
from arifosmcp.apps.command_center.some_app import some_handler

def _cc_tool_wrapper(*args, **kwargs) -> dict:
    return some_handler(*args, **kwargs)

mcp.tool(name="tool_name")(_cc_tool_wrapper)
```

## Why This Matters in arifOS
- `command_center` FastMCPApp has 7 dashboard tools (session_status, ops_vitals, judge_action, etc.)
- These must be visible to MCP clients for the governance dashboard to work
- `add_provider(command_center_app)` silently produced 0 visible tools
- Fix: wire each CC tool directly onto the main `mcp` server using `mcp.tool(name="...")(handler_func)`

## Verification
```python
import asyncio
from arifosmcp.server import mcp
async def check():
    tools = await mcp.list_tools()
    print(f'Total: {len(tools)}')  # should be 20 (13 canonical + 7 CC)
asyncio.run(check())
```

## Key Files
- `arifosmcp/server.py` — `_is_model_visible()` filter at line ~185
- `arifosmcp/apps/command_center/app.py` — FastMCPApp with 7 tools
- FastMCP provider path: `fastmcp/server/providers/aggregate.py` — `AggregateProvider._list_tools()` aggregates from all providers
