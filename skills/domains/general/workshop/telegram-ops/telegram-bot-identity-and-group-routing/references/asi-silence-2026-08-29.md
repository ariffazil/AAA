# ASI_arifOS_bot Silent Reply — 2026-08-29 Incident Transcript

> **Real failure transcript.** When future sessions see "Arif reports bot silent" with similar journal signatures, this is the canonical prior. Skill section above = condensed playbook; this file = raw evidence + reproduction recipe.

## Symptom (Arif's words)

> "im arif. so whats the satus of ny hermes ASI on telegram? why no reply at all. please check . why? fix and zen all . make sure hermes is all zen."

Arif then sent: `/new`, `/restart`, "Mana", "Smart ka x?", "Now tell me apa agent boleh buat dalam group ni" — none received a visible reply.

## What was actually true

- Bot `@ASI_arifOS_bot` (id `8410138119`) was live
- Token valid (`getMe` returned `ok: True`)
- Federation organs healthy: A-FORGE :7072 ok, LiteLLM :4011 ok, FRAME :18085 observer running
- BUT `getWebhookInfo.pending_update_count = 71`
- AND journalctl showed 33 errors matching `handle\(\) takes 1 positional argument`

## Root cause (single line)

`metabolism-hook/handler.py:102` declared `def handle(event: dict)` but gateway dispatcher (`/usr/local/lib/hermes-agent/gateway/hooks.py:195`) calls `fn(event_type, context)` — two positional args.

## Three-layer cascade

1. **Hook crash every turn** — 33 exceptions in 6h. Each one ate ~50ms of event-loop time and dumped a traceback to console.
2. **Event loop slow** — agent turn that should take 2-5s stretched past 30s.
3. **PTB reply_target expired** — Telegram moved Arif's original DM out of context window; PTB's `reply_to_message_id` lookup failed. The retry path stripped `reply_to` and resent, but by then Arif had already sent the next message — so the reply landed on stale context or got overwritten in his chat.

## Evidence snippets

### Journalctl (the smoking gun)

```
Aug 29 14:57:19 forge [hooks] Error in handler for 'agent:start': handle() takes 1 positional argument but 2 were given
Aug 29 14:59:17 forge [hooks] Error in handler for 'agent:end': handle() takes 1 positional argument but 2 were given
Aug 29 15:01:29 forge [hooks] Error in handler for 'agent:start': handle() takes 1 positional argument but 2 were given
Aug 29 15:13:09 forge [hooks] Error in handler for 'agent:end': handle() takes 1 positional argument but 2 were given
Aug 29 16:04:39 forge [hooks] Error in handler for 'agent:start': handle() takes 1 positional argument but 2 were given
Aug 29 16:13:10 forge [hooks] Error in handler for 'agent:end': handle() takes 1 positional argument but 2 were given
```

### Reply target latency tell

```
Aug 29 16:05:59 [Telegram] Reply target deleted, retrying without reply_to: Message to be replied not found
Aug 29 16:07:05 [Telegram] Reply target deleted, retrying without reply_to
Aug 29 16:08:35 [Telegram] Reply target deleted, retrying without reply_to
Aug 29 16:09:19 [Telegram] Reply target deleted, retrying without reply_to
Aug 29 16:10:16 [Telegram] Reply target deleted, retrying without reply_to
Aug 29 16:12:00 [Telegram] Reply target deleted, retrying without reply_to
Aug 29 16:12:44 [Telegram] Reply target deleted, retrying without reply_to
```

7 retries in 7 minutes. Each retry strips `reply_to` and sends fresh — but the original slow cause (hooks) was still burning CPU.

### Telegram queue

```
getWebhookInfo: pending_update_count: 71
getUpdates (100 limit): 76 messages, 4 had empty text (Arif's interactive /new, /restart attempts)
```

### Correct hook signatures (other three hooks)

```
/root/.hermes/hooks/arifos-route/handler.py:78:      def handle(event_type: str, context: dict | None = None)
/root/.hermes/hooks/constitutional-guard/handler.py:48: async def handle(event_type: str, context: dict)
/root/.hermes/hooks/verify-enforce-hook/handler.py:69: async def handle(event_type: str, context: dict)
/root/.hermes/hooks/metabolism-hook/handler.py:102:  def handle(event: dict)         ← BUG
```

## Fix applied (2026-08-29 19:00 MYT)

Patch `/root/.hermes/hooks/metabolism-hook/handler.py` line 102 — accept both signatures:

```python
def handle(event_type=None, context=None, event=None) -> dict:
    if isinstance(event_type, dict):
        event = event_type
        event_type = event.get("event_type", event.get("type", "unknown"))
        context = event
    else:
        event_type = event_type or "unknown"
        context = context or {}
    session_id = context.get("session_id", f"session_{int(time.time())}")
    # ... (agent:start branch uses context, agent:end uses context.get('messages', ...))
```

Sequence: drain 76 pending → restart gateway → wait 5s → verify clean.

## Verification

After fix:
```
journalctl -u hermes-asi-gateway --since "1 min ago" | grep -E "ERROR|hooks|handle\(\)|Forbidden"
# (empty)
BOT: @ASI_arifOS_bot id=8410138119 ok=True
WEBHOOK: url=<polling> pending=0
GATEWAY PID 3340434 alive: True
```

## What NOT to do

- ❌ Don't restart gateway first, patch second. Pending updates pile up to 100+ in seconds during restart and Telegram throws some away.
- ❌ Don't blame Mapbox/Aforge MCP "parking" warnings. Those are parked but not on the Telegram path.
- ❌ Don't add retry logic to "Reply target deleted". The retry path already exists in `/usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py:1489`; the real fix is upstream latency.
- ❌ Don't regenerate bot token. Token was valid throughout.
- ❌ Don't change `free_response_chats` in config.yaml. `267378578` (Arif's DM) was already in the list.

## Diagnostic recipe (steal this)

```bash
# 1. Is bot alive?
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getMe" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['username'], r['id'])"

# 2. Pending updates?
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getWebhookInfo" \
  | python3 -c "import sys,json; print('pending:', json.load(sys.stdin)['result'].get('pending_update_count'))"

# 3. Hook signature drift?
journalctl -u hermes-asi-gateway --since "1h ago" | grep -c "handle() takes 1"

# 4. Audit all hook signatures at once:
for f in /root/.hermes/hooks/*/handler.py; do
  echo "=== $f ==="
  grep -E "^def handle\(|^async def handle\(" "$f"
done

# 5. Latency symptom count:
journalctl -u hermes-asi-gateway --since "1h ago" | grep -c "Reply target deleted"

# 6. Drain + restart + verify (the fix)
MAX=$(curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getUpdates?limit=100&timeout=0" \
  | python3 -c "import sys,json; updates=json.load(sys.stdin)['result']; print(max((u['update_id'] for u in updates), default=0))")
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getUpdates?offset=$((MAX+1))&timeout=0" >/dev/null
systemctl restart hermes-asi-gateway.service
sleep 5
journalctl -u hermes-asi-gateway --since "30 sec ago" | grep -E "ERROR|hooks" | head -5
# (empty = clean)
```

## Files touched

- `/root/.hermes/hooks/metabolism-hook/handler.py:102` — patch handle() signature
- `/root/forge_work/2026-08-29-hermes-asi-telegram-silence-diagnosis.md` — full evidence (21 lines of postmortem if needed)