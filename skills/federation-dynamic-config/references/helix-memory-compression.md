# Hermes Memory Helix Compression — Session Pattern (2026-08-12)

## When This Pattern Applies

The Hermes `memory` tool hits its 3000-char limit and rejects new entries.
Memory is >90% full. The session cannot store new facts.

## The Fix (not delete-one-by-one)

Bulk compress via `write_file` directly to the memory file. Do NOT use the
`memory` tool for compression — it will loop-fail at the character limit.

### Steps

1. Read both `MEMORY.md` and `USER.md` (profile + global paths)
2. Identify compression targets:
   - Merge 3+ related entries → 1 summary line
   - Drop operational status (deployment hashes, version numbers)
   - Keep: identity, persona prefs, constitutional grammar, hard rules
3. Write compressed files via `write_file`
4. Verify: `wc -c` shows ≤50% of original

### Compression Heuristics

| Keep | Drop |
|------|------|
| "Arif prefers hang not abang" | "Arif deployed commit 4a7adaf31" |
| Telegram IDs (hard to rediscover) | Port numbers (lives in organs.yaml) |
| Constitutional grammar V1 | FLAME provider status |
| Exit strategy summary | Git log details |
| "Visual = real photo NEVER ASCII" | "OpenCode model = deepseek-v4-pro" |

### The Helix Principle

```
Memori sihat = sivar geseran.
Memori sakit = ingat benda yang dah tak perple.
```

Memory = muscle (ephemeral working state), not diary (hoarded history).
The body doesn't store enzymes twice. Scars (identity/cost) are permanent;
operational snapshots are ephemeral.

### Verification

```bash
wc -c /usr/local/lib/hermes-agent/profiles/aaa-hermes/memories/MEMORY.md
wc -c /usr/local/lib/hermes-agent/profiles/aaa-hermes/memories/USER.md
# Before: ~5700 bytes. After: ~1800 bytes (68% reduction)
```

### Pitfall

- The `memory` tool has a 3000-char hard limit. Attempting bulk writes via
  `memory(action='add')` when >2700 chars used will trigger a loop of
  failures. Always use `write_file` for compression operations.
- Profile memory and global memory may be separate files or symlinked.
  Check both paths: `~/.hermes/memories/` and
  `/usr/local/lib/hermes-agent/profiles/{profile}/memories/`
