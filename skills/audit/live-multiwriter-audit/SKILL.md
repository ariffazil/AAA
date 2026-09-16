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
  - "verify this report"
  - "second reader"
  - "correction report"
  - "peer report audit"
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

   The same test applies to a **control**, and this is the more expensive version. A ratified
   doctrine, or a skill that describes a check in precise and correct detail, is not enforcement:
   ask which process actually executes it, and when. A protocol with no runtime behind it is the
   worst shape in the library, because it reads as coverage — nobody builds the check, and the
   fault it describes runs unwatched for as long as the documentation stays convincing. Report
   "doctrine present, executor absent" as the finding itself. Prefer wiring an existing owner over
   minting a new artifact: a rank of ratified-but-unexecuted doctrine is a symptom of
   documentation outrunning enforcement, and the cure is one running check, not another document.

5. **Commit only into a quiet tree.** Compare newest source mtime against now and wait for a quiet window; a commit taken mid-write captures a torn snapshot and its message describes a state that never existed. Probe at both levels — files, then processes:
```bash
find <dir> -newermt "-180 seconds" -type f ! -path "*__pycache__*"   # empty = quiescent
find <dir> -newermt "-6 minutes" -type f | head                          # who is writing, and where
ps -eo pid,etimes,cmd | grep -E 'hermes|kernel_runner' | grep -v grep    # live sibling sessions
stat -c '%y %n' <shared-store>.db-wal <shared-store>.db 2>/dev/null      # store touched this minute?
```
   A second live session plus a store whose `-wal` moved inside the last few minutes means **do not mutate** — hold and say so. Report an authorized-but-racy hold as a *timing* verdict, never as *awaiting human authority*: the two are different findings, and conflating them parks a task on a sovereign decision nobody needed to make. When the hold lifts, re-probe rather than resuming from your earlier reading.

6. **Record reversibility with the resolution.** Move queued records into a `processed-<label>/` directory rather than deleting, and state the restore step in a receipt written beside them.

## Always-On Rules

- Dedupe by realpath before quoting any count or duplicate list.
- A queue of N rows may be one finding replicated N times — count distinct identity keys, not rows.
- Every absence claim carries its observation window. When reality moves after publication, append an **AMENDMENT** and leave the original sentence standing.
- An unconsumed queue is not a gate, it is an accumulation.
- A peer's report is a claim, not evidence: re-derive each number yourself, or mark it inherited and name the source you took it from.
- A hold inherits from the newest revision of a report, not the most-quoted one — reconcile the peer's own later corrections before repeating an earlier section's HOLD.
- Never commit mid-write.
- Resolution artifacts are additive: never rewrite another lane's receipt — write an addendum in a separate file.

## Pitfalls

- **Counting a store through `find -L`, or running `uniq -d` over basenames.** Symlinked mounts and stale backups re-report the same files as extra artifacts *and* as duplicates. A store that looks like 342 files with 78 name collisions is 218 files with 1 once deduped by realpath — the inflation is scan surface, not content.
- **A count that disagrees with the census is your command shape until proven otherwise.** One store yields three "true" numbers depending on the walk: `ls -1` counts top-level entries only and hides dotfiles, `find` without `-L` never enters symlinked subtrees, `find -L` walks the real tree — measured on one skills root in the same minute, 162 / 124 / 409, where only the last is loadable. Before escalating a count discrepancy as a finding, re-run with `-L`, with the artifact `-name` filter, and against the census: a missing `-name` filter counts every node in the tree. Your probe is the first suspect, not the report.
- **Reporting backlog depth without identity canonicalisation.** Recurrence with no collapse step at the producer looks like a workload and is a defect: report it as one finding with a frequency, not as N tasks to drain.
- **Publishing an absence claim without a fresh probe.** Any concurrent lane can falsify it inside minutes. Order of operations: probe → stamp → publish → amend if it moves.
- **Quoting a documented count or endpoint instead of calling it.** A producer's number and an advertised route are both hypotheses; an endpoint listed on a page can 404 while the page stays plausible, and two routes can carry different counts of the same surface. Probe the primitive, not the prose.
- **Silently editing a finding after reality moves.** A corrected report with no amendment trail is untrustworthy; one with an amendment is evidence. Keep the original, add the correction above it.
- **Publishing a finding about a file that is still being edited.** Stamp `sha256sum` and `stat -c %y` when you read it, re-stat before you publish, and name the revision your finding applies to. An actively-working sibling repairs the same class of defect as they go, so a verdict about a revision that has already been replaced is not a finding — it is a false alarm whose cost is the owner hunting for something that is not there.
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
5a. **When a sibling closes your finding mid-audit, audit their closing.** Their fix is the newest
   instance of the class you were measuring and therefore the likeliest to carry the same defect —
   a document declaring that reasoning grants no authority can itself be published on reasoning
   alone. Check whether their artifact carries the same class of receipt you were asking everyone
   else for (an authority record, a seal identifier, a session stamp) and report that as part of
   your finding, rather than reading "someone fixed it" as closure. Check the receipt identifier
   against the *sibling artifacts of the same directory*: absence is only measurable against a set
   that otherwise carries one, and a lone artifact without one is invisible.
