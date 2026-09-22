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
capability_tier: fed-agent-subagent
ecology_state: WARM
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

**Probe ownership before your FIRST write into a shared tree — not after the warning.** The
sibling-modification warning arrives *after* the damage, and when you are the one who wrote first no
warning fires for anyone. Before the first edit, look for another lane's work-in-progress staging
area in the same directory (`ls -a` for `backup-*`, `*-moved-*`, `PRE-hashes-*`, `DISPOSITION-*`,
`CONSOLIDATION-*`, `.pre-*`, `my-*-superseded-*`) and read its newest ledger. Finding one is the
cheapest possible detection, and it inverts your role: you become the independent auditor of a
declared change instead of a second writer racing it. If you skip this and write anyway, expect your
in-flight bytes to end up inside their backup as if they were the original (see Step 2).

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
  not the fix. Port the delta, drop the duplicate. Mind the distinction: restoring *their* artefact
  because a later step of theirs silently undid it is not re-adding yours — that is completing a move
  they already declared, and you should do it and say so. Re-adding a differently-shaped version of
  your own is the collision.
- **After every collision, re-run the affected tests.** Assume nothing of yours survived and nothing
  of theirs broke.
- **A sibling's partial edit can import cleanly and crash at runtime.** A reference to a constant
  nobody defined leaves the module syntactically valid, so an import check passes and every real
  invocation raises `NameError`. After a sibling touches a module you depend on, **execute** it — run
  its CLI and its suite — rather than reading it. Import-time success is not correctness, and a shared
  gate that raises fails *closed for every caller*, so the symptom arrives as downstream breakage
  rather than as the edit that caused it. A file whose mtime moved under you mid-session is not
  "probably fine"; it is unverified until it runs.
- **Snapshot the artifacts a shared task writes before you test-fire it.** Hash or copy the output
  files, fire the job, then re-check the hashes. A renderer that writes a content-addressed file plus
  a stable-named copy will otherwise destroy the previous run's artifact — the exact path a delivery
  contract names — and that destruction is invisible unless you kept the before-state to compare
  against. The same snapshot is what lets you prove, afterwards, that a test-fire left production
  untouched.
- **Read state back from the store.** A tool's success response says the call was accepted, not that
  the state changed.
- **An agent's account of what it changed is not evidence of what changed — diff the artifact.** A
  lane reporting its own edit can misremember it, and the report and the file then disagree in a way
  that reads as drift. Measured: a report of a config edit named three renumberings; the diff showed
  three different source values — all three wrong in the report. The file is the witness, the
  narrator is a hypothesis. When they disagree, trust the diff and state which one you used.
- **An exclusion with no owner is a rot hazard.** "Do not touch \<file\>" prevents a collision and also
  guarantees the file stays stale: the child that discovers it needs updating files the finding and
  moves on, and no one is tasked with it. Every exclusion must name an owner, and the close-out must
  route the excluded file's findings to that owner. Measured: a child was forbidden one manifest file
  while its own finding was that republishing that file would regress a live record — the file stayed
  wrong until the coordinator picked it up by hand. An exclusion list without owners is a list of
  places the work will silently stop.
- **Before auditing a shared config, read the working tree — not HEAD.** A change written by another
  lane minutes ago is invisible to any audit that reads committed state, while the running service
  has already loaded it. Check the file's mtime against the service's process start, and run
  `git status` / `git diff --stat` before citing its contents. An uncommitted edit is live
  behaviour, so a report built from HEAD describes a system that is not running.
- **A convention applied in one act and contradicted in the next is an auditability defect.** When a
  lane normalises a class of entries one way — demote to a low priority rather than delete — and its
  own audit, an hour later, proposes removing that same class outright, two policies now govern one
  file with nothing recording which was intended. Name the convention explicitly and hold the second
  act to it, or the file stops being able to distinguish intent from accident. Disposition policies
  are a governance choice, not a per-edit preference.
- **Another lane's `verified: true` row is a claim about one moment, not the file state now.** A
  consolidation ledger, manifest or receipt asserts what its author measured; a later step by the same
  or a third lane can undo it while the row stays green. For every entry a ledger declares
  `CONVERGED` / `DONE` / `verified`, resolve the path and hash it yourself before relying on it, and
  when the two disagree say which one you read. A file can stand in contradiction to a green ledger
  for minutes, and anyone acting on the ledger alone inherits the error.
