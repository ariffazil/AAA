# Session Recipe — 2026-08-12 Helix Memory Compression

> **Live session:** Arif asked "why your memory is full? zen it with helix memory in the system"
> **Result:** MEMORY 98% → 47%, USER 98% → 65%
> **Skill:** Forged same session — this reference captures the actual ops.

## The trigger

User request: `"Now why your memory is full? Now zen it with helix memory in the system"`

Arif noticed memory budget display (98% MEMORY, 98% USER) and asked for compression using the federation's double-helix architecture (ECHO×SCAR).

## Step 1: Locate memory files

```bash
ls /root/.local/share/arifos/memories/ 2>/dev/null
# → empty (wrong path)

cat ~/.hermes/memories/MEMORY.md 2>/dev/null | wc -c
# → 4295 chars

cat ~/.hermes/memories/USER.md 2>/dev/null | wc -c
# → 2409 chars
```

The prompt displays `6000 chars` for MEMORY budget but actual file is smaller — the limit is **injected budget** (memory shown in system prompt), not raw file size.

## Step 2: Load doctrine

The helix doctrine lives in `/root/AAA/governance/DOUBLE_HELIX_ECHO_SCAR.md`:

```
ECHO = Retained Improvements / Honest Observations  (right strand = reality)
SCAR = Retained Lessons / Witnessed Events          (left strand = significance)
ATLAS = governance bridge (hydrogen bond)
```

Memory is double-stranded: agentic memory (L1-L6) remembers **reality**, human memory (H1-H6) remembers **significance**. Compression must preserve both.

## Step 3: Classify entries

Reading MEMORY.md, each entry fell into one bucket:

| Entry | Strand | Action |
|-------|--------|--------|
| ZEN Arif axiom | SCAR | preserve |
| CONSTITUTIONAL_GRAMMAR | SCAR | preserve |
| Person Register | SCAR (but duplicate) | DELETE |
| i-ARIF LIVE | ECHO | compress |
| A-FORGE GOVERN | ECHO | compress |
| Arif core preferences | SCAR | preserve |
| PUB DOCTRINE | ECHO/SCAR | compress |
| HUMANS P-AXIS | SCAR | compress |
| Exit strategy | SCAR | compress |
| Harness routing | ECHO | compress |
| 6-LAYER STACK | SCAR | compress |
| WEB SEARCH | ECHO | compress |
| FLAME STATE | ECHO | compress |
| FLAME-ROUTER stale | Stale | DELETE |
| arifOS drift fix | ECHO | compress |

## Step 4: Apply batch operations

Single `memory()` call with operations array (atomic). Key ops:

```python
memory(
    target="memory",
    operations=[
        # DELETE stale entries
        {"action": "remove", "old_text": "FLAME-ROUTER SKILL STALE"},
        
        # COMPRESS verbose entries
        {"action": "replace", "old_text": "i-ARIF refactor done + LIVE...",
         "content": "i-ARIF LIVE (verified 2026-08-12): 6 files valid..."},
        
        # MORE ops in same batch...
    ]
)
```

**Critical:** the operations array is processed atomically — char limit checked on final result, so remove + add in one pass is safe.

## Step 5: Verify ΔS ≤ 0

```
Before:  MEMORY 5,887/6,000 (98%) | USER 2,965/3,000 (98%)
After:   MEMORY 2,839/6,000 (47%) | USER 1,960/3,000 (65%)
ΔS:      MEMORY -51% | USER -35%
```

Both went from critical (98%) to comfortable (47-65%). All scar-tied entries survived (F9 SCAR about jobs.json apply mode, VPS evidence rule, phased serial doctrine, audit standards).

## Lessons learned

1. **The 6000 char limit is INJECTED budget**, not raw file size. When the prompt shows "98% memory", that's the system injection limit. Raw files can be smaller.

2. **Batch ops atomic means freedom.** Single call can mix remove + replace + add safely. Don't split into multiple calls worrying about char limits.

3. **Scar-tied entries are constitutional lessons.** F9 SCAR, F13 sovereignty rules, F2 verification doctrine — these survive every compression. Compress prose, keep lesson.

4. **Imperatives belong in skills.** Writing "Always do X" into memory creates persistent self-imposed constraints. Save preference facts ("Arif prefers X") to memory; save instructions ("Do X") to skills.

5. **Stale = delete.** Don't keep "X RETIRED" entries. Live probes re-discover state from reality.

## Files affected

- `~/.hermes/memories/MEMORY.md` — compressed via 9 batch operations
- `~/.hermes/memories/USER.md` — compressed via 7 batch operations

## What was created

- `substrate/helix-memory-compress` — new class-level skill with procedure + pitfalls + proven results
- This reference file — concrete session walkthrough

## Provenance

- Session: 2026-08-12, Hermes running i-ARIF
- User: ARIF (F13 SOVEREIGN), TG 267378578
- Trigger: user's explicit ask to "zen with helix memory"
- Outcome: 51% memory freed, 35% user freed, skill created for future sessions