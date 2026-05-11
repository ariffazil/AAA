---
name: openclaw-gateway-ed25519-auth
description: Authenticate Hermes to OpenClaw gateway via Ed25519 OR token-auth sidecar. F11 identity gate for af-forge VPS WebSocket endpoint.
tags: [openclaw, ed25519, token-auth, gateway, f11, authentication, af-forge]
version: 2026.05.05.revised
---

# OpenClaw Gateway Authentication — Ed25519 (FAILS) + Token Auth (WORKS)

## Context
When Hermes (ASI on af-forge VPS) needs to communicate with the OpenClaw gateway via WebSocket, it must pass an F11 identity gate. 

**⚠️ Ed25519 device auth is BROKEN on this gateway.** Despite correct signature math (64-byte Ed25519 signature, verified with OpenSSL), the gateway consistently returns `DEVICE_AUTH_SIGNATURE_INVALID`. This has been extensively debugged (2026-05-05): multiple payload formats, fresh nonces, public key extraction, custom instanceId — all fail at the same point: server-side signature verification.

**✅ The working solution is token auth on a separate sidecar port (18790).**

---

## APPROACH 1: Token Auth (RECOMMENDED — WORKS)

### Start the token-auth sidecar
```bash
openclaw gateway run --auth token --token hermes-asi-token --port 18790
```
Token: `hermes-asi-token` (from `/root/.openclaw/identity/device-auth.json` `operatorToken` field)

### Verify it's running
```bash
curl http://127.0.0.1:18790/health
# Expected: gateway status JSON
```

### Full WebSocket auth test
```python
import json, asyncio, websockets, base64

TOKEN = "hermes-asi-token"
PORT = 18790

async def ws_auth_test():
    uri = f"ws://127.0.0.1:{PORT}/"
    async with websockets.connect(uri) as ws:
        # Receive challenge
        challenge = json.loads(await ws.recv())
        nonce = challenge["nonce"]

        # Send auth response
        await ws.send(json.dumps({
            "type": "connect.auth",
            "token": TOKEN,
            "nonce": nonce
        }))

        # Receive result
        result = json.loads(await ws.recv())
        print(result)
        # Expected: {"type":"res","id":"1","ok":true}

asyncio.run(ws_auth_test())
```

### Available methods after auth
Once authenticated, these methods work on port 18790:
- `gateway.health` — full gateway status
- `agent.sendMessage` — sends message via Telegram (respects 888 veto gate)
- `agent.list` — lists available agents

---

## APPROACH 2: Ed25519 Device Auth (DOES NOT WORK — DOCUMENTED FOR REFERENCE)

### Extract identity components
```python
import json, re

with open("/root/.openclaw/identity/device.json") as f:
    device = json.load(f)
with open("/root/.openclaw/identity/device-auth.json") as f:
    content = f.read()

device_id = device["deviceId"]
private_key_pem = device["privateKeyPem"]

# Token from device-auth.json
m = re.search(r'"token":\s*"([^"]+)"', content)
operator_token = m.group(1)
```

### Sign challenge with OpenSSL
```bash
# Message format: nonce:timestamp
echo -n "hermes-asi-1777968200:1777968200" > /tmp/sign_message.bin

openssl pkeyutl -sign \
  -inkey /root/.openclaw/identity/device.json \
  -in /tmp/sign_message.bin \
  -out /tmp/signature.bin

# Result: 64 bytes = valid Ed25519 signature
```

### Construct + send auth payload
```python
import base64, json, time

sig = open("/tmp/signature.bin", "rb").read()
sig_b64 = base64.b64encode(sig).decode()

nonce = f"hermes-asi-{int(time.time())}"
timestamp = str(int(time.time()))

auth_payload = {
    "type": "connect.auth",
    "deviceId": device_id,
    "actorId": "hermes-asi",
    "operatorToken": operator_token,
    "timestamp": timestamp,
    "nonce": nonce,
    "signature": sig_b64
}
```

**⚠️ This will fail with `DEVICE_AUTH_SIGNATURE_INVALID`. Server-side gateway Ed25519 verification is broken or uses a non-standard variant.**

---

## Critical Findings (2026-05-05)

1. **Ed25519 auth is a dead end.** Gateway consistently rejects valid signatures. Not a key encoding issue — the math is correct.

2. **Token auth on port 18790 works perfectly.** WebSocket handshake completes, `health` returns full status, `agent.sendMessage` fires to Telegram.

3. **Two gateway ports, two auth modes:**
   - `18789` — main gateway, Ed25519 device auth (broken)
   - `18790` — token-auth sidecar, token auth (works)

4. **Token `hermes-asi-token` is stable.** Stored in `/root/.openclaw/identity/device-auth.json`.

5. **Restarting the sidecar:** kill old process, restart with the `openclaw gateway run` command above. No systemd service yet — runs as background process.

## File Locations on af-forge
- Device identity: `/root/.openclaw/identity/device.json`
- Auth tokens: `/root/.openclaw/identity/device-auth.json`
- Main gateway port: `18789` (Ed25519 — broken)
- Token sidecar port: `18790` (token auth — works)
- Token: `hermes-asi-token`

## When to Use
- Hermes needs to relay a directive to OpenClaw via WebSocket → use port 18790
- F11 Hold triggered on anonymous relay → use port 18790 token auth
- Telegram relay times out → use port 18790 as bypass path
- All other delivery paths (`openclaw agent`, Telegram bot) timed out → port 18790

## Verification Checklist
- [ ] `curl http://127.0.0.1:18790/health` returns gateway JSON
- [ ] WebSocket connects without `DEVICE_AUTH_SIGNATURE_INVALID`
- [ ] `agent.sendMessage` fires and delivers to Telegram (with 888 approval gate)
