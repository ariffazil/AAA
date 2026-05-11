---
name: hermes-telegram-full-listen-config
description: Enable Hermes Agent full-listen mode in Telegram groups — not just @mentions or DM from allowed users
triggers:
  - hermes telegram group deaf
  - hermes bot not responding in group
  - full listen telegram hermes
  - configure hermes for group chat
---

# hermes-telegram-full-listen-config

Enable Hermes Agent to listen and reply to ALL messages in Telegram groups (not just @mentions or DM from allowed users).

## Investigation Chain

```bash
# 1. Check if Telegram is connected
cat ~/.hermes/gateway_state.json | python3 -m json.tool
# Look for: "state": "connected"

# 2. Check Telegram credentials
cat ~/.hermes/.env | grep TELEGRAM

# 3. Check current allowed users restriction
grep TELEGRAM_ALLOWED ~/.hermes/.env

# 4. List known chats (chat IDs)
cat ~/.hermes/channel_directory.json | python3 -m json.tool | grep '"id"'
```

## Files Involved

| File | Purpose |
|------|---------|
| `~/.hermes/.env` | Bot token + allowed users |
| `~/.hermes/config.yaml` | Platform config (channel_prompts) |
| `~/.hermes/gateway_state.json` | Runtime connection status |
| `~/.hermes/channel_directory.json` | Known chat IDs |

## The Fix — 3 Steps

### Step 1: BotFather — Disable Privacy Mode

In Telegram chat with @BotFather:
```
/setprivacy → Disable
```

This tells Telegram to forward ALL messages (not just @mentions) to the bot.

### Step 2: Update .env — Remove User Restriction

Two env vars control this. Both must be checked:

```bash
# TELEGRAM_ALLOWED_USERS — if set to a single user ID, Hermes drops ALL other messages
# Restrictive (current — only Arif's DM):
TELEGRAM_ALLOWED_USERS=267378578

# Full group listen — blank (opens DMs too!) or specific IDs:
TELEGRAM_ALLOWED_USERS=
# Safer: list explicit group IDs so DMs stay restricted:
TELEGRAM_ALLOWED_USERS=267378578,-1003815535761,-1003753855708

# TELEGRAM_GROUP_ALLOWED_USERS — independent group-level override
# If set to wildcard, groups are open EVEN when TELEGRAM_ALLOWED_USERS is restricted:
TELEGRAM_GROUP_ALLOWED_USERS=*
```

Group chat IDs in `channel_directory.json` start with `-100`.

**Risk:** Blank `TELEGRAM_ALLOWED_USERS` = any stranger can DM the bot. If you want groups fully open but DMs restricted to only you, keep `TELEGRAM_ALLOWED_USERS=267378578` and rely on `TELEGRAM_GROUP_ALLOWED_USERS=*` instead.

### Step 3: Restart Hermes Gateway

```bash
kill $(cat ~/.hermes/gateway.pid)
cd /root && nohup ~/.hermes/venv/bin/hermes gateway run &
sleep 5
cat ~/.hermes/gateway_state.json
```

## Key Finding

`TELEGRAM_ALLOWED_USERS` in `.env` acts as a hard filter — if set to a single user ID, Hermes silently drops messages from everyone else. This is separate from BotFather privacy mode.

## Additional Failure Mode — Telegram Connected, Still Silent

Hermes can show `telegram: connected` in `~/.hermes/gateway_state.json` and still fail to answer because the **main model provider auth is broken**.

Real case discovered:
- `~/.hermes/config.yaml` had `provider: kimi-coding` and `model: kimi-k2.6`
- the configured key returned `401 Invalid Authentication` when tested against Moonshot/Kimi API
- result: Telegram transport is healthy, but reply generation fails before output

Quick check:
```bash
python3 - <<'PY'
import os, yaml, requests
cfg = yaml.safe_load(open(os.path.expanduser('~/.hermes/config.yaml')))
api_key = cfg.get('model', {}).get('api_key')
r = requests.get(
    'https://api.moonshot.ai/v1/models',
    headers={'Authorization': f'Bearer {api_key}'},
    timeout=20,
)
print(r.status_code)
print(r.text[:300])
PY
```

Interpretation:
- `200` → Kimi/Moonshot auth is valid
- `401 Invalid Authentication` → Hermes is not silent because of Telegram; the Kimi key is bad

**Rule:** If Hermes is connected to Telegram but not replying, diagnose both:
1. transport/listener (`gateway_state.json`, privacy mode, allowlist)
2. model/provider auth (`config.yaml` provider + live API probe)

## Additional Failure Mode — Agent Routing `require_mention` in config.yaml

Even when the top-level `telegram:` block has no `require_mention`, individual **agent configs** inside `config.yaml` can have `platform_routing.telegram.require_mention: true`. This silently overrides group-wide settings for that agent's responses.

Check:
```bash
grep -n "require_mention" ~/.hermes/config.yaml
```

If you see hits under `platform_routing:` or agent-specific blocks, those are per-agent overrides. Change them to `false` if you want that agent to reply without mention.

Example location found:
```yaml
    platform_routing:
      telegram:
        enabled: true
        allowed_chat_ids: []
        require_mention: true   # <-- THIS BLOCKS NO-MENTION REPLIES FOR THIS AGENT
        respond_to_chat_id: true
```

## Verify BotFather Privacy Mode via API

Instead of trusting memory, query Telegram directly:

```bash
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe" | python3 -c "
import json,sys
d=json.load(sys.stdin)
r=d.get('result',{})
print('bot:', r.get('username'))
print('can_read_all_group_messages:', r.get('can_read_all_group_messages'))
print('can_join_groups:', r.get('can_join_groups'))
"
```

Expected for full listen:
- `can_read_all_group_messages: True`
- `can_join_groups: True`

If `can_read_all_group_messages` is `False`, go to @BotFather → `/setprivacy` → Disable.

## AAA Group Gotcha

AAA group chat ID is `-1003753855708`.
If `TELEGRAM_ALLOWED_USERS` does not include `-1003753855708`, Hermes will appear deaf in AAA even when Telegram is connected.

Example:
```bash
grep '^TELEGRAM_ALLOWED_USERS=' ~/.hermes/.env
# If AAA group missing, add it:
# TELEGRAM_ALLOWED_USERS=267378578,-1003815535761,-1003753855708
```

## Group Chat ID Reference (from channel_directory.json)

| Group | ID |
|-------|-----|
| Chatgpt | `-1003815535761` |
| arifOS | `-1003753855708` |
| WEALTH | `-1003921087042` |
| AGI | `-1003718232946` |
| 🅰❗️🅰 | `-1003521544074` |
| Kanak-kanak | `-1003768847825` |
| Grindr Stuff | `-1003932845760` |

## Risks

- Blank `TELEGRAM_ALLOWED_USERS` = any group Hermes is added to becomes interactive, AND any stranger can DM the bot. Use explicit group IDs if you want DMs restricted.
- `TELEGRAM_GROUP_ALLOWED_USERS=*` bypasses the user allowlist for groups only — safer if you want open groups but locked DMs.
- Cannot selectively enable per-group without additional config (use explicit `TELEGRAM_ALLOWED_USERS` with group IDs).
- Group members get Hermes responses visible to everyone.
- After fix, Hermes replies to ALL group messages — no per-user filtering.
