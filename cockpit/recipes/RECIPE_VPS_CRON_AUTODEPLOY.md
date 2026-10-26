# RECIPE 1 — VPS arif-forge auto-deploy via cron

**Author:** For Arif to execute from his laptop. No mutation from the agent.
**Goal:** `arif-forge` VPS polls `origin/main` every 5 min; if a new SHA appears,
runs `scripts/deploy-vps.sh` to rsync `public/` to `/var/www/html/arif`.

## Step 1 — Discover paths on the VPS

```bash
# SSH from Arif's laptop:
ssh arif@72.62.71.199

# On the VPS, find the repo and the deploy script:
sudo -i
find / -name "deploy-vps.sh" -type f 2>/dev/null
# Expected: /opt/arif-sites/scripts/deploy-vps.sh   (or wherever Arif placed it)
cd /opt/arif-sites
git rev-parse HEAD                       # note current SHA
git remote -v                           # confirm origin = arif-fazil.com
ls scripts/deploy-vps.sh                # confirm script exists
```

## Step 2 — Inspect the existing deploy script

```bash
cat /opt/arif-sites/scripts/deploy-vps.sh
```

The script should: (a) `git fetch origin main`, (b) check if HEAD moved,
(c) `rsync -a --delete public/ /var/www/html/arif/`, (d) optionally
`curl -X POST "https://api.cloudflare.com/.../purge_cache"` to invalidate
the Cloudflare edge cache.

If the script does NOT exist yet, a minimal one (60 lines) is at the
bottom of this recipe — paste it to `scripts/deploy-vps.sh` first.

## Step 3 — Install the cron entry

```bash
# Edit the VPS crontab:
crontab -e
# Add this single line at the bottom:
*/5 * * * * /opt/arif-sites/scripts/auto-deploy-cron.sh >> /var/log/arif-autodeploy.log 2>&1
```

The cron calls a thin wrapper (`auto-deploy-cron.sh`) — not `deploy-vps.sh`
directly — so we can log exit codes, lock against concurrent runs, and
keep the deploy script itself single-purpose.

## Step 4 — Install the wrapper

```bash
sudo tee /opt/arif-sites/scripts/auto-deploy-cron.sh > /dev/null <<'WRAPPER'
#!/usr/bin/env bash
# auto-deploy-cron.sh — invoked by cron every 5 min. Polls origin/main;
# if HEAD moved, runs deploy-vps.sh. Concurrency-locked so two cron
# invocations cannot run deploy at once.
set -euo pipefail
LOCK=/var/lock/arif-autodeploy.lock
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "[$(date -Iseconds)] another run in progress, exiting"; exit 0
fi
cd /opt/arif-sites
LOCAL=$(git rev-parse HEAD)
git fetch --quiet origin main
REMOTE=$(git rev-parse origin/main)
if [ "$LOCAL" = "$REMOTE" ]; then
  echo "[$(date -Iseconds)] no change (HEAD=$LOCAL)"; exit 0
fi
echo "[$(date -Iseconds)] new HEAD: $LOCAL -> $REMOTE"
git reset --hard origin/main >/dev/null
bash /opt/arif-sites/scripts/deploy-vps.sh
echo "[$(date -Iseconds)] deploy finished, exit=$?"
WRAPPER
sudo chmod +x /opt/arif-sites/scripts/auto-deploy-cron.sh
```

## Step 5 — Initial run + verification

```bash
# Manually run once to confirm it works:
bash /opt/arif-sites/scripts/auto-deploy-cron.sh
# Should print: "[date] no change" or "[date] new HEAD" + "deploy finished"

# Then wait one cron cycle (~5 min) and watch the log:
tail -f /var/log/arif-autodeploy.log
```

## Step 6 — Verify on the live site

From any machine:

```bash
curl -sI https://arif-fazil.com/earth/kinabalu-cross-section.html | grep last-modified
# Expected: a timestamp more recent than 2026-10-08 04:12:15 UTC
```

## Optional — minimal `deploy-vps.sh` if missing

```bash
sudo tee /opt/arif-sites/scripts/deploy-vps.sh > /dev/null <<'DEPLOY'
#!/usr/bin/env bash
# deploy-vps.sh — sync public/ to /var/www/html/arif. Idempotent.
set -euo pipefail
SRC=/opt/arif-sites/sites/arif-fazil.com/public
DST=/var/www/html/arif
mkdir -p "$DST"
rsync -a --delete \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='.build' \
  "$SRC/" "$DST/"
echo "[$(date -Iseconds)] rsync complete: $SRC -> $DST"
# Optional: invalidate Cloudflare edge if a token is set in env.
if [ -n "${CF_API_TOKEN:-}" ] && [ -n "${CF_ZONE_ID:-}" ]; then
  curl -s -X POST \
    "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/purge_cache" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"purge_everything":true}' >/dev/null
  echo "[$(date -Iseconds)] Cloudflare cache purged"
fi
DEPLOY
sudo chmod +x /opt/arif-sites/scripts/deploy-vps.sh
```

## Rollback

```bash
# Remove the cron line:
crontab -e   # delete the */5 line
# Or remove the wrapper entirely:
sudo rm /opt/arif-sites/scripts/auto-deploy-cron.sh
```

## Caveats

- **5-min lag between push and live.** Cron does not wake on push.
- **One VPS at a time.** If Arif has more than one VPS, the recipe covers
  one only.
- **rsync with --delete** will remove files from `/var/www/html/arif` that
  no longer exist in `public/`. This is normally correct; do NOT run if
  `/var/www/html/arif` is hand-edited outside `public/`.
- **Cloudflare purge** is optional. Without it, edge cache expires by
  TTL (Cloudflare default 4 h for HTML, longer for static). Without
  the API token in env, the script silently skips purge.

## Membrane compliance

- F13 SOVEREIGN: this recipe is a *template*. Arif pastes, Arif
  executes, Arif owns the VPS mutation. Agent has not SSHed.
- F1 AMANAH: crontab + wrapper are reversible (one `crontab -e` away).
- F2 TRUTH: documented expected output vs actual in Step 5/6.
