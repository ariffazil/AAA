# YouTube Multimodal — Pipeline Architecture

## Skill Relationship Map (2026-08-09)

```
youtube-multimodal (UNIFIED ENTRY POINT)
    |
    +--- youtube-content   (scripts: fetch_router.py, cache.py, fetch_transcript.py)
    |     Acquisition layer. S0-S8 cascade. Cache management.
    |     Located: media/youtube-content/scripts/
    |
    +--- youtube-eureka    (references: cache-schema.md, innertube-comments-extraction.md,
    |     malaysia-fitness-scene.md, pasted-pivot-audit-pattern.md,
    |     vps-acquisition-matrix.md, youtube-comments-extraction.md)
    |     Analysis layer. 11-part EUREKA contract. The intelligence format.
    |
    +--- youtube-analysis  (references: no-captions-pivot-evjOukIg_bQ-2026-08-08.md)
          Visual fallback. Frame extraction. Poster-vs-content detection.
```

## Why Unified?

Before this skill, the agent had to:
1. Decide which of 3 skills to load
2. Remember which script lives where
3. Manually pivot between transcript and visual paths
4. Know the EUREKA contract was in a different skill than the fetch command

Now: ONE skill, ONE pipeline, automatic routing.

## Original Skills (preserved for deep-dive)

The three original skills remain as detailed references for edge cases:
- **youtube-content**: When you need to understand the S0-S8 cascade internals
- **youtube-eureka**: When you need the full EUREKA contract with worked examples
- **youtube-analysis**: When you need the physique classification framework or identity verification patterns

## Reference Files (inherited)

These reference files live in the original skills but are relevant to the unified pipeline:

| File | From | When to read |
|------|------|-------------|
| cache-schema.md | youtube-eureka | Parsing fetch_router.py output |
| vps-acquisition-matrix.md | youtube-eureka | Understanding VPS bot-wall |
| innertube-comments-extraction.md | youtube-eureka | Comments pipeline |
| youtube-comments-extraction.md | youtube-eureka | Comments schema |
| malaysia-fitness-scene.md | youtube-eureka | Malaysian bodybuilding context |
| pasted-pivot-audit-pattern.md | youtube-eureka | Verifying pasted external analyses |
| no-captions-pivot-evjOukIg_bQ-2026-08-08.md | youtube-analysis | Worked no-transcript example |
