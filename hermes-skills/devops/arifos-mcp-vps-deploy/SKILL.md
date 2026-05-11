---
name: arifos-mcp-vps-deploy
description: Deploy and debug arifosmcp on VPS — non-root container, ephemeral /app/ layer, Python package installation, and permanent startup bootstrap
tags: [arifosmcp, docker, vps, deployment, python-packages]
related_skills: [fastmcp-container-restart-debug]
---

# arifOS MCP — VPS Production Deploy

## Problem Patterns

1. **arifosmcp restart loop** — container keeps restarting, `docker ps` shows "Restarting"
2. **Python package missing** — `ModuleNotFoundError: No module named 'asyncpg'` inside container
3. **Import errors on boot** — `SyntaxError` or `ImportError` from baked image files
4. **Env vars not persisting** — DATABASE_URL, QDRANT_URL, OLLAMA_URL missing inside container
5. **Container healthy but app dead** — container "Up X minutes (healthy)" but `/health` returns nothing

## Diagnostic First

```bash
# 1. Check restart loop
docker ps --format "{{.Names}}\t{{.Status}}" | grep arifosmcp

# 2. Restart count + exit code
docker inspect arifosmcp --format 'restart={{.RestartCount}} exit={{.State.ExitCode}} error={{.State.Error}}'

# 3. Actual container logs
docker logs arifosmcp --tail 100 2>&1

# 4. What code path is actually running?
docker exec arifosmcp sh -c 'ls -la /app/arifosmcp/runtime/tools.py /usr/src/app/arifosmcp/runtime/tools.py 2>&1 | grep -v "cannot access"'

# 5. Is the app listening?
docker exec arifosmcp sh -c 'ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null'
```

## Root Causes Found (arifosmcp on srv1325122)

### Cause 1: SyntaxError in baked image tools.py
The VPS image has a stale `tools.py` with `global _memory_engine` at line 2312 used before its declaration (referenced at line 2307 inside a nested `if` block). This is a Python scoping violation.

**Temporary fix** (survives `docker restart`, NOT `docker rm`):
```bash
docker cp /root/arifOS/arifosmcp/runtime/tools.py arifosmcp:/app/arifosmcp/runtime/tools.py
docker cp /root/arifOS/arifosmcp/memory_engine.py arifosmcp:/app/arifosmcp/memory_engine.py
docker restart arifosmcp
```

### Cause 2: Container runs as non-root (arifos:arifos)
The Dockerfile switches to `USER arifos`. pip cannot write to system site-packages. Package installation to `/tmp/pylibs` is required.

**Temporary fix**:
```bash
docker exec arifosmcp sh -c "pip install --target=/tmp/pylibs asyncpg qdrant-client 2>&1 | tail -3"
```

### Cause 3: Docker-compose mount paths are wrong
Compose file specifies:
```yaml
volumes:
  - /root/arifOS/arifosmcp:/usr/src/app/arifosmcp:ro
```

But `/usr/src/app/arifosmcp` does NOT exist inside the running container. All code lives in `/app/arifosmcp/` (ephemeral image layer). Fixes to `/app/` survive restarts but are lost on `docker rm`.

## Permanent Fix: Startup Bootstrap Script

Create a startup script that installs packages on each container start, then runs the server as the non-root user:

### 1. Create startup.sh
```bash
#!/bin/bash
set -e

echo "[bootstrap] Installing Python packages..."
pip install --target=/tmp/pylibs asyncpg qdrant-client --quiet 2>&1 | tail -2

echo "[bootstrap] Starting arifOS MCP server..."
export PYTHONPATH="/tmp/pylibs:/app:$PYTHONPATH"
export DATABASE_URL="${DATABASE_URL:-postgresql://arifos_admin:ArifPostgresVault2026!@postgres:5432/vault999}"
export QDRANT_URL="${QDRANT_URL:-http://qdrant:6333}"
export OLLAMA_URL="${OLLAMA_URL:-http://ollama:11434}"
export EMBEDDING_MODEL="${EMBEDDING_MODEL:-bge-m3}"

exec python -m arifosmcp.runtime.__main__
```

### 2. Update Dockerfile ENTRYPOINT
```dockerfile
COPY --chown=arifos:arifos deployments/af-forge/startup.sh /usr/local/bin/startup.sh
RUN chmod +x /usr/local/bin/startup.sh
ENTRYPOINT ["/usr/local/bin/startup.sh"]
```

### 3. Add environment variables to docker-compose
```yaml
environment:
  PYTHONPATH: "/tmp/pylibs:/app"
  DATABASE_URL: "postgresql://arifos_admin:ArifPostgresVault2026!@postgres:5432/vault999"
  QDRANT_URL: "http://qdrant:6333"
  OLLAMA_URL: "http://ollama:11434"
  EMBEDDING_MODEL: "bge-m3"
  ARIFOS_MCP_TRANSPORT: http
  ARIFOS_MCP_HOST: 0.0.0.0
  ARIFOS_MCP_PORT: 3000
```

### 4. Fix docker-compose volumes (so source mount actually works)
The mount path in compose must match where the container expects code. If container uses `/app/`, either:
- Change compose mount to `- /root/arifOS/arifosmcp:/app/arifosmcp:ro`
- OR keep `/app/` as-is and rely on the startup script (no mount needed)

## Health Check Pattern

