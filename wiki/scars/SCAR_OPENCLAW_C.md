---
title: "Scar — OpenClaw Telegram 409 Conflict + Webhook vs Polling Architecture"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: scar
status: canonical
tags: [openclaw, telegram, webhook, polling, 409, hermes, infrastructure]
confidence: high
domain: infra/telegram
severity: medium
actors: [openclaw, hermes-agent]
sources: [session-log-2026-05-17, openclaw-webhook-architecture-2026-05-17.md]
---

# Scar — OpenClaw Telegram 409 Conflict + Webhook vs Polling Architecture

## What Happened

During a diagnostic session on 2026-05-17, OpenClaw's Telegram channel (@AGI_ASI_bot) showed a `409 Conflict` error in gateway logs:

```
[telegram] [diag] polling cycle error
err=Call to 'getUpdates' failed! (409: Conflict: terminated by setWebhook request)
Another OpenClaw gateway, script, or Telegram poller may be using this bot token;
stop the duplicate poller or switch this account to webhook mode.
```

This was **not** Hermes vs OpenClaw bot token collision (they are separate bots with separate tokens). The 409 was caused by **Telegram's side having an old webhook registration** for @AGI_ASI_bot that conflicted with OpenClaw's getUpdates polling call.

## Root Cause Analysis

### Primary: Stale Telegram Webhook Registration

Telegram's API returns 409 Conflict when:
1. A webhook is set (`setWebhook` was previously called with a URL)
2. AND a `getUpdates` polling call is made on the same bot token

Telegram rejects polling when a webhook is configured because they are mutually exclusive modes.

**The sequence:**
```
1. Some prior operation called setWebhook for @AGI_ASI_bot → webhook registered in Telegram
2. OpenClaw started in polling mode → Telegram sees active webhook, rejects getUpdates with 409
3. OpenClaw auto-retried → 409 again
4. OpenClaw eventually recovered → Telegram's webhook expired or was cleared
```

### Secondary: Hermes Uses a Different Bot

| Agent | Bot | Token | Telegram Mode |
|-------|-----|-------|--------------|
| OpenClaw | @AGI_ASI_bot | 8149595687:AAGycp7nzl... | Polling (was failing with 409) |
| Hermes | @ASI_arifos_bot | different token | Polling |

**No token collision.** The 409 was entirely within @AGI_ASI_bot's Telegram state.

## The Architecture Reality

### SOUL.md Says Webhook...

OpenClaw's `SOUL.md` and `IDENTITY.md` specify:
```
Mode: Webhook (not polling)
Webhook: https://openclaw.arif-fazil.com/webhook/telegram
Local: http://127.0.0.1:8787/telegram-webhook
```

This means OpenClaw **should** be listening on port 8787 for Telegram webhook payloads, forwarded by Caddy from `https://openclaw.arif-fazil.com/webhook/telegram`.

### ...But Port 8787 Is Not Listening

```
$ ss -tlnp | grep 8787
(no output — nothing on port 8787)

$ curl -s http://127.0.0.1:8787/telegram-webhook
(connection refused)
```

The webhook receiver (port 8787) is **not implemented or not started**. OpenClaw 2026.5.7 on this VPS runs in **polling mode only**, despite SOUL.md saying webhook.

### Current Working Architecture

```
@AGI_ASI_bot ← Telegram API → OpenClaw gateway (port 18789)
                                mode: polling (not webhook)
                                status: connected, 0 pending updates
```

### Caddy Is Configured for Webhook (But Nothing On 8787)

Caddyfile already has the rewrite configured:
```caddy
openclaw.arif-fazil.com {
    handle /webhook/telegram* {
        reverse_proxy /telegram-webhook 127.0.0.1:8787
    }
    handle {
        reverse_proxy 127.0.0.1:18789
    }
}
```

This is correct — but port 8787 has no listener, so Telegram webhook traffic would 502.

## The Event Loop Saturation (Separate Issue)

The OpenClaw gateway showed **severe event loop saturation** during the session:

