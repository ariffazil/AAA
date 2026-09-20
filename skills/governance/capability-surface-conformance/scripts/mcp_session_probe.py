#!/usr/bin/env python3
"""mcp_session_probe.py — enumerate and dispatch tools through the FULL MCP lifecycle.

Why this exists: a single POST with correct headers and a correct body returns
`SESSION_MISSING: Mcp-Session-Id header required` (or `Missing session ID`) on any
session-negotiating MCP server. That reads like a broken contract and gets escalated as a
defect, but the server is behaving correctly — the client skipped the handshake.

Lifecycle, in order. Skipping any step produces a response that looks like a capability failure:

    1. POST initialize            -> session id arrives in the *response header*, not the body
    2. POST notifications/initialized
    3. POST methods (tools/list, tools/call, resources/list, ...) WITH the session header

Both header gates matter and they fail at different layers:
  - missing `Accept: ... text/event-stream`  -> transport refusal before any handler runs
  - missing `Mcp-Session-Id`                  -> `SESSION_MISSING` from the server

Usage:
    python3 mcp_session_probe.py --port 18083 --list
    python3 mcp_session_probe.py --port 18083 --call well_registry_status --args '{}'
    python3 mcp_session_probe.py --scan 8088,7071,8081,18082,18083,7073

Exit codes: 0 = all requested operations succeeded, 1 = at least one failed.
No third-party imports: stdlib only, so it runs on any host in the federation.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

ACCEPT = "application/json, text/event-stream"
PROTOCOL = "2025-06-18"


def _post(url: str, payload: dict, session: str | None = None, timeout: int = 25):
    """One JSON-RPC POST. Returns (parsed_body, response_headers)."""
    headers = {"Content-Type": "application/json", "Accept": ACCEPT}
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode()
        hdrs = {k.lower(): v for k, v in resp.headers.items()}
    # SSE framing: the JSON sits on the `data:` line
    for line in raw.splitlines():
        if line.startswith("data:"):
            raw = line[5:].strip()
            break
    try:
        return json.loads(raw), hdrs
    except json.JSONDecodeError:
        return {"_unparsed": raw[:400]}, hdrs


def handshake(base: str, timeout: int = 25):
    """initialize -> session id -> notifications/initialized. Returns (session_id, error)."""
    init = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": PROTOCOL,
            "capabilities": {},
            "clientInfo": {"name": "mcp-session-probe", "version": "1"},
        },
    }
    try:
        body, hdrs = _post(base, init, timeout=timeout)
    except urllib.error.HTTPError as e:
        return None, f"initialize HTTP {e.code}: {e.read()[:200].decode(errors='replace')}"
    except Exception as e:  # noqa: BLE001 - report anything, never raise
        return None, f"initialize failed: {type(e).__name__}: {e}"

    session = hdrs.get("mcp-session-id")
    if not session:
        return None, (
            "initialize returned no Mcp-Session-Id header. Some servers are stateless and "
            f"need none; this one returned: {json.dumps(body)[:200]}"
        )

    # Step 2 is required by servers that enforce the lifecycle.
    try:
        _post(base, {"jsonrpc": "2.0", "method": "notifications/initialized"}, session, timeout)
    except Exception:  # noqa: BLE001 - a notification may legitimately return no body
        pass
    return session, None


def list_tools(base: str, session: str | None, timeout: int = 25):
    body, _ = _post(
        base, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, session, timeout
    )
    tools = body.get("result", {}).get("tools", [])
    return sorted(t.get("name", "?") for t in tools)


def call_tool(base: str, session: str | None, name: str, args: dict, timeout: int = 30):
    """Dispatch one tool and grade the CONTENT — never the bare status code."""
    body, _ = _post(
        base,
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": name, "arguments": args},
        },
        session,
        timeout,
    )
    if "error" in body:
        return False, f"JSON-RPC error: {json.dumps(body['error'])[:300]}"
    result = body.get("result", {})
    if result.get("isError"):
        text = json.dumps(result.get("content", ""))[:300]
        return False, f"isError=true: {text}"
    text = result.get("content", result)
    return True, json.dumps(text)[:600]


def probe(port: int, host: str, want_list: bool, want_call, timeout: int = 25) -> bool:
    base = f"http://{host}:{port}/mcp"
    print(f"=== {host}:{port} ===")
    session, err = handshake(base, timeout)
    if err:
        print(f"  handshake: FAILED — {err}")
        print("  NOTE: distinguish 'needs a TCP client that speaks MCP' from 'capability is dead'.")
        return False
    print(f"  session: {session}")
    if want_list:
        try:
            names = list_tools(base, session, timeout)
            print(f"  tools/list: {len(names)}")
            for n in names:
                print(f"    - {n}")
        except Exception as e:  # noqa: BLE001
            print(f"  tools/list: FAILED — {type(e).__name__}: {e}")
            return False
    ok = True
    if want_call:
        name, args = want_call
        try:
            good, text = call_tool(base, session, name, args, timeout)
        except Exception as e:  # noqa: BLE001
            good, text = False, f"{type(e).__name__}: {e}"
        print(f"  tools/call {name}: {'OK' if good else 'FAILED'}")
        print(f"    {text}")
        ok = ok and good
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, help="single port to probe")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--scan", help="comma-separated ports; probes each")
    ap.add_argument("--list", action="store_true", help="enumerate tools/list")
    ap.add_argument("--call", help="tool name to dispatch")
    ap.add_argument("--args", default="{}", help="JSON object of arguments for --call")
    ap.add_argument("--timeout", type=int, default=25)
    a = ap.parse_args()

    want_call = None
    if a.call:
        want_call = (a.call, json.loads(a.args))

    if a.scan:
        results = [probe(int(p), a.host, a.list or not want_call, want_call, a.timeout) for p in a.scan.split(",")]
        print(f"\n{sum(results)}/{len(results)} ports probed successfully")
        return 0 if all(results) else 1
    if a.port:
        return 0 if probe(a.port, a.host, a.list or not want_call, want_call, a.timeout) else 1
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
