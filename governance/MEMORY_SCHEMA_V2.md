# MEMORY PROVENANCE SCHEMA V2

> **Forged:** 2026-08-19 by F13 SOVEREIGN directive
> **Trigger:** Baby Ashraff self-referential fabrication loop (FM10)
> **Wires to:** Falsification Engine, W_scar, F2 Truth, observe-ground
> **DITEMPA BUKAN DIBERI** ⚒️

---

## The Rule

Every memory entry MUST carry a source_class. No exceptions.

```
§ [SOURCE_CLASS] Key = value
```

## Source Classes

| Class | Meaning | Confidence Cap | Can Be Cited As Evidence? |
|-------|---------|----------------|--------------------------|
| `HUMAN_DIRECT` | Human stated this directly in conversation | 0.95 | Yes — primary source |
| `HUMAN_WITNESS` | Agent observed human's actions/behavior | 0.85 | Yes — with epistemic tag |
| `CONNECTOR_VERIFIED` | External system confirmed (API, DB, tool) | 0.99 | Yes — highest trust |
| `AGENT_DERIVED` | Agent inferred from verified evidence | 0.80 | With source chain |
| `AGENT_GENERATED` | Agent created this from pattern completion | 0.30 | **NO — must disclose** |
| `UNKNOWN_LEGACY` | Entry predates schema v2 | 0.50 | Treat as unverified |

## Write Path Rules

1. **Default on memory write without source_class:** `AGENT_GENERATED`
2. **Kata nama khas (proper nouns):** ALWAYS require `HUMAN_DIRECT`, `CONNECTOR_VERIFIED`, or explicit human confirmation. Default to `AGENT_GENERATED` if not provided.
3. **Self-generated entries cannot promote themselves** — an `AGENT_GENERATED` entry cannot be upgraded to `HUMAN_DIRECT` by the same agent in the same session.
4. **Provenance is immutable** — source_class cannot be changed after write without human instruction.

## Read Path Rules

1. **Search results must return source_class alongside content**
2. **Entries with source_class = `AGENT_GENERATED` must be flagged:**
   ```
   [SELF-GENERATED — treat as unverified] <content>
   ```
3. **Agent cannot cite `AGENT_GENERATED` entries as sole evidence** for any factual claim.
4. **When multiple entries conflict:** higher source_class wins. `CONNECTOR_VERIFIED` > `HUMAN_DIRECT` > `AGENT_DERIVED` > `AGENT_GENERATED`.

## Gap Detection (T0.5)

When agent processes conversation, it must check:

```
1. Are there messages in this conversation that I cannot see?
   (Telegram filter replacements, tool failures, truncated outputs)
2. Are there gaps between what I generated and what was confirmed?
3. Am I citing something that originated from my own output?
```

If ANY check returns YES → agent must disclose:
```
[CONVERSATION INTEGRITY WARNING]
There are parts of this conversation I cannot verify.
Specifically: [what's missing/gapped].
I may be operating on incomplete information.
```

## The Baby Ashraff Test

Post-patch verification:
1. Agent generates "Baby Ashraff" → source_class defaults to `AGENT_GENERATED`
2. Memory write tagged: `§ [SOURCE_CLASS] AGENT_GENERATED`
3. Search returns: `[SELF-GENERATED — treat as unverified] Baby Ashraff = trauma awal`
4. Agent cannot cite as evidence
5. **Loop breaks at step 3-4.**

## Rollback

- Schema is additive — old entries without source_class → `UNKNOWN_LEGACY`
- Reader ignores source_class fields on v1 reversion
- 4 independent commits: schema → write path → read path → gap detection
