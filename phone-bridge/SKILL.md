# Phone Bridge — VPS Skill

> **Sovereign Device Edge** — Hermes talks to Arif's phone through this skill.
> The phone enforces F13 policy independently. No arbitrary shell.

## What this is

A FastAPI server running on Termux (Android S24) that exposes a **minimal,
opinionated capability API** to the VPS Hermes instance. Bound to Tailscale
interface only. Bearer token + HMAC request signing + one-time approval
IDs for sensitive actions.

## VPS-side pickup layer (added 2026-08-25)

After the bridge stabilized on Tailscale, a thin federation pickup now
sits in front of `client.py` so any arifOS / A-FORGE / Hermes agent can
talk to the phone through one stable, governed surface.

- **File:** `/root/AAA/phone-bridge/pickup_proxy.py`
- **Bind:** `127.0.0.1:18800` (change via `PHONE_PICKUP_PORT`)
- **Pattern:** APA-style envelopes (same shape as `A-FORGE/bridges/gemini_bridge.py`)
- **Reach cache:** `phone_state` refreshed every 30s; ONLINE / DEAD / UNREACHABLE

### Verbs

| Verb | Required F13 `approval_id`? | Maps to phone |
|------|------------------------------|---------------|
| `health` | no  | GET `/v1/health` (probe only) |
| `battery` | no  | GET `/v1/status/battery` |
| `device` | no  | GET `/v1/status/device` |
| `sensors` | no  | POST `/v1/sensors/snapshot` |
| `locate` | **yes** (one-time, ≤300s TTL) | POST `/v1/location/once` |
| `capture` | **yes** (one-time, ≤300s TTL) | POST `/v1/camera/capture` |
| `vibrate` | no  | POST `/v1/vibrate` |
| `toast` | no  | POST `/v1/toast` |

### Start it

```bash
# venv-free: pure stdlib + requests (system pip)
set -a && source /root/.secrets/kunci-root.env && set +a
nohup python3 /root/AAA/phone-bridge/pickup_proxy.py \
  >> /var/log/phone_pickup.log 2>&1 &
```

### Probe

```bash
curl -s http://127.0.0.1:18800/health | jq       # liveness
curl -s http://127.0.0.1:18800/verbs  | jq       # list of verbs
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"verb":"battery"}' http://127.0.0.1:18800/battery | jq
```

The pickup applies a `phone_state` pre-flight on every non-health verb —
if the phone is `DEAD`, you get HTTP 503 with `phone_state`/`phone_detail`
in the envelope instead of a hung-up phone-call.

### Tailscale path (recommended)

`/etc/headscale/acl.yaml` has the rule:

```yaml
{src: "tag:arifos", dst: ["100.64.0.1:8765", "100.64.0.1:8022"]}
```

SIGHUP `headscale.service` (or write the file — inotify auto-reloads).
There is no need for `localhost.run` SSH tunnels or `frpc` if the Tailscale
ACL rule is in effect — direct `arifs-s24.arifOS.ts.net:8765` works.

### Frp fallback (when Tailscale ACL is patched down)

`frps` lives on VPS at `:7000` with token `arif-phone-tunnel-2026`. Phone
must run `frpc` (binary at `/root/frp_0.61.1_linux_amd64/frpc`) with a config
that:

```
serverAddr = "af-forge.arifOS.ts.net"
serverPort = 7000
[[proxies]]
name = "phone-bridge"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8765
remotePort = 18765
```

Then point `BRIDGE_PHONE_HOST=127.0.0.1` `BRIDGE_PORT=18765` for `pickup_proxy.py`.

### Known current state (2026-08-25)

- `acl.yaml` reloaded with `100.64.0.1:8765` + `100.64.0.1:8022` allow rules.
  Tailscale ping `arifs-s24` ⇒ 8ms. Direct TCP to `:8765` now returns
  `Failed to connect after 15 ms` (was 12 s timeout) ⇒ ACL permit,
  bridge server **DEAD on the phone**.
- The user's phone bridge was last running as the original invocation;
  multiple restart attempts hit `EADDRINUSE` for a moment, then
  the bridge died (Termux session doze / wake-lock dropped).
  Action needed on the phone: `pkill -f "python.*server.py"` then
  `tmux new -d -s bridge "cd ~/phone-bridge && source .env && exec python server.py"`.


## Capability matrix

