#!/usr/bin/env python3
"""MCP federation surface + usage audit.

Answers "which MCP tools exist, and which are actually used" with evidence rather
than intuition:

  1. Enumerates the live surface of every HTTP organ (initialize ->
     notifications/initialized -> tools/list) and of the A-FORGE stdio server
     through its own CLI.
  2. Cross-references the real invocation ledger in the Hermes session store
     (messages.tool_name), which records MCP calls as mcp__<server>__<tool>.
  3. Prints per-organ tool counts, the stateless-era probe result, and the
     zero-call share.

A tool list is a claim; the ledger is evidence. Report the zero-call share as a
measurement ("unexercised"), never as a verdict ("useless") -- a rarely-called
tool may be a critical fallback, and that call belongs to F13.

Usage:
    python3 mcp_surface_usage_audit.py
    python3 mcp_surface_usage_audit.py --json /tmp/mcp_surface.json
    python3 mcp_surface_usage_audit.py --skip-aforge
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import time
import urllib.error
import urllib.request

# HTTP organs: name -> MCP endpoint. Ports move; a refused connection here is a
# finding about the federation, not a bug in this script -- confirm with
# `ss -ltnp` before reporting an organ missing.
ORGANS = {
    "arifos": "http://127.0.0.1:8088/mcp",
    "fed": "http://127.0.0.1:7074/mcp",
    "geox": "http://127.0.0.1:8081/mcp",
    "wealth": "http://127.0.0.1:18082/mcp",
    "well": "http://127.0.0.1:18083/mcp",
}

# A-FORGE exposes MCP over stdio, not HTTP. Hermes registers it under the
# server name "aforge", so its usage rows are prefixed mcp__aforge__.
AFORGE_CMD = "node /root/A-FORGE/dist/src/interfaces/mcp/cli.js serve --transport stdio"
AFORGE_NAME = "aforge"
DEFAULT_DB = "/root/.hermes/state.db"


def _sse_json(raw: str):
    """MCP servers answer with either SSE (data: lines) or plain JSON."""
    txt = raw
    if "data:" in raw:
        parts = [l[5:].strip() for l in raw.splitlines() if l.startswith("data:")]
        if parts:
            txt = parts[-1]
    return json.loads(txt)


def rpc(url, method, params=None, session=None, timeout=25):
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if session:
        req.add_header("Mcp-Session-Id", session)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return _sse_json(r.read().decode(errors="replace")), r.headers.get("Mcp-Session-Id")


def probe_http(url):
    t0 = time.time()
    init, sid = rpc(url, "initialize", {
        "protocolVersion": "2025-11-25",
        "capabilities": {},
        "clientInfo": {"name": "surface-audit", "version": "1.0"},
    })
    rpc(url, "notifications/initialized", session=sid)
    tl, _ = rpc(url, "tools/list", session=sid)
    result = (init or {}).get("result", {})
    return {
        "server": result.get("serverInfo", {}),
        "protocol": result.get("protocolVersion"),
        "tools": [t["name"] for t in tl.get("result", {}).get("tools", [])],
        "ms": int((time.time() - t0) * 1000),
    }


def probe_stateless(url):
    """2026-07-28 stateless era needs the headers AND the _meta envelope."""
    body = {
        "jsonrpc": "2.0", "id": 1, "method": "server/discover",
        "params": {"_meta": {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientCapabilities": {},
            "io.modelcontextprotocol/clientInfo": {"name": "surface-audit", "version": "1.0"},
        }},
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    req.add_header("MCP-Protocol-Version", "2026-07-28")
    req.add_header("Mcp-Method", "server/discover")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = _sse_json(r.read().decode(errors="replace"))
        return "STATELESS_OK" if "result" in d else "REJECTED"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code} (legacy handshake only)"
    except Exception as e:
        return f"ERR {type(e).__name__}"


def probe_stdio(cmd, timeout=90):
    msgs = (
        '{"jsonrpc":"2.0","id":1,"method":"initialize","params":'
        '{"protocolVersion":"2025-11-25","capabilities":{},'
        '"clientInfo":{"name":"surface-audit","version":"1.0"}}}\n'
        '{"jsonrpc":"2.0","method":"notifications/initialized"}\n'
        '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n'
    )
    p = subprocess.run(cmd, shell=True, input=msgs, capture_output=True,
                       text=True, timeout=timeout)
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("id") == 2:
            return [t["name"] for t in d.get("result", {}).get("tools", [])]
    return []


def load_usage(db_path):
    con = sqlite3.connect(db_path)
    try:
        rows = con.execute(
            "select tool_name, count(*) from messages "
            "where tool_name is not null and tool_name<>'' group by tool_name"
        ).fetchall()
    finally:
        con.close()
    return {r[0]: r[1] for r in rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write the raw surface map here")
    ap.add_argument("--db", default=DEFAULT_DB, help="Hermes session store")
    ap.add_argument("--skip-aforge", action="store_true")
    args = ap.parse_args()

    surface = {}
    print("=== live MCP surface ===")
    for name, url in ORGANS.items():
        try:
            info = probe_http(url)
        except Exception as e:
            print(f"  {name:10} UNREACHABLE  {type(e).__name__}: {str(e)[:60]}")
            surface[name] = {"error": str(e)}
            continue
        era = probe_stateless(url)
        info["stateless_2026_07_28"] = era
        surface[name] = info
        srv = info["server"]
        print(f"  {name:10} proto={info['protocol']} srv={srv.get('name')} "
              f"v={srv.get('version')} tools={len(info['tools'])} "
              f"stateless={era} {info['ms']}ms")

    if not args.skip_aforge:
        try:
            af = probe_stdio(AFORGE_CMD)
            surface[AFORGE_NAME] = {"tools": af, "transport": "stdio"}
            print(f"  {AFORGE_NAME:10} tools={len(af)} (stdio)")
        except Exception as e:
            print(f"  {AFORGE_NAME:10} PROBE FAILED  {type(e).__name__}: {str(e)[:60]}")

    try:
        usage = load_usage(args.db)
    except Exception as e:
        print(f"\nusage ledger unavailable ({type(e).__name__}): {e}")
        usage = {}

    print("\n=== surface vs usage (ledger: messages.tool_name) ===")
    print(f"  ledger holds {sum(usage.values())} calls across {len(usage)} distinct tools")
    tot = called_tot = 0
    for name, info in surface.items():
        tools = info.get("tools") or []
        if not tools:
            continue
        pre = f"mcp__{name}__"
        called = sum(1 for t in tools if usage.get(pre + t, 0) > 0)
        tot += len(tools)
        called_tot += called
        print(f"  {name:10} {len(tools):>4} tools | {called:>4} ever called | "
              f"{len(tools) - called:>4} zero-call ({100 * (len(tools) - called) // len(tools)}%)")
    if tot:
        print(f"  {'TOTAL':10} {tot:>4} tools | {called_tot:>4} ever called | "
              f"{tot - called_tot:>4} zero-call ({100 * (tot - called_tot) // tot}%)")

    if args.json:
        with open(args.json, "w") as f:
            json.dump(surface, f, indent=1)
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
