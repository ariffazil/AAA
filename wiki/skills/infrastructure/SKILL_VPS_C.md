---
title: "SKILL: VPS Docker Manager"
type: skill
version: 1.0.0
category: infra
risk_band: HIGH
floors: [F1]
evidence_required: true
sources: [/root/.opencode/skills/vps-docker/SKILL.md]
confidence: high
---

# SKILL: VPS Docker Manager

> **Source:** `/root/.opencode/skills/vps-docker/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Docker container lifecycle management
- Compose up/down/restart operations
- Container logs, health status, volume inspection
- Image pruning, resource monitoring
- Keywords: docker, compose, container, vps, devops

---

## Pre-Action Checklist

Before ANY docker operation:
1. `docker compose config` — validate compose file syntax
2. `docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` — baseline state

---

## Container Operations

| Task | Command |
|------|---------|
| Status | `docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}"` |
| Logs (live) | `docker logs --tail=100 -f <container>` |
| Restart | `docker compose restart <service>` |
| Exec into | `docker exec -it <container> /bin/sh` |
| Resource usage | `docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"` |

---

## Compose Workflows

```bash
# Safe deploy sequence
docker compose pull
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail=20
```

---

## Destructive — 888_HOLD Required

- `docker system prune -af --volumes` — confirm with human first
- `docker rm -f <container>` — confirm container name before execute
- `docker volume rm <volume>` — data loss risk

---

## Health Check Pattern

For each service, verify:
1. Container status = "Up" (not "Restarting" or "Exited")
2. Port binding visible in `docker ps`
3. Application responds: `curl -sf http://localhost:<port>/health`

---

## Output Format

Always show: `[SERVICE] [STATUS] [ACTION TAKEN] [RESULT]`

---

## Related Pages

- [[skill-vps-management]] — VPS management (SSH level)
- [[skill-docker-thermodynamics]] — entropy management
- [[skill-docker-security]] — hardening and port audits
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Docker managed. Compose validated.*
