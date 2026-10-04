# Telegram Silent Gateway Diagnostic Ladder (SADO group, Syed Kudin)

**Symptom**: Arif reports "Hermes agent tak reply dalam SADO group and personal DM Syed Kudin @rico". Bot is admin, webhook is active, no Telegram errors. Yet messages don't reach gateway.log.

**Captured 2026-08-05**: SADO group `-1003815535761`, user `1042200555` (Syed Kudin, `@rico_ricaldo_33`), gateway `hermes-asi-gateway.service` on `:8444`. 12 hours of zero inbound after Syed's last successful message at 01:24 MYT. Diagnostic ladder (run in this order, each step rules out one cause):

## Step 1 — Is the bot still admin in the group?
```bash
BOT_TOKEN=$(grep ASI_ARIFOS_BOT_TOKEN /root/.secrets/kunci-mas.env | head -1 | cut -d= -f2 | sed 's/^"//;s/"$//;s/export //' | tr -d "'")
BOT_ID=$(curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe" | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["id"])')
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getChatMember?chat_id=-1003815535761&user_id=${BOT_ID}" | python3 -m json.tool
```
Look for `"status": "administrator"` and any of the `can_*` permissions true. If `status: "left"` or `status: "kicked"` — bot was removed from group. Re-invite. **NOT THE 2026-08-05 cause** — bot was full admin with custom title "HERMES AGENT".

## Step 2 — Is the webhook alive and not erroring?
```bash
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -c "
import sys, json
d = json.load(sys.stdin)['result']
print('url:', d['url'])
print('pending_update_count:', d['pending_update_count'])
print('last_error_message:', d.get('last_error_message'))
print('ip_address:', d.get('ip_address'))
"
```
- `pending_update_count > 0` → Telegram delivered but couldn't reach gateway (Caddy/Tunnel down, gateway crashed).
- `last_error_message` present → Telegram tried to deliver and got 4xx/5xx back. Note the error.
- Both null/zero → Telegram thinks delivery succeeded. **2026-08-05: this state — webhook silent, no error, 0 pending**. Look at next steps.

## Step 3 — Test the webhook handler directly
```bash
ENV_SECRET=$(grep TELEGRAM_WEBHOOK_SECRET /root/.secrets/kunci-mas.env | head -1 | sed 's/.*=//;s/"//g;s/'\''//g')
NOW=$(date +%s)
curl -sv -X POST "http://127.0.0.1:8444/telegram/webhook" \
  -H "Content-Type: application/json" \
  -H "X-Telegram-Bot-Api-Secret-Token: $ENV_SECRET" \
  -d '{
    "update_id": 888888888,
    "message": {
      "message_id": 9999,
      "from": {"id": 1042200555, "is_bot": false, "first_name": "TEST"},
      "chat": {"id": -1003815535761, "title": "SADO", "type": "supergroup"},
      "date": '"$NOW"',
      "text": "test"
    }
  }'
```
- `200 OK` → webhook handler is alive and accepts the secret. **2026-08-05: 200 OK confirmed**.
- `403 Request did not include the secret token` → handler is alive but secret rotated. Check `kunci-mas.env` `TELEGRAM_WEBHOOK_SECRET` matches what Telegram was told (re-set via `setWebhook`).
- `404` → no handler at this path on the port. Check Caddy route for `/telegram/webhook`.

## Step 4 — Look at LIVE journald, NOT `gateway.log`
**This is the trap that ate the most time on 2026-08-05.** When a unit has `StandardOutput=journal` in its `[Service]` block, the `gateway.log` file captures output **only from the previous instance**. After a restart, `gateway.log` mtime freezes at the restart timestamp and no new entries appear — but the service is alive and processing. Verify:
```bash
# confirm journald is the live sink:
systemctl cat <unit> | grep -E "StandardOutput|StandardError"
# confirm gateway.log mtime matches the last process restart, not the current time:
stat -c '%Y %n %y' /root/.hermes/logs/gateway.log
# the right live tail:
journalctl -u hermes-asi-gateway.service -f --no-pager
# windowed query:
journalctl -u hermes-asi-gateway.service --since "10 min ago" | grep -iE "inbound|SADO|1003815535761|1042200555"
```
**2026-08-05 finding**: gateway.log mtime was 06:21 UTC (the restart moment), 8 minutes stale. Live journald showed the actual inbound chatter. This single trap is worth burning a section for — it's the difference between "gateway silently broken" and "gateway healthy, look at the right log".

