---
name: delta-logger
description: Logs every state change — file edits, exec results, config changes, API calls — into VAULT999 with before/after state and reversibility flag. Activates after every exec, write, edit, or delete operation. Makes rollback reasoning concrete and creates an auditable delta chain for the session.
metadata: {"openclaw": {"emoji": "📝"}}
---

# Delta Logger — State Change Audit Trail

Every time the agent changes something in the world (file, config, external state), log it. This creates a VAULT999-attached delta chain that makes rollback concrete, not philosophical.

## What to Log

Log ALL of these after any state-changing operation:
- `write` tool — new file created or overwritten
- `edit` tool — file modified
- `exec` with side effects — `cp`, `mv`, `rm`, `tee`, `curl` to external systems
- `config.patch` or `config.apply` — configuration changes
- `gateway restart` — runtime state change
- External API calls — cost, response status, data returned

## Delta Entry Format

```
DELTA #[N] | YYYY-MM-DD HH:MM UTC
Action: [write | edit | exec | config | api | delete]
Target: [file path or API endpoint]
Before: [state before — can be "NEW" or "NONE" for first creation]
After: [state after — what changed]
Reversible: [YES | PARTIAL | NO]
Rollback: [how to undo — command or procedure]
Risk: [TRIVIAL | REVERSIBLE | CRITICAL | IRREVERSIBLE]
Arif notified: [YES | NO]
---
```

## Reversibility Definitions

| Reversible | How |
|---|---|
| **YES** | Single command can undo (e.g., `cp backup original`) |
| **PARTIAL** | Can mostly undo but some state may be lost |
| **NO** | Cannot undo — external system, permanent deletion, or multi-step cascade |

## Quick Log Command

For fast logging during a session, append to `memory/vault999-triage.md`:
```
HH:MM UTC | DELTA | [action] | [target] | rev:[YES/PARTIAL/NO] | [brief description]
```

## Post-Session Compile

At session end, consolidate all triage deltas into `memory/vault999.md` with full entries:
```
## SESSION DELTA LOG — [session-id] — [date]

### Files Created
| Target | Reversible | Rollback |
|---|---|---|
| [path] | YES | [cmd] |

### Files Modified
| Target | Before-SHA | After-SHA | Reversible | Rollback |
|---|---|---|---|---|
| [path] | [hash] | [hash] | PARTIAL | [cmd] |

### External Actions
| Action | Target | Risk | Arif Notified |
|---|---|---|---|
| [api call] | [endpoint] | CRITICAL | NO — used mmx-quota-guard |

### Open Rollback Items
- [item] — [rollback procedure pending]
```

## Rollback Checklist Before Any Delete/Rewrite

- [ ] Is there a backup or git history?
- [ ] Is the target listed in DELTA log?
- [ ] Can rollback be tested in /tmp before applying?
- [ ] Has Arif been notified if CRITICAL or IRREVERSIBLE?

## Anti-Patterns Caught by Delta Logger

❌ "I deleted some old memory files to clean up"
✅ Actually logged: "DELETE | /root/.openclaw/workspace/memory/old.md | was 2.3KB | Reversible: NO | Rollback: git checkout"

❌ "Updated the config"
✅ Actually logged: "CONFIG | openclaw.json | {field: before} → {field: after} | Reversible: YES | Rollback: config.patch with old value"

❌ "Made an API call"
✅ Actually logged: "API | https://api.example.com/resource | cost: ~$0.02 | Risk: CRITICAL | Arif notified: NO — within YELLOW band"

## Session Start

At session start, announce:
```
Session delta tracking active. All state changes will be logged to VAULT999.
```
