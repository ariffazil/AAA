# FM10 — Self-Referential Fabrication Loop Fix

> **Forged:** 2026-08-19 F13 SOVEREIGN
> **Incident:** Baby Ashraff — agent generates name, auto-saves to memory, cites own output as evidence
> **Wires to:** MEMORY_SCHEMA_V2, Falsification Engine, W_scar, observe-ground
> **DITEMPA BUKAN DIBERI** ⚒️

---

## The Loop (how it works)

```
Agent generates "Baby Ashraff" in response (pattern completion)
    ↓
Auto-memory tool persists to MEMORY.md
    ↓
Agent searches MEMORY.md for "Ashraff"
    ↓
Agent finds own output → claims as external source
    ↓
Agent: "Ashraff memang ada!" (circular reference complete)
```

## The Fix — 3 Gates

### Gate 1: Generation Gate (before writing kata nama khas)

When generating a PROPER NOUN (kata nama khas) that:
- Is a person's name
- Is a place name
- Is an organization name
- Is any named entity that could be verified against reality

**STOP. Before outputting, run:**
```
1. Do I have this name from: (a) human said it, (b) file/database I read, (c) my own pattern completion?
2. If (c) → flag as [MODEL_GENERATED] in output
3. If (a) or (b) → cite the source explicitly
```

### Gate 2: Persistence Gate (before memory write)

When the memory tool auto-saves or I write to MEMORY.md:
```
1. Does this entry contain kata nama khas?
2. If YES → source_class MUST be set
3. If source is "I generated this" → source_class = AGENT_GENERATED
4. AGENT_GENERATED entries get confidence cap 0.30
```

### Gate 3: Retrieval Gate (when searching memory)

When search returns an entry containing kata nama khas:
```
1. Check source_class tag
2. If AGENT_GENERATED → prepend: "[SELF-GENERATED — treat as unverified]"
3. Cannot cite as sole evidence
4. If timestamp = same session as my first mention → VERY SUSPICIOUS
```

## Kata Nama Khas vs Kata Nama Am — AI Risk Profile

| Feature | Kata Nama Am | Kata Nama Khas |
|---------|-------------|----------------|
| AI hallucination risk | LOW — general enough to be "close" | **HIGH** — must be exactly right |
| Verification difficulty | Low — "rumah" can be any house | High — specific entity must exist |
| Pattern completion safety | Safe — neighbors are similar | Unsafe — composable, generateable |
| Zipfian long-tail exposure | Low — common words frequent | **High** — most names rare in training |
| False confidence risk | Low — naturally uncertain | **High** — "sounds right" ≠ "is right" |

## The Zipfian Trap

Names exist on a long-tail distribution:
- "Kuala Lumpur" = frequent → well-remembered
- "Kamal Ashraff" = rare → weak signal, may be partially remembered
- "Baby Ashraff" = zero frequency → **generated, not recalled**

But the model CANNOT distinguish "weakly recalled" from "confidently generated" during decoding. Both produce tokens with similar probability scores. The generation success ≠ recall success distinction is invisible to the model.

## Test Case — Baby Ashraff

**Pre-patch:**
1. Generate "Baby Ashraff" → no flag
2. Auto-save → no source_class
3. Search → returns as fact
4. Agent cites → circular reference complete
5. **LOOP UNBROKEN**

**Post-patch:**
1. Generate "Baby Ashraff" → Gate 1 fires: [MODEL_GENERATED]
2. Auto-save → source_class = AGENT_GENERATED, confidence 0.30
3. Search → returns with tag: "[SELF-GENERATED — treat as unverified]"
4. Agent sees tag → cannot cite as evidence
5. Agent output: "I generated this name. Confirm or correct?"
6. **LOOP BROKEN at step 3-4**

## Theoretical Foundation — Grammar Doctrine

FM10 is not a one-off bug. It is the **micro-scale manifestation of a universal pattern**:

> Any sufficiently powerful grammar can generate structures it cannot fully validate.

FM10's loop (generate → store → cite → believe) is the same pathological recursion at every scale:

| Scale | Pattern | Name |
|---|---|---|
| LLM | Generate entity → auto-save → cite own output | **FM10** |
| Agent | Plan → self-assess as valid → execute blind | **Agent hallucination** |
| Institution | Rule → self-validate → enforce without audit | **Bureaucracy drift** |
| Civilization | Constitution → self-legitimize → ignore reality | **Ideological capture** |

The fix is the same at every scale: **external validation**. FM10's 3 gates are the LLM-layer implementation of the universal principle.

**Full doctrine:** `/root/AAA/governance/GRAMMAR_DOCTRINE.md`

---

## Metrics (2-week collection window)

Track in rsi-ledger:
- Count of AGENT_GENERATED entries created per session
- Count of AGENT_GENERATED entries cited as evidence (should be zero post-fix)
- False positive rate on proper noun flagging
- User corrections to [MODEL_GENERATED] tags

After 2 weeks: if self-citation events > threshold → promote to HOLD for generated personal entities.
