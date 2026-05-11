---
name: vps-architecture-audit
description: Systematically map all running containers, MCP servers, tools, routing, and integration status on the arifOS VPS. Trigger when Arif wants a full system picture.
triggers:
  - "map the VPS"
  - "what's running"
  - "full architecture"
  - "audit VPS"
  - "architecture map"
  - "map all components"
  - "what components are connected"
  - "SEA-LION"
  - "component map"
---

# VPS Architecture Audit — Live System Mapping

## Trigger
When: Arif wants a full picture of what's running on the VPS — containers, MCP servers, tools, routing, integration status, disk usage.

## Why save this
This is a recurring need. The approach used systematic multi-step probing that worked well:
1. Docker inventory first (`docker ps -a` + format)
2. Port probing for all known ports (curl health endpoints)
3. Container introspection (fastmcp.json, package.json, source files)
4. Tool counting via grep on source files
5. Caddy routing check
6. Integration status determination by reading actual bridge code

## Commands (in order)

### Step 1: Docker inventory
```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"
docker ps -a --format "{{.Names}}" | sort
```

### Step 2: Port health probes
```bash
for port in 7071 8000 8080 8081 8082 8083 11434 5432 6379 6333; do
  curl -s "http://localhost:$port/health" 2>/dev/null | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(f'port $port: {d.get(\"service\", d.get(\"status\", \"?\"))}')" \
    2>/dev/null || echo "port $port: no health"
done
```

### Step 3: MCP tool counts (per container)
```bash
docker exec <container> grep -c "@mcp.tool\|@mcp.resource" <entrypoint.py>
docker exec <container> cat /app/fastmcp.json  # shows entrypoint, transport, port
```

### Step 4: Container file system peek
```bash
docker exec <container> ls /app/
docker exec <container> cat /app/fastmcp.json
```

### Step 5: A-FORGE package.json (TypeScript deps)
```bash
docker exec af-bridge-prod cat /app/package.json | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print('name:', d.get('name')); print('deps:', list(d.get('dependencies',{}).keys()))"
```

### Step 6: GitHub repos
```bash
curl -s "https://api.github.com/users/ariffazil/repos?per_page=100" | \
  python3 -c "import sys,json; [print(r['name'], '|', r['language'], '|', r['default_branch']) for r in json.load(sys.stdin)]" | sort
```

### Step 7: Caddy routing
```bash
cat /root/compose/Caddyfile
# or
docker exec caddy cat /etc/caddy/Caddyfile
```

### Step 8: Integration wiring check (SIMULATED vs LIVE — CRITICAL)
```bash
# Check geox_bridge.py — CRITICAL: this returns SIMULATED, not live data
grep -n "SIMULATED\|TODO\|pending" /root/arifOS/arifosmcp/apps/geox_bridge.py

# Check if arifOS can actually reach postgres from inside the container
docker exec arifosmcp python3 -c "import psycopg2; print('postgres accessible')" 2>/dev/null \
  || echo "postgres NOT accessible from arifosmcp container"

# Check if arifOS can reach redis from inside the container
docker exec arifosmcp python3 -c "import redis; r=redis.Redis.from_url('redis://:@localhost:6379/'); print('redis:', r.ping())" 2>/dev/null \
  || echo "redis NOT accessible from arifosmcp container"

# Verify WEALTH/GEOX/WELL are SSE-only (POST will return 405/406)
curl -s -X POST http://localhost:8082/tools -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' 2>/dev/null \
  | python3 -c "import sys,json; print('WEALTH POST:', json.load(sys.stdin).get('error',{}).get('code','?'))" 2>/dev/null \
  || echo "WEALTH POST blocked (SSE-only transport)"

# Check rest_routes.py for live vs simulated federation calls
grep -n "SIMULATED\|geox\|wealth\|well\|8081\|8082\|8083" \
  /root/arifOS/arifosmcp/runtime/rest_routes.py \
  /root/arifOS/arifosmcp/apps/geox_bridge.py 2>/dev/null \
  | grep -v "^Binary" | head -20
```

**Known SIMULATED bridges (as of 2026-05-05):**
- `geox_bridge.py` lines 73, 77, 98 — returns "GEOX integration pending full MCP client wiring"
- arifOS has NO SSE client — cannot call WEALTH/WELL/GEOX via MCP JSON-RPC POST
- postgres/redis not accessible from inside arifOS container — DB ops must go through vault999 writer

