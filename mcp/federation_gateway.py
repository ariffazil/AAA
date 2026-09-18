"""
AAA Federation Gateway — MCP GUI federation for arifOS.

Single MCP endpoint → all organ tools + ui:// resources.
Raw JSON-RPC over HTTP. Bypasses FastMCP Client version incompatibility.

Host connects to :3003 → sees {organ}_{tool} + ui://{organ}/... resources.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import uuid
from typing import Any

import httpx
from fastmcp import FastMCP
from fastmcp.tools import FunctionTool

log = logging.getLogger("aaa-gateway")

# ── Organ registry ──────────────────────────────────────────────────
ORGS: dict[str, dict[str, str]] = {
    "geox": {"url": "http://127.0.0.1:8081/mcp", "desc": "GEOX — Earth Intelligence"},
    "wealth": {"url": "http://127.0.0.1:18082/mcp", "desc": "WEALTH — Capital Intelligence"},
    "well": {"url": "http://127.0.0.1:18083/mcp", "desc": "WELL — Substrate Vitality"},
    "forge": {"url": "http://127.0.0.1:7072/mcp", "desc": "A-FORGE — Execution"},
    "kernel": {"url": "http://127.0.0.1:8088/mcp", "desc": "arifOS — Constitutional Kernel"},
    "chron": {"url": "http://127.0.0.1:18102/mcp", "desc": "CHRON — Temporal Consequence Tracker"},
    # frame (:18085) and flow (:7073) don't expose /mcp HTTP endpoint
}

gateway = FastMCP(
    name="arifos-federation-gateway",
    version="2026.09.18",
    instructions=(
        "arifOS Federation Gateway — unified MCP surface. "
        "Tools: {organ}_{tool}. Resources: ui://{organ}/... "
        "DITEMPA BUKAN DIBERI."
    ),
)

_organ_status: dict[str, dict[str, Any]] = {}
_registered_tools: list[str] = []
_registered_resources: list[str] = []


# ── Raw JSON-RPC ────────────────────────────────────────────────────

# Session ID cache per organ URL (FastMCP 3.x requires mcp-session-id)
_session_ids: dict[str, str] = {}


async def _mcp_rpc(url: str, method: str, params: dict | None = None, timeout: float = 15) -> Any:
    """JSON-RPC call to MCP server via streamable-http. Tracks session IDs."""
    payload = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": method, "params": params or {}}
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream, application/json",
    }
    if url in _session_ids:
        headers["mcp-session-id"] = _session_ids[url]
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, json=payload, headers=headers)
        # Capture session ID from response
        if "mcp-session-id" in resp.headers:
            _session_ids[url] = resp.headers["mcp-session-id"]
        resp.raise_for_status()
        ct = resp.headers.get("content-type", "")
        if "text/event-stream" in ct:
            last = None
            for line in resp.text.split("\n"):
                if line.startswith("data: "):
                    last = json.loads(line[6:])
            return last.get("result", last) if last else None
        data = resp.json()
        if "error" in data:
            raise RuntimeError(f"MCP error: {data['error']}")
        return data.get("result", data)


async def _mcp_init(url: str) -> dict:
    """Initialize MCP session."""
    result = await _mcp_rpc(url, "initialize", {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "arifos-federation-gateway", "version": "2026.09.18"},
    })
    try:
        await _mcp_rpc(url, "notifications/initialized", timeout=3)
    except Exception:
        pass
    return result


# ── Dynamic tool handler factory ────────────────────────────────────

def _make_forwarding_handler(org_name: str, tool_name: str):
    """Create a handler function that forwards calls to a remote organ tool.
    Uses __annotations__ to tell FastMCP this accepts arbitrary kwargs."""

    async def _handler(arguments: dict[str, Any] = {}) -> Any:
        org_url = ORGS[org_name]["url"]
        await _mcp_init(org_url)
        result = await _mcp_rpc(org_url, "tools/call", {
            "name": tool_name,
            "arguments": arguments,
        })
        if isinstance(result, dict):
            content = result.get("content", [])
            if content and isinstance(content, list):
                texts = [c.get("text", "") for c in content if c.get("type") == "text"]
                if len(texts) == 1:
                    try:
                        return json.loads(texts[0])
                    except (json.JSONDecodeError, TypeError):
                        return texts[0]
                return texts
        return result

    _handler.__name__ = f"{org_name}_{tool_name}"
    _handler.__qualname__ = f"gateway.{org_name}_{tool_name}"
    _handler.__doc__ = f"[{org_name.upper()}] Forward to {org_name}/{tool_name}"
    _handler.__annotations__ = {"arguments": dict[str, Any], "return": Any}
    return _handler


# ── Resource handler factory ────────────────────────────────────────

def _make_resource_handler(org_name: str, uri: str):
    """Create a handler that reads a resource from a remote organ."""

    async def _handler() -> str:
        org_url = ORGS[org_name]["url"]
        await _mcp_init(org_url)
        result = await _mcp_rpc(org_url, "resources/read", {"uri": uri})
        if isinstance(result, dict):
            contents = result.get("contents", [])
            if contents:
                c = contents[0]
                return c.get("text", c.get("blob", str(c)))
        return str(result)

    _handler.__name__ = f"res_{org_name}_{uri.replace('/', '_').replace(':', '').replace('.', '_')}"
    _handler.__qualname__ = f"gateway.{_handler.__name__}"
    _handler.__doc__ = f"[{org_name.upper()}] {uri}"
    _handler.__annotations__ = {"return": str}
    return _handler


# ── Discovery ───────────────────────────────────────────────────────

async def _discover_org(org_name: str, org_config: dict[str, str]) -> None:
    url = org_config["url"]
    log.info(f"Discovering {org_name} at {url}")
    try:
        await _mcp_init(url)

        # Tools
        tools_result = await _mcp_rpc(url, "tools/list")
        tools = tools_result.get("tools", []) if isinstance(tools_result, dict) else []
        for tool in tools:
            name = tool.get("name", "")
            desc = tool.get("description", "")
            namespaced = f"{org_name}_{name}"
            handler = _make_forwarding_handler(org_name, name)
            gateway.tool(name=namespaced, description=f"[{org_name.upper()}] {desc}")(handler)
            _registered_tools.append(namespaced)

        # Resources
        try:
            res_result = await _mcp_rpc(url, "resources/list")
            resources = res_result.get("resources", []) if isinstance(res_result, dict) else []
            for res in resources:
                uri = res.get("uri", "")
                res_desc = res.get("description", "")
                res_mime = res.get("mimeType", "text/plain")
                if uri.startswith("ui://"):
                    # ui://geox/basin-explorer → ui://federation/geox/basin-explorer
                    ns_uri = uri.replace("ui://", "ui://federation/", 1)
                else:
                    ns_uri = uri
                handler = _make_resource_handler(org_name, uri)
                gateway.resource(ns_uri, description=f"[{org_name.upper()}] {res_desc}", mime_type=res_mime)(handler)
                _registered_resources.append(ns_uri)
        except Exception as e:
            log.warning(f"  {org_name}: resources failed: {e}")

        _organ_status[org_name] = {"status": "connected", "url": url, "tools": len(tools)}
        log.info(f"  ✓ {org_name}: {len(tools)} tools")

    except Exception as e:
        _organ_status[org_name] = {"status": "unreachable", "url": url, "error": str(e)[:200]}
        log.warning(f"  ✗ {org_name}: {e}")


@gateway.tool()
def federation_status() -> dict[str, Any]:
    """Federation gateway status — connected organs, tool/resource counts."""
    connected = sum(1 for s in _organ_status.values() if s.get("status") == "connected")
    return {
        "gateway": "arifos-federation-gateway",
        "version": "2026.09.18",
        "connected_organs": connected,
        "total_organs": len(ORGS),
        "total_tools": len(_registered_tools),
        "total_resources": len(_registered_resources),
        "organs": _organ_status,
        "tool_sample": _registered_tools[:15],
        "ui_resources": [r for r in _registered_resources if r.startswith("ui://")],
    }


async def _bootstrap() -> None:
    log.info("═══ Federation Gateway Bootstrap ═══")
    await asyncio.gather(*[_discover_org(n, c) for n, c in ORGS.items()], return_exceptions=True)
    connected = sum(1 for s in _organ_status.values() if s.get("status") == "connected")
    log.info(f"═══ {len(_registered_tools)} tools, {len(_registered_resources)} resources from {connected}/{len(ORGS)} organs ═══")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s", stream=sys.stderr)
    asyncio.run(_bootstrap())
    gateway.run(transport="http", host="127.0.0.1", port=3003)
