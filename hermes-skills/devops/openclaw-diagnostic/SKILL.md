---
name: openclaw-diagnostic
description: Diagnose and fix OpenClaw gateway issues — CRITICAL security, Telegram errors, stuck sessions, WEALTH MCP routing
trigger: "openclaw doctor, openclaw status shows CRITICAL, Telegram errors, gateway unreachable"
version: 1.0.0
---

# OpenClaw Diagnostic Skill

## Step 1 — Quick Status
```bash
openclaw status 2>&1 | grep -E "Gateway|Tasks|error|Telegram"
openclaw channels list --verbose 2>&1
```

## Step 0 — Gateway Is NOT in Docker (CRITICAL)

**The OpenClaw gateway runs as a host-level process on the VPS — NOT inside any Docker container.**

```
Process: /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789
User:    root
Systemd: openclaw-gateway.service (user-level)
Container: NONE
```

**This means:**
- `docker restart` commands have **NO EFFECT** on the gateway
- `docker ps` will NOT show the gateway process
- The gateway must be managed via `systemctl --user` or direct `kill`/`node` commands

**Exception — `docker restart` DOES restart these federation containers** (which run the MCP servers):
- `docker restart $(docker ps -a -q --filter "name=gateway" --filter "name=arifos")` restarts arifOS-related containers
- But the host-level OpenClaw gateway at port 18789 is UNTOUCHED by docker commands

**Two-bot identity (2026-05-07 verified):**
| Bot | Username | Token | Owner | Role |
|-----|----------|-------|-------|------|
| `@ASI_arifos_bot` | ASI💃 | `8410138119:AAH...` | Hermes Agent | ASI strategic lane |
| `@AGI_ASI_bot` | AGI ASI | `8149595687:...` | OpenClaw | AGI execution lane |

Both bots are SEPARATE Telegram bots with separate tokens. Both can be members of the same Telegram group. They poll independently — no conflict.

**Verify the gateway is running (host level):**
```bash
ps aux | grep "openclaw.*gateway" | grep -v grep
# Expected: root /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789

ss -tlnp | grep 18789
# Expected: LISTEN on 127.0.0.1:18789
```

**⚠️ STUCK GATEWAY SYMPTOM (2026-05-07):**
- Port is OPEN and LISTENING (`ss -tlnp` shows it)
- `curl http://127.0.0.1:18789/health` TIMEOUTS (exit code 28)
- Process shows ~100% CPU on one core (event loop stuck)
- No CIAO watchdog messages in log
- Gateway is "alive" (port open) but non-functional (event loop deadlocked)

**⚠️ IMPORTANT — Gateway can SELF-RESOLVE (2026-05-07 verified):**
The event loop saturation (P99 > 5000ms, CPU at 100%) may clear on its own as pending work completes. The gateway was stuck (port open, /health timeout) but recovered without manual intervention. Before doing a hard restart:
1. Wait 2-3 minutes — heavy processing (bundle loading, LLM bootstrap) can saturate the event loop temporarily
2. Re-test `curl --max-time 5 http://127.0.0.1:18789/health`
3. If still timeout → proceed with hard restart procedure below

**DIAGNOSIS:**
```bash
# 1. Check if port is listening
ss -tlnp | grep 18789

# 2. Test health (if timeout = stuck event loop)
curl -s --max-time 5 http://127.0.0.1:18789/health
# Timeout = event loop stuck. If it recovers after 2-3 min → was transient load, not a hard hang.

# 3. Check event loop P99 in logs
grep "eventLoopDelayP99Ms" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | tail -3

# 4. Check for external CPU hogs (clamscan etc.)
ps aux --sort=-%cpu | head -10
```

**FIX — Hard restart (kill + start, NOT systemctl restart):**
```bash
# 1. Stop systemd unit
systemctl --user stop openclaw-gateway

# 2. Kill ALL gateway processes (may be multiple PIDs)
ps aux | grep "openclaw.*gateway" | grep -v grep | awk '{print $2}' | xargs -r kill -9
sleep 5

# 3. Verify port is FREE
ss -tlnp | grep 18789 && echo "PORT STILL HELD" || echo "PORT FREE ✅"

# 4. Start fresh via systemd
systemctl --user start openclaw-gateway
sleep 20

# 5. Verify
curl -s --max-time 5 http://127.0.0.1:18789/health
# Expected: {"ok":true,"status":"live"}
```

**NEVER use `docker restart` for the gateway.** Only `systemctl --user` + `kill` at the host level works.

---

## Step 2 — Check Gateway Reachability
```bash
openclaw gateway probe 2>&1
# If unreachable: systemctl --user restart openclaw-gateway && sleep 12
```

**⚠️ CRITICAL: `gateway probe` false negative when `bind: "lan"`**

The `openclaw gateway probe` command ALWAYS probes `ws://127.0.0.1:18789` regardless of actual bind address.
If `gateway.bind: "lan"` (VPS LAN IP 72.62.71.199), the probe will report "unreachable" even when the gateway is perfectly healthy.

**To verify gateway is actually fine — use either:**
```bash
# HTTP health check (always works)
curl -s --max-time 5 http://72.62.71.199:18789/ | head -5
# Should return HTML (OpenClaw Control UI page)

# Channel probe (authoritative)
openclaw channels status --probe 2>&1
# Returns: "Gateway reachable" + Telegram connection status

# systemctl check
systemctl --user status openclaw-gateway
# Must show: enabled, running, state active
```

**Decision tree:**
- `gateway probe` fails + `channels status --probe` says "reachable" → gateway is FINE, bind address mismatch is expected
- `gateway probe` fails + `channels status --probe` fails + HTTP fails → gateway is DOWN → restart
- `systemctl` shows `state failed` → see Step 2b (ORPHANED PROCESS pattern)

**ALWAYS check `systemctl` first** — a failed systemd unit does NOT always mean the gateway process is dead. An orphaned process may be running outside systemd's supervision.

## Step 2c — Split State Directory (`/home/af/.openclaw` vs `$HOME/.openclaw`)

**Symptom:** `openclaw doctor` reports "Multiple state directories detected. This can split session history."

**Discovery:**
```bash
# Check both paths
ls -la /home/af/.openclaw 2>/dev/null && echo "STALE: /home/af/.openclaw exists"
ls -la ~/.openclaw 2>/dev/null | head -5
echo "HOME=$HOME, USER=$(whoami)"
# If HOME=/root and /home/af/.openclaw exists → stale path from old 'af' user
```

**Fix — remove stale split path:**
```bash
rm -rf /home/af/.openclaw && echo "Removed stale /home/af/.openclaw"
# Only $HOME/.openclaw should remain as active state
```

**Prevention:** Don't run OpenClaw as different users on the same VPS. State dir is determined by the user the gateway runs as.

## Step 2b — Orphaned Gateway Process (Systemd Failed, Process Alive)

**Symptom:** `systemctl --user status openclaw-gateway` shows `failed (exit-code 78)` but:
- `curl http://127.0.0.1:18789/health` returns `{"ok":true,"status":"live"}`
- A process `node ... gateway --port 18789` is running as root
- `openclaw status` shows the gateway is reachable and sessions are active

**Root cause:** Gateway was manually started as root (e.g., `sudo node ... gateway`) AFTER the systemd service crashed. The manual root process grabbed port 18789 first. When systemd tries to start, it sees "port already in use" and fails again with code 78.

**Discovery:**
```bash
systemctl --user status openclaw-gateway
# → Active: failed (Result: exit-code) ...

ps aux | grep "openclaw.*gateway" | grep -v grep
# → root 2173308 /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway
```

**Fix — MUST kill root orphan FIRST, then start via systemd:**
```bash
# 1. Identify the orphaned PID from ps aux output above
ORPHAN_PID=2173308  # example

# 2. Kill ONLY the orphaned gateway process (not systemd's attempt)
sudo kill $ORPHAN_PID

# 3. Wait for port to clear
sleep 3

# 4. Verify port is free
ss -tlnp | grep 18789  # should return nothing

# 5. Start via systemd (NOT manually)
systemctl --user start openclaw-gateway

# 6. Verify
sleep 10
curl -s --max-time 5 http://127.0.0.1:18789/health
# Expected: {"ok":true,"status":"live"}

# 7. Verify MCP connections
openclaw mcp list
# Expected: arifos, geox, minimax, wealth, well — all listed
```

**NEVER do `systemctl --user restart` while an orphaned root process holds the port** — systemd will fail again with code 78. Always kill the orphan first.

## Step 3b — Group Missing from Allowlist (Group Silently Ignored)

**Symptom:** Bot is added to a Telegram group, `can_read_all_group_messages: true`, but OpenClaw never replies in that group. No error in logs — the group is silently dropped.

**Root cause:** `groupPolicy: "allowlist"` — ANY group must be explicitly listed in `groups: {}` in openclaw.json. If the group chat_id is not in the groups block, OpenClaw accepts the message from Telegram but drops it internally.

