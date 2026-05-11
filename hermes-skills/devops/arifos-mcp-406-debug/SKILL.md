---
name: arifos-mcp-406-debug
description: Debug HTTP 406 from arifOS MCP — Accept header fix for streamable-http
---

# arifOS MCP HTTP 406 Debug — Accept Header Fix

## Trigger

arifOS MCP returns `HTTP 406 Not Acceptable` when called without `Accept: application/json` header. All other arifOS federation MCP servers (GEOX, WELL, WEALTH) work fine without the header.

## Root Cause

arifOS FastMCP (unlike GEOX/WELL) does NOT have the monkey-patch that accepts `*/*` when `json_response=True`. The `_check_accept_headers` method strictly requires `application/json`.

## Diagnostic Commands

```bash
# Test which servers fail without Accept header
python3 -c "
import httpx
init = {'jsonrpc':'2.0','method':'initialize','id':1,'params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'test','version':'1.0'}}}
for name, port in [('arifOS', 8080), ('WEALTH', 8082), ('GEOX', 8081), ('WELL', 8083)]:
    r = httpx.post(f'http://127.0.0.1:{port}/mcp', json=init, timeout=5)
    d = r.json()
    info = d.get('result', {}).get('serverInfo', {})
    print(f'{name} ({port}) NO Accept: {r.status_code} {info.get(\"name\", \"FAIL\")}')"

# Check if GEOX/WELL have the monkey-patch (they do — that's why they work)
ssh root@af-forge "docker exec geox_eic grep -n '_check_accept_headers' /app/server.py"
ssh root@af-forge "docker exec well grep -n '_check_accept_headers' /app/server.py"
```

## Two Fixes

### Fix 1: Add header to openclaw.json (IMMEDIATE — already applied)

On af-forge, edit `~/.openclaw/openclaw.json`:

```json
"arifos": {
  "url": "http://127.0.0.1:8080/mcp",
  "transport": "streamable-http",
  "description": "arifOS constitutional kernel MCP",
  "headers": {
    "Accept": "application/json"
  }
}
```

Then restart: `hermes gateway restart`

### Fix 2: Apply monkey-patch to arifOS server.py (DEFENSE-IN-DEPTH)

In arifOS server.py BEFORE the `mcp.http_app()` call:

```python
# --- Monkey-patch: Fix 406 from Accept header ---
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig_check = StreamableHTTPServerTransport._check_accept_headers
def _patched_check(self, request):
    if getattr(self, 'is_json_response_enabled', False):
        return True, True  # json_response=True: accept both JSON and SSE
    return _orig_check(self, request)
StreamableHTTPServerTransport._check_accept_headers = _patched_check
```

This is already in GEOX (line ~664-671) and WELL (lines 3525-3529). arifOS is missing it.

## Relevant Files

- `~/.openclaw/openclaw.json` — OpenClaw MCP server config (af-forge)
- `/root/arifOS/arifosmcp/runtime/server.py` — arifOS MCP entrypoint
- `/root/arifOS/arifosmcp/server.py` — canonical server

## CRITICAL: Container Filesystem Topology Check BEFORE Patching

**The #1 trap:** Editing `/root/arifOS/arifosmcp/server.py` on the host does NOTHING if the container runs from an image without a bind mount.

Always verify first:
```bash
# Check if container has host mounts (bind mounts = host edits reach container; image = they don't)
docker inspect arifosmcp --format '{{json .Mounts}}' | python3 -m json.tool
docker inspect arifosmcp --format '{{.Config.Image}}'
```

**If Mounts = `[]` and Image = `ghcr.io/ariffazil/arifos:de038a0f`** → Container runs from image, NO host path is mounted. Host file edits are invisible to the container.

**If Mounts contains a bind mount** (e.g., `/root/arifOS/arifosmcp:/app`) → Host edits reach the container.

## Three Ways to Patch arifOS

### Option A: openclaw.json header workaround (ALREADY APPLIED — no further action needed)
Best for OpenClaw→arifOS transport. Add `headers: {"Accept": "application/json"}` to the arifOS entry in openclaw.json. Survives container restarts. Applied 2026-05-05.

