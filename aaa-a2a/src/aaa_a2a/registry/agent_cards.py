"""Registry Bridge — wraps live agent-card-registry via HTTP.

Bridges to the Express server's /a2a/discover endpoints.
Python aaa-a2a reads from the live registry, never duplicates it.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

from typing import Any

import httpx


REGISTRY_URL = "http://localhost:3001"


async def discover_agents(registry_url: str = REGISTRY_URL) -> list[dict[str, Any]]:
    """Fetch all registered agents from live registry."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{registry_url}/a2a/discover", timeout=5.0)
            resp.raise_for_status()
            data = resp.json()
            return data.get("agents", [])
    except Exception:
        return []


async def get_agent_card(agent_id: str, registry_url: str = REGISTRY_URL) -> dict[str, Any] | None:
    """Fetch a specific agent card from the registry."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{registry_url}/a2a/discover/{agent_id}", timeout=5.0)
            resp.raise_for_status()
            data = resp.json()
            return data.get("card")
    except Exception:
        return None


async def search_agents(query: str, registry_url: str = REGISTRY_URL) -> list[dict[str, Any]]:
    """Search agents by query string."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{registry_url}/a2a/discover/search",
                params={"q": query},
                timeout=5.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("agents", [])
    except Exception:
        return []


async def find_by_capability(
    capability: str, registry_url: str = REGISTRY_URL
) -> list[dict[str, Any]]:
    """Find agents with a specific capability."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{registry_url}/a2a/discover/capability/{capability}",
                timeout=5.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("agents", [])
    except Exception:
        return []


async def find_by_skill(skill_id: str, registry_url: str = REGISTRY_URL) -> list[dict[str, Any]]:
    """Find agents with a specific skill."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{registry_url}/a2a/discover/skill/{skill_id}",
                timeout=5.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("agents", [])
    except Exception:
        return []


async def get_registry_stats(registry_url: str = REGISTRY_URL) -> dict[str, Any]:
    """Get registry statistics."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{registry_url}/a2a/discover/stats", timeout=5.0)
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return {"totalAgents": 0, "totalSkills": 0}
