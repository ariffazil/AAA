---
title: "SKILL: VPS Management"
type: skill
version: 1.0.0
category: infra
risk_band: HIGH
floors: [F1]
evidence_required: true
sources: [/root/.opencode/skills/vps-management/SKILL.md]
confidence: high
---

# SKILL: VPS Management

> **DITEMPA BUKAN DIBERI — VPS is the body's nervous system.**
> **Source:** `/root/.opencode/skills/vps-management/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Managing VPS server via SSH
- Docker container management, system monitoring
- Firewall rules, backups, server optimization
- Full root access to srv1325122.hstgr.cloud (72.62.71.199)
- Keywords: VPS, SSH, docker, devops, server-management, monitoring

---

## Connection

| Property | Value |
|----------|-------|
| Host | 72.62.71.199 |
| User | root |
| Port | 22 |
| Method | SSH with password |

All commands: `ssh root@72.62.71.199 "<command>"`

---

## Operating Principles

1. **Safe always** — Never destructive commands without explicit confirmation
2. **Diagnose first** — Check state before acting
3. **Verify after** — Confirm results with follow-up queries
4. **Disk hygiene** — Safe prune monthly or when disk >70%
5. **Backup before destructive** — Warn if data loss risk

---

## Command Reference

### System Status
```bash
ssh root@72.62.71.199 "uptime && free -h && df -h"
ssh root@72.62.71.199 "docker ps -a"
ssh root@72.62.71.199 "docker system df"
```

### Container Lifecycle
```bash
ssh root@72.62.71.199 "docker restart <container>"
ssh root@72.62.71.199 "docker logs --tail 50 -f <container>"
ssh root@72.62.71.199 "docker exec -it <container> /bin/sh"
```

### Docker Compose
```bash
ssh root@72.62.71.199 "cd /root/compose && docker compose ps"
ssh root@72.62.71.199 "cd /root/compose && docker compose config"
```

### Disk Cleanup (Safe)
```bash
ssh root@72.62.71.199 "docker builder prune -f && docker image prune -f"
```

---

## Current Stack (arifOS Federation)

| Service | Port |
|---------|------|
| arifOS | 8080 |
| A-FORGE | 7071 |
| GEOX | 8081 |
| WEALTH | 8082 |
| Vault999 | 5001, 8100 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Qdrant | 6333 |
| Caddy | 80/443 |
| Ollama | 11434 |
| uptime-kuma | 8086 |
| AAA A2A | 3001 |
| HERMES | 3002 |
| Vaultwarden | 8085 |

---

## Related Pages

- [[skill-vps-docker]] — Docker container lifecycle
- [[skill-vps-audit]] — full system audit
- [[skill-docker-thermodynamics]] — entropy management
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — VPS managed. Federation healthy.*
