---
name: arifos-deploy-ghcr-push-gap
description: "arifOS deploy.yml built images but never pushed to GHCR — stale images accumulated, broken Dockerfile fixed locally but not published"
triggers:
  - "deploy.yml CI not pushing to GHCR"
  - "docker image ghcr.io/ariffazil/arifos stale"
  - "dockerfile playwright install missing"
  - "broken GHCR image can't be pulled from other machines"
tags:
  - github-actions
  - docker
  - ghcr
  - deploy
  - arifOS
---

# arifOS Deploy GHCR Push Gap

## Problem
`deploy.yml` (GitHub Actions → VPS via SSH) was building Docker images locally on the VPS but **never pushing them to GHCR**. This meant:
1. Broken Dockerfile fixes were local-only
2. Other machines pulling `ghcr.io/ariffazil/arifos:<sha>` got stale/broken images
3. The `playwright` dependency was missing from pip install — local build worked (separate package install), but CI could never reproduce the build

## Root Cause
`deploy.yml` had `docker build` + `docker run` but no `docker push`.

```bash
# What existed (broken):
docker build -t "ghcr.io/ariffazil/arifos:${GIT_SHA}" ...
docker compose up -d ...

# What was added:
docker build -t "ghcr.io/ariffazil/arifos:${GIT_SHA}" ...
docker push ghcr.io/ariffazil/arifos:"${GIT_SHA}" &    # push in background
docker push ghcr.io/ariffazil/arifos:latest &
wait
```

## Second Bug: Dockerfile Missing playwright
```dockerfile
# BEFORE (broken):
RUN pip install --no-cache-dir ... psutil
# playwright referenced but never pip-installed
RUN python -m playwright install --with-deps chromium  # FAILS

# AFTER (fixed):
RUN pip install --no-cache-dir ... psutil playwright   # added playwright
RUN python -m playwright install --with-deps chromium  # now works
```

## Compose Repo Doesn't Exist
`/root/compose` remote set to `https://github.com/ariffazil/compose.git` — repository does not exist. `git reset --hard origin/main` in deploy.yml would fail. Removed entirely.

## What Deploy.yml Now Does
1. Build image with git metadata from GitHub Actions env (not local git)
2. Push to GHCR in background (parallel)
3. Auto-update docker-compose.yml image tag via `sed`
4. Force-recreate container
5. Verify health endpoint

## Key Files Changed
- `/root/arifOS/Dockerfile` — playwright fix
- `/root/arifOS/arifosmcp/Dockerfile` — already clean (no playwright issues)
- `/root/arifOS/.github/workflows/deploy.yml` — added push + sed tag update + removed git reset

## Verification
```bash
# Check what image running container uses
docker exec arifosmcp env | grep DEPLOY_GIT_COMMIT

# Check GHCR tags
docker images | grep arif

# Check compose points to correct image
grep "image:.*arifos" /root/compose/docker-compose.yml
```
