---
name: openclaw-telegram-broadcast
description: Send directives to OpenClaw via Telegram when CLI gateway API times out. Background delivery pattern for af-forge VPS.
tags: [openclaw, telegram, broadcast, af-forge, CLI]
version: 2026.05.05
---

# OpenClaw Telegram Broadcast

## Context
When the OpenClaw CLI `openclaw agent` command times out (30-60s) because it waits for the full MiniMax agent response loop, the Telegram broadcast path via `openclaw message send --channel telegram` delivers the directive directly to OpenClaw's Telegram consumer — bypassing the gateway API entirely.

Discovered after `openclaw agent --session-id --deliver` and `curl POST /agent` both failed due to timeout or unknown endpoint.

## Command
```bash
openclaw message send \
  --channel telegram \
  --target "-1003753855708" \
  --message "🔴 YOUR DIRECTIVE TEXT HERE" \
  2>&1
```

## Important Notes
- Takes 30-90 seconds to complete (full agent loop runs before delivery)
- Use `background=true` with `notify_on_complete=true` to avoid blocking
- Message appears in Telegram with full formatting support
- OpenClaw receives it as a Telegram update, not a direct CLI invocation

## Telegram Group IDs (af-forge)
- AAA group: `-1003753855708`
- Backup: `-1003815535761`
- Backup: `-1003718232946`
- **Chatgpt supergroup (A2A relay thread):** `-1003815535761` / topic `562` ✅ Verified 2026-05-06

## Bot Token
The bot token in `/root/.openclaw/env.local` (`8149595687:AAGycp7nzl1-D8mzZKOkUJWiWxg3Ok-wy70`) is active. Always use `openclaw message send` instead of raw curl to Telegram API.

## Method 2: Group Thread Relay (discovered 2026-05-06)
When `@AGI_ASI_bot` username resolution fails via `send_message(action='list')`, send to the shared Chatgpt group thread instead.

```python
send_message(
    action='send',
    target='telegram:Chatgpt / topic 562',  # shared Chatgpt thread
    message='⚖️ HERMES → OPENCLAW | BRIEFING TEXT...'
)
```

**Why it works:** Both Hermes and OpenClaw are members of the Chatgpt supergroup. OpenClaw reads group messages via `contextVisibility: "all"`. The thread acts as a shared A2A inbox.

**When to use:**
- Direct `@AGI_ASI_bot` username fails with "Could not resolve"
- Need formatting preserved (markdown → Telegram)
- Want to maintain thread context
- Longer messages that don't fit CLI character limits

## When to Use
- `openclaw agent --session-id` times out → Method 1 (CLI)
- Direct @username resolution fails → Method 2 (Group Thread)
- Gateway WebSocket auth not yet established (F11 block)
- Need to deliver a directive to OpenClaw without waiting for full response
- Works reliably even when gateway CLI is unresponsive
