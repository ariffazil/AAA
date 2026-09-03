# Federation Agent Communication Discovery — 2026-05-19

## Key Finding: No True A2A Between Hermes and OpenClaw

**Claim tested:** Hermes and OpenClaw communicate via A2A protocol (agent-to-agent).
**Reality:** They use Telegram as relay channel, not true A2A.

### Actual Communication Architecture

```
OpenClaw Gateway (port 18789) — WebSocket/HTTP/gateway only, NO A2A server
OpenClaw Telegram (@AGI_ASI_bot) — separate bot token, webhook mode
    ↓ Telegram message bus
Hermes polling (@ASI_arifos_bot) — separate bot token, polling mode
    ↓ forwards to
AAA Gateway (port 3001)
```

### Port Status Map

| Port | Service | HTTP Health | A2A POST /tasks |
|------|---------|-------------|------------------|
| 18789 | OpenClaw gateway | ✅ 200 ({"ok":true}) | ❌ 404 |
| 18790 | Non-existent | ❌ Connection refused | — |
| 18795 | OpenClaw agent-card | ✅ 200 (GET) | ❌ 501 |
| 8787 | OpenClaw webhook | N/A | N/A |
| 18001 | Hermes A2A adapter | ✅ 200 | ✅ Works |
| 3001 | AAA A2A gateway | ✅ 200 | ✅ Works |
| 3002 | APEX (888_JUDGE) | ✅ 200 | — |

### Critical Implication

OpenClaw's gateway at port 18789 is a **WebSocket gateway + web dashboard**, not an A2A server.
It cannot receive A2A task requests from Hermes via HTTP POST.
Hermes cannot delegate to OpenClaw via A2A.

### Discovery Method

```bash
# A2A POST test to OpenClaw gateway (port 18789)
curl -X POST http://127.0.0.1:18789/tasks \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test","method":"tasks/send",...}'
# → 404 Not Found

# A2A GET test to agent-card endpoint (port 18795)
curl http://127.0.0.1:18795/.well-known/agent-card.json
# → 200 OK (returns full agent card)

curl -X POST http://127.0.0.1:18795/tasks -H "Content-Type: application/json" -d '...'
# → 501 Unsupported (POST not implemented at this endpoint either)
```

### Hermes-A2A.py Configuration (Dead Reference)

`hermes-a2a.py` line 7 says: `Calls OpenClaw gateway at 127.0.0.1:18790 (token-auth sidecar) for model inference`
But **port 18790 does not exist** — nothing listens there.

The actual OpenClaw gateway is on port 18789 but doesn't support A2A POST.

### What This Means for Cross-Agent Coordination

1. **Telegram relay is the current coordination mechanism** — works but not true A2A
2. **True A2A requires**: OpenClaw ACPX sub-agent hook registration, or Hermes-a2a.py WebSocket client to port 18789
3. **888_HOLD applies** to Option A (OpenClaw config change) — Arif must decide
4. **Option C (Telegram relay)** works now, no changes needed

## A2A Protocol Discovery Checklist

When validating cross-agent A2A connectivity:
1. Test POST /tasks to the target agent's port — expect 200 or proper JSON-RPC response
2. If 404/501 → endpoint doesn't implement A2A server
3. Test GET /.well-known/agent-card.json — if this works but POST doesn't, endpoint is read-only
4. Check `ss -tlnp | grep <port>` to confirm what's actually listening
5. Never assume gateway port = A2A server

## Reference Commands

```bash
# Test A2A endpoint availability
curl -X POST http://<host>:<port>/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tasks/send","params":{"message":{"role":"user","parts":[{"kind":"text","text":"ping"}]}}}'

# Check what's actually listening on a port
ss -tlnp | grep <port>

# Get agent card (read-only endpoint — most agents support this)
curl http://<host>:<port>/.well-known/agent-card.json
```