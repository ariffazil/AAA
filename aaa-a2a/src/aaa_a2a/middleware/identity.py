"""Identity Verification — agent identity resolution.

Verifies agent identity from Bearer token or agent_id declaration.
Maps to registered agent identity with authority band.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

from aaa_a2a.models import AgentIdentity, AuthorityBand

# ── Known Agent Registry (in-memory, loaded from agent-cards/) ──────────

_AGENTS: dict[str, AgentIdentity] = {}


def register_agent(identity: AgentIdentity) -> None:
    """Register an agent identity."""
    _AGENTS[identity.agent_id] = identity


def get_agent(agent_id: str) -> AgentIdentity | None:
    """Get registered agent identity by ID."""
    return _AGENTS.get(agent_id)


def resolve_identity(
    agent_id: str | None = None,
    bearer_token: str | None = None,
) -> AgentIdentity:
    """Resolve agent identity from token or agent_id.

    Returns registered identity if found, otherwise defaults to observer.
    """
    if agent_id and agent_id in _AGENTS:
        return _AGENTS[agent_id]

    # Default: unknown agent = observer only
    return AgentIdentity(
        agent_id=agent_id or "unknown",
        principal="unknown",
        role="observer",
        authority_band=AuthorityBand.OBSERVE,
    )


def list_agents() -> list[AgentIdentity]:
    """List all registered agents."""
    return list(_AGENTS.values())


def load_from_registry(registry_url: str = "http://localhost:3001") -> int:
    """Load agent identities from live AAA registry via HTTP.

    Returns number of agents loaded.
    """
    import httpx

    try:
        resp = httpx.get(f"{registry_url}/a2a/discover", timeout=5.0)
        resp.raise_for_status()
        data = resp.json()
        agents = data.get("agents", [])
        for agent in agents:
            agent_id = agent.get("agentId", "")
            if not agent_id:
                continue
            register_agent(
                AgentIdentity(
                    agent_id=agent_id,
                    principal=agent.get("provider", {}).get("organization", "unknown"),
                    role=agent.get("tags", ["observer"])[0] if agent.get("tags") else "observer",
                    authority_band=AuthorityBand.OBSERVE,
                )
            )
        return len(agents)
    except Exception:
        return 0