- **Your own in-flight writes will be captured as another lane's "original".** A consolidation or dedup
  pass snapshots whatever bytes are on disk — including a file you are midway through writing. Its
  backup then records *your* draft as the pre-change state, its rollback set is wrong, and its report
  understates what it displaced. Two counters: keep your own pre-change copy under your own name so a
  true original survives somewhere, and when you find a mis-capture, repair it by recovering the file
  from version control and *proving* byte-equality to the committed object
  (`git hash-object <recovered>` equal to `git rev-parse HEAD:<path>`) rather than asserting a hash.
  Do not edit the other lane's ledger to fix it — that artifact is theirs and may still be being
  written. Publish the correction where they will find it and name them the owner.
- **Before writing "content lost / not recoverable", search for it — a loss declaration closes the
  search and is itself the harm.** A sibling that finds a path it expected to own will record your
  version as unrecoverable. Check the cheap places before accepting that: your own tool result
  (`verified: true` on the write), a staging or cache dir, a delegation log, and any copy you
  published under a nearby name. Then publish the recovered copy under a filename the other record
  itself nominated rather than a name of your choosing.
- **On a contested document path, append — never overwrite.** A designation record, manifest or
  ledger that two lanes both want to write is the same defect as a module two lanes both want to own:
  two writers, one artefact. Add a section and leave the other's intact; if you must correct a peer's
  record, correct it in your appended section and let theirs stand. Use a distinct filename for a
  full alternative version.
- **`write_file` through a symlink writes to the TARGET, not the link.** When a consolidation lane
  creates a symlink from T1 to T2, and you `write_file(path=<T1-link>)` with deprecation stubs,
  the tool resolves the symlink and overwrites the canonical T2 file. The T1 link then reads back
  your stub from T2. You have clobbered the authoritative tree while believing you were writing a
  shadow copy. Fix: before calling `write_file` on any path in a shared tree, run
  `readlink <path>` — if it resolves to a target you do not own, create a temporary file and `mv`
  it over the link instead.
- **A module file and a package with the same basename shadow each other.** `chron.py` (a module)
  sitting beside `chron/` (a package) on the same `sys.path` makes `import chron.chron_store`
  fail with `'chron' is not a package`. The shadow is invisible to `ls` and `git status`. Detect
  it by running `python3 -c "import <name>; print(<name>.__file__)"` and confirming the result is
  a directory `__init__.py`, not a sibling `.py` file. The fix is a rename, not a re-ordering of
  `sys.path`.
- **File size is not a monotonic signal of which copy is newer.** A corrected copy that stripped
  dead code can be smaller than the defective original. In the session: AAA copy 13927 B,
  canonical 3011 B — size heuristic picks the wrong file. Always classify by provenance
  (systemd ExecStart, `git log`, import resolution), never by size or date alone.

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

### A validating writer over a shared store

When one component gates every write to a shared store — a config validator, a schema check, a policy
engine — its verdict is a function of the **whole store**, not of your change. That inverts the
intuition in three ways worth knowing before you draft anything:

- **Probe the gate's own verdict BEFORE drafting.** Run the writer's check-only mode first. If the
  store already carries errors, a fail-closed writer refuses *every* change — including yours, and
  including changes unrelated to the bad entries — because it validates the merged result, not your
  patch. A patch built before that probe is a wasted turn, and it looks like your patch failed when
  nothing about it was judged.
- **Classify the errors with the writer's own predicate, not by reading its output.** Split them into
  baseline (present before you touched anything) and patch-caused. Only the second set is yours to
  fix. The first set is a report you owe the store's owner, plus a proposed repair — not a mess to
  absorb silently.
- **Never route around a fail-closed writer with a direct edit.** Every direct edit widens the gap
  between the store and the gate, so the gate stays shut for everyone and the baseline grows each
  time someone bypasses it. A direct edit is usually what created the baseline. Take the reversible
  repair instead.
- **A rejection is not evidence the thing rejected is broken.** A validating writer's vocabulary lags
  what the runtime actually supports: a target the runner handles correctly every day can be missing
  from a hardcoded allow-list, so a healthy, currently-working entry reports as an error. **Read the
  observed behaviour** (last succeeded, last error) before touching a working config. The repair is to
  widen the gate, never to change the thing that is already working.
- **Widen by SHAPE, not by adding another literal.** An enumerated allow-list cannot track a family of
  values it never anticipated, so each new variant re-opens the same gap and the list grows one
  incident at a time. When the rejected values are all one pattern, accept the pattern (`^<proto>:\d+`
  plus the named tokens) and keep the literal set only for genuinely irregular cases. Before you do,
  confirm from the runtime's own resolver that the pattern is real — a documented shape in the
  scheduler's source is evidence; your inference from the values you happened to see is not.
