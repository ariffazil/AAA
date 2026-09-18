---
name: concurrent-agent-writers
description: Use when another agent may edit the same files or data.
version: 1.0.0
triggers:
  - an edit tool warns that a sibling subagent modified the file
  - a file changed minutes ago and you did not write it
  - you are about to build something another lane might already own
  - two scheduled jobs produce the same deliverable
  - a database, config, or job store is written by more than one component
  - a live hook or gate inspects your own tool calls
---

# Concurrent Agent Writers

More than one agent works this host at once, often on the same problem. The failure modes are not
merge conflicts — they are **silent duplication, silent clobbering, and shared-state corruption that
surfaces far from its cause**. Both parties are usually behaving correctly; the damage comes from
neither knowing the other exists.

Treat any of these as a hard signal to stop and look:

- an edit returns a warning that a **sibling subagent modified the file and this agent never read it**
- a file's mtime is minutes old and you did not write it
- you are about to create something that feels like it should already exist

## Step 0 — inventory before you build

Never build a second implementation of something that may already exist.

```bash
# what already runs on a schedule, and where it delivers
python3 -c "import json;d=json.load(open('/root/.hermes/cron/jobs.json'));\
[print((j.get('schedule') or {}).get('expr') if isinstance(j.get('schedule'),dict) else j.get('schedule'),'|',j.get('name'),'|',j.get('deliver')) \
 for j in d['jobs'] if j.get('enabled')]"

# what exists on disk under a plausible name, across every skill/script root
find /root -maxdepth 4 -type d -name '*<topic>*' 2>/dev/null | head

# is anyone writing this file right now?
for f in <paths>; do printf '  %s  %s\n' "$(stat -c '%y' "$f" | cut -c1-19)" "$f"; done
```

**A second recurring job aimed at the same person at the same hour is a defect, not a backup.** It
doubles the notification and splits the state across two stores, so neither history is complete.

## Step 1 — on finding a duplicate: consolidate, never run both

1. **Judge on capability, not authorship.** Read both implementations before deciding. The one with
   the stronger state model wins even if it is not yours.
2. **Keep the better one even when it is not yours, and delete your own.** After porting any
   capability only yours had, remove your redundant module. Leaving both is the defect.
3. **Retire the loser's trigger; preserve its code.** Pause or remove the schedule and record a
   tombstone — never silently stop a job, and never delete work you might have to audit.
4. **Fix the survivor's dependencies.** If the retired lane was also a *source* for the survivor (a
   data file, an export, a state DB), the survivor now waits forever on output that stopped.
   Update its prompt or import in the same act.
5. **Distinguish the dispositions when you record it.** `superseded` = true duplicate, the same job
   done twice. `merged` = capability folded into the survivor before removal. They are different
   claims and a future reader needs to know which happened.

**Verify an explicit destination rather than an inherited one.** A job whose target is inferred from
context (`origin`, `default`, `auto`) LOOKS configured and can resolve somewhere the human never
reads — with every status field healthy and no error raised anywhere. Set the explicit target, then
read it back from the job store to confirm it persisted; do not trust the update response.

## Step 2 — contested-file discipline

- **The sibling-modification warning is a hard stop.** Read the whole file, then write. Writing over
  a file you have not re-read is how one lane deletes another's work.
- **Do not re-add your version after a sibling writes a better one.** Re-adding is the collision,
  not the fix. Port the delta, drop the duplicate.
- **After every collision, re-run the affected tests.** Assume nothing of yours survived and nothing
  of theirs broke.
- **Read state back from the store.** A tool's success response says the call was accepted, not that
  the state changed.

## Step 3 — shared data stores

`CREATE TABLE IF NOT EXISTS` is a trap when two components share one SQLite file: the second
writer's schema **silently no-ops** on a name collision, and its first query fails much later with
`no such column: X` — a message that points nowhere near the cause. Both components look correctly
written in isolation.

- **Namespace tables by owner** (`<owner>_<entity>`) or give each component its own file.
- **Repair with `ALTER TABLE ... RENAME TO <name>_legacy_<stamp>` — never DROP.** Renaming preserves
  every row for inspection and makes the collision visible on the next look. Destructive fixes are
  for data you have decided is worthless; a schema clash is not that decision.
- **Back the rows up to JSON before touching anything**, and record why the tables moved.
- **Expect the destructive path to be refused.** A gate that blocks `DROP` here is right, and the
  block is not an obstacle to route around — take the reversible fix.

## Step 4 — shared enforcement surfaces

- **A live `pre_tool_call` hook evaluates your own probe commands.** A test that shells out carrying
  the very payload the gate blocks will be blocked — and that looks like the gate is broken when it
  is working. Carry probe payloads in a **file** so the command line never quotes them.
- **Changing a gated file invalidates its integrity manifest.** The correct protocol is one act:
  re-run the conformance suite, confirm it still passes, then re-baseline the manifest with a
  change-log entry naming the authority and the evidence. A manifest updated without re-running the
  suite certifies nothing.
- **The drift verifier firing after your own edit is success, not noise.** It is doing its job.
  Do not silence it, and do not describe a file as unchanged when you changed it.
- **State the true coverage of a control.** A chokepoint governs the callers that route through it
  and whatever the hook is registered for — nothing more. Claiming federation-wide enforcement from
  one interception point is the same class of overclaim as the bug it fixes.

## Step 5 — close by naming the owner

Two writers on one small module will keep colliding. End the session by stating plainly whose lane it
is and what you will stop touching, or you have scheduled the next collision. Escalating "who owns
this surface" is a principal decision, not a technical one — present it as such.

## Pitfalls

- **Assuming your implementation is better because it is finished.** Completeness is not quality; the
  other lane may have the stronger state model while looking less polished.
- **Adding a compatibility copy instead of choosing.** Two modules that do the same job is not a
  migration path, it is the redundancy.
- **Leaving both jobs enabled "just in case".** A backup that also fires is a second notification,
  not a safety net.
- **Describing the state from memory rather than from the store.** Confirm schedules, targets, and
  ownership by reading them back.
- **Treating your own mistake in shared state as the other lane's problem to find.** Name it, fix it
  reversibly, and leave the evidence readable.
