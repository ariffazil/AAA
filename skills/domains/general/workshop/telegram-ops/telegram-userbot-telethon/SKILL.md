---
name: telegram-userbot-telethon
description: >
  Set up a Telethon userbot that runs as Arif's actual Telegram account —
  sees ALL DMs, groups, and channels. Distinct from bot API (which only sees
  chats the bot is added to). Use when: "manage all my telegram chats",
  "userbot", "telethon setup", "act as my account", "read all my messages",
  "telegram as me".
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [telegram, telethon, userbot, mtproto, relay]
    related_skills: [openclaw-channel-config, hermes-telegram-group-setup, telegram-group-relay]
---

# Telegram Userbot (Telethon)

Run a Telethon userbot that logs in as Arif's actual Telegram account via MTProto. Unlike the bot API (which only sees chats the bot is added to), a userbot sees EVERYTHING — all DMs, all groups, all channels.

## When to load

- User asks to "manage all my Telegram chats"
- User says "userbot", "telethon", "act as my account"
- User wants to read/respond to messages across ALL chats, not just bot-enabled ones
- User asks to set up message relay from their personal account

## Architecture: Bot vs Userbot

| | Bot API | Userbot (Telethon) |
|-|---------|-------------------|
| Identity | @ASI_arifos_bot | Arif's personal account |
| Sees | Only chats bot is added to | ALL chats (DMs, groups, channels) |
| Auth | Bot token from @BotFather | Phone number + one-time code |
| API | HTTP Bot API | MTProto (binary protocol) |
| Rate limits | 30 msg/sec to different chats | More generous |
| Group add | Must be invited | Already in all groups |

## Prerequisites

1. **Telethon installed**: `pip install telethon` (already on VPS as of 2026-07-11)
2. **API credentials** from https://my.telegram.org/apps (NOT my.telegram.org/app or my.telegram.org — see URL pitfall below)

## Step 1: Get API Credentials

**URL:** https://my.telegram.org/apps (must end in `/apps`)

1. Enter phone number with country code (e.g. `+601xxxx6789`)
2. Telegram sends a login code to the user's Telegram app
3. Enter the code
4. If no app exists: create one with Platform=Desktop, title/short name/description = anything
5. Record `api_id` (integer) and `api_hash` (32-char hex string)

**Store securely:** `/root/.secrets/vault.flat.env` or `/root/.hermes/.env`

## Step 2: Interactive Authentication

Telethon requires interactive auth ONCE. After that, the session file persists.

```python
from telethon import TelegramClient
import asyncio

API_ID = 37046798
API_HASH = '1bd06b1c4c9252c05a64512b066b8986'
SESSION_PATH = '/root/userbot/ari_session'  # or /root/.hermes/userbot.session

async def main():
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    await client.start()  # Prompts for phone + code interactively
    me = await client.get_me()
    print(f'Logged in as: {me.first_name} ({me.phone})')
    await client.disconnect()

asyncio.run(main())
```

**What happens:**
1. Script asks for phone number (or reads from env)
2. Telegram sends a code to the user's Telegram app
3. User enters the code
4. Telethon saves session to `/root/.hermes/userbot.session`
5. Future runs use the session file — no more codes needed

**UNBUILT — state on disk, verified 2026-09-19:** no session file exists on this host. `/root/.hermes/userbot.session`, `/root/userbot/`, and any `*.session` under `/root` are all absent, so no interactive auth has been completed here. The `/root/.hermes/userbot.session` literal below is the path Telethon *will* create on first successful `client.start()` — it does not resolve today, and every read/relay pattern below needs that auth run first.

## Step 3: Relay Script (Hermes Integration)

The userbot listens to all incoming messages and routes them through Hermes for processing.

```python
from telethon import TelegramClient, events
import asyncio
import os

API_ID = int(os.environ.get('TELETHON_API_ID', '37046798'))
API_HASH = os.environ.get('TELETHON_API_HASH', '')
SESSION = '/root/.hermes/userbot.session'

# Chats to monitor (empty = ALL)
MONITOR_CHATS = []  # or specific IDs: [-1003753855708, ...]
# Chats to auto-respond in (requires careful config)
AUTO_RESPOND_CHATS = []

client = TelegramClient(SESSION, API_ID, API_HASH)

@client.on(events.NewMessage(chats=MONITOR_CHATS or None))
async def handler(event):
    sender = await event.get_sender()
    chat = await event.get_chat()
    text = event.text

    # Log or route to Hermes
    print(f'[{chat.title or "DM"}] {sender.first_name}: {text}')

    # Auto-respond in specific chats if needed
    # if event.chat_id in AUTO_RESPOND_CHATS:
    #     await event.reply('response')

async def main():
    await client.start()
    me = await client.get_me()
    print(f'Userbot running as {me.first_name}')
    await client.run_until_disconnected()

asyncio.run(main())
```

