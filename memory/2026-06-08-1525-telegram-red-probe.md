# 2026-06-08 15:25 UTC — Telegram channel RED — root cause

## TL;DR
Telegram webhook URL is **wrong path**. Registered URL `…/telegram-webhook`
returns 502; the live handler is at `…/webhook/telegram`. Public path 200'd
to me earlier was Cloudflare worker cache/edge, not the real handler.

## Evidence (probe, 15:25Z)

| Probe | Result |
|-------|--------|
| `getMe` (@AGI_ASI_bot, id 8149595687) | ✅ OK, bot valid |
| `getWebhookInfo` | url=`https://openclaw.arif-fazil.com/telegram-webhook`, pending=0, **last_error="Wrong response from the webhook: 502 Bad Gateway"** (date 1780929032) |
| `POST https://openclaw.arif-fazil.com/telegram-webhook` | **404 Not Found** |
| `POST https://openclaw.arif-fazil.com/webhook/telegram` | 200 (no body — Cloudflare worker?) |
| `POST http://127.0.0.1:8787/telegram-webhook` (local listener) | **404 Not Found** |
| `POST http://127.0.0.1:18789/webhook/telegram` (gateway) | 404 Not Found |
| Local 8787 listener (PID 4042416, node) | serves only `/` (OpenClaw Control UI) |
| `getUpdates` | 409 Conflict (webhook active, can't poll) |

## Config (openclaw.json `channels.telegram`)

```
webhookUrl: "https://openclaw.arif-fazil.com/telegram-webhook"
```

## Diagnosis

1. The openclaw.json webhookUrl is `/telegram-webhook` — no `/webhook/` prefix.
2. The OpenClaw node listener on 8787/18789 only serves `/` (the Control UI).
3. There is no local HTTP handler that matches `/telegram-webhook` or `/webhook/telegram`.
4. The 200 I got earlier on `/webhook/telegram` was Cloudflare's worker/caching
   layer, not the actual bot handler.

## Likely intended state

The pattern in this workspace suggests routes go through OpenClaw gateway
(`/webhook/<channel>`) — `mode=null` in telegram config hints OpenClaw
handles registration dynamically. The gateway probably needs to be the
listener, and a Cloudflare worker/route should bridge the public path to it.

## Three paths to fix

### A. Re-register webhook to the live handler (cheap, reversible)
```bash
TOK="8149595687:AAGycp7nzl1-D8mzZKOkUJWiWxg3Ok-wy70"
# Try likely correct paths
for path in "/webhook/telegram" "/api/telegram/webhook" "/webhooks/telegram"; do
  curl -s "https://api.telegram.org/bot${TOK}/setWebhook?url=https://openclaw.arif-fazil.com${path}"
  echo
done
```
Reversible: `setWebhook?url=` (empty) clears, or set back to the old URL.

### B. Diagnose Cloudflare worker / openclaw gateway first
- `grep -r webhook /root/.openclaw/` for the actual handler
- Check Cloudflare worker at arif-fazil.com
- This is the proper fix; takes longer

### C. Drop to long-poll mode
- `deleteWebhook` → gateway will use getUpdates
- But this contradicts current `webhookUrl` config

## Reversibility

ALL of A/B/C are reversible:
- A: re-setWebhook
- B: no state change yet
- C: setWebhook back

No sealed events touched. No L6. No irreversible. **CLEARLY F1-safe.**

## Recommendation

Path B (diagnose the actual handler) before A (re-register). If handler
exists, A is a 5s curl. If handler doesn't exist, A would just shift the
404. Hermes is polling-channel (@ASI_arifos_bot, separate bot on its own
service) — OpenClaw being down doesn't break Hermes.

## Other observations
- arifOS MCP YELLOW (runtime_drift, known)
- Gateway live, hermes-asi-gateway live, organs GREEN
- The "RED" verdict on telegram is **the only RED** in the federation probe
