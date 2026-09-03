---
name: federation-runtime-audit
description: "Audit the arifOS federation runtime — validate architecture claims against live state."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [arifOS, federation, multi-agent, architecture, audit, runtime, docker, MCP]
    related_skills: [systematic-debugging, spike]
prerequisites:
  commands: [docker, curl]
---

# Federation Runtime Audit

Audit the arifOS federation (OpenClaw, Hermes, arifOS MCP, WEALTH, GEOX, WELL, AAA) against claimed architecture. Validate what's actually running vs. what the diagram says.

## When to Use

- User asks to "validate", "verify", or "check" an architecture claim
- User asks "is X actually running" or "does Y actually connect to Z"
- User wants a runtime health check of the federation
- User shares an architecture diagram and asks if it's accurate
- Routine heartbeat / health monitoring of the agent landscape

## Core Audit Loop

```
1. Map LIVE processes    → docker ps, ps aux
2. Map LIVE endpoints   → curl health, check ports
3. Read configs         → openclaw.json, gateway settings, MCP config
4. Trace DATA FLOW       → how does message X reach service Y
5. Compare CLAIM vs REAL → what the diagram says vs what runs
```

## Phase 1: Map Live Processes

```bash
# Docker containers — what's actually running
docker ps --format "{{.Names}}\t{{.Image}}\t{{.Status}}"

# Host processes — agents, adapters, gateways
ps aux | grep -E "openclaw|hermes|telegram|bot|a2a" -i | grep -v grep
```

Key services to identify:
- `openclaw` — main Telegram bot gateway (port 18789/18790)
- `hermes-a2a.py` — Hermes A2A adapter / Telegram poller (port 18001)
- `openclaw-a2a.py` — OpenClaw A2A adapter (port 18002)
- `arifosmcp` — arifOS MCP container (port 8080)
- `wealth-organ`, `geox_eic`, `well` — federation nodes

## Phase 1b: Container Image Audit (Critical for `registry_truth`)

```bash
# Check all federation container images against latest git commits
docker ps --format "{{.Names}}\t{{.Image}}" | grep -v pause

# For arifOS specifically (most commonly stale):
git -C /root/arifOS log --oneline -1
docker inspect arifosmcp --format '{{.Config.Image}}'

# If container image tag ≠ latest commit → stale, rebuild:
cd /root/arifOS && make deploy-local

# Known stale container (2026-05-17):
# arifosmcp: ghcr.io/ariffazil/arifos:8dfc8b18 — stale, predates registry_truth field
```

**This catches the MOST COMMON cause of `arifos_mcp_registry=UNKNOWN` (stale container vs probe bug).**

---

## Phase 2: Map Live Endpoints

```bash
# arifOS MCP — confirmed live on port 8080
curl -s http://127.0.0.1:8080/health | python3 -m json.tool

# OpenClaw gateway health — direct HTTP (no token needed for /health)
curl -s http://127.0.0.1:18789/health

# OpenClaw gateway immortally restarted 12+ times? Check acpx config invalid values:
python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); acpx=d['plugins']['entries']['acpx']['config']; print(f'permissionMode: {acpx.get(\"permissionMode\")}'); print(f'nonInteractivePermissions: {acpx.get(\"nonInteractivePermissions\")}')"
# Valid: permissionMode="deny-all", nonInteractivePermissions="deny"
# INVALID (causes 12+ restarts): permissionMode="off", nonInteractivePermissions="auto-approve"
```

MCP endpoints to check:
| Service | URL |
|---------|-----|
| arifOS | http://127.0.0.1:8080/mcp |
| WEALTH | http://127.0.0.1:8082/mcp |
| GEOX | http://127.0.0.1:8081/mcp |
| WELL | http://127.0.0.1:8083/mcp |

## Phase 3: Read Key Configs

```bash
# OpenClaw config — MCP servers, gateway, hooks, models
cat /root/.openclaw/openclaw.json | python3 -m json.tool

# Hermes config
cat /root/.hermes/config.yaml

# arifOS docker-compose (for container bindings and env)
cat /root/arifOS/docker-compose.yml
```

