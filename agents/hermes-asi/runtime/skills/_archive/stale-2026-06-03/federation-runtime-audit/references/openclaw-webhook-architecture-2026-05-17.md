# OpenClaw Telegram Webhook — Working Architecture (2026-05-17)

> **Supersedes:** `references/openclaw-telegram-webhook-analysis-2026-05-17.md` (contained wrong conclusion)

## What Was Wrong

The prior analysis concluded OpenClaw Telegram plugin was "polling-only." **This was incorrect.** The actual discovery:

- OpenClaw runs a webhook listener on `127.0.0.1:8787` at path `/telegram-webhook`
- Telegram sends to `/webhook/telegram` (registered via `setWebhook`)
- The path mismatch caused Telegram to see 404 even though OpenClaw was running correctly
- The fix is Caddy path rewrite, not Option B consolidation

## Final Working Architecture

| Component | Address | Path |
|-----------|---------|------|
| OpenClaw gateway | `127.0.0.1:18789` | / (WebSocket, web UI) |
| OpenClaw webhook listener | `127.0.0.1:8787` | `/telegram-webhook` |
| Telegram → Caddy | `https://openclaw.arif-fazil.com` | `/webhook/telegram` |
| Caddy rewrite | `/webhook/telegram*` | `/telegram-webhook` → `127.0.0.1:8787` |

## Caddyfile Block

```caddy
openclaw.arif-fazil.com {
    import tls_origin
    encode zstd gzip
    handle /webhook/telegram* {
        reverse_proxy /telegram-webhook 127.0.0.1:8787
    }
    handle {
        reverse_proxy 127.0.0.1:18789
    }
}
```

The path rewrite `/telegram-webhook` is the critical piece.

## Cloudflare DNS Requirement

`openclaw.arif-fazil.com` must be an **unproxied A record** pointing directly to the VPS IP:
- A record: `openclaw.arif-fazil.com` → `72.62.71.199`
- Proxy status: **DNS only** (grey cloud), not Proxied

If Cloudflare is proxying (orange cloud), it will SSL-terminate and Telegram's webhook verification will fail.

Verify: `dig +short A openclaw.arif-fazil.com @1.1.1.1` must return `72.62.71.199` (VPS IP), not Cloudflare proxy IPs (`104.x.x.x`, `172.x.x.x`).

## Webhook Registration Commands

```bash
# Get bot token from SOPS-encrypted .env
BOT_TOKEN=$(SOPSAGE=age1l9rr62kg0x9mpdfmuacgqdqh2l97exchwnr2rflnq0hm5r6y85hq3e85va \
  sops -d /root/.openclaw/.env | grep TELEGRAM_BOT_TOKEN | cut -d= -f2 | tr -d ' ')

# Get webhook secret from openclaw.json
WEBHOOK_SECRET=$(cat /root/.openclaw/openclaw.json | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(d['channels']['telegram']['webhookSecret'])")

# Delete old webhook + re-register (forces Telegram to re-validate)
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/deleteWebhook?drop_pending_updates=true"
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=https://openclaw.arif-fazil.com/webhook/telegram&secret_token=${WEBHOOK_SECRET}&drop_pending_updates=true"
```

## Stale Error Clearing

Telegram caches `last_error_message` even after fix. After applying the Caddyfile fix, force re-validation via delete + re-register above. Verify with:
```bash
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -c "
import json,sys
d=json.load(sys.stdin)
r=d['result']
print('pending:', r['pending_update_count'])
print('last_error:', r.get('last_error_message',''))
print('url:', r['url'])
"
```
Expected: `pending: 0`, `last_error: ` (empty).

## Root Cause of 409 Conflict (This Session)

Telegram 409 was **not** Hermes vs OpenClaw bot token collision. It was an **orphan PID** (944202) from a previous manual `openclaw gateway start` holding port 18789. Systemd tried to start a new instance → port conflict → restart loop. Fix: `systemctl reset-failed`, then `systemctl restart openclaw-gateway.service`. The orphan dies when the manual session ends.