### Step 8b: Active holds tracking
```bash
# Track all known ARCH-*, WEALTH-*, GEOX-*, FED-* holds
grep -rn "ARCH-\|WEALTH-\|GEOX-\|FED-\|HOLD" /root/.hermes/MEMORY.md 2>/dev/null | head -20
```

### Step 9: OpenClaw event loop P99 (CRITICAL check)
```bash
# Check latest openclaw log for liveness/event loop warnings
tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | \
  python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line)
        msg = d.get('1', d.get('message', ''))
        if 'liveness' in msg or 'eventLoop' in msg or 'P99' in msg:
            print(d['_meta']['date'], '|', msg[:200])
    except: pass
" 2>/dev/null | tail -10

# Also check for model fallback errors (wrong model IDs)
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | \
  grep -i "model_not_found\|fallback.*model\|kimi\|unknown model" | tail -5
```

**P99 Thresholds:**
| P99 | Status | Action |
|-----|--------|--------|
| < 100ms | ✅ Healthy | None |
| 100–500ms | ⚠️ Elevated | Monitor |
| 500–2000ms | 🔴 Warning | Investigate within 1 hour |
| 2000–10000ms | 🔴🔴 CRITICAL | Restart gateway immediately |
| > 10000ms | 💀 Choking | kill + restart immediately |

**To restart OpenClaw (when P99 > 2000ms):**
```bash
# 1. Kill existing gateway process
pkill -f "openclaw.*gateway" 2>/dev/null; sleep 3

# 2. Start fresh in background (use background=true, NOT shell &)
# Run as separate terminal() call with background=true

# 3. Verify health (wait 8s for full startup)
sleep 8 && curl -s --max-time 5 http://localhost:18789/health
```

### Step 10: Disk + RAM
```bash
df -h /
free -h
docker system df
docker volume ls
```

**Docker builder prune** (free build cache, drop disk from >85% to ~75%):
```bash
docker builder prune -af 2>&1 | tail -3
```

### Step 11: Missing substrates audit
Check what infrastructure is absent for the proactive mesh:
```bash
# Missing substrates (non-zero = installed, zero/empty = missing)
for tool in firejail nats-server loki promtail podman; do
  which $tool 2>/dev/null && echo "$tool: EXISTS" || echo "$tool: MISSING"
done

# Existing substrates (should all return EXISTS)
for tool in docker python3 node chromium-browser playwright cron; do
  which $tool 2>/dev/null && echo "$tool: EXISTS" || echo "$tool: MISSING"
done
```

### Step 12: A2A bridge health
```bash
curl -s --max-time 3 http://localhost:18000/ 2>/dev/null | head -3 || echo "openclaw-a2a 18000: no route"
curl -s --max-time 3 http://localhost:18001/health 2>/dev/null || echo "hermes-a2a 18001: no health route"
```

### Step 13: Ollama actual status
Port 11434 returns 404 on `/` but works on `/api/tags`:
```bash
curl -s --max-time 3 http://localhost:11434/api/tags 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); [print(m.get('name','?')) for m in d.get('models',[])]"
```

### Step 14: Duplicate/unhealthy containers
```bash
# Find containers with unhealthy status
docker ps -a --format "{{.Names}}|{{.Status}}" | grep -v "Up " | grep -v "healthy"

# Orphaned stack containers (same image/name pattern as main but on different network)
docker ps -a --format "{{.Names}}|{{.Image}}" | sort
```

## Key lessons learned (updated 2026-05-07)

### CRITICAL: "You're already in root" = local terminal IS the VPS
When Arif says "you're already in root la" about a VPS, he means this terminal session IS running ON the VPS itself. Do NOT attempt SSH to reach it.

**Wrong approach (wasted 4 attempts):**
```bash
ssh root@167.99.223.29          # Permission denied
ssh -i ~/.ssh/id_rsa ...       # Permission denied
ssh -i ~/.ssh/id_ed25519 ...   # Permission denied
ssh -i ~/.ssh/arif-forge-push  # Permission denied
```

**Right approach:**
```bash
docker ps              # Running directly on VPS host — containers visible immediately
docker exec <container> # Inspect internals
curl localhost:<port>  # Test services directly
```

**How to confirm you're on the VPS:**
- `uname -a` shows VPS kernel
- `docker ps` shows arifOS container stack
- `hostname` may show srv1325122.hstgr.cloud or similar
- Arif's VPS is `srv1325122.hstgr.cloud` (72.62.71.199) — this IS the host