After fixing, verify with:
```bash
# Container should be healthy
docker ps --format "{{.Names}}\t{{.Status}}" | grep arifosmcp
# Expected: "arifosmcp    Up X minutes (healthy)    restart=0"

# App should be reachable
docker exec arifosmcp sh -c 'curl -sf http://localhost:3000/health || curl -sf http://localhost:3000/ || echo "no_health_endpoint"'

# Memory engine should work
docker exec \
  -e PYTHONPATH=/tmp/pylibs:/app \
  -e DATABASE_URL="postgresql://arifos_admin:ArifPostgresVault2026!@postgres:5432/vault999" \
  -e QDRANT_URL="http://qdrant:6333" \
  -e OLLAMA_URL="http://ollama:11434" \
  -e EMBEDDING_MODEL="bge-m3" \
  arifosmcp \
  python3 -c "from arifosmcp.memory_engine import MemoryEngine; print('MemoryEngine OK')"
```

## MCP Transport Types and Caddyfile Routing

arifOS federation has **two distinct MCP transport types** — routing them correctly in Caddyfile is critical.

### Type 1: streamable_http (stateless) — arifOS MCP
```python
# arifOS: stateless streamable_http
app = mcp.http_app(stateless_http=True)
# Transport: POST /mcp with JSON body, GET /mcp for SSE fallback
# Caddyfile needs: handle /mcp, handle /mcp/*, handle /health
```
**Caddyfile routing** (stateless HTTP):
```
handle /mcp { reverse_proxy <container>:<port> { flush_interval -1 } }
handle /mcp/* { reverse_proxy <container>:<port> { flush_interval -1 } }
handle /health { reverse_proxy <container>:<port> }
```

### Type 2: streamable_http + SSE session (WEALTH, GEOX, WELL)
```python
# WEALTH/GEOX/WELL: SSE session transport
app = mcp.streamable_http_app()
# GET /mcp → returns event stream with session_id in first message:
#   data: /messages/?session_id=<uuid>
# POST /messages/?session_id=<uuid> → send JSON-RPC method calls
# POST /mcp → returns "Missing session ID" error
```
**Caddyfile routing** (SSE session — REQUIRES /messages/ route):
```
handle /mcp { reverse_proxy <container>:<port> { flush_interval -1 } }
handle /mcp/* { reverse_proxy <container>:<port> { flush_interval -1 } }
handle /messages/* { reverse_proxy <container>:<port> { flush_interval -1 } }
handle /health { reverse_proxy <container>:<port> }
handle { reverse_proxy <container>:<port> }
```

**Without `/messages/*` route**: MCP clients using SSE transport fail silently — `GET /mcp` returns session_id, but POSTs to `/messages/` get 404 and the session dies.

### Type 3: Express HTTP (A-FORGE bridge, AAA A2A)
```javascript
// A-FORGE: Express HTTP + SSE
// AAA A2A: Express JSON-RPC
app.get('/health', ...)     // GET /health → health JSON
app.post('/message/send')   // POST /message/send → A2A message
```
**Caddyfile routing**:
```
handle /mcp { reverse_proxy <container>:<port> { flush_interval -1 } }
handle /mcp/* { reverse_proxy <container>:<port> { flush_interval -1 } }
handle /health { reverse_proxy <container>:<port> }
handle /contract { reverse_proxy <container>:<port> }  # A-FORGE only
handle /a2a/* { reverse_proxy <container>:<port> }     # AAA A2A only
handle { reverse_proxy <container>:<port> }
```

### Known MCP container endpoints
| Container | Port | Transport | Public Domain |
|-----------|------|----------|--------------|
| `arifosmcp` | 8080 | streamable_http (stateless) | `mcp.arif-fazil.com`, `arifos.arif-fazil.com` |
| `geox` | 8081 | SSE session | `geox.arif-fazil.com` |
| `well` | 8083 | SSE session | `well.arif-fazil.com` |
| `wealth-organ` | 8082 | SSE session | `wealth.arif-fazil.com` |
| `af-bridge-prod` | 7071 | Express HTTP | `forge.arif-fazil.com` |
| `aaa-a2a` | 3001 | Express HTTP | `aaa.arif-fazil.com/a2a/*` |

## AAA A2A Routing Bug

**Bug**: `aaa.arif-fazil.com/a2a/*` was routing to `arifosmcp:8080` instead of `aaa-a2a:3001`. This is a critical A2A routing error.

**Fix**: In Caddyfile, ensure:
```
aaa.arif-fazil.com {
    ...
    handle /a2a/* { reverse_proxy aaa-a2a:3001 }
    handle /health { reverse_proxy aaa-a2a:3001 }
}
```

## Key Lesson

**On this VPS**: The docker-compose source mount (`/root/arifOS/arifosmcp:/usr/src/app/arifosmcp:ro`) is BROKEN — the target path doesn't exist inside the container. The container's `/app/` is ephemeral image layer. Permanent fixes require either:
1. Fixing the mount path in docker-compose to match actual container code location, OR
2. Baking fixes into the image via Dockerfile updates + rebuild

The startup script approach (option 2 alternative) installs packages at runtime and works even without a correct source mount.

**AAA version hardcoding**: AAA's `server.js` has hardcoded `version: '0.3.0'` in the A2A agent card AND `/health` response — package.json says `1.0.0`. If rebuilding the `aaa-a2a` image from source, update `server.js` line ~30 and line ~245 before building, OR add env var support and set in docker-compose.

## Postgres Credentials (srv1325122)
- User: `arifos_admin`
- Password: `ArifPostgresVault2026!`
- Database: `vault999`
- Host: `postgres` (from container network)
- Connection: `postgresql://arifos_admin:ArifPostgresVault2026!@postgres:5432/vault999`
- Note: Local unix socket uses `trust` auth — `gosu postgres psql -U arifos_admin -d vault999` works without password