```
Gateway event loop degraded:
  eventLoopUtilization: 1.0  (maxed out — gateway stalled)
  cpuCoreRatio: 1.031         (100%+ CPU on one core)
  eventLoopDelayMaxMs: 17381  (17 second event loop lag!)
```

**Causes:**
- Plugin bundling on startup (48 runtime deps bundled on every startup in logs)
- Heavy MCP tool calls running through the gateway
- Long-running inference sessions

**Symptoms:**
- High latency on gateway commands
- Commands timing out
- Gateway may appear slow but is not dead

## Anti-Pattern: Diagnosing Without Probing

The **wrong** way to check OpenClaw liveness:
```bash
openclaw doctor
openclaw plugins list     # ← has side effect: triggers gateway restart
openclaw gateway status   # ← reads systemd state, not process state
openclaw channels list
```

The **right** way:
```bash
curl -s http://127.0.0.1:18789/health
# → {"ok":true,"status":"live"}  ← direct, no side effects
```

## Countermeasures Applied

### 1. Telegram Webhook Reset
```bash
# Force Telegram to drop any stale webhook registration
curl -s "https://api.telegram.org/bot<REDACTED_TOKEN>/deleteWebhook?drop_pending_updates=true"
# Result: {"ok":true}
```

### 2. Verified Polling Is Working
```
getWebhookInfo → url: "" (empty — no webhook)
getUpdates → pending: 0 (clean polling)
```

### 3. Gateway Restart After Systemd Recovery
```
systemd service: active (running) PID 626541
gateway: live on 127.0.0.1:18789
event loop: still degraded (separate issue)
```

## Open Questions (Not Yet Resolved)

| Question | Status |
|----------|--------|
| Why does SOUL.md say webhook mode but 8787 is not listening? | Open issue — does OpenClaw 2026.5.7 support webhook receiver natively? |
| Should we enable webhook mode or stay on polling? | Polling works. Webhook is more efficient but needs 8787 listener. |
| What is causing event loop saturation? | Heavy MCP calls + plugin bundling — needs investigation |
| How to enable port 8787 webhook receiver? | Need to find OpenClaw 2026.5.7 webhook configuration |

## TREE777 Lessons

### Lesson 1: 409 = Telegram Side Has Webhook Set
**Never assume 409 means token collision.** Telegram 409 on getUpdates means Telegram has a webhook registered for that bot — the bot must use webhook mode or the webhook must be deleted.

### Lesson 2: CLI Status ≠ Process State
`systemctl status` and `openclaw gateway status` read systemd unit state, not the actual running process. The gateway can be live while systemd shows transitional states.

### Lesson 3: SOUL.md ≠ Current Configuration
SOUL.md records **intended** architecture, not current state. Port 8787 is in SOUL.md as the webhook listener but nothing is running there. Always verify against live system state.

### Lesson 4: Single Curl > CLI Cascade
One `curl http://127.0.0.1:18789/health` answers "is it alive?" without side effects. CLI commands can have hidden side effects (plugins list triggers restart, etc.).

### Lesson 5: Two Telegram Bots Can Coexist
OpenClaw and Hermes use separate bot tokens. They can both poll Telegram simultaneously without conflict as long as tokens are different.

## Verification (2026-05-17)

```bash
# Gateway live check
curl -s http://127.0.0.1:18789/health
# → {"ok":true,"status":"live"} ✅

# Telegram polling clean
curl -s "https://api.telegram.org/bot<REDACTED_TOKEN>/getWebhookInfo"
# → {"url": "", "pending_update_count": 0} ✅

# No port 8787 listener (webhook receiver missing)
ss -tlnp | grep 8787
# → (empty) ⚠️

# Event loop still degraded
openclaw channels status
# → eventLoopUtilization: 1 ⚠️
```

## Related Pages

- [[TREE777]] — the 7-layer intelligence tree this scar lives in
- [[scar-openclaw-diagnostic-cascade-2026-05-17]] — the separate diagnostic cascade failure (same day, different root cause)
- [[intelligence-tree]] — 7-layer model
- [[skill-anti-fabrication]] — fabrication detection (false claims are related to false diagnostics)

---
DITEMPA BUKAN DIBERI — The system told the truth. The agent misread it.
sread it.
misread it.
