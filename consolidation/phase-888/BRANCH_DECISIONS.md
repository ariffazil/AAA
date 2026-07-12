# Branch Decisions — Phase 888 (agentic, no force-delete)

**Epoch:** 2026-07-12  
**Rule:** Archive/label only. No remote branch deletion. No force-push main.

## Policy

| Class | Action |
|-------|--------|
| ACTIVE (main) | Keep protected |
| ARCHIVE (`archive/*`, pre-consolidation) | Keep forever |
| MERGE_CANDIDATE | Leave open; merge only with CI green + explicit PR |
| EXPERIMENTAL | Leave open; do not delete; optional local archive tag if abandoned later |
| UNKNOWN_OWNER | Investigate; never delete |

## Per-repo (from BRANCH_CLASSIFICATION.json + live)

### arifOS
- `main` — ACTIVE
- `zen-migration-2026-07-11` — MERGE_CANDIDATE (current work; merge via PR when green)
- `lifecycle-kernel-v0.2-post-hold-2026-07-04` — EXPERIMENTAL keep
- `archive/pre-consolidation-2026-07-12` — ARCHIVE keep

### A-FORGE
- `main` — ACTIVE
- `docs/readme-sot-alignment-2026-06-30`, `fix/agi-tool-readiness-2026-06-24` — MERGE_CANDIDATE via PR
- `feat/document-ingest`, `forge/tool-collapse-2026-06-24` — EXPERIMENTAL keep
- `archive/pre-consolidation-2026-07-12` — ARCHIVE keep

### AAA
- `main` — ACTIVE
- `feat/multi-agent-alignment` — EXPERIMENTAL / current work (not auto-merge)
- other feat/* — EXPERIMENTAL keep
- archive freeze tags — ARCHIVE keep

### GEOX / WEALTH / WELL
- `main` — ACTIVE
- `zen-migration-*` / `wealth-zen-clean` — working branches KEEP
- freeze/archive tags KEEP

## Explicit non-actions
- No `git push --delete`
- No mass merge
- No history rewrite

*Right way = named decisions + reversible tags, not a clean-looking remote.*
