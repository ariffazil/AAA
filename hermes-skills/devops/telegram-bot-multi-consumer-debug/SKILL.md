---
name: telegram-bot-multi-consumer-debug
description: Debug Telegram bot getUpdates returning 0 when another consumer (e.g. MaxHermes) is long-polling the same token. Includes diagnostic chain, workarounds, and prevention.
triggers: ["telegram getUpdates 0", "bot not receiving messages", "hermes telegram conflict", "ASI_bot updates empty"]
tags: [telegram, debugging, bot-api, long-polling, hermes]
---

# Telegram Bot Multi-Consumer Debug Skill

## Problem
Two or more processes are polling the same Telegram bot token via `getUpdates` (long-polling). Result: `getUpdates` returns 0 for all consumers except the one that established the poll first. The bot is confirmed alive in the group but updates are invisible.

## Symptoms
- `getUpdates` returns 0 messages
- `getMe` succeeds (token valid)
- `getChat` succeeds (bot can see the chat)
- `getChatMember` confirms bot IS in the group with correct status
- `getChatHistory` returns HTTP 404 (older Bot API version)

## Diagnostic Chain
```
1. Verify token works        → getMe
2. Confirm bot is in group   → getChatMember (does NOT consume updates)
3. Try getUpdates            → if 0, another consumer is likely long-polling
4. Check channel_directory   → ~/.hermes/channel_directory.json (Hermes known chats)
5. Check state.db messages   → SQLite store with 18k+ rows if Hermes is polling
```

## Key Insight
`getChatMember` is the diagnostic that doesn't disturb the existing poll stream. Use it to confirm bot membership and chat existence without consuming updates.

## New Diagnostic: Update ID Offset (2026-05-06)
When OpenClaw owns the polling consumer and you need to see what messages arrived AFTER your test:
```python
import requests
token = 'YOUR_BOT_TOKEN'

# Step 1: Get current highest update_id FIRST (before consuming)
r = requests.get(f'https://api.telegram.org/bot{token}/getUpdates',
    params={'limit': 1, 'timeout': 0}, timeout=5)
updates = r.json().get('result', [])
latest_uid = updates[-1]['update_id'] if updates else 0
print(f'Baseline update_id: {latest_uid}')

# Step 2: Send your test message
r2 = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={
    'chat_id': 'GROUP_ID',
    'text': '@sealion_ai_bot verify this claim',
    'reply_to_message_id': 1234,  # Thread reply
})
my_msg_id = r2.json().get('result', {}).get('message_id')

# Step 3: Wait for potential response
import time; time.sleep(10)

# Step 4: Get updates AFTER your message (offset = latest_uid + 1)
r3 = requests.get(f'https://api.telegram.org/bot{token}/getUpdates',
    params={'offset': latest_uid + 1, 'limit': 20, 'timeout': 0}, timeout=5)
new_msgs = r3.json().get('result', [])
for u in new_msgs:
    msg = u.get('message', {})
    print(f'[{msg.get("message_id")}] @{msg.get("from",{}).get("username","?")}: {str(msg.get("text",""))[:100]}')
```

**Critical:** The offset approach lets you see messages that arrived AFTER your baseline, bypassing the consumer lock. Messages your baseline already consumed will NOT appear — they belong to OpenClaw's consumer window.

## Workarounds

### Option A: Third observer bot (recommended for history fetching)
Create a dedicated history-fetching bot that joins groups as a silent observer. It has its own token, no other consumer. Steps:
1. Create new bot via @BotFather
2. Add to target group
3. Fetch via `getUpdates` — no conflict since no other process uses this token

### Option B: Read from Hermes state.db
If MaxHermes/Hermes is consuming updates for the target bot, messages may be stored in its local SQLite store:
```
~/.hermes/state.db
Tables: sessions (110 rows), messages (18347 rows)
```
Query: join messages to sessions on session_id to get Telegram context.

### Option C: Tap session JSON files
Hermes session files at `~/.hermes/sessions/session_*.json` contain full message history for Telegram sessions. Parse these for context.

## Self-Healing: Flood Control

**Telegram flood control is self-healing.** If `getUpdates` returns 0 but the bot was previously active, the most likely cause is Telegram's flood control (too many messages sent in short succession). Symptoms:
- 22–38 second retry waits in logs
- "Flood control" messages in Hermes logs
- Bot suddenly goes silent for 1–5 minutes, then resumes

**Do NOT restart the gateway during flood control** — it would reset the long-polling offset and Telegram would not know the bot is still connected, potentially causing duplicate message delivery.

**Wait 2–5 minutes.** Flood control clears automatically. Monitor with:
```bash
tail -n 20 ~/.hermes/logs/errors.log | grep -i flood
```

## Prevention
- One bot token = one consumer only
- For polling-based history fetch, always use a dedicated bot token separate from the live messaging bot
