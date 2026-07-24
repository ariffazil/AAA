"""
model_resolver.py — Canonical model resolver for AAA federation.
Reads from AGENT_MODEL_MAP.json (THE writable SOT) via symlink at
/root/.config/federation-models.json.

Schema: providers[] + agents[] + models{} + fallback_chains[] + routing_rules[]
Array-indexed internally, exposed as dict-lookup interface.

Usage:
    from model_resolver import resolve, validate, list_agents
    cfg = resolve("opencode")
    # → {"agent_id": "opencode", "model": "deepseek/deepseek-v4-pro", "provider": "deepseek", ...}

Forged: 2026-07-24 by FORGE (000Ω). DITEMPA BUKAN DIBERI.
"""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, List, Any

CANONICAL = Path("/root/.config/federation-models.json")


def _load() -> dict:
    """Load canonical registry. Raises FileNotFoundError if missing."""
    if not CANONICAL.exists():
        raise FileNotFoundError(f"Registry missing: {CANONICAL}")
    with open(CANONICAL) as f:
        return json.load(f)


def _providers_map(reg: dict) -> Dict[str, dict]:
    return {p["provider_id"]: p for p in reg.get("providers", [])}


def _agents_map(reg: dict) -> Dict[str, dict]:
    return {a["agent_id"]: a for a in reg.get("agents", [])}


# ── PUBLIC API ──


def resolve(agent_id: str) -> dict:
    """
    Resolve an agent's full model configuration from canonical registry.

    Returns keys: agent_id, agent_name, model, provider, provider_name,
                  fallbacks, endpoint, api_key_ref, status, timeout_ms,
                  cost_daily_usd
    """
    reg = _load()
    agents = _agents_map(reg)
    providers = _providers_map(reg)

    if agent_id not in agents:
        raise KeyError(f"Agent '{agent_id}' not found. Available: {list(agents.keys())}")

    a = agents[agent_id]
    pid = a.get("primary_provider", "unknown")
    p = providers.get(pid, {})

    # Extract model keys from fallback_chain (which is list of dicts with model_key)
    fb_raw = a.get("fallback_chain", [])
    fallbacks = [f["model_key"] for f in fb_raw if isinstance(f, dict) and "model_key" in f]

    return {
        "agent_id": agent_id,
        "agent_name": a.get("agent_name", agent_id),
        "model": a["primary_model"],
        "provider": pid,
        "provider_name": p.get("provider_name", pid),
        "fallbacks": fallbacks,
        "endpoint": p.get("endpoint_url", ""),
        "api_key_ref": p.get("api_key_ref", ""),
        "status": a.get("status", "UNKNOWN") if a.get("status") else p.get("status", "UNKNOWN"),
        "timeout_ms": a.get("timeout_ms", 30000),
        "cost_daily_usd": a.get("cost_budget_daily_usd", 0),
    }


def resolve_fallback(agent_id: str, after_model: str) -> Optional[str]:
    """Get next fallback model after a given model fails."""
    cfg = resolve(agent_id)
    chain = cfg["fallbacks"]
    # Find after_model in chain (loose match)
    for i, m in enumerate(chain):
        if after_model in m or m in after_model:
            return chain[i + 1] if i + 1 < len(chain) else None
    return chain[0] if chain else None


def validate() -> dict:
    """
    Run integrity checks on the registry.
    Returns {"valid": bool, "errors": [...], "warnings": [...]}
    """
    reg = _load()
    errors = []
    warnings = []
    providers = _providers_map(reg)
    agents = _agents_map(reg)

    for aid, a in agents.items():
        prim = a.get("primary_model")
        pid = a.get("primary_provider")
        if not prim:
            errors.append(f"{aid}: missing primary_model")
        if pid not in providers:
            errors.append(f"{aid}: provider '{pid}' not in registry")

        # Validate fallback chain model keys exist somewhere
        models_list = reg.get("models", [])
        known_models = set()
        if isinstance(models_list, list):
            for m in models_list:
                if isinstance(m, dict) and "model_key" in m:
                    known_models.add(m["model_key"])
        elif isinstance(models_list, dict):
            known_models = set(models_list.keys())
        
        for fb in a.get("fallback_chain", []):
            mk = fb.get("model_key", "")
            if mk and mk not in known_models:
                # Try loose match (provider prefix may differ)
                found = any(mk in km or km in mk for km in known_models)
                if not found:
                    warnings.append(f"{aid}: fallback model '{mk}' not in registry models catalog")

    for pid, p in providers.items():
        if p.get("status") in ("DEPRECATING", "RATE_LIMITED"):
            warnings.append(f"{pid}: {p['status']} — agents using this may fail")
        if p.get("cloud_act_exposed"):
            warnings.append(f"{pid}: US jurisdiction — not for sovereign data")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "providers": len(providers),
        "agents": len(agents),
    }


def list_agents() -> List[dict]:
    """List all agents with model assignments."""
    reg = _load()
    result = []
    for a in reg.get("agents", []):
        result.append(
            {
                "agent_id": a["agent_id"],
                "name": a.get("agent_name", a["agent_id"]),
                "model": a["primary_model"],
                "provider": a.get("primary_provider", "unknown"),
                "status": a.get("status", "?"),
            }
        )
    return sorted(result, key=lambda x: x["agent_id"])


def list_providers() -> List[dict]:
    """List all providers with balance and status."""
    reg = _load()
    result = []
    for p in reg.get("providers", []):
        result.append(
            {
                "provider_id": p["provider_id"],
                "name": p.get("provider_name", p["provider_id"]),
                "status": p.get("status", "?"),
                "balance_usd": p.get("balance_usd"),
                "jurisdiction": p.get("jurisdiction", "?"),
            }
        )
    return sorted(result, key=lambda x: x["provider_id"])


# ── CLI ──

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: model_resolver.py <agent_id>")
        print("       model_resolver.py --list")
        print("       model_resolver.py --providers")
        print("       model_resolver.py --validate")
        print("       model_resolver.py --fallback <agent_id> <failed_model>")
        sys.exit(1)

    cmd = args[0]

    if cmd == "--list":
        for a in list_agents():
            print(f"{a['agent_id']:15s} → {a['model']:40s} ({a['status']})")

    elif cmd == "--providers":
        for p in list_providers():
            bal = f"${p['balance_usd']}" if p["balance_usd"] is not None else "N/A"
            print(f"{p['provider_id']:20s} {p['status']:12s} {bal:>8s}  {p['jurisdiction']}")

    elif cmd == "--validate":
        v = validate()
        print(f"valid={v['valid']} providers={v['providers']} agents={v['agents']}")
        for e in v["errors"]:
            print(f"  ❌ {e}")
        for w in v["warnings"]:
            print(f"  ⚠️  {w}")
        sys.exit(0 if v["valid"] else 1)

    elif cmd == "--fallback" and len(args) >= 3:
        fb = resolve_fallback(args[1], args[2])
        print(fb if fb else "NONE — fallback chain exhausted")

    else:
        cfg = resolve(cmd)
        print(json.dumps(cfg, indent=2, default=str))
