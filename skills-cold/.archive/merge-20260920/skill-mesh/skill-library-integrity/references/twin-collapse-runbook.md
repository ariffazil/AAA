# Twin Collapse Runbook — one body, one address

For the operation: two trees (or two families in one store) hold **real bodies** for the same skill,
and you are reducing them to one body plus addresses. Distinct from root *consolidation* (which
promotes and links across roots) and from *resolution* repair (which fixes names that cannot load).

Order is fixed: **probe → back up → classify → collapse → verify by delta → record reversal.**

---

## 0. Probe the arena before planning anything

Two facts decide the whole plan, and both are cheap to measure and expensive to assume:

```python
# (a) live loader surface — run in the install that serves the session, HERMES_HOME set
from agent.skill_utils import get_skills_dir, get_external_skills_dirs, get_skill_create_dir
#     skills_dir       = the READ surface
#     external_dirs    = every OTHER scanned root (may be EMPTY)
#     skill_create_dir = where new skills are WRITTEN (may not be on the read path)

# (b) how the updater treats a diverged bundled copy -> read tools/skills_sync.py:
#     _update_existing_skill : hash mismatch -> user_modified -> KEPT  (not overwritten)
#     _install_new_skill     : same-named local skill -> "yours was kept"
#     _defer_to_external     : an external_dirs source WINS and a local copy may be REMOVED
```

If the write surface is not on the read path, a body that exists only there is reachable **only
through the links a view tree carries**. Collapsing a link is then deleting a capability. Establish
this before the first mutation, not after.

Because a relocated bundled entry does not break the sync but silently stops receiving upstream
changes, decide the bundled set explicitly: keep it harness-native (wants upstream updates) or
take ownership of it (wants the local version). "Bundled" answers *who writes it*, not *may it move*.

## 1. Back up BOTH sides, then write the reversal before the mutation

Capture every body you are about to touch, both sides, plus a restore script. The reversal for a
collapse is not `git revert` — it is an enumerated list:

```
backups/<collapse>/bodies/<skill>__<side>.md     # both sides, per pair
backups/<collapse>/RESTORE.sh                    # regenerates each side from those copies
backups/<collapse>/manifest.json                 # per pair: paths + sha of each side, pre-mutation
```

Record per operation which of the three it was: **minted** (remove it), **re-pointed** (restore its
recorded previous target), **already correct** (leave alone). Those three lists ARE the reversal —
never claim a before-map you did not capture.

## 2. Classify each pair by what differs (not by version string)

```python
only_a = {l for l in open(a).read().splitlines() if len(l.strip()) > 3} - set(open(b).read().splitlines())
only_b = {l for l in open(b).read().splitlines() if len(l.strip()) > 3} - set(open(a).read().splitlines())
```

| only_a | only_b | class | action |
|---|---|---|---|
| non-empty | empty | **SUPERSET** | keep that side's body |
| empty | non-empty | **SUPERSET** | keep that side's body |
| both empty | | **IDENTICAL** | collapse; nothing to merge |
| both non-empty, same design | | **UNION** | merge, then one home |
| both non-empty, different method | | **DESIGN FORK** | **HOLD — human decides** |

Also check the timestamp and the byte length, but **classify on the line sets** — a version string is
a claim, the differing lines are the evidence. A housekeeping pass that appends a marker can make the
older copy look newer.

**Frontmatter injection is its own defect class.** A bulk annotation pass can land a marker *inside*
the description string instead of after it, so the text reads mid-clause. If the marker sits in the
first ~57 characters, it degrades the selector window — the one field selection precision depends on.
Report it as a finding; it is not a merge input.

## 3. Merge a UNION mechanically

```python
def merge_union(primary_txt, other_txt):
    """Primary body wins. Pull across only top-level frontmatter keys the primary lacks."""
    af, ab = split_frontmatter(primary_txt)
    hf, _  = split_frontmatter(other_txt)
    have = {line.split(':', 1)[0].strip() for line in af.splitlines() if ':' in line}
    add  = [l for l in hf.splitlines()
            if re.match(r'^[A-Za-z_][\w\-]*\s*:\s*.+$', l)
            and l.split(':', 1)[0].strip() not in have
            and l.split(':', 1)[0].strip() not in ('name', 'description')]
    return f'---\n{af}\n' + '\n'.join(add) + f'\n---\n{ab}', [l.split(':', 1)[0] for l in add]
```

Exclude `name`/`description` — those are the routing identity and taking the wrong one renames the
capability. Record which keys were merged; that list is the part of the reversal a body hash cannot
prove.

## 4. Collapse: body in the write surface, address in the read surface

```python
os.remove(read_side)                    # the read-surface entry
os.symlink(write_side, read_side)       # it becomes an address to the one body
```

**Guard every child by ARTIFACT, not by container** (see SKILL.md — a container check passes on a
placeholder directory while the body lives elsewhere, and the children then vanish from the load
surface). Before collapsing a container, resolve each child to a real `SKILL.md` and reconcile any
child whose body sits at a different path than its declared home.

Carry across any non-`SKILL.md` child the surviving side lacks (`liveness.json`, `_manifest`, scripts)
— a silent loss there is a capability loss that no `SKILL.md` count will show.

Only collapse members of the bundled set once the ownership decision in §0 is made; collapsing them
stops upstream updates for those names.

## 5. Verify by LOAD-SURFACE DELTA, never by file count

```python
before = loadable(READ_ROOTS)        # followlinks=True, from before the operation
...mutate...
after  = loadable(READ_ROOTS)
lost, gained = sorted(before - after), sorted(after - before)
assert not lost, f"capability lost: {lost}"      # gained is usually fine; explain it anyway
```

Also assert, as separate numbers:

```
shared names still DIVERGED        -> only the HOLD set
names with a REAL body on both sides -> only the HOLD set
broken symlinks                      -> 0
write-surface entries borrowing a body from outside -> 0
```

A `lost` non-empty means a capability disappeared; a `gained` non-empty means an address was surfaced
or a walk flag changed — say which, because the two read identically in a diff.

## 6. Record what the operation exposed

A collapse is the best instrument the library has for finding hidden coupling, so capture, per pair:
the class, both paths, both hashes, and — for anything re-pointed — what it used to point at. Three
classes of defect routinely surface here and none of them are this operation's to fix: an entry whose
body resolves into a **runtime profile** or a **vendor checkout** (a portability defect — record
`body_held_here: false` and name the borrower), a **container whose children's bodies live elsewhere**,
and a **text read that differs between two copies of one skill** (one of them is fabricated; an OCR or
ASR transcript of one artifact must not depend on which copy you open).
