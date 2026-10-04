# Hermes Flat Memory → Helix Compression (2026-08-12)

> Session: Arif directive "Zen it. Seal the gaps and make room for more memory for my hermes agent."
> Technique: compress Hermes session MEMORY.md + USER.md to free the 6000-char tool budget.

## The problem

Hermes agent memory lives in TWO flat markdown files per profile:
- `MEMORY.md` (system/tool notes — 6000 char limit, injects every turn)
- `USER.md` (user profile — 3000 char limit, injects every turn)

At 98% full, the `memory` tool refuses writes:
```
Memory at 5,887/6,000 chars. Adding this entry would exceed the limit.
```

## The two-file discovery

There are actually TWO memory layers in a profile-based Hermes install:

| File | Scope | Char limit | Path |
|------|-------|-----------|------|
| Global canonical | All sessions | 6000 | `/root/.hermes/memories/MEMORY.md` |
| Profile-specific | Per profile | 6000 | `/usr/local/lib/hermes-agent/profiles/<profile>/memories/MEMORY.md` |

When active profile = `aaa-hermes`, the profile-specific file is what the `memory` tool reads/writes.
The global one at `/root/.hermes/memories/` is the legacy/default profile.
Both must be compressed if both are full.

USER.md follows the same split.

## The compression technique (helix-style)

The helix principle: **keep identity-bearing content, compress operational detail to one-liners, drop what already lives in the filesystem or git.**

### What to KEEP (identity-bearing — survives compression)
- Person register (Telegram IDs, chat IDs)
- Personality/behavior preferences (how Arif wants things done)
- Constitutional grammar / architectural principles
- Exit strategy, address preference, hard rules
- Active infrastructure state (what's LIVE, what's RETIRED)

### What to COMPRESS (merge related entries)
- Multiple audit-standard entries → one "5-layer audit" line
- Multiple build-audit entries → one "build discipline" block
- Multiple frustration-signal entries → one "behavior" block

### What to DROP (lives elsewhere)
- Specific commit hashes (in git log)
- Specific line numbers (in source)
- Specific backup paths (in filesystem)
- Detailed event narratives (in session_search / H2-experience)

### Worked results (2026-08-12)

| File | Before | After | Reduction |
|------|--------|-------|-----------|
| Global MEMORY.md | 4295 bytes | 1838 bytes | -57% |
| Profile MEMORY.md | 5717 bytes | 1838 bytes | -68% |
| Profile USER.md | 1989 bytes | 1358 bytes | -32% |

## Machine ledger sync (GAP-2 closure)

During the same session, the machine-side scar ledger had drifted:
- H5 canonical: 20 scars (v3.0.0)
- Machine-side index: 7 scars (old SCAR-001..005 + SCAR-000 + CEREMONY-002)

### Naming collision pitfall

The machine ledger had old `SCAR-001`..`SCAR-005` IDs that were the SAME scars as
`SCAR_LEBAH_EMAS`..`SCAR_MEMORY_DOCTRINE_V1` in H5. When syncing, adding H5 entries
naively produced 25 scars (7 + 18) — but 5 were duplicates.

**Fix:** dedup by checking if the old numeric ID maps to a descriptive H5 ID:
```
SCAR-001 = SCAR_LEBAH_EMAS
SCAR-002 = SCAR_RIGHTSIZING  (note: SCAR-002-CEREMONY_FAILED_406 is DIFFERENT — machine-only)
SCAR-003 = SCAR_UNHEARD
SCAR-004 = SCAR_MAKCIKGPT
SCAR-005 = SCAR_MEMORY_DOCTRINE_V1
```

Remove old numeric aliases, keep H5 descriptive IDs + machine-only scars.

### Verify after sync

```python
import json
h5 = json.load(open('/root/memory/H5-scars/H5_SCAR_REGISTRY.json'))
machine = json.load(open('/root/.local/share/arifos/scars/index.json'))
h5_ids = {s['scar_id'] for s in h5['scars']}
machine_ids = {s['scar_id'] for s in machine['scars']}
# Machine should have all H5 IDs + any machine-only (e.g. SCAR-CEREMONY-002)
missing = h5_ids - machine_ids
print(f"Missing from machine: {missing}")  # should be empty
```

## The "don't theorize, scan" lesson

When Arif said "zen it with helix memory in the system", the first response was
theoretical ("helix memory is like DNA, two strands..."). Arif corrected: "Nope.
U go and scan the vps to understand the helix memory architecture."

**Rule:** When asked about system architecture, SCAN FIRST (`search_files`, `read_file`,
`terminal ls/cat`). Never theorize from memory. The real files on disk are the truth.
Doctrine says it: "Pages are for humans. Contexts are for agents." — and the files ARE
the context.
