"""
AAA ACP — Agent Communication Protocol implementation for arifOS fleet.

Architecture:
    ACP Layer (this)
        ├── A2A Protocol (agent-to-agent messaging)
        ├── Agent Discovery (Agent Cards)
        └── Task Routing (OpenClaw → Hermes)

vs the stack:
    MCP = tool calling (agent → tools)
    A2A = peer messaging (agent ↔ agent)
    ACP = routing + discovery + sessions on top of A2A
"""

from AAA.acp.models import AgentCard, ACPMessage, ACPSkill, ACPProvider
from AAA.acp.client import ACPClient
from AAA.acp.router import ACPRouter

__all__ = [
    "AgentCard",
    "ACPMessage",
    "ACPSkill", 
    "ACPProvider",
    "ACPClient",
    "ACPRouter",
]