### Container debugging without curl
Many containers (e.g., vault999-writer) don't have `curl` installed. Use Python or wget:
```bash
# Python (most common — Alpine and distrol-based images):
docker exec <container> python3 -c "
import urllib.request
print(urllib.request.urlopen('http://localhost:5001/health').read().decode())
"

# wget as fallback:
docker exec <container> wget -q -O - http://localhost:5001/health

# Check what tools exist first:
docker exec <container> which python3 wget curl curl 2>/dev/null
```

### Finding credentials in container env
```bash
docker exec <container> env | grep -i "token\|auth\|secret\|vault"
```
The actual writer token for vault999-writer lives in `VAULT_WRITER_TOKEN` env var, not in prompts or chat. Tokens provided by agents may be truncated or wrong — always verify against `docker exec env`.

### SSE-only transport servers (WEALTH, GEOX, WELL)
WEALTH, GEOX, WELL use SSE-only transport — POST returns 405/406. You cannot JSON-RPC POST to them:
```bash
# These return error:
curl -X POST http://localhost:8082/mcp -d '{"jsonrpc":"2.0","method":"tools/list"}'

# These work (SSE GET):
curl -H "Accept: text/event-stream" http://localhost:8082/mcp?session_id=test
```
arifOS needs an SSE client to call them — it currently doesn't. Federation calls to WEALTH/GEOX/WELL from arifOS FAIL SILENTLY (returns simulated data from geox_bridge.py).

### arifOS container isolation — postgres and redis NOT accessible from inside
Despite postgres and redis containers running on the same Docker network, arifOS cannot import psycopg2 or redis from inside its container. Use vault999 container as proxy for DB ops, or exec into postgres/redis containers directly.

### Finding SIMULATED bridges is CRITICAL
geox_bridge.py returns "pending full MCP client wiring" — it does NOT call live GEOX. Always grep for SIMULATED before trusting federation call outputs.

### Caddyfile SSE proxy requirements
SSE transports (streamable-http) require two route blocks, not just one:
```
handle /mcp {
    reverse_proxy <container>:<port> {
        flush_interval -1
    }
}
handle /mcp/* {
    reverse_proxy <container>:<port> {
        flush_interval -1
    }
}
handle /messages/* {
    reverse_proxy <container>:<port> {
        flush_interval -1
    }
}
```
Without `/messages/` block, SSE session endpoints return 404 through Caddy even if the server is healthy.
**Do not add WebSocket support unless the MCP server explicitly requires it** — adding it to SSE-only servers breaks routing.

### Docker image rebuild traps
When rebuilding a container from source (e.g., `docker build -t image:tag .`):
1. Old container may have had dev fallbacks for env vars that the new image removes
2. Always check: `docker inspect <container> --format='{{json .Config.Env}}'`
3. If container won't start after rebuild, check for missing env vars vs old container's env
4. Add dev fallbacks in source code (e.g., `process.env.TOKEN || 'default-dev-value'`) before rebuilding
5. Verify package.json version vs hardcoded version in server code — both must match

### MCP endpoint verification sequence
```bash
# 1. Check internal port directly (bypass Caddy):
curl http://localhost:<port>/health

# 2. Check streamable-http GET (SSE transport):
curl -H "Accept: text/event-stream" http://localhost:<port>/mcp

# 3. Check POST if applicable:
curl -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  http://localhost:<port>/mcp

# 4. Check Caddy routing:
docker exec caddy caddy validate --config /etc/caddy/Caddyfile
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```

### Network isolation matters
Containers can be on different Docker networks and unable to reach each other:
```bash
for container in $(docker ps --format "{{.Names}}"); do
  nets=$(docker inspect "$container" --format '{{range .NetworkSettings.Networks}}{{.NetworkID}} {{end}}')
  echo "$container: $nets"
done
```
`funny_nash` is on `bridge` network only — cannot reach `arifos_core_network`.

### Tool counting — grep on source files
```bash
# For Python FastMCP:
docker exec <container> grep -c "@mcp.tool\|@mcp.resource" /app/server.py

# For Python where tools are plain functions:
docker exec <container> grep -c "def <prefix>_\|tool(" /app/monolith.py

# For TypeScript:
docker exec <container> cat /app/package.json | python3 -c "..." # check deps

# Direct inspection:
docker exec <container> ls /app/arifosmcp/runtime/
```

### Integration status — check the source code
```bash
# geox_bridge.py returns simulated:
grep -n "SIMULATED\|TODO\|pending" /root/arifOS/arifosmcp/apps/geox_bridge.py

# Check what rest_routes.py actually calls:
grep -n "wealth\|geox\|8081\|8082" /root/arifOS/arifosmcp/runtime/rest_routes.py
```

