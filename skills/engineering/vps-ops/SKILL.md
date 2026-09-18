---
name: vps-ops
id: vps-ops
version: 2.0.0
description: >
  Docker Compose runbook for af-forge VPS. Pinned versions, restart discipline,
  health checks, compose governance, thermodynamic fleet reasoning, and concrete
  container commands. Lower machine entropy.
owner: AAA
risk_tier: medium
autonomy_tier: T2
floor_scope: [F1, F2, F3, F4, F8]
tags: [docker, vps, runbook, ops, compose, entropy, fleet, container]
capability_tier: fed-long-context
ecology_state: WARM
---

# VPS Operations — Docker Compose Runbook & Fleet Entropy

> **Lower machine entropy = pinned versions + health checks + restart limits + one network one owner.**

## What This Skill Is

A unified VPS operations skill covering:

1. **Docker Operations** — pinned versions, restart discipline, health checks, compose governance
2. **Concrete Runbook** — exact commands for inspecting, operating, and troubleshooting the Docker stack
3. **Entropy Lens** — thermodynamic reasoning for container fleet health, resource pressure, and safe/dangerous intervention boundaries

## Stack Location

Primary compose: `/root/compose/docker-compose.yml`

## When to Use

- A federation organ or utility container needs health-checking, log inspection, or bounded restart
- Docker container or compose stack appears unhealthy, restarting, or resource-starved
- Disk pressure, memory pressure, or CPU saturation is suspected on the VPS
- Need to validate the compose config before a planned stack operation
- Resource usage or container state must be verified
- A service is flapping and needs stop → diagnose → restart

## When NOT to Use

- **Do not use for systemd-managed federation organs** (arifOS, WEALTH, WELL, GEOX, A-FORGE, AAA). Use their respective `systemctl` commands.
- **Do not use for Kubernetes or Swarm** orchestration (not deployed).
- **Do not use for Docker image authoring** or CI/CD pipeline configuration (use `cicd-deploy`).
- **Do not use for destructive cleanup** without 888 HOLD and human ack.

## §1. GOVERNANCE

### One Compose Project, One Network, One Owner
- All infra containers run on `arifos_core_network`
- Each service belongs to exactly ONE compose project
- Each compose project has exactly ONE owner
- **Never start a container outside a compose file** unless temporary diagnostic

### Pin Every Version
```yaml
# ✅ GOOD — pinned
image: postgres:16-alpine
image: redis:7-alpine

# ❌ BAD — no tag = "latest" drift
image: postgres
```

### Restart Policy Discipline
```yaml
# ✅ GOOD — production services
restart: unless-stopped

# ❌ AVOID — masks failure, infinite retries
restart: always
```
- If a service restarts >5 times in 5 minutes → **STOP AND INVESTIGATE**

### Every Container Needs a Health Check
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:<port>/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 15s
```

## §2. LIVE SERVICE MAP

```
postgres         :5432   (PostgreSQL 16-alpine, pinned)
redis            :6379   (Redis 7-alpine, pinned)
falkordb         :6380   (FalkorDB, knowledge graph)
qdrant           :6333   (Qdrant vector search)
minio            :9000   (MinIO object storage)
searxng          :8080   (Self-hosted search)
graphiti-mcp     :8000   (Graphiti MCP, Docker-managed)
```

## §3. SAFE OPERATIONS

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
docker logs -f <service> --tail 50
```

### Restart a service
```bash
docker restart <service>
# Or compose-scoped:
docker compose restart <service>
docker compose up -d <service>
```

### Check resource usage
```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker system df
```

### Validate compose config
```bash
cd /root/compose && docker compose config
```

### Safe stack reconcile
```bash
docker compose up -d --remove-orphans
```

## §4. ENTROPY LENS — Fleet Thermodynamic Reasoning

### Read Fleet Entropy (before any intervention)

1. `docker ps` — what is running, dead, or restarting?
2. `docker stats --no-stream` — who is consuming CPU/memory?
3. `docker system df` — how much disk entropy has accumulated?
4. `docker compose ps` and `docker compose config` if compose stack involved

### Signal Priority (rank findings)

1. Container health status (Up vs Restarting vs Exited)
2. Memory pressure (approaching limit)
3. Disk entropy (dangling images, volumes, build cache)
4. CPU saturation (sustained >80%)
5. Log anomalies (error rate spikes)

### Intervention Classification

**Safe / reversible — proceed with witness:**
- `docker compose config` (validate, no mutation)
- `docker compose ps` (state inspection)
- `docker logs --tail=N <service>` (observation)
- `docker compose restart <service>` (reversible)
- `docker compose up -d <service>` (restore known state)

**Dangerous / irreversible — 888 HOLD required:**
- `docker system prune -af --volumes` (irreversible disk purge)
- `docker rm -f <container>` (data loss risk)
- `docker volume rm <volume>` (permanent data destruction)

### Uncertainty Protocol

- Container is Restarting → read logs before restarting again
- Disk usage >85% → diagnose before pruning
- Unsure whether a volume is in use → inspect; do not delete
- Service unhealthy but cause unclear → 888 HOLD
- Never prune without first running `docker system df`

## §5. DANGEROUS OPERATIONS (888_HOLD)

### Disk cleanup (safe subset)
```bash
docker builder prune -f
docker image prune -f
# NEVER: docker system prune -af --volumes  (F1 — irreversible!)
```

### Remove a container
```bash
docker rm -f <container>   # data loss risk! 888 HOLD required
```

### Remove a volume
```bash
docker volume rm <volume>   # permanent data loss! 888 HOLD required
```

## §6. EMERGENCY: Service Keeps Restarting

### Step 1: STOP THE LOOP
```bash
docker stop <service>
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
```

### Step 5: VERIFY
```bash
docker inspect <service> --format '{{.State.Health.Status}}'
# Must return "healthy", not just "running"
```

## §7. ANTI-PATTERNS

- ❌ `restart: always` without limit — infinite restart loops
- ❌ Starting containers without health checks
- ❌ Running containers outside compose/network governance
- ❌ Restarting a looping service without investigation
- ❌ `latest` tag in production — version drift
- ❌ Two agents managing the same container
- ❌ Panic pruning (`docker system prune -af`) as first response
- ❌ Assuming "container is Up" means "container is healthy"

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Destructive cleanup requested | arifOS 888_JUDGE + Arif | 888 HOLD |
| Data-bearing volume/container affected | arifOS 888_JUDGE | verdict_request |
| Docker daemon unresponsive | A-FORGE ops / system triage | A2A/incident |
| Full stack or host restart needed | A-FORGE + human ack | 888 HOLD |
| Repeated service crashes after restart | Service owner organ | A2A handoff |
| Scope creep into systemd/K8s/Dockerfile work | STOP; route to correct skill | A2A message |
