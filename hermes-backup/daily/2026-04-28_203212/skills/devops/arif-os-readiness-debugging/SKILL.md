---
name: arif-os-readiness-debugging
description: arifOS endpoint/container debugging protocol — runtime witness before infrastructure speculation
tags: [debugging, runbook, arifOS]
version: 1.0.0
author: arifOS Constitutional Federation
created: 2026-04-28
trigger_on: ["endpoint down", "container issue", "deployment problem", "/ready partial", "Caddy 502", "network unreachable"]
---

# arifOS Readiness Debugging Protocol

## Core Rule
**Never debug infrastructure until the constitutional readiness surface has been read.**

Authority order (highest to lowest):
1. `/ready` — constitutional readiness (14 checks, authoritative)
2. `/status.json` — federation status
3. `/health` — service health
4. Running Caddyfile inside container
5. Container logs
6. Listener/network diagnostics
7. iptables/firewall

## Diagnostic Chain

```
1. curl -s https://mcp.arif-fazil.com/ready
   → If status: pass → readiness is NOT the issue
   → If status: partial → READ the failures list

2. If /ready names a failing check (e.g., forge_dry_run_check):
   → Treat that as primary until disproven
   → Inspect source code for that check's implementation
   → Do NOT assume Docker bind / networking

3. If /ready passes but public endpoint fails:
   → Inspect Caddyfile inside running container:
     docker exec caddy cat /etc/caddy/Caddyfile
   → Check Caddy logs:
     docker logs caddy --tail 20
   → Verify reverse_proxy directives point to correct container service name

4. Only after /ready is clean AND the failure still persists:
   → docker exec <container> cat /proc/net/tcp (decode hex IP:port)
   → Check Docker network membership:
     docker inspect <container> --format '{{json .NetworkSettings.Networks}}'
   → docker exec caddy nc -vz <target-service> <port>
   → docker exec caddy curl -v --connect-timeout 5 http://<target>:PORT/endpoint
```

## Common Pitfalls

- **Jumping to Docker networking before /ready** — wastes 30-60 min on ghost bugs
- **Using `ss` or `netstat` without checking if they're installed** — these are often absent
  → Use `cat /proc/net/tcp` + Python decode instead
- **Trusting secondary sources** — always verify disk/API directly, never trust docs
- **Forgetting `ss` isn't in minimal containers** — probe first with `which ss || which netstat`

## Decode TCP Table (when /proc/net/tcp is the only option)

```python
import socket
STATE = {0x01:'ESTABLISHED', 0x06:'TIME_WAIT', 0x08:'CLOSE_WAIT', 0x0A:'LISTEN', 0x0B:'LISTEN'}
with open('/proc/net/tcp') as f:
    for i, line in enumerate(f):
        if i == 0: continue
        p = line.split()
        if len(p) < 10: continue
        lip, lport = p[1].split(':')
        rport = int(lport, 16)
        state = int(p[3], 16)
        ip = socket.inet_ntoa(bytes.fromhex(lip)[::-1])
        sn = STATE.get(state, hex(state))
        if rport == 8080 or state == 0x0A:
            print(f'{sn}  {ip}:{rport}')
```

## The arifOS Debugging Mantra

> "I have not yet proven transport failure. First witness /ready. Second witness Caddy route. Third witness container listener. Only then decide."

## Verification Steps After a Redeploy

```bash
# 1. Wait for healthy
sleep 8 && docker ps --filter name=arifosmcp --format "{{.Status}}"

# 2. Check /ready
curl -s https://mcp.arif-fazil.com/ready | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'Status: {d[\"status\"]}')
[print(f'  {k}: {v[\"verdict\"]}') for k,v in d['checks'].items()]
print(f'Failures: {d[\"failures\"]}')
"

# 3. Check public endpoint
curl -s https://mcp.arif-fazil.com/health | python3 -m json.tool | head -10
curl -s https://mcp.arif-fazil.com/status.json | python3 -m json.tool | head -10
```
