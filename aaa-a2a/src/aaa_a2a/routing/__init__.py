"""A2A task routing — intent to organ to MCP tool.

Routes A2A tasks to the correct federation organ via MCP HTTP.
Each organ owns a domain: GEOX=earth, WEALTH=capital, WELL=vitality, etc.
"""

from aaa_a2a.routing.organ_router import route_intent, call_mcp_tool, ORGANS

__all__ = ["route_intent", "call_mcp_tool", "ORGANS"]