Key sections in openclaw.json:
- `mcp.servers` — configured MCP endpoints
- `gateway` — port, auth mode
- `hooks` — path → agent mappings
- `agents.defaults` — primary model, fallbacks

## Phase 4: Trace Data Flow

For Telegram bots, trace the message path:

```bash
# Who owns which Telegram bot token?
cat /opt/arifOS/a2a-adapters/hermes-a2a.py | grep -E "TELEGRAM_TOKEN|TELEGRAM_API" | head -3
cat /opt/arifOS/a2a-adapters/openclaw-a2a.py | grep -E "PORT|send_to_openclaw" | head -5
```

**Critical check: Verify port 18790 (OpenClaw sidecar) is actually listening.**
hermes-a2a.py points to `OPENCLAW_GATEWAY = "http://127.0.0.1:18790"` — if nothing listens there, Hermes inference silently fails:

```bash
ss -tulpn | grep 18790  # Nothing listening = Hermes cannot do inference
```

**Also check: openclaw-a2a.py (port 18002) is deployed but not running.** Dead adapter — remove config or start it.

Typical flow patterns:
```
# Pattern 1: Bot → A2A Adapter → OpenClaw gateway → Model
Telegram DM → openclaw-a2a.py (18002) → openclaw gateway (18789) → MiniMax

# Pattern 2: Bot → Hermes Adapter → AAA Gateway → OpenClaw gateway → Model  
Telegram → hermes-a2a.py (18001) → AAA gateway (3001) → openclaw (18789)

# Pattern 3: MCP tools
OpenClaw → arifOS MCP (8080) → F1-F13 floors → Qdrant/Postgres
```

### Telegram Token Isolation (TREE777 SCAR)

**Before running the audit, load:** `skill: tree777-telegram-bot-token-isolation`

This check prevents the critical bug where two agents share the same Telegram bot token (CRITICAL severity). Run the scalpels audit BEFORE declaring federation healthy.

```bash
# TREE777 Scalpel — MUST PASS before audit continues
# Detect: openclaw token pattern
cat /root/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('OpenClaw botToken:', d['channels']['telegram']['botToken'])"

# Detect: hermes token pattern  
cat /root/.hermes/platforms/telegram/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('Hermes botToken:', d['botToken'])"

# Detect: A-FORGE notifier token
grep NOTIFIER_TELEGRAM /root/A-FORGE/infra/live/compose/docker-compose.yml

# Verify they are DIFFERENT
# OpenClaw: 8149595687:AAFwy70... (partial visible)
# Hermes: 8410138119:*** (partial visible)
# A-FORGE notifier: 8149595687:*** (shares with OpenClaw — safe, A-FORGE only sends)

# CRITICAL CHECK: OpenClaw token MUST ≠ Hermes token
# If same → STOP → 888_HOLD → report to Arif immediately
```

| Audit shows `arifos_mcp_registry=UNKNOWN` | **Stale container image (common) OR probe bug (rare)** | See "Stale Container Image" section below |

---

## Stale Container Image Diagnostic

**Symptom:** `registry_truth: {arifos_mcp: UNKNOWN}` while other organs show `VERIFIED` or `PASS`.

**Two root causes — diagnose in order:**

### Step 1: Check source vs container (do this FIRST)
```bash
# Source code — does the field exist?
grep -n "registry_truth" /root/arifOS/arifosmcp/runtime/rest_routes.py

# Running container — does it have the field?
docker exec arifosmcp grep -n "registry_truth" /app/arifosmcp/runtime/rest_routes.py

# If source has it but container doesn't → STALE IMAGE, rebuild
# If neither has it → probe bug, fix health.py
```

### Step 2: Container image audit checklist
```bash
# Compare container image to latest git commit
docker ps --format "{{.Names}}\t{{.Image}}"
git -C /root/arifOS log --oneline -1

# Known stale (2026-05-17): arifosmcp image 8dfc8b18 — rebuild
cd /root/arifOS && make deploy-local
```