6. **Re-read before you conclude, and cite the revision.** Capture `sha256sum` / `stat -c %y` with
   the read, re-stat immediately before publishing any finding about the file, and name the short
   hash in it. If the hash moved, your analysis describes a revision that no longer exists —
   re-read and redo it rather than shipping the old verdict.

**A replication you wrote can be born stale.** Extracting a predicate into a throwaway script to
prove whether it can ever fire is the right move — but bind it to the revision you captured. Run
against a file that was rewritten while the script was being written, it tests nothing, and the
verdict ("this check can never fail") is about code that was already gone.

**A test that mutates live state must restore the pre-image, verified.** Forcing a code path by
editing a real record — backdating a timestamp, clearing a flag, moving a row, renaming a file —
writes a falsehood into the system the moment the session ends. Capture the original value before
the edit, restore that exact value afterwards, and confirm the restore by reading it back. The
live state file is not scratch space, and the artifact a test leaves behind is the record the
next reader trusts.

### Auditing the detector itself

When the thing you are auditing is a check, sweep, gate, or sensor, its verdict is a claim about
reality and gets audited like any other claim. Detectors fail in two symmetric directions: **silent
false-PASS** (never fires) and **latent false-FAIL** (fires wrongly the moment inputs move).

- **A marker probe can pass on the echo of its own request.** When the instrument searches its
  output for a marker string and the thing under test logs its own request, the request itself
  satisfies the search — a PASS with no answer behind it. Strip lines that still carry the request
  before matching, and prove the probe discriminates by running it against a known-dead input.
- **After you edit a predicate, re-run BOTH controls.** The fix for a silent false-PASS is the most
  likely source of the next false-FAIL: reordering the checks moves which class of incidental noise
  the predicate fires on. Re-run the must-trip fixture and the must-not-trip fixture after every
  edit to the predicate, not only when you first write it, and confirm the verdict distribution
  changed only where you intended.
- **An alarm that fires on incidental noise trains the reader to skip the whole list.** A predicate
  matching a string that also appears in a health/telemetry error surfaces a healthy component as
  broken every cycle; the cost is not the false positive itself but the credibility of the genuine
  FAIL scrolling behind it.
- **A check that has never fired is not evidence.** "It passes every cycle" is indistinguishable
  from "its predicate can never be satisfied" until you make it fail on purpose. Plant a fixture
  that must trip it and confirm non-zero exit plus the expected message; then run a healthy fixture
  and confirm it does NOT trip. One direction proves half a sensor.
- **Validate a schedule/interval parser against hand-computed windows before trusting its SILENT
  list.** A staleness check that mis-expands `*/n`, a day-of-week restriction, or a month field
  produces confident false alarms — and a false SILENT costs more than a missed one, because it
  burns the human's trust in every later verdict. Pick windows whose expected count you can work
  out on paper (a daily job across 13.5 days → 13; a weekday-restricted job across 23 days → 3; a
  healthy daily job last fired 9h ago → 0, which must read OK) and assert the parser reproduces
  them. Ship that as a `--self-test` flag on the tool itself so the next change re-proves it.
- **A metric built on a cutoff is a threshold reading, not a measurement.** "Count the items sharing
  at least N tokens" has its size set by N: lower the cutoff and the reported rate rises with no
  change in reality. Before quoting such a figure — or accepting agreement between two of them —
  ask what the denominator is. Two threshold-only rules landing on the same number means the
  cutoffs agree with each other, which is a statement about the code, not about the corpus. Score
  overlapping-set claims as a proportion instead, state the cutoff and corpus size beside the
  percentage, and check that the shared tokens are content rather than metadata: embedded routing
  annotations leak into the compared strings and manufacture clusters that vanish once the strings
  are de-annotated.
- **Compare like units.** A predicate mixing two quantities is unsound even when it never fires:
  `recursive_file_count <= len(os.listdir(root))` pits files-under-tree against entries-at-one-level,
  so any healthy tree with few files per top-level entry can trip it. Write down the unit on each
  side of a threshold before trusting it; if they differ, the check compares nothing. A latent
  false-FAIL far from its trigger today is a time bomb that a green run will never reveal.
- **An unwired test is prose in a .py file.** A regression suite nobody invokes protects nothing.
  Wire it into the periodic runner's own self-test section so it executes every cycle, then prove
  the wiring by pointing the runner at a synthetic failing suite and confirming it reports FAIL and
  exits non-zero — unexercised wiring is a third unverified layer.
- **Unit cases plus a harness test still do not prove end-to-end classification.** A decision
  function can discriminate every fixture and the runner can return FAIL on a planted assertion,
  while the production path (parse → derive → resolve → classify → exit code) has never once been
  run against a known-bad input. Drive the shipping CLI itself against a synthetic input through an
  environment override, assert the known-dead case surfaces as dead, and clean the fixture up
  afterwards. Order the verification ladder explicitly — unit → harness → end-to-end negative
  control — and say which rung you actually reached.
