---
name: openclaw-channel-a2a-debug
description: Debug OpenClaw Telegram channel config and A2A bridge status on arifOS VPS
trigger: When OpenClaw Telegram polling is not working, duplicate bot token error, or A2A routing needs verification
category: devops
---

# OpenClaw Channel + A2A Bridge Debug

## Gateway Health Check
```bash
curl -s http://localhost:18789/health
openclaw channels status --probe 2>/dev/null | head -20
```

## Channel Config Inspection
```bash
# Read current Telegram channel config
openclaw config get channels.telegram 2>/dev/null

# Check if accounts sub-key is configured
openclaw config get channels.telegram.accounts 2>/dev/null

# List all agents
openclaw agents list 2>/dev/null

# Check agent defaults
openclaw config get agents.defaults 2>/dev/null | head -40
```

## Bot Token Sources
```bash
# Find where bot tokens are stored
grep -r "TELEGRAM_BOT_TOKEN" /root/.openclaw/ /root/.env /root/.hermes/.env 2>/dev/null

# Read OpenClaw env file
cat ~/.openclaw/env.local 2>/dev/null

# Read Hermes env file
cat ~/.hermes/.env 2>/dev/null | grep TELEGRAM
```

## Known Token Mappings (2026-05-07)
| Bot | Token | Status |
|-----|-------|--------|
| `@AGI_ASI_bot` | `8149595687:AAGycp7nzl1-D8mzZKOkUJWiWxg3Ok-wy70` | Active ✅ |
| `@ASI_arifos_bot` | `8410138119:AAHrXysyxI8yuBM7QW6QTafKsgpqEyd19DA` | No own token ❌ |

## A2A Bridge Status
```bash
# Check live A2A processes
ps aux | grep -E "a2a|hermes-a2a|openclaw-a2a" | grep -v grep

# Find A2A adapter scripts
ls /opt/arifOS/a2a-adapters/ 2>/dev/null

# Hermes A2A bridge
cat /opt/arifOS/a2a-adapters/hermes-a2a.py | head -80

# OpenClaw A2A bridge
cat /opt/arifOS/a2a-adapters/openclaw-a2a.py | head -80
```

## Key Ports
- OpenClaw gateway: `localhost:18789`
- Hermes A2A adapter: `18001`
- OpenClaw A2A adapter: `18002`

## Duplicate Token Fix
When second bot shows `Duplicate Telegram bot token` error — it means the `channels.telegram.accounts` entry is using the same token as `channels.telegram.botToken`. Fix:

```bash
# 1. Add new token to env
echo 'TELEGRAM_BOT_TOKEN_ASI=NEW_TOKEN_HERE' >> ~/.openclaw/env.local

# 2. Set the account config
openclaw config set channels.telegram.accounts.'1003890512851'.botToken \
  '{"source":"env","provider":"default","id":"TELEGRAM_BOT_TOKEN_ASI"}'

# 3. Restart
systemctl restart openclaw-gateway

# 4. Verify
openclaw channels status --probe 2>/dev/null | grep -E "connected|stopped|error"
```

## Gateway Restart
```bash
systemctl restart openclaw-gateway
sleep 3
curl -s http://localhost:18789/health
```

## Known Findings (2026-05-07)
- Gateway live at `{"ok":true,"status":"live"}`
- `channels.telegram.accounts` is empty — second bot not configured
- Hermes A2A bridge running at port 18001, calls `hermes chat -q --provider minimax`
- OpenClaw A2A bridge running at port 18002, calls `openclaw agent --message ...`
- Both bridges are live Python HTTP servers (not systemd services)
- A2A backbone wired but routing between them untested
- MiniMax key returning 2049 (invalid api key) — replacement needed
