#!/usr/bin/env python3
"""
Minimal claim-ledger-mcp client — thin async wrapper over the MCP streamable-http
transport so other federation organs can call the ledger without reimplementing
the client.

    from client import LedgerClient
    async with LedgerClient() as L:
        print(await L.trace("2026-09-15-syed-mokhtar-bank-consolidation-c01"))

CLI:
    python client.py trace <claim_id>
    python client.py stats
    python client.py verify
"""

import asyncio
import json
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

DEFAULT_ENDPOINT = "http://127.0.0.1:8791/mcp"


class LedgerClient:
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT):
        self.endpoint = endpoint
        self._cm = None
        self._sess_cm = None
        self.session = None

    async def __aenter__(self):
        self._cm = streamablehttp_client(self.endpoint)
        read, write, _ = await self._cm.__aenter__()
        self._sess_cm = ClientSession(read, write)
        self.session = await self._sess_cm.__aenter__()
        await self.session.initialize()
        return self

    async def __aexit__(self, *exc):
        await self._sess_cm.__aexit__(*exc)
        await self._cm.__aexit__(*exc)

    async def call(self, tool: str, **args) -> dict:
        res = await self.session.call_tool(tool, args)
        if getattr(res, "structuredContent", None):
            out = res.structuredContent
            return out["result"] if isinstance(out, dict) and set(out) == {"result"} else out
        for blk in res.content:
            if getattr(blk, "type", "") == "text":
                try:
                    return json.loads(blk.text)
                except json.JSONDecodeError:
                    return {"_raw": blk.text}
        return {}

    # convenience wrappers — one per tool
    def init(self):                       return self.call("claim_ledger_init")
    def register_artifact(self, **kw):    return self.call("claim_artifact_register", **kw)
    def record(self, **kw):               return self.call("claim_record", **kw)
    def verify(self, **kw):               return self.call("claim_verify", **kw)
    def get(self, claim_id):              return self.call("claim_get", claim_id=claim_id)
    def trace(self, claim_id):            return self.call("claim_trace", claim_id=claim_id)
    def list(self, **kw):                 return self.call("claim_list", **kw)
    def stats(self):                      return self.call("claim_ledger_stats")
    def export_brief(self, brief_id):     return self.call("claim_export_brief", brief_id=brief_id)
    def verify_chain(self, **kw):         return self.call("claim_ledger_verify_chain", **kw)


async def _cli():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    async with LedgerClient() as L:
        if cmd == "trace":
            out = await L.trace(sys.argv[2])
        elif cmd == "stats":
            out = await L.stats()
        elif cmd == "verify":
            out = await L.verify_chain()
        else:
            out = {"error": f"unknown command {cmd!r}",
                   "usage": "client.py [stats|verify|trace <claim_id>]"}
        print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(_cli())