### "Supabase" = Postgres backend
VAULT999 uses Postgres. "Supabase alignment" in seals = shared Postgres tech, not a separate Supabase cloud instance.

### Contaminated git working directory rescue
When the local `/root/arifOS` git working directory has hundreds of uncommitted changes (from prior sessions) that block `push --force` or normal commits:

**Problem:** `git reset --hard` fails with `"error: unable to unlink old 'Caddyfile': Device or resource busy"` — Caddyfile is bind-mounted and locked by the Caddy container.

**Solution (in order):**
1. `git reset --soft origin/main` — moves HEAD but PRESERVES the working tree. The locked file doesn't matter because nothing touches the filesystem. Staged files = only what you `git add` after.
2. Then `git add <only-the-file-you-changed>` and `git commit` — only your intended change commits.
3. If `git reset --soft` fails too (too many conflicting files), clone fresh: `git clone --depth=1 https://github.com/ariffazil/arifos.git /tmp/arifos-fresh`, apply your patch there, commit and push from the clean clone.

**Never do:**
- `git reset --hard` — requires unlinking every file, fails on bind-mounted files
- `git pull --no-rebase` — picks up all contaminated changes
- `git push --force` alone — doesn't fix the local contaminated state

### The `/components` endpoint pattern
For dynamic live topology visible at `arifos.arif-fazil.com/components`:

Add a new `@route("/components", methods=["GET"])` to `rest_routes.py` that:
- Uses `asyncio.wait_for(asyncio.open_connection(host, port))` for TCP probes
- Uses `httpx.AsyncClient` for HTTP probes
- Returns `JSONResponse` with `Access-Control-Allow-Origin: *`
- Groups results by layer (mcp_servers, ai_external, infrastructure)
- Include `latency_ms`, `status` (ON/OFF/DEGRADED), and `error` for each
- Version-stamp with current release (e.g., `2026.05.01`)

This replaces static "Providers" configuration with live probing.

### For VAULT999 probing specifically — see audit-verification-protocol skill

### Step 15: SSH access setup (CRITICAL — not always root, not always port 22!)

**15a. Discover SSH config and user accounts FIRST:**
```bash
# Check actual SSH listening port
ss -tlnp | grep sshd

# Check if root login is allowed (MUST be "no" on Hetzner for root)
grep "PermitRootLogin" /etc/ssh/sshd_config

# Find non-root users with login shells (Hetzner default: creates non-root on first login)
cat /etc/passwd | grep -E ":/bin/(bash|sh)$" | grep -v "nologin\|false"

# Check SSH auth method config
grep -E "PasswordAuth|PubkeyAuth" /etc/ssh/sshd_config
cat /etc/ssh/sshd_config.d/*.conf 2>/dev/null | grep -v "^#"

# Check failed login attempts (tells you if client is reaching VPS at all)
journalctl -u ssh --no-pager -n 50 | grep -E "failed|REFUSED|invalid" | tail -15
```

**15b. Determine correct user for SSH:**
```
IF PermitRootLogin = yes  → use root
IF PermitRootLogin = no  → MUST use a non-root user
                           → check /etc/passwd for users with uid 1000+ and /bin/bash
                           → arifOS VPS has: ariffazil (uid 1002, home /home/ariffazil)
```

**15c. Add SSH key to CORRECT authorized_keys:**
```bash
# For root (if PermitRootLogin yes):
echo "ssh-ed25519 KEY user@host" >> /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

# For non-root user (ariffazil on arifOS VPS):
mkdir -p /home/ariffazil/.ssh
chmod 700 /home/ariffazil/.ssh
echo "ssh-ed25519 KEY user@host" >> /home/ariffazil/.ssh/authorized_keys
chmod 600 /home/ariffazil/.ssh/authorized_keys
chown -R ariffazil:ariffazil /home/ariffazil/.ssh
```

**15d. SSH in with the RIGHT user:**
```bash
# WRONG (will fail if PermitRootLogin no):
ssh -p 22888 root@100.111.84.52

# CORRECT (use non-root username):
ssh -p 22888 ariffazil@100.111.84.52
```

**15e. Debug failed key auth:**
```bash
# On VPS: watch auth log in real time
journalctl -u ssh --no-pager -f

# On client: verbose SSH to see exactly where auth fails
ssh -v -p 22888 ariffazil@100.111.84.52
# Look for: "Offering public key" (key sent) then "Server refused our key" (key not in authorized_keys)
```

