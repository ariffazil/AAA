---
name: docker-sed-multiline-corruption-recovery
description: Recover from sed multiline patch corrupting a Docker container server.py — single concatenated line, duplicate patches. Use when a sed -i '.../i ...' multiline insertion breaks a Python file in a container.
version: 2026-05-05
trigger: sed -i '/^if __name__/i ...' produces a single 354-char concatenated line instead of proper multiline insertion
---

# docker-sed-multiline-corruption-recovery

## Symptom

```bash
ssh root@af-forge "docker exec well sed -i '/^if __name__/i \
from mcp.server.streamable_http import StreamableHTTPServerTransport\
_orig_check = StreamableHTTPServerTransport._check_accept_headers\
...'
```

Result: single 354-char line with all content concatenated — Python syntax error, container starts but functions break or server won't restart.

## Root Cause

`sed -i '/pattern/i TEXT' ` treats `\n` as literal characters, not newlines. Shell escaping (`\\n`) doesn't work reliably across SSH pipes. The entire patch lands on one line.

## Recovery

### Step 1 — Find the corrupted line

```bash
ssh root@af-forge "docker exec CONTAINER grep -n '_patched_check' /app/server.py"
```

If you see a single line with `from mcp.server..._orig_check...def _patched_check...StreamableHTTPServerTransport._check_accept_headers = _patched_check` concatenated — it's corrupted.

### Step 2 — Get the line number

```bash
ssh root@af-forge "docker exec CONTAINER grep -n 'mcp.server.streamable_http import StreamableHTTPServerTransport_orig_check' /app/server.py"
```

### Step 3 — Delete the corrupted line

```bash
ssh root@af-forge "docker exec CONTAINER sed -i 'CORRUPTED_LINENUMBERd' /app/server.py"
```

Example: `sed -i '3531d'` deleted the concatenated line in WELL.

### Step 4 — Verify

```bash
ssh root@af-forge "docker exec CONTAINER grep -c '_patched_check' /app/server.py"
```

Should return **2** (function def + assignment), not 3 or more.

### Step 5 — Test

```bash
ssh root@af-forge "docker restart CONTAINER && sleep 3 && curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:PORT/mcp -X POST -H 'Content-Type:application/json' -H 'Accept:application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\",\"id\":1,\"params\":{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{},\"clientInfo\":{\"name\":\"gw-test\",\"version\":\"1.0\"}}}' --max-time 5"
```

Should return `200`.

## Prevention — Use Python Instead

Python one-liner is idempotent and shell-independent:

```bash
ssh root@af-forge "python3 - <<'PYEOF'
import re
path = '/root/PROJECT/server.py'
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
    open(path, 'w').write(c)
    print('PATCHED')
else:
    print('Already patched')
PYEOF"
```

## Key Distinction — Container vs Host Source

Even after fixing the container, the **host source** may differ:
```bash
ssh root@af-forge "docker exec CONTAINER md5sum /app/server.py && md5sum /root/PROJECT/server.py"
```

WELL confirmed: container (`bff8cf...`) ≠ host source (`622f21...`). Image was built from different source.

To fix host source AND update image:
```bash
# Fix host
ssh root@af-forge "python3 - <<'PYEOF' ... PYEOF"
# Commit to running container (ephemeral — lost on next image build)
ssh root@af-forge "docker exec CONTAINER sed -i '3531d' /app/server.py"
# For permanent fix: rebuild image
ssh root@af-forge "docker build -t ghcr.io/ariffazil/well:streamable-v2 /root/WELL/"
```

## Verified Recovery

WELL: corrupted line 3531 deleted → `_patched_check` count back to 2 → HTTP 200 ✅
