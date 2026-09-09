#!/usr/bin/env python3
"""
AAA MCP shim — bridges MCP stdio (JSON-RPC) to the AAA intelligence routing
organ on 127.0.0.1:3001.

AAA is DISPLAY_ONLY — it shows state, queues A2A, aggregates organ cards.
Never judges. Never executes. Never writes VAULT999.

Tools:
  aaa_health              — GET /health: organ health + apex scalars
  aaa_agent_card          — GET /.well-known/agent-card.json: A2A agent card
  aaa_federation_manifest — GET /.well-known/arifos-federation.json: federation state
  aaa_discovery           — GET /.well-known/a2a-discovery.json: A2A discovery contract

Stdlib only. MCP stdio = newline-delimited JSON-RPC 2.0.
"""

import json
import sys
import urllib.request
import urllib.error

AAA_HOST = "127.0.0.1"
AAA_PORT = 3001
PROTOCOL_VERSION = "2024-11-05"

TOOLS = [
    {
        "name": "aaa_health",
        "description": (
            "AAA organ health — identity, deployment status, apex scalars "
            "(G, C_dark, W3), vault chain, version. Read-only. DISPLAY_ONLY authority."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "aaa_agent_card",
        "description": (
            "A2A agent card for the AAA gateway — capabilities, interfaces, "
            "extensions, supported protocols. Discovery surface for federation agents."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "aaa_federation_manifest",
        "description": (
            "Federation manifest — registered agents, organs, topology. "
            "Shows who is in the federation and how they connect."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "aaa_discovery",
        "description": (
            "A2A discovery contract — protocol version, auth requirements, "
            "available endpoints. Used by agents to discover AAA capabilities."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
]


def aaa_get(path: str) -> dict:
    """HTTP GET to AAA daemon via urllib."""
    url = f"http://{AAA_HOST}:{AAA_PORT}{path}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": str(e), "status_code": e.code}


def call_tool(name: str, args: dict) -> dict:
    if name == "aaa_health":
        return aaa_get("/health")
    if name == "aaa_agent_card":
        return aaa_get("/.well-known/agent-card.json")
    if name == "aaa_federation_manifest":
        return aaa_get("/.well-known/arifos-federation.json")
    if name == "aaa_discovery":
        return aaa_get("/.well-known/a2a-discovery.json")
    raise ValueError(f"unknown tool: {name}")


def respond(msg_id, result=None, error=None):
    out = {"jsonrpc": "2.0", "id": msg_id}
    if error is not None:
        out["error"] = error
    else:
        out["result"] = result
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = msg.get("method", "")
        msg_id = msg.get("id")

        if method == "initialize":
            respond(
                msg_id,
                {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "aaa", "version": "2026.08.25"},
                },
            )
        elif method == "ping":
            respond(msg_id, {})
        elif method and method.startswith("notifications/"):
            continue
        elif method == "tools/list":
            respond(msg_id, {"tools": TOOLS})
        elif method == "tools/call":
            params = msg.get("params", {})
            tname = params.get("name", "")
            targs = params.get("arguments", {}) or {}
            try:
                result = call_tool(tname, targs)
                respond(
                    msg_id,
                    {
                        "content": [
                            {"type": "text", "text": json.dumps(result, indent=2)}
                        ],
                        "isError": False,
                    },
                )
            except Exception as e:
                respond(
                    msg_id,
                    {
                        "content": [{"type": "text", "text": f"AAA error: {e}"}],
                        "isError": True,
                    },
                )
        else:
            if msg_id is not None:
                respond(
                    msg_id,
                    error={"code": -32601, "message": f"method not found: {method}"},
                )


if __name__ == "__main__":
    main()
