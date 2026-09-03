# GHCR Push 403 — Diagnosis + VPS Autonomous Fallback

## Root Cause Pattern

**Symptom:** GitHub Actions `docker/build-push-action@v6` fails with:
```
ERROR: failed to push ghcr.io/ariffazil/wealth:99e00ab: 
unexpected status from HEAD request to https://ghcr.io/v2/ariffazil/wealth/blobs/sha256:...: 403 Forbidden
```

**Observation:** `docker/login-action@v3` shows `refs/heads/main: read/write` — auth succeeds. Build completes. Push fails at **manifest stage**, not auth stage.

**Possible causes:**
1. GHCR package visibility or policy blocking the push
2. Provenance attestations rejected by GHCR
3. Package repository settings (org-level or repo-level GHCR config)
4. Quota exceeded on the GHCR org

## Diagnostic Sequence

```bash
# 1. Check recent failed runs
gh run list --limit 5

# 2. Get the actual error from failed job
gh run view <run_id> --log-failed 2>&1 | grep -E "ERROR|403|push" | head -20

# 3. Verify auth works locally (use gh auth token for docker login)
docker login ghcr.io -u ariffazil --password-stdin <<< "$(gh auth token)"
# If this succeeds → auth is fine, push issue is GHCR-side

# 4. Check what image SHA was built
docker images ghcr.io/ariffazil/wealth --format "{{Digest}}" | head -1

# 5. Check GHCR package settings:
# https://github.com/ariffazil/wealth/settings/packages
# Look for: visibility (public/private), delete permissions, policy
```

## VPS Autonomous Fallback

When GitHub Actions fails to push, use the VPS as fallback:

```bash
# Step 1: Login to GHCR using GitHub token (still valid)
docker login ghcr.io -u ariffazil --password-stdin <<< "$(gh auth token)"

# Step 2: Build locally (same Dockerfile, same context)
cd /root/WEALTH
docker build -t ghcr.io/ariffazil/wealth:<short_sha> .

# Step 3: Push manually
docker push ghcr.io/ariffazil/wealth:<short_sha>

# Step 4: Also push :latest and :main
docker tag ghcr.io/ariffazil/wealth:<short_sha> ghcr.io/ariffazil/wealth:latest
docker tag ghcr.io/ariffazil/wealth:<short_sha> ghcr.io/ariffazil/wealth:main
docker push ghcr.io/ariffazil/wealth:latest
docker push ghcr.io/ariffazil/wealth:main

# Step 5: Update compose pin
COMPOSE="/root/compose/docker-compose.yml"
CURRENT=$(grep -o 'ghcr.io/ariffazil/wealth:[a-f0-9]*' "$COMPOSE" | head -1)
sed -i "s|$CURRENT|ghcr.io/ariffazil/wealth:<short_sha>|" "$COMPOSE"

# Step 6: Restart container
docker compose -f "$COMPOSE" restart wealth-organ

# Step 7: Verify health
curl -s http://127.0.0.1:8082/health | python3 -c "import sys,json; d=json.load(sys.stdin); print('image:', d['image_tag'], 'status:', d['status'])"
```

## Script: `/root/scripts/wealth-build-push.sh`

```bash
#!/bin/bash
# Autonomous WEALTH build/push/restart — VPS fallback when GitHub Actions fails
set -euo pipefail

REPO_ROOT="/root/WEALTH"
IMAGE="ghcr.io/ariffazil/wealth"
COMPOSE="/root/compose/docker-compose.yml"

cd "$REPO_ROOT"

# Login via gh token
docker login ghcr.io -u ariffazil --password-stdin <<< "$(gh auth token)"

# Build + push
SHA=$(git rev-parse --short=7 HEAD)
TAG="${IMAGE}:${SHA}"

docker build -t "$TAG" .
docker push "$TAG"

# Update tags + compose + restart
docker tag "$TAG" "${IMAGE}:latest" "${IMAGE}:main"
docker push "${IMAGE}:latest" "${IMAGE}:main"

sed -i "s|ghcr.io/ariffazil/wealth:[a-f0-9]*|${IMAGE}:${SHA}|" "$COMPOSE"
docker compose -f "$COMPOSE" restart wealth-organ 2>/dev/null || docker restart wealth-organ

echo "✅ ${IMAGE}:${SHA} deployed"
```

## Workflow Fix (for when GHCR is fixed)

```yaml
# .github/workflows/publish-image.yml — KEY CHANGE:
# Use ONLY GITHUB_TOKEN (auto-managed, never expires)
# REMOVE: GHCR_TOKEN || GITHUB_TOKEN (broken fallback when GHCR_TOKEN expired)

- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}  # NOT: GHCR_TOKEN || GITHUB_TOKEN
```

Also add `cache-from: type=gha` and `cache-to: type=gha,mode=max` for faster rebuilds.

## Status as of 2026-05-19

- **GitHub Actions push:** Still failing 403 (investigation pending)
- **VPS fallback:** Working — `ghcr.io/ariffazil/wealth:99e00ab` pushed + running
- **Compose pin:** Updated to `99e00ab`
- **Container:** `wealth-organ` healthy on `ghcr.io/ariffazil/wealth:99e00ab`
- **Script:** `/root/scripts/wealth-build-push.sh` created for autonomous fallback