---
name: vps-live-probe-audit
description: Systematic live-probe validation of arifOS VPS deployments — Docker containers, HTTP endpoints, container-to-container connectivity, and auth. Found 2 live bugs the original report missed.
---

# VPS Live Probe Audit — arifOS Federation

## Context
When validating a deployment report for arifOS VPS (docker-based federation), live probe
verification is MANDATORY — the report's claims are not trusted. This skill captures
the systematic approach that found two live bugs the original report missed.

## Trigger
Any "validation", "verification", "audit", "confirm" request for a VPS/deployment report
where the user wants live evidence, not trust.

## Methodology — 4-Layer Probe

### Layer 1 — Container State
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "arif|loki|grafana|promtail|nats|wealth|well|forge" | sort
```
Purpose: Confirm containers are running, healthy/unhealthy, port bindings.

### Layer 2 — Endpoint Reachability (from HOST)
```bash
# HTTP health endpoints
curl -s --max-time 5 http://localhost:PORT/health

# Loki special case — /ready not /health
curl -s --max-time 5 http://localhost:3100/ready

# NATS internal-only check (should be connection refused from host)
curl -s --max-time 5 http://localhost:4222/healthz
```

### Layer 3 — Container-to-Container Connectivity (from WITHIN container)
```bash
docker exec CONTAINER sh -c "python3 -c \"
import urllib.request
try:
    r = urllib.request.urlopen('http://TARGET:PORT/path', timeout=8)
    print('OK', r.status)
except Exception as e:
    print('FAIL —', str(e)[:80])
\""
```
CRITICAL: Container names differ from docker-compose service names:
- Actual: `arifosmcp` — NOT `arifOS`
- Actual: `wealth-organ` — NOT `wealth`
- Actual: `well` — correct
- Actual: `vault999` — the arifOS vault service

**Tools inside containers are LIMITED** — `wget`, `nc`, `curl` may not be installed.
Use Python stdlib (`urllib.request`, `socket`) as universal probe.

### Layer 4 — Postgres Auth Check
```bash
docker exec arifosmcp sh -c "python3 -c \"
import psycopg2
conn = psycopg2.connect(host='TARGET_IP', port=5432, user='USER', password='PW', database='DB')
print('CONNECT_OK')
conn.close()
\""
```
If TCP connects but auth fails → credentials are NOT propagated to the container,
even if `POSTGRES_URL` exists in the compose `.env` file.

## Known Bugs Found (2026-05-07)

### Bug 1 — Loki Cardinality Overflow (P0)
**Symptom:** Loki logs show repeated:
```
level=error caller=manager.go:50 component=distributor path=write
"entry for stream has 16 label names; limit 15"
```
**Root cause:** Docker compose metadata label `com_docker_compose_replace=true` on
`arifos-promtail` container adds 16th label. Loki's `max_label_names_per_stream=15`.

**Fix:** The correct `promtail-config.yaml` with `labeldrop` rules already exists at
`/root/compose/promtail-config.yaml` but is a VOLUME MOUNT — changes to the file
do NOT update the running container. Must restart the container:
```bash
docker compose -f /root/compose/docker-compose.yml restart arifos-promtail
```

**Verification:**
```bash
# Before fix: errors every ~5s
docker logs arifos-loki --since 2m 2>&1 | grep "16 label names"

# After fix: no such errors
```

### Bug 2 — Postgres Credentials Not Propagated to arifosmcp
**Symptom:** `POSTGRES_URL` in `.env` shows `arifos_admin:***@postgres:5432/vault999`,
but `docker exec arifosmcp env | grep POSTGRES` returns NOTHING.

**Root cause:** arifosmcp docker-compose service definition does NOT reference the
`POSTGRES_URL` env var — it is defined for other services (vault999, arifos) but not
injected into the arifosmcp container's environment.

**Status:** vault999 connects fine (healthy). arifosmcp cannot authenticate.

**Fix (P1):** Add `POSTGRES_URL` env var to arifosmcp service in docker-compose.yml:
```yaml
arifosmcp:
  environment:
    POSTGRES_URL: postgresql://arifos_admin:${POSTGRES_PASSWORD}@postgres:5432/vault999
```

## Network Topology (Verified 2026-05-07)
```
arifosmcp is on 3 networks simultaneously:
  - af-forge_arifos-network: 172.20.0.3  (→ Loki, Grafana, NATS, Promtail)
  - arifos_core_network: 172.19.0.2        (→ Postgres vault999 at 172.19.0.5)
  - bridge: 172.17.0.4                    (→ WEALTH at 172.17.0.2, WELL at 172.17.0.3)

WEALTH reachable: arifosmcp(bridge) → 172.17.0.2:8082 ✅
WELL reachable: arifosmcp(bridge) → 172.17.0.3:8083 ✅
Postgres TCP: arifosmcp → 172.19.0.5:5432 = OPEN ✅
Postgres auth: FAILS ❌ (credentials not propagated)
```

## Key Lesson
The gap between "service definition in docker-compose.yml" and "running container
with propagated env" is a persistent source of false-positive health claims.
Always probe FROM the container itself, not just from the host.

## File References
- `/root/compose/docker-compose.yml` — main stack definition
- `/root/compose/promtail-config.yaml` — promtail config (labeldrop rules here but not applied)
- `/root/compose/.env` — credentials source (verify what's actually injected)
