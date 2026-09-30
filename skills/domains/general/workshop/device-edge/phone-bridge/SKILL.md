---
name: phone-bridge
description: "Use when bridging Termux phone sensors (battery, camera, GPS) via FastAPI for edge-device workflows. Termux FastAPI bridge for battery, camera, GPS, sensors."
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Phone Bridge

## Architecture (Tailscale direct — verified 2026-09-29)

Phone (Termux) runs the stdlib `server.py` bound `0.0.0.0:8765`. VPS reaches it
directly over the Headscale tailnet at `100.64.0.6:8765`. No tunnel.

The earlier claim "Android Tailscale blocks incoming TCP to Termux" is **WRONG**
— refuted 2026-09-29: ping and HTTP both succeed phone-ward once the Headscale
ACL grants the port. The tunnel was the fragile path all along.

Two layers must both allow the port:
1. Headscale ACL (`/etc/headscale/acl.yaml`) — phone IP:8765 in the `tag:arifos` dst list
2. Phone `server.py` binding `0.0.0.0` (NOT `127.0.0.1`)

## Files at /root/AAA/phone-bridge/

- server.py — FastAPI bridge (phone)
- client.py — VPS Python client
- setup.sh — Termux bootstrap
- .env — VPS env
- .env.phone — Phone env

## Security

1. Bearer token on every request
2. HMAC-SHA256 request signing on POST
3. F13 approval_id for sensitive actions (one-time, scoped, 5-min TTL)
4. No shell endpoint — hardcoded termux-* commands only
5. Audit log — metadata only

## Endpoints

- GET /health — auto, NO AUTH (open liveness probe). `client.py` must probe `/health`, NOT `/v1/health` — the server has no `/v1/health` route, so a `/v1/health` probe returns 401 and the proxy reports `phone_state: DEAD` while the phone is perfectly healthy.
- GET /v1/status/battery — auto
- GET /v1/status/device — auto
- POST /v1/location/once — F13 approval
- POST /v1/camera/capture — F13 approval
- POST /v1/sensors/snapshot — auto
- POST /v1/vibrate — auto
- POST /v1/toast — auto

Default deny: clipboard, SMS, notifications, continuous GPS, shell.

## Tunnel (legacy — not the default)

The tunnel was the original path and died 2026-09-29 (`*.lhr.life` → HTTP 503).
Prefer Tailscale direct. Keep the tunnel only as a fallback for a device that
cannot join the tailnet.

`ssh -R 80:localhost:8765 nokey@localhost.run -N` — the hostname rotates, and a
dead tunnel answers **503**, not a connection error.

## Deploy

Preferred — one-shot installer `honor-install.sh` (embeds `server.py` + `.env`,
installs the pkg deps, starts a tmux session `bridge`, takes a wake-lock).

Serve it from the VPS on the tailnet, download it on the phone with curl into a
file, then run that file. The serving port needs a temporary Headscale ACL grant
for the phone — remove the grant and stop the static server after use. Bind the
static server to the tailnet IP, not `0.0.0.0`.

Manual (legacy):

Phone:
```
mkdir -p ~/phone-bridge
scp -P 22888 root@72.62.71.199:/root/AAA/phone-bridge/server.py ~/phone-bridge/
scp -P 22888 root@72.62.71.199:/root/AAA/phone-bridge/setup.sh ~/phone-bridge/
scp -P 22888 root@72.62.71.199:/root/AAA/phone-bridge/.env.phone ~/phone-bridge/.env
cd ~/phone-bridge && bash setup.sh &
```

Tunnel (separate session):
```
ssh -R 80:localhost:8765 nokey@localhost.run -N
```

## Pitfalls

- pip install fastapi fails on Android (Pydantic needs Rust). Use --only-binary :all:
- BRIDGE_BIND_HOST must be 127.0.0.1 for tunnel mode, not 100.64.0.1
- address already in use = pkill -f "python.*server.py"
- setup.sh must source .env before server
- localhost.run unstable, use autossh for production
- Zombie sshd-session on VPS from failed tunnels
- **`python3` on the Hermes VPS is Hermes's own interpreter and has no `requests`.** Run the bridge with `/usr/bin/python3` or it dies at `import client` with `ModuleNotFoundError`.
- **Headscale ACL is a silent cross-node port gate.** A port not listed is TCP-dropped with no journal entry — it looks exactly like the phone being down. Check `/etc/headscale/acl.yaml` first, then `headscale policy check -f <file>` + `systemctl restart headscale` to apply.
- **Proxy verbs are POST, not GET.** `curl -X POST -d '{}' http://127.0.0.1:18800/battery`; a GET returns `unknown path`.
- **Play-Store Termux:API is incomplete** — `termux-telephony-deviceinfo` answers "Termux:API is not yet available on Google Play". Battery still works. Install Termux **and** Termux:API from F-Droid (same source, or the signatures clash).
- **The bridge is not durable.** It lives in a tmux session; a phone reboot or Termux kill stops it. Restart with:
  `tmux kill-session -t bridge; tmux new -d -s bridge 'cd ~/phone-bridge && source .env && exec python server.py'`
- **New device = new tailnet node.** Re-register into Headscale (`headscale auth register --auth-id <id> --user arifos-federation`), THEN add its IP:8765 to the ACL, then point `.env` `BRIDGE_PHONE_HOST` at the new IP. A new phone does not inherit the old node's IP.
