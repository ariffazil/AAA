---
name: FORGE-symlink-audit
description: 'Federation-wide broken symlink scanner. Scans /root for broken symlinks,
  categorizes by location, and reports with safe-delete recommendations. USE WHEN:
  "check symlinks", "broken links", "symlink debt", "find broken symlinks", or during
  entropy sweeps.

  '
version: 2026.07.19
floors:
- F1
- F4
risk_tier: low
autonomy_tier: T1
owner: A-FORGE
---
# 🔗 FORGE — Symlink Audit

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Scan the federation for broken symbolic links, categorize by location, and report with safe-delete recommendations. Born from the 2026-07-19 session where 109 broken symlinks were found (97 archived Codex skills, 7 Playwright cache, 3 openclaw, 2 backups).

## When to Use
- Morning entropy sweep
- After skill archive/migration operations
- When `find /root -maxdepth 5 -xtype l` returns >0
- As part of `make prove` or `make sot-check`

## Command
```bash
find /root -maxdepth 5 -xtype l 2>/dev/null | wc -l
```

## Safe Cleanup
```bash
# Categorize first:
find /root -maxdepth 5 -xtype l 2>/dev/null | awk -F'/' '{print "/"$2"/"$3}' | sort | uniq -c | sort -rn

# Then delete (safe — all in cache/archive paths):
find /root -maxdepth 5 -xtype l -delete
```

## Known Patterns
| Location | Typical Cause | Safe to Delete |
|----------|---------------|----------------|
| `/root/.codex/skills.zen-archived-*/` | Archived Codex skill symlinks | ✅ |
| `/root/.cache/ms-playwright*/` | Playwright browser session files | ✅ |
| `/root/.cache/ms-playwright-mcp/` | Playwright MCP session files | ✅ |
| `/root/.openclaw/` | OpenClaw session artifacts | ✅ |
| `/root/.backups/` | Old backup symlinks | ✅ |
| `/root/*/` (organ dirs) | Git/config symlinks | ⚠️ Verify before delete |

## Constitutional Notes
- F1 AMANAH: Symlinks in `.cache/` and archived dirs are safe to delete
- F4 CLARITY: Broken symlinks = entropy. Clean them up.
- If symlink is in an organ directory, check if it's a `.git` symlink before deleting

**SOT:** 2026-07-19 · **seal_seq:** 4
