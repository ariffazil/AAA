# New Telegram Group Onboarding — Production Checklist

> Source session: `20260829_121902_8e7914` (Syed Sado Agent Client)
> Created: 2026-08-29

## Background

When adding a new Telegram group where the bot must auto-reply (monetization, client-facing, production), the full checklist MUST be completed before declaring "done." Arif's frustration (verbatim): "Test no reply at all from the hermes agent. omg whyvtak so long to make sure new telegram grou and user can be updated. if this go monetization, fail weiiiii."

## The Checklist (5 gates, all required)

### Gate 1: Bot is member of the group
```bash
source /root/.secrets/kunci-mas.env
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChat?chat_id=<CHAT_ID>" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['title'])"
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChatMember?chat_id=<CHAT_ID>&user_id=8410138119" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['status'])"
# Expected: title visible, status = 'administrator' or 'member'
```

### Gate 2: Chat_id in BOTH allowlists
```bash
# allowed_chats (inbound permission)
hermes config get telegram.allowed_chats | grep -c '<CHAT_ID>'
# free_response_chats (auto-reply mode)
hermes config get telegram.free_response_chats | grep -c '<CHAT_ID>'
# Both must return 1. If 0 = THE ROOT CAUSE of silent non-delivery.
```

**If missing:** `hermes config set telegram.allowed_chats '["id1","id2",...,"NEW_CHAT_ID"]'` — rebuild the FULL list. Then fix the YAML format:
```python
# After hermes config set (which writes JSON string), fix to YAML list
python3 -c "
import re, json, sys
path = '/root/.hermes/config.yaml'
with open(path) as f: c = f.read()
arr = json.loads(re.search(r\"allowed_chats: '(\[.*?\])'\", c).group(1))
lines = '\n'.join(['    - \\'' + x + '\\'' for x in arr])
c = re.sub(r\"allowed_chats: '\[.*?\]'\", 'allowed_chats:\n' + lines, c, count=1)
# Repeat for free_response_chats
with open(path,'w') as f: f.write(c)
"
```

### Gate 3: Gateway restart (picks up new config)
```bash
# From OUTSIDE the gateway session (subagent, cron, or separate terminal)
systemctl restart hermes-asi-gateway
sleep 8
journalctl -u hermes-asi-gateway --since "30 seconds ago" --no-pager | grep -i "Connecting to Telegram"
# Expected: "Connecting to Telegram (attempt 1/8)…"
```

### Gate 4: Real user sends text from Telegram app
- NOT curl simulation (proves pipeline but not full round-trip)
- NOT /new@ASI_arifos_bot (that's inline query syntax, not a group command)
- Just: type a normal text message in the group from Arif's phone
- Watch journal for inbound processing

### Gate 5: Agent reply appears in group
```bash
# If no reply in 30s, check:
journalctl -u hermes-asi-gateway --since "1 minute ago" --no-pager | grep -iE "TTS|timeout|Blocked|Forbidden"
# Common failures:
# - "Forbidden: the bot can't send messages to the bot" = reply going to bot's own ID, not group
# - TTS timeout 120s = voice pipeline hanging, kills text reply too
# - "Blocked unauthorized user" = user/chat not in allowlist
```

## Two groups, same bot — privacy model

When bot is in multiple groups (e.g. private SADO room + public client group):

| Group | Config | Behavior |
|-------|--------|----------|
| Private (Arif+Syed only) | `allowed_chats` ✓, `free_response_chats` ✓ | Auto-reply but nobody's watching so it's fine |
| Public (clients) | `allowed_chats` ✓, `free_response_chats` ✓ | Auto-reply = monetization surface |
| Private emotional room | `allowed_chats` ✓, `free_response_chats` — ✓ but `require_mention: true` | Reply ONLY when @mention'd |

**Arif's preference**: Private bromance room should be auto-silent. The agent exists there but stays quiet unless directly addressed.

## Known failure patterns

| Symptom | Root Cause | Fix |
|---------|------------|-----|
| Zero inbound traffic in journal for a group | chat_id missing from `allowed_chats` | Add chat_id to both lists + restart |
| Agent processes but no outbound reply | TTS pipeline timeout (120s) kills turn | Text-only mode or fix TTS |
| "Forbidden: can't send messages to bot" | Reply routing to bot's own chat_id (8410138119) | Check lane routing / session target |
| `/new@bot` doesn't trigger anything | That's inline query syntax, not a group command | Tell user to just type text or @mention |

## Evidence transcript

Session `20260829_121902_8e7914`:
- Added `-1003747272167` to both `allowed_chats` and `free_response_chats`
- Verified on disk as proper YAML list format (not JSON string)
- Gateway restarted via subagent (3162217)
- Agent processed test message, attempted outbound reply (hit "forbidden bot-to-bot" on test)
- Live message posted via Bot API (msg_id 8) confirmed bot is admin and can post
- Remaining: real user round-trip verification (Arif posts from phone)
