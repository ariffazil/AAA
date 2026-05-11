---
name: fastmcp-streamable-http-406-fix
description: Fix FastMCP 3.2.4 streamable-http returning HTTP 406 on valid JSON-RPC POSTs due to Accept header rejection
trigger: HTTP 406 from MCP server using streamable-http transport
---

# FastMCP 3.2.4 streamable-http 406 Bug — Accept Header Rejection

## Trigger

MCP client POSTs to `http://host:port/mcp` with:
```
Content-Type: application/json
Accept: application/json
```

Server returns `HTTP 406 Not Acceptable`, even though the request is perfectly valid JSON-RPC.

## Root Cause

FastMCP 3.2.4's `StreamableHTTPServerTransport._check_accept_headers` enforces strict Accept header validation. When `is_json_response_enabled=False` (the default), it rejects any Accept header that doesn't match its internal criteria, causing 406 on otherwise valid requests.

## Solution

Two-part fix required simultaneously:

### Part 1 — http_app flags

```python
app = mcp.http_app(
    path="/mcp",
    transport="streamable-http",
    json_response=True,      # enables is_json_response_enabled
    stateless_http=True,     # required for remote MCP
)
```

### Part 2 — Monkey-patch before `if __name__ == "__main__":`

```python
from starlette.requests import HTTPConnection
from modelcontextprotocol.server import StreamableHTTPServerTransport

_orig_check = StreamableHTTPServerTransport._check_accept_headers

def _patched_check(self, request: HTTPConnection):
    if getattr(self, 'is_json_response_enabled', False):
        return True, True
    return _orig_check(self, request)

StreamableHTTPServerTransport._check_accept_headers = _patched_check
```

Both parts are required. Part 1 sets the flag; Part 2 makes the transport respect it.

## Verified Servers

| Server | Version | Transport | Status |
|--------|---------|-----------|--------|
| GEOX | FastMCP 3.2.4 | streamable-http | ✅ Fixed |
| WELL | FastMCP 3.2.4 | streamable-http | ✅ Fixed |
| WEALTH | FastMCP ? | streamable-http | ✅ Fixed (entrypoint override) |

## Key Insight

**`arifOS` DOES need this fix.** Confirmed 2026-05-05: arifOS returns HTTP 406 without `Accept: application/json` header, same as WEALTH/GEOX/WELL. It has `http_app(..., json_response=True, stateless_http=True)` with explicit `transport=` but lacks the monkey-patch. Fix: openclaw.json `Accept: application/json` header workaround (production-stable), or monkey-patch arifOS server.py for defense-in-depth.

| Server | http_app json_response | Monkey-patch | Needs Fix? |
|--------|----------------------|--------------|------------|
| WEALTH | ✅ | ✅ | No (both) |
| GEOX | ✅ | ✅ | No (both) |
| WELL | ✅ | ✅ | No (both) |
| arifOS | ✅ | **❌** | **Yes — needs patch OR openclaw.json workaround** |

**Confirmed 2026-05-05:**
- `curl` without Accept → arifOS 406, WEALTH 200
- `curl` with `Accept: application/json` → arifOS 200, WEALTH 200
- WELL container MD5 (`bff8cf...`) ≠ host source MD5 (`622f21...`) — image built from different source
- WELL image tags `latest` and `streamable-v2` aligned to same digest `sha256:330426...` after push

## Verification

```bash
# POST probe — should return tools list, not 406
curl -s -X POST http://127.0.0.1:PORT/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## Gotcha

Patching the running container (`/app/server.py`) does NOT update the source file (`~/WELL/server.py`). Both must be patched separately. Use `md5sum` to verify source vs container match after patching.

## Source vs Container

| Environment | File Path | How to Patch |
|-------------|-----------|--------------|
| Container | `/app/server.py` | `docker exec CONTAINER sed -i ...` or `docker exec CONTAINER python3 -c ...` |
| Source | `~/WELL/server.py` | `patch` tool or direct file edit |

Rebuild image after source patching: `docker build -t ghcr.io/ariffazil/well:streamable-v2 ~/WELL/`
