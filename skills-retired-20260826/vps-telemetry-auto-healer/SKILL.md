---
name: vps-telemetry-auto-healer
description: Real-time Caddy HTTP error spike monitor, Docker container log stream analyzer, and automated container health recovery watchdog.
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# VPS Telemetry & Auto-Healer Skill (`vps-telemetry-auto-healer`)

Monitors live container resource usage (`docker stats`), Caddy HTTP 502/504 error spikes, and container log streams to automatically triage degradation and execute governed recovery circuits.

## Diagnostic & Triage Workflow

### 1. Check Container Health & Memory Throttling
```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.PIDs}}"
```

### 2. Scan Caddy Log Stream for 502 / 504 Spikes
```bash
tail -n 200 /var/log/caddy/access.log | grep -E "status\":(502|504|500)"
```

### 3. Graceful Container Self-Healing Circuit
```bash
# Verify container failure state before restart
if ! docker inspect --format='{{.State.Health.Status}}' searxng | grep -q "healthy"; then
    echo "[AUTO-HEALER] SearXNG unhealthy. Restarting..."
    docker restart searxng
fi
```

---

## Best Practices for Federation Agents

1. **Governed Recovery**: Always verify container failure traceback before executing restart operations.
2. **Telemetry Log Receipt**: Record all auto-healing actions in `telemetry_audit.log`.