**Diagnosis:**
```bash
# Get the chat_id from the group (use @userinfobot or @RawDataBot)
# Then check if it's in the allowlist
python3 -c "
import json
with open('/root/.openclaw/openclaw.json') as f:
    d = json.load(f)
groups = d.get('channels', {}).get('telegram', {}).get('groups', {})
print('Configured groups:', list(groups.keys()))
# Compare with the group chat_id you're trying to add
"
```

**Fix — add group to allowlist:**
```bash
# Get current groups list
cat /root/.openclaw/openclaw.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
groups = d['channels']['telegram']['groups']
print('Current groups:', list(groups.keys()))
"

# Add the missing group (replace -100XXXXXXXXX with actual chat_id)
python3 -c "
import json
with open('/root/.openclaw/openclaw.json') as f:
    d = json.load(f)
d['channels']['telegram']['groups']['-100XXXXXXXXX'] = {'requireMention': False}
with open('/root/.openclaw/openclaw.json', 'w') as f:
    json.dump(d, f, indent=2)
print('Added group -100XXXXXXXXX to allowlist')
"

# Restart gateway
systemctl --user restart openclaw-gateway && sleep 15
```

**Key rule:** `groupPolicy: allowlist` + missing from `groups {}` = silent ignore. The bot receives the message but OpenClaw discards it. No log error.

**Also check:** Ensure `bindings` array has the correct routing:
```json
"bindings": [
  {
    "type": "route",
    "agentId": "main",
    "match": {
      "channel": "telegram",
      "accountId": "-100XXXXXXXXX"
    }
  }
]
```

## Step 3c — Kimi CLI Delegation for OpenClaw Gateway Work

**When to use:** When Arif says "beyond my role" or explicitly asks to use Kimi for OpenClaw work. The ASI (Hermes) audits but Kimi executes OpenClaw diagnostics.

**Standard delegation workflow:**
```bash
# Single command OpenClaw diagnostic (non-interactive)
kimi -y --print --no-thinking -p "Run: openclaw doctor
Fetch docs: curl -s https://docs.openclaw.ai/llms.txt
Fix ALL issues found.
Specifically ensure @AGI_ASI_bot can READ and REPLY in AAA group (chat_id: -1003753855708).
After fixes, restart: systemctl --user restart openclaw-gateway.service
Verify: curl -s http://127.0.0.1:18789/health
Report what was fixed and final health status." 2>&1

# Multi-step: session resume for context continuity
# First call (with new session):
kimi -y --print --no-thinking -p "openclaw doctor --fix" 2>&1

# Second call (resume same session if lock issues):
kimi -y --print --no-thinking -r <SESSION_ID> -p "Continue. Retry session cleanup now that lock is released.
Run: openclaw sessions cleanup --store ~/.openclaw/agents/main/sessions/sessions.json --enforce --fix-missing
Also: openclaw memory status --deep
Report results." 2>&1
```

**Key flags discovered (2026-05-06):**
- `--print` = non-interactive, output final result only
- `--no-thinking` = suppress reasoning trace logs
- `-y` = auto-approve all actions
- `-r <session_id>` = resume prior session for multi-step tasks
- `--non-interactive` = useful for openclaw doctor calls

**Session cleanup lock issue:** `openclaw sessions cleanup --enforce --fix-missing` fails with `SessionWriteLockTimeoutError` if the gateway process holds the session lock. Workaround: restart gateway first OR wait for lock to release, then retry.

**OpenClaw Doctor findings (2026-05-06 verified):**
- Session store: `~/.openclaw/agents/main/sessions/sessions.json`
- Memory search provider: ollama (bge-m3)
- Health check command: `curl -s http://127.0.0.1:18789/health` → `{"ok":true,"status":"live"}`
- Memory deep check: `openclaw memory status --deep` (more reliable than doctor summary)

## Step 3 — grammy Module (Telegram Fails to Load)

**Symptom:** `openclaw doctor --non-interactive` shows:
```
[channels] failed to load bundled channel telegram: Cannot find module 'grammy'
Require stack:
- /usr/lib/node_modules/openclaw/dist/extensions/telegram/send-t4GTTdHF.js
```

**Root cause:** OpenClaw's bundled Telegram extension requires `grammy` as a **global npm package**, not a project dependency. The module lives in `@grammyjs/grammy` globally but the extension looks for `require('grammy')`.

**Fix:**
```bash
npm install -g grammy
systemctl --user restart openclaw-gateway
sleep 8
openclaw doctor --non-interactive 2>&1 | grep -E "channels|Telegram|telegram"
# Should show: [channels] ✓ telegram: ok
```

## Step 4 — Security Audit (CRITICAL priority)
```bash
openclaw security audit 2>&1
# 3 CRITICAL = groupPolicy="open" + elevated tools exposed
```

## Step 4 — Find the REAL config file
```bash
openclaw config file  # → ~/.openclaw/openclaw.json
# NOT /srv/openclaw/workspace/config/openclaw/openclaw.json (that's the workspace copy)
```

## Step 5 — Critical Fix: groupPolicy
The `~/.openclaw/openclaw.json` Telegram config has `groupPolicy: "open"` which is a CRITICAL security issue.

Fix in `~/.openclaw/openclaw.json`:
```json
"groupPolicy": "allowlist",
"groups": {
  "-1003718232946": { "requireMention": false },
  "-1003815535761": { "requireMention": false },
  "-1003753855708": { "requireMention": false }
}
```

## Step 6d — ALL MCP Servers Unreachable via Cloudflare URLs

**⚠️ SYSTEMIC PATTERN discovered 2026-05-04**

All 4 MCP servers (arifOS, WEALTH, GEOX, WELL) were configured with their Cloudflare public URLs:
- `https://arifos.arif-fazil.com/mcp`
- `https://wealth.arif-fazil.com/mcp`
- `https://geox.arif-fazil.com/mcp`
- `https://well.arif-fazil.com/mcp`

**All 4 timeout when accessed from the VPS host itself.** This is because Cloudflare proxy cannot reach back to the origin server from inside the same VPS network — it creates a loop or is blocked by the hosting provider's firewall.

**Key diagnostic command — test ALL MCP URLs from VPS host:**
```bash
for url in \
  "https://arifos.arif-fazil.com/health" \
  "https://wealth.arif-fazil.com/health" \
  "https://geox.arif-fazil.com/health" \
  "https://well.arif-fazil.com/health"; do
  echo -n "$url: "
  curl -s --max-time 5 "$url" 2>&1 | head -1
done
# All will timeout or return 522
```

**Rule: MCP URLs in openclaw.json MUST use localhost Docker host ports when the gateway runs on the VPS itself:**
- `http://127.0.0.1:8080/mcp` for arifOS (container port 8080)
- `http://127.0.0.1:8081/mcp` for GEOX
- `http://127.0.0.1:8082/mcp` for WEALTH
- `http://127.0.0.1:8083/mcp` for WELL

**Container hostname patterns DO NOT work** (e.g., `http://wealth-organ:8082`) from the VPS host — use `127.0.0.1`.

**Correct MCP config patch (run with backup first):**
```bash
# Backup
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d%H%M%S)

# Patch all MCP URLs to localhost Docker host
cat ~/.openclaw/openclaw.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
servers = d.get('mcp', {}).get('servers', {})
fixes = {
    'arifos': 'http://127.0.0.1:8080/mcp',
    'wealth': 'http://127.0.0.1:8082/mcp',
    'geox':   'http://127.0.0.1:8081/mcp',
    'well':   'http://127.0.0.1:8083/mcp',
}
for name, url in fixes.items():
    if name in servers:
        servers[name]['url'] = url
        servers[name]['transport'] = 'streamable-http'
        print(f'Patched {name} -> {url}')
d['mcp']['servers'] = servers
print(json.dumps(d, indent=2))
" > /tmp/openclaw_mcp_localhost.json && mv /tmp/openclaw_mcp_localhost.json ~/.openclaw/openclaw.json
```

## Step 6e — arifOS MCP `/health` Returns 404 (Module Import Error)

**Symptom:**
- `curl http://127.0.0.1:8080/health` → `404 Not Found`
- `docker logs arifosmcp` shows: `REST routes registration failed: No module named 'arifosmcp.runtime.rest_routes.build_info'`
- `curl http://127.0.0.1:8080/mcp` → `Method Not Allowed` (MCP protocol IS working)

**Root cause:** `rest_routes.py` imports modules that don't exist inside the Docker image:
- `from arifosmcp.runtime.build_info import get_build_info` — module missing in image
- `from .floors import get_floor_count` — `floors.py` not in `rest_routes/` subpackage

The FastMCP server starts without REST routes, so `/health` is never registered. The MCP protocol at `/mcp` still works.

**Diagnosis:**
```bash
docker exec arifosmcp python3 -c "
import sys; sys.path.insert(0, '/app')
try:
    from arifosmcp.runtime.build_info import get_build_info
    print('build_info: OK')
except ImportError as e:
    print(f'build_info: MISSING - {e}')
try:
    from arifosmcp.runtime.rest_routes.floors import get_floor_count
    print('floors: OK')
except ImportError as e:
    print(f'floors: MISSING - {e}')
"

# Check what files actually exist in rest_routes/
docker exec arifosmcp ls /app/arifosmcp/runtime/rest_routes/
# Expected files: __init__.py rest_routes.py __pycache__/
# Missing: build_info.py, floors.py
```

