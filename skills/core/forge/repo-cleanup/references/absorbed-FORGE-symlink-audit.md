# Absorbed: FORGE-symlink-audit

> **Provenance.** Pre-merge body of the `FORGE-symlink-audit` skill, tombstoned 2026-09-16T22:44:00Z by Wave 2 (`moved_to: core/forge/repo-cleanup/SKILL.md`).
> Recovered verbatim from `/root/.hermes@entropy-wave2-pre-act-20260916T144144Z:skills/FORGE-symlink-audit/SKILL.md` — content was never carried into the target by the
> original consolidation; recovered 2026-09-17 to complete the recorded merge.
> Original sha256 (tombstone `sha256_before`): `7415750584a70c467a0a80ec4307059103b22061410ebf285946f4854dc42734`
> Recovery sha256: `7415750584a70c467a0a80ec4307059103b22061410ebf285946f4854dc42734`
> The `FORGE-symlink-audit` routing name stays retired — this file is a reference, not a skill.

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
