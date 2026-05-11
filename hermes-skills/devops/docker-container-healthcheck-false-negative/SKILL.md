---
name: docker-container-healthcheck-false-negative
description: When a Docker container shows (unhealthy) but the app inside is actually responding — diagnose and fix the healthcheck probe, not the app
tags: ["docker", "debugging", "healthcheck"]
category: devops
---

# docker-container-healthcheck-false-negative

## Problem
Docker reports a container as `(unhealthy)` but the application inside is actually working fine. Direct HTTP probe from host succeeds; container logs show no errors; only Docker's healthcheck fails.

## Symptoms
```
docker ps --format "{{.Names}} {{.Status}}"
hermes-agent   Up 8 minutes (unhealthy)
```

But:
```bash
# App responds from host
curl -s --max-time 5 http://127.0.0.1:3002/health
# → {"status":200}

# App responds from inside container (with wget or node)
docker exec <container> wget -q -O- --timeout=5 http://localhost:3002/health
# → 200 OK
```

## Diagnosis
The Docker healthcheck command is failing — common causes:

1. **Container has no curl/wget** — healthcheck uses `curl` but container image has no curl binary
2. **Healthcheck uses wrong port or path** — app listens on different port inside container vs host
3. **Healthcheck timeout too short** — app starts slowly, probe times out before response
4. **Network mode mismatch** — healthcheck runs from container network namespace, can't reach localhost

## Fix Patterns

### Pattern 1: App has no curl (use wget or node)
```bash
# Instead of curl, use wget (usually available)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -q -O- http://localhost:3002/health || exit 1

# Or use node built-in HTTP (no external binary needed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD node -e "const http=require('http');http.get('http://localhost:3002/health',(r=>process.exit(r.statusCode===200?0:1)))"
```

### Pattern 2: Fix the healthcheck in docker-compose.yml
```yaml
healthcheck:
  test: ["CMD", "wget", "-q", "-O-", "--timeout=5", "http://localhost:PORT/health"]
  # not curl (container may not have it)
  # not 127.0.0.1 if app only listens on localhost inside container
  interval: 30s
  timeout: 5s
  retries: 3
  start_period: 10s
```

### Pattern 3: Use a custom healthcheck script
Create a small shell script in the container:
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s CMD /app/healthcheck.sh
```

### Pattern 4: TCP port check (no HTTP needed)
```yaml
healthcheck:
  test: ["CMD-SHELL", "wget -q -O- --timeout=2 http://localhost:3002/health || exit 1"]
```

## Diagnostic Chain
```bash
# 1. Check what healthcheck command the container is running
docker inspect --format='{{json .State.Health}}' <container> | python3 -m json.tool

# 2. Check healthcheck log (last failure reason)
docker inspect --format='{{json .State.Health}}' <container> | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('Log',[])[-1])"

# 3. Check if app is actually responding from host
curl -s --max-time 5 http://127.0.0.1:<HOST_PORT>/health

# 4. Check if app is responding from inside container
docker exec <container> wget -q -O- --timeout=5 http://localhost:<INTERNAL_PORT>/health
# or
docker exec <container> node -e "const http=require('http');http.get('http://localhost:<PORT>/health',(r=>console.log(r.statusCode)))"
```

## Key Rule
**When Docker says unhealthy but app works — fix the healthcheck, not the app.** The app is fine. The probe is wrong.
