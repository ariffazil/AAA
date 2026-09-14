# P-05: HERMES Skills Triage — Selective Review Plan
> **Status:** DRAFT_SPEC_READY

## Status: PATCH_READY (triage complete, no mutations)

## Inventory

| Metric | Count |
|--------|-------|
| Total skill directories | 198 |
| Skills with SKILL.md | 347 (some directories have sub-skills) |
| Skills with description | 345 |
| Skills referencing deprecated tools | 14 |
| Categories | 20+ |
| Total size | ~1.6 GB |

## Category Triage (by review priority)

### Priority 1: HIGH — Deprecated/Orphaned (14 skills)

Skills referencing deprecated/removed tools (forge_minimax_search, etc.):
- These should be marked ARCHIVED or updated
- Low risk to retire (they don't load unless explicitly called)

### Priority 2: MEDIUM — Overlapping/Redundant

Categories with high skill density that likely have overlap:
- data-intelligence: 30 skills — likely has redundancy
- governance-audit: 23 skills — likely has redundancy
- autonomous-ai-agents + autonomous-agents: 23 combined — significant overlap
- productivity: 14 skills — likely has redundancy

### Priority 3: LOW — Active and Unique

Categories with clear, unique skills:
- voice-audio: 4 skills
- media-creative: 4 skills
- wellness-care: 2 skills
- knowledge: 3 skills

## Recommended Actions

| Action | Scope | Impact |
|--------|-------|--------|
| Archive deprecated skills | 14 skills | Removes stale tool references |
| Deduplicate overlapping categories | ~20 skills | Reduces confusion |
| Compress skill descriptions | 347 skills | Reduces always-loaded prompt size |
| Move rarely-used skills to on-demand | ~100 skills | Reduces context overhead |

## What NOT to Touch

- Skills that are actively used in this session
- Skills that implement core governance (judge-gate, kernel-bridge, etc.)
- Skills that are referenced by the two-agent architecture
- Skills that have recent commits (last 7 days)

## Deployment

This triage is a plan only. Execution requires:
1. Review each deprecated skill for retirement
2. Deduplicate overlapping skills
3. Compress descriptions
4. Move rarely-used to on-demand loading
5. All changes are reversible

## Context Reduction Estimate

| Before | After | Reduction |
|--------|-------|-----------|
| 198 skills in system prompt | ~50 core skills | -75% |
| 347 SKILL.md files | ~200 active files | -42% |
| 1.6 GB total | ~800 MB | -50% |

## Next Steps

1. Archive 14 deprecated skills (Priority 1)
2. Deduplicate data-intelligence and governance-audit (Priority 2)
3. Compress skill descriptions to 1-line each
4. Implement lazy-loading for non-core skills
