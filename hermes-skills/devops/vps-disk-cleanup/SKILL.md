---
name: vps-disk-cleanup
description: arifOS VPS disk cleanup workflow — diagnose before delete, handle stopped containers, distinguish named volumes from bind mounts
tags: [docker, disk, maintenance, arifOS-VPS]
version: 2026-04-30
---

# VPS Disk Cleanup Workflow

## Trigger
Disk >90% on arifOS VPS (or routine maintenance).

## Principles
1. **Verify before deleting** — never trust an analysis that doesn't use `docker ps` and `docker images`
2. **Named volumes vs bind mounts** — containers may use bind mounts (`/root/volumes/`) while Docker reports named volumes as orphaned. Always cross-check.
3. **Stopped containers hold image references** — an Exited container can block `docker rmi`. Must `docker rm` first.
4. **Images may already be deleted** — if `docker rmi` returns "No such image", fine, move on.

## Step 1 — Diagnose (always run first)
```bash
df -h /
docker system df
docker images ghcr.io/ariffazil/arifos:* --format "{{.Tag}}\t{{.Size}}"
docker ps --format "{{.Image}}\t{{.Status}}"
```

## Step 2 — Identify in-use vs orphaned
- Running containers → in-use
- `docker images` tags present in `docker ps` → in-use
- All others → verify no stopped containers reference them

```bash
docker ps -a --format "{{.ID}}\t{{.Image}}\t{{.Status}}" | grep <tag>
```

## Step 3 — Delete in correct order
```bash
# 1. Remove stopped containers blocking image deletion
docker rm <container_id>

# 2. Delete unused image tags (skip in-use: latest, a-forge, and any tag in docker ps)
docker rmi --force \
  ghcr.io/ariffazil/arifos:<tag1> \
  ghcr.io/ariffazil/arifos:<tag2> \
  ...

# 3. Prune build cache
docker builder prune -f

# 4. Prune dangling images
docker image prune -f --filter "dangling=true"
```

## Step 4 — Volume audit
```bash
docker volume ls
docker system df -v  # shows volumes with LINKS=0 = orphaned
```

**Named volumes with LINKS=0 are safe to remove** (unless bind mounts are in use via `/root/volumes/`).

```bash
docker volume rm <vol1> <vol2> ...
```

## Step 5 — Workspace cruft
```bash
du -sh /opt/arifos/data /root/go /root/A-FORGE /root/AAA /root/arif-sites-work
```

**Known decommissioned paths (safe to rm without asking):**
- `/opt/arifos.bak.20260505/` — **DECOMISSIONED** (30GB restic backup repo from May 5). Backup script exists but live system uses GHCR + Docker volumes. **Safe to `rm -rf` immediately.** Reclaims 30GB in one shot.
- `/opt/arifos/data/` — **DECOMISSIONED** (replaced by `/root/volumes/`). 5.5GB, safe to `rm -rf`.
- `/root/go/pkg/mod/` — **ORPHANED** (2.5GB). No `go` binary exists in `/root/go/bin/`. Go module cache is only needed to BUILD Go projects, not run them. Safe to `rm -rf`. Keep `/root/go/bin/` — 8 tools (wacli, blogwatcher, sonos, eightctl, gifgrep, blu, ordercli, xcaddy) are all actively in use via `$PATH`.

**Paths needing human review before touching:**
- `/archive/` (8.7GB) — contains `ARCHIVE_SYSTEM_2026/LEGACY_CHAOS` (5.8GB) + `repo-snapshots/` (2.9GB). LEGACY_CHAOS name suggests mixed old state. **Ask Arif before deleting.**
- `/var/lib/containerd/` (59GB!) — Containerd snapshotter on a Docker-hosted VPS. Usually old image layers from when machine ran containerd workloads directly. **Do NOT prune without confirming no k3s/cri/containerd containers running.** Check: `crictl ps 2>/dev/null` or `nerdctl ps 2>/dev/null`.
- `/snap/` (5.6GB) — Snap packages. `snap list` to see what's installed. Usually safe to `snap remove` old revisions.

**Check before touching:**
- `/root/A-FORGE/` and `/root/AAA/` — old workspaces (187MB and 466MB). Check if canonical repos are on GitHub (`ariffazil/A-FORGE`, `ariffazil/AAA`). If yes and local dirs are identical copies, safe to rm.
- `/root/arif-sites-work/` — usually active WIP with recent commits, check first.

**Critical distinction this session (2026-04-30):**
- `/root/volumes/` = bind mounts used by LIVE containers (ollama, postgres, neo4j, qdrant, caddy)
- Docker named volumes (`docker volume ls`) = orphaned (LINKS=0), ALL safe to prune
- **The machine analysis wrongly said `latest` tag was unused — it IS running** (docker ps confirmed). Always verify with `docker ps`, not just image listing.

## Step 6 — Git shallow (optional, arifOS only)
```bash
cd /root/arifOS
# Check history depth
git rev-list --count --all
# Shallow to last 5 commits (safe for push/pull, breaks bisect/history)
git repack -ad
# Or: git gc --prune=now --aggressive
```

**Risk:** Breaks `git bisect`, `git log --all`. Only do if repo is deploy-only.

## Verification
```bash
df -h /
docker system df
```

