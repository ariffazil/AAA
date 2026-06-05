---
name: vps-docker
description: Full VPS Docker status — all containers, resource usage, arifOS health. Use when Arif asks about container status, VPS health, what's running, memory/CPU usage, or wants to restart/rebuild services.
user-invocable: true
---

# VPS Docker Manager

**Host:** `arifos` (SSH alias → ariffazil@mcp.arif-fazil.com)
**F1 Amanah:** All destructive operations require 888_HOLD confirmation.

## Quick Status Commands

```bash
# List all containers with status and ports
ssh arifos "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

# Resource usage (CPU + Memory)
ssh arifos "docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'"

# Full compose stack health
ssh arifos "cd /root/arifOS && docker compose ps"

# Check logs for a specific service
ssh arifos "docker logs arifosmcp --tail 50"

# VPS system resources
ssh arifos "free -h && df -h /"
```

## Service Map (arifOS Stack)

| Container | Port | Purpose |
|-----------|------|---------|
| `arifosmcp` | 8080 | Constitutional MCP kernel (Rail A) |
| `caddy` | 443/80 | Reverse proxy + TLS |
| `authentik` | 9000 | Identity provider |
| `postgresql` | 5432 | Database |
| `redis` | 6379 | Cache + memory |
| `langfuse` | 3000 | Observability |

## Restart / Rebuild (888_HOLD required for production)

```bash
# 888_HOLD — confirm with Arif before executing:
ssh arifos "cd /root/arifOS && docker compose restart arifosmcp"
ssh arifos "cd /root/arifOS && docker compose up -d --build arifosmcp"
```

## Health Check Integration

```bash
# Full arifOS health via MCP
curl -sf https://mcp.arif-fazil.com/health | jq

# Local (when on VPS)
curl -sf http://localhost:8080/health | jq
```

## F1 Amanah — Irreversibility Classification

- `docker ps` / `docker stats` / `docker logs` → SAFE (read-only)
- `docker restart` → LOW RISK (reversible)
- `docker compose down` → 888_HOLD (service disruption)
- `docker compose down -v` → 888_HOLD (data loss risk)
- `docker system prune` → 888_HOLD (irreversible)

---

*DITEMPA BUKAN DIBERI — VPS ALIVE*