**Fix — two paths:**

**Path A — Hot patch (fastest, no rebuild):**
Stub out the broken imports in the running container:
```bash
docker exec arifosmcp python3 -c "
import sys
sys.path.insert(0, '/app')

# Stub get_build_info if missing
try:
    from arifosmcp.runtime.build_info import get_build_info
except ImportError:
    import os
    # Write a minimal stub
    stub_path = '/app/arifosmcp/runtime/build_info.py'
    if not os.path.exists(stub_path):
        with open(stub_path, 'w') as f:
            f.write('def get_build_info(): return {\"version\": \"stub\", \"commit\": \"unknown\"}\\n')
        print('Created build_info stub')
"
```

**Path B — Rebuild (proper, survives container restart):**
```bash
# Check if source is ahead of image
cd /root/arifOS && git log --oneline -3
docker exec arifosmcp cat /app/.git_commit 2>/dev/null || docker exec arifosmcp cat /srv/openclaw/workspace/.git_commit

# If source is ahead, rebuild:
cd /root/arifOS
docker build -t ghcr.io/ariffazil/arifos:$(git rev-parse --short HEAD) .
docker stop arifosmcp && docker rm arifosmcp
# Re-run with same docker run flags from compose
docker run -d --name arifosmcp ... (use original docker run command from compose)
```

**Key rule:** arifOS MCP `/health` 404 is NOT the same as MCP being dead. Test `/mcp` directly:
```bash
curl -s -X POST http://127.0.0.1:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
# If this returns JSON with tools list → MCP IS WORKING, only REST routes are broken
```

## Step 6 — Fix WEALTH MCP URL

OpenClaw WEALTH MCP must use `127.0.0.1` not container hostname when gateway runs on VPS host.

Fix in `~/.openclaw/openclaw.json` (all MCP URLs use localhost Docker host):
```json
"wealth": {
  "url": "http://127.0.0.1:8082/mcp",
  "transport": "streamable-http"
}
```

**Always use `127.0.0.1` not container hostnames** (`wealth-organ`, `geox_eic`) from the VPS host.

## Step 6b — Fix WELL MCP URL (AFWELL EXPIRED TOKEN)
**Symptom:** `well_forge_precheck` and `arif_heart_critique` return `502: Upstream or external service errors`

**Root cause:** OpenClaw is configured to use `https://afwell.fastmcp.app/mcp` — an external CloudFront service whose Bearer token has expired. This is a LEGACY external dependency that should be replaced with the self-hosted WELL MCP on Arif's own VPS.

**Discovery chain:**
1. `curl https://afwell.fastmcp.app/health` → `Bearer token required`
2. `curl https://afwell.fastmcp.app/mcp` → `The access token expired`
3. `nslookup afwell.fastmcp.app` → CloudFront CDN, NOT Arif's VPS
4. `curl https://well.arif-fazil.com/health` → `{"status":"healthy"}` ✅
5. WELL container is at `localhost:8083` (bound to `127.0.0.1`) inside `arifos_core_network`

**Two configs need updating:**

1. `/root/.openclaw/openclaw.json` — add well server:
```json
"well": {
  "url": "https://well.arif-fazil.com/mcp",
  "transport": "streamable-http",
  "description": "WELL biological substrate MCP"
}
```

2. `/root/.hermes/workspace/openclaw/agents/maxhermes/workspace.yaml` — fix existing entry:
```yaml
- id: well-mcp
  url: https://well.arif-fazil.com/mcp
  enabled: true
```

**Restart:**
```bash
systemctl restart openclaw-gateway && sleep 4
openclaw mcp list  # → should show: arifos, minimax, wealth, well
```

**Verify:**
```bash
curl https://well.arif-fazil.com/health
# → {"status":"healthy","service":"well-mcp","version":"2026.04.29"} ✅
```

**Key rule:** `afwell.fastmcp.app` is dead. Always use `well.arif-fazil.com` (public) or `http://well:8083/mcp` (from inside arifos_core_network). No Bearer token needed for self-hosted.

## Step 6c — Fix GEOX MCP URL (streamable-http pattern)

**Symptom:** OpenClaw reports `failed to start server "geox" ... Streamable HTTP error: {"error":"Method not found"}` and the gateway event loop chokes (P99 delay 8000ms+, CPU at 96%+). Bundle retry loop saturates the event loop.

**Root cause:** OpenClaw bundle-mcp subsystem retries failed MCP servers on every event loop cycle. A single failing bundle creates a retry storm that chokes the entire gateway.

**Discovery:**
```bash
# Check openclaw log for bundle-mcp errors
grep "bundle-mcp\|Method not found\|failed to start server" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# Test both endpoints
curl -s -X POST https://geox.arif-fazil.com/mcp \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":0}'

curl -s -X POST https://geox.arif-fazil.com/mcp/stream \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":0}'
```

**Fix — update OpenClaw MCP config in `~/.openclaw/openclaw.json`:**

```json
"geox": {
  "url": "https://geox.arif-fazil.com/mcp",
  "transport": "streamable-http",
  "description": "GEOX Earth coprocessor MCP"
}
```

**Restart gateway:**
```bash
# Kill old gateway
kill <OLD_PID>
sleep 2

# Start fresh (background)
cd /tmp && /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789 > /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>&1 &

# Verify
sleep 10 && curl -s --max-time 5 http://localhost:18789/health
```

**Key rule:** GEOX MCP endpoint is `/mcp` (not `/mcp/stream`). The `streamable-http` transport on FastMCP registers at `/mcp`. Both `/mcp` and `/mcp/stream` routes may exist in server.py but only `/mcp` works for OpenClaw bundle initialization.
**Dual-endpoint servers:** GEOX (`/mcp/stream`), most FastMCP servers with legacy bridge.

## Step 7 — Restart gateway
```bash
systemctl --user restart openclaw-gateway && sleep 12
openclaw security audit 2>&1 | grep Summary
```

## Step 10 — Zero DM Sessions / Bot Never Replies Personally

**Symptom:** Bot works in groups, heartbeat runs, but never replies to direct messages. User says "I'm the owner @ariffazil — why won't it reply to me?"

**Diagnosis — run in this exact order:**

```bash
# 1. Test Telegram API outbound from VPS (AUTHORITATIVE)
curl -s --max-time 10 -X POST \
  "https://api.telegram.org/bot$(grep TELEGRAM_BOT_TOKEN /root/.openclaw/env.local | cut -d= -f2)/sendMessage" \
  -d "chat_id=267378578" \
  -d "text=⚖️ DM test from VPS" 2>&1 | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('ok:', d.get('ok'), 'msg_id:', d.get('result',{}).get('message_id','?'))
"
# If ok:true → VPS→Telegram outbound works. Problem is gateway inbound/processing.
# If FAILED → VPS cannot reach Telegram API (outbound firewall issue).

# 2. Check the openclaw log for sendMessage patterns
grep "sendMessage" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | tail -20
# Pattern to recognize:
#   "sendMessage ok chat=-1003753855708"      → group message SUCCEEDED ✅
#   "sendMessage ok chat=267378578"           → DM SUCCEEDED ✅
#   "sendMessage failed"                       → outbound API call FAILED (event loop choke)
#   "sendChatAction failed"                    → Telegram API timeout (less severe)
# KEY INSIGHT: group messages succeed while DMs fail = event loop saturation

# 3. Check event loop P99 — THIS IS THE USUAL CULPRIT
grep "eventLoopDelayP99Ms" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | tail -3
# If P99 > 5000ms → event loop is saturated, replies queue up and time out

# 4. Check openclaw channels probe status (has TIMEOUT issue — don't trust blindly)
timeout 15 openclaw channels status --probe 2>&1
# ⚠️ TIMEOUT at 15s ≠ Telegram disconnected
# The probe itself times out even when Telegram IS connected and sending group messages
# Verify Telegram is actually working by the log pattern above

# 5. Check Telegram pending updates queue
curl -s --max-time 10 \
  "https://api.telegram.org/bot$(grep TELEGRAM_BOT_TOKEN /root/.openclaw/env.local | cut -d= -f2)/getUpdates" \
  2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print('Pending updates:', len(d.get('result',[])))"
# If 100+ pending → stale messages are flooding the queue

# 6. Check security + DM config
cat ~/.openclaw/openclaw.json | python3 -c "
import json,sys; d=json.load(sys.stdin)
tg = d.get('channels', {}).get('telegram', {})
print('groupPolicy:', tg.get('groupPolicy'))
print('dmPolicy:', tg.get('dmPolicy'))
print('allowFrom:', tg.get('allowFrom'))
print('groupAllowFrom:', tg.get('groupAllowFrom'))
"
# groupPolicy:open = CRITICAL security issue (anyone can command the bot)
# dmPolicy must include 267378578 in allowFrom
```

