---
name: Docker Guardian
slug: docker-guardian
version: 1.0.0
homepage: https://arif-fazil.com/skills/docker-guardian
description: "Federation stack guardian for OpenClaw. Monitors Docker containers, auto-restarts unhealthy services, tracks restart counts, and alerts on disk pressure. Built for the arifOS constitutional federation (arifOS, GEOX, WEALTH, WELL, AAA, APEX, A-FORGE)."
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["docker","curl"]},"os":["linux"]}}
---

## When to Use

Use when:
1. A federation service (arifOS, GEOX, WEALTH, WELL, AAA, APEX) is down or unresponsive
2. Docker containers need health checks or restart orchestration
3. Disk usage is climbing and cleanup is needed
4. You need a post-mortem on container crashes or restart loops

## Core Federation Stack

| Service | Container | Port | Critical |
|---------|-----------|------|----------|
| arifOS MCP | arifosmcp | 8080 | YES |
| GEOX MCP | geox_eic | 8081 | YES |
| WEALTH MCP | wealth-organ | 8082 | YES |
| WELL MCP | well | 8083 | YES |
| AAA A2A | aaa-a2a | 3001 | YES |
| APEX | apex-prime | 3002 | YES |
| A-FORGE | af-bridge-prod | 7071 | YES |
| Vault999 | vault999 | 8100 | YES |
| Postgres | postgres | 5432 | INFRA |
| Redis | redis | 6379 | INFRA |
| Qdrant | qdrant | 6333 | INFRA |
| NATS | nats | 4222 | INFRA |

## Commands

### Full Stack Health Check
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | sort
```

### Check Restart Counts (24h)
```bash
docker events --since "24h ago" --filter event=restart --format '{{.Actor.Attributes.name}}' | sort | uniq -c | sort -rn
```

### Auto-Restart Unhealthy Federation MCPs
```bash
for svc in arifosmcp geox_eic wealth-organ well; do
  status=$(docker inspect --format='{{.State.Health.Status}}' $svc 2>/dev/null)
  if [ "$status" != "healthy" ] && [ "$status" != "" ]; then
    docker restart $svc
  fi
done
```

### Disk Pressure Alert
```bash
df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
# > 85% → WARN Arif
# > 90% → CRITICAL → prune orphans, archive logs
```

### Prune Orphaned Resources
```bash
docker system prune -f --volumes
docker image prune -af
```

## Alert Thresholds

| Metric | WARN | CRITICAL |
|--------|------|----------|
| Disk usage | 80% | 90% |
| Container restarts (1h) | 3 | 5 |
| MCP response time | 2s | 5s |
| Zombie processes | 10 | 25 |

## Rules

1. **Never prune running containers** — only orphans and dangling images
2. **Restart one at a time** — avoid cascading failures across the federation mesh
3. **Log every action** — append to `~/.openclaw/workspace/logs/docker-guardian.log`
4. **Preserve Vault999** — never restart vault999 without explicit ack (append-only ledger)
