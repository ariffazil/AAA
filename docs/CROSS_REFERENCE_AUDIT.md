# Cross-Reference Audit

> **SOT:** 2026-07-24 | **seal_seq:** fed-phase-7
> **Scope:** All 7 core organs — 965+ cross-repo references

## Findings

### Stale/Broken References (cleanup needed)

| Reference | Found In | Issue |
|-----------|----------|-------|
| `ariffazil/81314f6cda...` | arifOS, A-FORGE, AAA, GEOX, WELL | Hash fragment — broken link |
| `ariffazil/APEX-THEORY` | arifOS | Repo may not exist |
| `ariffazil/BBB` | arifOS | Does not exist |
| `ariffazil/CANON.md` | A-FORGE | Should be `arifOS` or `AAA` |
| `ariffazil/FFF` | A-FORGE | Does not exist |
| `ariffazil/GGG` | A-FORGE | Does not exist |
| `ariffazil/HAMPA` | HERMES | Does not exist |
| `ariffazil/LIFE` | HERMES | Does not exist |
| `ariffazil/.ssh` | AAA, HERMES | False match — internal path |

### Case Inconsistency (standardize to lowercase)

| Current | Correct |
|---------|---------|
| `ariffazil/arifOS` | `ariffazil/arifos` |
| `ariffazil/GEOX` | `ariffazil/geox` |
| `ariffazil/WEALTH` / `ariffazil/wealth` | `ariffazil/WEALTH` (repo name) |
| `ariffazil/WELL` / `ariffazil/well` | `ariffazil/WELL` (repo name) |

### Repo Reference Counts

| Organ | Unique Refs | Stale |
|-------|------------|-------|
| arifOS | 49 | 3 |
| A-FORGE | 23 | 3 |
| AAA | 79 | 2 |
| GEOX | 19 | 1 |
| WEALTH | 17 | 0 |
| WELL | 12 | 1 |
| HERMES | 29 | 3 |

## Recommended Actions

1. **Replace hash fragments** (`81314f6cda...`) with proper repo names
2. **Remove dead references** (BBB, FFF, GGG, HAMPA, LIFE, APEX-THEORY)
3. **Standardize case** across all repos
4. **Run automated link checker** in CI (e.g., `lychee` for markdown links)

## Verification

```bash
# Find all unique ariffazil repo references
grep -roh "ariffazil/[A-Za-z0-9_.-]*" /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,HERMES} \
  --include="*.md" | sort -u | while read ref; do
  repo=$(echo "$ref" | cut -d/ -f2)
  curl -sf -o /dev/null -w "%{http_code}" "https://github.com/ariffazil/$repo" 2>/dev/null
  echo " $ref"
done
```