**Rule:** `registry_truth=UNKNOWN` → check source → check container → rebuild container before touching probe code.

### Step 3: If rebuild doesn't fix it — probe bug
Then the `health.py` probe is calling MCP endpoint (`/mcp`) instead of HTTP `/health`. Fix `health.py:591-601` to call the HTTP endpoint.

---

## References

- **`references/openclaw-telegram-debugging.md`** — OpenClaw Telegram webhook debugging: path mismatch root cause (Caddy forwards `/webhook/telegram` but OpenClaw expects `/telegram-webhook`), Cloudflare DNS A record must be DNS-only not proxied, stale webhook error fix (delete + re-register), no-mention behavior in groups, critical rule: test via external URL not internal port. Born from 2026-05-17 session where OpenClaw silent-failed without any error visible from direct port probe.
- **`references/tree777-telegram-bot-token-isolation.md`** — TREE777 protocol: token isolation enforcement. OpenClaw and Hermes MUST have separate Telegram bot tokens. Verification scalpels, collision detection, enforcement in AAA JOINT SEAL. Severity CRITICAL — token collision causes cross-agent message routing confusion. Added 2026-05-17 after Arif caught potential shared token concern (confirmed separate — no collision).
- **`references/audit-2026-05-18-openclaw-hermes-contrast.md`** — Full audit report from 2026-05-18 session: OpenClaw vs Hermes architecture contrast, identity boundary fix (OpenClaw SOUL.md patched to prevent persona bleed), TREE777 SCALPEL implementation (scripts verified working), pre-commit hook installed. TREE777 now has: SCALPEL audit script (`/root/.hermes/scripts/telegram-token-isolation-check.sh` ✅), pre-commit hook (`/root/.hermes/scripts/pre-commit-telegram-token-check.sh` ✅), implementation status doc (`references/TREE777-implementation-status.md`). Audit result: OPENCLAW ≠ HERMES tokens confirmed, A-FORGE send-only sharing safe.

**Common claims to validate:**
| Claim | Check |
|-------|-------|
| "OpenClaw → Hermes for deliberation" | Are they separate bots? Check `hermes-a2a.py`, `openclaw-a2a.py` ports |
| "OpenClaw connects to arifOS MCP" | Check `openclaw.json` → `mcp.servers.arifos.url` |
| "arifOS MCP is live" | `curl http://127.0.0.1:8080/mcp` |
| "Constitutional floors run on every message" | MCP tools only called when invoked — routine chat bypasses F1-F13 |
| "Hermes coordinates Kimi/Claude" | Check active processes, hooks config |

## Output Format

Structure the audit as:

```
## Validation: [Claim Title]

✅ CONFIRMED / ❌ WRONG / ⚠️ MISLEADING / ⚠️ UNVERIFIED

Evidence:
- [command output or finding 1]
- [command output or finding 2]

## Verdict
[One paragraph summary of actual architecture]
```

## Critical Distinction to Always State

```
MCP tools are CONFIGURED but not necessarily INVOKED.
Routine Telegram messages → model inference only.
arifOS F1-F13 floors → only when MCP tools are called.
```

The gap to highlight: "Constitutional reasoning only fires if arifOS MCP tools are actually invoked. For routine chat, OpenClaw just does model inference."

## Tips

- `openclaw status` (CLI) gives gateway runtime state
- Docker container restart loops = check `docker ps -a` for exit codes
- arifOS MCP container restarting → check `docker logs arifosmcp --tail 50`
- Two bots on separate Telegram tokens = two independent agents, NOT hierarchical

## OpenClaw Gateway Immortality Protocol

**Skill class:** federation-runtime-audit — infrastructure hardening for openclaw

**Trigger:** User wants OpenClaw gateway to survive reboot, crash, and systemd failures autonomously.

### The Problem

