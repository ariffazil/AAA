---
id: vps-docker-runbook
name: FORGE-vps-runbook
version: 1.0.0
description: Concrete Docker Compose and container commands for the af-forge VPS stack.
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills:
  - arifos-act
  servers: []
  tools: []
examples:
- Check health of all Docker services in the af-forge stack
- Restart a single federation service container safely
- Inspect logs and resource usage for a failing container
- Validate docker-compose.yml before restarting the stack
tests:
- docker compose ps returns the expected service list
- docker compose config validates without errors
- Restarting a service restores its /health endpoint
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Ω
  functional:
  - Ops
  layer: RUNTIME
  autonomy_tier: T2
floor_scope:
- F1
- F2
- F3
- F4
---

# VPS Docker Runbook

## Overview

This skill gives agents the exact commands to inspect, operate, and troubleshoot the Docker-based data/utility stack on the `af-forge` VPS. It covers the `docker-compose.yml` at `/root/compose/`, the live service map, safe read-only checks, bounded restarts, and the dangerous operations that require escalation.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- A federation organ or utility container needs health-checking, log inspection, or bounded restart.
- You need to validate the compose config before a planned stack operation.
- Resource usage or container state must be verified (`docker stats`, `docker system df`).
- A service is flapping and you need to stop → diagnose → restart it safely.

## When NOT to Use

- **Do not use for systemd-managed federation organs** (arifOS, WEALTH, WELL, GEOX, A-FORGE, AAA a2a, APEX). Those live as bare-metal services; use their respective `systemctl` commands instead.
- **Do not use for destructive cleanup** (`docker system prune`, volume removal, forced container deletion) without 888 HOLD and human ack.
- **Do not run `docker compose down` or `--volumes` variants** on the full stack unless explicitly authorized.
- If the Docker daemon itself is unresponsive, escalate to A-FORGE / system triage rather than guessing.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| service_name | no | Target container/service name from `docker compose ps` |
| operation | yes | One of: status, logs, restart, validate, resources, emergency-stop, diff |
| tail_lines | no | Number of log lines to retrieve (default: 100) |

## Procedure

### Step 1: Locate the stack

```bash
cd /root/compose
```

All Docker services are defined in `/root/compose/docker-compose.yml`.

### Step 2: Check service status

```bash
docker compose ps
docker compose config   # validate before any change
```

### Step 3: Inspect one service

```bash
# Health status
docker inspect <service> --format '{{.State.Health.Status}}'
curl -sf http://localhost:<port>/health

# Logs
docker compose logs --tail=100 <service>
docker compose logs -f <service>

# Changed files and config
docker diff <container>
docker inspect <container> --format '{{json .Config}}' | python3 -m json.tool
```

### Step 4: Bounded restart

```bash
# Restart in place
docker compose restart <service>

# Rebuild and restart only this service
docker compose up -d <service>

# Restart the whole Docker stack (safe bounded variant)
docker compose up -d --remove-orphans
```

### Step 5: Check resource usage

```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker system df
```

### Step 6: Emergency stop for a flapping service

```bash
docker compose stop <service>
docker logs <service> --tail 200
# Fix the issue, then:
docker compose up -d <service>
```

## Allowed Tools

| Tool / Command | Purpose |
|----------------|---------|
| `docker compose ps` | List running compose services |
| `docker compose config` | Validate compose file |
| `docker compose logs` | Read or tail service logs |
| `docker compose restart` | Bounded in-place restart |
| `docker compose up -d <service>` | Rebuild/restart a single service |
| `docker compose up -d --remove-orphans` | Safe stack reconcile |
| `docker compose stop <service>` | Graceful emergency stop |
| `docker inspect` | Container health/config inspection |
| `docker stats` / `docker system df` | Resource usage and disk summary |
| `docker diff` | Files changed since container start |
| `curl -sf http://localhost:<port>/health` | HTTP health probe |

## Forbidden Actions

- **NEVER** run `docker system prune -af --volumes` — irreversible data loss (F1 HOLD).
- **NEVER** run `docker volume rm <volume>` without sovereign ack and a verified backup.
- **NEVER** run `docker rm -f <container>` on data-bearing services without escalation.
- **NEVER** run `docker compose down --volumes` on the full stack.
- **NEVER** restart the Docker daemon or the full host without A-FORGE/systemd clearance.
- Escalate to **arifOS 888_JUDGE** if any destructive action is requested or if a service holds persistent data.

## Output Format

```
## Skill Result: vps-docker-runbook

### Summary
One-paragraph summary of what was checked, restarted, or diagnosed.

### Evidence
- Service status: <running / stopped / unhealthy>
- Health endpoint: <HTTP code / not reachable>
- Logs tail: <key lines or "clean">
- Resource snapshot: <if checked>

### Recommendations
- Next safe step, or
- Escalation reason and target

### Escalations
- None / <list>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Destructive cleanup requested | arifOS 888_JUDGE + Arif | 888 HOLD |
| Data-bearing volume/container affected | arifOS 888_JUDGE | verdict_request |
| Docker daemon unresponsive | A-FORGE ops / system triage | A2A/incident |
| Full stack or host restart needed | A-FORGE + human ack | 888 HOLD |
| Repeated service crashes after restart | Service owner organ / runbook | A2A handoff |

---

*Skill version 1.0.0 — AAA Skill Library*