- **Alarm taxonomy: unpayable conditions belong at INFO, not a permanent WARN.** A condition that
  can never be cleared (a deliberate symlink farm, a debt scheduled for a migration) emitted as WARN
  every cycle trains the reader to skip the WARN list, and the genuine FAIL scrolling behind it stops
  being read. Give the runner an explicit declared-set reported at INFO, keep real defects at FAIL,
  and raise a level only when a real defect would otherwise be invisible.
- **Never declare a tree empty from a plain walk.** A root whose content arrives through symlinks
  returns zero without `-L`; report the trap, never the zero. Scope the check per-root, because a
  sensor watching one root cannot catch a claim made about another.
- **Patch the detector in the same pass, name the revision, and do not revert the owner's fix.**
  A sibling may be editing the same file; capture `sha256sum` / `stat -c %y` with the read, re-run
  after the patch, and confirm the verdict distribution changed only where you intended.

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

### Attributing a review of "your" output when sessions are concurrent

An external model's review of what "the agent" said is a claim about a **session**, not about you.
When several sessions run the same question in parallel, the review silently samples one of them,
and every quantity in it may belong to a sibling.

Attribute before you accept or dispute anything:

```python
import sqlite3
c = sqlite3.connect('file:/root/.hermes/state.db?mode=ro', uri=True); cur = c.cursor()
for r in cur.execute("select id, source, title, last_activity_at from sessions "
                     "order by last_activity_at desc limit 10"):
    print(r)
```

- Match the review's **distinctive quantities** — counts, phrasings, named artifacts — against
  the recent sessions. A review can be accurate about the system and still be reviewing a
  different agent's reply than the one you sent; the second is invisible until you look at the
  session list, and it makes both defending and accepting the wrong move.
- Do not defend a claim you never made. Do not quietly accept one either — say which session it
  came from and what that session did. A wrong attribution left standing poisons the human's
  model of what this agent is.
- **Split the attribution from the diagnosis.** A reviewer's structural finding can be correct
  about the system while its attribution is wrong. Adopt the diagnosis on the evidence you can
  independently verify; reject the attribution on the evidence you have. Dismissing a whole review
  because one quote is misattributed throws away the real signal, and the signal is usually the
  expensive half.
- State the split to the human plainly: "that part is another session's reply; the pattern it
  names is real and I verified it here" — then show the verification.
- **Sign your own artifacts with session id + host, not a role name.** With many sessions running
  the same questions on one host, `Actor: <agent>` disambiguates none of them, and a later auditor
  cannot tell which session's numbers a report describes. Put session id and hostname in the header
  of every report, receipt and commit body you write. It costs one line and it is the only thing
  that makes your own finding attributable — and the moment you need it, you are usually looking at
  a peer's audit of a reply that was not yours.

### Verifying a peer's correction report

When a peer lane hands you a correction — "that number was wrong, here is the right one" — the
report is a claim like any other, and the audit is cheap. Re-derive every number on disk.

1. **Re-derive each number; never accept a correction because it sounds more careful.** A report
   can be right about the headline and wrong about the remedy. Verify the dose, not the tone —
   especially when the correction changes *who* has to act (a human merge decision vs a mechanical
   re-sync of stale copies).
2. **Say which numbers you did not re-derive, and why.** A verification receipt that silently
   inherits a value it never measured repeats the defect it is auditing. Name the substitute (a
   document read, a different lane's probe) and mark it inherited.
3. **Reconcile the peer's HOLD list against their own later sections.** A hold the peer has since
   resolved gets carried forward by everyone who quotes the earlier section, and parks a task on a
   decision nobody needs to make. Read the newest section of the newest report first.
4. **When a document quotes a producer snapshot, compare its refresh stamp to the live reading.**
   A registry written by a periodic cron is a point-in-time claim: if the last run predates the
   live census, the document is quoting a stale figure as current. Name both numbers and say which
   one is the source of truth.
5. **Write your findings as an addendum in your own file.** Never rewrite the peer's receipt to
   insert your correction — additive artifacts only, and cite the revision you audited.
6. **Resolve which repository a cited hash belongs to before calling it missing.** A commit id is
   meaningful only inside its own repo, and a federation keeps several side by side (each organ has
   its own `.git`). `git -C <wrong-repo> cat-file -t <sha>` answers `unknown revision` for a hash
   that is perfectly valid next door, and that reads as a fabricated receipt when it is actually a
   wrong search root — the same mistake recurs independently across agents, in both directions. Run
   `git -C <dir> rev-parse --show-toplevel` on the file's path and let the path choose the repo,
   rather than inferring it from the filename or from the tree you happen to be standing in.
7. **A peer's figure that matches yours is not corroboration until you know both denominators** —
   see the threshold-reading bullet under *Auditing the detector itself* for why agreement between
   two cutoff-based metrics proves nothing. What is specific to the peer context: never silently
   adopt their figure in place of your own, and never leave theirs unqualified beside yours. Quote
   both with their cutoffs and say which one you would route on, because a reader cannot tell which
   of the two was measured.

## References

- `references/pending-write-queue-resolution.md` — resolving a staged write-approval queue: read, anchor-match, decide, record.