**Root cause chain (most common first) — discovered through live debugging 2026-05-06:**

1. **Event loop P99 saturation** (most common during warm-up) — P99 hits 9,000–12,000ms. DM replies are queued behind heavy processing (plugin bundle loading, MCP initialization, LLM bootstrap). Eventually they time out. Group messages go through because they're already in-flight when the choke starts. **Fix: restart gateway.**

2. **Telegram pending updates queue flood** — `getUpdates` returns 100+ stale items. Every poll cycle spends its budget on old messages instead of new ones. **Fix: clear queue with `offset=-1` then restart gateway.**

3. **DM policy misconfiguration** — `dmPolicy: "allowlist"` with `allowFrom` missing or wrong Telegram ID. User's DMs are silently accepted by Telegram servers (bot receives them) but OpenClaw drops them internally. **Fix: ensure `allowFrom: ["267378578"]` and `dmPolicy: "allowlist"`.**

4. **Outside activeHours** — `activeHours: {start: "08:00", end: "23:00"}` means heartbeat and some DM handling skipped 23:00–08:00 MYT. **Fix: adjust window or set `activeHours` to null.**

5. **Heavy group session context** — AAA group session at 78%+ of 205k tokens. New DM requests in isolated sessions compete for LLM slots. Usually secondary factor on top of #1.

6. **VPS→Telegram outbound blocked** — outbound API calls fail entirely. Check with Step 1 direct curl. If FAILED: `api.telegram.org` is blocked from VPS outbound. Requires firewall review.

**Fix — in order of impact:**

```bash
# FIX 1 (highest impact): Clear pending queue + restart gateway
curl -s --max-time 10 -X POST \
  "https://api.telegram.org/bot$(grep TELEGRAM_BOT_TOKEN /root/.openclaw/env.local | cut -d= -f2)/getUpdates?offset=-1&limit=1" \
  2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print('Cleared. Pending:', len(d.get('result',[])))"

# Kill old gateway process (may be orphaned root process)
ps aux | grep "openclaw.*gateway" | grep -v grep
# If root process exists: sudo kill <PID>

# Start fresh via systemd
systemctl --user start openclaw-gateway
sleep 30

# FIX 2: Patch security config
python3 -c "
import json
with open('/root/.openclaw/openclaw.json') as f:
    d = json.load(f)
tg = d['channels']['telegram']
tg['groupPolicy'] = 'allowlist'
tg['dmPolicy'] = 'allowlist'
tg['allowFrom'] = ['267378578']
tg['groupAllowFrom'] = ['267378578']
with open('/root/.openclaw/openclaw.json', 'w') as f:
    json.dump(d, f, indent=2)
print('Security config patched: dmPolicy=allowlist, allowFrom=[267378578]')
"

systemctl --user restart openclaw-gateway
sleep 30

# FIX 3: Verify DM works
curl -s --max-time 10 -X POST \
  "https://api.telegram.org/bot$(grep TELEGRAM_BOT_TOKEN /root/.openclaw/env.local | cut -d= -f2)/sendMessage" \
  -d "chat_id=267378578" \
  -d "text=⚖️ Gateway restarted. Reply if you see this." 2>&1

# Check log for successful DM reply from gateway
sleep 10
grep "sendMessage ok chat=267378578" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | tail -3
# Expected: "[telegram] sendMessage ok chat=267378578 message=30894"
```

**Key diagnostic rules (2026-05-06 verified):**

| Log pattern | Meaning |
|-------------|---------|
| `sendMessage ok chat=-100XXXXXXX` (group ID) | Group message succeeded ✅ |
| `sendMessage ok chat=267378578` | DM reply succeeded ✅ |
| `sendMessage failed` | Outbound Telegram API failed (event loop choke) |
| `sendChatAction failed` | Less severe — typing indicator failed |
| `eventLoopDelayP99Ms=9772` | Event loop saturated — DMs queue and timeout |
| `openclaw channels status --probe` → TIMEOUT | Probe timeout ≠ channel dead. Check log for actual sendMessage status. |
| `[telegram] starting provider` | Telegram channel initializing (normal on restart) |
| `[telegram] message thread not found; retrying without message_thread_id` | DM retry in progress — will succeed if event loop is healthy |

---

## Step 11 — Known Issues That Are Non-Fatal
- **`allowWithoutThread` is NOT a valid OpenClaw group property** — attempting to add it causes `invalid config: must NOT have additional properties` and prevents gateway startup entirely. There is no config-level fix for "message thread not found" / `400: Bad Request` errors in Telegram forum groups — this is a runtime Telegram topic session state issue. The bot retries "without message_thread_id" automatically; if it still fails, the issue is bot permissions or stale thread state in Telegram, not OpenClaw config.
- **`gateway.bind: lan` + probe fails** — INTENTIONAL on VPS. Gateway binds to LAN IP (72.62.71.199) for cross-container access. `openclaw gateway probe` ALWAYS hits `127.0.0.1` and will always report "unreachable" on VPS setups. Gateway is fine — verify with `curl http://72.62.71.199:18789/` or `openclaw channels status --probe`.
- **MiniMax "cookie missing"** — non-fatal, API key works fine
- **MiniMax API health check** — MiniMax API uses `https://api.minimax.io/v1/text/chatcompletion_v2`. Model is passed in request body, not URL. Verify with:
  ```bash
  curl -s --max-time 20 -X POST https://api.minimax.io/v1/text/chatcompletion_v2 \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"MiniMax-M2.7","messages":[{"role":"user","content":"hi"}]}'
  # Returns 200 with completion → API healthy
  # Returns 2061 "token plan not support model" → wrong model name
  # Returns 2049 "invalid api key" → key bad
  ```
- **112 Telegram commands (over limit 100)** — OpenClaw says "limits bots to 100 commands. 112 configured; registering first 100." Fix: disable unused commands via `channels.telegram.commands.native: false` or reduce custom commands in config.
- **WEALTH MCP "Method not found" during bundle startup** — See Item 27 for root cause (custom `legacy_mcp_handler` missing `initialize`) and the fix. The old "transient / no fix needed" assessment was incorrect.
- **Event loop P99 spikes >5000ms during warm-up** — During gateway restart, P99 can hit 9,000–12,000ms as plugin bundles load. This causes DM replies to queue and timeout even while group messages succeed. Normal after ~2–3 minutes of uptime. If sustained >5min, check for MCP bundle retry storm (see Step 6c GEOX MCP).
- **`channels status --probe` timeout ≠ Telegram disconnected** — The probe command has a 15s timeout. It times out even when Telegram is actively connected and sending group messages. Always check the actual log for `sendMessage` success/failure patterns instead.
- **`sendMessage ok` to group + `sendMessage failed` to DM** — Classic event loop saturation signature. Group messages were already queued; DM replies get queued behind heavy processing and time out.
- **`sendChatAction failed` alone** — Non-fatal. Just means the "typing..." indicator failed. Messages still go through.
- **14 "lost" cron tasks** — backing sessions gone, cannot auto-prune, manual `openclaw tasks cancel <id>` if needed
- **GEOX `/health` returns 404** — GEOX has no `/health` route. Use `/mcp/stream` for MCP protocol; health is confirmed by successful `initialize` handshake, not a dedicated endpoint.
- **npm update available** — `openclaw update` when ready
- **Discord channel fails to load** — `Cannot find module 'discord-api-types/v10'`. Discord plugin has a missing dependency. Non-blocking if Discord not in use.

## Step 9 — Telegram Token Rotation

### Full Token Rotation Procedure (2026-05-05 verified)

**⚠️ CRITICAL: Rotating via BotFather creates a NEW bot identity.**
Old bot (`@AGI_ASI_bot`) memberships do NOT transfer to new bot (`@AAA_AGI_bot`).
Groups must re-add the new bot after rotation.

**Step 1 — Get new token from BotFather:**
```
/mybots → @BOT_USERNAME → API Token → Revoke/Regenerate
```

**Step 2 — Inject via SecretRef (NEVER raw value in openclaw.json):**
```bash
# Option A: Via openclaw config set (REQUIRES --ref-provider default)
openclaw config set channels.telegram.botToken \
  --ref-provider default \
  --ref-source env \
  --ref-id TELEGRAM_BOT_TOKEN
# WRONG (will error): --ref-source env --ref-id TELEGRAM_BOT_TOKEN (missing --ref-provider)

# Option B: Direct env.local write (for systemd EnvironmentFiles)
python3 -c "
import os
token = 'NEW_TOKEN_HERE'
env_file = '/root/.openclaw/env.local'
existing = {}
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                existing[k] = v
existing['TELEGRAM_BOT_TOKEN'] = token
with open(env_file, 'w') as f:
    for k, v in existing.items():
        f.write(f'{k}={v}\n')
print('Written')
"
```

**Step 3 — Restart gateway:**
```bash
systemctl --user restart openclaw-gateway
sleep 20  # Telegram takes 20-30s to stabilize after restart
```

