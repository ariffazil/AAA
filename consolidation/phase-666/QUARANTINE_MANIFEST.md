# Quarantine Manifest — Phase 666

**Created:** 2026-07-12T05:37Z

## Purpose

This manifest identifies artifacts proposed for quarantine BEFORE any deletion. All items remain in their original locations until explicit human approval.

## QUARANTINE PROPOSED — Awaiting Human Approval

### Q1: Duplicated FEDERATION_CONTRACT.md (4 files)

| File | Repo | Lines | Action |
|------|------|-------|--------|
| FEDERATION_CONTRACT.md | A-FORGE | 92 | Replace with symlink/reference to arifOS canonical |
| FEDERATION_CONTRACT.md | AAA | 84 | Replace with symlink/reference to arifOS canonical |
| FEDERATION_CONTRACT.md | geox | 90 | Replace with symlink/reference to arifOS canonical |
| FEDERATION_CONTRACT.md | WEALTH | 85 | Replace with symlink/reference to arifOS canonical |

**Canonical:** `/root/arifOS/FEDERATION_CONTRACT.md` (342 lines)
**Rollback:** `archive/pre-consolidation-2026-07-12` branches contain all originals
**Observation period:** 1 full federation cycle (~24 hours)

### Q2: Duplicated CLAUDE.md (4 files)

| File | Repo | Lines | Action |
|------|------|-------|--------|
| CLAUDE.md | arifOS | 225 | Replace with thin bootstrap pointing to AAA canonical |
| CLAUDE.md | A-FORGE | 126 | Replace with thin bootstrap pointing to AAA canonical |
| CLAUDE.md | geox | 65 | Replace with thin bootstrap pointing to AAA canonical |
| CLAUDE.md | WEALTH | 89 | Replace with thin bootstrap pointing to AAA canonical |

**Canonical:** `/root/AAA/CLAUDE.md` (382 lines)
**Rollback:** `archive/pre-consolidation-2026-07-12` branches
**Observation period:** 1 full federation cycle

### Q3: Non-existent forge_* Tool References in Docs

| File | Repo | References |
|------|------|------------|
| Various docs | arifOS, AAA | forge_systemctl, forge_accessible, forge_audit, etc. |

**Action:** Remove references to non-existent tools
**Rollback:** git history
**Observation period:** None (doc-only change)

### Q4: Port :7072 References

| File | Repo | Action |
|------|------|--------|
| Various docs | A-FORGE, others | Change :7072 → :7071 |

**Action:** Fix port references
**Rollback:** git history
**Observation period:** None (doc-only change)

### Q5: Open Issues — RESOLVED_BY_DECISION (8 issues)

| Issue | Repo | Classification |
|-------|------|----------------|
| #559, #545, #544 | arifOS | Automation health reports — close or archive |
| #122, #43, #117, #21 | AAA, A-FORGE, geox, well | Weekly hygiene — close or convert to workflow |
| #124 | AAA | VOID sentinel — close with evidence |

**Action:** Close with documented reason
**Rollback:** Reopen if needed
**Observation period:** None

## NOT PROPOSED FOR QUARANTINE

- All source code files (ACTIVE or CANONICAL)
- All test files
- All deployment configs
- All skills and prompts
- All VAULT999 records
- Any file classified as UNKNOWN (protected until reviewed)

