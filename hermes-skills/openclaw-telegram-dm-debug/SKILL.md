---
name: openclaw-telegram-dm-debug
category: devops
description: Debug and fix OpenClaw Telegram DM failures after bot token rotation — systemd restart loop is the usual culprit
---

# openclaw-telegram-dm-debug

## When to Use
OpenClaw Telegram DM is not responding to direct messages, or Telegram doesn't appear in `channels list` output despite being configured.

## Symptoms
- `openclaw channels list` shows no Telegram, or `status` shows Channels table with Telegram missing
- `systemctl status openclaw-gateway` shows `failed` or restart loop (exit code 78)
- DM to `@AGI_ASI_bot` gets no response
- Token is confirmed valid (seen in `journalctl -u openclaw-gateway` as `OK: Telegram token valid`)

## Root Cause Pattern
Token rotation (via BotFather) leaves the token in `/etc/systemd/system/openclaw-gateway.service.d/env.conf` but the OpenClaw gateway process is not actually running the updated config. Common scenario: gateway was running when token was rotated, old PID persists and blocks new service start.

## Diagnostic Sequence

```bash
# 1. Check if service is running
systemctl status openclaw-gateway

# 2. Check for stale PID blocking startup
journalctl -u openclaw-gateway --no-pager -n 20

# 3. Check if token is in env.conf (it should be there)
cat /etc/systemd/system/openclaw-gateway.service.d/env.conf | grep TELEGRAM

# 4. Confirm token is valid (shows "OK: Telegram token valid")
journalctl -u openclaw-gateway --no-pager -n 5 | grep token
```

## Fix Sequence

```bash
# 1. Kill any stale openclaw gateway processes
pkill -f "openclaw.*gateway" || true
sleep 2

# 2. Restart the systemd service cleanly
systemctl restart openclaw-gateway
sleep 6

# 3. Verify service is active
systemctl status openclaw-gateway --no-pager -n 10

# 4. Verify Telegram channel is detected
openclaw channels list

# 5. Test DM — send any message to @AGI_ASI_bot
```

## Key Insight
The token is almost always already configured in `env.conf`. The problem is the **service restart loop**. Do NOT re-add the channel or re-configure the token — just fix the service lifecycle. Exit code 78 = "gateway already running, refusing to start duplicate."

## Verification
- Service shows: `Active: active (running)`
- `channels list` shows Telegram configured
- DM to `@AGI_ASI_bot` returns a response (even "Hey Arif. What's on your mind?" = success)