**arifOS VPS SSH facts:**
- Port: **22888** (not 22)
- `PermitRootLogin: no` — root cannot SSH in
- Non-root user: `ariffazil` (uid 1002, home `/home/ariffazil`)
- Key must go to: `/home/ariffazil/.ssh/authorized_keys`
- Password auth: disabled (PubkeyAuthentication only)

**Tailscale SSH transport (bypasses ISP blocking):**
```bash
# Tailscale IP for af-forge VPS:
ssh -p 22888 ariffazil@100.111.84.52    # Tailscale IP (preferred)
ssh -p 22888 ariffazil@72.62.71.199     # Public IP (fallback)
```

### Step 16: Tailscale as SSH transport (bypasses ISP blocking)
If the ISP/mobile network blocks port 22/22888 outgoing, use Tailscale:
```bash
# Install Tailscale on the client device (phone/laptop)
# Authenticate to the same Tailscale network as the VPS
# VPS is already on Tailscale: verify with:
tailscale status | grep af-forge

# SSH via Tailscale IP (not public IP):
ssh -p 22888 root@100.111.84.52

# Or add to ~/.ssh/config:
Host vps
    HostName 100.111.84.52
    User root
    Port 22888
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
```
Tailscale IP is `100.111.84.52` for af-forge. This bypasses port blocking because it goes through the Tailscale tunnel, not the ISP's public internet.

Write a markdown file to `/root/VPS_ARCHITECTURE_YYYY-MM-DD.md`
- Port: **22888** (not 22)
- `PermitRootLogin: no` — root cannot SSH in
- Non-root user: `ariffazil` (uid 1002, home `/home/ariffazil`)
- Key must go to: `/home/ariffazil/.ssh/authorized_keys`
- Password auth: disabled (PubkeyAuthentication only)

**Tailscale SSH transport (bypasses ISP blocking):**
```bash
ssh -p 22888 ariffazil@100.111.84.52    # Tailscale IP (preferred)
ssh -p 22888 ariffazil@72.62.71.199     # Public IP (fallback)
```

### Step 16: Tailscale status and evaluation

**Check Tailscale on VPS:**
```bash
tailscale status --self   # Shows VPS Tailscale IP (100.111.84.52 for af-forge)
tailscale status           # Shows all peers (arif's phone = arifs-s24, laptop, GHA runners)
```

**Tailscale qualitative assessment framework:**
| Use case | Public IP enough? | Tailscale adds value? |
|----------|-------------------|------------------------|
| Home/Office WiFi SSH | ✅ Yes (port 22888 open) | Minimal — encrypts tunnel further |
| Mobile SSH (cellular/hotel/corporate) | ❌ Port often blocked by ISP/network | ✅ Bypasses port restrictions |
| arifOS HTTP traffic via Caddy | ✅ Cloudflare handles | None — already HTTPS |
| Locking down SSH to zero-public-face | ❌ Requires open port | ✅ Close 22888 to public, Tailscale-only |

**Tailscale advantages beyond SSH:**
- Encrypted tunnel — all traffic between devices and VPS is private
- No port forwarding needed on router
- VPS appears as `100.111.84.52` on Arif's phone Tailscale network — no exposure to public internet
- Can close SSH port 22888 to public entirely via UFW after Tailscale key is distributed

**When Tailscale is already active on phone:** `arifs-s24` shows `active; direct` in `tailscale status` — phone already has Tailscale running. SSH to `100.111.84.52` works through the tunnel automatically.

### Step 17: Hetzner Console rescue access

**When SSH is completely broken:** Use Hetzner Robot console (last resort access).

**URL:** https://accounts.hetzner.com
**Client number:** K0514334226
**Login:** arifbfazil@gmail.com

**Steps:**
1. Log into Hetzner Robot dashboard
2. Go to your server → Rescue → Enable rescue mode → Reboot
3. Receive temporary root password via email
4. Access via VNC in browser (no SSH needed)
5. Run `nano /root/.ssh/authorized_keys` and paste SSH key in

**Hetzner Console = browser-based KVM over IP** — full keyboard/mouse access to server regardless of network state.

Write a markdown file to `/root/VPS_ARCHITECTURE_YYYY-MM-DD.md` with sections:
1. Stack topology (ASCII diagram)
2. MCP servers table (name, port, container, type, tools, status)
3. Tool breakdown per server
4. HTTP endpoints
5. Infrastructure (DBs, LLM, observability)
6. Routing (Caddy)
7. GitHub repos
8. Integration status
9. What needs wiring
10. Disk breakdown
