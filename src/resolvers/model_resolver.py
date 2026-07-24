"""
model_resolver.py — Canonical model resolver for AAA federation.
Reads strictly from /root/.config/federation-models.json.
Zero hardcoded model strings. Drift impossible by construction.

Usage:
    from model_resolver import resolve_agent_model, resolve_tier_model, list_agents

    cfg = resolve_agent_model("opencode")
    # → {"provider": "deepseek", "model": "deepseek/deepseek-v4-pro", ...}

    model = resolve_tier_model("heavy")
    # → "deepseek/deepseek-v4-pro"

Forged: 2026-07-24 by FORGE (000Ω). DITEMPA BUKAN DIBERI.
"""

import json
from pathlib import Path
from typing import Optional, Dict, List

CANONICAL_PATH = Path("/root/.config/federation-models.json")


def _load_registry() -> dict:
    """Load canonical registry. Raises FileNotFoundError if missing."""
    if not CANONICAL_PATH.exists():
        raise FileNotFoundError(
            f"Canonical model registry not found at {CANONICAL_PATH}. Run: forge --option-a to create it."
        )
    with open(CANONICAL_PATH) as f:
        return json.load(f)


def resolve_agent_model(agent_id: str) -> dict:
    """
    Resolve an agent's model configuration from canonical registry.

    Args:
        agent_id: Agent identifier (e.g. 'opencode', 'kimi-code', 'hermes')

    Returns:
        dict with keys: provider, model, fallback_chain, timeout_ms, cost_budget_daily_usd

    Raises:
        KeyError: Agent not found in registry
        FileNotFoundError: Canonical registry missing
    """
    registry = _load_registry()
    agents = registry.get("agents", {})

    if agent_id not in agents:
        raise KeyError(f"Agent '{agent_id}' not found in canonical registry. Available agents: {list(agents.keys())}")

    agent_cfg = agents[agent_id]
    provider_id = agent_cfg.get("primary_provider", "unknown")
    providers = registry.get("providers", {})
    provider_cfg = providers.get(provider_id, {})

    return {
        "agent_id": agent_id,
        "agent_name": agent_cfg.get("name", agent_id),
        "provider": provider_id,
        "provider_name": provider_cfg.get("name", provider_id),
        "model": agent_cfg["primary_model"],
        "fallback_chain": agent_cfg.get("fallback_chain", []),
        "timeout_ms": agent_cfg.get("timeout_ms", 30000),
        "cost_budget_daily_usd": agent_cfg.get("cost_budget_daily_usd", 0),
        "api_key_ref": provider_cfg.get("api_key_ref", ""),
        "endpoint": provider_cfg.get("endpoint", ""),
        "status": agent_cfg.get("status", "UNKNOWN"),
    }


def resolve_tier_model(tier: str) -> str:
    """
    Resolve the model for a given usage tier.

    Args:
        tier: One of 'bulk', 'default', 'heavy', 'apex'

    Returns:
        Model string (e.g. 'deepseek/deepseek-v4-pro')
    """
    registry = _load_registry()
    tiers = registry.get("tiers", {})

    if tier not in tiers:
        raise KeyError(f"Tier '{tier}' not found. Available: {list(tiers.keys())}")

    return tiers[tier]["model"]


def resolve_fallback(agent_id: str, failed_model: str) -> Optional[str]:
    """
    Given a failed model, return the next fallback for an agent.

    Args:
        agent_id: Agent identifier
        failed_model: The model that failed (to skip past)

    Returns:
        Next model in fallback chain, or None if exhausted
    """
    cfg = resolve_agent_model(agent_id)
    chain = cfg["fallback_chain"]

    # Find current position in chain
    for i, m in enumerate(chain):
        if m == failed_model or failed_model in m:
            if i + 1 < len(chain):
                return chain[i + 1]
            break

    # If not found, return first fallback
    return chain[0] if chain else None


def list_agents(status_filter: Optional[str] = None) -> List[dict]:
    """
    List all agents with their model assignments.

    Args:
        status_filter: Optional filter by status (ACTIVE, STANDBY, etc.)

    Returns:
        List of agent summaries
    """
    registry = _load_registry()
    agents = []

    for aid, cfg in registry.get("agents", {}).items():
        status = cfg.get("status", "UNKNOWN")
        if status_filter and status != status_filter:
            continue
        agents.append(
            {
                "agent_id": aid,
                "name": cfg.get("name", aid),
                "model": cfg["primary_model"],
                "provider": cfg.get("primary_provider", "unknown"),
                "status": status,
            }
        )

    return sorted(agents, key=lambda x: x["agent_id"])


def list_providers() -> List[dict]:
    """List all providers with status and balance."""
    registry = _load_registry()
    providers = []

    for pid, cfg in registry.get("providers", {}).items():
        providers.append(
            {
                "provider_id": pid,
                "name": cfg.get("name", pid),
                "status": cfg.get("status", "UNKNOWN"),
                "balance_usd": cfg.get("balance_usd"),
                "jurisdiction": cfg.get("jurisdiction", "unknown"),
                "billing": cfg.get("billing", "unknown"),
            }
        )

    return sorted(providers, key=lambda x: x["provider_id"])


# CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python model_resolver.py <agent_id>")
        print("       python model_resolver.py --list")
        print("       python model_resolver.py --tier <tier>")
        print("       python model_resolver.py --providers")
        sys.exit(1)

    if sys.argv[1] == "--list":
        for a in list_agents():
            print(f"{a['agent_id']:15s} → {a['model']:40s} ({a['status']})")

    elif sys.argv[1] == "--tier" and len(sys.argv) > 2:
        model = resolve_tier_model(sys.argv[2])
        print(f"tier={sys.argv[2]} → {model}")

    elif sys.argv[1] == "--providers":
        for p in list_providers():
            bal = f"${p['balance_usd']}" if p["balance_usd"] is not None else "N/A"
            print(f"{p['provider_id']:20s} {p['status']:12s} {bal:>8s}  {p['jurisdiction']}")

    else:
        agent_id = sys.argv[1]
        cfg = resolve_agent_model(agent_id)
        print(json.dumps(cfg, indent=2, default=str))
