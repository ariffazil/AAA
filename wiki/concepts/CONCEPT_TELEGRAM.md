---
title: "Concept — Telegram Dual-Bot Architecture: OpenClaw vs Hermes"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: concept
status: canonical
tags: [telegram, openclaw, hermes, architecture, dual-bot, webhook]
confidence: high
domain: infra/telegram
sources: [AAA/workspace/MEMORY.md, session-log-2026-05-17]
---

# Telegram Dual-Bot Architecture: OpenClaw vs Hermes

> **Design intent confirmed 2026-05-17:** OpenClaw and Hermes use separate Telegram bots with intentionally different triggering mechanisms. This is not a bug — it is a feature.

## The Two Bots

| Property | OpenClaw | Hermes |
|---------|----------|--------|
| **Bot name** | @AGI_ASI_bot | @ASI_arifos_bot |
| **Token** | `8149595687:AAGycp7nzl...` | Different token |
| **Telegram mode** | Webhook (intended) / Polling (current) | Polling |
| **Trigger** | @mention only | Ambient (all messages) |
| **Role** | AGI-level operator | ASI-level relay |
| **Session scope** | Per-sender (direct) | Group ambient |
| **Model** | MiniMax-M2.7 primary | Configured model |

## The Intentional Separation

```
OpenClaw (@AGI_ASI_bot)
├── Only responds when @mentioned
├── Webhook receiver: port 8787 (SOUL.md intent)
├── Caddy route: openclaw.arif-fazil.com/webhook/telegram → 127.0.0.1:8787
└── DM policy: open (anyone can DM)

Hermes (@ASI_arifos_bot)
├── Sees ALL group messages (ambient polling)
├── Group chat: -1003753855708
├── No mention required
└── Relay to arifOS for governance
```

**Why this is intentional:**
- OpenClaw = operator agent, responds when called
- Hermes = ambient awareness, watches everything, sends summaries/alerts
- They don't conflict because they have different tokens and different triggering rules

## Why 409 Conflict Was NOT a Token Collision

The 409 Conflict error on OpenClaw's @AGI_ASI_bot was caused by:
1. Telegram's server had a stale webhook registration for @AGI_ASI_bot
2. OpenClaw tried to poll (getUpdates)
3. Telegram rejected polling because webhook was set
4. **NOT** Hermes interfering — Hermes uses a completely different bot token

**Fix:** `deleteWebhook?drop_pending_updates=true` cleared Telegram's stale webhook state.

## Current Working State (2026-05-17)

| Component | Status |
|-----------|--------|
| OpenClaw polling | ✅ Working (webhook 8787 not listening) |
| Hermes polling | ✅ Working |
| Telegram webhook for OpenClaw | ❌ Not registered (polling handles it) |
| Port 8787 webhook receiver | ❌ Not running |
| Caddy webhook route | ✅ Configured correctly |
| OpenClaw gateway | ✅ Live PID 626541 on 18789 |

## The Webhook Receiver Gap

SOUL.md specifies:
```
Mode: Webhook (not polling)
Webhook: https://openclaw.arif-fazil.com/webhook/telegram
Local: http://127.0.0.1:8787/telegram-webhook
```

But port 8787 has no listener. The webhook receiver is not running. OpenClaw is operating in **polling mode** despite SOUL.md saying webhook.

**This is a SOUL.md drift issue**, not a functional failure. Polling works.

## Group Chat Behavior

**AAA Group** (`-1003753855708`):
- Hermes sees ALL messages (ambient polling)
- OpenClaw only responds to @mentions of @AGI_ASI_bot
- Result: Two independent conversation flows in the same group

**Direct messages:**
- Both bots accept DMs
- OpenClaw: `dmPolicy: open`
- Hermes: ambient relay

## Telegram Session Key Format

OpenClaw Telegram sessions use this format:
```
agent:main:direct:267378578      ← Direct message
agent:main:telegram:group:-1003753855708  ← Group message
```

## Key Rules for Agents

1. **Don't worry about "conflict" between the two bots**
   They are completely separate Telegram accounts with separate tokens.

2. **If 409 on getUpdates → delete webhook first**
   Telegram has a stale webhook on the bot's Telegram server, not a local conflict.

3. **OpenClaw webhook intent is in SOUL.md but not running**
   This is drift. Not a crisis — polling works. But the webhook receiver (port 8787) needs to be enabled for full SOUL.md compliance.

## Related Pages

- [[scar-openclaw-telegram-409-2026-05-17]] — the 409 incident with root cause analysis
- [[TREE777]] — where these bots sit in the agent landscape
- [[intelligence-tree]] — AGI (OpenClaw) vs ASI (Hermes) distinction

---
DITEMPA BUKAN DIBERI — Two bots, two roles, no collision.
