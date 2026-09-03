# Docker Disk Investigation Sequence

## Trigger

Disk alert (93%+ or similar) on a machine running Docker. 32GB vanished in ~11h.

## Investigation Sequence (in order)

### Step 1: Top-level overview
```bash
df -h /                          # overall disk: used/total/%
du -sh /* 2>/dev/null | sort -rh | head -30  # biggest top-level dirs
```

### Step 2: Identify Docker as the consumer
```bash
du -sh /var/lib/docker/* 2>/dev/null | sort -rh | head -10
```
Usually `/var/lib/docker/rootfs` (overlayfs) or `/var/lib/docker/buildkit`.

### Step 3: Docker space accounting
```bash
docker system df
# Output: Images | Containers | Local Volumes | Build Cache + reclaimable sizes
```

### Step 4: Image inventory
```bash
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}} {{.CreatedSince}}" | sort -k3 -r
```
Look for: many recent tags of the same repo (build churn), large images (≥5GB), dangling `<none>` images.

### Step 5: Running containers vs images
```bash
docker ps --format "{{.Names}}\t{{.Image}}\t{{.Status}}"
```
Only prune images NOT used by running containers.

### Step 6: Build cache audit
```bash
docker builder df 2>/dev/null | head -20  # buildkit cache
# Or: du -sh /var/lib/docker/buildkit/*
```

## Common Root Causes

| Cause | Evidence | Fix |
|-------|----------|-----|
| **Image tag accumulation** (many builds → many tags) | 7+ geox variants, 4+ arifos variants, all recent | `docker image prune --filter "until=24h"` (dangling only) or targeted `docker rmi` of old tags |
| **Build cache bloat** | Build Cache ≥ 40GB, RECLAIMABLE high | `docker builder prune --filter "until=24h"` (buildkit) or full `docker builder prune -a` |
| **Log explosion** | `/var/lib/docker/containers/` large, many log files | `docker container prune -f` (stops containers first if needed) |
| **Overlayfs grow** | `/var/lib/docker/rootfs/overlayfs/` large | Usually active container layers; investigate what container |
| **Volume bloat** | `/var/lib/docker/volumes/` large | `docker volume prune -f` |

## Reclaimable by Category

```
Images:      27.81GB reclaimable (23% of 117.4GB total)
Build Cache: 19.86GB reclaimable (of 45.32GB total)
```

## Targeted Prune (Safe, no system prune)

```bash
# Dangling images only (safe, no running container impact)
docker image prune -f

# Specific old tags not used by any running container
# e.g. old geox/arifos variants
docker rmi ghcr.io/ariffazil/geox:a6a5177e ghcr.io/ariffazil/arifos:c18880a1

# Build cache older than 24h
docker builder prune --filter "until=24h"
```

## DO NOT RUN without 888_HOLD

```bash
docker system prune -a   # Removes ALL unreferenced images, build cache, more
# HIGH RISK — will break running containers if they reference pruned images
```

## Signs of Build Churn (this session's pattern)

- 11 new geox images in 13 hours (5.35GB each = ~58GB raw, shared layers reduce)
- 4 arifos images in 12 hours (9.23GB each)
- Shared layers mean actual unique size is less than sum
- `geox_eic` container running `f73d39b9` — only one geox image actively in use
- Build cache at 45GB with 19.86GB reclaimable

## Key Nuances from Session (2026-05-18)

### `--filter "until=24h"` on `docker image prune` is ineffective for old tags
- `docker image prune --filter "until=24h"` → prompts interactively (blocked, exit 125)
- `docker image prune -f` → bypasses confirmation, works correctly
- Result: 208MB reclaimed (dangling image `1a9db4d22d87`)

### Sequence that worked:
```bash
# Step 1: prune dangling images (safe — no running container impact)
docker image prune -f
# Output: "Total reclaimed space: 208.5MB"

# Step 2: immediately verify disk
df -h /

# Step 3: verify containers still healthy
docker ps --format "{{.Names}} {{.Image}} {{.Status}}"
```

### Build cache reclaim:
- Build cache showed 45.32GB total / 19.86GB reclaimable
- After image prune: Build Cache dropped to 0B (co-reclaimed with image removal)
- Total reclaim: ~45GB across images + cache
- Before: 179G used / 93% | After: 134G used / 70%

### Root cause pattern confirmed:
- 11 new geox images in ~13h (5.35GB each × 7 active tag variants)
- 4 arifos images in ~12h (9.23GB each × 4 tag variants)
- Shared layers reduce actual unique size but accumulated fast
- Build cache bloat added to the pressure

### 888_HOLD behavior observed:
- `docker system prune -a` correctly blocked (requires 888_JUDGE verdict + human ack)
- Targeted `docker image prune -f` ran autonomously (dangling = reversible re-pull)

## Session-Specific Data (2026-05-18)

- Root cause: frequent geox/arifos builds → image accumulation
- Active containers: 26 running, none crashed
- 35GB in overlayfs (active container layers, not reclaimable)
- Dangling image: 1.12GB (`1a9db4d22d87`) — safe to prune
- Old unreferenced geox tags (a6a5177e): ~5.9GB unique — safe to prune
- Old unreferenced arifos tags (c18880a1): ~47MB unique — safe to prune
- Build cache: 19.86GB reclaimable via `docker builder prune`