---
name: vps-caddyfile-debug
description: Debug Caddyfile edits not reaching running container on VPS — always check mount topology first
---

# VPS Caddyfile Debug Skill

## Trigger
Editing Caddyfile for any arifOS surface and seeing no effect after `caddy reload`.

## Root Cause Pattern
The Caddy container on the VPS uses bind mounts. The running config may differ from source files on disk because:
1. Container's Caddyfile bind-mount overrides the compose source
2. Or: the Caddyfile on disk hasn't been copied to the container's mount point

## Always-Verify First (before editing)
```bash
# 1. Check actual mount sources for the caddy container
docker inspect caddy --format '{{range .Mounts}}{{.Type}} {{.Source}} → {{.Destination}}{{"\n"}}{{end}}'

# 2. Diff running Caddyfile against source
diff $(docker exec caddy cat /etc/caddy/Caddyfile) /root/compose/Caddyfile | head -20

# 3. Also check the arifOS Caddyfile (VPS uses this one directly)
diff $(docker exec caddy cat /etc/caddy/Caddyfile) /root/arifOS/Caddyfile | head -20
```

## Common Mount Topologies on VPS
| Compose file | Bind mount source |
|---|---|
| `/root/compose/docker-compose.yml` | `/root/compose/Caddyfile` → `/etc/caddy/Caddyfile` |
| VPS deploy (direct) | `/root/arifOS/Caddyfile` → `/etc/caddy/Caddyfile` |

**On VPS, the canonical Caddyfile is `/root/arifOS/Caddyfile`**, not `/root/compose/Caddyfile`.

## Quick Fix When Mounts Differ
```bash
# If running config != source, copy correct file to container
docker cp /root/arifOS/Caddyfile caddy:/etc/caddy/Caddyfile
docker exec caddy caddy reload --config /etc/caddy/Caddyfile

# Alternative: copy to tmp then overwrite
docker cp /root/arifOS/Caddyfile caddy:/tmp/Caddyfile
docker exec caddy sh -c 'cp /tmp/Caddyfile /etc/caddy/Caddyfile'
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## Caddy Reload Without Restart
```bash
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
# Or if caddy-admin socket available:
docker exec caddy caddy reload
```

## Related Gotchas
- `handle_path /.well-known/mcp/*` — `handle_path` strips the prefix before matching. `handle /.well-known/mcp/*` does NOT strip. Use the right one.
- Global `strip_path_prefix: "/.well-known"` in observatory block means requests to `/.well-known/mcp/*` get `/mcp/*` stripped TWICE if you also use `uri strip_prefix` in a sub-handle.
- Caddy always logs "using config from file" even if the file is identical — check actual adapted JSON to confirm your changes are live.
