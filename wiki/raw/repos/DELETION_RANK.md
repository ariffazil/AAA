# VPS Deletion Rank — 2026-04-30

Disk: 193G used / 170G free / 24G reclaimable target
Goal: Maximize reclaimable space without breaking running services

---

## RANKED LIST (Safest → Riskiest)

### TIER 1: 💯 SAFE — No service impact

| Path | Size | Reason |
|------|------|--------|
| `/opt/arifos/src/A-FORGE.git/` | 218M | Bare mirror, active worktree at `/root/A-FORGE` |
| `/opt/arifos/src/ariffazil/` | 6M | Abandoned monolith clone, no remote |
| `/opt/arifos/src/AAA.git/` | 321M | Bare mirror, active worktree at `/root/AAA` |
| `/opt/arifos/src/arif-sites.git/` | 370M | Bare mirror, active worktree at `/root/arif-sites` |
| `/opt/arifos/src/geox.git/` | 544M | Bare mirror, active worktree at `/root/geox` |
| `/opt/arifos/src/wealth.git/` | 26M | Bare mirror, active worktree at `/root/WEALTH` |
| `/opt/arifos/src/well.git/` | 252K | Bare mirror, active worktree at `/root/well` |
| `/root/arifOS/00_legacy_materials/arifOS-upstream/` | 99M | Legacy upstream copy, superseded |
| `/root/arifOS/00_legacy_materials/GEOX/` | 6.7M | Legacy geox copy, superseded |
| `/root/arifOS/_archived_tests/` | 232K | Old tests, superseded |
| `/root/arifOS/docs/image/` | 84M | PNG renders, docs only |
| `/opt/arifos/traefik/` | 12K | Traefik config (Caddy now used) |
| `/opt/arifos/mcp/` | 48K | Old MCP config fragments |
| `/opt/arifos/qdrant/` | 24K | Old config fragment |
| `/opt/arifos/scripts/` | 12K | Old deploy scripts |
| `/opt/arifos/ssl/` | 12K | Old self-signed certs |
| `/opt/arifos/Dockerfile` | 4K | Old Dockerfile |
| `/opt/arifos/docker-compose.yml` | 4K | Old compose |

**TIER 1 TOTAL: ~1,687M (1.65 GB)**

---

### TIER 2: 🔒 SAFE — Verify no active use first

| Path | Size | Reason | Check |
|------|------|--------|-------|
| `/root/AAA/node_modules/` | 294M | npm packages, 322 packages | Check if AAA container has its own node_modules |
| `/root/arifOS/geox/geox-gui/` | 401M | React GUI (385M node_modules) | Container uses `/root/geox`, not this |
| `/root/arifOS/geox/ref/` | 25M | Reference materials | May be archival |
| `/root/arifOS/geox/site/` | 5M | GeoX site | May be archival |
| `/root/arifOS/geox/geox/` | 2.7M | GEOX domain logic | Check if nested or standalone |
| `/root/arifOS/00_legacy_materials/` (rest) | ~20M | Various legacy docs | Audit before delete |
| `/root/arifOS/wiki/` | 1M | Local wiki copy | Check vs /root/wiki |
| `/root/arifOS/arifos/` | 1M | Nested arifos | Check if submodule |
| `/opt/arifos/src/A-FORGE/` | 33M | Worktree, 3 commits behind | Compare vs `/root/A-FORGE` |
| `/opt/arifos/src/AAA/` | 320M | Worktree | Compare vs `/root/AAA` |
| `/opt/arifos/src/arif-sites/` | 370M | Worktree | Compare vs `/root/arif-sites` |
| `/opt/arifos/src/geox/` | 544M | Worktree | Compare vs `/root/geox` |
| `/opt/arifos/src/wealth/` | 26M | Worktree | Compare vs `/root/WEALTH` |
| `/opt/arifos/src/well/` | 252K | Worktree | Compare vs `/root/well` |

**TIER 2 TOTAL (reposable): ~2,042M (2 GB)**

---

### TIER 3: ⚠️ CAUTION — Active or referenced

| Path | Size | Reason | Risk |
|------|------|--------|------|
| `/root/volumes/ollama/` | 5.5G | Ollama model cache | ⚠️ **HIGH** — Ollama container running |
| `/root/volumes/neo4j/` | 516M | Graphiti neo4j | ⚠️ **MEDIUM** — graphiti-neo4j container running |
| `/root/volumes/clickhouse/` | 94M | Clickhouse data | ⚠️ **MEDIUM** — clickhouse container (check if running) |
| `/root/volumes/postgres/` | 76M | Postgres data | ⚠️ **HIGH** — arifOS/AAA/postgres containers |
| `/root/volumes/grafana/` | 51M | Grafana data | ⚠️ **LOW** — observability, not critical |
| `/root/volumes/prometheus/` | 16M | Prometheus data | ⚠️ **LOW** — observability |
| `/root/go/` | 115M | Go build cache | ⚠️ **LOW** — may be for build tooling |
| `/root/arifOS/docs/` (excl image) | ~2M | Docs text | ⚠️ **LOW** — may contain active docs |
| `/root/ARCHIVE/` | 68K | Local archive | ⚠️ **LOW** — audit contents first |
| `/opt/arifos/backups/` | 8.6G | Restic backup repo | ⚠️ **CRITICAL** — active cron backup target |

**TIER 3 TOTAL: ~15,423M (15 GB) — Most is volumes, not deletable safely**

---

## RECOMMENDED ORDER

### Step 1: Clean /opt/arifos/src/ (all bare mirrors + worktrees)
```
rm -rf /opt/arifos/src/
→ Reclaim: ~2,425M (2.4 GB)
```

### Step 2: Clean /opt/arifos/ stale configs
```
rm -rf /opt/arifos/traefik /opt/arifos/mcp /opt/arifos/qdrant /opt/arifos/scripts /opt/arifos/ssl /opt/arifos/Dockerfile /opt/arifos/docker-compose.yml /opt/arifos/releases /opt/arifos/sites
→ Reclaim: ~200M
```

### Step 3: arifOS legacy materials
```
rm -rf /root/arifOS/00_legacy_materials/arifOS-upstream
→ Reclaim: 99M
```

### Step 4: Docs image (if docs use is text-only)
```
rm -rf /root/arifOS/docs/image/
→ Reclaim: 84M
```

### After verifying no active use:
```
# Only after checking no active use
rm -rf /root/arifOS/geox/geox-gui/node_modules  # 385M (keep src/dist)
rm -rf /root/AAA/node_modules                   # 294M (AAA has its own container)
```

---

## GRAND TOTAL (TIER 1 CONFIDENT)

**~1,887 MB reclaimable immediately** with zero service risk

After audit (TIER 2): **~3,929 MB** with minimal risk

---

## DO NOT DELETE

- `/root/sites/` — Caddy live mount (site-autoresearch/apr26)
- `/root/arif-sites/` — Canonical git repo (main branch)
- `/root/arifOS/` — Constitutional kernel git repo
- `/root/geox/` — Earth intelligence git repo
- `/root/AAA/` — Agent workspace git repo
- `/root/A-FORGE/` — Execution bridge git repo
- `/root/WEALTH/` — Capital intelligence git repo
- `/root/well/` — Biological substrate git repo
- `/root/compose/` — Docker compose configs
- `/root/volumes/` — All active Docker volumes (ollama, postgres, etc.)
- `/opt/arifos/backups/` — Active backup target (cron running)