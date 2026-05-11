---
name: arifos-publish-ghcr-workflow
description: Build and push arifOS Docker image to GHCR. Fixes Makefile cut delimiter bug. Run from /root/arifOS/.
tags: [docker, ghcr, makefile, arifos, release]
last_updated: 2026-05-01
---

# arifOS GHCR Publish Workflow

## Trigger
Run `make publish-ghcr` in `/root/arifOS/` to build and push Docker image to GHCR.

## Current Makefile State
The `VERSION=` override is already hardcoded in the Makefile:
```makefile
publish-ghcr:
	@VERSION=2026.05.01; \
	docker build -t ghcr.io/ariffazil/arifos:$$VERSION . && \
	...
```
No `cut` delimiter workaround is needed — it works as-is.

If bumping version: update the `VERSION=` line in the Makefile AND update the Dockerfile comment label.
## Standard publish steps

1. **Update version** in `pyproject.toml` (`version` field) to today's date `YYYY.MM.DD`
2. **Update version** in `arifosmcp/__init__.py` (`__version__`) — keep `-KANON` suffix for canonical-lock releases
3. **Commit:** `git add . && git commit -m "chore: version bump to YYYY.MM.DD" && git push origin main`
4. **Verify pre-commit passes** (all hooks must green before pushing)
5. **Build + push container:** `make publish-ghcr`
6. **Verify push:** check output ends with `✅ GHCR: arifos:... pushed`

## Image tags produced
- `ghcr.io/ariffazil/arifos:YYYY.MM.DD` — versioned tag
- `ghcr.io/ariffazil/arifos:latest` — alias tag

## Prerequisites
- Docker daemon running and authenticated to GHCR: `docker login ghcr.io -u ariffazil`
- GHCR package write access on `ariffazil` GitHub org
- Network access to `ghcr.io`

## Related
- `arifos-version-sync-vaul999` — version sync protocol; run this before `make publish-ghcr` to ensure all 8 surfaces are aligned
- `arifos-production-deploy-diagnosis` — diagnose post-deploy issues
- `arifos-mcp-vps-deploy` — deploy pushed image on VPS