- **A field the gate REQUIRES that no runtime code reads is the mirror of a false rejection.** Grep for
  the consumer, not the declaration: a mandated key can appear in the schema, in every validator error
  message, and in the docs while nothing at all reads it — the delivery path reads a sibling field and
  has never heard of it. Jobs written after such a rule are permanently invalid and nobody notices,
  because the field is inert either way. **Before backfilling one across many entries, prove whether
  anything consumes it** — then derive the value mechanically from an observable so the backfill is
  reproducible (`deliver` is local/absent → machine, else human), and **report that the field is
  inert.** Conforming restores the writer; it does not make the requirement meaningful. Saying so is
  the difference between a repair and a plausible-looking change that quietly laundered a dead rule
  into an apparently-enforced one. Whether to wire it or drop it is the owner's decision.
- **A refused write is not a no-op.** A fail-closed writer commonly takes its backup BEFORE it
  validates, so the backup directory gains entries from patches it rejected. Do not read a fresh
  backup as evidence a write landed — read the receipt, which a refused patch never writes.
- **Hash the exact field, not just the file, immediately before writing.** A field replaced wholesale
  does not merge: the concurrent writer's version is deleted, and your write reports success while
  doing it. Re-check right before the write, and on drift ABORT and rebuild on the new text. Keep the
  base text you built from on disk so the check is a byte comparison, not a memory. A long free-text
  field is the highest-risk case, because it is the thing most lanes are asked to update.
- **When the re-read shows a sibling already covered part of your change, drop that part.** Re-adding
  it is duplication dressed as diligence, and it leaves two restatements of one rule in a field that
  has to stay legible. Keep only what is genuinely absent, and say so in the report — the redundant
  section you deleted is itself information about what the other lane already did.
- **Repairing the gate is a higher tier than using it.** Widening an allow-list or backfilling a field
  the gate now requires is a mutation of the gate itself, so it is the owner's decision rather than
  self-service cleanup. Propose it as one explicit choice — repair (reversible, with a rollback
  command) versus leave it and accept the workaround — and state what each costs. Capability to write
  the store is not authority to change the rule that governs it.
- **Hash the exact field, not just the file, immediately before writing.** A field replaced wholesale
  does not merge: the concurrent writer's version is deleted, and your write reports success while
  doing it. Re-check right before the write, and on drift ABORT and rebuild on the new text. Keep the
  base text you built from on disk so the check is a byte comparison, not a memory.

## Step 3.5 — one `.git`, two writers

A git repository is a shared mutable store, and a **history rewrite** (`filter-repo`, `rebase`,
`branch -D`, `gc --prune=now`) moves refs that another lane may be reading. The signature is that
**the target moves between your own two commands** — a ref you resolved minutes ago now resolves
differently, and only one of the two readings can appear in your report.

