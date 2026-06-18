---
name: federation-orchestrator
description: >
  Monitor and manage the arifOS federation: docker compose ps, restart dead services,
  MCP health probes (8080-8083), container drift detection, restart count monitoring.
  USE WHEN: "federation status", "restart dead container", "container health",
  "docker drift", "service down", "probe MCP", "health check federation".
  Runs on af-forge (VPS) — native docker and curl required.
---

# Federation Orchestrator

**arifOS federation infrastructure operator. Monitors, recovers, and reports on all federation nodes.**

## Capabilities

- `docker compose ps` across all federation stacks
- Container restart count tracking (flag containers with >3 restarts)
- MCP endpoint health probes (8080-8083)
- Dead service auto-restart (with confirmation threshold)
- Federation status report generation
- Restart history audit

## Commands

```bash
# Full federation status
docker compose ps
docker ps -a --filter "status=restarting"

# Check MCP endpoints
curl -s --max-time 5 http://localhost:8080/health
curl -s --max-time 5 http://localhost:8081/health
curl -s --max-time 5 http://localhost:8082/health
curl -s --max-time 5 http://localhost:8083/health

# Restart dead container
docker compose restart <service>
docker restart <container>

# Restart count audit
docker inspect --format='{{.Name}} {{.RestartCount}}' $(docker ps -aq)

# Federation stack locations
cd /root/arifOS && docker compose ps
cd /root/AAA && docker compose ps
```

## Health Probe Script

```bash
#!/bin/bash
# Probe all MCP endpoints
for port in 8080 8081 8082 8083; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:$port/health)
  if [ "$code" = "200" ]; then
    echo "✅ MCP:$port OK"
  else
    echo "❌ MCP:$port FAILED (HTTP $code)"
  fi
done
```

## Restart Count Thresholds

| Restarts | Severity | Action |
|---|---|---|
| 0 | ✅ Healthy | No action |
| 1–3 | ⚠️ Watch | Log + warn |
| 4–9 | 🔴 Degraded | Alert + review |
| 10+ | ⛔ Critical | Auto-restart cooldown + human alert |

## Federation Nodes

| Container | Port | Stack | Criticality |
|---|---|---|---|
| arifosmcp | 8080 | arifOS | CRITICAL |
| geox_eic | 8081 | GEOX | CRITICAL |
| wealth-organ | 8082 | WEALTH | HIGH |
| well | 8083 | WELL | HIGH |
| vault999 | — | Vault999 | CRITICAL |
| vault999-writer | — | Vault999 | HIGH |
| graphiti-mcp | — | arifOS | HIGH |
| postgres | 5432 | arifOS | CRITICAL |
| qdrant | 6333 | arifOS | HIGH |
| redis | 6379 | arifOS | HIGH |
| nats | 4222 | arifOS | MEDIUM |
| aaa-a2a | 3001 | AAA | HIGH |
| apex-prime | 3002 | APEX | HIGH |
| ollama-engine-prod | 11434 | Ollama | MEDIUM |
| headless_browser | — | Browser | MEDIUM |
| uptime-kuma | 3001 | Monitoring | LOW |
| searxng | 8080 | Search | LOW |
| netdata | 19999 | Monitoring | LOW |
| vaultwarden | 8080 | Security | MEDIUM |
| agent-zero | — | AAA | HIGH |
| forge-notifier | — | Notification | MEDIUM |
