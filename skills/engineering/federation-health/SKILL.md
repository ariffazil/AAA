---
name: federation-health
description: >
  Unified federation monitoring, container health, auto-recovery, and entropy reasoning. Covers
  federation orchestration (docker compose, restart, MCP health probes, container drift detection),
  VPS telemetry auto-healing (Caddy error spikes, container log analysis, automated recovery), and
  Docker entropy reasoning (thermodynamic fleet health, resource pressure, safe/dangerous intervention
  boundaries). Merges: FORGE-federation-orchestrator, vps-telemetry-auto-healer, FORGE-docker-entropy.
id: federation-health
version: 2.0.0
owner: A-FORGE
risk_tier: low
floor_scope: [F1, F2, F3, F4, F8, F11, F13]
autonomy_tier: T1
tags: [federation, docker, health, monitoring, recovery, entropy, telemetry, caddy, container, orchestrator]
capability_tier: fed-agent-subagent
ecology_state: WARM
supersedes:
  - FORGE-federation-orchestrator
  - vps-telemetry-auto-healer
  - FORGE-docker-entropy
triggers:
  - "federation status"
  - "restart dead container"
  - "container health"
  - "docker drift"
  - "service down"
  - "probe MCP"
  - "health check federation"
  - "docker compose"
  - "container restart"
  - "restart count"
  - "Caddy error"
  - "502 spike"
  - "504 spike"
  - "auto-healer"
  - "container recovery"
  - "docker entropy"
  - "docker system df"
  - "disk pressure"
  - "memory pressure"
  - "container fleet"
  - "thermodynamic"
  - "docker prune"
  - "resource pressure"
---

# Federation Health

> **Three domains unified:** Federation Orchestrator + VPS Telemetry Auto-Healer + Docker Entropy.
> Containers are thermodynamic systems: CPU is energy, memory is state, disk is storage, network is exchange.
> *DITEMPA BUKAN DIBERI*

## Overview

Unified federation health covering three domains:
1. **Federation Orchestrator** — Monitor and manage the arifOS federation: docker compose ps, restart dead services, MCP health probes, container drift detection, restart count monitoring.
2. **VPS Telemetry Auto-Healer** — Real-time Caddy HTTP error spike monitor, Docker container log stream analyzer, and automated container health recovery watchdog.
3. **Docker Entropy** — Thermodynamic reasoning lens for container fleet health, resource pressure, and safe/dangerous intervention boundaries.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- A Docker container or compose stack appears unhealthy, restarting, or resource-starved.
- Disk pressure, memory pressure, or CPU saturation is suspected on the VPS.
- You need to decide whether to restart, prune, inspect logs, or escalate.
- An MCP server returns connection refused, timeout, or 5xx.
- Caddy HTTP 502/504 error spikes detected.
- Federation status report needed.
- Container restart count tracking (flag containers with >3 restarts).
- After cron changes to verify telemetry pipeline.

## When NOT to Use

- **Do not use** for non-Docker services (systemd-native, bare-metal processes) — use systemd skills.
- **Do not use** for Kubernetes or Swarm orchestration (not deployed).
- **Do not use** for Docker image authoring, Dockerfile creation, or CI/CD pipeline configuration.
- **Do not use** as authority to run destructive commands without 888 HOLD.

---

## Section 1: Federation Orchestrator

### Commands

```bash
# Full federation status
docker compose ps
docker ps -a --filter "status=restarting"

# Check organ endpoints (verified 2026-08-14)
for url in 8088 7071 7072 7073 7074 8081 18082 18083; do
  curl -s -o /dev/null -w "%{http_code} :$url\n" --max-time 5 http://localhost:$url/health
done

# Restart dead container
docker compose restart <service>
docker restart <container>

# Restart count audit
docker inspect --format='{{.Name}} {{.RestartCount}}' $(docker ps -aq)

# Federation stack locations
cd /root/arifOS && docker compose ps
cd /root/AAA && docker compose ps
```

### Health Probe Script

```bash
#!/bin/bash
for port in 8088 7071 7072 7073 7074 8081 18082 18083; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:$port/health)
  if [ "$code" = "200" ]; then
    echo "✅ MCP:$port OK"
  else
    echo "❌ MCP:$port FAILED (HTTP $code)"
  fi
done
```

### Restart Count Thresholds

| Restarts | Severity | Action |
|---|---|---|
| 0 | ✅ Healthy | No action |
| 1–3 | ⚠️ Watch | Log + warn |
| 4–9 | 🔴 Degraded | Alert + review |
| 10+ | ⛔ Critical | Auto-restart cooldown + human alert |

### Observed Port Map (verified 2026-08-14 via ss + systemctl + curl)

| Port | Service | Owner |
|---|---|---|
| 8088 | arifOS kernel | systemd arifos.service |
| 7071 | A-FORGE executor | systemd a-forge.service |
| 7072 | A-FORGE MCP gateway | systemd a-forge-mcp.service |
| 7073 | arifFlow daemon | systemd arifflow.service |
| 7074 | FED router | systemd fed-router.service |
| 8081 | GEOX MCP | systemd geox-mcp.service |
| 18082 | WEALTH | systemd wealth-organ.service |
| 18083 | WELL | systemd (python3) |
| 8080 | searxng (Docker) | NOT an organ — do not probe as arifOS |
| 8083 | headscale | NOT an organ |

### Federation Nodes (LEGACY docker-compose era — verify at runtime before trusting)

