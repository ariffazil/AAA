---
name: arifos-federation-mcp-406-fix
description: Fix arifOS MCP HTTP 406 by adding Accept header to openclaw.json, plus federation health check command
version: 2026-05-05
trigger: arifOS MCP returns HTTP 406 without Accept header; federation MCP audit
---

# arifos-federation-mcp-406-fix

## Trigger
arifOS MCP returns HTTP 406 when called without `Accept: application/json` header. Other federation servers (WEALTH, GEOX, WELL) don't have this issue because they have monkey-patches.

## Root Cause
FastMCP's `StreamableHTTPServerTransport._check_accept_headers` enforces strict content negotiation. When `json_response=True` is set, servers like WEALTH/GEOX/WELL monkey-patch this method to accept `*/*` alongside `application/json`. arifOS has the `http_app(..., json_response=True)` params but lacks the monkey-patch.

## Two Fixes

### Fix 1 — openclaw.json (recommended, immediate)
Add `Accept: application/json` header to each federation MCP entry in `/root/.openclaw/openclaw.json` under the `mcp.servers` key:

```json
"mcp": {
  "servers": {
    "arifos": {
      "url": "http://127.0.0.1:8080/mcp",
      "transport": "streamable-http",
      "headers": {
        "Accept": "application/json"
      }
    },
    "wealth": {
      "url": "http://127.0.0.1:8082/mcp",
      "transport": "streamable-http",
      "headers": {
        "Accept": "application/json"
      }
    },
    "geox": {
      "url": "http://127.0.0.1:8081/mcp",
      "transport": "streamable-http",
      "headers": {
        "Accept": "application/json"
      }
    },
    "well": {
      "url": "http://127.0.0.1:8083/mcp",
      "transport": "streamable-http",
      "headers": {
        "Accept": "application/json"
      }
    }
  }
}
```

**Critical path:** The servers dict lives under `mcp.servers`, NOT `mcpServers`. Verify with:
```bash
python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); print(list(d.get('mcp',{}).get('servers',{}).keys()))"
```

Then restart the gateway:
```bash
hermes gateway restart
# or
systemctl --user restart openclaw-gateway
```

This is the production-stable fix. No server-side changes needed.

### Fix 2 — Monkey-patch in server.py (defense-in-depth)
Add the patch immediately before `if __name__ == "__main__":` in `server.py`:

```python
# --- Monkey-patch: Fix 406 from Accept header ---
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig_check = StreamableHTTPServerTransport._check_accept_headers
def _patched_check(self, request):
    if getattr(self, 'is_json_response_enabled', False):
        return True, True
    return _orig_check(self, request)
StreamableHTTPServerTransport._check_accept_headers = _patched_check
```

**Critical gotcha:** The container's `server.py` may come from a Docker **image**, not the host source tree. Check with:
```bash
docker exec <container> md5sum /app/server.py
md5sum /root/<project>/server.py
```

If they differ, the image is built from a different source. Patching the host file won't affect the running container unless you rebuild the image.

## Federation MCP Health Check
```bash
# NOTE: Avoid piping curl to python3 in a loop — times out. Use individual calls.
for svc in arifos wealth geox well; do
  case $svc in
    arifos) url=http://127.0.0.1:8080/mcp ;;
    wealth) url=http://127.0.0.1:8082/mcp ;;
    geox)   url=http://127.0.0.1:8081/mcp ;;
    well)   url=http://127.0.0.1:8083/mcp ;;
  esac
  result=$(curl -s --max-time 8 "$url" -X POST \
    -H 'Content-Type:application/json' \
    -H 'Accept:application/json' \
    -d '{"jsonrpc":"2.0","method":"tools/list","id":2}')
  count=$(echo "$result" | python3 -c 'import json,sys; print(len(json.load(sys.stdin).get("result",{}).get("tools",[])))' 2>/dev/null || echo "ERR")
  echo "$svc: $count tools"
done
# Also check vault (non-MCP health endpoint):
curl -s --max-time 5 http://127.0.0.1:8100/health
```

## Ports
- arifOS: 8080
- GEOX: 8081
- WEALTH: 8082
- WELL: 8083
- VAULT: 8100 (non-MCP, health only)

## Related
- WELL/GEOX monkey-patch location: immediately before `if __name__ == "__main__":`
- WELL also has `mcp.http_app(..., json_response=True, stateless_http=True)` — both patch AND http_app params needed for full compatibility
- GHCR image tags: `ghcr.io/ariffazil/well:latest`, `ghcr.io/ariffazil/well:streamable-v2`
