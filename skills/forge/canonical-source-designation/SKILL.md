---
name: canonical-source-designation
description: "Use when a module exists in several trees; pick canonical."
version: 1.0.0
triggers:
  - the same module exists in two or more directories
  - reconcile divergent source trees
  - one canonical source per module
  - which copy actually runs
  - dedup a code tree
  - consolidate a duplicated organ or service tree
  - a tree is documented in one place and executes from another
  - symlink a duplicate tree to its canonical copy
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Canonical Source Designation

When one module exists in N trees, the work is not "delete the older copies". It is: **prove which tree
executes, classify each diverged module by capability, converge the safe ones, HOLD the unsafe ones,
and leave a record someone else can audit.** Getting this wrong silently deletes reasoning that was
deliberately removed, or re-introduces a defect a previous repair had killed.

Deliverables of a pass: (1) a designation record, (2) the code changes, (3) hash-backed preservation
sets, (4) rollback commands, (5) open items each with a named owner.

Run `scripts/tree_divergence_probe.py` for Step 1, and read `references/divergence-triage.md` when a
specific pair is genuinely hard to call.

## Step 0 — designate by measured executing path, never by documentation

Documentation naming a path is not evidence that path runs. A README, a cron-card "evidence path" or
a comment can point at a tree that stopped executing days ago, which is exactly how a dead copy stays
plausible. Measure instead:

```bash
# 1. What do the service units actually execute?
grep -H '^ExecStart' /etc/systemd/system/<svc>-*.service
#    (include WorkingDirectory= and Environment= — a relative ExecStart resolves against them)

# 2. Which package does an import resolve to, under the SAME path the unit sets?
PYTHONPATH=<same as unit> python3 -c "import <pkg>; print(<pkg>.__file__)"

# 3. Is the designated tree the one actually serving?
curl -s http://127.0.0.1:<port>/health

# 4. Confirm the suspect tree has no executor:
grep -rl '<suspect-path>' /etc/systemd/system/ | head
```

The tree with the ExecStart lines is canonical. Record the commands and their output in the record —
the designation must be reproducible by a reader who trusts nothing.

**A stale copy can be structurally unimportable and still look documented.** If the suspect tree
contains a module whose name shadows the package (a flat `chron.py` next to a `chron/` package), any
absolute `chron.` import from that directory fails with `'chron' is not a package`. Reproduce that
failure on the *pristine* copy before citing it — it is the strongest available proof that the
divergence had zero live impact, and it is a reason not to "fix" the shadowing inside a dedup pass
(renaming a module named by scheduled-job prompts is a larger blast radius than the dedup).

## Step 1 — inventory every co-named file and measure the divergence

Hash-based census, not eyeballing. See `scripts/tree_divergence_probe.py`. The core measurement is a
**line-level** diff, because byte size lies:

```python
import difflib
old = open(f"{tree_a}/{name}").read().splitlines()
new = open(f"{tree_b}/{name}").read().splitlines()
old_only = [l for l in difflib.unified_diff(old, new, n=0)
            if l.startswith('-') and not l.startswith('---')]
```

Report, per module: bytes in each tree, sha256, `old_only` count, `new_only` count. Also count the
byte-identical set — those prove the trees were once one tree. And check **git history per path**, not
per repo: a single bulk commit touching all the diverged copies is the signature of a frozen snapshot.

## Step 2 — classify by capability, then decide

| disposition | test | action |
|---|---|---|
| `IDENTICAL` | byte-identical | converge, no content question |
| `STRICT_SUBSET` | one side's unique lines = 0 | converge; the winner lacks nothing |
| `SUPERSEDED_NOT_MERGED` | loser's unique lines are all *superseded versions* of canonical lines | converge, but record WHY — must never be re-merged |
| `DIVERGED_INCOMPATIBLE` | **both** sides carry lines the other lacks | **HOLD** — read both, decide per module |
| `TREE_ORIGINAL` | exists in exactly one tree, has live consumers | designate that tree the owner; do not move |

**Size is not a classifier — the superseded copy can be the LARGER one.** A module whose canonical
form became a thin delegating entry point (scheduler shim over one shared implementation) is far
smaller than the duplicate it replaced, which still carries the full original implementation. Picking
"the bigger file" would select the defect. Same for recency: a copy can be both stale *and wrong*, not
merely older — check it against the current data model rather than against its own date.

**Verify the loser's unique logic line-by-line before calling it a subset.** Grep the unique lines for
executable content (a `def`, a constant, a branch). If the only unique lines are docstrings, comments or
blank lines, the subset claim holds and you must say that explicitly, because "nothing is lost" is a
claim that needs evidence, not an assumption.

### The `SUPERSEDED_NOT_MERGED` trap — the disposition that matters most

When the duplicate's unique logic is *deliberately-removed defect*, converging is right and re-merging
is catastrophic. You must record it as such, because the structural test fails: this is not a strict
subset, and a future reader who diffs will see "unique logic" and helpfully restore it.

Write the reason in the record, one row per capability, in the form *what the duplicate did → why it
is refused*. Refused classes worth naming explicitly when you find them:

