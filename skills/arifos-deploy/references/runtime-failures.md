# Runtime Failure Patterns — arifOS MCP VPS

**Assumed context:** VPS access via `ariffazil@100.111.84.52:22888`. Running containers via `docker` on the VPS host.

---

## Pattern 1: F13 KERNEL PANIC — Vault Path Permission Error

**Symptom:** `/health` returns HTTP 500 with `PermissionError: [Errno 13] Permission denied: '/root/arifOS/VAULT999'`

**Root cause:** `federation_epistemology.py` (inside container) defaults `VAULT999_PATH` to `/root/arifOS/VAULT999` when the env var is unset. The container user is `arifos` (uid 1000), which has no write permission on that host path. The actual vault data lives at `/root/volumes/vault999` (bind-mounted to `/var/lib/arifos/vault` inside the container).

**Diagnosis:**
```bash
# Step 1: Confirm the error in logs
docker logs arifosmcp --tail 40 2>&1 | grep -E "VAULT999|PermissionError|KERNEL PANIC"

# Step 2: Verify the vault path env var is missing inside container
docker exec arifosmcp env | grep VAULT999_PATH
# Expected (if broken): empty output

# Step 3: Check what the container user can actually write to
docker exec arifosmcp id
# Expected: uid=1000(arifos)

# Step 4: Confirm the bind mount target is uid 1000
ls -la /root/volumes/vault999
# Expected: drwxr-xr-x 1000:1000 ...
```

**Fix — add missing env var to compose:**
```bash
# Edit /root/arifOS/deploy/docker-compose.yml — add to arifosmcp environment block:
VAULT999_PATH: /var/lib/arifos/vault

# Then restart (docker compose up -d reads the env_file and environment block):
docker compose -f /root/arifOS/deploy/docker-compose.yml up -d arifosmcp

# Wait for health:
sleep 12 && curl -s http://127.0.0.1:8080/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['status'], d.get('vault999_health',''))"
# Expected: healthy healthy
```

**Why this survives restarts:** The compose file is the persistent definition. `docker compose up -d` reads it on every start. The env var must be in the YAML, not added manually to the running container.

**Blast radius:** Zero. Changing `VAULT999_PATH` only redirects where the epistemology DB is written. Existing data at `/root/volumes/vault999` is unaffected.

**Indicator that the fix worked:** `vault999_health: "healthy"` in `/health` JSON response.

---

## Pattern 2: 406 Not Acceptable on MCP POST

**Symptom:** `POST /mcp` returns HTTP 406 with `406 Not Acceptable`. Tools list works (`GET /mcp` returns 200).

**Root cause:** Usually a missing `Accept: application/json` header on the POST request, OR the server is rejecting the JSON-RPC content type.

**Diagnosis:**
```bash
# Does tools/list work?
curl -s -X POST http://127.0.0.1:8080/mcp \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Check logs for what the 406 is about
docker logs arifosmcp --tail 20 2>&1 | grep 406
```

**Fix:** Always include both headers:
```
-H "Accept: application/json" \
-H "Content-Type: application/json"
```

---

## Pattern 3: Container UNHEALTHY — healthcheck failing

**Symptom:** `docker ps` shows `(unhealthy)` or `(health: starting)` indefinitely.

**Diagnosis:**
```bash
# Check healthcheck test
docker inspect arifosmcp --format '{{json .HostConfig.Healthcheck.Test}}'

# Run the healthcheck manually inside the container
docker exec arifosmcp python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Check what the /health endpoint actually returns
curl -s http://127.0.0.1:8080/health
```

**Common causes:**
- Port mismatch: container port 8080 not bound to host 127.0.0.1:8080
- App crashed on startup — check `docker logs arifosmcp --tail 50` for traceback
- Dependency containers (postgres, headless_browser) not yet healthy

---

## Health Check Sequence

When diagnosing any runtime issue on VPS, run in order:

```bash
# 1. Container list — who is down?
docker ps -a --format "table {{.Names}}\t{{.Status}}"

# 2. Full logs for the sick container
docker logs arifosmcp --tail 80 2>&1

# 3. Health endpoint
curl -s http://127.0.0.1:8080/health | python3 -m json.tool | grep -E "status|vault999|federation_epistemology|error"

# 4. MCP tools list (confirms server is responding)
curl -s -X POST http://127.0.0.1:8080/mcp \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['result']['tools']),'tools')"

# 5. Vault persistence check
docker exec arifosmcp ls -la /var/lib/arifos/vault/
```

---

## Vault Path Quick Reference

| Location | Host path | Container path | Used by |
|----------|-----------|---------------|---------|
| Vault volume | `/root/volumes/vault999` | `/var/lib/arifos/vault` | vault999 container |
| Epistemology DB | — | `/var/lib/arifos/vault/federation_epistemology.db` | arifosmcp (needs `VAULT999_PATH=/var/lib/arifos/vault`) |
| Host code (ro mount) | `/root/arifOS/arifosmcp/` | `/app/arifosmcp/` | arifosmcp |
