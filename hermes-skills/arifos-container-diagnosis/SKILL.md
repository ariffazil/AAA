---
name: arifos-container-diagnosis
description: "Diagnose broken arifOS Federation containers: wrong image, wrong entry point, port mismatches, import chain failures. Use when a container won't start, serves wrong content, or shows as unhealthy despite having a valid image."
triggers: ["502", "GEOX broken", "container won't start", "wrong image", "import error", "port mismatch", "geox_mcp_server not found", "healthcheck failing", "FastMCP 406", "qdrant healthcheck", "docker health: starting forever", "Caddy 502 arifosmcp", "arifOS MCP unreachable"]
tags: ["arifOS", "docker", "debug", "container", "geox", "mcp"]
category: devops
---

# arifOS Container Diagnosis

## The arifOS Federation Pattern

Images like `arifos-geox:v1.0.0` often contain MULTIPLE possible entry points:
- `arifosmcp/runtime/server.py` — arifOS kernel
- `geox_mcp/server.py` — GEOX FastMCP
- `geox_unified_mcp_server.py` — GEOX unified shim
- Legacy paths in `arifosmcp/geox/legacy_servers/`

The container CMD in the Dockerfile may be wrong, but the actual server files usually exist inside.

## Diagnosis Pipeline

### Step 1 — Find what's actually running
```bash
docker exec <container> cat /proc/1/cmdline | tr '\0' ' '
docker inspect <container> --format '{{.Config.Cmd}}'
```

### Step 2 — Find all server entry points inside
```bash
docker exec <container> find / -name "*.py" -path "*/server.py" 2>/dev/null | grep -v __pycache__
docker exec <container> find /usr/src/app -name "*mcp_server.py" 2>/dev/null
docker exec <container> find /app -name "*mcp_server.py" 2>/dev/null
```

### Step 2b — Overlayfs or Persistent?
```bash
docker inspect <container> --format '{{json .Mounts}}'
```
Empty Mounts = overlayfs (ephemeral /app). All `/app` edits survive `docker restart` but NOT image rebuild.

**If overlayfs**: Find the host source path by matching the container's CMD to a host workspace file:
```bash
docker inspect <container> --format '{{.Config.Cmd}}'
# e.g. [python control_plane/fastmcp/server.py]
find /root -type d -name "control_plane" 2>/dev/null | head -5
# → /root/geox/control_plane
```

**Test persistence**: Edit a file, `docker restart`, verify edit survived. If gone → overlayfs.

### Step 3 — Persistent Fixtures
Never use `/tmp/` for fixtures inside overlayfs containers — wiped on every restart:
```bash
docker exec <container> mkdir -p /data/fixtures
docker cp fixtures/BOKOR_1_demo.las <container>:/data/fixtures/
```

### Step 4 — Test import chains
```bash
docker exec <container> python3 -c "
import sys
sys.path.insert(0, '/path/to/parent/dir')
try:
    from module.path import mcp
    print('OK - mcp imported')
    app = mcp.streamable_http_app()
    print('OK - app created')
except Exception as e:
    print('ERROR:', type(e).__name__, str(e)[:200])
"
```

### Step 4 — Find listening ports inside container
```bash
docker exec <container> python3 -c "
import socket
for port in [5000, 5001, 8000, 8001, 8080, 8081, 8082, 9000]:
    s = socket.socket()
    s.settimeout(0.3)
    try:
        s.connect(('127.0.0.1', port))
        print(f'Port {port}: OPEN')
    except:
        print(f'Port {port}: closed')
    s.close()
"
```

### Step 5 — Find correct PYTHONPATH
```bash
docker exec <container> python3 -c "import sys; print(sys.path[:3])"
```

## Common Fixes

### Wrong entry point (arifOS instead of GEOX)
```bash
# arifOS runs on 8080, GEOX needs 8081
# Override CMD with:
python3 -c "import uvicorn; from geox_mcp.server import mcp; uvicorn.run(mcp.streamable_http_app(), host='0.0.0.0', port=8081)"
```

### qdrant — no curl inside container
qdrant image has no `curl` and `python3` is not available via CMD-SHELL. If healthcheck fails with "executable file not found", either remove the healthcheck (service is fine) or use a host-side check. Do NOT assume CMD-SHELL runs on the host.

### Port mapping mismatch
```yaml
# WEALTH: uvicorn inside 8082, compose mapped 8000:8000 (wrong) → 8000:8082 (correct)
ports:
  - "127.0.0.1:8000:8082"
```

