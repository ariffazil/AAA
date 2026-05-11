---
name: openclaw-telegram-token-refresh
description: Refresh a revoked or replaced Telegram bot token in OpenClaw gateway — read current value first, patch correctly via SecretRef/env.local, restart gateway, verify with getMe.
triggers: ["telegram token refresh", "openclaw telegram 401", "bot token revoked", "openclaw gateway restart telegram", "openclaw telegram connected disconnected"]
tags: [telegram, openclaw, bot-api, gateway, restart, secret-ref]
version: 2.0.0
---

# OpenClaw Telegram Token Refresh Skill

## Problem
Telegram bot returns 401 Unauthorized — token is revoked or replaced. New token obtained from @BotFather. Need to update OpenClaw and restart the gateway.

## Root Cause Discovery (2026-05-05)

The `openclaw.json` `botToken` field is NOT stored as a raw string when using SecretRef — it becomes a dict:
```json
"botToken": {
  "source": "env",
  "provider": "default",
  "id": "TELEGRAM_BOT_TOKEN"
}
```
This means naive JSON patching with `replace_all` on the old token string will **silently fail** — the old token is already stored as a SecretRef, not a raw value.

**The correct approach is the SecretRef pattern with env.local injection** (see Step 2 below).

Also: `channels status --probe` shows `disconnected` for ~30s after gateway restart before switching to `connected` — this is normal startup latency, not a failure.

## THE FULL TOKEN SOURCE MAP (CRITICAL — 3 override layers)

When the gateway starts, the `TELEGRAM_BOT_TOKEN` env var is read from **up to THREE sources**, in systemd precedence order (last wins):

```
1. /etc/systemd/system/openclaw-gateway.service    ← main service file
   Environment="TELEGRAM_BOT_TOKEN=..."
   
2. /etc/systemd/system/openclaw-gateway.service.d/env.conf  ← DROP-IN (overrides #1)
   [Service]
   Environment="TELEGRAM_BOT_TOKEN=..."
   
3. /etc/environment                                ← OS-level env (overrides #1 and #2)
   TELEGRAM_BOT_TOKEN="..."
```

**The ExecStartPre token check script** (`/usr/local/bin/openclaw-telegram-token-check.sh`) reads the env var directly from the environment — if ANY of the three sources has the wrong token, the check fails with HTTP 401 and the gateway never starts.

**ALWAYS update all three locations.** Missing one causes silent failure.

## Local vs VPS Config (CRITICAL — 2026-05-07 UPDATE)

Running `openclaw channels add --channel telegram --token ...` from your local machine **only updates your LOCAL config file** (`~/.openclaw/openclaw.json` on the machine where you run the command). The VPS gateway runs its own process with its **own copy** of the config.

- If the VPS gateway has `bind: loopback` (default), you CANNOT SSH in or restart the service remotely
- The local config update does NOT propagate to the VPS automatically
- **Without VPS SSH access**, the VPS gateway cannot be restarted and continues running with the old token in memory

**Workaround when VPS SSH is blocked:** Use Hermes `send_message` to send a DM to yourself. If it delivers, the local token is working. The VPS gateway remains on the old token — needs someone with VPS console access to restart.

**To push config to VPS:** Use `OPENCLAW_GATEWAY_URL=ws://VPS_IP:18789 openclaw channels add ...` — but this requires explicit auth credentials (`--token` + `--password` gatewayToken), and the VPS must have network access from your location (port 18789 not blocked/filtered).

## Steps

### 1. Read current config
```bash
cat /root/.openclaw/openclaw.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
token = d.get('channels', {}).get('telegram', {}).get('botToken', '')
print('botToken:', repr(token))
"
```
- If it returns `{'source': 'env', 'provider': 'default', 'id': 'TELEGRAM_BOT_TOKEN'}` → SecretRef already set, just update env.local
- If it returns a raw token string → replace with SecretRef

### 2. Write token to env.local AND set SecretRef

The gateway's systemd unit has `EnvironmentFiles=/root/.openclaw/env.local`. The env var MUST be written there — not just set in current shell session (which dies on disconnect).

