---
name: session-seal
description: Seal current session with constitutional audit trail, decisions log, and next-session priorities before ending work
user-invocable: true
---

# Session Seal

Constitutionally seal the current session before ending. Creates a structured record of what happened, what was decided, and what comes next.

## Invocation

`/session-seal` — Run at end of any working session.

## Execution Steps

1. **Gather session data** (from conversation context):
   - Key decisions made
   - Files created or modified (use `git status` and `git diff --stat`)
   - Unresolved items or blockers
   - Floor violations encountered (if any)

2. **Generate session seal document** using the template below

3. **Save to file**:
   - Path: `C:\Users\User\arifOS\.claude\sessions\seal_YYYYMMDD_HHMM.md`
   - Create the `.claude\sessions\` directory if it doesn't exist

4. **Update auto memory** if stable patterns were confirmed:
   - Edit `C:\Users\User\.claude\projects\C--Users-User-arifOS\memory\MEMORY.md` with new insights (only if genuinely new and verified)

5. **Copy to clipboard** via `/export` as backup

## Output Template

```markdown
# Session Seal: [YYYY-MM-DD HH:MM]

## Key Decisions
- [Decision 1]
- [Decision 2]

## Files Modified
- [file]: [what changed]

## Constitutional Audit
- Verdicts: X SEAL, Y PARTIAL, Z VOID
- Floor violations: [list or "None"]

## Unresolved
- [item or "None"]

## Next Session Priorities
1. [top priority]
2. [second priority]
3. [third priority]

## Context to Restore
- [key files or concepts needed next time]

---
Sealed by: arifOS v60.0-FORGE
```
