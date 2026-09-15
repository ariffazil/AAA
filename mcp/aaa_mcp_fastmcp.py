"""
AAA MCP Server — FastMCP (replaces stdio shim aaa-mcp.py)

AAA is DISPLAY_ONLY — it shows state, queues A2A, aggregates organ cards.
Never judges. Never executes. Never writes VAULT999.

Tools:
  aaa_health              — GET /health: organ health + apex scalars
  aaa_agent_card          — GET /.well-known/agent-card.json: A2A agent card
  aaa_federation_manifest — GET /.well-known/arifos-federation.json: federation state
  aaa_discovery           — GET /.well-known/a2a-discovery.json: A2A discovery contract

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from typing import Any

from fastmcp import FastMCP

AAA_HOST = "127.0.0.1"
AAA_PORT = 3001

mcp = FastMCP(
    name="aaa-mcp",
    version="2026.09.14",
    instructions=(
        "AAA — Intelligence routing organ for arifOS Federation. "
        "Authority: DISPLAY_ONLY. Shows state, queues A2A, aggregates organ cards. "
        "Never judges. Never executes. Never writes VAULT999."
    ),
)


def _aaa_get(path: str) -> dict[str, Any]:
    """HTTP GET to AAA daemon."""
    url = f"http://{AAA_HOST}:{AAA_PORT}{path}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": str(e), "status_code": e.code}
    except urllib.error.URLError as e:
        return {"error": f"AAA daemon unreachable: {e.reason}"}


@mcp.tool()
def aaa_health() -> dict[str, Any]:
    """AAA organ health — identity, deployment status, apex scalars
    (G, C_dark, W3), vault chain, version. Read-only. DISPLAY_ONLY authority."""
    return _aaa_get("/health")


@mcp.tool()
def aaa_agent_card() -> dict[str, Any]:
    """A2A agent card for the AAA gateway — capabilities, interfaces,
    extensions, supported protocols. Discovery surface for federation agents."""
    return _aaa_get("/.well-known/agent-card.json")


@mcp.tool()
def aaa_federation_manifest() -> dict[str, Any]:
    """Federation manifest — registered agents, organs, topology.
    Shows who is in the federation and how they connect."""
    return _aaa_get("/.well-known/arifos-federation.json")


@mcp.tool()
def aaa_discovery() -> dict[str, Any]:
    """A2A discovery contract — protocol version, auth requirements,
    available endpoints. Used by agents to discover AAA capabilities."""
    return _aaa_get("/.well-known/a2a-discovery.json")


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=3002)