OpenClaw gateway was:
- Running under systemd with `Restart=always` but in a **7-restart loop** due to orphan PID holding port 18789
- **NOT enabled** at boot (`systemctl is-enabled` = disabled)
- Lacking **WatchdogSec** (systemd alive ping)
- No independent health guardian

### Step-by-step Repair + Hardening

**PHASE A: Kill Orphan, Reset Systemd**

```bash
# 1. Stop orphan process cleanly
openclaw gateway stop

# 2. Verify port free
ss -tulpn | grep 18789  # expect: no output

# 3. Reset failed state
systemctl reset-failed openclaw-gateway.service

# 4. Start under systemd
systemctl start openclaw-gateway.service

# 5. Enable boot persistence
systemctl enable openclaw-gateway.service

# 6. Verify
systemctl is-enabled openclaw-gateway.service  # expect: enabled
systemctl status openclaw-gateway.service       # expect: active (running)
ss -tulpn | grep 18789                         # expect: LISTEN on 127.0.0.1:18789
```

**PHASE B: WatchdogSec (Critical Immortality Feature)**

Add to `[Service]` section:

```ini
WatchdogSec=60
```

This makes systemd ping every 60s. If OpenClaw freezes, systemd auto-restarts within ~70s. **Keep it simple** — this is the single most important immortality feature.

**PHASE C: Boot Persistence Verification**

```bash
systemctl is-enabled openclaw-gateway.service
loginctl show-user root | grep Linger
# Both must be yes/enabled
```

**PHASE D: Health Guardian (systemd timer, not cron)**

Create `/usr/local/bin/openclaw-health-guardian.sh`:
```bash
#!/bin/bash
set -euo pipefail
GATEWAY_PORT=18789
log() { echo "[$(date '+%Y-%m-%dT%H:%M:%S%z')] [guardian] $1"; }

if ! ss -tulpn | grep -q ":$GATEWAY_PORT "; then
    log "PORT $GATEWAY_PORT — DEAD — restarting"
    systemctl restart openclaw-gateway.service
fi

status=$(systemctl is-active openclaw-gateway.service)
[[ "$status" != "active" ]] && systemctl restart openclaw-gateway.service
log "SERVICE — $status"
```

Create timer + service:
```ini
# /etc/systemd/system/openclaw-health-guardian.timer
[Unit] Description=OpenClaw Health Guardian Timer (every 5 min)
[Timer] OnBootSec=30 OnUnitActiveSec=300 AccuracySec=1min
[Install] WantedBy=timers.target
```
```ini
# /etc/systemd/system/openclaw-health-guardian.service
[Unit] Description=OpenClaw Health Guardian Service After=openclaw-gateway.service
[Service] Type=oneshot ExecStart=/usr/local/bin/openclaw-health-guardian.sh
[Install] WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now openclaw-health-guardian.timer
systemctl status openclaw-health-guardian.timer
```

### Critical Pitfall: Systemd Security Hardening BREAKS Node.js

**What failed:**
```ini
ProtectSystem=strict
ProtectHome=read-only
ReadOnlyPaths=/
```
Causes `exit code 226/NAMESPACE` — Node.js cannot read its own modules under strict mode.

**What worked:**
- `WatchdogSec=60` ✅
- `Restart=always RestartSec=10` ✅
- `LimitNOFILE=65536` ✅
- Boot enable ✅
- Health guardian timer ✅

**Rule:** Node.js services need module write access. If hardening is required:
```ini
ProtectSystem=full   # not strict
ReadOnlyPaths=/boot /firmware /usr /opt /etc
WritablePaths=/root /var/log /tmp
```
But test thoroughly before deploying — `exit code 226` = namespace isolation blocking Node.js dynamic requires.

### OpenClaw Webhook Mode — Correct Architecture (2026-05-17)

OpenClaw DOES support webhook mode — it runs internally on `127.0.0.1:8787` at path `/telegram-webhook`. Telegram sends to `/webhook/telegram`. Caddy must rewrite the path.