**Step 4 — Verify:**
```bash
openclaw channels status --probe
# Expected: running, connected, mode:polling, bot:@NEW_BOT_NAME

# Verify token is valid (not 401):
curl -s "https://api.telegram.org/botNEW_TOKEN:getMe"
# Expected: {"ok":true,"result":{...,"is_bot":true,...}}
```

**Step 5 — Verify SecretRef (no raw token in config):**
```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
token = d.get('channels', {}).get('telegram', {}).get('botToken', '')
if isinstance(token, dict):
    print('✅ SecretRef:', token)
else:
    print('⚠️  Raw token in config — fix needed!')
"
```

**Step 6 — Set ownerAllowFrom (required for privileged commands):**
```bash
openclaw config set commands.ownerAllowFrom '["telegram:267378578"]'
systemctl --user restart openclaw-gateway
```

**Step 7 — Verify heartbeat policy:**
```bash
openclaw config set agents.defaults.heartbeat.directPolicy allow
systemctl --user restart openclaw-gateway
```

**Systemd secret injection:** The gateway reads `EnvironmentFiles=/root/.openclaw/env.local` on startup. The token in env.local is loaded before the gateway process starts, satisfying the SecretRef lookup.

### Step 9b — Orphan Session Transcripts

**Symptom:** `openclaw doctor` shows "572 orphan transcript files" or similar.

**Fix — archive orphans (include trajectory files too):**
```bash
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
COUNT=$(ls "$SESSIONS_DIR"/*.jsonl 2>/dev/null | wc -l)
echo "Orphan transcripts: $COUNT"
for f in "$SESSIONS_DIR"/*.jsonl; do
  [ -f "$f" ] && mv "$f" "${f%.jsonl}.deleted.$(date +%s)"
done
# Also archive orphaned .trajectory.jsonl files that reference missing sessions
for f in "$SESSIONS_DIR"/*.trajectory.jsonl; do
  [ -f "$f" ] && [ ! -f "${f%.trajectory.jsonl}.jsonl" ] && \
    mv "$f" "${f%.trajectory.jsonl}.trajectory.deleted.$(date +%s)" && \
    echo "Archived trajectory: $f"
done
REMAIN=$(ls "$SESSIONS_DIR"/*.jsonl 2>/dev/null | wc -l)
echo "Archived: $((COUNT - REMAIN)) | Remaining: $REMAIN"
```

**Verify sessions are healthy:**
```bash
openclaw sessions --active 120
# Expected: sessions listed with recent age
```

## Step 10 — Post-Rotation Telegram Checks

```bash
# Confirm Telegram is connected (takes ~20s after restart)
openclaw channels status --probe
# → connected, mode:polling ✅

# Confirm gateway event loop healthy
journalctl --user -u openclaw-gateway -n 20 --no-pager 2>&1 | \
  grep -i "telegram\|error\|connected\|disconnected" | tail -10

# Confirm MCP tools still accessible
openclaw mcp list
# → arifos, geox, minimax, wealth, well ✅

# Verify all 5 MCP endpoints
for port in 8080 8081 8082 8083; do
  echo -n "Port $port: "
  curl -s --max-time 3 http://127.0.0.1:$port/health | python3 -c \
    "import json,sys; d=json.load(sys.stdin); print(d.get('status','??'))" 2>/dev/null || echo "FAIL"
done
# Expected: healthy × 4 (arifOS, GEOX, WEALTH, WELL)
```

## Common Root Causes
1. Event loop P99 saturation → DM replies queue and timeout while group messages succeed → restart gateway
2. Telegram pending updates flood (100+ stale) → clear queue with `getUpdates?offset=-1` + restart gateway
3. Telegram outbound API intermittent failures → VPS network flakiness; direct curl test confirms
4. Orphaned gateway process (systemd failed, root process alive) → `sudo kill <PID>` first, then `systemctl --user start`
5. WEALTH MCP wrong URL → fix to `127.0.0.1:8082/mcp` (localhost, not hostname)
6. ALL Cloudflare MCP URLs timeout from VPS host → always use `127.0.0.1:<port>/mcp` for local Docker containers
7. `groupPolicy: "open"` → CRITICAL security; set to `"allowlist"` with explicit groupIds
8. GEOX MCP bundle retry storm → failing MCP bundles retry every event loop cycle, saturating CPU
9. `/tmp` full → ENOSPC on gateway lock file → gateway crash loop
10. MEMORY.md oversized → OpenClaw workspace bootstrap has a 12,000-char limit
11. arifOS `/health` 404 → rest_routes.py import errors; test `/mcp` directly for MCP health
12. `allowWithoutThread` NOT valid → invalid property → gateway fails to start; no config fix for Telegram topic thread errors
13. Orphan gateway process → kill with `kill -9 <PID>` then verify port free before `systemctl --user start`
14. Two PIDs after restart → orphan not fully killed; kill both and restart cleanly
12. grammy module missing → `npm install -g grammy`
13. Telegram 401 Unauthorized after token rotation → bot identity changed; re-add to groups
14. `openclaw channels status --probe` timeout → probe timeout ≠ channel dead; check log for sendMessage patterns
15. Orphan transcript files → `openclaw doctor` reports hundreds; fix via archive script
16. **Split state directory** — two `~/.openclaw` paths detected (`/home/af/.openclaw` vs `$HOME/.openclaw`). Only `$HOME/.openclaw` is active. Remove stale path: `rm -rf /home/af/.openclaw`

### Step 15 — Duplicate Telegram Bot Token from Phantom Account

**Symptom:** `openclaw channels status` shows TWO Telegram accounts with the same bot token:
```
- Telegram 1003753855708: running, connected
- Telegram 1003890512851: error: Duplicate Telegram bot token: account "1003890512851" shares a token with account "1003753855708"
```
The second account (`1003890512851`) is NOT a real Telegram bot — it's a phantom created by a stale group chat_id in config.

**Root cause:** A numeric chat_id in `bindings[]` with `accountId: "-100XXXXXXXXX"` causes OpenClaw to treat it as a second Telegram account sharing the same token. This can happen when:
- A group was previously configured, then removed from `groups {}` but its binding entry was left behind
- A stale `-100XXXXXXXXX` chat_id exists in `bindings[]` pointing to the `main` agent

**Diagnosis — find phantom accounts:**
```bash
openclaw channels status 2>&1
# If a second Telegram account appears with "Duplicate Telegram bot token" → phantom account

# Check bindings for numeric accountId entries
cat ~/.openclaw/openclaw.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
for b in d.get('bindings', []):
    acc = b.get('match', {}).get('accountId', '')
    if acc.startswith('-100'):
        print(f'Phantom candidate in bindings: {acc} -> {b.get(\"agentId\")}')
"
```

**Fix — remove phantom from BOTH `groups{}` AND `bindings[]`:**
```bash
# 1. Remove from groups block
python3 -c "
import json
with open('/root/.openclaw/openclaw.json') as f:
    d = json.load(f)
phatom_id = '-1003890512851'
groups = d['channels']['telegram']['groups']
if phatom_id in groups:
    del groups[phatom_id]
    print(f'Removed {phatom_id} from groups')
bindings = d['bindings']
d['bindings'] = [b for b in bindings
                 if b.get('match', {}).get('accountId') != phatom_id]
print(f'Removed {phatom_id} from bindings ({len(bindings)} -> {len(d[\"bindings\"])} entries)')
with open('/root/.openclaw/openclaw.json', 'w') as f:
    json.dump(d, f, indent=2)
"

# 2. Restart (kill orphan root process first if needed)
systemctl --user stop openclaw-gateway
sleep 3
systemctl --user start openclaw-gateway
sleep 25

# 3. Verify — should show only ONE Telegram account
openclaw channels status 2>&1
# Expected: only 1003753855708, no duplicate
```
17. **MiniMax 2049 `invalid api key` — BLOCKING** (discovered 2026-05-07)

**Symptom:** All reasoning/reasoning-heavy responses fail. OpenClaw returns errors or falls back to Ollama silently.

**Root cause:** The active MiniMax key `***REDACTED***` is returning `{"base_resp":{"status_code":2049,"status_msg":"invalid api key"}}`.

**Confirmed dead across all locations:**
- `/root/.secrets/vault.env`: `# MINIMAX_API_KEY ❌ DEAD` (already commented out)
- Live `arifosmcp` container: same dead key injected
- Direct API test from VPS: 2049 confirmed

**Diagnostic:**
```bash
curl -s -X POST "https://api.minimax.chat/v1/text/chatcompletion_v2" \
  -H "Authorization: Bearer ***REDACTED***" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2.7","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'
# → {"base_resp":{"status_code":2049,"status_msg":"invalid api key"}}
# If 2049: key is dead. If different error (e.g., 2061): key alive but wrong model.
```

**Short-term fallback available:**
- Ollama `qwen2.5:7b` at `localhost:11434` — confirmed live, no API key needed
- SEA-LION (`sk-znz...ewfr`) — live but 401 + 32K context < 64K minimum

**Fix path:**
1. Get fresh MiniMax key from https://www.minimaxi.com/
2. Update `/root/.secrets/vault.env` (uncomment and replace)
3. Update all `.env` files that reference the dead key
4. Restart affected services