| Container | Port | Stack | Criticality |
|---|---|---|---|
| arifosmcp | 8080 | arifOS | CRITICAL |
| geox_eic | 8081 | GEOX | CRITICAL |
| wealth-organ | 8082 | WEALTH | HIGH |
| well | 8083 | WELL | HIGH |
| vault999 | — | Vault999 | CRITICAL |
| postgres | 5432 | arifOS | CRITICAL |
| qdrant | 6333 | arifOS | HIGH |
| redis | 6379 | arifOS | HIGH |
| nats | 4222 | arifOS | MEDIUM |
| aaa-a2a | 3001 | AAA | HIGH |
| searxng | 8080 | Search | LOW |
| netdata | 19999 | Monitoring | LOW |

---

## Section 2: VPS Telemetry Auto-Healer

### Diagnostic & Triage Workflow

#### 1. Check Container Health & Memory Throttling
```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.PIDs}}"
```

#### 2. Scan Caddy Log Stream for 502 / 504 Spikes
```bash
tail -n 200 /var/log/caddy/access.log | grep -E "status\":(502|504|500)"
```

#### 3. Graceful Container Self-Healing Circuit
```bash
# Verify container failure state before restart
if ! docker inspect --format='{{.State.Health.Status}}' searxng | grep -q "healthy"; then
    echo "[AUTO-HEALER] SearXNG unhealthy. Restarting..."
    docker restart searxng
fi
```

### Best Practices
1. **Governed Recovery**: Always verify container failure traceback before executing restart operations.
2. **Telemetry Log Receipt**: Record all auto-healing actions in `telemetry_audit.log`.

---

## Section 3: Docker Entropy — Thermodynamic Fleet Health

### Step 1: Read Fleet Entropy

Run these in order before any intervention:

1. `docker ps` — what is running, dead, or restarting?
2. `docker stats --no-stream` — who is consuming CPU/memory?
3. `docker system df` — how much disk entropy (images, volumes, build cache) has accumulated?
4. `docker compose ps` and `docker compose config` if a compose stack is involved.

### Step 2: Interpret Signal Priority

Rank findings in this order:
1. Container health status (Up vs Restarting vs Exited)
2. Memory pressure (approaching limit)
3. Disk entropy (dangling images, volumes, build cache)
4. CPU saturation (sustained >80%)
5. Log anomalies (error rate spikes)

### Step 3: Choose the Intervention Class

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
- `docker rmi <image>` when the image is actively used

### Step 4: Apply Uncertainty Protocol

- Container is Restarting → read logs before restarting again.
- Disk usage >85% → diagnose before pruning.
- Unsure whether a volume is in use → inspect; do not delete.
- Service unhealthy but cause unclear → 888 HOLD.
- Never prune without first running `docker system df`.

---

## Alert Conditions

| Condition | Action |
|-----------|--------|
| MCP HTTP 000/502/503 | Auto-restart container + log |
| MCP response > 3s | WARN in heartbeat |
| Model provider 401/402 | Disable from fallback chain + alert |
| Ollama cold-start > 15s | Pre-warm model via `/api/generate` |
| Caddy 502/504 spike | Scan logs, identify target container, verify + restart |
| Container restart count > 3 | Flag degraded, review logs |
| Disk entropy > 85% | Diagnose before pruning, 888 HOLD for prune |

## Allowed Tools

| Tool / Command | Purpose |
|----------------|---------|
| `docker ps` | Fleet state snapshot |
| `docker stats --no-stream` | Resource consumption |
| `docker system df` | Disk entropy inventory |
| `docker logs --tail=N <service>` | Diagnostic observation |
| `docker compose ps` | Compose stack state |
| `docker compose config` | Validate compose configuration |
| `docker compose restart <service>` | Reversible service restart |
| `docker compose up -d <service>` | Restore known-good state |
| `docker inspect` | Container health status, restart count |
| `curl` | MCP endpoint health probes |
| `tail` / `grep` | Caddy log stream analysis |

## Forbidden Actions

- **NEVER** run `docker system prune -af` as a first response to any problem (panic pruning).
- **NEVER** restart a container without reading its logs first.
- **NEVER** assume "container is Up" means "container is healthy".
- **NEVER** ignore disk entropy until it causes system failure.
- **NEVER** delete volumes without verifying they contain no critical data.
- **NEVER** run prune without human confirmation (F1 violation).
- **NEVER** restart Vault999 — append-only ledger, human ack required.
- **NEVER** restart multiple containers simultaneously — avoid federation cascade.
- Escalate to **arifOS 888_JUDGE** before any destructive action.

## Output Format

```
## Skill Result: federation-health

### Summary
One-paragraph summary of fleet thermodynamic state and chosen intervention.

### Evidence
- Container state: <running / restarting / exited>
- Resource pressure: <CPU / memory / disk findings>
- Disk entropy: <docker system df output>
- Log anomalies: <yes/no with snippet>
- Caddy errors: <502/504 count in last N requests>

### Recommendations
- Safe reversible action, OR
- 888 HOLD with reason and proposed next step

### Escalations
- None / <list>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Destructive or irreversible Docker action | arifOS 888_JUDGE + Arif | 888 HOLD |
| Data-loss risk (volume/container removal) | arifOS 888_JUDGE | verdict_request |
| Scope creep into systemd/K8s/Dockerfile work | STOP; route to correct skill | A2A message |
| Root cause unclear after diagnosis | arifOS 888_JUDGE | hold with reason |
| All containers healthy but Caddy still 502 | Caddy config review + arifOS | health triage |

---

*Consolidated 2026-08-26 from: FORGE-federation-orchestrator, vps-telemetry-auto-healer, FORGE-docker-entropy.*
*AAA Skill Library — version 2.0.0*
