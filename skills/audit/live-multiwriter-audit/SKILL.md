---
name: live-multiwriter-audit
description: "Use when auditing state other agents are mutating."
version: 1.0.0
owner: Hermes (arifOS federation)
risk_tier: low
floor_scope: [F2, F4, F7, F11]
autonomy_tier: T1
triggers:
  - "live audit"
  - "concurrent writers"
  - "queue backlog"
  - "duplicate counts"
  - "absence claim"
  - "skill store count"
  - "is this wired"
  - "how many skills"
---

# Live Multi-Writer Audit

## When to Use
Any audit where the thing being measured is also being written by other agents, cron lanes, or sessions — "how many skills do we have", "is this wired", "what is in the backlog", "does X exist". Also fire it immediately before quoting any count, and before publishing any claim that something is absent or has never run.

The audit is true at the instant you probe it. Everything below exists to keep that instant honest.

## Procedure

1. **Enumerate the scan surfaces before counting.** Mounts stack — one store reached through several symlinked paths, plus backups that shadow the live tree.
```bash
for p in <path1> <path2> <path3>; do printf "%-42s " "$p"; readlink -f "$p"; done
find <store> -name '<artifact>' | wc -l          # raw — may double-count
```
Then dedupe by resolved path in Python. This is the only number worth quoting:
```python
seen = {}
for dp, dn, fn in os.walk(root, followlinks=True):
    if '<artifact>' in fn:
        seen[os.path.realpath(os.path.join(dp, '<artifact>'))] = dp
print(len(seen))
```

2. **Canonicalise every queue before reporting its depth.** Build an identity key from the row's own fields, then count distinct keys.
```python
key = lambda r: (r.get('tool'), r.get('trigger'), r.get('action'))
print(len(rows), 'rows ->', len({key(r) for r in rows}), 'distinct findings')
```

3. **Stamp the window, then re-probe before publishing.** Record the observation timestamp inside the artifact. For any absence claim ("never wired", "never fired", "does not exist") run one fresh probe immediately before writing it out.

   **Counts printed by a producer are claims, not measurements.** A docs page, dashboard,
   or static surface file that displays "10 tools / 4 prompts" and lists endpoints is a
   producer of numbers, not a source of them — and a hardcoded number can only ever go
   stale. Re-derive each one from the primitive (`tools/list`, `prompts/list`,
   `resources/list`, a bare `curl -o /dev/null -w '%{http_code}'` per advertised route)
   and check whether the displayed value is computed or typed in markup:
   `grep -oE '(10|4)[^<]{0,40}(Prompts|Resources)' <page>.html` finding the literal
   means it will drift. A page can fetch some live data and still print stale counts and
   dead routes; its honesty in one block licenses nothing in another.

4. **Check for a consumer before recommending a gate.** For every queue or ledger you report on, name the process that drains it. If nothing drains it, that is the finding — not a missing feature.

5. **Commit only into a quiet tree.** Compare newest source mtime against now and wait for a quiet window; a commit taken mid-write captures a torn snapshot and its message describes a state that never existed.
```bash
find <dir> -newermt "-180 seconds" -type f ! -path "*__pycache__*"   # empty = quiescent
```

6. **Record reversibility with the resolution.** Move queued records into a `processed-<label>/` directory rather than deleting, and state the restore step in a receipt written beside them.

## Always-On Rules

- Dedupe by realpath before quoting any count or duplicate list.
- A queue of N rows may be one finding replicated N times — count distinct identity keys, not rows.
- Every absence claim carries its observation window. When reality moves after publication, append an **AMENDMENT** and leave the original sentence standing.
- An unconsumed queue is not a gate, it is an accumulation.
- Never commit mid-write.
- Resolution artifacts are additive: never rewrite another lane's receipt — write an addendum in a separate file.

## Pitfalls

