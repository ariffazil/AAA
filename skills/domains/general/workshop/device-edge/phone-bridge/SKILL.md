---
name: phone-bridge
description: "Use when bridging Termux phone sensors (battery, camera, GPS) via FastAPI for edge-device workflows. Termux FastAPI bridge for battery, camera, GPS, sensors."
---

# Phone Bridge

## Architecture

Phone (Termux) runs FastAPI server at 127.0.0.1:8765. VPS calls through outbound SSH tunnel (localhost.run). Android Tailscale blocks incoming TCP to Termux.

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

- GET /v1/health — auto
- GET /v1/status/battery — auto
- GET /v1/status/device — auto
- POST /v1/location/once — F13 approval
- POST /v1/camera/capture — F13 approval
- POST /v1/sensors/snapshot — auto
- POST /v1/vibrate — auto
- POST /v1/toast — auto

Default deny: clipboard, SMS, notifications, continuous GPS, shell.

## Tunnel

Why not Tailscale: Android blocks incoming TCP to Termux. All ports fail.
Why not ssh -R: Termux OpenSSH fails "remote port forwarding failed".
Working: `ssh -R 80:localhost:8765 nokey@localhost.run -N`

## Deploy

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
