---
name: openclaw-cli-timeout-workaround
description: Bypass OpenClaw CLI timeouts by using Telegram direct message to @AGI_ASI_bot instead of openclaw agent CLI
triggers:
  - openclaw agent timeout
  - CLI hangs on agent call
  - message not reaching OpenClaw
category: devops
author: hermes
updated: 2026-05-05
tags: [openclaw, telegram, cli, workaround]
---

# openclaw-cli-timeout-workaround

## Problem
`openclaw agent --session-id X --message Y` and `openclaw agent --deliver ...` both timeout (30-60s) because MiniMax M2.7 model takes 30-60s per response. The CLI foreground-blocks waiting for the full agent loop.

## Root Cause
MiniMax M2.7 is slow. `openclaw agent` is blocking by design — it waits for the agent to produce a response before returning.

## Workaround (Arif-approved, verified 2026-05-05)
**Send the message directly to `@AGI_ASI_bot` in the AAA Telegram group** (ID: -1003753855708).

OpenClaw reads Telegram via polling consumer. A message sent to the bot in the group goes directly into OpenClaw's message queue — no CLI involved, no timeout.

## Session ID Format (verified)
- **Correct:** `5f67d92f-78fe-4eb2-bac7-605d91b0c9b1` (OpenClaw's internal system ID for the active group session)
- **Wrong:** `agent:main:telegram:group:-1003753855708:267378578` (full logical key — rejected by CLI as invalid)
- **Discover active sessions:** `openclaw sessions --active 60`

## Fallback: Gateway API (port 18789 vs 18790 distinction)
```
GET  http://127.0.0.1:18789/health          # main gateway, Ed25519 (broken)
GET  http://127.0.0.1:18790/health          # token-auth sidecar — WORKS
openclaw gateway call health --json         # uses port 18789
```

**`agent.sendMessage` IS valid** — but only on port 18790 (token-auth sidecar). On port 18789 (Ed25519), it returns `unknown method`. Use port 18790 token sidecar for direct WebSocket agent commands.

## Key Insight
This aligns with Arif's Acemoglu-inclusive institutional pattern: send intent to Telegram, let OpenClaw consume it natively. Don't use CLI as a proxy that competes with the agent's own Telegram consumer.

## Verification
- OpenClaw Telegram polling: confirmed active
- Gateway WebSocket: loopback-only on port 18789
- Bot (@AGI_ASI_bot): receives direct Telegram messages in group
