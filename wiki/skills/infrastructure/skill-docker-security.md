---
title: "SKILL: Docker Security"
type: skill
version: 1.0.0
category: security
risk_band: HIGH
floors: [F1, F11]
evidence_required: true
sources: [/root/.opencode/skills/docker-security/SKILL.md]
confidence: high
---

# SKILL: Docker Security

> **Source:** `/root/.opencode/skills/docker-security/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Auditing Docker containers for security
- Setting resource limits
- Hardening Docker configuration
- Port audits, UFW firewall checks
- Keywords: docker security, resource limits, container hardening, port audit

---

## Quick Security Audit

```bash
# 1. Check exposed ports
ss -tlnp | grep -v "127.0.0.1" | grep -v "::1"
# Only SSH (22888), HTTP (80), HTTPS (443), Tailscale (51820) should show

# 2. Check UFW status
ufw status verbose

# 3. Check Docker socket permissions
ls -la /var/run/docker.sock
# Should be: srw-rw---- 1 root docker

# 4. Check for privileged containers
docker ps --format "{{.Names}}" | while read c; do
  docker inspect "$c" --format "{{.Name}}: Privileged={{.HostConfig.Privileged}}"
done

# 5. Check container resource limits
docker stats --no-stream --format "table {{.Name}}\t{{.MemPerc}}\t{{.MemUsage}}"
```

---

## Expected Port State

| Port | Interface | Service | Public? |
|------|-----------|---------|---------|
| 22888 | 0.0.0.0 | SSH | ✅ key-only |
| 80, 443 | * | Caddy | ✅ reverse proxy |
| 51820/udp | * | Tailscale | ✅ |
| 2377, 7946 | * | Docker Swarm | ❌ DENIED |

---

## Resource Limits — Recommended

```yaml
services:
  postgres:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2'

  arifosmcp:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2'

  redis:
    deploy:
      resources:
        limits:
          memory: 768M

  ollama-engine-prod:
    deploy:
      resources:
        limits:
          memory: 6G
```

---

## F1 Amanah — Docker Rules

1. **NEVER** `docker system prune -a` without 888_HOLD + human confirmation
2. **NEVER** `docker volume prune` — remove volumes individually, approved per-volume
3. **SAFE**: `docker system prune --filter "until=168h"` (old stuff only, logged)
4. **SAFE**: `docker image prune` (dangling only)
5. Before any prune: `docker system df` first

---

## Related Pages

- [[skill-vps-docker]] — container lifecycle
- [[skill-vps-audit]] — full system audit
- [[skill-vps-management]] — VPS management
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Docker hardened. Security verified.*