## Step 5 — Check model quota (silent inbound, silent outbound)
When inbound arrives but outbound never lands, the gateway is accepting the webhook (200 to Telegram) but the agent call inside fails. **HTTP 429 from a token-plan provider = the message was processed, the response was attempted, every retry returned quota-exhausted.** No error reaches the user; the agent just goes quiet. Detection:
```bash
grep -E "RateLimitError|HTTP 429|quota has been exhausted" /root/.hermes/logs/errors.log | tail -10
journalctl -u hermes-asi-gateway.service --since "10 min ago" | grep -E "RateLimitError|HTTP 429"
```
**2026-08-05 finding**: 50+ RateLimitError lines per minute on `qwen-token-plan-standard` and `qwen-token-plan-team-owner` (model `qwen3.8-max`). When user messages arrived, gateway processed them, called the model, model said "no quota", retry ×3, eventually failed silently. **Fix surface**: rotate to a provider with available quota (MiMo, DeepSeek, MiniMax), top up Qwen plan, or fall back to a free-tier model in the FED cascade.

## Step 6 — Filter / allowlist drift
Even when config says `require_mention: false`, runtime filters may drop messages silently. Verify the allowlist is in **all three** locations (vault, flat.env, systemd drop-in) — `verify-sibling-ops-reports` Pitfalls covers the token-zoo, but the chat-allowlist version is the same pattern. The runtime allowlist (read from drop-in or flat.env at process start) may have been captured before the group was added to `free_response_chats`.

## Step 7 — Parallel sessions, parallel gateways
Each gateway has its own allowlist. If Arif's "the bot didn't reply" is about `@ASI_arifos_bot` but the message actually went to `@AGI_ASI_bot` (openclaw) or another gateway, the issue is per-gateway allowlist divergence, not the bot itself. `journalctl -u hermes-asi-gateway -u openclaw-gateway --since "1 hour ago" | grep "<user_id>"` to find which gateway saw the message, then diff that gateway's allowlist against the others. **2026-08-05**: not the cause, but the diagnostic structure is the right reflex — assume per-gateway first when "user X can't reach bot Y".

## The full ladder summary
| Step | Question | 2026-08-05 answer |
|---|---|---|
| 1 | Bot still admin? | ✅ Full admin, custom title "HERMES AGENT" |
| 2 | Webhook alive + no error? | ✅ 0 pending, no last_error_message |
| 3 | Handler accepts POST? | ✅ 200 OK with correct secret |
| 4 | gateway.log current? | ❌ **STALE — 8min frozen at restart**. Switch to journald |
| 5 | Model quota exhausted? | ❌ 50+ RateLimitError/min on qwen3.8-max |
| 6 | Allowlist drift? | ⚠️ Not the proximate cause, but always check |
| 7 | Cross-gateway confusion? | ⚠️ Not the proximate cause, but always check |

**Convergence**: Step 4 (log-file trap) + Step 5 (silent 429 on inbound) explain the symptom together. The "inbound was silent" perception was actually "we were looking at the wrong log". When we switched to journald, the inbound chatter was visible — it was the response-side 429 that was the actual problem.

## Reusable lessons
- **`StandardOutput=journal` + `gateway.log` = stale-by-default after any restart.** Always journalctl -f for live traces.
- **HTTP 429 from a quota plan = silent inbound-success but outbound-fail.** No user-facing error. Detect via the `errors.log` or journald grep.
- **"Bot didn't reply" is ambiguous** — it can mean (a) message never arrived, (b) message arrived but no response, (c) response sent but user didn't see it, (d) response sent to wrong chat. Always run the 7-step ladder.
- **Webhook handler 200 OK ≠ webhook handler processed.** The handler accepts the JSON, but downstream filters (allowlist, mention, session routing) may drop before logging. Live journald is the only witness; a quiet journald after a confirmed 200 means a downstream drop.
