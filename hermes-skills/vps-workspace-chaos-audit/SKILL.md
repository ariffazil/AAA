---
name: vps-workspace-chaos-audit
description: Audit /root filesystem for workspace chaos — broken symlinks, ghost placeholder dirs, same-repo duplicates, giant files, and case-confused directories. Trigger when Arif says "organize", "audit", "clean up" the VPS workspace.
triggers:
  - "organize repo"
  - "no chaos no redundant"
  - "audit workspace"
  - "clean up VPS"
  - "full picture of what's on VPS"
  - "what repos are on VPS"
category: devops
---

# VPS Workspace Chaos Audit — /root Filesystem Census

## Trigger
When: Arif wants to understand what's actually on the VPS `/root` workspace — before organizing, before cleaning, before committing to any plan. **Ground truth first. Always.**

## Core principle
**DITEMPA BUKAN DIBERI** — Generate from canon. Do not trust derived claims. Curl the filesystem directly. Read the directory listings. Verify git remotes. Do not speculate from memory or prior transcripts.

## Audit Sequence

### Step 1: Broken Symlinks + Giant Files
```bash
cd /root
echo "=== BROKEN SYMLINKS ===" && find . -maxdepth 1 -type l ! -exec test -e {} \; -print 2>/dev/null
echo "=== VALID SYMLINKS ===" && find . -maxdepth 1 -type l -exec test -e {} \; -print 2>/dev/null
echo "=== GIANT FILES (>10MB) ===" && du -sh * 2>/dev/null | sort -rh | head -20
echo "=== DIRECTORY SIZES ===" && du -sh */ 2>/dev/null | sort -rh | head -30
```

### Step 2: Ghost Placeholder Dirs (Caddy web roots — empty index.html only)
```bash
echo "=== aaa/ ===" && ls -la aaa/ 2>/dev/null
echo "=== arif/ ===" && ls -la arif/ 2>/dev/null
echo "=== mcp/ ===" && ls -la mcp/ 2>/dev/null
echo "=== wawa/ ===" && ls -la wawa/ 2>/dev/null
# If each contains only index.html → these are Caddy web root ghosts, candidates for deletion
```

### Step 3: Same-GitHub Repo Duplicates
```bash
# Find all git repos
for dir in */; do
  if [ -d "$dir/.git" ]; then
    echo "=== $dir git remote ===" && (cd "$dir" && git remote -v 2>/dev/null)
  fi
done

# Check if two dirs point to same GitHub repo
# If sites/ and arif-sites/ both have origin → https://github.com/ariffazil/arif-sites.git
# Compare git HEAD commits:
diff <(cd sites && git rev-parse HEAD 2>/dev/null) <(cd arif-sites && git rev-parse HEAD 2>/dev/null)
```

### Step 4: Case-Insensitive Filesystem Check
```bash
# Linux (ext4) is case-sensitive, but git clone can create both geox/ and GEOX/
# Check if they're the same directory:
ls -la geox/ 2>/dev/null | head -1
ls -la GEOX/ 2>/dev/null | head -1
# If both show same inode → same directory (case-insensitive filesystem or git clone quirk)
```

### Step 5: Volume Contents (Docker volumes breakdown)
```bash
du -sh volumes/* 2>/dev/null | sort -rh
# Identify: live data (postgres, redis, qdrant) vs. model cache (ollama)
# 5.5GB ollama = model weights (may be pruneable if not in use)
# 517MB neo4j, 94MB clickhouse = live data (do not touch without 888_HOLD)
```

### Step 6: GitHub Repo Canonical List
```bash
curl -s "https://api.github.com/users/ariffazil/repos?per_page=100" | \
  python3 -c "import sys,json; [print(r['name'], '|', r.get('language',''), '|', r['default_branch']) for r in json.load(sys.stdin)]" | sort
```

## Classification Taxonomy

| Type | Action |
|------|--------|
| **Broken symlink** | Delete (broken link serves no function) |
| **Ghost placeholder** (empty dir with only index.html) | Delete (Caddy web root litter) |
| **Same-repo duplicate** (two dirs, same GitHub remote) | Keep canonical, archive the out-of-sync one |
| **Case-confused dir** (geox/ == GEOX/) | No action needed — Linux same-dir |
| **Giant log file** (>10MB, e.g. duplicate_files.txt) | Archive then delete |
| **Active repo** (matches GitHub canonical list) | Keep clean |
| **volumes/ Docker data** | Audit carefully — never prune without 888_HOLD |
| **Non-project tooling** (go/, go/bin/, go/pkg/) | Assess if go is actually used; if not, delete |

## Key findings from 2026-05-01 audit

### Broken symlinks found
- `arifos` → `/opt/arifos/src/arifOS` (BROKEN)
- `runtime` → `/opt/arifos/src/arifOS` (BROKEN)

### Ghost placeholders (Caddy web roots)
- `aaa/` — only `index.html` (20 bytes)
- `arif/` — only `index.html` (21 bytes)
- `mcp/` — only `index.html` (20 bytes)
- `wawa/` — only `index.html` (21 bytes)

### Same-repo duplicates
- `sites/` vs `arif-sites/` — both git remote = `https://github.com/ariffazil/arif-sites.git`, different HEAD commits (out of sync)
  - `arif-sites/` is 378MB (canonical, more complete)
  - `sites/` is 75MB (older checkout)
  - **Action:** Keep `arif-sites/`, archive `sites/`

### Case-confused directories
- `geox/` and `GEOX/` are the **same directory** (same inode) — no action needed

### Giant files
- `duplicate_files.txt` — 44MB old cleanup log — archive then delete
- `volumes/` — 6.2GB total (ollama 5.5GB, neo4j 517MB, clickhouse 94MB, postgres 76MB)

### Non-project tooling
- `go/` — 115MB Go toolchain — assess if Go is used
- `WELL/` vs `well/` — `well/` is actual project with Dockerfile/server.py; `WELL/` is in-memory state log

## Output
Write findings to `/root/WORKSPACE_CHAOS_AUDIT_YYYY-MM-DD.md` with:
1. Summary table: Canonical repos vs. chaos
2. Broken symlinks → DELETE list
3. Ghost placeholders → DELETE list  
4. Same-repo duplicates → CONSOLIDATE plan
5. Giant files → ARCHIVE then DELETE plan
6. Volumes assessment → 888_HOLD decision needed for data volumes
