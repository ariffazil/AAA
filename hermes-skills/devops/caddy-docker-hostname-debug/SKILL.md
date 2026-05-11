---
name: caddy-docker-hostname-debug
description: Debug Caddy proxy HTTP hangs to Docker containers — nc succeeds but HTTP times out due to stale hostname resolution
tags: [caddy, docker, networking, arifOS]
last_updated: 2026-04-29
---

# arifOS Caddy–Docker Hostname Resolution Debug Skill

## Problem
Caddy proxy to a container (`reverse_proxy arifosmcp:8080`) returns HTTP 404 or hangs, even though:
- `nc -zv arifosmcp 8080` shows the port is OPEN
- Both containers are on the same Docker network
- The Caddyfile adapted JSON shows the correct route and upstream

## Root Cause Pattern
Caddy's embedded DNS resolver caches a **stale container IP**. Docker's internal DNS (`127.0.0.11`) correctly resolves the hostname to the current IP, but Caddy's resolver returns an old/stale IP from its cache. TCP (`nc`) tests bypass this by using Docker's DNS directly. HTTP hangs because it connects to the stale IP where the service no longer listens.

**Diagnostic evidence:**
```
getent hosts arifosmcp  →  172.19.0.17  (STALE — service moved)
nc -zv 172.19.0.3 8080 →  open         (correct IP, service listening)
HTTP to 172.19.0.3:8080 →  TIMEOUT      (because Caddy uses 172.19.0.17)
```

## Debugging Sequence

### Step 1 — Confirm TCP reachability
```bash
docker exec caddy sh -c "nc -zv <container_name> <port> 2>&1; echo exit=$?"
```
If exit=0 → TCP can reach. If fails → networking issue between containers.

### Step 2 — Check hostname resolution vs actual IP
```bash
docker exec caddy sh -c "getent hosts <container_name>"
docker inspect <container_name> --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```
If these differ → hostname resolution is stale.

### Step 3 — Confirm service is listening on actual IP
```bash
docker exec <container_name> sh -c "ss -tlnp | grep <port>"
docker exec <container_name> sh -c "cat /proc/net/tcp | python3 -c \"
import sys
for line in sys.stdin:
    parts = line.split()
    if len(parts) < 4: continue
    if parts[3] == '0A':
        lip, lport = parts[1].split(':')
        lport = int(lport, 16)
        lip_dec = '.'.join(str(int(lip[i:i+2], 16)) for i in [6,4,2,0])
        if lport == <PORT>:
            print(f'Listening on {lip_dec}:{lport}')
\""
```
Must show `0.0.0.0:<PORT>` on the correct network.

### Step 4 — Test HTTP to actual IP (bypass hostname)
```bash
docker exec caddy sh -c "timeout 5 curl -sv http://<ACTUAL_IP>:<PORT>/health 2>&1 | tail -10"
```
If this works but `curl http://<container_name>:<PORT>/health` fails → hostname resolution is the bug.

## Fixes (pick one)

### Fix 1 — Hardcode IP in Caddyfile (fastest)
```caddy
handle /.well-known/mcp/* {
    reverse_proxy <ACTUAL_IP>:<PORT>
}
```

### Fix 2 — Static host mapping in Caddyfile
Add a `hosts` directive or use `resolve` in the upstream block:
```caddy
handle /.well-known/mcp/* {
    reverse_proxy <container_name>:8080 {
        resolve 172.19.0.3:8080
    }
}
```

### Fix 3 — Fix Docker network (long-term)
Use static IP in docker-compose:
```yaml
networks:
  arifos_core_network:
    ipv4_address: 172.19.0.17  # consistent IP
```

## Related Traps

### Trap: HTTP→HTTPS redirect inside Caddy loopback
When proxying from one Caddy site block to another via `http://hostname:80`, the target block may redirect to HTTPS. The proxy returns the redirect (308), treated as 404 by Caddy.

**Fix:** Use `https://` with `tls_insecure_skip_verify`:
```caddy
reverse_proxy https://observatory.arif-fazil.com {
    transport http {
        tls_insecure_skip_verify
    }
}
```

### Trap: handle_path vs handle for static files
- `handle_path /.well-known/mcp/*` — **strips** `/.well-known/mcp/` from URI
- `handle /.well-known/mcp/*` — **keeps** full URI

For static files:
- `handle_path` + `root * /dir` → file at `/dir/mcp/server.json`
- `handle` + `root * /dir/.well-known/mcp` → file at `/dir/.well-known/mcp/server.json`

### Trap: nc succeeds but HTTP hangs
This is the primary symptom of hostname resolution staleness. Always verify HTTP with `curl -sv` to the actual IP, not just `nc -zv`.

## Context
Discovered debugging `/.well-known/mcp/server.json` → 404 on `arifos.arif-fazil.com`. arifosmcp container moved IPs after restart. Caddy's `getent hosts arifosmcp` returned `172.19.0.17` (stale) while service was on `172.19.0.3`.

## Files
- `/root/arifOS/Caddyfile` — active Caddy config (bind-mounted to `/etc/caddy/Caddyfile`)
