---
title: "Scar — wiki Drift: /for-agents Section Missing from Source, Stale Paths, Config Deleted"
created: 2026-10-06
updated: 2026-10-06
version: 1.0.0
type: scar
status: canonical
tags: [wiki, mkdocs, drift, documentation, build-system, source-of-truth, faction-coupling]
confidence: high
domain: infra/build-system
severity: medium
actors: [fi-003]
sources: [wiki/INDEX.md, wiki/SCHEMA.md, /var/www/html/wiki, mkdocs-1.6.1]
floors: [F2, F8]
update_class: ARIF_ONLY
---

# Scar — wiki Drift: /for-agents Section Missing from Source, Stale Paths, Config Deleted

## What Happened

During 2026-10-06 16:00 MYT audit of `https://wiki.arif-fazil.com/#for-agents`:
- **Live HTML** had a `<h2 id="for-agents">` section with the llm-wiki protocol — but **NO** corresponding source `.md` file in `/root/AAA/wiki/` contained this content.
- The live HTML referenced `/root/wiki/WIKI_SCHEMA.md` — **wrong path** (actual SOT is `/root/AAA/wiki/SCHEMA.md`).
- The build config `mkdocs.yml` was **DELETED** from source — no copy existed in any backup.
- 80+ files grepped "stale dates" — all were legitimate historical incident timestamps (false positive).

## The Failure Chain

```
Phase 1 [wiki]              → 145 .md pages, 11 source directories, live HTML 2026-08-25 build
Phase 2 [audit 2026-10-06]  → /for-agents URL requested by F13
Phase 3 [drift detection]   → live HTML ≠ source MD
Phase 4 [recovery]          → Phase 1 sync (date + count + /for-agents restored)
Phase 5 [Phase 3 rebuild]   → site_dir wiped during 5 build attempts (docs_dir: .. trap)
Phase 6 [recovery #2]       → switched to absolute docs_dir, build completed in 2.85s
```

## What This Means

Three independent drift modes coexisted:

1. **Code/source drift** — `/for-agents` section existed only in stale live HTML, missing from source
2. **Path drift** — `/root/wiki/WIKI_SCHEMA.md` (old) vs `/root/AAA/wiki/SCHEMA.md` (new)
3. **Config drift** — mkdocs.yml deleted, only the build output survived

This is the **same defect class** as the broader federation drift problem (live vs source desync). The wiki was no exception.

## The False-Positive Lesson

A naive `grep -rln "2026-08-25\|2026-05-17" --include="*.md"` returned 80+ files as "stale dates". On probing context, all 80 were **legitimate historical timestamps** — scar creation dates, audit run dates, incident dates. The actual stale data was in 2 files only:
- `wiki/INDEX.md` — frontmatter `updated: 2026-08-14`
- `wiki/index.md` — same
- Plus 1 missing section (`## For Agents`)

**Lesson:** When using `grep` to find "stale" data, **always sample 5-10 hits in context** before bulk-replacing. Dates are usually history, not staleness.

## The docs_dir Trap

```yaml
# Does NOT work in mkdocs 1.6.1
docs_dir: ..  # mkdocs interprets this relative to cwd, not config-file-dir
```

```yaml
# Works
docs_dir: /root/AAA/wiki  # absolute path
```

The first form silently wipes `site_dir` during cleanup before timing out the build, leaving the wiki empty. Five failed attempts before identifying the cause.

**Lesson:** mkdocs 1.6.1 resolves `docs_dir: ..` to the parent of the **current working directory**, not the parent of the config file. Always use absolute paths for `docs_dir`.

## The Cascading Risk

If the build had succeeded silently with the wrong `docs_dir`:
- It would have built from `/root` (parent of cwd `/root/AAA`)
- It would have included unrelated files from `/root` as wiki content
- The wiki would have appeared "live" but contained federation secrets, scar evidence, terminal output

This is a **silent data exfiltration via build system misconfiguration**. Mitigated by:
1. Always using absolute `docs_dir`
2. Always specifying explicit `exclude_docs` for raw/, scar/, infrastructure/, nine-signal/, playbook/
3. Adding build-system-level gates that verify `docs_dir` is inside the source repo

## Recovery Actions Taken (Phase 1 + 3)

1. Updated `wiki/INDEX.md` frontmatter: `2026-08-14 → 2026-10-06`, `136 → 145`
2. Updated `wiki/index.md` same frontmatter + added `## For Agents` section
3. Fixed schema path: `/root/wiki/WIKI_SCHEMA.md → /root/AAA/wiki/SCHEMA.md`
4. Wrote fresh `wiki/mkdocs.yml` with absolute `docs_dir: /root/AAA/wiki`
5. Created `wiki/skills/index.md` (53 skills cataloged)
6. Built + deployed: 88 pages, 2.85s, 12 top-level tabs (was 10), 42 side-nav links (was 10)

## Reversible

```bash
cd /root/AAA
git revert aebe8701   # Phase 3 architecture
git revert d1d6ebfe   # Phase 1 sync
```

## Scar Signature (for SCAR-BINDING DOCTRINE v3)

```yaml
scar_id: SCAR_WIKI_DRIFT_2026_10_06
signature: wiki+must+drift+config+site+build
floors: [F2, F8]
consultation_count: 0
created: 2026-10-06T16:00+08:00
```