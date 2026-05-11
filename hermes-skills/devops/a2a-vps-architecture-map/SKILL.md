---
name: a2a-vps-architecture-map
description: Map the arifOS A2A backbone on the VPS — identify the production hub vs local dev adapters, auth tokens, and routing paths
trigger: "probe A2A, wire OpenClaw Hermes, debug A2A routing, federation manifest"
---

# arifOS A2A VPS Architecture Map

## The ONE Production A2A Hub

**AAA A2A Gateway (Docker) — port 3001**

```
Container: aaa-a2a
Port: 3001 (mapped via docker-proxy)
Auth: Bearer token + x-a2a-key header required
Verdict: 888_JUDGE enforcement — tasks go to "pending-human-review"
Federation manifest: GET /.well-known/arifos-federation.json
```

- Primary endpoint: `POST /tasks`
- Agent card: `GET /.well-known/agent-card.json`
- Registered agents: AAA architect, engineer, auditor, GEOX witness, WEALTH witness
- Vault status: DISCONNECTED

## Auth Tokens (from ~/AAA/a2a-server/server.js)

```javascript
A2A_TOKEN = process.env.A2A_TOKEN || 'aaa-a2a-token-dev'
A2A_API_KEY = process.env.A2A_API_KEY || 'aaa-a2a-apikey-dev'
ARIFOS_API_KEY = process.env.ARIFOS_API_KEY || 'hermes-agent-apikey-dev'
```

**Headers:**
```
Authorization: Bearer aaa-a2a-token-dev
x-a2a-key: aaa-a2a-apikey-dev
```

## Verified Working A2A Probe

```bash
curl -s -X POST http://127.0.0.1:3001/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer aaa-a2a-token-dev" \
  -H "x-a2a-key: aaa-a2a-apikey-dev" \
  -d '{"jsonrpc":"2.0","id":"probe","method":"tasks/send","params":{"taskId":"t-001","message":{"parts":[{"kind":"text","text":"ping"}]}}}'
```

Returns: `{"status":{"state":"pending-human-review"}}` — 888_JUDGE is LIVE.

## Red Herrings — Local Python Adapters

These exist at `/opt/arifOS/a2a-adapters/` but are NOT the production A2A path:

| Port | Script | Status | Notes |
|------|--------|--------|-------|
| 18001 | hermes-a2a.py | LISTENING | Calls `hermes chat -q`; POSTs timeout if MiniMax dead |
| 18002 | openclaw-a2a.py | LISTENING | Calls `openclaw agent --message`; slow subprocess |

NOT registered in AAA federation manifest. Personal dev tooling only.

## Other A2A Services

| Service | Port | Status |
|---------|------|--------|
| AAA A2A Gateway | 3001 | ✅ LIVE — production hub |
| GEOX A2A Gateway | 3002 | ✅ LIVE — GEOX-specific |
| a2a-server (srv) | 3001 | ⚠️ Legacy — Docker container is canonical |

## Telegram Bot Token Issue

Only ONE Telegram bot polls — both channel IDs share the SAME token:

```
Telegram 1003753855708 (@AGI_ASI_bot):   connected, polling ✅
Telegram 1003890512851 (@ASI_arifos_bot): stopped — Duplicate token error ❌
```

BotFather never issued a separate token for @ASI_arifos_bot.

## Key Findings (2026-05-07)

1. **AAA gateway is the A2A hub** — all dispatch goes through port 3001
2. **888_JUDGE enforcement is live** — every task hits HOLD_888
3. **VAULT999 is disconnected** — AAA gateway reports `vault: DISCONNECTED`
4. **MiniMax 2049 blocks everything** — primary reasoning model dead
5. **GEOX and WEALTH are registered mesh agents** in federation manifest

## A2A Routing Path

```
OpenClaw → Kimi → AAA A2A Gateway (3001)
                        ↓ agent-dispatch skill
                   Hermes / GEOX / WEALTH / etc.
                        ↓
                   888_JUDGE verdict
                        ↓
                   OpenClaw → Telegram response
```

## Verification Commands

```bash
# Check port 3001 holder
ss -tlnp | grep 3001

# AAA gateway health
curl -s http://127.0.0.1:3001/health

# Federation manifest
curl -s http://127.0.0.1:3001/.well-known/arifos-federation.json | python3 -m json.tool | grep '"id"'

# Hermes agent card via gateway
curl -s http://127.0.0.1:3001/.well-known/agent-card.json | python3 -m json.tool | grep '"name"'
```

## Notes

- Do NOT probe ports 18001/18002 for production A2A — local dev adapters only
- AAA gateway runs as Docker container `aaa-a2a`
- The a2a-server in /srv/openclaw/workspace/ is legacy — Docker container is canonical
