---
name: caddyfile-ro-bind-mount-patch
description: How to patch a Caddyfile when it is bind-mounted read-only into the Caddy container
tags: [caddy, docker, bind-mount, ops]
last_updated: 2026-05-01
---

# Skill: Patching Caddyfile When Bind-Mounted Read-Only

## Critical Pre-check: Which Caddyfile?

**There are TWO Caddyfiles on the VPS.** Only ONE matters:

| File | Used by Container? | Purpose |
|------|-------------------|---------|
| `/root/arifOS/Caddyfile` | ✅ YES — mounted to `/etc/caddy/Caddyfile:ro` | Production routing |
| `/root/compose/Caddyfile` | ❌ NO — local development copy | Local reference |

**Before patching anything, verify which file the container actually reads:**
```bash
docker inspect caddy --format '{{json .Mounts}}' | python3 -m json.tool | grep -E "Caddyfile|Source|Destination"
```

Patching `/root/compose/Caddyfile` does NOTHING to the running container. Always patch `/root/arifOS/Caddyfile`.

## Symptom
- `docker exec caddy cat /etc/caddy/Caddyfile` shows OLD content after `patch` reports success
- `docker cp <file> caddy:/etc/caddy/Caddyfile` fails with: `unlinkat ... device or resource busy`
- Caddy continues serving stale config even after `docker exec caddy caddy reload`
- Root cause: the file is mounted `ro` from host `/root/arifOS/Caddyfile` → container `/etc/caddy/Caddyfile:ro`

## Problem: Read-Only Bind Mount
Patching `/root/arifOS/Caddyfile` (source) does NOT update what a running Caddy container sees when the file is bind-mounted as read-only (`ro`).

## Symptom
- `docker exec caddy cat /etc/caddy/Caddyfile` shows OLD content after `patch` reports success
- `docker cp <file> caddy:/etc/caddy/Caddyfile` fails with: `unlinkat ... device or resource busy`
- Caddy continues serving stale config even after `docker exec caddy caddy reload`
- Root cause: the file is mounted `ro` from host `/root/arifOS/Caddyfile` → container `/etc/caddy/Caddyfile:ro`

## Correct Fix (two-step)

**Step 1:** Patch the correct source file:
```
patch /root/arifOS/Caddyfile <old> <new>
```

**Step 2:** Restart the Caddy container so it re-reads the source mount:
```
docker restart caddy
```

Then verify:
```
sleep 3 && curl -s https://arifos.arif-fazil.com/health
```

## Why This Happens
Read-only bind mounts are enforced by the Linux kernel at the mount point. The container's view of the file is snapshot-at-start-time. A reload alone doesn't re-read the source — only a full container restart does.

## ALWAYS Test Before Patching Routing
Before assuming a routing rule is wrong, test the actual endpoint:
```bash
# Test GEOX MCP (already works at /mcp — don't assume it's broken)
curl -s -X POST https://geox.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  -w "\nHTTP_STATUS:%{http_code}" | head -c 200

# Inside container (for debugging):
docker exec geox_eic python3 -c "
import urllib.request
for path in ['/health', '/mcp', '/mcp/stream']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8081{path}')
        print(f'{path}: {r.status}')
    except Exception as e:
        print(f'{path}: {e}')
"
```

## Verification Command
Always confirm the container's actual config after patching:
```
docker exec caddy grep "reverse_proxy arifosmcp" /etc/caddy/Caddyfile
```
If it still shows old value → restart the container.

## Relevant Volumes (arifOS stack)
- `/root/arifOS/Caddyfile` → `/etc/caddy/Caddyfile:ro` (Caddyfile, read-only mount) ← USE THIS
- `/root/sites/` → `/var/www/html:ro` (webroot, read-only mount)
- `/root/volumes/caddy/data` → `/data` (Caddy data dir)
- `/root/volumes/caddy/config` → `/config` (Caddy config dir)
