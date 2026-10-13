import json, urllib.request, sys
URL = "http://127.0.0.1:18420/mcp"
HEADERS_BASE = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": "2025-06-18",
}
def post(payload, extra_headers=None, timeout=8):
    h = dict(HEADERS_BASE)
    if extra_headers: h.update(extra_headers)
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(URL, data=data, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, {}, f"err: {e}"

# Try initialize first.
s, h, b = post({"jsonrpc":"2.0","id":"init-1","method":"initialize",
                  "params":{"protocolVersion":"2025-06-18",
                            "capabilities":{},
                            "clientInfo":{"name":"p6-fixture","version":"1.0"}}})
print("INIT HTTP", s, "body:", b[:400])
session_id = h.get("Mcp-Session-Id") or h.get("mcp-session-id") or h.get("Mcp-Session-Id")
print("session id:", session_id)