**Key ports and paths:**
- OpenClaw gateway (WebSocket, web UI): `127.0.0.1:18789`
- OpenClaw webhook listener (Telegram inbound): `127.0.0.1:8787` at `/telegram-webhook`
- Caddy route: `https://openclaw.arif-fazil.com/webhook/telegram` → rewrites to `/telegram-webhook` → `127.0.0.1:8787`

**Critical pitfall — path mismatch:**
- Telegram calls `/webhook/telegram` (registered via `setWebhook`)
- OpenClaw listens on `/telegram-webhook` (NOT `/webhook/telegram`)
- Caddy MUST use path rewrite: `reverse_proxy /telegram-webhook 127.0.0.1:8787`
- Without rewrite: HTTP 200 from gateway (wrong path) but Telegram sees 404

**Webhook registration:**
```bash
BOT_TOKEN=$(SOPSAGE=age1l9rr62kg0x9mpdfmuacgqdqh2l97exchwnr2rflnq0hm5r6y85hq3e85va sops -d /root/.openclaw/.env | grep TELEGRAM_BOT_TOKEN | cut -d= -f2 | tr -d ' ')
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=https://openclaw.arif-fazil.com/webhook/telegram&secret_token=$(cat /root/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['channels']['telegram']['webhookSecret'])")&drop_pending_updates=true"
```

**Stale Telegram webhook error (last_error_date stays old after fix):**
- Telegram caches the last error even after the issue is fixed
- Fix: delete + re-register the webhook to force fresh validation
  ```bash
  curl -s "https://api.telegram.org/bot${BOT_TOKEN}/deleteWebhook?drop_pending_updates=true"
  curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=https://openclaw.arif-fazil.com/webhook/telegram&secret_token=<SECRET>&drop_pending_updates=true"
  ```
- Verify cleared: `pending_update_count` = 0 and `last_error_message` = empty

**Cloudflare DNS requirement:**
- `openclaw.arif-fazil.com` MUST resolve to VPS public IP (NOT Cloudflare proxy IPs)
- Create A record: `openclaw.arif-fazil.com` → VPS IP `72.62.71.199`
- Verify: `dig +short A openclaw.arif-fazil.com @1.1.1.1` should return VPS IP, not `104.x.x.x`

### Known Issue: Orphan Process Not Killed by `openclaw gateway stop`

The current `openclaw gateway stop` sometimes leaves orphaned processes. Workaround: run `openclaw gateway stop` twice, or manually `pkill -f openclaw` before starting.

### Verification Commands

```bash
# Service state
systemctl status openclaw-gateway.service
systemctl is-enabled openclaw-gateway.service

# Port binding
ss -tulpn | grep 18789

# Recent logs (check Telegram 409 resolved)
journalctl -u openclaw-gateway --no-pager -n 30

# Health guardian
systemctl status openclaw-health-guardian.timer
journalctl -u openclaw-health-guardian.service --no-pager -n 5

# Telegram polling health
journalctl -u openclaw-gateway --no-pager -n 50 | grep -E "(Telegram|409|polling)"
```

### Coordination Workflow (Verified 2026-05-18)

**Trigger:** User asks "is X alive", "why isn't X responding", or "check both agents"

This is the OPPOSITE of the cascade anti-pattern — single targeted probes, not CLI command chains.

```
Step 1: ps aux | grep <agent>   → confirm process exists (don't use CLI status command)
Step 2: curl <health_endpoint>  → confirm service responding
Step 3: ss -tlnp | grep <port> → confirm port binding
Step 4: Run TREE777 audit script (ALWAYS after config changes)
Step 5: Forge working state into relevant skill
```

**Working commands (2026-05-18 verified):**
```bash
# OpenClaw liveness (single probe — NOT openclaw status)
curl -s http://127.0.0.1:18789/health
ps aux | grep "openclaw/dist/index.js gateway" | grep -v grep

# Hermes liveness (A2A bridge — NOT CLI)
curl -s http://localhost:18001/.well-known/agent-card.json
ps aux | grep "hermes.*gateway" | grep -v grep

# AAA A2A gateway
curl -s http://localhost:3001/health

# TREE777 audit (MUST run after any Telegram config change)
bash /root/.hermes/scripts/telegram-token-isolation-check.sh
```

