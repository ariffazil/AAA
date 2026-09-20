# Quarantine Runbook — retiring a skill body without losing a capability

Use when a body must leave the load surface: a half-finished collapse, a duplicate owner whose
redundancy is proven, an orphan left behind by a recorded retirement, or an archive-bound stub.

> **The one rule this whole page exists for:** *recover, then remove.* A retirement has two halves,
> and the half people skip is proving the survivor actually holds what is leaving.

## Why the order is not negotiable

Two traps sit in the path, both measured:

- **The archive can be circular.** An `.archive/<date>-<name>/<skill>` entry was a symlink whose target
  was the *live body it claimed to have archived*. "It is archived" was a claim with no copy behind it,
  so removing first would have destroyed the only one.
- **The successor can have absorbed nothing.** A stub pointing at a successor is evidence the redirect
  was *written*, not that the content arrived.

Either trap turns a structure repair into a permanent content loss. Neither raises an error.

## The order

### 0. Probe the loader's real read path first

Never assume a root is read because it exists or because a config names it as the create target.

```python
from agent.skill_utils import get_scan_ordered_skills_dirs
print(get_scan_ordered_skills_dirs())   # the roots actually scanned, in FIRST-WINS order
```

Run it in the live install's environment with `HERMES_HOME` set. `get_skills_dir()`,
`get_external_skills_dirs()`, and `get_skill_create_dir()` can name three different trees, and the
create dir is frequently **not** on the read path.

### 1. Classify the target before touching it

| Class | Test | Action |
|---|---|---|
| Unreachable orphan | body on disk, name not served | recover-then-quarantine |
| Served duplicate | two bodies, one routing name, first-wins | decide the SURVIVOR, then retarget |
| Live owner | the body the loader serves | not removable — this is the capability |

For a served duplicate, replicate the loader's scan order to learn **which** body wins. The two
possible answers are opposite defects and need opposite repairs.

### 2. Guard — is the source the only copy?

```python
h = sha256(source)
same = [p for p in every_SKILL_md_on_disk if sha256(p) == h]
assert len(same) == 1, same     # >1 means a live copy already exists; nothing is at risk
```

Also resolve the archive link and require it to land outside the live path:

```python
assert not os.path.realpath(archive_link).startswith(os.path.dirname(source))
```

### 3. Recover — compare headings against the successor PACKAGE

Compare the source's H2 set against the successor's SKILL.md **and** `references/`. Testing only
SKILL.md reports a correct merge as defective, because an absorbed body legitimately belongs in a
reference (progressive disclosure), not in index tax.

Anything missing goes to `<successor>/references/absorbed-<source>.md` with a provenance header:
what was retired, when, by which directive or tombstone, the path it came from, and the original
`sha256_before`. Add one pointer line under the successor's support-files heading.

### 4. Verify the recovery, not the copy

```python
assert sha256(recovered_payload_without_header) == sha256_before
```

Print that comparison. A recovery that reports success without it is the same shape of claim the
tombstone made.

### 5. Quarantine — move, never delete

Destination **outside every scanned root**, so no census or index picks it up as live. Record the
inverse operation beside it: `mv <quarantine> <original>`.

```
/root/AAA/.quarantine-<topic>-<date>/
  <name>/            the moved body
  LEDGER.json        one entry per op: {op, from, to, sha_before/after, reverse}
  LEDGER.md          the human-readable reversal list
```

Append to an existing ledger; never truncate one. A truncated ledger silently discards the reverse
operation for every earlier pass — and the earlier pass is the one a rollback needs.

### 6. Sweep the downstream twice

The pre-move dependency check proves the move is *safe*; it does not clean up *after* it. Two surfaces
must be re-swept, and neither errors when missed:

```python
# (a) links whose RESOLVED target was the moved path
for dp, dn, fn in os.walk(root, followlinks=False):
    for n in list(dn) + list(fn):
        p = os.path.join(dp, n)
        if os.path.islink(p):
            t = os.readlink(p)
            ab = t if t.startswith('/') else os.path.normpath(os.path.join(dp, t))
            if any(ab.startswith(q) for q in QUARANTINED_PREFIXES): hits.append(p)
```

- **(b) inventory files that still NAME the dead path** — alias table, placement manifest, ownership
  map, package READMEs. Patch them (as targeted text edits, not load/dump rewrites) to the successor
  plus a `quarantined: <date>` marker. A stale path claim resolves to nothing and the next agent
  believes it.

A circular archive pointer found in step 2 leaves a *dangling* link once the body moves — repoint it at
the recovered `references/absorbed-<source>.md` so the archive entry still leads somewhere true.

### 7. Verify from the loader, not from the tool

Three assertions, all cheap:

```
served_names_after   == served_names_before     # nothing lost, nothing gained
links_pointing_at_quarantined == 0              # step 6 completeness
census: broken_symlinks == 0                    # structural health
```

The first is the important one: compare the loader's own served-name set before and after, using
`get_scan_ordered_skills_dirs()` plus first-wins. A file count cannot see a silently-dropped name.

## What is NOT safe to remove in this class

- **N independent write-ups of one job.** Content similarity near zero across the group means they are
  not copies; removing all but one discards other people's texts unread. That is a canonical-owner
  decision, not a delete.
- **Unreachable bodies that are content, not duplicates.** If the only copy on disk is the unreachable
  one, removing it destroys the capability. Reachability and redundancy are different findings.
- **One body reached by several paths.** Resolve by inode: identical `st_ino` means zero bytes of
  redundancy and zero to reclaim.
- **A dormant tree with its own config.** Another harness home is not a redundant copy of yours.
- **Genuinely divergent twins.** A design fork needs a human; content similarity below the copy
  threshold means two designs, not one duplicated.

## Commit shape

Stage exactly the paths this runbook produced — the quarantine dir, the recovered references, the
updated inventories, the fixed links. Print what you deliberately left out (a concurrent writer's
in-flight files are the usual case), and never `git add -A`, which sweeps another agent's uncommitted
work into a commit that claims to be yours.
