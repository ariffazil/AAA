# VPS Build/Push Fallback — When GitHub Actions Fails

## The Problem

GitHub Actions `docker/build-push-action` fails with 403 on GHCR push (auth succeeds, build succeeds, manifest push fails). Local VPS still has valid GitHub token via `gh auth token`.

## The Pattern

When GitHub Actions cannot push to GHCR:
1. The image was built (either in GA or locally)
2. Push fails at GHCR layer, not auth
3. VPS can authenticate with same GitHub token via `gh auth token`
4. VPS can build locally and push
5. Compose + restart completes the deploy

## The Commands

```bash
# 1. Login using GitHub token (same token GA uses, still valid)
docker login ghcr.io -u ariffazil --password-stdin <<< "$(gh auth token)"

# 2. Build
cd /root/WEALTH
docker build -t ghcr.io/ariffazil/wealth:<short_sha> .

# 3. Push all tags
docker push ghcr.io/ariffazil/wealth:<short_sha>
docker tag ghcr.io/ariffazil/wealth:<short_sha> ghcr.io/ariffazil/wealth:latest
docker tag ghcr.io/ariffazil/wealth:<short_sha> ghcr.io/ariffazil/wealth:main
docker push ghcr.io/ariffazil/wealth:latest
docker push ghcr.io/ariffazil/wealth:main

# 4. Update compose
sed -i 's|ghcr.io/ariffazil/wealth:[a-f0-9]*|ghcr.io/ariffazil/wealth:<short_sha>|' /root/compose/docker-compose.yml

# 5. Restart
docker compose -f /root/compose/docker-compose.yml restart wealth-organ
```

## Script: `/root/scripts/wealth-build-push.sh`

Pre-made script at `/root/scripts/wealth-build-push.sh`. Run with:
```bash
bash /root/scripts/wealth-build-push.sh
```

## GitHub Actions Workflow Fix

**Before (broken):**
```yaml
password: ${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}
```

**After (correct):**
```yaml
password: ${{ secrets.GITHUB_TOKEN }}
```

`GITHUB_TOKEN` is auto-managed by GitHub, never expires. `GHCR_TOKEN` was expired → 403 → broken fallback that masked the real error.

## Verify Deploy

```bash
# Check container image updated
docker ps --filter name=wealth-organ --format "{{.Image}}"

# Check health endpoint
curl -s http://127.0.0.1:8082/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['image_tag'], '→', d['status'])"

# Check compose pin
grep 'ghcr.io/ariffazil/wealth' /root/compose/docker-compose.yml
```

## When to Use This

- GA workflow shows `ERROR: failed to push ... 403 Forbidden`
- `gh run list` shows workflow failed but build succeeded
- You have local SSH + docker access to VPS
- No new secrets needed — uses `gh auth token` which is already configured

## Limitation

This is a one-time fallback. When the next code change lands, GA will try again. If the 403 persists, investigate GHCR package settings or provenance config.