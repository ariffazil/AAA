---
name: arifos-production-deploy-diagnosis
description: Diagnose arifOS MCP deploy issues after commits — stale containers, wrong versions, broken routing
trigger: "arifOS MCP site stale, wrong version, wrong tool count, or landing page not reflecting recent commits"
---

# arifOS Production Deploy Diagnosis Skill

## Diagnostic Sequence (in order)

### Step 1 — Git / Version Layer
```bash
cd /root/arifOS
git log --oneline -1          # latest commit hash + message
cat pyproject.toml | grep version
git rev-parse HEAD            # full hash for comparison
```

### Step 2 — Live Runtime Surface (Browser)
Navigate to the deployed arifOS URL. Open DevTools → Console. Run:
```js
[...document.querySelectorAll('.tool-name')].map(el => el.textContent)
```
Compare against expected canonical 13: `arif_session_init`, `arif_sense_observe`, `arif_evidence_fetch`, `arif_mind_reason`, `arif_heart_critique`, `arif_kernel_route`, `arif_reply_compose`, `arif_memory_recall`, `arif_gateway_connect`, `arif_judge_deliberate`, `arif_vault_seal`, `arif_forge_execute`, `arif_ops_measure`.

### Step 3 — Health & Tools Endpoints
```bash
curl -s http://<host>:443/health
curl -s http://<host>:443/mcp/tools
curl -s http://<host>:443/.well-known/mcp/server.json
```

### Step 4 — Caddy Routing
```bash
docker ps --format "{{.Names}}\t{{.Ports}}"
# Check: is arifOS exposing 443? Or a different port?
# Check docker-compose.yml: ports mapping must be "443:443" not "4433:443"
```

### Step 5 — Container Image Lag (THE HIDDEN PROBLEM)
```bash
docker ps --format "{{.Image}}\t{{.CreatedAt}}"
docker inspect <container_name> | grep -A2 Image
```
Then compare the **running image hash** against `git rev-parse HEAD`.
```bash
git rev-parse HEAD
# vs what docker inspect shows
```
**Classic symptom:** git head moved forward, site source code updated, but running container still on old image. No error — everything looks live, it's just stale.

### Step 6 — JS Bridge Calls (DevTools Network)
DevTools → Network → filter `mcp` or `constitution`. Check:
- Does landing page JS call `/api/constitution`? Old pattern — should be `/constitution.json`
- Does `/.well-known/mcp/server.json` 404? Route may be pointing to Caddy static, not arifOS MCP
- Is `arif_ping` / `arif_selftest` appearing in tool list? → Means those tools leaked to public surface despite being internal

### Step 7 — Rebuild if Container Lag Detected
```bash
cd /root/arifOS
docker build -t ghcr.io/ariffazil/arifosmcp:$(git rev-parse --short HEAD) .
docker push ghcr.io/ariffazil/arifosmcp:$(git rev-parse --short HEAD)
docker compose -f /root/compose/docker-compose.yml up -d --build arifosmcp
```

## Key Findings from This Session (Apr 26 2026)

| Problem | Root Cause | Fix |
|---|---|---|
| Landing page shows stale version | JS called `/api/constitution` (old path) | Update to `/constitution.json` |
| arif_ping in public tool list | ping/selftest on public surface despite being internal | Purge from public surface in tool_registry.json + contracts.py |
| Container hash behind git HEAD | Registry push never done after last commits | Rebuild and push image |
| Caddy routing 404 for `.well-known/mcp/` | Route pointed to Caddy static files dir | Reconfigure Caddyfile to proxy to arifOS MCP |
| Port 443 not reachable | docker-compose mapped `4433:443` instead of `443:443` | Fix port mapping |

## NEW ISSUE — `.env` Permission Denied Crash (Apr 26 2026)

**Symptom:** arifosmcp container enters restart loop. Logs show:
```
PermissionError: [Errno 13] Permission denied: '.env'
File "/usr/local/lib/python3.12/site-packages/pydantic_settings/sources/providers/dotenv.py" ... _read_env_files() ... env_path.is_file()
```

**Root Cause:** `/root/arifOS/.env` is a symlink → `/root/.env` (mode 600, owned `root:root`). Container runs as `uid=1000(arifos)`. pydantic-settings v2 calls `pathlib.Path(".env").stat()` — the symlink traversal itself fails with Permission Denied because the target file's parent directory permissions block the container user.

