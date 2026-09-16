---
name: mobile-device-edge
description: Bridge Hermes to Android Termux via FastAPI for camera/GPS.
---

# Mobile Device Edge — arifOS Sovereign Device Edge

> **Philosophy:** Phone hardware is high-trust boundary. Never auto-call sensitive endpoints. Every sensitive action requires signed F13 approval.

## What this is

A FastAPI server running on Termux (Android S24) that exposes a minimal, opinionated capability API to the VPS Hermes instance. Bound to Tailscale/Loopback only — never 0.0.0.0. Bearer token + HMAC request signing + one-time approval IDs for sensitive actions.

## Capability Matrix

| Endpoint | Action | Approval Needed |
| --- | --- | --- |
| `GET /v1/health` | Server health check | No |
| `GET /v1/status/battery` | Phone battery status | No |
| `GET /v1/status/device` | Device info (model, OS) | No |
| `POST /v1/location/once` | One-shot GPS fix | **Yes** (Signed F13 ID) |
| `POST /v1/camera/capture` | Photo capture (rear/front) | **Yes** (Signed F13 ID) |
| `POST /v1/sensors/snapshot` | Accelerometer/Gyro/Light | No |
| `POST /v1/vibrate` | Haptic feedback | No |

**Disabled (default deny):** Clipboard read/write, SMS read/send, Notification scraping, Arbitrary shell execution.

## Security Model

1.  **Bind Scope:** Bind to loopback (`127.0.0.1`) or Tailscale IP ONLY. Never 0.0.0.0.
2.  **Bearer Token:** Rotatable secret shared between VPS `.env` and Phone `.env`.
3.  **HMAC Request Signing:** Every POST request signed with `X-Timestamp`, `X-Nonce`, `X-Signature`. Timestamp window is 60s. Nonce is one-time use.
4.  **Approval IDs (F13 Gate):** Format `f13_<hex>_<endpoint>_<expiry_unix>`. Scoped to specific endpoint, one-time use, 5-minute TTL. Validated on the edge (phone) side.

## Tunneling Strategies (Phone -> VPS)

To reach localhost:8765 on the phone from the VPS:

1.  **FRP (Recommended):** Free, reliable outbound-only tunnel. VPS runs `frps`; phone runs `frpc`. No SSH required on phone side. Stable for recurring connections.
2.  **SSH Reverse Tunnel:** `ssh -R <remote_port>:localhost:<local_port> root@vps_ip`. Frequently fails on VPS if `PermitOpen` or `ForceCommand /bin/false` restricts the user. Requires OpenSSH client on phone.
3.  **Localhost.Run (Unstable):** Quick prototype via `ssh -R 80:localhost:8765 nokey@localhost.run`. Often drops after minutes due to free-tier limitations.

## File Structure

- `server.py` — FastAPI bridge (runs on phone)
- `client.py` — VPS-side Python client (imports `health()`, `capture_camera()`)
- `setup.sh` — Termux bootstrap script (installs dependencies, handles wake-lock)
- `frpc.ini` — Client tunnel config

## Pitfalls (from first build, 2026-08-25)

### Tailscale IP Swap
Always verify Tailscale IPs from BOTH sides before configuring bind hosts. In this mesh:
- VPS (`af-forge`) = `100.64.0.2`
- Phone (`arifs-s24`) = `100.64.0.1`
Arif sent a screenshot of the Headscale admin panel to confirm this.

### SSH Reverse Tunnel Often Fails
If `ssh -R` fails twice with `remote port forwarding failed for listen port`, don't keep retrying — pivot to frp immediately. Common causes:
- `ForceCommand /bin/false` in sshd_config (tunnel-arif user has this)
- IPv4/IPv6 binding mismatch
- Stale sshd-session processes from previous failed attempts (kill them)

### Termux Paste Pitfall (CRITICAL)
When Arif copies a multi-line response from Telegram into Termux, Termux tries to execute every line as a shell command. Explanatory text like "Fix cepat kat phone:" becomes "No command Fix found". 

**Rule:** When giving Arif commands to paste into Termux, give ONLY the command block. No explanation text adjacent. One command at a time. If multiple steps needed, provide a single script file he can `scp` and `bash`.

### FastAPI pip install on Termux
`pip install fastapi` fails because `pydantic-core` tries to compile Rust (target `aarch64-unknown-linux-android` not supported by rustup). Solutions:
1. `pkg install rust clang -y` then retry pip install
2. Use `--only-binary :all:` flag
3. Install pre-built wheels if available

### openssl Missing on Termux
`openssl rand -hex 16` fails silently if `openssl-tool` not installed. Install first: `pkg install openssl-tool`.

### .env Loading
`setup.sh` must explicitly `set -a && source .env && set +a` before starting server. Python `os.environ["KEY"]` will `KeyError` otherwise.