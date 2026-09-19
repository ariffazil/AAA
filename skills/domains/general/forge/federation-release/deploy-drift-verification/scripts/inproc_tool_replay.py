#!/usr/bin/env python3
"""In-process tool replay: is the failing tool the CODE, or the PROCESS?

Registers a tool module on a FRESH server instance and invokes the named tools through the
framework's own ``call_tool`` -- the same path the live MCP boundary takes.

    passes here, fails live  ->  PROCESS_STALE  (reload needed; the committed code is fine)
    fails here too           ->  CODE_DEFECT    (traceback, no production action spent)

Run with the SERVICE's interpreter, the repo root on sys.path, from a neutral cwd:

    PYTHONPATH=<repo-root> <repo>/.venv/bin/python3 inproc_tool_replay.py \
        --server-module <pkg>.server \
        --server-factory create_mcp_server \
        --register <pkg>.tools.<mod>:register_<feature> \
        --calls calls.json

calls.json:
    [{"tool": "<name>", "args": {"mode": "..."}},
     {"tool": "<known-good-sibling>", "args": {}}]        <- the control call: keep it

Mirror the service's framework import: ``fastmcp.FastMCP`` and ``mcp.server.fastmcp.FastMCP``
share a name but not a decorator signature, so a probe that guesses raises during registration
and the harness error looks like a defect in the module under test. Check the entry module:

    grep -n 'FastMCP\|from mcp\|import mcp' <service-entry>.py
"""
from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import sys


def _load(spec: str):
    """Resolve 'module' or 'module:attribute'."""
    mod_name, _, attr = spec.partition(":")
    mod = importlib.import_module(mod_name)
    return getattr(mod, attr) if attr else mod


async def _run(mcp, calls):
    out = []
    for call in calls:
        tool, args = call["tool"], call.get("args", {})
        entry = {"tool": tool, "args": args}
        try:
            res = await mcp.call_tool(tool, args)
            payload = res[1] if isinstance(res, tuple) else res
            entry["ok"] = True
            entry["type"] = type(payload).__name__
            if isinstance(payload, dict):
                entry["top_keys"] = sorted(payload)[:10]
        except Exception as exc:  # noqa: BLE001 - the failure IS the finding
            entry["ok"] = False
            entry["error"] = f"{type(exc).__name__}: {exc}"[:500]
        out.append(entry)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--server-module", required=True, help="module holding the server factory")
    ap.add_argument("--server-factory", required=True, help="callable returning the server instance")
    ap.add_argument("--register", action="append", default=[],
                    help="module:callable binding tools onto the server (repeatable)")
    ap.add_argument("--calls", help="JSON file (or inline JSON) of [{tool, args}, ...]")
    ap.add_argument("--import-only", action="store_true",
                    help="register without calling; proves the module imports under THIS interpreter")
    args = ap.parse_args()

    factory = _load(f"{args.server_module}:{args.server_factory}")
    mcp = factory()
    for spec in args.register:
        _load(spec)(mcp)

    if args.import_only or not args.calls:
        print(json.dumps({"registered": args.register, "import_ok": True}, indent=2))
        return 0

    if args.calls.endswith(".json"):
        with open(args.calls) as fh:
            calls = json.load(fh)
    else:
        calls = json.loads(args.calls)

    results = asyncio.run(_run(mcp, calls))
    print(json.dumps(results, indent=2, default=str))
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
