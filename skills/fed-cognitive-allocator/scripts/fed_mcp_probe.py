#!/usr/bin/env python3
"""fed_mcp_probe.py — call FED (:7074) MCP tools without a full MCP client.

Usage:
  python3 fed_mcp_probe.py fed_status
  python3 fed_mcp_probe.py fed_route '{"task":"fact-check","constitutional_tier":333,"effort_level":"low"}'
  python3 fed_mcp_probe.py tools/list

Does the full handshake (initialize -> Mcp-Session-Id -> tools/call) and unwraps
FED's SSE responses: strips the `event: message` / `data: ` framing, then
double-decodes the escaped JSON inside result.content[0].text.

Verified 2026-08-08. Python stdlib only, talks to 127.0.0.1:7074.
"""
import json
import sys
import urllib.request

BASE = "http://127.0.0.1:7074/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": "2025-11-25",
}


def _post(body: dict, sid: str | None = None) -> tuple[dict, str | None]:
    headers = dict(HEADERS)
    if sid:
        headers["Mcp-Session-Id"] = sid
    req = urllib.request.Request(
        BASE, data=json.dumps(body).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode()
        new_sid = resp.headers.get("mcp-session-id")
    # strip SSE framing: "event: message\r\ndata: {...}"
    if raw.startswith("event: "):
        raw = raw.split("data: ", 1)[1].strip()
    return json.loads(raw), new_sid


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    env, sid = _post(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "fed_mcp_probe", "version": "1.0"},
            },
        }
    )
    if not sid:
        print("ERROR: no Mcp-Session-Id in initialize response", file=sys.stderr)
        return 1

    if tool in ("tools/list", "resources/list", "prompts/list"):
        method, params = tool, {}
    else:
        method, params = "tools/call", {"name": tool, "arguments": args}

    result, _ = _post(
        {"jsonrpc": "2.0", "id": 2, "method": method, "params": params}, sid
    )
    if "error" in result:
        print(json.dumps(result["error"], indent=2))
        return 1

    for item in result["result"].get("content", []):
        text = item.get("text")
        if text is None:
            continue
        try:
            print(json.dumps(json.loads(text), indent=2))
        except json.JSONDecodeError:
            print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
