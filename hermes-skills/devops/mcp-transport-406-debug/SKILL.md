---
name: mcp-transport-406-debug
description: Debug HTTP 406 from arifOS federation MCP servers — strict content negotiation vs GEOX/WELL monkey-patch pattern
tags: [mcp, federation, streamable-http, fastmcp, arifos]
severity: high
trigger:
  - HTTP 406 from arifOS MCP
  - MCP bundle transport not working
  - Accept header negotiation failure
---

# MCP Transport 406 Debug — arifOS Federation

## Problem
arifOS MCP returns HTTP 406 when OpenClaw bundle transport sends `Accept: */*` or no Accept header. Other federation servers (WEALTH, GEOX, WELL) work fine.

## Root Cause
- arifOS FastMCP uses strict content negotiation
- GEOX/WELL have monkey-patch that overrides `StreamableHTTPServerTransport._check_accept_headers` to accept any content type when `json_response=True`
- arifOS lacks this patch

## Diagnostic Command
```bash
# Test without Accept header (should 406 on arifOS, 200 on WEALTH/GEOX/WELL)
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:PORT/mcp -X POST \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'

# Test with Accept header (all should 200)
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:PORT/mcp -X POST \
  -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

## Solution Options

### Option A: openclaw.json header (preferred — no rebuild needed)
Add `headers: {"Accept": "application/json"}` to the arifOS MCP server entry in `/root/.openclaw/openclaw.json` on the VPS. Restart gateway: `hermes gateway restart`.

### Option B: Patch arifOS server.py (defense-in-depth)
```bash
ssh root@AFORGE "
python3 - <<'PYEOF'
path = '/root/arifOS/arifosmcp/server.py'
with open(path) as f: c = f.read()
patch = '''# --- Monkey-patch: Fix 406 from Accept header ---
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig_check = StreamableHTTPServerTransport._check_accept_headers
def _patched_check(self, request):
    if getattr(self, 'is_json_response_enabled', False): return True, True
    return _orig_check(self, request)
StreamableHTTPServerTransport._check_accept_headers = _patched_check
'''
if 'Monkey-patch: Fix 406' not in c:
    c = c.replace('if __name__ == \"__main__\":', patch + '\nif __name__ == \"__main__\":')
    open(path,'w').write(c)
    print('PATCHED')
else:
    print('Already patched')
PYEOF
"
```
**NOTE**: This patches HOST source. Does NOT affect running container unless image is rebuilt.

## Critical Insight: Container Image vs Host Source

**WELL example** (proves the pattern):
```
Host:   ~/WELL/server.py      line 3257  MD5: 622f21...
Container: /app/server.py    line 3531  MD5: bff8cf...
```
Container is ~274 lines longer, completely different hash. Image was built from a different/larger source tree.

**Check**:
```bash
docker inspect CONTAINER --format '{{json .Mounts}}'   # shows explicit mounts only
docker exec CONTAINER md5sum /app/server.py
md5sum /host/path/server.py   # compare
```

**If MD5s differ**: container uses image. Host edits DON'T reach container.

**Hot-patch running container** (survives restart if image tag stable):
```bash
docker exec WELL sed -i '3531d' /app/server.py   # delete corrupted concat line
docker restart WELL
```

**sed is fragile**: multiline `sed -i '/^if __name__/i ...' ` breaks due to shell escaping. Use Python instead.

**WELL sed corruption incident**: sed created a 354-char single-line concat (line 3531) that broke the Python file. Fixed by deleting the line. Verify with:
```bash
docker exec WELL grep -c '_patched_check' /app/server.py   # should be 2 (def + assignment)
```

## Ports
- arifOS: 8080
- WEALTH: 8082
- GEOX: 8081
- WELL: 8083
- OpenClaw Gateway: 18789
