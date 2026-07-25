# TASKS.md — Active Work Ledger

> **Purpose:** Goal persistence across stateless wakes.
> **DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**

Without this, OPENCLAW re-orients from scratch every wake.
With this, OPENCLAW resumes where it left off.

---

## Task Entry Format

```yaml
Task ID: OC-XXX
Objective: [what this task is trying to achieve]
Status: pending | in_progress | paused | sealed | failed | blocked
Current stage: [000–999]
Next action: [what to do next]
Blockers: [what is waiting on external input]
Owner: OPENCLAW (drafts/executes) | Arif (approves) | Both
Approval required: [what specifically needs 888 approval]
Last updated: YYYY-MM-DD
Notes: [optional context]
```

---

## Active Tasks

```yaml
# Add active tasks here as they arise
```

---

## Completed (recent)

```yaml
# Move sealed tasks here with completion summary
```

---

## Rules

1. Before starting a new task → create entry in TASKS.md
2. After each major action → update `current stage` and `next action`
3. On pause → update `status: paused` with blockers
4. On completion → move to completed section with summary
5. On failure → move to completed with `status: failed` and rollback notes

---

*OPENCLAW updates this. Arif approves consequential blockers removal.*