- **Counting a store through `find -L`, or running `uniq -d` over basenames.** Symlinked mounts and stale backups re-report the same files as extra artifacts *and* as duplicates. A store that looks like 342 files with 78 name collisions is 218 files with 1 once deduped by realpath — the inflation is scan surface, not content.
- **Reporting backlog depth without identity canonicalisation.** Recurrence with no collapse step at the producer looks like a workload and is a defect: report it as one finding with a frequency, not as N tasks to drain.
- **Publishing an absence claim without a fresh probe.** Any concurrent lane can falsify it inside minutes. Order of operations: probe → stamp → publish → amend if it moves.
- **Quoting a documented count or endpoint instead of calling it.** A producer's number and an advertised route are both hypotheses; an endpoint listed on a page can 404 while the page stays plausible, and two routes can carry different counts of the same surface. Probe the primitive, not the prose.
- **Silently editing a finding after reality moves.** A corrected report with no amendment trail is untrustworthy; one with an amendment is evidence. Keep the original, add the correction above it.
- **Reading "no data" as "all clear".** An empty meter and a healthy meter look identical from a distance. Check whether the measurement has ever produced a reading at all.
- **Your push can be in flight while a sibling session rebases and pushes over you.** A backgrounded write that has returned no output yet has not necessarily failed — by the time you re-issue it the remote ref has already moved (your first push landed, a sibling's `pull --rebase --autostash` stacked its commits on top, and your local remote-tracking ref is now stale). A rejection reading `cannot lock ref 'refs/heads/main': is at <X> but expected <Y>` is that race, not a failure: `<X>` may be your own commit. Before concluding anything, `git fetch -q origin main` and compare `git rev-parse HEAD` against `git rev-parse origin/main`; re-push only when HEAD is genuinely ahead.
- **Never read the exit status through a pipeline.** `git push ... | tail -3; echo $?` prints `tail`'s status, so a rejected push reports `0`. Capture the real one (`git push ...; echo "exit=$?"`) or check `PIPESTATUS[0]` — and verify the outcome from the remote (`git ls-remote origin main`), never from the command that issued it. Same trap applies to `git commit | grep`, `systemctl restart | tail`, and any other check whose status you are about to trust.
- **Resolving a queue with `approve all`.** Batches staged at different times overwrite each other on the same entry; the newest silently erases the rest. Read them together, decide per item.

## Patching a file a sibling is editing

When a tool warns that the file you are about to patch was modified by another agent since
your last read, the warning is the finding: you are one of at least two writers and your
in-memory copy is already stale.

1. **Take your own named backup before any patch.** It is the only diff base you will have.
2. **Re-read the file, then diff against that backup** to see exactly what the sibling
   changed. Do not overwrite their work to reinstate yours.
3. **Re-apply only your hunk**, anchored on text the sibling did not touch.
4. **Verify the sibling's premise before deferring to their value.** A concurrent edit is not
   automatically better informed than yours: a sibling can set a constant correctly *and*
   justify it with a claim about another file that is false, in a comment that will read as
   provenance to everyone after them. Check the source their comment cites — if it disagrees,
   fix the value and the comment together.
5. **A sibling may have already closed part of what you were assigned.** The honest outcome is
   often "their half is done, mine is the remainder", and in a shared session reporting that as
   shared work is worth more than reporting it as yours.

**A test that mutates live state must restore the pre-image, verified.** Forcing a code path by
editing a real record — backdating a timestamp, clearing a flag, moving a row, renaming a file —
writes a falsehood into the system the moment the session ends. Capture the original value before
the edit, restore that exact value afterwards, and confirm the restore by reading it back. The
live state file is not scratch space, and the artifact a test leaves behind is the record the
next reader trusts.

## Running the same task twice at once

A job that writes to a shared output path (artifact directory, cache file, snapshot) is not
safe to run concurrently **with itself** — including through two entry points that look
independent but resolve to the same destination (an MCP tool and the CLI behind it, two
shells, a cron lane and a manual run). Observed: two simultaneous runs of one URL wrote the
same artifact directory, produced disagreeing frame counts from it, and paid the metered
provider twice for one fetch.

- **Key the lock on the target, not the caller.** A lock per entry point does not protect a
  shared destination; lock the artifact path itself so the second run waits.
- **Cache the successful result.** A target already resolved can return its stored result and
  skip the metered work entirely; keep an explicit force/refresh flag for when fresh data is
  genuinely wanted. This turns a repeated request from a cost into a lookup.
- **Read a mismatch between two runs as evidence of the race, not as a flaky lane.** Two
  results that disagree from one destination is the signature above; the remedy is
  serialisation, not retries.

### Cheap pre-flight on a file two agents are editing

When the file is large and the sibling's edits are unknown, marker counting beats a full diff:

```bash
grep -c "<my marker>" file      # is my work still present?
grep -c "<their marker>" file   # did they add something I should not clobber?
python3 -c "import ast;ast.parse(open('file').read())"   # does it still parse?
```

Distinct anchors are why two sets of edits can coexist — but that is luck, not design. Take a
timestamped backup before every write, and **never revert code you did not write**: a sibling's
fix in a shared file is a decision, so name it in your report and reconcile rather than undo it.

**A sibling's status description can be stale about your own work.** A peer report described a
change as "staged, not installed" while it was already live and verified. Treat a peer's
*status* claim (staged/pending/not done) the same as their negative finding: re-probe current
reality before acting on it, and correct the record so the next reader is not misled.

## References

- `references/pending-write-queue-resolution.md` — resolving a staged write-approval queue: read, anchor-match, decide, record.
