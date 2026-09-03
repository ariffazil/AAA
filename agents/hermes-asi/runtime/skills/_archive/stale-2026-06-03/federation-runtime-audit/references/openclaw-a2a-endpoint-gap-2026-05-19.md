# OpenClaw A2A Endpoint Gap — 2026-05-19

## Problem

Arif wants Hermes and OpenClaw to communicate via A2A (agent-to-agent protocol).
Reality: **OpenClaw does NOT implement an A2A server endpoint.**

## Architecture Reality

| Service | Port | What it does | A2A POST /tasks |
|---------|------|--------------|-----------------|
| OpenClaw Gateway | 18789 | WebSocket/HTTP gateway + HTML dashboard | ❌ 404 |
| OpenClaw Webhook | 8787 | Telegram webhook listener | ❌ Not HTTP |
| OpenClaw Agent Card | 18795 | GET only | ❌ 501 (POST not supported) |
| Hermes A2A Adapter | 18001 | ✅ A2A server (POST /tasks) | ✅ Works |

**OpenClaw port 18789 is a gateway for WebSocket + web UI — NOT an A2A server.**

## Evidence

```bash
# Gateway health — works
curl http://127.0.0.1:18789/health
# → {"ok":true,"status":"live"}

# A2A POST to OpenClaw gateway — 404
curl -X POST http://127.0.0.1:18789/tasks -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test","method":"tasks/send",...}'
# → Not Found (404)

# Agent card endpoint — GET works, POST fails
curl http://127.0.0.1:18795/.well-known/agent-card.json
# → 200 OK with full agent card

curl -X POST http://127.0.0.1:18795/tasks -H "Content-Type: application/json" -d '...'
# → 501 Unsupported (POST not implemented)
```

## Current Communication Path

```
Hermes (18001) → polls @ASI_arifos_bot → forwards to AAA gateway (3001)
                                        ↓
OpenClaw (18789) ← Telegram webhook ← @AGI_ASI_bot
```

**They use DIFFERENT Telegram bots as communication channel — not true A2A.**

## Options to Enable True A2A

### Option A: OpenClaw ACPX sub-agent hook
Register Hermes as an ACPX sub-agent. OpenClaw calls `hermes acp-sops` CLI for ASI judgment.
- Requires: edit `openclaw.json` → `plugins.entries.acpx.config.agents`
- Pro: Proper A2A
- Con: Touches OpenClaw config (requires 888_HOLD for Arif)

### Option B: Hermes-a2a.py WebSocket client bridge
Hermes-a2a.py (port 18001) adds a WebSocket client to OpenClaw gateway (18789).
- Requires: hermes-a2a.py modification
- Pro: No OpenClaw config change
- Con: Complex, breaks if gateway API changes

### Option C: Telegram relay (current, works)
Both agents use Telegram as message bus with structured JSON payloads.
- Requires: Nothing — already working
- Con: Not true A2A, latency, no native agent-to-agent semantics

## Recommended

**Option C for now (working), Option A for proper A2A (requires Arif decision).**

## Config Fix Applied (2026-05-19)

OpenClaw was in 12-restart crash loop due to invalid enum values:
```
Before: permissionMode="off", nonInteractivePermissions="auto-approve"  ← INVALID
After:  permissionMode="deny-all", nonInteractivePermissions="deny"    ← VALID
```

File: `/root/.openclaw/openclaw.json`
Fix: `systemctl restart openclaw-gateway` → gateway stable on port 18789

## Ports Summary

```
18789 — OpenClaw gateway (WebSocket, HTTP, dashboard) — MAIN
18790 — DOES NOT EXIST (hermes-a2a.py points here but nothing listens)
18795 — OpenClaw agent-card server (GET only)
 8787 — OpenClaw Telegram webhook listener
18001 — Hermes A2A adapter (POST /tasks working)
3001  — AAA A2A gateway
3002  — APEX (888_JUDGE)
```