---
name: arifos-loki-healthcheck-fix
description: Fix Loki 3.x single-binary healthcheck returning 503 — use /loki/api/v1/label instead of /ready
triggers:
  - "Loki container unhealthy in docker-compose"
  - "/ready returns 503 in Loki single-binary mode"
  - "depends_on service_healthy blocks Loki stack"
category: devops
---

# arifOS — Loki 3.x Single-Binary Healthcheck Fix

## Problem
When deploying Loki 3.x in single-binary mode (one container, not distributed),
`/ready` returns HTTP 503 even when Loki is functioning. Docker compose's
`depends_on: condition: service_healthy` blocks the entire stack from starting.

## Symptom
```
container arifos-loki is unhealthy
dependency failed to start: container arifos-loki is unhealthy
```

Yet `curl http://localhost:3100/loki/api/v1/label` returns HTTP 200 with actual data.

## Root Cause
Loki 3.x single-binary mode disables the readiness probe endpoint.
The frontend/query components are not fully initialized in single-instance mode,
causing `/ready` to report not-ready.

## Fix
**In docker-compose.yml for Loki service:**

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -sf http://localhost:3100/loki/api/v1/label || exit 1"]
  interval: 15s
  timeout: 5s
  retries: 3
  start_period: 10s
```

Use `/loki/api/v1/label` instead of `/ready`. This endpoint returns HTTP 200
when Loki's HTTP API is listening, sufficient for a single-binary setup.

## Additional Notes
- Loki 3.x runs as UID 10001 by default. Mounted volumes must be chown'd:
  `chown -R 10001:10001 /path/to/loki-data`
- `wget` is not available in Alpine-slim based Loki images. Use `curl` or `python3`.
- Grafana UID 472, not 10001.

## Trigger
When deploying Loki via docker-compose in arifOS stack.
