# OpenClaw Telegram Webhook Path Mismatch — Root Cause Analysis

**Date:** 2026-05-17
**Type:** SCAR (Root Cause + Fix)
**Severity:** P1 — Telegram bot silent failure

---

## What Failed

OpenClaw configured in **webhook mode**. Telegram sends updates to `https://openclaw.arif-fazil.com/webhook/telegram`. Caddy proxies to `127.0.0.1:8787`.

**The problem:** Caddy's `reverse_proxy /telegram-webhook 127.0.0.1:8787` does NOT strip the request path. Caddy forwards the full path `/webhook/telegram` to port 8787.

OpenClaw's webhook listener on port 8787 expects the path `/telegram-webhook` (not `/webhook/telegram`).

Result:
- Caddy → OpenClaw: HTTP 200 (OpenClaw sees request but wrong path)
- Telegram: receives 200 but message never processed (no-mention filter bypassed?)
- pending_updates: stays > 0

**Why direct port test was misleading:**
```bash
# This returns HTTP 200 — but the path is wrong
curl -X POST http://127.0.0.1:8787/telegram-webhook -d '{}'  # ✅ 200

# Test with /webhook/telegram — also returns 200 (gateway fallback)
curl -X POST http://127.0.0.1:8787/webhook/telegram -d '{}'  # ✅ 200 (but wrong path)

# Caddy sends /webhook/telegram to port 8787 → OpenClaw sees wrong path → silent drop
```

---

## The Fix

Caddyfile route must strip the `/webhook/telegram` prefix before forwarding:

```
handle /webhook/telegram* {
    reverse_proxy /telegram-webhook 127.0.0.1:8787 {
        header_up X-Telegram-Bot-Api-Secret-Token "..."
    }
}
```

The `/telegram-webhook` in `reverse_proxy` target tells Caddy to rewrite the destination path to `/telegram-webhook` when forwarding.

---

## Diagnostic Lessons

### Rule: Test external URL, not internal port

Direct port test (curl to 127.0.0.1:8787) gives false positive because OpenClaw's gateway also listens on 8787 and returns 200 for any path.

**Correct diagnostic:**
```bash
# Test via external URL — this catches Caddy path rewrite issues
curl -sv -X POST \
  -H "Content-Type: application/json" \
  -H "X-Telegram-Bot-Api-Secret-Token: <SECRET>" \
  https://openclaw.arif-fazil.com/webhook/telegram \
  -d '{"update_id":99999,"message":{"message_id":99999,"chat":{"id":-1003753855708,"type":"supergroup"},"text":"test"}}'

# Then check OpenClaw logs for the update being received:
tail -20 /tmp/openclaw/openclaw-2026-05-17.log | grep -iE "update_id|chat_id|mention|no-mention"
```

### Rule: Check Caddy logs for proxy errors, not just HTTP status

Caddy returns 200 even when the upstream (OpenClaw) rejects the path. Check:
```bash
journalctl -u caddy --no-pager -n 20 | grep -iE "webhook|telegram|502"
```

### Rule: Telegram getUpdates conflict confirms webhook is active

```bash
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getUpdates"
# → {"ok":false,"error_code":409,"description":"Conflict: can't use getUpdates method while webhook is active"}
# This means webhook IS registered and Telegram is delivering to it ✅
```

---

## Cloudflare DNS Issue

`openclaw.arif-fazil.com` DNS A record was reverting to Cloudflare proxy IPs (`172.67.134.76` / `104.x.x.x`) instead of VPS IP (`72.62.71.199`).

**Fix:** Set Cloudflare DNS to:
- Type: A
- Name: openclaw
- Content: `72.62.71.199`
- Proxy status: **DNS only** (grey cloud, NOT orange/proxied)

Telegram requires the webhook URL to have a public IP (not CDN-proxied).

---

## Telegram Webhook Fresh Reset (When last_error is stale)

Telegram caches the last error even after you fix the underlying issue. Force fresh validation:

```bash
BOT_TOKEN=$(SOPSAGE=age1l9rr62kg0x9mpdfmuacgqdqh2l97exchwnr2rflnq0hm5r6y85hq3e85va \
  sops -d /root/.openclaw/.env | grep TELEGRAM_BOT_TOKEN | cut -d= -f2 | tr -d ' ')

# Step 1: Delete webhook (clears Telegram's cached state)
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/deleteWebhook?drop_pending_updates=true"

# Step 2: Re-register webhook
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=https://openclaw.arif-fazil.com/webhook/telegram&secret_token=$(cat /root/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['channels']['telegram']['webhookSecret'])")&drop_pending_updates=true"

# Step 3: Verify
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -m json.tool
# Expect: pending_update_count: 0, last_error: null
```

---

## OpenClaw Group Message Behavior

OpenClaw in group chat (AAA: -1003753855708):
- **@mention required** for bot to respond (standard Telegram bot behavior)
- Without @mention: bot stays silent (logged as `no-mention` in OpenClaw logs)
- DMs to @AGI_ASI_bot: always processed ✅

This means when Arif asks "@AGI_ASI_bot whereeee" in group — OpenClaw SHOULD respond directly. If it doesn't, check:
1. Caddy is proxying correctly (path rewrite working)
2. OpenClaw received the update (check logs for `chat_id:-1003753855708`)
3. Bot has mention requirement satisfied

---

## OpenClaw Identity Card (A2A)

When asked for identity, OpenClaw responds with its agent card via the A2A protocol:
- Endpoint: `/.well-known/agent-card.json` on `openclaw.arif-fazil.com`
- Caddy route: `/webhook/telegram` → port 8787; `/.well-known/agent-card.json` → port 18795

```bash
# Get OpenClaw's agent card
curl -s https://openclaw.arif-fazil.com/.well-known/agent-card.json | python3 -m json.tool
```

---

## Key Commands This Session

```bash
# Check OpenClaw webhook path is listening
ss -tulpn | grep 8787

# Test Caddy proxy end-to-end
curl -sv -X POST \
  -H "Content-Type: application/json" \
  -H "X-Telegram-Bot-Api-Secret-Token: <SECRET>" \
  https://openclaw.arif-fazil.com/webhook/telegram \
  -d '{}'

# Check OpenClaw received webhook
tail -30 /tmp/openclaw/openclaw-2026-05-17.log | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        print(d.get('time','')[-14:], str(d.get('1',''))[:200])
    except: pass
"

# Check Telegram webhook info
BOT_TOKEN=$(SOPSAGE=age1l9rr62kg0x9mpdfmuacgqdqh2l97exchwnr2rflnq0hm5r6y85hq3e85va \
  sops -d /root/.openclaw/.env | grep TELEGRAM_BOT_TOKEN | cut -d= -f2 | tr -d ' ')
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -m json.tool
```