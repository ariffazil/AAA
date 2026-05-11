---
name: mcp-live-probe
description: Probe a live MCP server's JSON-RPC endpoint directly instead of reading source code. Faster, ground-truth over code archaeology.
tags: [mcp, debug, discovery, json-rpc, fastmcp]
created: 2026-05-06
---

# MCP Live Probe — Direct JSON-RPC Discovery

## Trigger
Debugging or auditing an MCP server's live surface — especially when source code is large/truncated or you need ground-truth over code archaeology.

## Pattern
When you need to verify what an MCP server actually exposes (tools, prompts, resources, or specific method responses), **call the live endpoint directly** instead of reading source files.

## Steps

### 1. Identify the MCP endpoint
For arifOS federation containers:
```
arifOS:  http://127.0.0.1:8080/mcp
GEOX:    http://127.0.0.1:8081/mcp  (or direct HTTP if streamable-http)
WEALTH:  http://127.0.0.1:8082/mcp
WELL:    http://127.0.0.1:8083/mcp
```
For remote servers: check the server's MCP URL (not the web UI URL).

### 2. Probe with JSON-RPC
Use `execute_code` (Python stdlib) to send a direct POST:

```python
import urllib.request, json

endpoint = "http://127.0.0.1:8080/mcp"
methods = ["prompts/list", "tools/list", "resources/list"]

for method in methods:
    req = urllib.request.Request(
        endpoint,
        method='POST',
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method}).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read().decode())
        print(f"=== {method} ===")
        print(json.dumps(result, indent=2))
```

### 3. Probe a specific resource (prompts/get, resources/read)
```python
method = "prompts/get"
params = {"name": "system"}  # change per call

req = urllib.request.Request(
    endpoint,
    method='POST',
    data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
    headers={"Content-Type": "application/json", "Accept": "application/json"}
)
with urllib.request.urlopen(req, timeout=10) as r:
    print(json.dumps(json.loads(r.read().decode()), indent=2))
```

## Why This Works
- FastMCP's JSON-RPC endpoint handles `prompts/list`, `tools/list`, `resources/list`, etc. as native methods
- Source code is often split across many files, uses dynamic decorators, and can be misleading
- Live response is always ground-truth
- Round-trip is ~0.3s — faster than multi-file code search

## Pitfalls
- Streamable-http transport requires `Accept: application/json` header
- SSE responses need different parsing — use `application/json, text/event-stream` and parse SSE manually
- Timeout: 10s is sufficient for most calls
- If endpoint returns 404, the server may use a different path (check `/mcp`, `/api/mcp`, `/mcp/v1`)

## arifOS-specific
- arifOS MCP on VPS: port 8080, streamable-http transport
- Probed successfully 2026-05-06 — 8 prompts, 13 tools, 5 resources confirmed live
- REST `/prompts` (GET) is a separate layer from MCP `prompts/list` — don't confuse them

## Verification
After any MCP server change, re-probe to confirm surface matches expectations.
