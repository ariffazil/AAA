---
name: arif-cf-token-discovery
description: arifOS Cloudflare token discovery — two-token system, truncated path trap, invalid VPS token vs active root token
tags: [cloudflare, tokens, arif-os, debugging, vps]
last_updated: 2026-05-04
---

# arifOS Cloudflare Token Discovery

## Context
When debugging Cloudflare API access for arifOS VPS deployment, a critical finding:
**Two separate CF tokens exist in the system, with different purposes and validity.**

## Discovery Path

```bash
# Check both token locations
cat /root/.cloudflare_token
cat /opt/arifos/secrets/cloudflare_token

# Test each token
curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer $(cat /root/.cloudflare_token)" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print('✅ Active' if d.get('result',{}).get('status')=='active' else '❌ Invalid')"
```

## Two Token System

| Token File | Purpose | Validity |
|-----------|---------|----------|
| `/root/.cloudflare_token` | CF API access (DNS, Pages, Workers) | ✅ ACTIVE |
| `/opt/arifos/secrets/cloudflare_token` | VPS deployment secrets | ❌ INVALID (stale/revoked) |

## The drift_detector.sh Trap

The drift detector at `/root/ops/drift_detector.sh` has:
```bash
CF_TOKEN_FILE="/root/...oken"
```
This **truncated path comment** hides the fact there are TWO distinct token files. It masks the invalid VPS token vs the valid root token.

When debugging CF token issues:
1. Always test `/root/.cloudflare_token` first — that's the working one
2. The `/opt/arifos/secrets/` path token is stale and returns `{"success":false,"errors":[{"code":1000,"message":"Invalid API Token"}]}`
3. Do NOT assume both tokens are the same or both valid

## arifOS VPS Token State (as of 2026-05-04)
- CF API Token (root): `***CF_TOKEN_REDACTED***` — ACTIVE ✅
- CLOUDFLARE_ZONE_NAME: `arif-fazil.com`
- CLOUDFLARE_ACCOUNT_ID: `22cc94b77b6481d2b054bee7952710e6`
- CLOUDFLARE_ZONE_ID: `6e837d3be53b37dcf79e0f09a1e14faa`
- All four vars live in the current shell's `os.environ` (printenv | grep CLOUDFLARE)

## Caddy + VPS Token Access (CRITICAL — Updated 2026-05-04)

**Symptom:** Caddy won't start, logs: `API token '' appears invalid`. The token exists in the shell env but `sudo caddy run` can't read it.

**Root cause:** Caddy runs as `sudo` (user `root`). The token is set in the current user shell environment (`os.environ['CLOUDFLARE_API_TOKEN']`) but NOT in `/root/.env` or any file `sudo` can reach. Also: `sudo -E` is ignored by Caddy's Go runtime (`warning: preserving the entire environment is not supported, -E is ignored`).

**The fix — extract token via Python, pass explicitly:**

```python
# Python can read the token from current process env
import os
token = os.environ['CLOUDFLARE_API_TOKEN']
print(token)  # ***CF_TOKEN_REDACTED***
```

Then start Caddy with explicit env vars:

```bash
CLOUDFLARE_API_TOKEN='***CF_TOKEN_REDACTED***' \
CLOUDFLARE_ZONE_NAME=arif-fazil.com \
CLOUDFLARE_ACCOUNT_ID=22cc94b77b6481d2b054bee7952710e6 \
CLOUDFLARE_ZONE_ID=6e837d3be53b37dcf79e0f09a1e14faa \
sudo caddy run --config /root/arifOS/Caddyfile --adapter caddyfile
```

**Why `sudo` can't see user env vars:** On this VPS, the `CLOUDFLARE_API_TOKEN` is injected into the shell profile (`~/.bashrc` or similar) but NOT into `/etc/environment` or a service file. `sudo` starts a fresh process without the user shell's env vars.

**Systemd masked Caddy:** Caddy was `masked` (`/etc/systemd/system/caddy.service` → `/dev/null`). `systemctl start caddy` does nothing. Start manually with `sudo caddy run` instead.

**Permanent fix needed:** Create `/etc/systemd/system/caddy.service.d/override.conf` with `Environment=CLOUDFLARE_API_TOKEN=...` so Caddy auto-starts on boot with the correct token.

## Cloudflare API Base Endpoints
- Token verify: `GET https://api.cloudflare.com/client/v4/user/tokens/verify`
- Zones: `GET https://api.cloudflare.com/client/v4/zones`
- Zone DNS: `GET https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records`
- Zone ID for arif-fazil.com: `6e837d3be53b37dcf79e0f09a1e14faa`
- Account ID: `22cc94b77b6481d2b054bee7952710e6`

## Pages API (requires valid account-level token)
- `GET https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects`
- Note: The root-level CF token may not have Pages permissions — Pages uses account-level auth
- Current account ID: `22cc94b77b6481d2b054bee7952710e6`
- Verified: root token CANNOT read Pages projects (returns error 10000 "Authentication error")
- Token scope confirmed: DNS + Workers ✅ | Pages ❌

## Site 404 Debugging Pattern (2026-05-01)
When sites return 404 from outside but 200 with Host header from inside:
- External check: `curl -sI https://site.arif-fazil.com` → 404
- Internal check (from VPS): `curl -s "https://site.arif-fazil.com" -H "Host: site.arif-fazil.com"` → 200
- Root cause: DNS/Cloudflare proxy routing issue, NOT missing files
- Files confirmed present via: `ls /var/www/html/<name>` on VPS