- **Freeze readers, then rewrite, then audit.** One writer at a time. The writer declares `DONE` with
  a receipt (new ref heads, store size, the rewrite's own maps); only then does an audit run — on the
  frozen state, never alongside the rewrite.
- **Pin anything the rewrite can prune BEFORE it starts** — dangling commits, dropped stashes,
  worktree heads. An audit or an `fsck --dangling` listing is a report, not a lock; the next
  `gc --prune=now` deletes it. Pin with `git update-ref refs/keep/<name> <sha>`, then verify with
  `git cat-file -t <sha>`.
- **Take your own pre-rewrite snapshot if you are the auditor.** Do not assume the writer's backup
  covers what you need: a bundle of `--all` omits `refs/stash` and `worktrees/*/HEAD` unless they are
  listed. Check `git bundle list-heads`, and prove the objects are inside by bare-cloning the bundle.
- **When two probes disagree, re-run before reconciling.** A changed value with an unchanged command
  is a concurrent write, not a contradiction in your data — check the clock and re-probe instead of
  averaging the two readings into a claim.
- **Publish against a stated snapshot.** Every figure carries the state it was read from. A verdict
  over a tree that changed mid-pass is not a verdict.

### N children, one working tree

Fanning several subagents at one repository is the same one-`.git`-two-writers problem at higher
fan-out. Three things break that do not break with two writers:

- **Children commit to whatever branch is checked out; they do not create branches.** If the tree sits
  on a feature branch, every child's work lands there — not on `main` — and nothing merges it. Name the
  branch in the task strings, and at close-out state where the work actually is and whether it was
  pushed, rather than assuming "committed" means "in the trunk".
- **Each child stages only its own paths.** A child running `git add -A` commits another child's
  half-written files and the coordinator's own in-flight edits. Require `git add <your path>`, and ask
  for a `git status --porcelain` excerpt in the return; the parent reconciles the tree.
- **Stamp the baseline.** Have each child record the commit it started from. "Committed and pushed"
  reported against a HEAD that moved several times during the run is not evidence of a clean delta —
  only a start hash plus a per-path diff is. Expect the coordinator's own commit to land mid-run, and
  name the two readings rather than reconciling them into one.
- **Check a deliverable path is trackable before assigning it.** A directory the repo `.gitignore`s
  refuses `git add` outright, and a child that works around it with `git add -f` has committed
  something the repo declared ignored. Either place the artifact outside the ignored tree or authorise
  the force-add explicitly — and record which you chose, because the next reader will assume the
  artifact was wanted.

### What the rewrite does to your reads (`filter-repo`)

Beyond the paths you asked it to drop:

- **It removes the `origin` remote** — `remote.origin.url` comes back empty and every fetch/push fails
  until it is re-added. Restore it as part of the rewrite, not after someone reports a broken push.
- **It rewrites every ref** — `main` and all tags move along with the branch you were thinking about, so
  "main's hash will not change" is not a promise you can make. Publish which refs moved (`ref-map`).
- **It clears reflogs** — objects that were recoverable through a reflog become prunable.
- **It rewrites the rescue refs created during the same window.** A `refs/stash` or `refs/keep/*` made
  while the rewrite is running is itself mapped — `ref-map` carries `refs/stash <old> -> <new>` — so a
  safety SHA you copied from the writer's own output is stale the moment the rewrite finishes. Keep
  rescue state **outside** the ref set being rewritten (a second clone, or a bundle), and re-resolve
  every pin against `ref-map` after the writer declares `DONE` before quoting any hash.
- **It leaves `.git/filter-repo/{commit-map,ref-map,changed-refs,first-changed-commits}`** — the
  commit-map is the **only** old→new hash bridge for seals, tag citations and ledger entries that quoted
  an old hash. **Copy it out of `.git` before anything else touches the repo** — it lives inside the tree
  you are about to gc.
- **Scope it to the smallest thing that works.** A blob on one unmerged branch is a branch rewrite, not
  a rewrite of `main` plus every tag. Count unmerged work before deleting a branch to reclaim space
  (`git rev-list --count main..HEAD`).

**A backup bundle does not carry unreferenced objects.** `git bundle create x.bundle --all` covers refs
only — dangling commits, dropped stashes and orphan worktree heads are silently omitted, which is
precisely the set under threat. Name them explicitly (`refs/stash`, `worktrees/*/HEAD`) or they are not
in the backup. `git bundle verify` proves **integrity**, `git bundle list-heads` proves **coverage**, and
the only proof of **recoverability** is a bare-clone into a scratch dir plus `git cat-file -t <sha>` per
object — assert recovery only after that answers.

**"Object pruned" ≠ "work lost."** Work is routinely stashed, popped and committed by another lane
before the prune. Test for landed before writing a loss into any report: compare the lost object's own
recorded per-file deltas with what later commits added to the **same paths**
(`git show <later> --numstat -- <path>`) — a recorded `+82` matching a later `+81/-1`, or `+42` against
`+42`, is the work landing, not a coincidence. A path that returns 0 lines has usually **moved**
namespace; resolve its current location before calling the content absent.

Read what a lost object **contains** by diffing it against **its own base**, never against HEAD: once
HEAD has advanced, `git diff --stat HEAD <stash>` renders the whole tree — hundreds of files, tens of
thousands of deleted lines — and buries the handful of paths that actually matter.
`git diff --name-status <sha>^1 <sha>` is the delta.

**A derived index is not evidence of absence.** A memory graph, vector store, or RAG index is a lossy
projection of a source that is itself derived; a zero-hit lookup there says nothing about git — or about
any other system of record. Answer a git question with git (`git log -- <path>`,
`git show <commit> --numstat`). Declaring an "irreversible loss" from the wrong index is not a harmless
overstatement: it is the harm, because it closes the search.

**A node is not a mirror until probed.** `.git/shallow` present, or a partial-clone filter such as
`[blob:none]`, means a truncated history: that node is a consumer, not a recovery floor. Do not list it
among surviving copies.

**`git tag -f <name> <sha>` without `-m` opens an editor** and hangs a non-interactive shell; and
`git bundle create <f> <bare-sha>` refuses with *"Refusing to create empty bundle"* — bundle a ref name.

Probe recipes for all of the above: `references/recovery-verification.md`.

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