**Why this matters:** MiniMax is the primary reasoning model. Until a new key is installed, every agent relying on MiniMax is operating with degraded reasoning quality.

---

18. **112 Telegram commands exceed 100-bot-limit** — OpenClaw silently registers first 100, drops the rest. Fix in `~/.openclaw/openclaw.json`: `"channels.telegram.commands.native": false` OR reduce custom commands count
17. Memory search ollama shows "not confirmed" in doctor but IS actually healthy — `openclaw memory status --deep` shows `Embeddings: ready`, `Vector: ready`, `FTS: ready`. Doctor health-check has a timeout false-negative; ignore this warning if `--deep` confirms healthy.
22. **Hermes curl stealing OpenClaw's Telegram updates** — ROOT CAUSE of "OpenClaw silent but polling connected". Every `curl getUpdates` consumed messages from Telegram's queue before OpenClaw's polling session could process them. OpenClaw saw the message, tried to reply, but the message was already acked → "reply target deleted" / "reply target not found" error. **Fix: STOP using curl for Telegram. Let OpenClaw exclusively own its polling session. Use only OpenClaw's own `openclaw channels status` and log analysis for diagnostics.**

23. **Two bot tokens on VPS (2026-05-06 verified)** — Hermes Agent uses `@ASI💃` (`841013...19DA`) via `/root/.hermes/.env`. OpenClaw uses `@AGI_ASI_bot` (`814959...wy70`) via `/root/.openclaw/env.local`. These are SEPARATE bots. The "Duplicate Telegram bot token" error occurs when BOTH configs point to the SAME bot AND both processes poll Telegram simultaneously. Separation by itself (different bots) eliminates the 409 Conflict. Both can poll simultaneously without conflict.

24. **hdfr group needs BOTH groups{} entry AND bindings[] entry** — A group in `channels.telegram.groups{}` only allows the bot to READ messages. A `bindings[]` entry routes the channel+accountId to a specific agentId. Without the binding, the group messages reach OpenClaw but get routed to a default/null agent and produce no response. Both are required:
    - `channels.telegram.groups["-100XXXXXXXXX"]` = allowlist (read permission)
    - `bindings[{match: {channel: "telegram", accountId: "-100XXXXXXXXX"}, agentId: "main"}]` = routing (which agent handles it)

25. **Multi-PID restart failure pattern** — After a crash or failed restart, multiple orphaned node processes can hold port 18789 simultaneously. `systemctl start` fails because the port is already in use. `systemctl restart` fails because old processes haven't fully released the port. **Clean restart sequence:**
    ```bash
    # Kill ALL openclaw gateway processes (may be multiple PIDs)
    ps aux | grep "openclaw.*gateway" | grep -v grep | awk '{print $2}' | xargs -r kill -9
    sleep 5
    # Verify port is FREE
    ss -tlnp | grep 18789 && echo "PORT STILL HELD" || echo "PORT FREE ✅"
    # ONLY NOW start fresh
    systemctl --user start openclaw-gateway
    sleep 15
    curl -s --max-time 5 http://127.0.0.1:18789/health
    ```