```bash
# Write token to env.local using python (avoids shell history)
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
print('Written to env.local')
"
```

Then set the SecretRef in openclaw.json:
```bash
# CRITICAL: ALL THREE flags required — --ref-provider AND --ref-source AND --ref-id
openclaw config set channels.telegram.botToken \
  --ref-provider default \
  --ref-source env \
  --ref-id TELEGRAM_BOT_TOKEN

# Verify the config updated
cat ~/.openclaw/openclaw.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
token = d['channels']['telegram']['botToken']
print('Config now:', json.dumps(token, indent=2))
"
# Expected: {"source": "env", "provider": "default", "id": "TELEGRAM_BOT_TOKEN"}
```

### 3. Update ALL THREE token locations simultaneously

**IF you have VPS SSH access**, update all three locations:

```bash
# LOCATION 1: systemd main service file
# USE SUDO TEE — NOT sed. sed truncates long tokens (>~20 chars gets cut to "814959...y70")
sudo tee /etc/systemd/system/openclaw-gateway.service > /dev/null << EOF
[Unit]
Description=OpenClaw Gateway (Host-based)
Documentation=https://docs.openclaw.ai
After=network.target docker.service

[Service]
Type=simple
Restart=always
RestartSec=10
StartLimitInterval=60s
StartLimitBurst=3
User=root
WorkingDirectory=/root

# Environment
Environment="OLLAMA_API_KEY=ollama...red"
Environment="TELEGRAM_BOT_TOKEN=NEW_TOKEN_HERE"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="QDRANT_URL=http://172.19.0.5:6333"
Environment="REDIS_URL=redis://172.19.0.3:6379"
Environment="ARIFOS_MCP_URL=http://127.0.0.1:8080"
Environment="OPENCLAW_GATEWAY_PORT=18789"
Environment="NODE_OPTIONS=--max-old-space-size=1024"

ExecStartPre=/usr/local/bin/openclaw-telegram-token-check.sh
ExecStart=/usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway

TimeoutStopSec=30
KillSignal=SIGTERM

[Install]
WantedBy=multi-user.target
EOF

# LOCATION 2: systemd drop-in (overrides main service file)
sudo tee /etc/systemd/system/openclaw-gateway.service.d/env.conf > /dev/null << EOF
[Service]
Environment="MINIMAX_API_KEY=***"
Environment="KIMI_API_KEY=***"
Environment="TELEGRAM_BOT_TOKEN=NEW_TOKEN_HERE"
Environment="OPENCLAW_BROWSER_FLAGS=--no-sandbox --disable-setuid-sandbox --disable-gpu"
Environment="GITHUB_PERSONAL_ACCESS_TOKEN=***"
Environment="CLOUDFLARE_API_TOKEN=***"
Environment="HERMES_SESSION_KEY=agent:main:telegram:dm:267378578"
EOF

# LOCATION 3: OS-level /etc/environment (overrides both above)
sudo sed -i 's|^TELEGRAM_BOT_TOKEN=.*|TELEGRAM_BOT_TOKEN="NEW_TOKEN_HERE"|' /etc/environment
grep "TELEGRAM_BOT_TOKEN" /etc/environment  # verify
```

**IF you DON'T have VPS SSH access**, the gateway runs as a root system service with `bind: loopback` and cannot be reached remotely. Your `openclaw channels add` command only updates the LOCAL config file. The VPS gateway will continue running with the old token in memory until someone with console access restarts it.

Workaround: Use Hermes `send_message` to send a test DM from the local machine. If it delivers, the local config is working. The VPS gateway remains unaffected.

### 4. Reload systemd and reset any failed state (StartLimitBurst trap)

```bash
# If the service has been restarting too fast, systemd enters failed state
# and refuses to start even after fixes. Must reset first.
sudo systemctl reset-failed openclaw-gateway
sudo systemctl daemon-reload
```

### 5. Restart gateway

