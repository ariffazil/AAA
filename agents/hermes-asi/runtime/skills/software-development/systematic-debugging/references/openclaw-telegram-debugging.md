# OpenClaw Telegram Debugging Reference

**Loaded by:** `systematic-debugging` skill when OpenClaw Telegram issues arise
**Type:** Troubleshooting reference

---

## Common OpenClaw Telegram Failure Modes

### 1. Bot Not Responding to @mentions in Group

**Symptoms:** Bot alive (health check passes) but silent when @mentioned in group.

**Diagnostic path:**
```bash
# 1. Check OpenClaw received the message
tail -50 /tmp/openclaw/openclaw-*.log | grep -iE "chat_id.*-1003753855708|no-mention|mention"

# 2. Check Caddy proxy for webhook path
journalctl -u caddy --no-pager -n 20 | grep -iE "webhook|telegram|502"

# 3. Check Telegram webhook registration
BOT_TOKEN=$(SOPSAGE=age1l9rr62kg0x9mpdfmuacgqdqh2l97exchwnr2rflnq0hm5r6y85hq3e85va \
  sops -d /root/.openclaw/.env | grep TELEGRAM_BOT_TOKEN | cut -d= -f2 | tr -d ' ')
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -m json.tool
```

**Root causes (in order of likelihood):**
1. Caddy path rewrite broken — Telegram sends `/webhook/telegram`, OpenClaw expects `/telegram-webhook`
2. Cloudflare DNS proxied — Telegram can't reach webhook URL
3. Bot token wrong — messages routed to wrong bot
4. `require_mention: true` in config — needs @mention (expected behavior)

---

### 2. OpenClaw Gateway Restart Loop

**Symptom:** `systemctl status` shows active but continuously restarting.

**Root cause:** Orphan process holding port 18789.

**Fix:**
```bash
# Stop orphan
openclaw gateway stop
pkill -f openclaw  # guarantee kill

# Reset systemd
systemctl reset-failed openclaw-gateway.service

# Start fresh
systemctl start openclaw-gateway.service
systemctl enable openclaw-gateway.service

# Verify
ss -tulpn | grep 18789  # should show LISTEN
```

---

### 3. Telegram 409 Conflict

**Symptom:** `getUpdates` returns 409 Conflict.

**This is expected when webhook is active** — Telegram is delivering updates to the webhook, not accepting polling. Not a bug. The webhook is working.

---

### 4. pending_update_count > 0 After Webhook Fix

**Symptom:** `getWebhookInfo` shows `pending_update_count: N` (N > 0) even after you fixed the webhook URL.

**Cause:** Telegram cached the last error. You fixed the issue but Telegram hasn't re-delivered yet, OR there's a mismatch where Telegram is delivering to the old URL.

**Fix:**
```bash
BOT_TOKEN=$(SOPSAGE=... | grep TELEGRAM_BOT_TOKEN | cut -d= -f2 | tr -d ' ')
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/deleteWebhook?drop_pending_updates=true"
# Then re-register
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=https://openclaw.arif-fazil.com/webhook/telegram&secret_token=<SECRET>&drop_pending_updates=true"
```

---

### 5. OpenClaw CLI Commands Cause Gateway Restart

**Symptom:** Running `openclaw plugins list` or similar CLI commands triggers a gateway restart.

**Root cause:** Some `openclaw` CLI commands trigger gateway restart as a side effect.

**Fix:** Use single health probe instead of CLI cascade:
```bash
# Single probe — does NOT restart gateway
curl -s http://127.0.0.1:18789/health

# vs multiple CLI commands — triggers restart cascade
openclaw doctor  # ❌ runs several commands
openclaw plugins list  # ❌ triggers gateway restart
```

---

### 6. Gateway Port 18789 Not Listening After Restart

**Symptom:** `ss -tulpn | grep 18789` shows nothing, gateway not binding.

**Root cause:** Orphan process was not killed by `openclaw gateway stop`.

**Fix:** Manual kill required:
```bash
pkill -f "openclaw|gateway" 2>/dev/null || true
sleep 2
ss -tulpn | grep 18789  # should be clear now
systemctl start openclaw-gateway.service
```

---

## OpenClaw Log Interpretation

Key log patterns to watch:
```
[default] starting provider (@AGI_ASI_bot)  → Bot connecting
webhook local listener on http://127.0.0.1:8787/telegram-webhook  → Webhook listening
webhook advertised to telegram on https://...  → Telegram notified of webhook URL
no-mention  → Message received but no @mention, bot ignoring (expected behavior)
```

---

## Critical: Test Via External URL, Not Internal Port

```bash
# WRONG — gives false positive
curl -X POST http://127.0.0.1:8787/telegram-webhook -d '{}'  # HTTP 200 but doesn't prove Caddy→OpenClaw works

# CORRECT — tests full chain
curl -sv -X POST \
  -H "Content-Type: application/json" \
  -H "X-Telegram-Bot-Api-Secret-Token: <SECRET>" \
  https://openclaw.arif-fazil.com/webhook/telegram \
  -d '{"update_id":99999,"message":{"message_id":99999,"chat":{"id":-1003753855708,"type":"supergroup"},"text":"test"}}'
```

---

## Caddyfile Webhook Route (Correct)

```
handle /webhook/telegram* {
    reverse_proxy /telegram-webhook 127.0.0.1:8787 {
        header_up X-Telegram-Bot-Api-Secret-Token "SECRET"
    }
}
```

The `/telegram-webhook` in the reverse_proxy target rewrites the destination path. Without this, OpenClaw receives `/webhook/telegram` instead of `/telegram-webhook` and silently drops the request.