---
name: arifos-vps-git-metadata
description: "Diagnose and fix arifOS Docker image git metadata failures on VPS: DEPLOY_GIT_COMMIT=unknown, .env override bugs, and image-vs-compose drift. Triggers: runtime_drift TRUE, Observatory showing unknown git SHA, container env showing wrong commit."
category: devops
---

# arifOS VPS Git Metadata — Diagnosis & Fix

arifOS Docker images embed git commit/branch/time via `--build-arg ARIFOS_BUILD_SHA`. When this fails, the Observatory dashboard shows all dashes and `git_commit: unknown`. The VPS runtime also shows `runtime_drift: TRUE` even after container restarts.

---

## Diagnostic Steps

### Step 1 — Check container env
```bash
docker exec arifosmcp env | grep DEPLOY
```
Expected: `DEPLOY_GIT_COMMIT=<7-char-sha>`  
Bad: `DEPLOY_GIT_COMMIT=unknown` or `DEPLOY_GIT_COMMIT=<wrong-sha>`

### Step 2 — Check image baked metadata (before it starts)
```bash
docker run --rm ghcr.io/ariffazil/arifos:<tag> env | grep DEPLOY
```
If image shows `unknown` → image build failed. See Fix A.  
If image shows correct SHA but container shows wrong → .env override. See Fix B.

### Step 3 — Check compose .env
```bash
grep DEPLOY_GIT_COMMIT /root/compose/.env
```
Stale value here overrides image at runtime.

---

## Fix A — Image Built with --build-arg Defaulting to "unknown"

**Cause:** `--build-arg` values didn't reach Docker (often due to Makefile chaining with `&&` obscuring the build command).

**Fix:**
```bash
cd /root/arifOS
GIT_SHA=$(git rev-parse --short HEAD)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
BUILD_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)

docker build \
  --build-arg ARIFOS_BUILD_SHA=$GIT_SHA \
  --build-arg ARIFOS_BUILD_BRANCH=$GIT_BRANCH \
  --build-arg ARIFOS_BUILD_TIME=$BUILD_TIME \
  -t ghcr.io/ariffazil/arifos:$GIT_SHA \
  -t ghcr.io/ariffazil/arifos:latest \
  -f arifosmcp/Dockerfile .

# Verify before pushing
docker run --rm ghcr.io/ariffazil/arifos:$GIT_SHA env | grep DEPLOY

# Then push
docker push ghcr.io/ariffazil/arifos:$GIT_SHA
docker push ghcr.io/ariffazil/arifos:latest
```

---

## Fix B — .env Override (Image Correct, Container Wrong)

**Cause:** `/root/compose/.env` has `DEPLOY_GIT_COMMIT=<stale-sha>` which Docker Compose injects as environment override, taking precedence over image-baked `ENV`.

**Fix:**
```bash
# Update .env with correct SHA
sed -i 's/^DEPLOY_GIT_COMMIT=.*/DEPLOY_GIT_COMMIT=e9204365/' /root/compose/.env

# Restart container to pick up new env
docker stop arifosmcp && docker rm arifosmcp
cd /root/compose && docker compose up -d arifosmcp
# OR via background:
cd /root/compose && docker compose up -d --force-recreate arifosmcp
```

---

## Prevention — Makefile publish-ghcr

The `publish-ghcr` target in `/root/arifOS/Makefile` should sync `.env` after every successful push:

```makefile
publish-ghcr:
	@GIT_SHA=$$(git rev-parse --short HEAD); \
	# ... docker build with --build-arg ... && \
	# ... docker push ... && \
	sed -i 's/^DEPLOY_GIT_COMMIT=.*/DEPLOY_GIT_COMMIT=$$GIT_SHA/' /root/compose/.env && \
	echo "✅ GHCR: arifos:$$GIT_SHA pushed"
```

---

## Root Cause Chain

```
make publish-ghcr → docker build (--build-arg didn't reach Docker)
                → image has DEPLOY_GIT_COMMIT=unknown
                → docker push (succeeds, image is "valid")

Container restart → compose reads .env → DEPLOY_GIT_COMMIT=<stale> overrides image ENV
                  → Observatory shows all dashes (git_commit unknown)
                  → runtime_drift: TRUE (even though image was "correct")
```

**Key insight:** Docker Compose `environment:` and `.env` files override image-baked `ENV` at container start. Both Fix A (rebuild image) AND Fix B (update .env) are usually needed together.

---

## Verify After Fix

```bash
# 1. Container running correct image
docker ps --filter name=arifosmcp --format "{{.Names}}: {{.Status}} ({{.Image}})"

# 2. Container env shows correct SHA
docker exec arifosmcp env | grep DEPLOY_GIT_COMMIT

# 3. API confirms correct metadata
curl -s http://localhost:8080/api/status | grep -o '"git_commit":"[^"]*"'

# 4. No runtime drift
curl -s http://localhost:8080/api/status | grep -o '"runtime_drift":[^,]*'
```
All four should return consistent correct SHA and `runtime_drift: false`.

---

## Related Skills

- `arifos-deploy` — broader deployment doctrine
- `arifos-vps-runtime-audit` — VPS runtime source-of-truth protocol
- `vps-architecture-audit` — full container/service audit
