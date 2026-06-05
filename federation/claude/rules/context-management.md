---
paths:
  - "**/*"
---

# Context Management Rules

## Token Budget Governance

### Thresholds
- **Green Zone** (0-60%): Normal operation
- **Yellow Zone** (60-75%): Suggest `/compact-smart` to user
- **Red Zone** (75-90%): Warn user, recommend compaction before new work
- **Critical** (90%+): Autocompact triggers

### Proactive Actions

1. **After completing major features**: Suggest `/compact-smart`
2. **Before complex reasoning**: Ensure sufficient headroom
3. **End of session**: Remind user about `/session-seal`

## Memory Hierarchy

```
L0 (Session)  → Current conversation context
L1 (Auto)     → ~/.claude/projects/*/memory/MEMORY.md
L2 (Sessions) → .claude/sessions/seal_*.md
L5 (Canon)    → Constitutional law (CLAUDE.md, immutable)
```

## Anti-Patterns

- Running at >90% without compacting
- Losing important decisions to autocompact
- Not sealing sessions before exit
- Ignoring context warnings
