#!/usr/bin/env python3
"""
mcp_client.py — minimal MCP streamable-http client for the compositor's
producer adapters. Honors the GEOX Phase A1 lifecycle gate
(initialize → notifications/initialized → tools/call).
"""
import json, urllib.request, urllib.error, os

DEFAULT_ENDPOINT = "http://127.0.0.1:8081/mcp"


class MCPClient:
    def __init__(self, endpoint=DEFAULT_ENDPOINT, client_name="aforge-compositor"):
        self.endpoint = endpoint
        self.sid = None
        self._seq = 0
        self.client_name = client_name

    def _post(self, payload, timeout=30):
        data = json.dumps(payload).encode()
        hdrs = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.sid:
            hdrs["mcp-session-id"] = self.sid
        req = urllib.request.Request(self.endpoint, data=data, headers=hdrs, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode()
            if resp.headers.get("mcp-session-id"):
                self.sid = resp.headers["mcp-session-id"]
            return json.loads(body) if body else {}

    def initialize(self):
        self._seq += 1
        r = self._post({
            "jsonrpc": "2.0", "id": self._seq, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": self.client_name, "version": "0.1"}},
        }, timeout=10)
        # notify initialized (server returns 202 no body)
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"}, timeout=10)
        return r

    def list_tools(self):
        self._seq += 1
        r = self._post({"jsonrpc": "2.0", "id": self._seq, "method": "tools/list"}, timeout=15)
        return [t["name"] for t in r.get("result", {}).get("tools", [])]

    def call(self, name, arguments=None, timeout=120):
        self._seq += 1
        r = self._post({
            "jsonrpc": "2.0", "id": self._seq, "method": "tools/call",
            "params": {"name": name, "arguments": arguments or {}},
        }, timeout=timeout)
        res = r.get("result", {})
        texts = [b.get("text", "") for b in res.get("content", []) if b.get("type") == "text"]
        joined = "\n".join(texts)
        try:
            parsed = json.loads(joined)
        except Exception:
            parsed = {"raw": joined}
        return {"is_error": res.get("isError", False), "data": parsed}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--tools", action="store_true")
    ap.add_argument("--call")
    ap.add_argument("--args", default="{}")
    a = ap.parse_args()
    c = MCPClient()
    c.initialize()
    if a.tools:
        print(json.dumps(c.list_tools(), indent=2))
    if a.call:
        print(json.dumps(c.call(a.call, json.loads(a.args)), indent=2)[:3000])
