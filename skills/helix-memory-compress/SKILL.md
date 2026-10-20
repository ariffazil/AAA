---
name: helix-memory-compress
description: Practical double-strand memory compression procedure — classify ECHO (operational) vs SCAR (human significance) vs stale, batch-compress via memory operations array, verify ΔS ≤ 0. Triggered when memory ≥85% or user says "zen memory". Class-level skill covering the interactive compression pattern (NOT the autonomous dream-cycle consolidation — see AGI-dream-engine for that).
tags: [memory, compression, helix, echo-scar, zen, arif-bridge]
floor_scope: [F1, F2, F4, F7]
autonomy_tier: T1
version: 1.1.0
owner: 333-AGI
forged: 2026-08-12
forged_by: 333-AGI
patched: 2026-08-12 (added bridge architecture + address preference + scan-first pitfall)
related_skills:
  - AGI-dream-engine (autonomous dream-cycle consolidation, different trigger)
  - memory-manage (schema-level memory lifecycle, bundled)
  - references/bridge-architecture-2026-08-12.md (Hermes flat vs helix file system topology)
---

# Helix Memory Compression

> Double-strand compression for interactive sessions. Compress at the meaning level, not the word level. ΔS ≤ 0 every cycle.

## When to trigger

- `memory(action='add')` returns rejected or usage ≥85%
- User says "zen memory", "compress", "memory penuh", "clean memory"
- Session start shows bloated MEMORY.md or USER.md

## The helix model

Memory is double-stranded. Each entry belongs to one strand:

| Strand | What it carries | Compression rule |
|--------|----------------|-----------------|
| **ECHO** (right) | Operational facts — provider states, tool wiring, config, bugfixes, procedure notes | **Compress aggressively:** merge related entries, kill stale state, shorten descriptions |
| **SCAR** (left) | Human significance — preferences, corrections, identity axioms, scar-tied lessons | **Preserve meaning, compress words.** Never delete scar-tied entries |
| **Stale** | Changed state — old port numbers, deprecated tools, resolved bugs, superseded procedures | **DELETE entirely** — live probes re-discover from reality |

## Procedure (5 steps)

### Step 1: Read raw stores

```bash
cat ~/.hermes/memories/MEMORY.md   # operational ECHO strand
cat ~/.hermes/memories/USER.md     # human SCAR strand
```

### Step 2: Classify each entry

For each entry, ask:
- Does this reference a specific scar or correction event? → SCAR (preserve)
- Is this operational state that may have changed? → ECHO (compress) or Stale (delete)
- Is this duplicated elsewhere? → DELETE the duplicate

### Step 3: Compress

Apply these patterns to SCAR and ECHO entries:

| Pattern | Before | After |
|---------|--------|-------|
| **Merge** | 3 entries about same provider | 1 bullet covering all |
| **Strip dates** | "FLAME STATE 2026-08-12:" | "FLAME: 6 providers, 15 tiers..." |
| **Keyword register** | "Arif design: MakcikGPT is the Primer Dark visual identity for the words/writing forge section..." | "Arif design: MakcikGPT=Primer Dark. /words/writing/=forge." |
| **Kill filler** | "I should note that the default timezone is..." | "Default TZ: MYT (UTC+8)." |

### Step 4: Batch apply (single atomic call)

Use the `memory` tool with one `operations` array call. Mix `replace` (compress) and `remove` (delete) in the same call.

```python
memory(
    target="memory",
    operations=[
        {"action": "replace", "old_text": "<original substring>", "content": "<compressed>"},
        {"action": "remove", "old_text": "<stale entry substring>"},
        # ... more operations
    ]
)
```

The char limit is checked on the **final** result, so remove + add in one pass is safe.

### Step 5: Verify

After the call, check:
- `usage` percentage decreased (not just entry count)
- All scar-tied entries survive (spot-check F9/F13 references still present)
- No imperatives created — memory stores facts about preferences, NOT instructions

```
ΔS = chars_after - chars_before
Negative = entropy reduced ✓
Zero = neutral ≈ acceptable
Target: ≥30% reduction on first pass
```

## Pitfalls

### SCAN ARCHITECTURE FIRST — never compress blind
**Forged 2026-08-12 (Arif correction):** when the user says "zen with helix memory", do NOT immediately start compressing `~/.hermes/memories/`. The user may be asking you to understand the FULL helix architecture on the VPS first — which is a separate, richer system.