### MCP SSE server has no /health endpoint
FastMCP's `streamable_http_app()` exposes only `/mcp`, not `/health`. GET requests return 406.
The working healthcheck uses curl with POST + proper Accept headers:

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -sf -X POST http://localhost:8081/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\",\"id\":1,\"params\":{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{},\"clientInfo\":{\"name\":\"health\",\"version\":\"1.0\"}}}' --max-time 3"]
  interval: 30s
  timeout: 10s
  retries: 3
```

The python3 urllib approach fails because FastMCP returns 406 on GET. Only POST with SSE Accept headers works.

## GEOX Compose Template (correct)
```yaml
  geox:
    image: arifos-geox:v1.0.0
    container_name: geox
    restart: unless-stopped
    command: >
      /bin/sh -c "python3 -c 'import uvicorn; from geox_mcp.server import mcp;
      uvicorn.run(mcp.streamable_http_app(), host=\"0.0.0.0\", port=8081)'"
    environment:
      PYTHONPATH: /usr/src/app/arifosmcp/geox
      PORT: "8081"
    ports:
      - "127.0.0.1:8081:8081"
    networks: [arifos_core]
    healthcheck:
      test: ["CMD-SHELL", "curl -sf -X POST http://localhost:8081/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{\"jsonrpc\":\"2.0\",\"method\":\"initialize\",\"id\":1,\"params\":{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{},\"clientInfo\":{\"name\":\"health\",\"version\":\"1.0\"}}}' --max-time 3"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

## 502 Bad Gateway — arifOS MCP specific (critical path)

Three distinct root causes found 2026-05-04. Diagnose in order:

### 1. Network isolation (most common after restart)
Caddy and arifOS MCP may be on different Docker bridge networks after `docker restart`.
```
Symptom: Caddy logs show empty response; arifosmcp health endpoint inside container works fine.
Test: docker exec caddy wget -O- http://arifosmcp:8080/health
If "bad address" → network isolation.

Fix: docker network connect arifos_core_network arifosmcp
(Caddy is on arifos_core_network; arifOS MCP may be on default bridge.)
```

### 2. Stale image (git metadata missing)
`docker build` without `--build-arg DEPLOY_GIT_COMMIT` produces image labeled `unknown`.
```
Symptom: /health shows "version: kanon-unknown" and "git_commit: unknown"
         but docker ps shows the correct tag (e.g., de038a0f).
         Container may also show wrong entrypoint (see TWO Dockerfiles above).

Fix — two parts:

(a) Use correct Dockerfile (root-level, not arifosmcp/Dockerfile):
  cd /root/arifOS && docker build -f Dockerfile -t ghcr.io/ariffazil/arifos:<tag> .

(b) Pass git metadata at run time:
  docker run -d ... -e DEPLOY_GIT_COMMIT=<sha> ghcr.io/ariffazil/arifos:<tag>

Or bake in at build time — add to Dockerfile:
  ARG DEPLOY_GIT_COMMIT=unknown
  ENV DEPLOY_GIT_COMMIT=${DEPLOY_GIT_COMMIT}

Then rebuild with:
  docker build --build-arg DEPLOY_GIT_COMMIT=$(git rev-parse --short HEAD) \
    -f Dockerfile -t ghcr.io/ariffazil/arifos:<tag> .
```

### 3. snarkjs not in container
snarkjs installed on VPS host is NOT inside the Docker image.
```
Symptom: _snarkjs_available() returns False inside container.
         VPS host has snarkjs but container does not.

Fix: Add to Dockerfile runtime stage:
  RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
      apt-get install -y nodejs && \
      npm install -g snarkjs && \
      rm -rf /var/lib/apt/lists/*

Rebuild and redeploy.
```

### 4. VAULT999 is a named Docker volume
VAULT999/SEALED_EVENTS.jsonl is NOT in the container filesystem — it's a named volume.
```
Container path: /app/VAULT999/ (empty inside container image)
Host volume: /var/lib/docker/volumes/<vault999-data>/_data/
Verify: docker volume ls | grep vault999
```

### Live snarkjs Groth16 verification test (inside container)
```bash
docker exec <container> python3 -c "
import sys; sys.path.insert(0,'/app')
from arifos.security.zkpc_v2 import _snarkjs_available, _groth16_verify
import json
proof = json.load(open('/app/arifos/security/zkp_artifacts/proof.json'))
public = json.load(open('/app/arifos/security/zkp_artifacts/public.json'))
v, out = _groth16_verify(proof, public)
print('snarkjs available:', _snarkjs_available())
print('groth16 verified:', v)
"
```
Expected: snarkjs available: True, groth16 verified: True (with real proof artifacts)

## Critical: The Running Container Is Never The Image You Just Built

**This is the #1 failure mode.** Every `docker build` + `docker push` creates a NEW image digest, even if the tag is the same. The running container does NOT automatically update.

```
# BAD assumption:
docker build -t ghcr.io/ariffazil/arifos:2026.05.04 .
docker push ghcr.io/ariffazil/arifos:2026.05.04
# → Container still running OLD image. Tag looks right. Content is wrong.

# ALWAYS verify the running container's actual image SHA:
docker ps --filter 'name=arifosmcp' --format '{{.ID}} {{.Image}}'
# → Compare the image SHA (second column) against:
docker images ghcr.io/ariffazil/arifos --format '{{.Tag}}\t{{.ID}}'
# If SHA differs → the running container has an older image
```

**Correct restart sequence:**
```
docker stop <container>
docker rm <container>
docker pull ghcr.io/ariffazil/arifos:<tag>   # pull latest digest
docker run ... --name <container> ghcr.io/ariffazil/arifos:<tag>
```

### The definitive code drift check — `docker diff` + diff against local source

When you suspect the running container has different code than both (a) the latest pushed image and (b) the local source, use this two-step diff:

```bash
# Step 1: docker diff — what has changed inside the container vs image
docker diff <container>

# Step 2: diff running container's file against LOCAL source
diff <(docker exec <container> cat /app/internal/monolith.py) /root/WEALTH/internal/monolith.py
```

**What this reveals:**
- `docker diff` shows files changed inside container (overlayfs) — confirms container has been modified
- `diff <(docker exec cat)` shows exactly what lines differ between running container and local source
- If diff shows local has MORE lines (e.g., `briefing_handler` exists locally but not in container) → container image is OLDER than local
- If diff shows container has MORE lines → container has been patched locally (overlayfs edit) not present in local source

**Example output showing container is stale:**
```
4565a4566,4567
>     BRIEFING_PATH = "/root/arif-sites/..."
>
4568a4571,4581
>     async def briefing_handler(request):
>         ...
>             Route("/briefing", briefing_handler, methods=["GET"]),
```
The `>` lines exist in LOCAL but not in running container → container is running an older image.

**Example output showing container has been hot-patched:**
```
< some_old_function()
---
> some_new_function()
```
The `<` lines exist in container but not in local source → overlayfs patch applied directly to container.

### WEALTH /briefing endpoint failure pattern (May 2026)

**Symptoms:**
- `curl https://mcp.arif-fazil.com/briefing` → HTTP 301 redirect to arifos.arif-fazil.com/briefing
- `curl http://127.0.0.1:8082/briefing` → 404 Not Found
- `docker exec wealth-organ grep briefing_handler /app/internal/monolith.py` → no output
- `docker diff wealth-organ` → `/app/internal/monolith.py` CHANGED

**Three root causes always check in order:**
1. **Container running old image** — `/briefing` handler doesn't exist in running container's code. Fix: rebuild and redeploy WEALTH image.
2. **Data path mount missing** — `BRIEFING_PATH=/root/arif-sites/...` but container has no volume mount to that path. `docker inspect <container> --format '{{json .Mounts}}'` returns `[]`. Fix: add mount to docker-compose:
   ```yaml
   volumes:
     - /root/arif-sites/sites/arif-fazil.com/public/data/wealth:/app/data/wealth:ro
   ```
   And update `BRIEFING_PATH` to `/app/data/wealth/latest.json` (container-internal path).
3. **Caddyfile routing wrong** — `mcp.arif-fazil.com/briefing` falls through to catch-all redirect instead of proxying to `wealth-organ:8082`. Fix: add explicit `handle /briefing` route to Caddyfile under `mcp.arif-fazil.com` block.

**Diagnostic sequence:**
```bash
# 1. Check container has the route
docker exec wealth-organ grep -c "briefing_handler" /app/internal/monolith.py
# 0 = route missing in container

# 2. Check mount exists
docker inspect wealth-organ --format '{{json .Mounts}}'
# [] = no mounts

# 3. Check Caddy routing
curl -sI https://mcp.arif-fazil.com/briefing | grep -E "HTTP|Location"
# 301 to arifos = Caddyfile catch-all redirect

# 4. Check internal route works (bypass Caddy)
curl http://127.0.0.1:8082/briefing
# 404 despite container running = route missing in container code
```

**Verify filesystem content, not image labels:**
```
# Don't trust: docker ps shows the "right" tag
# DO trust: actual filesystem inside running container
docker exec <container> find /app -name 'zkpc_v2.py'       # check code files exist
docker exec <container> node --version                     # check binaries exist
docker exec <container> python3 -c "import sys; print(sys.path[:2])"
```

**The correct restart sequence (always in this order):**
```
docker build -t ghcr.io/ariffazil/arifos:latest .        # build new image
docker push ghcr.io/ariffazil/arifos:latest              # push to registry
docker restart <container>                               # ONLY THEN restart
```
**NOT:** `docker restart` first (pulls nothing new) → then build → then push (container still running old image).

**Verify container is actually running the new image:**
```bash
docker inspect <container> --format '{{.Image}}'
# Compare against:
docker images ghcr.io/ariffazil/arifos:latest --format '{{.ID}}'
# If digests match → container is running the newly pushed image
```

**Volume mounts survive `docker rm` — network connections do NOT:**
```
docker network connect arifos_core_network arifosmcp   # runtime only
# After docker rm + docker run: must re-run network connect
```

## Gotcha: `rest_routes.py` May Be a Package, Not a File

The `rest_routes.py` may have been refactored into a package directory:
```
arifosmcp/runtime/rest_routes/         ← package directory
arifosmcp/runtime/rest_routes/__init__.py
arifosmcp/runtime/rest_routes/rest_routes.py  ← actual file
```
**If editing `rest_routes.py` directly doesn't take effect**, check:
```bash
docker exec <container> find /app -name "rest_routes.py" 2>/dev/null
# If it returns /app/arifosmcp/runtime/rest_routes/rest_routes.py → it's a package
```
The old path `arifosmcp/runtime/rest_routes.py` would be stale.

**`Path(__file__)` parent depth is DIFFERENT inside the package:**
- `/app/arifosmcp/runtime/rest_routes/rest_routes.py` → `parents[0]` = `rest_routes/`, `parents[1]` = `runtime/`, `parents[2]` = `arifosmcp/`
- `/app/arifosmcp/runtime/rest_routes.py` (old monolithic path) → `parents[0]` = `runtime/`, `parents[1]` = `arifosmcp/`, `parents[2]` = `/app`

Always verify depth inside the running container before committing path-construction code.

## Registry Wipe on Container Restart — F11 HOLD Root Cause

`_JUDGE_STATE_REGISTRY` and `_JUDGE_CHAIN_REGISTRY` (used by vault seal / `arif_vault_seal`) are **plain in-memory dicts** (line 987-988 of `runtime/tools.py`). They are NOT persisted to the session store.

**Symptom:** After a container restart, vault seal returns:
```
status: HOLD, verdict: HOLD
reason: "judge contract required — irreversible execution requires a prior judge packet"
failed_floors: ["F11"]
```

**Why:** The pre-restart `_JUDGE_STATE_REGISTRY[judge_state_hash]` and `_JUDGE_CHAIN_REGISTRY[constitutional_chain_id]` are gone. Both lookups return `None` → `_resolve_judge_contract` returns a HOLD.

**Diagnosis:**
```bash
# Check if session store is the only thing surviving restart
docker exec <container> python3 -c "
from arifosmcp.runtime.tools import _JUDGE_STATE_REGISTRY, _JUDGE_CHAIN_REGISTRY
print('JUDGE_STATE size:', len(_JUDGE_STATE_REGISTRY))
print('JUDGE_CHAIN size:', len(_JUDGE_CHAIN_REGISTRY))
"
# Both should be > 0 during normal operation. If 0 after restart → registry wipe.
```

**Fix:** Wire judge registries into the existing `_FileSessionStore` (same pattern already used for sessions). Add `_load_judge_registries()` on startup and `_save_judge_registry()` on write.

## TWO Dockerfiles Exist — Use the Root One

arifOS has **two Dockerfiles** with **different entrypoints**:

```
/root/arifOS/Dockerfile                          ← CORRECT (root-level)
  CMD ["python", "-m", "arifosmcp.runtime.server"]  ✅ serves on :8080

/root/arifOS/arifosmcp/Dockerfile                ← WRONG (sub-directory)
  CMD ["python", "-m", "arifosmcp.runtime.__main__"]  ❌ exits immediately
```

**Symptom when using wrong Dockerfile:** Container starts, runs, then immediately exits with code 0 and **no logs**. The `__main__` module completes instantly without serving anything.

**Diagnosis:**
```bash
# Check what entrypoint the container actually used
docker inspect <container> --format '{{.Config.Cmd}}'
# [python -m arifosmcp.runtime.__main__] = wrong Dockerfile used

# Verify inside running container
docker exec <container> cat /proc/1/cmdline | tr '\0' ' '
# Should say: python -m arifosmcp.runtime.server
```

**Fix:** Always build from the root directory using root-level Dockerfile:
```bash
cd /root/arifOS
docker build --pull -f Dockerfile -t ghcr.io/ariffazil/arifos:<tag> .
#                        ^^^^^^^ NOT arifosmcp/Dockerfile
```

## Container Exits 0 Silently — No Logs

When a container entrypoint process fails immediately, Docker may show exit code 0 with no error output. This is the trickiest "it doesn't work" scenario.

**Debugging technique — background process with watch patterns:**
```bash
# Start container in background with watch
docker run --rm -p 8080:8080 --name arifosmcp_test ghcr.io/ariffazil/arifos:<tag> 2>&1

# OR use Hermes terminal background=true with watch_patterns
docker run --rm -p 8080:8080 --name arifosmcp_test ghcr.io/ariffazil/arifos:<tag> 2>&1 &
sleep 10 && curl -s http://127.0.0.1:8080/health

# OR run foreground and capture exit code
docker run --rm ghcr.io/ariffazil/arifos:<tag> 2>&1; echo "EXIT_CODE=$?"
```

**Other diagnostic commands:**
```bash
# Get the container's actual PID 1 command
docker exec <container> cat /proc/1/cmdline | tr '\0' ' '

# Try running the server manually inside container
docker run --rm ghcr.io/ariffazil/arifos:<tag> python -m arifosmcp.runtime.server
# If this exits immediately → entrypoint mismatch (see TWO Dockerfiles above)

# Verify port is listening
docker exec <container> python3 -c "import socket; s=socket.socket(); s.connect(('127.0.0.1',8080)); print('OPEN')"
```

## kanon-unknown — Git Metadata Missing in Container

`/health` shows `version: kanon-unknown`, `git_commit: unknown`, `build_commit: unknown`.

**Root cause:** `get_build_info()` in `rest_routes.py` reads git commit from environment variable `DEPLOY_GIT_COMMIT`. Inside the Docker container, no `.git` directory is mounted and no env var is set → everything falls back to "unknown".

**Two fixes — use both for complete coverage:**

### Fix 1 — Env var at docker run (immediate, no rebuild)
```bash
docker stop arifosmcp && docker rm arifosmcp
docker run -d \
  --name arifosmcp \
  --restart unless-stopped \
  -p 8080:8080 \
  -e DEPLOY_GIT_COMMIT=de038a0f \
  ghcr.io/ariffazil/arifos:de038a0f
```

### Fix 2 — Bake into Dockerfile (all future deploys)
Add build args to the root `Dockerfile`:
```dockerfile
ARG DEPLOY_GIT_COMMIT=unknown
ARG DEPLOY_GIT_BRANCH=main
ARG DEPLOY_BUILD_TIME=unknown
ENV DEPLOY_GIT_COMMIT=${DEPLOY_GIT_COMMIT}
ENV DEPLOY_GIT_BRANCH=${DEPLOY_GIT_BRANCH}
ENV DEPLOY_BUILD_TIME=${DEPLOY_BUILD_TIME}
```

Then at build time:
```bash
GIT_SHA=$(git log --oneline -1 --format=%H)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
BUILD_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)
docker build \
  --build-arg DEPLOY_GIT_COMMIT=$GIT_SHA \
  --build-arg DEPLOY_GIT_BRANCH=$GIT_BRANCH \
  --build-arg DEPLOY_BUILD_TIME=$BUILD_TIME \
  -f Dockerfile \
  -t ghcr.io/ariffazil/arifos:$GIT_SHA .
```

## Disk Space — Docker Builder Cache

Docker build fails with `no space left on device` when builder cache fills the disk. Signs:
- `df -h /` shows 100%
- `docker system df` shows large build cache

**Fix:**
```bash
docker builder prune -af
df -h /
```
Build cache (27GB+) gets reclaimed. Then rebuild.

## Key Insight
When `docker run` fails but `docker exec` works → the entry point is wrong, not the image.
The image is almost always fine. The CMD/command override is what's broken.

502 from Caddy = network isolation FIRST, then stale image (wrong container), then backend not listening.

## FastMCP Streamable-HTTP 406 — The Real Root Cause (May 2026)

**Symptom:** arifOS MCP returns HTTP 406 on `/mcp` when called without `Accept: application/json` header. WEALTH and GEOX return 200 with the same call.

**Root cause:** FastMCP's `StreamableHTTPServerTransport._check_accept_headers` enforces strict content negotiation. arifOS passes `json_response=True` but has no monkey-patch → rejects `Accept: */*`. GEOX and WELL both have the monkey-patch; arifOS doesn't.

**The monkey-patch (GEOX/WELL pattern):**
```python
from mcp.server.streamable_http import StreamableHTTPServerTransport
_orig_check = StreamableHTTPServerTransport._check_accept_headers
def _patched_check(self, request):
    if getattr(self, "is_json_response_enabled", False):
        return  # accept anything when json_response=True
    return _orig_check(self, request)
StreamableHTTPServerTransport._check_accept_headers = _patched_check
```

**Diagnosis:**
```bash
# arifOS without Accept → 406
curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8080/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{...}}'
# → 406

# arifOS with Accept → 200
curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8080/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{...}}'
# → 200

# GEOX without Accept → 200 (has monkey-patch)
curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8081/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{...}}'
# → 200
```

**Two fixes (use both for defense in depth):**

1. **OpenClaw transport workaround** (no code change needed):
   Add `headers: {"Accept": "application/json"}` to the arifOS MCP server entry in `/root/.openclaw/openclaw.json`. This fixes OpenClaw→arifOS bundle calls without touching arifOS source.

2. **arifOS server.py monkey-patch** (defense in depth):
   Add the monkey-patch above to `arifosmcp/server.py` before `if __name__ == "__main__":`. This makes arifOS fully match WEALTH/GEOX behavior for ALL callers, not just OpenClaw.

**`json_response=True` alone is NOT sufficient.** The parameter is necessary but the monkey-patch is what makes the server tolerant of `Accept: */*`. arifOS has `json_response=True` at line ~266 but lacks the patch → 406 for `*/*` callers.

**Verify GEOX/WELL monkey-patch location:**
```bash
docker exec geox_eic grep -n '_patched_check' /app/server.py
# → lines 3525 (definition), 3529 (application)

docker exec well grep -n '_patched_check' /app/server.py
# → lines 3525 (definition), 3529 (application)
```

## TriWitness Verification (ZKPC live check)

Three independent witnesses must all pass before claiming ZKPC is live:

```
# Witness 1: binary present inside container
docker exec <container> node --version
docker exec <container> npm list -g snarkjs --depth=0 | grep snarkjs

# Witness 2: Groth16 mathematical proof
docker exec <container> python3 -c "
import sys; sys.path.insert(0,'/app')
from arifos.security.zkpc_v2 import _snarkjs_available, _groth16_verify
import json
proof = json.load(open('/app/arifos/security/zkp_artifacts/proof.json'))
public = json.load(open('/app/arifos/security/zkp_artifacts/public.json'))
v, out = _groth16_verify(proof, public)
print('snarkjs:', _snarkjs_available())
print('groth16 verified:', v)
print('output:', out.strip() if out else None)
"

# Witness 3: verification key present
docker exec <container> cat /app/arifos/security/zkp_artifacts/verification_key.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('protocol:', d.get('protocol'))"

# All three must PASS before claiming TriWitness complete
```

## VAULT999 Is A Named Volume

VAULT999 data is NOT in the container filesystem — it's a named Docker volume.
```
Container path:  /app/VAULT999/ (empty at image build time)
Host volume:    /var/lib/docker/volumes/<vault999-data>/_data/
Write to:       /app/VAULT999/SEALED_EVENTS.jsonl (from inside container)
Read from host: /var/lib/docker/volumes/<vault999-data>/_data/SEALED_EVENTS.jsonl
Verify:         docker volume ls | grep vault999
```

VAULT999 is intentionally gitignored (runtime data, not source). Seal events are written from inside the container and persist in the named volume across container restarts.
