---
name: vps-health-ops
description: VPS health and diagnostics runbook. Load when checking system resources, Docker state, disk pressure, service ports, logs, SSL/Caddy, databases, or memory pressure on af-forge.
version: 1.0.0
last_verified: 2026-06-12
license: Proprietary
agents: claude | opencode
---

# VPS Health & Diagnostics

## Quick Health Sweep
```bash
# System resources
echo "=== DISK ===" && df -h | grep -E "Filesystem|/$"
echo "=== MEMORY ===" && free -h | grep -E "total|Mem:"
echo "=== CPU ===" && uptime
echo "=== SWAP ===" && free -h | grep Swap
```

## Docker Health Sweep
```bash
# All container status
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Only unhealthy or dead
docker ps -a --filter "status=exited" --filter "status=restarting"

# Resource hogs
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | sort -k2 -r
```

## Disk Emergency (>85% full)
```bash
# Find what's eating space
du -sh /var/lib/docker/* 2>/dev/null | sort -rh | head -10
du -sh /root/*/ 2>/dev/null | sort -rh | head -10

# Docker cleanup (safe)
docker builder prune -f
docker image prune -f

# Docker cleanup (need ARIF: docker system prune -af --volumes)
```

## Service Status Check
```bash
# Check all federation ports respond
for port in 8080 8081 8082 8083 3001 3002 7071 8100 5001; do
  status=$(curl -sf -o /dev/null -w "%{http_code}" http://localhost:$port/health 2>/dev/null || echo "DOWN")
  echo "Port $port: $status"
done
```

## Log Investigation
```bash
# Last 100 lines of service logs
docker compose -f /root/compose/docker-compose.yml logs --tail=100 <service>

# Search logs for errors
docker compose -f /root/compose/docker-compose.yml logs <service> 2>&1 | grep -i error | tail -20

# System logs
journalctl -u docker --since "1 hour ago" --no-pager
```

## SSL / Caddy Check
```bash
caddy validate --config /etc/caddy/Caddyfile
docker compose -f /root/compose/docker-compose.yml logs caddy --tail 30
```

## Database Check
```bash
# PostgreSQL
docker exec postgres psql -U arifos_admin -d vault999 -c "SELECT count(*) FROM vault_seals;"

# Redis
docker exec redis redis-cli PING
docker exec redis redis-cli INFO memory | grep used_memory_human
```

## Memory Pressure
```bash
# Top memory consumers
ps aux --sort=-%mem | head -10

# OOM killer history
dmesg | grep -i "out of memory" | tail -5
```