```bash
# NOT systemctl --user — this is a root system service
sudo systemctl restart openclaw-gateway
sleep 5

# Check if it started successfully
systemctl is-active openclaw-gateway
journalctl -xeu openclaw-gateway.service --no-pager -n 5 | grep -E "OK:|ERROR"
```

### 6. Verify token with Telegram API
curl -s "https://api.telegram.org/botNEW_TOKEN_HERE/getMe"
```

Expected: `{"ok":true,"result":{"id":1234567890,"is_bot":true,"username":"SOME_BOT","first_name":"AGI🦞",...}}`

**If 401**: Token was already revoked by BotFather or is wrong.
**If 404**: Malformed URL — check the token format is `BOTID:TOKEN`.

### 7. Verify channel is connected
```bash
openclaw channels status --probe 2>&1
# Wait ~30s if just restarted — shows "disconnected" initially then "connected"
# Expected: "... running, connected, mode:polling, bot:@SOME_BOT"
```

### 8. Check logs for sendChatAction errors
```bash
journalctl -xeu openclaw-gateway.service --no-pager -n 50 2>&1 | grep -i "sendChatAction failed"
# Empty = healthy. Non-empty = stale connection holding dead token.
```

## Token Format
Telegram bot tokens are `BOT_ID:TOKEN` — format: `1234567890:AAQwVrXyZ_...` (46 chars total).

## Key Insight: Bot Identity May Change
After token rotation, the bot **username and name may be different** from the previous bot. The old bot's group memberships do NOT transfer — you must re-add the new bot to Telegram groups.

Example:
- Old: `@AGI_ASI_bot` → revoked
- New: `@AAA_AGI_bot` → active, different identity

## Verification Checklist
- [ ] `getMe` returns `ok: true` with correct username
- [ ] `channels status --probe` shows `connected` (wait up to 30s after restart)
- [ ] `journalctl` shows NO `sendChatAction failed` errors
- [ ] `[telegram] [CHAT_ID] starting provider` appears in recent logs
- [ ] Bot responds to DMs in Telegram

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `curl getMe` → 401 | Token already revoked by BotFather | Get fresh token from @BotFather |
| `channels status` → `disconnected` after 60s | Gateway didn't restart cleanly | Kill orphan processes, restart via systemd |
| `sendChatAction failed` in logs | Stale gateway process holding old token | Kill old processes, `sudo systemctl restart` |
| `disconnected` then `connected` in ~30s | Normal startup latency | Wait, not a failure |
| `channels status` → `stopped` | Bot was manually stopped | `openclaw channels start telegram` |
| `systemctl restart` → "Start request repeated too quickly" | Hitting `StartLimitBurst=3` — systemd refuses to restart | `sudo systemctl reset-failed openclaw-gateway` BEFORE restart |
| Gateway restarts but ExecStartPre fails 401 | Token in systemd service file or env.conf drop-in is wrong | Check `grep TELEGRAM /etc/systemd/system/openclaw-gateway.service*` — all 3 locations must match |
| `sed` replaces token but gateway still fails | sed truncates long tokens (>~20 chars) to `814959...y70` | Use `sudo tee << EOF` instead of sed for the systemd service file |
| `journalctl` shows `OK: Telegram token valid` but gateway is `failed` | `/etc/environment` has wrong token — systemd drop-in or main service file is correct, but OS env var overrides | Check `grep TELEGRAM /etc/environment` — update there too |
| `systemctl --user restart` says "not found" | The gateway runs as a system service (root), not a user service | Use `sudo systemctl restart openclaw-gateway` |
| Cannot SSH to VPS on port 22 | VPS SSH blocked/filtered from your current network | Use `OPENCLAW_GATEWAY_URL=ws://VPS_IP:18789` approach with explicit auth flags |
| `OPENCLAW_GATEWAY_URL=...` times out / unreachable | VPS gateway has `bind: loopback` OR port 18789 is blocked by firewall | Gateway must be bound to LAN interface or exposed via Cloudflare Tunnel |
| `nc -z VPS_IP 22` → filtered/timeout | Port 22 blocked from your current location, not a VPS problem | Try alternate ports or ask VPS owner to check its firewall |
