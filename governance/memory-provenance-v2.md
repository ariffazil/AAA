# Memory Provenance Schema v2

**Created:** 2026-08-19 23:15 MYT
**Author:** Arif (F13) — system patch after Baby Ashraff incident
**Status:** SCHEMA DEFINED — runtime adoption PARTIAL (corrected 2026-08-19 by 333-AGI probe)
**Probe evidence:** /root/HERMES/memories/MEMORY.md (37 lines, mtime 23:14) contains ZERO [SG:/[TS:/[SY: prefix tags. Observed runtime style = suffix tag `[AGENT_DERIVED]` (matches MEMORY_SCHEMA_V2.md 6-class scheme, not this file's 4-class prefix scheme). The fabricated "Baby Ashraff" entry itself is absent — replaced by a line-35 meta-entry documenting the FM10 incident, correctly tagged [AGENT_DERIVED].
**Lesson:** This file's original "DEPLOYED" claim was itself an unverified assertion — caught by probe-before-claim. The doctrine must hold for its own artifacts.

## Problem

Agent writes term → auto-memory saves → agent searches → finds own output → claims as source.
No mechanism to distinguish "entry created by agent from nothing" vs "entry reported by user."

## Schema

Every memory entry MUST carry provenance metadata. Two formats:

### v2 entries (new writes):
```
[SG:TIMESTAMP] content here
```
- `SG` = SELF_GENERATED — agent created this entry from its own output, no external source
- `TS` = EXTERNAL_REPORTED — user or external system provided this data
- `SY` = SYSTEM_OBSERVED — tool output, API response, file content (not user-typed)
- `UNKNOWN_LEGACY` = entry predates v2 schema, no provenance available

### v2 format examples:
```
[SG:2026-08-19T21:44] Baby Ashraff — trauma awal
[TS:2026-08-17T22:48] Syed disclosed ex-girlfriend knife scars
[SY:2026-08-19T18:00] D'Popeye gym research: Kamal Ashraff = WFF Pro
```

## Read Path Rules

When agent reads memory entries during reasoning:

1. **[SG:*] entries** = SELF_GENERATED. Treat as UNVERIFIED. Cannot be sole evidence for any factual claim. Must cross-check with external source before use.
2. **[TS:*] entries** = EXTERNAL_REPORTED. Treat as user testimony. Confidence depends on source reliability.
3. **[SY:*] entries** = SYSTEM_OBSERVED. Tool/API output. Higher confidence than TS.
4. **UNKNOWN_LEGACY** = no provenance. Treat as UNVERIFIED until source confirmed.

## Write Path Rules

When agent writes to memory via `memory(action=add)`:

1. **If content comes from agent's own generation** (not from user message, not from tool output):
   → Prepend `[SG:TIMESTAMP]`
2. **If content comes from user's direct statement**:
   → Prepend `[TS:TIMESTAMP]`
3. **If content comes from tool output/API/file**:
   → Prepend `[SY:TIMESTAMP]`

## Timestamp Gate (FM10 Prevention)

Before citing any memory entry as evidence:

```
1. What is the entry's source_class? (SG/TS/SY/UNKNOWN)
2. When was this entry CREATED?
3. When did I FIRST mention this term in THIS session?
4. Compare:
   - Entry predates my mention AND source_class != SG → independent source
   - Entry postdates my mention → I wrote it → NOT a source
   - Entry timestamp = my mention timestamp → same turn → VERY SUSPICIOUS
   - Source_class = SG → ALWAYS treat as unverified
```

## Rollback

Schema v2 is additive. Old entries (no tag) parse as `UNKNOWN_LEGACY`.
If v2 reader breaks: revert to v1 reader (ignores new fields).
4 separate commits: schema → write path → read path → gap detection.
