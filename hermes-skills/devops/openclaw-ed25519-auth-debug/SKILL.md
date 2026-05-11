---
name: openclaw-ed25519-auth-debug
description: Debug DEVICE_AUTH_SIGNATURE_INVALID when connecting Hermes to OpenClaw gateway via A2A WebSocket. Token auth sidecar is the working resolution.
tags: [openclaw, auth, ed25519, websocket, a2a, hermes]
---

# openclaw-ed25519-auth-debug

## Trigger

When Hermes/any agent tries to A2A-connect to OpenClaw gateway (`ws://127.0.0.1:18789`) and receives `DEVICE_AUTH_SIGNATURE_INVALID`.

## Debugging Sequence

### Step 1 — Verify the challenge

Fetch the challenge payload first:
```bash
wscat -x '{"jsonrpc":"2.0","method":"gateway.auth.challenge","id":1}' \
  ws://127.0.0.1:18789 2>&1 | python3 -m json.tool
```

Look for `challenge` (base64), `deviceId`, `scope`.

### Step 2 — Attempt standard signing

Use the device private key to sign the canonical payload:

```python
# Canonical payload format (pipe-delimited):
canonical = f"{challenge}|{device_id}|{scope}"
# Sign with Ed25519 PEM key at /root/.openclaw/identity/device.json
```

Try with `openssl pkeyutl -sign -inkey device.pem -in payload.txt -out signature.bin`
Verify 64-byte raw signature output.

### Step 3 — Signature variants to test

If Step 2 fails, try these variants (in order):

| Variant | Payload Format | Notes |
|---------|---------------|-------|
| Standard | `{challenge}\|{device_id}\|{scope}` | Try first |
| Challenge-only | `{challenge}` | Some gateways accept this |
| JSON | `{"challenge":"..."}` | Not typical but possible |
| Raw challenge | Raw base64 bytes | Edge case |

### Step 4 — Public key encoding check

The gateway may expect SPKI-encoded (SubjectPublicKeyInfo) public key, not raw 32-byte key:

```python
# Wrong — raw 32-byte
pubkey_raw = private_key.public_key().public_bytes_raw()

# Correct — SPKI (what OpenClaw expects)
pubkey_spki = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.SPKI,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
```

This was the suspected root cause — the gateway's Ed25519 verification may not accept raw key format.

## The Resolution (What Actually Worked)

**Do NOT spend more than 3 hours on Ed25519 sig debugging.**

The working path: **Token Auth Sidecar**

```bash
OPENCLAW_GATEWAY_TOKEN="hermes-asi-token" \
  openclaw gateway run \
  --auth token \
  --token "hermes-asi-token" \
  --port 18790 \
  --bind loopback
```

Test with Python WebSocket:
```python
import asyncio, websockets, json

async def test():
    async with websockets.connect("ws://127.0.0.1:18790") as ws:
        # Send auth
        await ws.send(json.dumps({
            "jsonrpc": "2.0", "method": "gateway.auth.token",
            "params": {"token": "hermes-asi-token"}, "id": 1
        }))
        result = await asyncio.wait_for(ws.recv(), timeout=5)
        data = json.loads(result)
        if data.get("result", {}).get("ok"):
            print("✅ Token auth successful")
        else:
            print(f"❌ Token auth failed: {data}")

        # Test health
        await ws.send(json.dumps({
            "jsonrpc": "2.0", "method": "gateway.health", "id": 2
        }))
        health = await asyncio.wait_for(ws.recv(), timeout=5)
        print(json.loads(health))
```

## Key Files

- Device identity: `/root/.openclaw/identity/device.json` (Ed25519 PEM — **never transmit**)
- Device auth token: `/root/.openclaw/identity/device-auth.json`
- Token auth sidecar: runs on port 18790 (separate from main gateway on 18789)
- A2A token: `hermes-asi-token` — Hermes use only, never expose to external LLMs

## Anti-Patterns

- **Option C (LLM-context private key)**: REJECTED definitively. Private key in LLM context = Langfuse logging + API transmission + vector memory storage. Irreversible security cascade.
- **Do NOT try more than 3 Ed25519 signature variants** before pivoting to token auth. The root cause is likely gateway SPKI encoding mismatch, not your signing code.
- **Do NOT restart the main gateway** (18789, systemd-managed) to test auth changes — use the sidecar port 18790 instead.

## If Token Auth Also Fails

1. Check the gateway actually supports `--auth token` mode (`openclaw gateway --help`)
2. Verify the token string matches exactly (no trailing spaces, no quotes)
3. Try binding to `0.0.0.0` vs `loopback` if the sidecar fails to start

## Verification

After successful token auth, test these methods:
- `gateway.health` — should return plugin status with all loaded plugins
- `gateway.agent.list` — should list configured agents
- `gateway.agent.sendMessage` — triggers Telegram delivery (with 888 approval gate, this is correct behavior)