**Why this works:** Single health endpoint beats CLI cascade. CLI commands like `openclaw gateway status` trigger internal state queries that can cause restarts. Direct HTTP probes are non-invasive.

**Rule:** When user asks "is agent X alive" → ONE targeted health check + ONE process check. Run TREE777 audit only if config was touched.

### Success Criteria

- `systemctl status` shows `active (running)` with uptime > 10s
- Port 18789 owned by NEW systemd PID (not orphan)
- No 409 Conflict in Telegram logs
- `systemctl is-enabled` = enabled (survives reboot)
- `WatchdogSec=60` configured in service file

## References

- **`references/openclaw-webhook-architecture-2026-05-17.md`** — **CORRECTED** architecture: OpenClaw runs webhook listener on port 8787 at `/telegram-webhook`, Telegram sends to `/webhook/telegram`, Caddy path-rewrites between them. Cloudflare DNS A record must point to VPS IP (not proxied). Includes webhook registration commands and stale error clearing procedure.
- **`references/vault999-supabase-architecture-2026-05-19.md`** — VAULT999 three-layer architecture: JSONL files (12,342 entries), docker postgres `vault999` DB (8 sealed entries), Supabase cloud (JWT verification only). Docker postgres auth: socket user mismatch requires `docker exec postgres bash -c "psql 'postgresql://USER:PASS@localhost:5432/vault999?sslmode=disable' -c '...'"` pattern. Cross-agent patch validation: OpenClaw caught 3 bugs in Arif's WEALTH proposal, corrected patch applied and verified.
- **`references/agent-spatial-amnesia-fix-2026-05-17.md`** — Agent spatial amnesia diagnosis and fix: all agents kept trying to SSH into the VPS they were already running on. Fix: inject SPATIAL LAW into system prompts.
- **`references/openclaw-immortality-2026-05-17.md`** — OpenClaw gateway immortality protocol: orphan kill, systemd hardening, WatchdogSec, health guardian timer, and the critical pitfall of `ProtectSystem=strict` breaking Node.js with exit 226/NAMESPACE.
- **`references/image-analysis-local-file-handling-2026-05-17.md`** — Pattern for analyzing local image files via browser_vision: copy to webroot, navigate via HTTPS, then analyze. Also covers Telegram direct send fallback.
- **`references/scar-openclaw-diagnostic-cascade-2026-05-17.md`** — **SCAR DOCUMENT**: Hermes ran 6 OpenClaw CLI commands in 3 minutes to diagnose a liveness question, causing a gateway restart cascade and false "OpenClaw dead" declaration. Root cause: `openclaw plugins list` triggers gateway restart; CLI cached state showed stale "stopped" while gateway was live. Anti-pattern: multi-command diagnostic cascade for a single liveness check. Evidence chain and fix documented.
- **`references/anti-cascade-diagnostic-protocol.md`** — Entropy-first diagnostic protocol for federation runtime diagnosis. **Single probe rule**: one targeted health endpoint check beats a CLI command cascade. Born from the OpenClaw cascade incident.
- **`references/meyhem-search-api-research-2026-05-18.md`** — Research: Meyhem is NOT an MCP server package — it's a search API (api.rhdxm.com, no API key, blends Exa+Tavily). Already integrated in arifOS `reality_handlers.py` as fallback cascade: Brave → DDGS → Meyhem. No installation needed; lesson: verify what X is before proposing "install X for agent Y".
- **`references/federation-transient-vs-persistent-2026-05-17.md`** — Transient vs persistent failure classification for federation audit tools. Core rule: trust direct JSON-RPC probe over audit flag. Includes `arifos_mcp_registry=UNKNOWN` detection bug (P1), WELL tool federation format verification results (15/15 PASS), and the `well_444_gateway` alias separate failure note.
- **`references/openclaw-telegram-webhook-analysis-2026-05-17.md`** — OpenClaw Telegram webhook debugging: path mismatch root cause, Cloudflare DNS requirement, stale webhook fix, no-mention behavior in groups.
- **`references/tree777-telegram-bot-token-isolation.md`** — TREE777 protocol: token isolation enforcement. OpenClaw and Hermes MUST have separate Telegram bot tokens.
- **`references/ghcr-push-403-vps-fallback-2026-05-19.md`** — GHCR 403 diagnosis + VPS autonomous build/push fallback when GitHub Actions fails. Includes the `wealth-build-push.sh` script pattern.
- **`references/wealth-abstraction-enhancement-pending-2026-05-19.md`** — WEALTH MCP abstraction proposal: OpenClaw found 3 bugs in Hermes's original proposal, corrected patches ready for `energy_crisis_assess` and `wealth_evaluate_prospect`. Status: pending apply.
- **`references/openclaw-webhook-architecture-2026-05-17.md`** — Corrected architecture: OpenClaw webhook on port 8787 at `/telegram-webhook`, Caddy path-rewrites `/webhook/telegram`.
- **`references/openclaw-immortality-2026-05-17.md`** — OpenClaw immortality: orphan kill, systemd hardening, WatchdogSec, health guardian, ProtectSystem=strict pitfall.
- **`references/scar-openclaw-diagnostic-cascade-2026-05-17.md`** — SCAR: multi-command diagnostic cascade caused gateway restart cascade. Anti-pattern: single probe beats CLI cascade.
- **`references/openclaw-health-json-cron-stall.md`** — `openclaw health --json` spawns isolated subagent sessions that stall at model_call in cron environments. Fix: replace with `curl http://127.0.0.1:18789/health`. Load when investigating watchdog session stalls or 54+ stalled sessions accumulating in logs.
- **`references/openclaw-acpx-config-invalid-values-2026-05-19.md`** — OpenClaw acpx config invalid enum values causing 12-restart crash loop. Fix: permissionMode "off"→"deny-all", nonInteractivePermissions "auto-approve"→"deny". Born from 2026-05-19 session where OpenClaw gateway was in crash loop and Hermes diagnosed via log analysis + systemd journal.
- **`references/openclaw-a2a-endpoint-gap-2026-05-19.md`** — CRITICAL: OpenClaw gateway port 18789 does NOT implement A2A POST /tasks. It's WebSocket/HTTP gateway + HTML dashboard. Port 18795 agent-card endpoint returns 200 GET /agent-card but 501 for POST /tasks. True A2A between Hermes and OpenClaw requires either OpenClaw ACPX sub-agent hook registration, Hermes-a2a.py WebSocket client bridge to port 18789, or Telegram relay as fallback. Discovery: 2026-05-19, symptoms: A2A curl POST returns 404 from gateway, 501 from port 18795.
- **`references/hermes-openclaw-data-flow-2026-05-19.md`** — Federation agent data flow map (2026-05-19): Hermes (18001→3001), OpenClaw (18789, webhook 8787), APEX (3002). Key discovery: Hermes polls Telegram (@ASI_arifos_bot) and forwards to AAA gateway (3001); OpenClaw uses webhook mode on separate token. They communicate via Telegram relay, NOT direct A2A. Port 18790 doesn't exist. Port 18795 only serves GET /agent-card (200), POST /tasks (501).
- **`references/tree777-workflow-engine-design-2026-05-17.md`** — TREE777 workflow engine: verification AFTER execution, branch resolution heuristics, dry-run 888_HOLD behavior.
- **`references/tree777-workflow-engine-design-2026-05-17.md`** — TREE777 workflow engine design notes from Week 1 build: verification runs AFTER execution (correct), branch resolution uses fragile substring heuristics, dry-run 888_HOLD is correct governance behavior not a bug, datetime deprecation fix.