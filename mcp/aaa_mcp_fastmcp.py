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


# -- READ-ONLY KILL-SWITCH (2026-10-24 - kimi-code/FI-008 - sovereign directive) --
# aaa-mcp (:3002) is a READ-ONLY manifest surface. Any tool outside the
# read-class allowlist is REFUSED at startup - fail closed. Registry mutations
# (agent register, lane change) belong to the F13 signing lane (:18900) +
# judge/seal - NEVER MCP, NEVER A2A. F8 LAW: capability != authority.
READ_CLASS_ALLOWLIST = frozenset(
    {
        "aaa_health",
        "aaa_agent_card",
        "aaa_federation_manifest",
        "aaa_discovery",
    }
)


def _assert_read_class(tool_names) -> bool:
    """Fail-closed audit: every registered tool must be read-class."""
    offenders = sorted(n for n in tool_names if n not in READ_CLASS_ALLOWLIST)
    if offenders:
        raise RuntimeError(
            "READ-ONLY KILL-SWITCH: aaa-mcp (:3002) refuses non-read-class "
            "tool(s): "
            + ", ".join(offenders)
            + " - mutation belongs to the F13 signing lane, never MCP"
        )
    return True


def _kill_switch_audit() -> bool:
    """Enumerate registered FastMCP tools and enforce the allowlist."""
    manager = getattr(mcp, "_tool_manager", None)
    tools = getattr(manager, "_tools", None)
    if not isinstance(tools, dict):
        raise RuntimeError(
            "READ-ONLY KILL-SWITCH: cannot enumerate registered tools - "
            "fail closed (FastMCP internals changed?)"
        )
    return _assert_read_class(set(tools.keys()))


if __name__ == "__main__":
    _kill_switch_audit()
    mcp.run(transport="http", host="127.0.0.1", port=3002)
