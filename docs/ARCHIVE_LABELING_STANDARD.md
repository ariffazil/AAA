# ARCHIVE LABELING STANDARD — arifOS Federation

> **Ratified:** 2026-07-26 | **Authority:** ARIF / F13 SOVEREIGN  
> **Standard:** GitHub-compatible archive conventions for federation repos  
> **Rule:** Every archive must declare its own death.

---

## Naming Convention

| Pattern | Use Case | Example |
|---------|----------|---------|
| `ARCHIVE-YYYY-MM-DD-<kebab-case>/` | Archived projects, repos, major directories | `ARCHIVE-2026-07-13-apex-legacy/` |
| `_archive/YYYY-MM-DD-<descriptor>/` | Orphaned projects, snapshots | `_archive/2026-07-25-orphaned-projects/` |
| `ARCHIVE-<name>/` (in `_retired/`) | Retired skills | `_retired/ARCHIVE-code-wiki/` |
| `_legacy/` | Web surfaces, pre-unification | `arif-sites/_legacy/` |
| `.archive-YYYY-MM/` | Hidden archives, memory dumps | `memory/.archive-2026-07/` |

## Required Files Per Archive

Every archive directory containing doctrinal, architectural, or constitutional content MUST include:

```
<archive-dir>/
├── .github/ARCHIVE_METADATA.json   ← machine-readable archive manifest
└── README.md (optional)            ← ⚠️ ARCHIVED banner for humans
```

### ARCHIVE_METADATA.json Schema

```json
{
  "archived": "YYYY-MM-DD",
  "reason": "Why this was archived (1-2 sentences)",
  "superseded_by": {
    "component": "path or URL to live replacement"
  },
  "retention_policy": "KEEP_INDEFINITELY | KEEP_UNTIL_<condition> | COLD_STORAGE | PURGE_AFTER_<date>",
  "eureka_distilled": ["List of insights extracted"],
  "last_accessed": "YYYY-MM-DD",
  "read_only": true,
  "classification": "DOCTRINE | OPERATIONAL | NOISE | BACKUP"
}
```

## Retention Policy Tiers

| Tier | Policy | Applies To |
|------|--------|------------|
| **KEEP_INDEFINITELY** | Never delete. Constitutional origin. | Autobiographical docs, scar maps, EUREKA seals, genesis docs |
| **KEEP_UNTIL_MIGRATION_VERIFIED** | Delete after confirmed migration to live. | APEX formula v1→v2, old skill implementations |
| **COLD_STORAGE** | Archive as tarball. Delete directory. | Bulk copies (>1000 files), pre-consolidation noise |
| **PURGE_AFTER_<date>** | Delete after date. | Backups, config snapshots, session logs older than 90 days |

## Anti-Patterns (Forbidden)

- ❌ `EMPTY-*` — use `ARCHIVE-YYYY-MM-DD-empty/`
- ❌ `*.bak`, `*.backup`, `*.old` — stage into dated archive dir
- ❌ Archives without metadata — every archive declares its own death
- ❌ `_archive` AND `archive` AND `00_legacy` all in same repo — pick one convention per root
- ❌ Archives inside active repos without `.github/ARCHIVE_METADATA.json`

## For New Archives

When archiving a project, repo, or directory:

1. **Move** to appropriate archive location (`_archive/` or `ARCHIVE-*/`)
2. **Create** `.github/ARCHIVE_METADATA.json` with full metadata
3. **Tag** the archive commit in git: `git tag ARCHIVE-YYYY-MM-DD`
4. **Update** `FEDERATION_EUREKA_DISTILLATION_REPORT.md` if insights exist
5. **Do NOT delete** until retention policy matures

---

## Current Archive Inventory (2026-07-26)

| Location | Labeled | Classification |
|----------|:-------:|---------------|
| `/root/_archive/2026-07-25-orphaned-projects/` | ✅ | DOCTRINE |
| `/root/_archive/2026-07-25-doctrine-backups/` | ✅ | BACKUP |
| `/root/_archive/2026-07-15/` | ✅ | OPERATIONAL |
| `/root/_archive/ARCHIVE-2026-07-12-empty/` | ✅ | NOISE |
| `/root/_archive/ARCHIVE-2026-07-12-empty-dot/` | ✅ | NOISE |
| `/root/_archive/hermes-rsi-2026-06-22/` | 🔲 | OPERATIONAL |
| `/root/_archive/void-false-positives-2026-06-26/` | ✅ | OPERATIONAL |
| `/root/A-FORGE/archive_apex_legacy_2026-07-13/` | ✅ | DOCTRINE |
| `/root/AAA/archive/` | ✅ | DOCTRINE |
| `/root/AAA/_archive/` | 🔲 | OPERATIONAL |
| `/root/memory/archive/` | 🔲 | OPERATIONAL |
| `/root/memory/.archive-2026-07/` | ✅ | DOCTRINE |
| `/root/arifOS/archive/` | 🔲 | OPERATIONAL |
| `/root/arifOS/00_legacy_materials/` | ✅ | NOISE |
| `/root/arif-sites/_legacy/` | 🔲 | OPERATIONAL |
| `/root/arif-sites-legacy/` | 🔲 | OPERATIONAL |
| `/root/.agents/skills/_retired/` (28 skills) | ✅ | OPERATIONAL |
| `/root/.agents/skills-archive/` (83 skills) | 🔲 | DOCTRINE |
| `/root/.openclaw/_archive/` | 🔲 | BACKUP |
| `/root/.backups/prompts-archive-2026-07-03/` | 🔲 | BACKUP |
| `/root/.archive/` | ✅ | DOCTRINE |
| `/root/.bash_archive/` | 🔲 | OPERATIONAL |

**✅ 12 of 22 labeled. 🔲 10 remaining — non-critical, can complete in next pass.**

---

*DITEMPA BUKAN DIBERI — Archives are sealed past. Every archive declares its own death.*