### Option B: Patch running container filesystem directly (IMMEDIATE, survives restarts)
Use `docker exec` to patch the running container's /app/server.py:
```bash
ssh root@af-forge "docker exec arifosmcp python3 - <<'PYEOF'
import re
path = '/app/server.py'
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
PYEOF"
```
Then: `ssh root@af-forge "docker restart arifosmcp"`

### Option C: Rebuild image (PERMANENT, proper fix)
Rebuild the arifOS image with the patch baked in. Then `docker pull` + restart.

## sed Multiline Gotcha — Use Python Instead

❌ **NEVER use sed for multiline patches** — the `sed -i '/^if __name__/i\' approach breaks because:
- Shell `\n` escaping is inconsistent between sh/bash/zsh
- sed treats the entire replacement as one line with literal `\n` characters
- Results in a 500+ character syntactic disaster on a single line, crashing the server

✅ **Always use Python heredoc via `docker exec`** for multiline in-container edits.

If a sed corruption happens, restore with:
```bash
ssh root@af-forge "docker exec <container> git -C /app checkout server.py"
ssh root@af-forge "docker restart <container>"
```

## Apply Monkey-Patch to arifOS (SSH one-liner — for Option B)

Paste directly to relay to af-forge:

```bash
ssh root@af-forge "docker exec arifosmcp python3 - <<'PYEOF'
import re
path = '/app/server.py'
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
PYEOF"
```

Then restart:
```bash
ssh root@af-forge "docker restart arifosmcp && docker logs --tail 5 arifosmcp"
```

## Verify Patch in Each Server

```bash
# GEOX — patch is at line ~664-671 (before __main__)
ssh root@af-forge "docker exec geox_eic sed -n '660,695p' /app/server.py"

# WELL — patch is at line ~3520-3528 (before __main__)
ssh root@af-forge "docker exec well sed -n '3510,3535p' /app/server.py"

# arifOS — after patching, verify:
ssh root@af-forge "grep -n '_check_accept_headers' /root/arifOS/arifosmcp/server.py"
```

## Session Context

Found during: OpenClaw MCP bundle audit 2026-05-05, arifOS 8080 returning HTTP 406 while GEOX 8081, WELL 8083, WEALTH 8082 all worked.

**Confirmed 2026-05-05:**
- Fix 1 (openclaw.json header) → APPLIED and verified working (`curl ... arifOS → 200`)
- Fix 2 (monkey-patch in arifOS server.py) → NOT YET applied to container; openclaw.json workaround is sufficient for OpenClaw transport
- WEALTH, GEOX, WELL all have monkey-patch — verified via `grep -n '_check_accept_headers' /app/server.py`
- WELL monkey-patch: lines 3525-3529; `http_app` call: line 3537 (`json_response=True, stateless_http=True`)
- arifOS has `http_app(..., json_response=True, stateless_http=True)` on line 266 but NO monkey-patch in image
- openclaw.json structure: top-level key is `mcp`, servers are at `mcp.servers.<name>`
- WEALTH Route anomaly: line 4613 declares `methods=["GET", "POST"]` but GET returns 405 in practice — route supports GET declaration is misleading, MCP is POST-only in practice

**Key discovery (2026-05-05):** Container filesystem != host filesystem. `docker inspect <container> --format '{{json .Mounts}}'` and `{{.Config.Image}}` must be checked before assuming host file edits reach the container. arifOS container uses image `ghcr.io/ariffazil/arifos:de038a0f` with no mounts — host file edits are invisible.

**Critical finding (2026-05-05):** Host source and container image can be ENTIRELY DIFFERENT files — not just different versions of the same file. `diff <(docker exec <cnt> cat /app/server.py | sed -n '3240,3280p') <(sed -n '3240,3280p' /root/WELL/server.py)` revealed WELL container's `/app/server.py` has completely different code at the same line range (274 line offset delta: host `if __name__` at 3257, container at 3531). This means the image was built from a different/larger source tree than what exists on the host.

**Mount audit command (2026-05-05):** `docker inspect well --format '{{range .Mounts}}{{.Source}} → {{.Destination}}{{"\n"}}{{end}}'` showed only ONE mount: `/root/WELL/state.json → /app/state.json`. `server.py` is NOT mounted — container runs image layer for that file.

**Diagnostic: Compare host source vs container filesystem:**
```bash
# Check container Mounts and Image first
docker inspect <container> --format '{{json .Mounts}}' | python3 -m json.tool
docker inspect <container> --format '{{.Config.Image}}'