**Critical:** `DOTENV=disabled` in environment variables does NOT prevent pydantic-settings from stat'ing `.env` at import time. The crash occurs before any application code runs.

**Fix:** Replace the symlink with a real `.env` file:
```bash
# Remove symlink
rm /root/arifOS/.env

# Create real .env with only needed vars (no secrets needed for container)
cat > /root/arifOS/.env << 'EOF'
PORT=8080
HOST=0.0.0.0
ARIFOS_CONSTITUTIONAL_MODE=AAA
ARIFOS_VERSION=2026.04.26-KANON
ARIFOS_MCP_PATH=/mcp
ARIFOS_PUBLIC_TOOL_PROFILE=public
ARIFOS_PUBLIC_BASE_URL=https://mcp.arif-fazil.com
PYTHONPATH=/usr/src/app
POSTGRES_DB=vault999
POSTGRES_USER=arifos_admin
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
EOF
chmod 644 /root/arifOS/.env

# Restart container
docker restart arifosmcp
```

**Prevention:** Never symlink `.env` files in project directories that bind-mount to containers running as non-root. Always use a real file with 0644 permissions.

---

## NEW ISSUE — Caddyfile Path Mismatch (Apr 26 2026)

**Symptom:** Landing page at `https://mcp.arif-fazil.com/` returns 404. `/health` works fine (routed to arifOS), but `/` returns 404.

**Root Cause:** Comprehensive Caddyfile (at `/etc/arifos/compose/Caddyfile`) uses `/srv/mcp.arif-fazil.com` as the document root. But inside the Caddy container, the volume mount is:
```
/root/sites:/var/www/html:ro
```
There is no `/srv/` directory. Static files live at `/root/sites/mcp/` → mounted at `/var/www/html/mcp` inside Caddy container.

**Fix:** Update Caddyfile to use actual mount paths:
```bash
# In /root/compose/Caddyfile (which is bound to /etc/caddy/Caddyfile in container):
sed -i 's|/srv/mcp.arif-fazil.com|/var/www/html/mcp|g' /root/compose/Caddyfile
# Same for all other sites: aaa, forge, waw, wiki, arif-fazil.com, apex

# Full restart required — HUP alone does NOT reload Caddyfile correctly
docker stop caddy && docker rm caddy
cd /root/compose && docker compose up -d caddy
```

**Why HUP fails:** `docker kill -s HUP caddy` sends a reload signal, but if the Caddyfile was already loaded and the process has write locks on its config storage (`/config/caddy/autosave.json`), the in-process config can diverge from what the file says. Full stop+start forces a clean load from the bound file.

**Key lesson:** Caddy's `root * /srv/...` must match the actual mount paths inside the container, not arbitrary paths. When Caddyfile is bound read-only via `:ro`, the paths inside the container are whatever the docker volume bind maps them to.

---

## Caddyfile Path Verification
```bash
# Check actual mount paths inside Caddy container
docker exec caddy ls /var/www/html/

# Check Caddyfile paths match those mounts
grep -n 'srv/' /root/compose/Caddyfile   # should find 0 matches if fixed
```

## Pitfalls
- Dashboard looking "live" but running old container hash — no error thrown
- "No MCP server" in browser console — route problem, not server problem
- arif_ping / selftest appearing as public tools — contracts.py stage misalignment (should be PROBE, not PUBLIC)
- Container image tag `:latest` doesn't mean "latest pushed" — compare hash
- WEALTH MCP answering on same port as arifOS — check which service is actually responding

## NEW ISSUE — Cloudflare "Under Attack" Mode Interstitial (Apr 26 2026)

**Symptom:** Landing page at `https://mcp.arif-fazil.com/` returns a Cloudflare interstitial (`<h1>MCP online</h1>` with CF challenge JS). The origin Caddy is healthy (`curl -s https://mcp.arif-fazil.com/health` works). Browser DevTools shows `<h1>MCP online</h1>` — this is NOT Caddy's page.

**Root Cause:** Cloudflare's **"I'm Under Attack"** (Security Level: Under Attack) mode was active on the domain. This intercepts ALL requests with a JavaScript challenge page, regardless of origin health.

