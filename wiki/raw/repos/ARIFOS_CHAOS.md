# VPS Architecture Audit — 2026-04-30

## Root Cause: The Chaos

Multiple overlapping copies of the same repos across `/root/` and `/opt/arifos/src/`, with symlinks and divergent git states creating confusion about which is canonical.

---

## Architecture Map

### Layer 1: Production Live (Docker Compose at `/root/compose/`)

Running containers derived from `/root/compose/docker-compose.yml`:

| Container | Image | Source | Status |
|-----------|-------|--------|--------|
| arifosmcp | `ghcr.io/ariffazil/arifos:7ddc9ffc` | Built from `/root/arifOS/` | Up (healthy) |
| postgres | postgres:16-alpine | /root/volumes/postgres | Up |
| qdrant | qdrant/qdrant:latest | /root/volumes/qdrant | Up |
| redis | redis:7-alpine | /root/volumes/redis | Up |
| caddy | caddy:2-alpine | /root/arifOS/Caddyfile | Up |
| ollama | ollama/ollama:latest | /root/volumes/ollama | Up |
| aaa | compose-aaa:latest | /root/AAA | Up |
| geox | fa108ca1e65e | /root/geox | Up |
| well | ghcr.io/ariffazil/well:latest | /root/well | Up |
| wealth-organ | compose-wealth-organ:latest | /root/WEALTH | Up |
| af-bridge-prod | a-forge-af-bridge | /root/A-FORGE | Up |

**Canonical source for running system:** `/root/arifOS/`, `/root/AAA/`, `/root/geox/`, `/root/well/`, `/root/WEALTH/`, `/root/A-FORGE/`

---

### Layer 2: Production Deploy Pipeline (`/opt/arifos/`)

| Path | Purpose | Status |
|------|---------|--------|
| `/opt/arifos/docker-compose.yml` | FHS-aligned compose (references `/root/arifOS` via `/root/arifos` symlink → broken) | **STALE — not used** |
| `/opt/arifos/deploy_kernel.sh` | References `/root/arifOS` via broken symlink | STALE |
| `/opt/arifos/src/` | Working clones of repos (1.5G) | STALE — diverges from /root |
| `/opt/arifos/backups/restic/` | Restic backup repo (8.6G) | ACTIVE — running daily |
| `/opt/arifos/backups/backup-volumes.sh` | Volume backup cron script | ACTIVE |
| `/opt/arifos/secrets/` | Cloudflare token, governance.secret | ACTIVE |
| `/opt/arifos/releases/` | Site tarballs from Apr 23 | ORPHANED |
| `/opt/arifos/sites/` | Static site files | ORPHANED |
| `/opt/arifos/ssl/` | TLS config | ACTIVE (Caddy handles TLS) |
| `/opt/arifos/traefik/` | Traefik config (Caddy now used instead) | ORPHANED |
| `/opt/arifos/qdrant/` | Qdrant config (bind-mounted to /root/volumes/qdrant) | ACTIVE |
| `/opt/arifos/mcp/` | MCP config fragments | ACTIVE |

---

### Layer 3: Symlink Chaos

```
/root/arifos -> /opt/arifos/src/arifOS    ← BROKEN (src/arifOS doesn't exist)
/root/arifOS/  ← REAL canonical (git repo, .git is a directory)
/opt/arifos/src/ariffazil  ← clone of ariffazil/ariffazil.git
/opt/arifos/src/arifOS     ← DOES NOT EXIST
```

---

### Git State Comparison

| Repo | `/root/` | `/opt/arifos/src/` | Diverged? |
|------|----------|-------------------|-----------|
| arifOS | `7ddc9ffc` (main) | ❌ Not present | N/A |
| A-FORGE | `a4fff29` | `5e70483` | **YES — 3 commits behind** |
| AAA | — | `7c8ad47` (main) | N/A (root/AAA is apex branch) |
| geox | `main` | `main` | SYNCED |
| well | `0126b6d` | `893517c` | **YES — root is ahead** |
| WEALTH | `main` | `main` | SYNCED |
| arif-sites | `main` | `main` | SYNCED |
| ariffazil (monolith) | — | `d36611b` | N/A |

---

## Deletion Plan

### SAFE TO DELETE (no active use, redundant, or orphaned):

1. **`/opt/arifos/releases/`** (1.6M) — Site tarballs from Apr 23, superseded by current site
2. **`/opt/arifos/traefik/`** (12K) — Traefik config, Caddy is now reverse proxy
3. **`/opt/arifos/mcp/`** (48K) — Old MCP config fragments, superseded by root/A-FORGE
4. **`/opt/arifos/qdrant/`** (24K) — Config fragment, actual qdrant runs via /root/compose
5. **`/opt/arifos/scripts/`** (12K) — Old deploy scripts, superseded by /root/arifOS/Makefile
6. **`/opt/arifos/src/A-FORGE.git/`** (218M) — Bare mirror, redundant with `/opt/arifos/src/A-FORGE/`
7. **`/opt/arifos/src/ariffazil/`** (6M) — Monolith src clone, not referenced by any running service

### KEEP (active backups or configs):

- `/opt/arifos/backups/` (8.6G restic) — **active daily backup**
- `/opt/arifos/secrets/cloudflare_token` — used by Caddy
- `/opt/arifos/docker-compose.yml` — references `/root/arifOS` build context, might be revived
- `/opt/arifos/deploy_kernel.sh` — references `/root/arifOS`
- `/opt/arifos/ssl/` — TLS storage
- `/opt/arifos/sites/` (108K) — static site content (check if /root/sites is same)

### INVESTIGATE BEFORE DELETE:

- `/opt/arifos/src/AAA` — might be a backup of apex/seal-fusion branch
- `/opt/arifos/src/well` — 252K, root/well is more current
- `/opt/arifos/src/arif-sites` — synced but check vs /root/arif-sites

---

## Orphaned Volumes (not from /root/compose)

These volumes exist but aren't referenced by any running compose stack:

- `compose_ollama_data` → `/root/volumes/ollama` (5.5G — active, in use)
- `af-forge_*` → from old a-forge compose
- `geox_vault_999` → referenced but maybe duplicated

---

## Actions

1. Delete releases/, traefik/, mcp/, qdrant/, scripts/ from /opt/arifos/
2. Delete /opt/arifos/src/A-FORGE.git (bare mirror)
3. Delete /opt/arifos/src/ariffazil (monolith clone)
4. Verify /opt/arifos/sites vs /root/sites overlap before deleting
5. Keep backups, secrets, docker-compose.yml, deploy_kernel.sh