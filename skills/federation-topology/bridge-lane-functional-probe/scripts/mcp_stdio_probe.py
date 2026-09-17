#!/usr/bin/env python3
"""Prove an MCP stdio server is FUNCTIONAL, not merely configured.

Spawns the launcher, runs the JSON-RPC `initialize` handshake, then `tools/list`,
and prints server name/version plus every tool name. Exits non-zero on any failure
so it can gate a report.

Usage:
  python3 mcp_stdio_probe.py -- python3 /path/to/server-mcp.py
  python3 mcp_stdio_probe.py --cmd /opt/venv/bin/python -- /path/to/server.py --transport stdio
  python3 mcp_stdio_probe.py --timeout 40 -- npx -y some-mcp

Exit codes: 0 tools present | 1 handshake/parse failure | 2 bad argv | 3 initialized but zero tools
"""

import argparse
import json
import subprocess
import sys

PROTOCOL_VERSION = "2024-11-05"


def main() -> int:
    ap = argparse.ArgumentParser(description="MCP stdio handshake + tools/list probe")
    ap.add_argument("cmd", nargs=argparse.REMAINDER, help="launcher argv (after --)")
    ap.add_argument("--cmd", dest="interp", default=None, help="interpreter/binary to prepend")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--quiet", action="store_true", help="print only the OK/FAIL line")
    args = ap.parse_args()

    argv = list(args.cmd)
    if argv and argv[0] == "--":
        argv = argv[1:]
    if args.interp:
        argv = [args.interp] + argv
    if not argv:
        print("FAIL no_command", file=sys.stderr)
        return 2

    proc = subprocess.Popen(
        argv,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    def rpc(req_id, method, params=None):
        msg = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            msg["params"] = params
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()
        return json.loads(proc.stdout.readline())

    try:
        init = rpc(1, "initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "lane-probe", "version": "1"},
        })
        info = init.get("result", {}).get("serverInfo", {})
        name, version = info.get("name", "?"), info.get("version", "?")

        try:
            proc.stdin.write(json.dumps(
                {"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
            proc.stdin.flush()
        except Exception:
            pass  # some servers reject the notification; tools/list still works

        listed = rpc(2, "tools/list", {})
        tools = listed.get("result", {}).get("tools", [])
        names = sorted(t.get("name", "<unnamed>") for t in tools)

        if args.quiet:
            print("OK %s %s tools=%d" % (name, version, len(names)))
        else:
            print("HANDSHAKE_OK  %s %s" % (name, version))
            print("TOOLS (%d): %s" % (len(names), ", ".join(names)))
        return 0 if names else 3

    except json.JSONDecodeError as exc:
        print("FAIL not_jsonrpc (%s)" % exc, file=sys.stderr)
        print("stderr: " + (proc.stderr.read() or "")[:800], file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - report whatever killed the handshake
        print("FAIL %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        try:
            print("stderr: " + (proc.stderr.read() or "")[:800], file=sys.stderr)
        except Exception:
            pass
        return 1
    finally:
        proc.kill()


if __name__ == "__main__":
    sys.exit(main())
