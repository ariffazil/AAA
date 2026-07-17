---
id: vps-docker-ops
name: FORGE-vps-docker
version: 2.0.0
description: "Runbook for VPS Docker operations — pinned versions, restart discipline, health checks, compose governance. Lower machine entropy."
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F4, F8]
autonomy_tier: T2
tags: [docker, vps, runbook, ops, compose, entropy]
---

# VPS Docker Operations — Production Discipline

> **Lower machine entropy = pinned versions + health checks + restart limits + one network one owner.**

## Stack Location
Primary compose: `/root/compose/docker-compose.yml`
Individual services may be managed via systemd units with Docker CLI.

## Governance

### One Compose Project, One Network, One Owner
- All infra containers run on `arifos_core_network` (Docker network)
- Each service belongs to exactly ONE compose project
- Each compose project has exactly ONE owner (the organ that depends on it)
- **Never start a container outside a compose file** unless it's a temporary diagnostic

### Pin Every Version
Every `image:` field in compose files MUST reference a specific tag:
```yaml
# ✅ GOOD — pinned
image: postgres:16-alpine
image: redis:7-alpine
image: falkordb/falkordb:latest    # acceptable for actively-developed

# ❌ BAD — no tag = "latest" drift
image: postgres
image: redis
```
- Prefer `<major>.<minor>` tags over `latest`
- Audit quarterly: `docker images --digests | grep -v "^<none>"`

### Restart Policy Discipline
```yaml
# ✅ GOOD — production services
restart: unless-stopped

# ❌ AVOID — masks failure, infinite retries
restart: always

# ❌ AVOID — containers die silently on host reboot
# (no restart policy set)
```
- Set `RestartMaxRetries` and `RestartSec` in systemd for sidecar services
- If a service restarts >5 times in 5 minutes → **STOP AND INVESTIGATE** — do not let it loop

### Every Container Needs a Health Check
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:<port>/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 15s
```
- Without a health check, Docker cannot tell you the service is broken
- Systemd units should also have `HealthCheck` or watchdog integration

## Live Service Map

```
postgres         :5432   (PostgreSQL 16-alpine, pinned)
redis            :6379   (Redis 7-alpine, pinned)
falkordb         :6380   (FalkorDB, knowledge graph)
qdrant           :6333   (Qdrant vector search)
minio            :9000   (MinIO object storage)
searxng          :8080   (Self-hosted search)
graphiti-mcp     :8000   (Graphiti MCP, Docker-managed)
```

## Safe Operations

### Check all services
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Check one service health
```bash
docker inspect <service> --format '{{.State.Health.Status}}'
curl -sf http://localhost:<port>/health
```

### View logs
```bash
docker logs <service> --tail 100
docker logs -f <service> --tail 50   # live
```

### Restart a service
```bash
docker restart <service>
```

### Stop a failing service (don't let it loop)
```bash
docker stop <service>
# Investigate first. Never restart blindly.
```

### Check resource usage
```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker system df
```

## Dangerous Operations (888_HOLD)

### Disk cleanup
```bash
docker builder prune -f
docker image prune -f
# NEVER: docker system prune -af --volumes  (F1 — irreversible!)
```

### Remove a container
```bash
docker rm -f <container>   # data loss risk!
```

### Remove a volume
```bash
docker volume rm <volume>   # permanent data loss!
```

## Emergency: Service Keeps Restarting

### Step 1: STOP THE LOOP
```bash
docker stop <service>          # immediate stop
systemctl stop <service>.service   # if systemd-managed
```

### Step 2: CHECK WHY
```bash
docker logs <service> --tail 200
journalctl -u <service>.service --since '5m ago'
```

### Step 3: FIX THE ROOT CAUSE
- Auth failure → update credentials in env
- DNS resolution → check network and dependent containers
- Missing file/dir → check volume mounts and permissions
- Port conflict → check `ss -tlnp`

### Step 4: RESTART WITH INTENT
```bash
docker start <service>
# Or for systemd-managed: systemctl start <service>
```

### Step 5: VERIFY
```bash
docker inspect <service> --format '{{.State.Health.Status}}'
# Must return "healthy", not just "running"
```

## How to Check What Changed
```bash
docker diff <container>
docker inspect <container> --format '{{json .Config}}' | python3 -m json.tool
```

## Anti-Patterns
- ❌ `restart: always` without limit — infinite restart loops
- ❌ Starting containers without health checks
- ❌ Running containers outside compose/network governance
- ❌ Restarting a looping service without investigation
- ❌ `latest` tag in production — version drift
- ❌ Two agents managing the same container
