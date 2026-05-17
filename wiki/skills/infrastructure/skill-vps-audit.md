---
title: "SKILL: VPS Health Audit"
type: skill
version: 1.0.0
category: infra
risk_band: LOW
floors: []
evidence_required: false
sources: [/root/.opencode/skills/vps-audit/SKILL.md]
confidence: high
---

# SKILL: VPS Health Audit

> **Source:** `/root/.opencode/skills/vps-audit/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Auditing VPS health, server condition
- System resource inspection (disk, memory, CPU)
- Security scanning, service monitoring
- Investigating system anomalies
- Keywords: VPS audit, health, monitoring, system-status

---

## Full Audit Sequence

### 1. Disk
```bash
df -h | awk 'NR==1 || $5+0 > 75 {print}'
du -sh /var/log/* 2>/dev/null | sort -rh | head -10
```

### 2. Memory & Swap
```bash
free -h
cat /proc/meminfo | grep -E "MemTotal|MemAvailable|SwapTotal|SwapFree"
```

### 3. CPU Load
```bash
uptime
top -bn1 | head -15
```

### 4. Systemd Failed Services
```bash
systemctl --failed
systemctl status caddy docker
```

### 5. Docker Health
```bash
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.RunningFor}}"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
docker system df
```

### 6. Security Scan
```bash
ss -tulpn
journalctl -u ssh --since "24h ago" | grep -c "Failed"
last -n 10
ufw status verbose 2>/dev/null || iptables -L INPUT -n
```

### 7. Caddy + FastMCP Health
```bash
systemctl is-active caddy
curl -sf http://localhost:8000/health && echo "FastMCP OK" || echo "FastMCP DOWN"
```

---

## Output Format

Report with severity tags:
- **[CRITICAL]** — Immediate action, service impacted
- **[HIGH]** — Fix within 24h
- **[MEDIUM]** — Fix within week
- **[LOW]** — Nice to have
- **[OK]** — Healthy

End with: **Action Items** sorted by severity.

---

## Known Services to Monitor

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
| WELL | 8083 |
| Vaultwarden | 8085 |

---

## Related Pages

- [[skill-vps-management]] — VPS management
- [[skill-vps-docker]] — Docker container audit
- [[skill-docker-security]] — security hardening
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Audit complete. Status known.*
