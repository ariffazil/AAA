---
name: caddyfile-ro-bind-mount-patch
description: How to patch a Caddyfile when it is bind-mounted read-only into the Caddy container
tags: [caddy, docker, bind-mount, ops]
last_updated: 2026-04-27
---

# Skill: Patching Caddyfile When Bind-Mounted Read-Only

## Problem
Patching `/root/arifOS/Caddyfile` (source) does NOT update what a running Caddy container sees when the file is bind-mounted as read-only (`ro`).

## Symptom
- `docker exec caddy cat /etc/caddy/Caddyfile` shows OLD content after `patch` reports success
- `docker cp <file> caddy:/etc/caddy/Caddyfile` fails with: `unlinkat ... device or resource busy`
- Caddy continues serving stale config even after `docker exec caddy caddy reload`
- Root cause: the file is mounted `ro` from host `/root/arifOS/Caddyfile` → container `/etc/caddy/Caddyfile:ro`

## Correct Fix (two-step)

**Step 1:** Patch the source file as normal:
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

## Verification Command
Always confirm the container's actual config after patching:
```
docker exec caddy grep "reverse_proxy arifosmcp" /etc/caddy/Caddyfile
```
If it still shows old value → restart the container.

## Relevant Volumes (arifOS stack)
- `/root/arifOS/Caddyfile` → `/etc/caddy/Caddyfile:ro` (Caddyfile, read-only mount)
- `/root/sites/` → `/var/www/html:ro` (webroot, read-only mount)
- `/root/volumes/caddy/data` → `/data` (Caddy data dir)
- `/root/volumes/caddy/config` → `/config` (Caddy config dir)