| Action            | Endpoint                  | Approval needed |
| ----------------- | ------------------------- | --------------- |
| Health check      | `GET /v1/health`          | No              |
| Battery status    | `GET /v1/status/battery`  | No              |
| Device info       | `GET /v1/status/device`   | No              |
| GPS one-shot      | `POST /v1/location/once`  | **Yes** (F13)   |
| Camera capture    | `POST /v1/camera/capture` | **Yes** (F13)   |
| Sensors snapshot  | `POST /v1/sensors/snapshot` | No            |
| Vibrate           | `POST /v1/vibrate`        | No              |
| Toast notification| `POST /v1/toast`          | No              |

**Disabled (default deny):**
- Clipboard read/write
- SMS read/send
- Notification scraping
- Continuous location tracking
- Arbitrary shell execution

## Security model

1. **Bind to localhost or Tailscale IP** — never `0.0.0.0` in production
2. **Bearer token** — every request, rotated on VPS rebuild or phone loss
3. **HMAC request signing** — `X-Timestamp` + `X-Nonce` + `X-Signature`
   on every POST. Timestamp window: 60s. Nonce: one-time use.
4. **Approval IDs** — `f13_<hex>_<endpoint>_<expiry>` for sensitive
   actions. One-time use, scoped, 5-minute TTL.
5. **Audit log** — metadata only (timestamp, action, approval_id hash).
   Never SMS/clipboard/photo content.
6. **Artifact TTL** — phone artifacts auto-delete after 24h.
7. **No shell endpoint** — every `termux-*` command is hardcoded server-side.

## F13 flow

```
Arif asks: "snap my field sample"
    │
    ▼
Hermes proposes via Telegram:
   🔒 Hermes requests phone action
   Action: capture rear-camera image
   Purpose: inspect field sample
   TTL: 300s
   Approve? [YES] [NO]
    │
    ▼
Arif: YES
    │
    ▼
Hermes calls issue_approval("camera_capture")
    │
    ▼
Hermes calls capture_camera(approval_id=..., save_to=...)
    │
    ▼
Phone bridge:
   1. Verify bearer token
   2. Verify HMAC signature + timestamp + nonce
   3. Verify approval_id (one-time, scoped, not expired)
   4. Run fixed termux-camera-photo -c 0 <safe-path>
   5. Return image bytes
   6. Delete local copy after upload
    │
    ▼
Hermes logs metadata, returns result
```

## Files

- `server.py` — FastAPI bridge (runs on phone)
- `client.py` — VPS-side Python client (Hermes imports this)
- `setup.sh` — Termux bootstrap script
- `.env` — Shared secrets (NEVER commit)
- `frpc.ini` — frp tunnel client config (phone side)
- `frps.ini` — frp server config (VPS side)

## Setup (on phone)

```bash
# 1. Install Termux:API from F-Droid
#    https://f-droid.org/en/packages/com.termux.api/

# 2. Pull files from VPS
scp server.py setup.sh .env ~/phone-bridge/

# 3. Run setup
cd ~/phone-bridge && bash setup.sh
```

## Setup (on VPS)

```bash
# Already have client.py. Hermes loads it as a skill.
# .env lives at /root/AAA/phone-bridge/.env
# Hermes sources it before importing client.

# To start frps:
/root/frp_0.61.1_linux_amd64/frps -c /root/frp_0.61.1_linux_amd64/frps.ini &
```

## Failure modes

- **Bridge offline** → VPS health check fails → Hermes reports
  `PHONE_BRIDGE_UNAVAILABLE`, no auto-retry storm
- **Token leak** → rotate `BRIDGE_TOKEN` on both sides + restart phone service
- **Signing secret leak** → rotate `BRIDGE_SIGNING_SECRET` + invalidate all
  in-flight approval IDs (re-issue F13 prompts)
- **Phone lost** → revoke Tailscale ACL for phone hostname, rotate all secrets
- **Tunnel drop** → autossh will reconnect automatically within 30s

## Future scope

After MVP stabilizes:
- Notification posting (low-risk, useful for Hermes→user push)
- Clipboard write (user-triggered only, e.g. share URL)
- Sensor streaming (rate-limited)

**Never scope:**
- SMS send (always F13, only for emergencies)
- Clipboard read (privacy risk)
- Notification scraping (oversharing risk)
- Arbitrary termux-* (RCE risk)
