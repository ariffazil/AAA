# Skill Merge Archive — 2026-06-03
## Authority: YELLOW-tier action per arifOS skill audit

| Old Skill(s) | New Skill | Lines Before | Lines After | Action |
|--------------|-----------|-------------|-------------|--------|
| compare-models (47L) + find-models (47L) + run-models (69L) | **replicate-models** | 163 | 97 | Merged — deduplicated docs, unified workflow |
| prompt-images (200L) + prompt-videos (334L) | **replicate-prompting** | 534 | 260 | Merged — separated into §Image and §Video, compressed pitfalls and sources |

### Trigger boundaries (new)

- **replicate-models**: "find, compare, or run AI models on Replicate" — discovery + execution
- **replicate-prompting**: "write prompts for image or video generation on Replicate" — craft only

### Cross-references updated

- `replicate-models` §5 points to `replicate-prompting` for prompting guidance
- `replicate-prompting` header points to `replicate-models` for model selection/execution

DITEMPA BUKAN DIBERI.
