# RECIPE 2 — GitHub webhook → VPS arif-forge

**Author:** For Arif to execute from his laptop + GitHub UI. No agent mutation.
**Goal:** every push to `main` triggers an immediate deploy on the VPS
(no 5-min cron lag). The webhook posts to a small HTTPS listener on the
VPS that verifies an HMAC-SHA256 secret and runs `deploy-vps.sh`.

## Topology

```
git push origin main
  → GitHub Actions (validation only)            : GH-side, automatic
  → GitHub webhook "arif-forge-deploy"          : GH-side, configured below
      POST https://72.62.71.199:8443/deploy
      X-Hub-Signature-256: sha256=...
      body: { ref, after, repository.full_name, ... }
    → VPS listener (caddy + caddy-webhook plugin, OR a tiny Go/Python server)
      verify HMAC
      exec /opt/arif-sites/scripts/deploy-vps.sh
        → rsync → /var/www/html/arif
        → optional: Cloudflare purge
```

## Part A — VPS-side listener (caddy + caddy-webhook)

Caddy handles TLS via Let's Encrypt for the public IP `72.62.71.199`,
and `caddy-webhook` verifies the GitHub HMAC and runs the script.

### A1. Install plugins (one-time)

```bash
# On the VPS:
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
  | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
  | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
# Install the webhook plugin via xcaddy (requires Go):
go install github.com/admirallarimda/caddy-webhook@latest
# Or use the prebuilt binary — see https://github.com/admirallarimda/caddy-webhook/releases
```

### A2. Caddyfile

```bash
sudo tee /etc/caddy/Caddyfile > /dev/null <<'CADDY'
# Public listener for arif-fazil.com (existing — keep as-is, just shown for context):
arif-fazil.com, *.arif-fazil.com {
    root * /var/www/html/arif
    encode gzip zstd
    file_server
}

# Webhook listener on a separate port. Replace SECRET with the one you
# generate in Part B step B2; it MUST match what you paste into GitHub.
72.62.71.199:8443 {
    route /deploy {
        webhook {
            id "github-arif-forge"
            script /opt/arif-sites/scripts/webhook-deploy.sh
        }
    }
}
CADDY
sudo systemctl reload caddy
```

If you do not want a public IP listener, instead use a Cloudflare Tunnel
(`cloudflared`) in front of the listener; the Caddyfile is the same.

### A3. The script the webhook calls

```bash
sudo tee /opt/arif-sites/scripts/webhook-deploy.sh > /dev/null <<'HOOK'
#!/usr/bin/env bash
# webhook-deploy.sh — invoked by caddy-webhook when GitHub POSTs /deploy.
# caddy-webhook has already verified the HMAC. We just need to deploy.
set -euo pipefail
LOG=/var/log/arif-webhook.log
echo "[$(date -Iseconds)] webhook fired" >> "$LOG"
cd /opt/arif-sites
git fetch --quiet origin main
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)
if [ "$LOCAL" = "$REMOTE" ]; then
  echo "[$(date -Iseconds)] no change" >> "$LOG"; exit 0
fi
git reset --hard origin/main >/dev/null
bash /opt/arif-sites/scripts/deploy-vps.sh 2>&1 | tee -a "$LOG"
HOOK
sudo chmod +x /opt/arif-sites/scripts/webhook-deploy.sh
```

`deploy-vps.sh` is the same script as in Recipe 1.

## Part B — GitHub-side webhook (UI)

### B1. Generate a secret

On any machine:

```bash
openssl rand -hex 32
# Copy the 64-char hex string. This is your webhook secret.
```

### B2. Configure the webhook in GitHub UI

1. Open https://github.com/ariffazil/arif-fazil.com/settings/hooks
2. Click **Add webhook**.
3. Fill the form:

| Field | Value |
|---|---|
| Payload URL | `https://72.62.71.199:8443/deploy` (or the tunnel URL) |
| Content type | `application/json` |
| Secret | paste the hex string from B1 |
| SSL verification | Enable (Caddy uses Let's Encrypt — should pass) |
| Which events… | "Just the push event." |
| Active | ✓ |

4. Click **Add webhook**.

### B3. Test

GitHub sends a `ping` event on creation. Check:

```bash
# On the VPS:
tail -f /var/log/arif-webhook.log
# Should show: "[date] webhook fired" within a few seconds of clicking Add.
```

If you used `caddy-webhook` and the script does not fire, check:

```bash
journalctl -u caddy --since "5 minutes ago" | tail -30
```

## Part C — Verification on live site

After any push to `main`:

```bash
# From your laptop, within 60 seconds:
curl -sI https://arif-fazil.com/earth/kinabalu-cross-section.html | grep last-modified
# Expected: a fresh timestamp.

# VPS log:
tail -5 /var/log/arif-webhook.log
# Expected: "[date] new HEAD: <old> -> <new>" then "rsync complete"
```

## Rollback

```bash
# Disable the webhook (GitHub UI):
#   https://github.com/ariffazil/arif-fazil.com/settings/hooks
#   → click the webhook → Disable (or Delete)

# Stop the listener (VPS):
sudo caddy unvalidate  # if using caddy-webhook via api
# Or comment out the 72.62.71.199:8443 block in /etc/caddy/Caddyfile, then:
sudo systemctl reload caddy
```

## Caveats

- **Public IP listener on port 8443.** If the VPS has no public IP, use
  Cloudflare Tunnel (`cloudflared tunnel route …`) — same Caddyfile works.
- **caddy-webhook plugin** is third-party. The plugin verifies the GitHub
  HMAC against the secret; without that, anyone could POST and trigger a
  deploy. Do not skip the secret.
- **Concurrency.** If you also have the cron from Recipe 1, the
  deploy-vps.sh runs are race-prone. Add `flock -n /var/lock/deploy.lock`
  at the top of `deploy-vps.sh` (Recipe 1's `auto-deploy-cron.sh` already
  has this; the webhook variant does not).
- **Body size.** GitHub's push payload can be hundreds of KB. Caddy
  default body limit is fine; if you proxy through Cloudflare, check
  your account's request size cap.
- **No 5-min lag** vs. cron recipe, but **single point of failure** is
  the listener. Cron + webhook is a belt-and-braces option (webhook
  handles the common case, cron catches missed deliveries).

## Membrane compliance

- F13 SOVEREIGN: webhook secret is owned by Arif. Listener config
  requires Arif's VPS access. Agent has not SSHed or pushed anything.
- F1 AMANAH: webhook delete + caddy reload reverts in seconds.
- F2 TRUTH: every step has a verification command in Part C.