**Scan before acting:**
```bash
cat /root/memory/ZEN_HELIX.md          # the real helix doc
ls /root/memory/H1-capture/             # capture inbox (may be empty)
ls /root/memory/H5-scars/               # scar registry
cat /root/.arifos/scripts/memory-helix-rollup.sh  # daily rollup
ls /root/.arifos/memory/learned/        # episodic learned store
```

Two systems exist (see `references/bridge-architecture-2026-08-12.md`):
1. **Hermes flat memory** — `~/.hermes/memories/` (6KB cap, injected to every prompt)
2. **arifOS helix memory** — `/root/memory/` H1-H6 + `/root/.arifos/memory/` L1-L6 (file-based, NO cap)

The Hermes memory tool writes ONLY to flat memory. There is no auto-bridge to the helix file system. When the user says "zen", they may mean: understand the helix, archive to H1, THEN compress the flat stores. Not just compress blindly.

### User address preference — Arif = "hang", NOT "abang"
**Forged 2026-08-12 (Arif correction):** Address Arif as **"hang"** (Penang peer register). NEVER use "abang" — that term is reserved for the sado/gym bodybuilder image-gen context ONLY. Save to both memory AND this skill because it governs tone in every interaction.

### Scar-tied lessons must survive
Entries tied to F9 SCAR events (e.g., "validate_jobs_json apply is FULL REPLACE not patch") are hard-won constitutional lessons. Compress the prose, keep the lesson. These entries are the left strand.

### Imperatives belong in skills, not memory
- "Arif prefers execute_code for calculations" → ✓ memory (fact about preference)
- "Use execute_code for calculations" → ✗ skill instruction (not a memory fact)

If you catch yourself writing "always" or "never" in memory, that's a skill instruction masquerading as a memory fact.

### Stale = delete, not compress
If a provider was retired, an API key was purged, or a service was migrated — delete the entry entirely. Don't keep "X RETIRED" entries; live probes re-discover this from reality. Stale entries are entropy, not signal.

### Batch operations are atomic
One call, all changes applied together. The char limit is checked on the final result. This means you can safely remove stale entries AND add compressed replacements in the same pass.

### Target ≤70% after compression
Leave room for new preferences and corrections in future sessions. If you compress to 95%, you'll be back at capacity in one conversation.

## Proven results

| Session | Before | After | Freed | Method |
|---------|--------|-------|-------|--------|
| 2026-08-12 (Arif + Hermes) | MEMORY 98% (5,887/6,000) | 47% (2,839/6,000) | 51% | 9 replace + 0 remove ops |
### Target ≤70% after compression

Leave room for new preferences and corrections in future sessions. If you compress to 95%, you'll be back at capacity in one conversation.

### H5 scar registry sync — after compression
**Forged 2026-08-12:** after compressing Hermes flat memory, check whether any entries reference scars that need registry sync.

```python
# After compression, verify H5 registry is in sync
import json
with open('/root/memory/H5-scars/H5_SCAR_REGISTRY.json') as f:
    reg = json.load(f)
# Count: should match narrative .md count
# If drift → add missing scars + remove old-format duplicates
```

**Old-format duplicates to check for:**
- `SCAR_WAKID_3.md` → should be `SCAR-1.md`
- `SCAR_PUTERI_BASEMENT_1.md` → should be `SCAR-2.md`
- Any `SCAR_<NAME>.md` with the same well name as a `SCAR-N.md` is a duplicate.

## References

- `DOUBLE_HELIX_ECHO_SCAR.md` — the double-helix architecture (ECHO = right strand, SCAR = left strand, ATLAS = bridge)
- `HUMAN_MEMORY_DOCTRINE.md` — H1-H6 human memory tiers
- `AGI-dream-engine` — autonomous dream-cycle consolidation (companion skill for overnight/dream patterns)
- `substrate/memory-manage` — schema-level memory lifecycle (bundled, provides Axis 1/2/3 framework)

---

*Forged: 2026-08-12 from live session — Arif asked to zen memory with helix double-strand procedure. DITEMPA BUKAN DIBERI ⚒️*

<!-- SKILL-WITNESS-NOTE (auto, additive-only) -->
Witnessed reality moved this skill's selection to **ROUTE or MERGE**.
Scar signatures: 2026-10-18-stale-audit-batch-p0-already-fixed, SCAR-LEDGER-HUMAN-ARIF-FAZIL-2026-09-23
Do not treat this skill as neutral until the signatures are resolved.
<!-- /SKILL-WITNESS-NOTE -->