- **minting a verdict from absence of evidence** — deciding a claim held because a calendar date
  passed, or because a search backend was unreachable. Turns "I did not check" into a scored result.
- **rewriting an append-only record in place** — destroys the belief snapshot later calibration is
  audited against. Canonical form keeps the immutable record and writes a *separate* result that
  references it.
- **a second full implementation of a gated path** — two writers, two log schemas, ambiguous joins.
  Canonical form is one implementation plus a scheduler entry point that gathers no evidence.
- **unconditional append in a loop** — N cycles append N copies of one finding, inflating counts with
  no new information. Canonical form dedups on a stable content fingerprint.
- **ignoring a `dry_run` flag** — a dry run that mutates is not a dry run.
- **reporting only deltas** — an all-zero delta summary reads the same on a quiet day and on a silently
  broken run. Canonical form reports status plus both delta and absolute state, so a reader can
distinguish idle from hollow.

A read-side expression can also be *wrong on current data* rather than merely older: a filter on a
field the current writer no longer updates returns an empty list forever, with no error.

## Step 3 — converge with a reversible move, and state the symlink caveat

Move-aside then link, keeping the displaced bytes:

```bash
cp -p <dup> <preserve-dir>/<name>     # preserve BEFORE removing
rm -f <dup> && ln -s <canonical>/<name> <dup>
```

Then verify what each link resolves to and that bytes read through it hash equal to the target —
all of them, not "looks right":

```python
import os, hashlib
a = hashlib.sha256(open(link,'rb').read()).hexdigest()
b = hashlib.sha256(open(os.path.realpath(link),'rb').read()).hexdigest()
assert a == b and os.path.realpath(link).startswith(canonical_root + '/')
```

**Caveat to write into the record, not to omit.** In a git repo a file→symlink change shows as a
` T` **typechange**, and an absolute symlink into a sibling repo records a host-specific path: a
fresh clone or `git checkout -- <path>` on another machine follows it into nothing, so the files are
**absent**, not merely stale. Commit the typechange deliberately with that in the message, or move the
copies out of version control. Leaving it uncommitted is the worst of the three, because `HEAD` and the
working tree disagree and nothing announces it.

## Step 4 — verify the canonical tree still works, and pin a snapshot

Run every ExecStart target **as a binary** — never `systemctl start`, never touch a timer:

```bash
PYTHONPATH=<as-unit> /usr/bin/python3 <exec-start-path>
```

Also: run the tree's test suite, re-probe the live service health, and confirm the stores grew only by
append. Snapshot data-file hashes **before** the pass and compare after, so you can prove the pass
itself wrote nothing. Confirm the tests do not write into production data — check for `tempfile` /
`mkdtemp` redirection before trusting a green suite.

**Publish against a stated snapshot.** If another lane is editing the canonical tree, module content
moves mid-pass; every hash you quote is a hash-at-time. Pin the snapshot time beside the verification
table, re-verify convergence on your final pass, and say plainly which figures are stable and which
have already moved.

## Step 5 — the record

The record is the deliverable that outlives the pass. Structure that survives audit:

1. **Which tree runs** — the commands and their output, not a conclusion.
2. **Divergence table** — bytes, hashes, unique-line counts per module, pre-convergence.
3. **Per-module designation** — disposition + reason. This is where `SUPERSEDED_NOT_MERGED` rationales
   live, as a table a future reader can consult before "restoring" something.
4. **TREE_ORIGINAL files** — and any **cross-tree coupling** you found and deliberately did NOT move.
   A live data file read by modules in two trees is a migration with a rollback obligation, not a
   dedup. Say so, so the HOLD reads as a decision rather than an oversight.
5. **Preservation sets** — every path holding displaced bytes, with hashes.
6. **Verification** — the ExecStart/health/suite results with exit codes, pinned to a snapshot.
7. **Rollback** — literal commands.
8. **Open items, each with a named owner.** An open item without an owner is a place the work quietly
   stops.

Copy the disposition vocabulary from Step 2 verbatim, so records from different passes are comparable.
On a contested path, **append** to an existing record; publish a full alternative under a distinct
filename.

## Pitfalls

- **Deleting the older copy because it is older.** Recency is not correctness and size is not
  capability. Classify on measured unique logic.
- **Reporting one of two disagreeing counts as "the" number.** When two stores or two calibration
  surfaces both report healthy but disagree, they are computing over different universes — report both
  or neither, and treat the derived disagreement as its own finding. Two surfaces agreeing on one
  figure (same accuracy) while disagreeing on another (active count) is the signature of two universes,
  not of agreement.
- **Converging the tree but not the data.** Code dedup and state dedup are separate problems; a shared
  store split across two paths keeps producing divergent numbers after the code is unified.
- **Treating "no unit references it" as the whole impact test.** Also grep the scheduled-job prompts,
  skills and docs that name the dead path as an "evidence" location — the path may be load-bearing for
  documentation, which is how a dead tree survives.
- **Assuming a clean test run means the pass wrote nothing.** Hash the data files before and after.
- **Writing into the duplicate tree before checking who owns it.** Another lane may be consolidating
  the same tree right now; your in-flight file becomes its "original". See `concurrent-agent-writers`.

DITEMPA BUKAN DIBERI
