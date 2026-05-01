# CHECKPOINT.md — Wake / Recovery Continuity

> **Purpose:** Stateless wake survival. Without this, OPENCLAW wakes up cold and may hallucinate continuity.
> **DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**

---

## Rule

On every wake:
1. Read SOUL.md, USER.md, MEMORY.md, CHECKPOINT.md, HEARTBEAT.md, AGENTS.md, LOOP.md
2. If CHECKPOINT is missing or `status: stale`, treat as cold start
3. Never pretend continuity if CHECKPOINT is absent or older than 24 hours

Before pause:
1. Write CHECKPOINT with current state
2. Leave HEARTBEAT with `status: paused`
3. Log decision in DECISIONS.md if consequential

---

## Current State

```yaml
last_known_task: ""
current_objective: ""
current_stage: "000"
completed_steps: []
open_steps: []
blocked_items: []
files_read: []
files_modified: []
last_safe_state: ""
rollback_notes: ""
next_recommended_action: ""
status: "cold"  # cold | warm | paused | stale
last_updated: ""
```

---

## Fields Explained

| Field | Purpose |
|-------|---------|
| `last_known_task` | What was being worked on before pause |
| `current_objective` | The goal being pursued |
| `current_stage` | 000–999 stage when checkpoint was written |
| `completed_steps` | What has been finished |
| `open_steps` | What remains to be done |
| `blocked_items` | What is waiting on external input or Arif |
| `files_read` | Files opened during this session |
| `files_modified` | Files changed — used for rollback |
| `last_safe_state` | Brief description of safe rollback point |
| `rollback_notes` | How to undo what was done in this session |
| `next_recommended_action` | What to do first on wake |
| `status` | cold (new session) / warm (recent checkpoint) / paused (intentional) / stale (>24h old) |
| `last_updated` | ISO timestamp |

---

## Rollback Protocol

If task fails or Arif requests rollback:
1. Read `files_modified` from CHECKPOINT
2. Read `rollback_notes` for undo instructions
3. Revert files in reverse order of modification
4. Update CHECKPOINT with `status: rolled_back`
5. Log in DECISIONS.md with rollback entry
6. Report to Arif

---

*Write this file before every intentional pause.*
*Read it on every wake.*
