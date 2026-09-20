# Identity Keying and Routing-Name Collisions

Companion to SKILL.md §6–§9. Two defect classes with one cause: **the key you use to identify a
capability determines whether your audit can see it.** Get the key wrong and you get a false
positive and a false negative from the same line, and the result looks clean either way.

---

## 1. Match on a stable key, never a basename

A leaf folder name is not unique. Any comparison that reduces an identity to `os.path.basename(path)`
collapses a namespace, because the dict comprehension keeps exactly one entry per name:

```python
# WRONG — 103 entries collapse to 42 keys
cbase = {os.path.basename(k): v for k, v in canon.items()}
hbase = {os.path.basename(k): v for k, v in herm.items()}
shared = set(cbase) & set(hbase)
diverged = [k for k in shared if cbase[k]["sha"] != hbase[k]["sha"]]
```

The collapse cuts **both ways in one line**, and the second half is worse than the first:

- **False positive** — two unrelated skills whose leaf folders share a name get paired and reported
  as *one skill that diverged*. Real example: a verdict-hold skill (11,071 B) paired against an
  onboarding procedure (5,914 B), reported as a single capability that had drifted.
- **False negative** — every entry the comprehension overwrote is never compared at all. A genuine
  divergence can be silently skipped and the audit reports a confident zero.

**Correct shape.** Compare on a stable key (full relative path, or the body digest). Keep the loose
key only as a DECLARED fallback, gated on unambiguity, and publish the ambiguity as its own field so
the sensor cannot hide how much it had to collapse:

```python
cbase, hbase = {}, {}
for k, v in canon.items():
    cbase.setdefault(os.path.basename(k), []).append((k, v))
# ... same for herm ...

ambiguous = sorted(n for n in (set(cbase) & set(hbase))
                   if len(cbase[n]) > 1 or len(hbase[n]) > 1)

shared = set(canon) & set(herm)                       # stable key
real_diverged = sorted(k for k in shared if canon[k]["sha"] != herm[k]["sha"])
fallback = sorted(                                    # declared, reported separately
    n for n in (set(cbase) & set(hbase))
    if len(cbase[n]) == 1 and len(hbase[n]) == 1
    and cbase[n][0][0] not in herm and hbase[n][0][0] not in canon
    and cbase[n][0][1]["sha"] != hbase[n][0][1]["sha"])
```

Publish `ambiguous_leaf_names` and `ambiguous_entry_collapse` alongside the result. A number that
cannot say how much it collapsed is not a measurement.

**Never quote a stored count as a fresh measurement.** Counters about this store are built on
different keys and drift apart the moment the tree changes. Same-name groups, groups whose *bodies
differ*, and cross-surface identity keys are three answers to three different questions; any of them
can also be recalled from an earlier session's memory long after the store it described moved. Re-run
the instrument at the moment of citation and carry the measurement date with the number. If the
instrument cannot be run, the figure is UNVERIFIED — write that, not the number.

**A correction is a new claim, not an amnesty.** When a figure is retracted, its replacement is
subject to the same key discipline as the original — and the *ancestry* you assign the old number
("this count descends from that earlier audit's count") is itself unproven until the two keys are
shown to be the same key. Corrections assembled from memory reproduce the original defect one layer
up, where it is harder to see and more expensive to catch. When a correction is itself corrected,
leave the intermediate wrong version visible with its retraction rather than quietly overwriting it.

**Sibling reference:** `references/instrument-verification.md` — the five checks that establish a
sensor is alive and able to fail before any number from it is believed.

The same defect reaches **derived counts**: an identity key of `{basename}` makes 642 addresses read
as ~601 distinct and treats unrelated same-named folders as one skill. Where a count claims to answer
"how many capabilities", key it on the body digest; where it claims to answer "how many addresses",
key it on the path. State which question the number answers, in the same breath as the number.

---

## 2. Routing-name collisions — a capability that exists and can never load

Two skills can declare the SAME frontmatter `name:` at different paths. The loader keeps the first it
walks and drops the rest with no log and no warning:

```python
name = frontmatter.get("name", skill_md.parent.name)
if name in seen_names or name in disabled:
    continue
```

So a colliding name is not cosmetic: it is a capability on disk, indexed by nothing, unreachable.

**Verify the dedupe rule by reading the loader's own code, never a comment about the loader.** A
docstring stated the rule first, but only the real loader showed the walk order that decides which
body survives — and that order is what tells you which copy is the dead one.

### Discriminate before you count

**One body at many addresses is NOT a collision.** Identical bodies at several paths are the intended
address/view tree (bands over a single body) and cost nothing. Only *different bodies sharing one
name* are the defect. Undiscriminated, one store reported 60 colliding names where the true defect
count was 2 — a 30x overstatement whose only product is 50 phantoms for the next agent to hunt.

### Procedure

1. Group every `SKILL.md` by frontmatter `name:`, keeping `(relpath, body digest)` per member.
2. Keep only groups whose digests DIFFER.
3. Per group, the NEWEST body wins. The store's own convergence rule is already written down — follow
   it rather than inventing a preference, and freeze the losers with per-file digests plus an undo
   line.
4. Fix the case-twin DIRECTORY too when the loser's parent differs only by casing. Two directories
   differing by case are two directories; casing is not a routing key you may rely on.
5. Sweep the mirror trees LAST: every view symlink that pointed at a frozen loser must be re-pointed
   to the survivor, or a name collision is traded for a dangling link and the census flips to FAIL.

### The metric moves without meaning anything

After one collision is fixed, a naive detector simply re-pairs whatever names remain and reports a new
number. **A changed collision count is evidence about the detector until the pairing rule is proven
stable** — do not read the movement as progress.

---

## 3. Committing these repairs in a shared worktree

Store repairs happen in a git tree that concurrent agents are also writing.

- **Stage explicit file paths. Never `git add <directory>/`.** A directory-level add sweeps whatever
  another lane has left uncommitted — 17 files from a different lane rode into a commit whose message
  described only one lane's work, so the message and the contents disagreed and the receipt became
  misleading. Stage the paths you actually changed, check the staged diff before committing, and let
  each lane close its own commit.
- **Verify the staged set is yours** with a staged diff/stat, not with the working-tree status —
  working-tree status lists every lane's dirt and cannot tell you what you are about to commit.
- **Prefer a second undo route.** Where the store is a git work tree, a freeze is reversible twice:
  by the ledger's `mv` line and by `git checkout` of the original path. Record both.
- **Do not fix another lane's file to make a check pass.** Report it; a concurrent lane's angle on the
  same defect may be better informed than yours, and the reconciliation is a decision, not a cleanup.
