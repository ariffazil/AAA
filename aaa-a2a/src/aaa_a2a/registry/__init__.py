"""Agent card registry bridge — wraps live agent-card-registry via HTTP.

Python aaa-a2a reads from the live Node registry, never duplicates it.
"""

from aaa_a2a.registry.agent_cards import (
    discover_agents,
    get_agent_card,
    search_agents,
    find_by_skill,
)
from aaa_a2a.registry.discovery import generate_agents_json

__all__ = [
    "discover_agents",
    "get_agent_card",
    "search_agents",
    "find_by_skill",
    "generate_agents_json",
]