## Step 4: Systemd Service

```ini
# /etc/systemd/system/telegram-userbot.service
[Unit]
Description=Telegram Userbot (Telethon)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root
EnvironmentFile=/root/.secrets/vault.flat.env
ExecStart=/usr/bin/python3 /root/.hermes/scripts/telegram-userbot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**UNBUILT — verified 2026-09-19.** The unit above is a spec, not something installed: `/etc/systemd/system/telegram-userbot.service` does not exist and neither does its `ExecStart` target `/root/.hermes/scripts/telegram-userbot.py` (nor any `userbot`-named file anywhere under `/root`). What would have to exist: the Step 3 relay listing saved verbatim to that exact path, and the session from Step 2 — then `systemctl enable --now telegram-userbot`. Until then this step cannot execute and should not be reported as a running service.

### Pitfall: phone_code_hash not persisted between auth steps (2026-07-11)

When splitting Telethon auth into two scripts (step 1: send code, step 2: verify), the first attempt will fail with `You also need to provide a phone_code_hash`. `send_code_request()` returns the hash — you MUST save it and pass it to `sign_in()`.

**Broken pattern (hash lost between calls):**
```python
# step1.py
sent = await client.send_code_request(PHONE)  # hash returned but not saved

# step2.py
await client.sign_in(PHONE, code)  # FAILS — no hash
```

**Working pattern (persist hash to JSON):**
```python
# step1.py
sent = await client.send_code_request(PHONE)
with open("auth_state.json", "w") as f:
    json.dump({"phone_code_hash": sent.phone_code_hash}, f)

# step2.py
with open("auth_state.json") as f:
    state = json.load(f)