26. **Telegram polling "running, connected" but OpenClaw appears silent** — If VPS `curl getUpdates` returns 0 pending BUT OpenClaw is still silent, the issue is likely: (a) Hermes curl stole the messages earlier (see #22), or (b) flood control from prior excessive sends (wait 30s), or (c) event loop saturation (P99 > 5000ms causes replies to queue and timeout). Check log: `grep "sendMessage ok\|response ready" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -5`. If log shows "response ready" + "Sending response" → OpenClaw IS working, Telegram just hasn't received yet due to flood control.

27. **WEALTH MCP "Method not found" during bundle startup** — OpenClaw's bundle-mcp subsystem sends JSON-RPC `initialize` to WEALTH on probe. WEALTH uses a custom `legacy_mcp_handler` in `internal/monolith.py:4255` that bypasses FastMCP's native HTTP handler. The `legacy_mcp_handler` only implements `tools/list` and `tools/call` — it returns `"Method not found"` for `initialize`, causing bundle probe to fail. WEALTH IS working (50 tools accessible via `curl -X POST http://127.0.0.1:8082/mcp -d '{"method":"tools/list"}'`), but OpenClaw can't establish the MCP session.

**Fix — add `initialize` handler to `legacy_mcp_handler`:**

```python
# Location: /root/WEALTH/internal/monolith.py
# Insert in legacy_mcp_handler() just BEFORE the final "Method not found" return (~line 4294)
if method == "initialize":
    return _JR({
        "jsonrpc": "2.0",
        "id": response_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": True}},
            "serverInfo": {"name": "WEALTH", "version": __version__},
        }
    })
```

**Deploy — WEALTH container has NO bind mount:**
```bash
# Copy patched file into container (container has its own copy, no volume mount)
docker cp /root/WEALTH/internal/monolith.py wealth-organ:/app/internal/monolith.py

# Restart container
docker restart wealth-organ
sleep 8

# Verify initialize now works
curl -s --max-time 5 -X POST http://127.0.0.1:8082/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":0}'
# Expected: {"jsonrpc":"2.0","id":0,"result":{"protocolVersion":"2024-11-05",...}}

# Restart gateway to reload bundle
systemctl --user restart openclaw-gateway && sleep 25

# Verify bundle health
openclaw doctor --non-interactive 2>&1 | grep -E "Errors:|MCP servers"
# Expected: Errors: 0, all 5 servers listed
```

**Key discovery (2026-05-07):** WEALTH's container has `Entrypoint: ['python', 'internal/monolith.py']` with NO bind mount to the host repo. All edits must be `docker cp`'d in. This is different from arifOS/GEOX which DO have bind mounts.

**Why this isn't caught by FastMCP's native handler:** WEALTH wraps `mcp_app` (FastMCP) under `Mount("/", app=mcp_app)` but also registers `Route("/mcp", legacy_mcp_handler)` which runs BEFORE the mount catches it. The `legacy_mcp_handler` short-circuits all requests to `/mcp` before FastMCP sees them.

**Note:** Adding `initialize` to `legacy_mcp_handler` is the surgical fix. The full/better fix would be to remove the `legacy_mcp_handler` route entirely and let FastMCP handle `/mcp` natively — but that requires testing all tools/call paths first.

28. **openclaw channels status telegram → "groups:unmentioned"** — This means the group config has `requireMention: false` for all groups.

29. **Bot token validity test** — VPS can reach Telegram API: `curl -s --max-time 10 "https://api.telegram.org/bot$TOKEN/getMe"` returns `{"ok":true,...}`. If this succeeds but `sendMessage` still fails, the issue is OpenClaw's event loop or the message payload (reply_to message ID no longer valid, etc.).

### Step 15b — P99 Event Loop Saturation: External CPU Contention

**Symptom:** `eventLoopDelayP99Ms` shows WARNING (>2000ms) or CRITICAL (>5000ms). `cpuCoreRatio` near or at 1.0. OpenClaw event loop is congested but the cause may NOT be OpenClaw itself.

**Discovery (2026-05-07):**
```bash
# Check ALL CPU consumers — sort by %CPU
ps aux --sort=-%cpu | head -10
```

**Key rule:** A rogue `clamscan` process consuming 97% CPU will starve the Node.js event loop WITHOUT any OpenClaw internal issue. The P99 degradation is a symptom of external CPU contention, not gateway failure.

**Real-world example (2026-05-07):**
```
PID 954448: clamscan -r --infected / \
  Started: 03:30 UTC
  CPU: 97.0% — STARVING Node.js event loop
  P99: 6,459ms (was 332ms immediately after gateway restart)

Clamscan doing full root filesystem scan (1.1M+ files, 55GB+)
Duration: ~160 minutes for full scan
```

**Diagnosis chain:**
1. `eventLoopDelayP99Ms` elevated → don't restart gateway immediately
2. Run `ps aux --sort=-%cpu | head -10` to find external CPU hogs
3. If clamscan at 97% CPU → THIS is the P99 cause, not OpenClaw
4. Kill it: `kill -9 <PID>` — P99 recovers within minutes

**Fix — kill the rogue scan:**
```bash
# 1. Identify PID
ps aux | grep clamscan | grep -v grep

# 2. Kill it
sudo kill -9 <PID>

# 3. Verify P99 recovery (wait 2-3 minutes)
sleep 120
curl -s http://localhost:18789/diagnostics | python3 -c "
import json, sys
d = json.load(sys.stdin)
p99 = d.get('eventLoopDelayP99Ms', 'N/A')
print(f'P99: {p99}ms')
"

# Expected: P99 back to 200-500ms range
```

**Why restarting gateway alone doesn't fix this:** The rogue process keeps consuming CPU. Even a fresh gateway restart will immediately degrade again. Kill the external process FIRST.

**Prevention:** Check crontab for legitimate clamav scans vs rogue ones:
```bash
# Legitimate daily scan (limited scope)
0 3 * * * /usr/bin/clamscan -r /srv/arifosmcp ...

# Rogue full-filesystem scan — check if it's from cron or a separate process
# A full scan of '/' started by cron will show in crontab
# A full scan running outside cron = rogue process
```

---

### Step 15 — Duplicate Telegram Bot Token from Phantom Account

**Symptom:** `openclaw cron list` shows `arifOS-KERNEL-EVALS` in error state for 2+ days. `breach_test_runner.py` exits 1 with no output. `mcp_inspector_test.py --all` produces 0 results.

**Diagnosis:**
```bash
# Check cron job error
openclaw cron list
# Note the job ID, then check its last error output via logs

# Verify eval tools are stubs (the REAL cause)
cd /root/arifOS
python3 -c "
import sys; sys.path.insert(0, '/root/arifOS')
from arifosmcp.runtime.tools import _wrap_call
result = _wrap_call('agi_reason', query='Is deleting /root reversible?', mode='reason')
print('verdict:', result.get('verdict'))
print('payload:', result.get('payload'))
print('nine_signal:', result.get('nine_signal'))
print()
print('ALL NULL = tools are stubs, no real reasoning backend wired')
print('Has real output = tools are working')
"

# Also check if the right module names even exist
python3 -c "
import sys; sys.path.insert(0, '/root/arifOS')
try:
    from arifosmcp.runtime.tools import arifos_mind
    print('arifos_mind: EXISTS')
except ImportError:
    print('arifos_mind: DOES NOT EXIST (wrong import in breach_test_runner.py)')
try:
    from arifosmcp.runtime.tools import agi_reason
    print('agi_reason: EXISTS')
except ImportError:
    print('agi_reason: DOES NOT EXIST')
"
```

**Root cause:** The arifOS eval tools are STUBS. `_wrap_call()` in `tools.py:126-145` is a pure passthrough:
```python
def _wrap_call(name, **kwargs):
    return {"ok": True, "tool": name, "kwargs": kwargs,
            "verdict": None, "payload": None, "nine_signal": None}
```
It returns inputs wrapped in a dict — no actual reasoning, no constitutional judgment, no tool execution.

The three test files have additional problems:
- `breach_test_runner.py` imports `arifos_mind` which doesn't exist (wrong name)
- `mcp_inspector_test.py` tests external substrates (filesystem/git/fetch) — NOT arifOS itself
- `substrate_alignment_test.py` imports `arifos_fetch` which doesn't exist

**Options:**

**Option A — Quick fix (silence the cron):**
```bash
openclaw cron list
# Find arifOS-KERNEL-EVALS job ID
openclaw cron delete <JOB_ID>
# Recreate after fixing tools
```

**Option B — Real fix (wire the tools to actual backend):**
The `_wrap_call()` function needs to be replaced with real implementations that route to an actual LLM/reasoning backend. This is a major implementation task — the entire `tools.py` section needs real tool bodies.

**Note:** The arifOS MCP itself IS healthy (13 tools loaded, 8080 responding). The problem is specifically the `agi_reason`, `AGI_REFLECT`, `ASI_CRITIQUE`, `ASI_SIMULATE`, `APEX_JUDGE`, `VAULT_SEAL` tools — these are stubs. The cron job tests these stubs and gets nulls back, producing errors.

---

## `/tmp` Full — ENOSPC Crash Loop

**Symptom:** `journalctl` shows `ENOSPC: no space left on device` and `gateway already running under systemd; existing gateway is healthy, exiting with code 78`. Gateway appears in a restart loop.

**Diagnosis:**
```bash
df -h /tmp
# → tmpfs 7.9G 100% Used  # ← /tmp is tmpfs, 100% full
du -sh /tmp/
# → may show 7.9G even with lsof showing 0 deleted files (ghost files)
```

**Root cause:** Ghost files — deleted files still held open by running processes. `lsof +D /tmp | grep deleted` may show 0, but `du` still shows full because kernel maintains the deleted file's data in open file descriptors.

**Fix:**
```bash
# 1. Stop gateway and all openclaw processes
systemctl --user stop openclaw-gateway
pkill -f "openclaw.*gateway"  # kill ALL gateway processes

# 2. Clear /tmp of known workspace garbage
rm -rf /tmp/open_well_logs /tmp/arifOS-check /tmp/arifos-cleanup \
       /tmp/oo0-state-check /tmp/geox-inspect /tmp/arifos-backup \
       /tmp/arifos-surgery /tmp/arifos.git /tmp/arifos-fresh \
       /tmp/arifos-push /tmp/chrome-cdp-test /tmp/chrome-profiles \
       /tmp/node_modules /tmp/hermes-agent.tar.gz \
       /tmp/openclaw-2026.4.24.tgz /tmp/openclaw-2026.4.23-beta.5.tgz \
       /tmp/*.las /tmp/*.wav /tmp/gemini-client-error* \
       /tmp/Kansas* /tmp/BOKOR* /tmp/arifos*

# 3. Verify free space
df -h /tmp  # → should show ~18% used (1.4G) with 6.5G free

# 4. Restart gateway fresh
systemctl --user start openclaw-gateway
sleep 20
openclaw cron list  # → should work
```

**Prevention:** Old agent workspace operations leave large artifacts in `/tmp`. Clean periodically or set up a cron job to prune `/tmp` weekly.

---

## Cron CLI — Correct Usage

**Critical CLI quirks discovered through trial and error:**

| Goal | Wrong | Correct |
|------|-------|---------|
| Edit delivery target | `openclaw cron edit <id> --set.delivery` | **Delete + recreate** — `edit` has no `--set.*` flags |
| Edit any cron field | `openclaw cron edit <id> --set.field value` | **Delete + recreate** — no field-level update supported |
| View cron job details | `openclaw cron get <id>` | **Does not exist** — `cron` subcommand takes 0 args |
| Find job IDs | `openclaw cron list` | Shows all jobs with IDs, status, delivery targets |
| Create with delivery | `--delivery` | `--deliver` (different flag, deprecated meaning) |
| Create with message | `openclaw cron add <id> <message>` (positional) | `--message "..."` flag only; no positional args |
| Disable at create time | `--enabled false` | `--disabled` flag (absence of flag = enabled) |

**Delete + Recreate pattern:**
```bash
# Find the job
openclaw cron list
# → ID  Name  Status  Delivery

# Delete it
openclaw cron delete <ID>

# Recreate with corrections
openclaw cron add \
  --name "sites-health-15min" \
  --every "15m" \
  --agent "main" \
  --to "267378578" \
  --best-effort-deliver \
  --message "curl -s --max-time 5 https://arif-fazil.com/health && echo ALL_UP"
```

**Useful create flags:**
- `--every "15m"` or `--cron "0 */6 * * *"` with `--tz "Asia/Kuala_Lumpur"`
- `--announce` — fallback deliver to Telegram (with `--to "267378578"`)
- `--best-effort-deliver` — don't fail job if Telegram delivery fails
- `--light-context` — cheaper bootstrap for automation jobs

**Gateway bind mismatch (another crash loop cause):**
- Config has `bind: "lan"` but CLI uses loopback → `gateway closed (1000)` on every CLI command
- Fix: `patch` openclaw.json: `"bind": "loopback"` then `systemctl --user restart openclaw-gateway`
- Also: old process (pid from previous crash) fights new one → always `pkill -f "openclaw.*gateway"` before restart

## Step 12 — AAA Group: Agents Streaming Partial Text / Interrupting Each Other

**Symptom:** In the AAA group chat, agents interrupt each other mid-thought. You see partial responses, reasoning chains, or stream fragments posted to the group while an agent is still thinking.

**Root cause (discovered 2026-05-06):** Two OpenClaw config settings control group reply behavior:

1. **`messages.queue.mode: "steer"`** — queued messages get injected into the active run at the next model boundary while the agent is still generating. This causes agents to see each other's partial outputs and potentially respond mid-stream.

2. **`messages.groupChat.visibleReplies: "automatic"`** — the gateway auto-posts every final reply to the group as soon as it completes. Combined with `steer`, this means partial/queued content can leak into the group.

**Fix — patch `~/.openclaw/openclaw.json`:**
```bash
# Backup
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d%H%M%S)

# Apply both fixes
python3 -c "
import json
with open('/root/.openclaw/openclaw.json') as f:
    d = json.load(f)
d['messages'] = d.get('messages', {})
d['messages']['queue'] = d['messages'].get('queue', {})
d['messages']['queue']['mode'] = 'followup'
d['messages']['groupChat'] = d['messages'].get('groupChat', {})
d['messages']['groupChat']['visibleReplies'] = 'message_tool'
print(json.dumps(d, indent=2))
" > /tmp/oc_messages_fix.json && mv /tmp/oc_messages_fix.json ~/.openclaw/openclaw.json
```

**What each setting does:**
- `"queue.mode": "followup"` — new group messages wait for the current response to finish before being delivered to the agent. No mid-stream interruptions.
- `"groupChat.visibleReplies": "message_tool"` — agents must explicitly `send` to the group. No auto-broadcast of partial or final text.

**⚠️ After patch: `visibleReplies: "message_tool"` means agents in AAA group must use the message tool to post.** The system prompt tells agents this automatically. Existing agent instructions should already say "reply normally" — with `"message_tool"` mode, "reply normally" maps to the message tool send action.

**Restart and verify:**
```bash
# Check for orphaned process FIRST (see Step 2b pattern)
ps aux | grep "openclaw.*gateway" | grep -v grep
# If a root process is on port 18789 → sudo kill <PID> first

systemctl --user stop openclaw-gateway && sleep 3
systemctl --user start openclaw-gateway && sleep 20

curl -s --max-time 5 http://127.0.0.1:18789/health
# Expected: {"ok":true,"status":"live"}

openclaw channels status --probe | grep Telegram
# Expected: running, connected, mode:polling
```

**`openclaw doctor` findings to address each run:**
```bash
# Session store cleanup
openclaw sessions cleanup --store ~/.openclaw/agents/main/sessions/sessions.json --enforce --fix-missing

# Archive orphan transcripts (from doctor output — list the filenames)
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
for f in $SESSIONS_DIR/6e6232ed-c0a7-4886-9976-b6520fe7bcb0*.jsonl; do
  [ -f "$f" ] && mv "$f" "${f%.jsonl}.deleted.$TIMESTAMP.jsonl" && echo "Archived: $f"
done

# Verify no more orphan warnings
openclaw doctor 2>&1 | grep -E "orphan|missing|State integrity"
```

**Key lesson:** The orphan-process-after-restart pattern recurs every session. Always check `ps aux | grep openclaw.*gateway` before `systemctl start`. Kill root orphan first, then start via systemd.

---

## Step 13 — Reasoning Content Leaking to Telegram

**Symptom:** MiniMax `reasoning_content` appears in Telegram replies. Users see raw chain-of-thought text prefixed with "reasoning:" visible in group chat.

**Root cause (discovered 2026-05-06):** Two-layer failure:
1. OpenClaw sends `thinking: { type: "disabled" }` in the API request payload — but MiniMax-M2.7 **ignores this** and still returns `reasoning_content` in the response
2. In `openai-transport-stream-aPa0aR5w.js` lines 536-539, when `isSameModel = false` (model/provider/api string mismatch), thinking blocks are **converted to visible text** and pushed into the content stream:
   ```javascript
   // LEAK: thinking content becomes visible Telegram text
   content.push(isSameModel ? block : {
       type: "text",
       text: block.thinking   // ← reasoning_content leaked here
   });
   ```

**Diagnosis:**
```bash
# Test if MiniMax respects thinking:disabled
curl -s --max-time 10 -X POST https://api.minimax.io/v1/text/chatcompletion_v2 \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2.7","messages":[{"role":"user","content":"Hi"}],"thinking":{"type":"disabled"}}' \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
msg = d.get('choices',[{}])[0].get('message',{})
rc = msg.get('reasoning_content','')
print('reasoning_content present:', bool(rc))
print('content:', msg.get('content','')[:60])
"
# If reasoning_content is present despite thinking:disabled → API ignores it
```

**Fix — patch the stream file to drop thinking for non-same-model:**
```bash
STREAM_FILE="$HOME/.openclaw/plugin-runtime-deps/openclaw-2026.4.29-4eca5026e977/dist/openai-transport-stream-aPa0aR5w.js"

# Backup
cp "$STREAM_FILE" "$STREAM_FILE.bak.$(date +%Y%m%d%H%M%S)"

# Patch: replace the thinking→text leak with a silent drop for non-same-model
sed -i 's/if (!block\.thinking\.trim()) continue;/if (!block.thinking.trim()) continue;\n\t\t\t\tif (!isSameModel) continue; \/\/ DROP: prevent reasoning_content leak to Telegram/' "$STREAM_FILE"

# Restart gateway
systemctl --user restart openclaw-gateway
sleep 20

# Verify Telegram — reasoning should stop appearing
```

**Note:** This is a hot-patch inside the plugin-runtime-deps directory. It survives `systemctl restart` but NOT `openclaw update` which replaces plugin bundles. Re-apply after update if reasoning reappears.

**Why `isSameModel` is false for MiniMax:** The model string in openclaw.json is `minimax/MiniMax-M2.7` but the streaming transport may normalize it differently, causing `isSameModel = msg.provider === model.provider && msg.api === model.api && msg.model === model.id` to evaluate `false`, triggering the text conversion path.

---

## Step 14 — CIAO/Bonjour Watchdog Restart Loop (v2026.4.29 Bug)

**Symptom:** Gateway crashes every ~6 seconds in a restart loop. Log shows repeating pattern:

```
01:54:51 [INFO] starting HTTP server...
01:54:51 [INFO] started (interval: 300s, startup-grace: 60s, ...)
01:54:57 [WARN] bonjour: watchdog detected non-announced service; attempting re-advertise
01:54:58 [WARN] bonjour: gateway name conflict resolved; newName="af-forge (OpenClaw) (2)"
01:54:58 [INFO] bonjour: advertised gateway fqdn=af-forge (OpenClaw) (2)._openclaw-gw._tcp.local...
01:54:59 [INFO] shutdown started: gateway startup failed
01:54:59 [WARN] bonjour: suppressing ciao cancellation: CIAO ANNOUNCEMENT CANCELLED
01:54:59 [WARN] bonjour: suppressing ciao cancellation: CIAO PROBING CANCELLED
```

Systemd auto-restarts → same pattern repeats. Gateway is reachable between crashes because systemd keeps bringing it back up.

**Root cause:** OpenClaw v2026.4.29 CIAO/Bonjour mDNS watchdog has a bug where it triggers `CIAO ANNOUNCEMENT CANCELLED` or `CIAO PROBING CANCELLED` on every startup, causing the gateway to call `shutdown started: gateway startup failed` and exit. Systemd restarts it, loop repeats.

**Discovery:**
```bash
# Look for the repeating pattern in logs
grep -E "CIAO|shutdown started: gateway startup failed|watchdog detected non-announced" \
  /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -20

# Check if gateway is alive despite the crashes (systemd keeping it up)
systemctl --user status openclaw-gateway
# → active (running) but showing rapid restarts or young uptime

# Check event loop - will show elevated P99 even when gateway is "stable"
grep "eventLoopDelayP99Ms" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -3
```

**Key diagnostic rule:** The log shows BOTH "shutdown started: gateway startup failed" AND "gateway ready" in the same session = CIAO watchdog bug. The gateway starts, CIAO fires, shutdown triggers, but systemd catches and restarts before port is freed. Multiple restarts accumulate → event loop stays saturated (P99 6000-12000ms).

**Fix — No permanent fix without OpenClaw update.** Workarounds in order of preference:

**Workaround A — Let systemd manage it (recommended for now):**
The gateway IS working between crashes. Systemd auto-restarts it. After ~2-3 restarts within 10 minutes, the CIAO watchdog may settle down and the gateway stays up. Monitor:
```bash
# Watch for stability
for i in {1..6}; do
  systemctl --user status openclaw-gateway | grep "Active:"
  ss -tlnp | grep 18789 || echo "PORT DOWN"
  sleep 15
done
# If active (running) for 5+ consecutive minutes → stable
```

**Workaround B — Systematic clean restart (when gateway is in crash loop AND systemd can't keep up):**
```bash
# 1. Stop systemd AND kill ALL openclaw processes simultaneously
systemctl --user stop openclaw-gateway
sudo pkill -9 -f "openclaw.*gateway"
sleep 5

# 2. Verify port is FREE (critical - orphaned processes can hold port)
ss -tlnp | grep 18789 && echo "PORT STILL HELD" || echo "PORT FREE ✅"

# 3. ONLY NOW start via systemd
systemctl --user start openclaw-gateway
sleep 20

# 4. Verify gateway is up and Telegram connected
curl -s --max-time 5 http://127.0.0.1:18789/health
grep "sendMessage ok\|Telegram" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -5
```

**Why Workaround B works:** The CIAO bug fires on EVERY fresh start. By killing all processes and waiting 5 seconds, we ensure no ghost processes interfere when systemd brings up the fresh gateway.

**Why `systemctl restart` alone doesn't fix it:** `systemctl restart` tries to stop then start in quick succession. If the old process hasn't fully released the port (or a zombie remains), the new start hits "port already in use" and fails. Always do explicit `stop` + `pkill -9` + wait + `start`.

**When to suspect this bug vs other issues:**

| Symptom | Likely cause |
|---------|-------------|
| Gateway restarts every ~6s, "CIAO ANNOUNCEMENT CANCELLED" in log | CIAO bug (this step) |
| Gateway down, `systemctl failed`, no orphan process | Actual crash, check `journalctl` |
| Gateway down, orphan root process on port 18789 | Orphaned process (Step 2b) |
| Gateway up but P99 > 5000ms for >5 min | MCP bundle retry storm (Step 6c) or CIAO bug warming up |
| Telegram not replying, log shows `sendMessage failed` | Event loop saturation (Step 10) |
| Telegram not replying, no log activity | Pending updates flood (Step 10, FIX 1) |