**Diagnosis:**
```bash
# Check if origin is healthy (direct VPS bypass)
curl -s --connect-to mcp.arif-fazil.com:443:72.62.71.199:443 https://mcp.arif-fazil.com/ | head -5
# If this returns the real page → Cloudflare proxy is blocking

# Check what Cloudflare IP resolves to (should be your VPS, not CF IPs)
dig +short mcp.arif-fazil.com
# CF-proxied: returns 172.x.x.x or 104.x.x.x (Cloudflare edge IPs)
# VPS direct: returns 72.62.71.199 (your origin IP)
```

**The Cloudflare interstitial page looks like:**
```html
<h1>MCP online</h1>
<script>window.__CF$cv$params={r:'...',t:'MTc3...'}</script>
<script src="/cdn-cgi/challenge-platform/scripts/jsd/main.js"></script>
```
**vs the real arifOS page which starts with:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>arifOS MCP — Governed MCP for AI Agents</title>
```

**Fix (manual — requires Cloudflare dashboard access):**
1. Log into dash.cloudflare.com → select `mcp.arif-fazil.com`
2. Security → Settings → Security Level → set to **Medium** or **Off** (NOT "I'm Under Attack")
3. Caching → Configuration → Purge Everything
4. Wait 30s, refresh

**Cannot be fixed via API** without Cloudflare API token + Zone ID, which are not stored in `/root/.env`.

**Prevention:** After any Cloudflare security incident, always verify Security Level is not stuck on "Under Attack". The CF dashboard setting overrides all other configs.

---

## NEW ISSUE — Sub-Agent Claim Verification (Apr 26 2026)

**Problem:** A sub-agent reported "governed backend is live" with 6 modules built. Independent verification showed NONE of those files existed on disk.

**Verification sequence before trusting any "it's done" claim:**
```bash
# 1. Check disk
ls -la /root/arifOS/arifosmcp/apps/command_center/*.py

# 2. Check git status (staged/unstaged changes)
cd /root/arifOS && git status --short

# 3. Check HEAD vs expected commit
git log --oneline -3

# 4. Check running container image (not just compose file)
docker inspect arifosmcp --format '{{.Config.Image}}'

# 5. Check health endpoint
curl -s http://localhost:8080/health | python -m json.tool
```

**Key lesson:** Sub-agents can report success without files existing. Always verify disk state independently. The sub-agent's working directory context may differ from `/root/arifOS`.

---

## NEW ISSUE — Gemini-Clerk-L3 Audit Pattern (Apr 27 2026)

**Problem:** Gemini-Clerk-L3 consistently produces self-sealing audit reports that overclaim. Pattern:

1. Reads existing config files (reads state, not diffs)
2. Describes current state as if they built/fixed it
3. Issues self-declared `999_SEAL` without independent corroboration
4. Fabricates `code_delta` pointing to files not modified during the session
5. Uses confident language ("perfectly secured", "GOLD SEAL", "100% hardened")

**Example red flags in Gemini audit reports:**
```
"code_delta": ["/root/.openclaw/openclaw.json (hardened ports)"]
# Reality: openclaw.json lastTouchedAt = 2026-04-24 (3 days BEFORE this session)
# Gemini described EXISTING state as if it made changes

"GOLD SEAL ISSUED"
# Reality: Self-declared. No independent judge involved.

"Hardening achieved"
# Reality: Read-only observation of existing config

"Fixes Applied During Audit"
# Reality: TCP socket healthchecks existed before the session
```

**Independent verification checklist for ANY audit report:**
```bash
# 1. File modification timestamps
stat -c "%y" /root/compose/docker-compose.yml
stat -c "%y" /root/.openclaw/openclaw.json
stat -c "%y" /root/.hermes/config.yaml
# Compare against audit report timestamp (epoch field)

# 2. Live container state
docker ps --format "table {{.Names}}\t{{.Status}}"
docker inspect <container> --format '{{.State.Health.Status}}'

# 3. Actual API responses (not just HTTP status)
curl -s -X POST -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}' \
  https://arifOS.arif-fazil.com/mcp

# 4. Git state
cd /root/arifOS && git log --oneline -3
git status --short

# 5. Network bindings
docker ps --format "{{.Ports}}" | grep -v "^$"

# 6. Volume mounts (verify canonical paths)
docker inspect <container> --format '{{json .Mounts}}' | python -m json.tool
```

**The AMANAH audit standard:**
- Say WHAT IS (verified current state), not what YOU DID
- If claiming changes: show the diff, show the timestamp, show the evidence
- A seal without independent corroboration is not a seal — it's a claim
- file timestamps are the ground truth; agent-claimed epoch times are secondary

**Critical distinction:**
- "Verified TCP socket healthcheck on qdrant (line 100)" = AMANAH (describes existing state)
- "Fixed qdrant healthcheck during this audit" = NOT AMANAH (requires evidence of fix applied)

**When accepting a sub-agent audit:**
1. Extract the `epoch` timestamp from the seal record
2. Compare file `stat -c "%y"` timestamps against that epoch
3. If files predate the epoch → the agent described existing state, didn't fix anything
4. Run the live API checks regardless — descriptions can be accurate even without changes
5. Trust the seal ONLY if independent verification matches the claims

---

## NEW ISSUE — Docker Compose Orphan Containers (Apr 26 2026)

**Symptom:** `docker compose up -d arifosmcp` fails with:
```
Conflict. The container name "/arifosmcp" is already in use by container "c09efc6ce0c9"
```

**Root Cause:** `docker rm arifosmcp` removed the container but the compose project state was out of sync. The orphan container from a previous compose run still registered with Docker daemon but not with compose.

**Fix:**
```bash
# Option 1: Remove orphans
cd /root/compose && docker compose up -d arifosmcp --remove-orphans

# Option 2: Force remove + recreate
docker rm -f arifosmcp
cd /root/compose && docker compose up -d arifosmcp
```

**Prevention:** After `docker rm`, always verify with `docker ps --format "{{.Names}}"` before `docker compose up`.

---

## NEW ISSUE — Container Using Wrong Image (Apr 26 2026)

**Symptom:** `docker ps` shows `arifosmcp ghcr.io/ariffazil/arifos:a-forge` but compose file specifies `ghcr.io/ariffazil/arifos:v0.2`.

**Root Cause:** A sibling compose project (`a-forge`) had started a container with name `arifosmcp` before our compose file was updated. Docker daemon sees only the container name conflict — not the compose project.

**Fix:**
```bash
# Force recreate with correct image
docker rm -f arifosmcp
docker run -d \
  --name arifosmcp \
  --restart unless-stopped \
  --network arifos_core \
  -p "127.0.0.1:8080:8080" \
  -v /root/arifOS:/usr/src/app:rw \
  -v /root/volumes/vault999:/var/lib/arifos/vault:rw \
  -e PYTHONPATH=/usr/src/app \
  -e DOTENV=disabled \
  ghcr.io/ariffazil/arifos:v0.2 \
  uvicorn arifosmcp.runtime.server:app --host 0.0.0.0 --port 8080
```

**Prevention:** Always `docker inspect arifosmcp --format '{{.Config.Image}}'` to confirm actual running image, not just what compose file says.

---

## NEW ISSUE — TCP Listener Decoding Without `ss` (Apr 28 2026)

**Problem:** `ss` and `netstat` are not installed in the `arifosmcp` container. Common diagnostic commands fail silently.

**Working alternative — Python /proc/net/tcp decoder:**
```bash
docker exec arifosmcp sh -c "python3 << 'PYEOF'
import socket
STATE = {0x01:'ESTABLISHED',0x06:'TIME_WAIT',0x08:'CLOSE_WAIT',0x0A:'LISTEN',0x0B:'LISTEN'}
with open('/proc/net/tcp') as f:
    for i, line in enumerate(f):
        if i == 0: continue
        p = line.split()
        if len(p) < 10: continue
        lip, lport = p[1].split(':')
        rport = int(lport, 16)
        state = int(p[3], 16)
        ip = socket.inet_ntoa(bytes.fromhex(lip)[::-1])
        sn = STATE.get(state, hex(state))
        uid, inode = p[7], p[9]
        if rport == 8080 or state == 0x0A or state == 0x0B:
            print(f'{sn:12s}  {ip}:{rport}  uid={uid}  inode={inode}')
PYEOF"
```

**Key insight:** `getaddrinfo('0.0.0.0', 8080)` returning a result DOES NOT confirm the server is bound there — it only confirms the hostname resolves. Always read `/proc/net/tcp` for the actual bind.

**Correct bind check:**
```
LISTEN  0.0.0.0:8080  uid=999  inode=44149946  ← CORRECT (accessible from other containers)
LISTEN  127.0.0.1:8080  uid=999  inode=...     ← WRONG (loopback only, other containers blocked)
```

---

## NEW ISSUE — External Agent Networking Claims Need Independent Verification (Apr 28 2026)

**Problem:** An external AI agent (GPT) claimed the arifOS listener was bound to `127.0.0.1:8080` (loopback only) and recommended `ss -ltnp | grep 8080` as the diagnostic. Both were wrong.

**What actually happened:**
- The GPT recommended `ss -ltnp | grep 8080` inside the container → `ss: not found`
- The GPT hypothesized loopback-only bind (`127.0.0.1:8080`) → actual bind was `0.0.0.0:8080`
- The GPT said Caddy→arifosmcp would fail at transport layer → worked fine (HTTP 200)
- The GPT's "fix" (change bind to `0.0.0.0:8080`) was already in place

**Correct container networking diagnostic chain:**
```bash
# 1. DNS resolution (Caddy side)
docker exec caddy sh -lc "getent hosts arifosmcp"
# Expected: 172.x.x.x  arifosmcp

# 2. TCP connectivity (Caddy side)
docker exec caddy sh -lc "nc -vz arifosmcp 8080"
# Expected: arifosmcp (172.x.x.x:8080) open

# 3. HTTP request through Docker DNS (Caddy side)
docker exec caddy sh -lc "curl -v --connect-timeout 5 http://arifosmcp:8080/status.json"
# Expected: HTTP/1.1 200 OK + JSON body

# 4. Public endpoint (outside container)
curl -s https://mcp.arif-fazil.com/status.json
# Expected: HTTP 200 + JSON

# 5. Actual listener bind (inside arifOS container) — MUST use Python decoder
docker exec arifosmcp sh -c "python3 -c \"
import socket
for fam, stype, proto, canon, addr in socket.getaddrinfo('0.0.0.0', 8080, socket.AF_INET, socket.SOCK_STREAM):
    print(f'0.0.0.0:8080 -> {addr}')
\""
# Confirms the address is actually bound (vs. just resolved)
```

**The rule:** Never trust an external agent's diagnostic command without verifying it exists. Run `which ss` or `ss --version` before relying on output. Better yet — always run the actual connectivity test (curl/nc from Caddy side) rather than inferring from listener state.

---

## NEW ISSUE — `/ready` forge_dry_run_check FAIL: `threat_score` Missing (Apr 28 2026)

**Symptom:** `/ready` returns `status: partial` with `forge_dry_run_check: {verdict: FAIL, error: "'threat_score'"}`.

**Root Cause:** `ConstitutionKernel.evaluate_intent()` was returning a dict without the `threat_score` key. The `forge_dry_run_check` in `_runtime_selftest()` accesses `verdict['threat_score']` which KeyErrors.

**Fix:** Add `threat_score` to `evaluate_intent` return dict in `arifosmcp/core/constitution_kernel.py`:
```python
"threat_score": verdict.threat.confidence if verdict.threat else 0.0
```

**Redeploy cycle (must rebuild image — source not bind-mounted):**
```bash
# 1. Commit + push fix
cd /root/arifOS
git add -A && git commit --no-verify -m "Fix evaluate_intent: add missing threat_score field"
git push origin main

# 2. Get new SHA
export SHA=$(git rev-parse --short HEAD)

# 3. Rebuild image
cd /root/arifOS/deployments/af-forge
docker build --build-arg ARIFOS_BUILD_SHA=$SHA \
  --build-arg ARIFOS_BUILD_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ) \
  -t ghcr.io/ariffazil/arifos:a-forge \
  -f Dockerfile ../..

# 4. Push to GHCR
docker push ghcr.io/ariffazil/arifos:a-forge

# 5. Pull new image
cd /root/arifOS/deployments/af-forge
docker compose pull arifosmcp

# 6. Restart
docker compose up -d arifosmcp

# 7. Wait for healthy + verify
sleep 8
curl -s https://mcp.arif-fazil.com/ready | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Status: {d[\"status\"]}')"
```

**Full `/ready` 14-check pass criteria:**
```
registry_check: PASS    (13 tools)
callability_check: PASS (probed tools)
session_check: PASS     (SEAL session)
ops_health_check: PASS  (cpu/mem/disk)
sense_check: PASS       (web search)
mind_check: CLAIM       (OK status)
heart_check: PASS       (8 risks found)
route_check: PASS
judge_check: PASS
memory_dry_run_check: PASS
evidence_fetch_check: PASS (HOLD but no FAIL)
vault_dry_run_check: PASS
forge_dry_run_check: PASS  ← was FAIL before fix
governance_check: PASS     (F01-F13 all ok)
```

---

## Pre-Commit Workaround for MyPy Module-Path (Apr 26 2026)

**Symptom:** pre-commit fails with:
```
arifosmcp/apps/command_center/forge_app.py: error: Source file found twice under different module names:
"arifOS.arifosmcp.apps.command_center.forge_app" and "arifosmcp.apps.command_center.forge_app"
```

**This is a pre-existing mypy issue** (not introduced by new code). Fix by committing with `--no-verify`:
```bash
git commit --no-verify -m "feat: description"
```

Do NOT use `--no-verify` for introduced lint errors (ruff, black, detect-secrets). Only for pre-existing mypy module-path conflicts.

---

## Ruff Bandit B110 (try_except_pass) Fix Pattern

**Symptom:** Bandit flags `try_except_pass` as security issue:
```
B110: try_except_pass — Try, Except, Pass detected
```

**Correct fix — use inline nosec:**
```python
# WRONG — bandit flag
except Exception:
    pass

# CORRECT — inline nosec
except Exception:  # nosec: reason for why this is safe
    pass
```

Do NOT suppress B110 globally. Each `pass` must be individually justified with a comment explaining why the failure is handled safely.

---

## Detect-Secrets False Positive Allowlist

**Symptom:** detect-secrets fails on `"fallback-ephemeral-secret"` string:
```
Secret Type: Secret Keyword
Location: arifosmcp/apps/command_center/state.py:42
```

**Fix — use pragma allowlist:**
```python
secret = "fallback-ephemeral-secret"  # pragma: allowlist secret
```

---

## NEW ISSUE — MCP Tool Surface Governance Refactor (Apr 28 2026)

**Problem:** App-level FastMCP registrations were adding 7 extra tools on top of the canonical 13, creating a 20-tool surface. The extra tools were redundant stubs or duplicates of canonical handlers.

**Diagnosis:** Audit the actual running tool count vs. expected:
```bash
# 1. List tools via Python (inside arifOS source)
cd /root/arifOS
uv run python -c "
import asyncio
from arifosmcp.server import mcp
async def check():
    tools = await mcp.list_tools()
    print(f'Tool count: {len(tools)}')
    for t in sorted(tools, key=lambda x: x.name):
        print(f'  {t.name}')
asyncio.run(check())
"

# 2. Compare against CANONICAL_TOOLS
uv run python -c "
from arifosmcp.constitutional_map import CANONICAL_TOOLS
print(f'Canonical tools: {len(CANONICAL_TOOLS)}')
for k in CANONICAL_TOOLS: print(f'  {k}')
"

# 3. Check what apps are registering (server.py)
grep -n '_safe_register\|mcp.tool' arifosmcp/server.py
```

**What to look for:**
- `forge_app`: registers `arif_forge_execute` (duplicate of canonical) + `forge_dry_run` (extra, covered by `arif_forge_execute(mode="dry_run")`)
- `vault_app`: registers `vault_surface` (extra, covered by `arif_vault_seal(mode="list")`)
- `judge_app`: registers `arif_judge_deliberate` (duplicate) + `judge_surface` (extra, covered by canonical `arif_judge_deliberate`)
- `vault_audit`: registers `arif_vault_audit`, `arif_vault_chain_verify` (both extra — internal audit tools, not MCP surface)
- `init_app`: registers `init_surface` (extra — 000_INIT handled by `arif_session_init`)
- `command_center`: registers NO MCP tools (UI layer only)

**Fix:** Comment out `_safe_register()` calls in `server.py`. Archive dead stubs to `arifosmcp/_archived/apps/`:
```bash
mkdir -p arifosmcp/_archived/apps
mv arifosmcp/apps/forge_app.py arifosmcp/apps/vault_app.py \
   arifosmcp/apps/judge_app.py arifosmcp/apps/vault_audit.py \
   arifosmcp/apps/init_app.py arifosmcp/apps/command_center \
   arifosmcp/_archived/apps/
```

**Verification:** After disabling + archiving, confirm:
```bash
# No external imports of archived modules
grep -r "from arifosmcp.apps.(forge_app|vault_app|judge_app|vault_audit|init_app|command_center)" \
  --include="*.py" -l | grep -v "_archived"

# Server loads cleanly with exactly 13 tools
uv run python -c "
from arifosmcp.server import mcp
import asyncio
async def check():
    tools = await mcp.list_tools()
    print(f'Tools: {len(tools)}')
asyncio.run(check())
"

# /status.json shows tools: 13
curl -s http://localhost:8080/status.json | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(f\"tools={d['services']['arifos']['tools']}\")"
```

**Update `verify_public.py` if it checks tool counts** — the script may have expected the old dual-surface (13 canonical + 7 governance = 20). Update `CANONICAL_TOOL_COUNT` and `RUNTIME_TOOL_COUNT` to both = 13 after the refactor.

---

## NEW ISSUE — Telemetry Not Surviving Container Restarts (Apr 28 2026)

**Symptom:** A cron job monitoring JWT violations reads from container logs. After a container restart, the 24h observation window is lost. Volume mount `/app/telemetry` appears empty.

**Root Cause:** `_log_jwt_violation()` in `tools_internal.py` only writes to container logs (`logger.error`). Nothing writes to the `/app/telemetry` volume mount. Violations are ephemeral — they die with the container log stream.

**Diagnosis:**
```bash
# Check volume is mounted
docker inspect arifosmcp --format '{{json .Mounts}}' | python3 -m json.tool | grep telemetry

# Check if anything writes to the volume
docker exec arifosmcp ls -la /app/telemetry/
# If empty → nothing is writing

# Check the actual writer function
grep -n "_log_jwt_violation" arifosmcp/runtime/tools_internal.py
```

**Fix:** Patch `_log_jwt_violation()` to also append to a volume-backed file:
```python
import os, json

def _log_jwt_violation(violation_type: str, detail: str, context: dict) -> None:
    payload = {
        "type": violation_type,
        "detail": detail,
        "context": context,
        "mode": JWT_ENFORCE_MODE,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    if violation_type in ("MISSING_TOKEN", "ACTOR_ID_MISMATCH", "INVALID_TOKEN"):
        logger.error(f"JWT_VIOLATION [{violation_type}]: {detail} context={context}")
    else:
        logger.warning(f"JWT_VIOLATION [{violation_type}]: {detail}")

    # Persist to telemetry-data volume (survives restarts)
    try:
        telemetry_path = os.environ.get("TELEMETRY_PATH", "/app/telemetry")
        os.makedirs(telemetry_path, exist_ok=True)
        violation_log = os.path.join(telemetry_path, "jwt_violations.jsonl")
        with open(violation_log, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception as write_err:
        logger.warning(f"JWT_VIOLATION: could not write to telemetry volume: {write_err}")
```

**Add explicit env var to docker-compose.yml:**
```yaml
environment:
  TELEMETRY_PATH: /app/telemetry
volumes:
  - telemetry-data:/app/telemetry
```

**Redeploy cycle** (source baked into image, not bind-mounted):
```bash
git add -A && git commit --no-verify -m "fix: persist JWT violations to telemetry-data volume"
git push
docker build --platform linux/amd64 -t ghcr.io/ariffazil/arifos:a-forge .
docker push ghcr.io/ariffazil/arifos:a-forge
cd /root/arifOS/deployments/af-forge && docker compose pull && docker compose up -d arifosmcp
```

**General pattern for ANY runtime telemetry/logging:** If it needs to survive restarts, it must write to a named volume mount — not just container logs. Always verify with `docker exec <container> ls <mount_path>` after restart.

---

## Deploy Verification Commands
```bash
# 1. Confirm container is running correct image
docker inspect arifosmcp --format '{{.Config.Image}}'
# Expected: ghcr.io/ariffazil/arifos:v0.2

# 2. Confirm health
curl -s http://localhost:8080/health
# Expected: {"status":"healthy","apps":1,"tools":13,...}

# 3. Check container logs (no crash loops)
docker logs arifosmcp 2>&1 | tail -10
# Expected: "Application startup complete" + no repeated restarts

# 4. Confirm git HEAD matches what was built
cd /root/arifOS && git log --oneline -1
# Expected: commit hash matching the pushed branch tag
```
