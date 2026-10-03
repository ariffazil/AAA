"""
federation_ports.py — Dynamic port resolver for Hermes.

DOCTRINE: All ports flow from /root/AAA/federation/organs.yaml (SOT)
or environment variables. NEVER hardcode ports in source.

Source-of-truth chain (highest to lowest priority):
  1. os.environ (HERMES_MCP_PORT, ARIFOS_PORT, etc.)
  2. /root/AAA/federation/port-registry.json (derived from organs.yaml)
  3. /root/AAA/federation/organs.yaml (SOT)

F13 Sovereign Override: 2026-08-12.
"""

import os
import json
from pathlib import Path
from typing import Optional

# Canonical paths
REGISTRY_PATH = os.environ.get(
    "FEDERATION_PORT_REGISTRY",
    "/root/AAA/federation/port-registry.json"
)
ORGANS_SOT = os.environ.get(
    "FEDERATION_ORGANS_SOT",
    "/root/AAA/federation/organs.yaml"
)

# Cache to avoid re-reading on every call
_REGISTRY_CACHE: Optional[dict] = None


def _load_registry() -> dict:
    """Load port registry from JSON file."""
    global _REGISTRY_CACHE
    if _REGISTRY_CACHE is not None:
        return _REGISTRY_CACHE

    path = Path(REGISTRY_PATH)
    if path.exists():
        try:
            with open(path) as f:
                _REGISTRY_CACHE = json.load(f)
                return _REGISTRY_CACHE
        except (IOError, json.JSONDecodeError):
            pass

    # Fallback: return empty (caller handles missing)
    return {"components": {}, "env_vars": {}, "ports": {}}


def get_port(
    organ: str,
    *,
    default: Optional[int] = None,
    interface: str = "port",
) -> int:
    """
    Resolve port for an organ with env-first resolution.

    Resolution chain:
      1. os.environ[{ORGAN}_PORT]
      2. os.environ[FEDERATION_{ORGAN}_PORT]
      3. port-registry.json (derived from organs.yaml)
      4. `default` parameter

    Example:
        port = get_port("ARIFOS")           # 8088
        port = get_port("HERMES_MCP")       # 18086
        port = get_port("CUSTOM", default=9999)
    """
    # Env var variants
    env_keys = [
        f"{organ}_PORT",
        f"FEDERATION_{organ}_PORT",
        f"FEDERATION_{organ.upper()}_PORT",
    ]
    for key in env_keys:
        val = os.environ.get(key)
        if val and val.isdigit():
            return int(val)

    # Registry lookup
    reg = _load_registry()
    env_vars = reg.get("env_vars", {})

    def _as_port(value):
        """A null or non-numeric registry value means "not declared here".

        SCAR-PORT-REGISTRY-NULL (2026-10-03): port-registry.json legitimately
        carries nulls for organs whose port lives in another section — env_vars
        holds {"HERMES": null, "HERMES_MCP": null} while
        components.hermes.mcp_port is 18087. The previous `return int(v)` raised
        TypeError on the null, which aborted resolution BEFORE the component
        lookup below could succeed, so get_port() crashed for every organ with a
        null env_vars entry no matter which interface was requested. Skip to the
        next source instead of raising; the final fallback still decides.
        """
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    # Try direct match
    if organ in env_vars:
        _direct = _as_port(env_vars[organ])
        if _direct is not None:
            return _direct

    # Try case-insensitive
    organ_upper = organ.upper()
    for k, v in env_vars.items():
        if k.upper() == organ_upper:
            _matched = _as_port(v)
            if _matched is not None:
                return _matched

    # Component lookup (mcp_port or port)
    components = reg.get("components", {})
    for comp_id, comp_data in components.items():
        if comp_id.upper() == organ_upper:
            port = comp_data.get(interface if interface != "port" else "port")
            if port:
                return int(port)

    # Final fallback
    if default is not None:
        return default
    raise ValueError(f"Port for organ '{organ}' not found in env, registry, or default")


def get_host(organ: str, *, default: str = "127.0.0.1") -> str:
    """
    Resolve host for an organ. Defaults to localhost.
    Override via {ORGAN}_HOST env var.
    """
    env_keys = [
        f"{organ}_HOST",
        f"FEDERATION_{organ}_HOST",
    ]
    for key in env_keys:
        val = os.environ.get(key)
        if val:
            return val
    return default


def get_endpoint(organ: str, *, scheme: str = "http", path: str = "/mcp") -> str:
    """
    Build full endpoint URL for an organ's MCP service.
    """
    host = get_host(organ)
    # Try MCP port first
    port = get_port(organ + "_MCP", interface="mcp_port")
    if port is None:
        port = get_port(organ)
    return f"{scheme}://{host}:{port}{path}"


def all_organs() -> dict:
    """Return all organs from the registry."""
    return _load_registry().get("components", {})


def invalidate_cache():
    """Force re-read of registry (for hot-reload)."""
    global _REGISTRY_CACHE
    _REGISTRY_CACHE = None


if __name__ == "__main__":
    # Smoke test
    print("Federation Port Resolver — Smoke Test")
    print(f"  SOT: {REGISTRY_PATH}")
    print(f"  Organs: {len(all_organs())}")
    print()
    test_organs = ["ARIFOS", "AFORGE", "FED", "GEOX", "WEALTH", "WELL",
                   "HERMES_MCP", "HERMES_AGENT", "HERMES_A2A",
                   "POSTGRES", "REDIS", "QDRANT", "GRAPHITI", "LITELLM"]
    for org in test_organs:
        try:
            port = get_port(org)
            host = get_host(org)
            print(f"  ✓ {org:18s} → {host}:{port}")
        except ValueError as e:
            print(f"  ❌ {org:18s} → {e}")