await client.sign_in(PHONE, code, phone_code_hash=state["phone_code_hash"])
```

Or use `client.start()` which handles the hash internally (single interactive session only).

**For non-interactive environments** (e.g. Hermes agent running auth on behalf of user): use the two-step script in `references/two-step-auth.py`. Step 1 sends the code and saves the hash. Step 2 takes the code as argv and verifies.

## Pitfalls

### ⚠️ Pitfall: Telegram BLOCKS login codes shared in chat (2026-07-12)

**THE #1 BLOCKER.** Telegram's security system detects when a login code is shared in a Telegram message and **blocks the login attempt**. You'll get:

> "sign in was not allowed, because this code was previously shared by your account"

This means you **CANNOT** have the user send the code back in the same Telegram chat. Every attempt will fail. Even screenshots sent as text get OCR'd and blocked.

**Workarounds (in order of reliability):**
1. **SSH terminal** — user SSHs into the server and runs `python3 auth.py` directly, types code in terminal
2. **Web form** — run a tiny HTTP server on the VPS, user opens URL in browser (NOT Telegram browser), enters code there. See `templates/auth_web.py` in the `social-media/telegram-userbot` sister skill.
3. **Screenshot as photo** — user sends code as an IMAGE (not text). Telegram's scanner reads text, not images. Unverified but plausible.

**After auth, shut down the web server and close the firewall port.** Session file persists.

**Working template:** `templates/auth_web.py` — uses `.format()` (not f-strings) to avoid CSS brace conflicts. Run it, open URL in browser, enter code, done.

### Pitfall: CSS f-string conflict in Python HTTP servers (2026-07-12)

When building a web form with Python's f-strings, CSS braces `{}` conflict with f-string syntax. The server runs but crashes on every request with `KeyError: 'font-family'`.

**Broken:**
```python
html = f"<style>body{{font-family:system-ui}}</style>"  # KeyError on {
```

**Fix:** Use `str.replace()` or string concatenation for HTML with CSS. Or use `{{` and `}}` for literal braces in f-strings:
```python
html = f"<style>body{{font-family:system-ui}}</style>"  # This actually works
# But complex CSS with many braces is error-prone. Better: read HTML from a file.
```

### Pitfall: my.telegram.org URL confusion (2026-07-11)

The user may navigate to:
- `my.telegram.org` → shows app listing page (Home/FAQ/Apps links), NOT the create form
- `my.telegram.org/app` → shows app CONFIG page (if app already exists), with api_id/api_hash visible
- `my.telegram.org/apps` → shows CREATE new application form (correct URL for first-time setup)

If the user already has an app, `my.telegram.org/app` shows the credentials directly. If not, they need `my.telegram.org/apps` to create one first.

**The user may paste the apps LISTING page (telegram.org/apps — the page listing all official Telegram apps like Android, iOS, Desktop, TDLib, etc.) thinking it's my.telegram.org/apps.** Correct them: the URL is `my.telegram.org/apps` (note: no `telegram.org`, it's `my.telegram.org`).

### Pitfall: User asks to "read group X" — fall back to "no capability" too quickly (2026-08-19)

When a user (especially Arif) asks "can you read SADO group," the natural temptation is to claim "no live Telegram access" — but this is often WRONG. Before saying "no," check these in order:

1. **Check for archivally-set-up session**: `ls -la /root/_archive/*/userbot/*.session 2>/dev/null && ls -la /root/userbot/*.session 2>/dev/null && ls -la /root/.hermes/*.session 2>/dev/null`
2. **Check for archived auth files with API_ID/HASH**: `grep -r "API_ID = " /root/_archive/*/userbot/ 2>/dev/null`
3. **Check for live scripts/config**: `find /root -maxdepth 4 -name "*userbot*.py" -o -name "telegram-userbot.service" 2>/dev/null`

**Arif's case 2026-08-19:**
- Live signal: user asked "U can read from SADO group right" → "Lie"
- Reality discovered later: `/root/_archive/2026-08-04/userbot/ari_session.session` (143KB, modified 2026-07-30) + archived `auth.py` with hardcoded `API_ID=37046798`, `API_HASH="1bd06b1c4c9252c05a64512b066b8986"`, `PHONE="+601****0258"` + active `auth_state.json` with `phone_code_hash="cc616d530e88943cc1"`.
- Capability was sitting there all along. Saying "no" was both inaccurate and a missed capability surfacing.

**Correct protocol when user asks to read/observe group:**
1. **State.db check** — query historical messages from current session/last 24-48h.
2. **Archive session scan** — check `_archive/*/userbot/` for stale but possibly-still-valid Telethon sessions.
3. **Live token scan** — check `/root/.secrets/kunci-*.env` for current TELETHON_API_ID/HASH.
4. **Only after exhausting all three** claim "no live Telegram access" — and even then, name what was checked.

**Authorization floor (F2 TRUTH + F1 AMANAH):** Even when session+creds are archivally available, DO NOT connect without explicit Arif authorization. Telegram credentials authenticate as Arif's personal account — using them without authorization is identity impersonation. In the 2026-08-19 case, correctly stopped and surfaced the choice ("Go" / "Stop" / "Setup") instead of just connecting.

**Approximate working read pattern** (use ONLY after Arif authorizes — and only once a session file exists; none does today, see Step 2):

```python
import asyncio, os
from telethon import TelegramClient

API_ID = int(os.environ.get('TELETHON_API_ID'))  # from arkib or env
API_HASH = os.environ.get('TELETHON_API_HASH')
SESSION = '<live Telethon session file>'  # the 2026-08-04 archive was rotated away — do not point this at a dead path (verified 2026-09-19)

async def read_group(group_id, limit=30):
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        print('Session expired — need re-auth.')
        await client.disconnect()
        return
    entity = await client.get_entity(group_id)
    msgs = await client.get_messages(entity, limit=limit)
    for m in msgs:
        ts = m.date.strftime('%Y-%m-%d %H:%M:%S')
        sender = m.sender.first_name if m.sender else '?'
        print(f'[{ts}] {sender} ({m.sender_id}): {(m.text or "[media]")[:200]}')
    await client.disconnect()

asyncio.run(read_group(-1003815535761))  # SADO group
```

### Pitfall: Session file expires

Telethon sessions can expire if:
- Account is logged out from another device
- Telegram detects suspicious activity
- Two-factor auth is changed

When this happens, the userbot stops receiving messages. Fix: re-run interactive auth.

### Pitfall: Rate limits

Telegram rate-limits user accounts differently than bots:
- ~30 messages/second to different chats
- ~20 messages/minute to the same chat
- Exceeding = flood wait (seconds to hours)

Don't auto-respond to every message. Be selective.

### Pitfall: Privacy settings

Some Telegram users restrict who can see their messages. A userbot respects the TARGET's privacy settings, not the operator's. If a user has "nobody" for forwarding, the userbot may not see their messages in groups.

### Pitfall: Two-step verification

If Arif's account has 2FA enabled, Telethon will also prompt for the password during first auth. Store this securely.

## When NOT to use a userbot

- **Simple group management** → use bot API (simpler, no phone auth)
- **Responding in specific groups** → bot API + OpenClaw/Hermes config
- **Scheduled tasks** → Hermes cron jobs with bot API
- **Channel broadcasting** → bot API with channel admin rights

A userbot is for when you need to see and act on ALL chats as the human account itself.

## Related

- `openclaw-channel-config` — bot API Telegram config (the simpler path)
- `hermes-telegram-group-setup` — adding groups/users to Hermes bot
- `telegram-group-relay` — relaying group conversations via bot
- `references/claim-no-access-protocol.md` — audit sequence to run BEFORE claiming "no Telegram access" (proven gap 2026-08-19)
