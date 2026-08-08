# Claude Code Auto Memory — arifOS Federation

> **DITEMPA BUKAN DIBERI** — Memory is forged through experience, not given by default.

## What Auto Memory Is

Claude Code's auto memory feature learns preferences and patterns across sessions. When enabled, Claude Code writes learned preferences to `~/.claude/memory/` so they persist across sessions.

## arifOS Federation Memory

The arifOS Federation has its own memory architecture (L1-L6), but Claude Code's auto memory serves as an additional L2.5 layer — session-thread preferences that supplement the federation's structured memory.

### What to remember
- **Codebase preferences**: "Use `forge_shell` not raw `bash` for governed execution"
- **Constitutional patterns**: "Always run `arif_init` before mutation work"
- **Workflow shortcuts**: "Use `make prove` for full proof pack"
- **Tool choices**: "Prefer A-FORGE forge_* tools over raw shell commands"
- **Pattern corrections**: "Never use `rm -rf` without snapshot first"

### What NOT to remember
- Secrets, tokens, or keys
- Session-specific state (that's what carry_forward.json is for)
- Ephemeral tool results

## Enablement

Auto memory requires Claude Code CLI interaction. Run:

```bash
claude
# Then in the Claude Code session:
# Claude will ask if you want to enable memory — say yes
# Or manually: /memory
```

## Memory Files Location
- `~/.claude/memory/` — auto-learned preferences
- `~/.claude/CLAUDE.md` — manually authored persistent instructions

## Integration with Federation Memory
- Auto memory → L2.5 (session preferences, learned patterns)
- Carry-forward → L2 (session state between sessions)
- Qdrant → L3 (fuzzy similarity search)
- Supabase → L4 (structured domain data)
- FalkorDB → L5 (relationship graphs)
- VAULT999 → L6 (immutable truth)

## Current Status
[2026-08-08] Auto memory file not yet populated. Enable via `/memory` in Claude Code CLI session.