## Post-Cleanup: Tag Known-Good Images
After major image pruning, tag live images with a clean timestamp so future audits can distinguish old vs fresh:
```bash
# Tag current live images as restore points
docker tag ghcr.io/ariffazil/arifos:latest ghcr.io/ariffazil/arifos:SEAL-clean-$(date +%Y%m%d)
docker tag ghcr.io/ariffazil/wealth:latest ghcr.io/ariffazil/wealth:SEAL-clean-$(date +%Y%m%d)
docker tag ghcr.io/ariffazil/well:latest ghcr.io/ariffazil/well:SEAL-clean-$(date +%Y%m%d)
# Push if you want restore points in GHCR
docker push ghcr.io/ariffazil/arifos:SEAL-clean-$(date +%Y%m%d)
```

## Telegram Group Audit (OpenClaw Gateway)
When auditing which Telegram groups the @AGI_ASI_bot can reach:
```bash
# Bot info
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"

# Check if bot is member of a group
curl -s "https://api.telegram.org/bot<TOKEN>/getChat?chat_id=<GROUP_ID>"

# OpenClaw config groups are in:
grep '"groups"' /root/.openclaw/openclaw.json
# Add missing group IDs to groups{} block with "requireMention": false

# Verify bot can send to group directly
curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<GROUP_ID>" -d "text=Test message"
```

**Critical config structure for OpenClaw Telegram groups:**
- `groupPolicy: allowlist` — only listed groups are allowed
- `groups{}` — individual group IDs with `requireMention: false`
- `groupAllowFrom[]` — sender IDs allowed to trigger in groups (Arif: `267378578`)
- Missing group = silently ignored by OpenClaw

**To add a new group:** edit `/root/.openclaw/openclaw.json`, add the group ID to `groups{}`, restart: `systemctl --user restart openclaw-gateway.service`

## Critical distinction this session (2026-04-30):
- `/root/volumes/` = bind mounts used by LIVE containers (ollama, postgres, neo4j, qdrant, caddy)
- Docker named volumes (`docker volume ls`) = orphaned (LINKS=0), ALL safe to prune
- **The machine analysis wrongly said `latest` tag was unused — it IS running** (docker ps confirmed). Always verify with `docker ps`, not just image listing.
- **Docker and containerd are SEPARATE storage subsystems** — this VPS has both. `docker system df` only shows Docker. Use `df -h /var/lib/containerd` to check containerd separately.

## Disk Diagnosis — Quick Sweep (2026-05-11)
Top-level breakdown:
```bash
df -h /
du -h --max-depth=1 /root | sort -rh
docker system df
```
Then drill into outliers:
```bash
du -h --max-depth=2 /root/AAA | sort -rh | head -25  # AAA = 44G, main target
du -ah /root/AAA/.hermes/venv/lib/python*/site-packages/ | sort -rh | head -20  # GPU packages in venv?
du -sh /root/AAA/.openclaw/plugin-runtime-deps/* | sort -rh  # OpenClaw plugin versions
```

**Key findings from 2026-05-11:**

**Hermes venv GPU packages — verified removable:**
- `hermes-a2a.py` (host relay) uses ONLY stdlib: `http.server`, `json`, `uuid`, `requests`, `asyncio`, `websockets`
- Zero torch, CUDA, or GPU imports
- 6G venv: ~4.5G is GPU packages (nvidia/cu13 1.7G, torch 1.2G, triton 641M, cudnn 471M, nvidia/cusparselt 223M, nvidia/nccl 209M)
- Hermes Agent Docker container handles all actual inference
- **Confirmed safe to `rm -rf /root/AAA/.hermes/venv`** — requires F1 override + sovereign confirmation

**OpenClaw plugin-runtime-deps — verified live:**
- Both `/root/.openclaw/plugin-runtime-deps/` and `/root/AAA/.openclaw/plugin-runtime-deps/` share same inode (hard link / bind mount)
- Single version: `openclaw-2026.4.29-4eca5026e977` — matches running gateway version (2026.4.29)
- **KEEP** — not stale

**Disk growth tracking:**
- May 9: ~63%
- May 11: ~74% (11G jump in 2 days)
- Primary driver: AAA at 44G (hermes venv 6G, openclaw plugin 4.6G, kimi sessions 440M, copilot session-state 542M)

## NATS Container — Standalone Docker (Not Compose)
**Discovery (2026-05-11):** NATS was started via `docker run` standalone, NOT via docker-compose. Always check:
```bash
docker ps --format "{{.Names}} {{.Image}}" | grep nats
ss -tlnp | grep 4222
```
If NATS appears in `docker ps` but NOT in `docker compose ps`, it is a standalone container — fix via host config file + container restart, not compose.

**NATS config location inside container:** `docker cp nats:/nats-server.conf /tmp/nats-check.conf`

**Hardened NATS config must have:**
```conf
port: 4222
authorization {
  user: nats_client
  password: <random-secure-password>
  timeout: 5
}
monitor_port: 127.0.0.1:8222  # bind to localhost
cluster { port: 6222; authorization { user: ruser; password: T0pS3cr3t; timeout: 2 }; routes = [] }
```

Restart with localhost binding:
```bash
docker stop nats && docker rm nats
docker run -d \
  --name nats --restart unless-stopped \
  -p 127.0.0.1:4222:4222 \
  -p 127.0.0.1:8222:8222 \
  -v /etc/nats/nats-server.conf:/nats-server.conf \
  nats:latest --config nats-server.conf
```

**C4 Critical — requires sovereign approval before executing.**
