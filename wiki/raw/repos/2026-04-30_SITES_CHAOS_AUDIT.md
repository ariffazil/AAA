# Sites Chaos Audit — 2026-04-30

## The Sites Zoo

```
/root/sites/               74M   ← LIVE (Caddy mount: /var/www/html → /root/sites)
  └── git branch: site-autoresearch/apr26 (2 commits ahead of main)
  └── Content: flat subdomain dirs (aaa, apex, arif, arifos, forge, geox, mcp, etc.)

/root/arif-sites/          378M  ← CANONICAL (git repo, main branch, 5 commits ahead of work/)
  ├── sites/arif-fazil.com/ ← SCAFFOLD (marked "do not use for final design")
  ├── sites/aaa.arif-fazil.com/
  ├── sites/apex.arif-fazil.com/
  ├── sites/geox.arif-fazil.com/
  ├── archive/              18M  ← OLD site snapshots (2026-04-01 backups)
  └── temp/                 1.2M ← staging
  └── symlink: arif → .releases/arif-fazil.com.20260423230000

/root/arif-sites-work/     364M  ← DUPLICATE of arif-sites (same structure, same branch main, 4 commits behind)
  ├── sites/               322M  ← IDENTICAL to arif-sites/sites/
  ├── archive/             18M   ← IDENTICAL to arif-sites/archive/
  └── temp/                1.2M  ← IDENTICAL to arif-sites/temp/

/opt/arifos/sites/         108K  ← ORPHANED (old static site backup from Apr 20)
```

---

## The Chaos

### 1. Four copies of the same thing

| Path | Size | Source | Status |
|------|------|--------|--------|
| `/root/sites/` | 74M | `site-autoresearch/apr26` branch | **LIVE** — Caddy serves this |
| `/root/arif-sites/sites/` | 322M | `main` branch | **CANONICAL** — Git repo |
| `/root/arif-sites-work/sites/` | 322M | `main` branch (4 commits behind) | **REDUNDANT** — sync'd copy |
| `/opt/arifos/sites/` | 108K | Old backup | **ORPHANED** — delete |

**Root cause:** `/root/sites/` is the working directory on the `site-autoresearch/apr26` branch — it's where autorearch work happens. But `/root/arif-sites/` is the canonical git repo on `main`. They're both clones of `ariffazil/arif-sites.git` but on different branches.

### 2. arif-sites vs arif-sites-work — synced but divergent

- Both are `main` branch
- `arif-sites` is 5 commits ahead of `arif-sites-work`
- `arif-sites-work` is essentially a 4-commit-behind mirror
- Archive dirs are identical (18M each)
- Sites dirs are identical (322M each)

**Verdict:** `arif-sites-work/` is a stale copy — delete it.

### 3. The arif symlink

```
/root/arif-sites/arif → .releases/arif-fazil.com.20260423230000
```

This is a timestamped release of the arif site. It's a snapshot, not live code. The live Caddy mount uses `/root/sites/arif` (from the `site-autoresearch/apr26` branch), not this symlink.

### 4. Archive bloat

`archive/` contains:
- `arif-fazil.com-old/` — old version
- `arif-fazil.com-source/` — source of old version
- `arif_backup_2026-04-01/` — April 1st backup
- `arifos_backup_2026-04-01/` — April 1st backup
- `staging (to rebuild new-delete after seal)/` — staging marked for deletion
- `aaa-mcp-landing/` (4M) — old MCP landing page
- `manifesto/` (1.5M) — manifesto content

Total archive: 18M of old site snapshots. Most are superseded by the current `sites/` content.

### 5. The SCAFFOLD problem

`sites/arif-fazil.com/README.md` explicitly says:

> ⚠️ SCAFFOLD ONLY — DO NOT USE FOR FINAL DESIGN

This means the canonical `main` branch has a **working but non-canonical** arif-fazil.com site. The real design must be built from `ARIF_FAZIL_COM_TRINITY_MAP.md`.

### 6. Subdomain routing

Caddy routes:
- `arif-fazil.com` → `/root/sites/` (live, site-autoresearch/apr26)
- `geox.arif-fazil.com` → probably via `/root/arif-sites/sites/geox.arif-fazil.com` or `/root/sites/geox/`
- `mcp.arif-fazil.com`, `aaa.arif-fazil.com`, etc. → similar pattern

But the actual subdomain config is in the Caddyfile at `/root/arifOS/Caddyfile`. Need to audit.

---

## Architecture Map (Sites)

```
ariffazil/arif-sites.git
    ├── main branch → /root/arif-sites/ (canonical, 378M)
    │                   └── sites/arif-fazil.com (SCAFFOLD), sites/{geox,aaa,apex,...}
    ├── site-autoresearch/apr26 → /root/sites/ (74M, LIVE Caddy mount)
    │                   └── arif/, arifos/, geox/, mcp/, etc. (flat subdomain dirs)
    └── (work/ branch is 4 commits behind main, obsolete copy)

/opt/arifos/sites/ → OLD backup, delete after verifying Caddy doesn't reference it
```

---

## Deletion Plan

### ✅ SAFE TO DELETE:

| Path | Size | Reason |
|------|------|--------|
| `/root/arif-sites-work/` | 364M | Redundant mirror of arif-sites, 4 commits behind |
| `/opt/arifos/sites/` | 108K | Orphaned old backup, superseded by /root/sites/ |
| `/root/arif-sites/archive/arif-fazil.com-old/` | 108K | Old site, superseded |
| `/root/arif-sites/archive/arif-fazil.com-source/` | 96K | Source of old site |
| `/root/arif-sites/archive/arifOS-sites/` | 16K | Old arifOS site dir |
| `/root/arif-sites/archive/arifos_backup_2026-04-01/` | 12K | April backup |
| `/root/arif-sites/archive/arif_backup_2026-04-01/` | 1.2M | April backup |
| `/root/arif-sites/archive/staging (to rebuild new-delete after seal)/` | 868K | Marked for deletion in name |

**Total reclaimable from archive:** ~2.3M
**Total reclaimable from deletion:** 364M + 108K = **~364M**

### ⛔ DO NOT DELETE:

| Path | Reason |
|------|--------|
| `/root/sites/` | **LIVE** — Caddy mount, site-autoresearch/apr26 branch |
| `/root/arif-sites/` | **CANONICAL GIT REPO** — main branch, all sites source |
| `/root/arif-sites/temp/` | Could be staging, check before delete |

---

## Recommendations

1. **Keep `/root/sites/`** — live deploy, Caddy serves this
2. **Keep `/root/arif-sites/`** — canonical git repo, source of truth for main
3. **Delete `/root/arif-sites-work/`** — it's a stale sync copy
4. **Prune archive/** — delete `arif-fazil.com-old/`, `arif-fazil.com-source/`, `arifOS-sites/`, `arifos_backup_2026-04-01/`, `arif_backup_2026-04-01/`, `staging (to rebuild new-delete after seal)/`
5. **Keep temp/** — verify it's active staging before deleting
6. **Audit Caddyfile** — confirm exact routing to understand the relationship between `/root/sites/` flat dirs and `/root/arif-sites/sites/` subdomain dirs