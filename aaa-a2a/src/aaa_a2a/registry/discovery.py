""".well-known/agents.json generator.

Generates the A2A-spec-compliant /.well-known/agents.json shape
from the live registry.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

from typing import Any

from aaa_a2a.registry.agent_cards import discover_agents


async def generate_agents_json(registry_url: str = "http://localhost:3001") -> dict[str, Any]:
    """Generate the /.well-known/agents.json payload from live registry.

    Returns:
        dict with 'agents' list, each containing id, name, capabilities, endpoint.
    """
    agents = await discover_agents(registry_url)

    return {
        "federation": "arif-fazil.com",
        "version": "1.0",
        "agents": [
            {
                "id": agent.get("agentId", ""),
                "name": agent.get("name", ""),
                "description": agent.get("description", ""),
                "capabilities": agent.get("capabilities", {}),
                "endpoint": agent.get("endpoints", {}).get("baseUrl", ""),
                "protocolVersion": agent.get("protocolVersion", "1.0.0"),
                "skills": [s.get("id") for s in agent.get("skills", [])],
            }
            for agent in agents
        ],
    }