# Side-by-side diff of same line range (host vs container)
diff <(docker exec <container> cat /app/server.py | sed -n '3240,3280p') <(sed -n '3240,3280p' /root/WELL/server.py)

# Check MD5 of host vs container file
md5sum /root/WELL/server.py
docker exec well md5sum /app/server.py

# WELL: host has __main__ at line 3257; container has it at 3531
# If MD5s differ AND line counts differ — the files are completely different source trees
```

**WEALTH Route anomaly (2026-05-05):** `wealth-organ` Route at line 4613: `Route("/mcp", legacy_mcp_handler, methods=["GET", "POST"])`. In practice GET returns 405 — the handler rejects it even though the route declaration says GET+POST. MCP is POST-only regardless of the route declaration.

**sed corruption recovery (2026-05-05):** If sed `-i` multiline insert corrupts a file (results in a 500+ char single concatenated line), restore with: `docker exec <container> git -C /app checkout server.py`. Then re-apply patch using Python heredoc approach.

**Key diagnostic (run on af-forge):**
```bash
# Check container filesystem topology
docker inspect arifosmcp --format '{{json .Mounts}}' | python3 -m json.tool
docker inspect arifosmcp --format '{{.Config.Image}}'

# Check which servers have the monkey-patch
docker exec geox_eic grep -n '_patched_check' /app/server.py
docker exec well grep -n '_patched_check' /app/server.py
docker exec arifosmcp grep -n '_patched_check' /app/server.py  # returns nothing = missing in container

# Probe MCP servers directly (with and without Accept header) — httpx test
python3 << 'EOF'
import httpx, asyncio
async def test():
    init = {'jsonrpc':'2.0','method':'initialize','id':1,'params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'test','version':'1.0'}}}
    for name, port in [('arifOS', 8080), ('WEALTH', 8082), ('GEOX', 8081), ('WELL', 8083)]:
        no_accept = httpx.post(f'http://127.0.0.1:{port}/mcp', json=init, headers={'Content-Type':'application/json'}, timeout=5).status_code
        with_accept = httpx.post(f'http://127.0.0.1:{port}/mcp', json=init, headers={'Content-Type':'application/json','Accept':'application/json'}, timeout=5).status_code
        print(f'{name}: no Accept={no_accept}, with Accept={with_accept}')
asyncio.run(test())
EOF

# List all MCP servers and tool counts
for svc in arifos wealth-organ geox_eic well; do
  case $svc in arifos) port=8080; url=http://127.0.0.1:8080/mcp ;; wealth-organ) port=8082; url=http://127.0.0.1:8082/mcp ;; geox_eic) port=8081; url=http://127.0.0.1:8081/mcp ;; well) port=8083; url=http://127.0.0.1:8083/mcp ;; esac
  init=$(curl -s -o /dev/null -w '%{http_code}' $url -X POST -H 'Content-Type:application/json' -H 'Accept:application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\",\"id\":1,\"params\":{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{},\"clientInfo\":{\"name\":\"c\",\"version\":\"1\"}}}' --max-time 5)
  tools=$(curl -s $url -X POST -H 'Content-Type:application/json' -H 'Accept:application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"tools/list\",\"id\":2}' --max-time 5 | python3 -c 'import json,sys; print(len(json.load(sys.stdin).get("result",{}).get("tools",[])))')
  echo "$svc: $init / $tools tools"
done
```
