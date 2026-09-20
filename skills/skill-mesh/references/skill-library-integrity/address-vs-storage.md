# Address vs Storage — probe recipe

Two trees, one name. STORAGE holds the bytes; the VIEW holds addresses as symlinks into storage. Take
every census twice, once per side, and report two fields. Run this before proposing any move, rename,
or re-merge — it is read-only.

## 1. Enumerate the two sides separately

```python
import os

STORAGE_ROOT = '<canonical>/skills'      # real directories
VIEW_ROOT    = '<view>/skills'           # symlinks, resolving into storage
EXCL = {'.git', '.archive', '.system', '__pycache__', 'references', 'templates',
        'assets', 'scripts', 'node_modules', '.venv'}


def scan_links(root):
    """Every symlink in a tree as {relpath: realpath}. followlinks=False on purpose."""
    out = {}
    for dp, dn, fn in os.walk(root, followlinks=False):
        if EXCL.intersection(set(dp.split(os.sep))):
            dn[:] = []
            continue
        for e in list(dn) + fn:
            p = os.path.join(dp, e)
            if os.path.islink(p):
                out[os.path.relpath(p, root)] = os.path.realpath(p)
    return out


def scan_storage(root):
    """Real skill dirs (walked, not followed) PLUS top-level symlinked skills.
    os.walk(followlinks=False) lists a symlinked dir in `dn` but never enters it,
    so without the second loop a symlinked skill is invisible."""
    rows = {}
    for dp, dn, fn in os.walk(root, followlinks=False):
        if EXCL.intersection(set(dp.split(os.sep))):
            dn[:] = []
            continue
        if 'SKILL.md' in fn:
            rel = os.path.relpath(dp, root)
            rows[os.path.basename(dp)] = dict(rel=rel, is_link=False, target=None)
    for e in sorted(os.listdir(root)):
        p = os.path.join(root, e)
        if os.path.islink(p) and os.path.exists(os.path.join(p, 'SKILL.md')):
            rows[e] = dict(rel=e, is_link=True, target=os.path.realpath(p))
    return rows


BODIES = scan_storage(STORAGE_ROOT)
LINKMAP = scan_links(VIEW_ROOT)
ADDRESSED = {os.path.basename(os.path.realpath(p)) for p in LINKMAP}
```

## 2. Classify each storage entry

| question | test | field |
|---|---|---|
| does an address point at it? | name in `ADDRESSED` | `address` / `placed` |
| is the body held here, or borrowed? | `is_link` and target outside the storage root | `body_held_here`, `borrowed_from` |
| will the updater re-seed it? | name in `<view>/.bundled_manifest` | `bundled` |
| which layout generation? | depth of `rel` — one level / bucket / taxonomy | `generation` |
| is the name ambiguous? | basename appears more than once across roots | `name_ambiguous` |
| broken link? | `not os.path.exists(link)` | — |
| self-referential link? | `realpath(link) == dirname(link)` | — |

The **generation split** is the number that matters for a move plan: one-level entries belong to the
updater's layout, taxonomy entries are authored. Never average them into one figure.

## 3. Assertion discipline

- Before claiming a path "does not exist", test `os.path.isdir()` on the EXACT path in EVERY root. A
  bounded `find -maxdepth N` cannot refute existence at depth > N.
- Pick `followlinks` on purpose and say which you picked. `True` merges the trees and makes every count
  uninterpretable; `False` (plus an explicit top-level link scan) keeps them separable.
- Report a census as `{addresses, placements, hints, unresolved, borrowed}` — never one total.
- A directory existing is not evidence a skill belongs in it. A fuzzy match that resolves is still a
  guess: keep it in `hint`, publish `resolved: false`, never let it enter the placement tree.
- When two roots disagree, compare **inodes** before calling either a copy:
  `os.stat(a).st_ino == os.stat(b).st_ino` proves one body, not drift.

## 4. Minting an address (when the body has none)

Adding an address is cheap and reversible; moving bytes is neither. Prefer, in order:

1. Point the address at the body that already exists (a symlink) — the author keeps single-writer status.
2. Create a new capability bucket only when that organ has none, and only with a name from its own
   domain; filing a capability under another domain's bucket is a category error, and a category is an
   address, not a keyword.
3. Never copy a body to create a placement. A second copy is a second writer.

Record per address whether it was **minted / re-pointed / already correct**, and write the exact
reversal as those three lists (`rm` the minted; re-point the changed ones at their recorded previous
target). Those lists ARE the reversal — do not substitute a before-map you did not capture. Verify by
regenerating the index and confirming each new address reports `source=tree` with its real coordinate.

## 5. Reachability — is the store even on the loader's read path?

Address and storage are both about bytes. Reachability is a third question and it is the one that
silently undoes a tidy-up: **can the loader open the body at all.**

Probe the LIVE install — not a dev checkout, not a config comment, not a previous report:

```python
# run with HERMES_HOME set, importing from the install that actually serves the session
from agent.skill_utils import get_skills_dir, get_external_skills_dirs, get_skill_create_dir
print(get_skills_dir())            # the READ surface — always scanned
print(get_external_skills_dirs())  # every OTHER root that is scanned
print(get_skill_create_dir())      # where NEW agent-authored skills are WRITTEN
```

If the create dir is not among the read roots, the store is **write-only**: bodies land there, load
from nowhere, and no surface errors. Its entire reachability is the symlinks a view tree happens to
carry into it.

```python
READ = [get_skills_dir()] + get_external_skills_dirs()

def loadable(roots):
    names = set()
    for r in roots:
        for dp, dn, fn in os.walk(r, followlinks=True):        # followlinks=True: describe what loads
            if EXCL.intersection(set(dp.split(os.sep))):
                dn[:] = []
                continue
            if 'SKILL.md' in fn:
                names.add(os.path.basename(dp))
    return names

LOAD = loadable(READ)
STORE = set(scan_storage(STORAGE_ROOT))
UNREACHABLE = sorted(STORE - LOAD)
print(len(STORE), len(LOAD), len(UNREACHABLE))
```

Confirm the finding terminally on one entry before reporting the class: `skill_view(name=<n>)` for any
`n` in `UNREACHABLE`. Observed shape — a body on disk, fully formed, that the loader reports as *not
found*, so `skills_list` shows a smaller library than the store holds and nothing anywhere raises.

**Two rules follow.**

- **Report `unreachable` beside every firing/usage metric.** A firing count measures *loads*; a body
  that cannot load is never counted, so "N% never fired" silently absorbs this set. A prune list drawn
  from that metric deletes capabilities that were only unreachable. Reduce the denominator first.
- **Fix reachability before minting addresses.** A symlink added under a read path the loader does not
  scan moves the census and not the capability. Sequence: read path → addresses → bodies.

### 5a. The direct fix is refused — `external_dirs` may not shadow

Adding the store to `external_dirs` looks like the one-line cure for a write-only store. The loader
refuses it, and the refusal is deliberate:

```
_defer_to_external()  ->  "An external_dirs source provides this skill; a local copy would be a name
                          collision the loader refuses."
                          it then REMOVES a stale local copy when that copy is byte-identical.
```

Two consequences, both measured:

- A root added to `external_dirs` **collides with every name the two trees already share** — and the
  shared-and-diverged set is exactly the set you were trying to reconcile, so the fix arrives blocked
  by the problem it was meant to solve.
- The deferral can **delete** a local copy it finds identical, which is a mutation performed by a sync
  you triggered to read a config. Confirm the byte-identity yourself first.

So the working ladder out of write-only reachability is **an address per skill inside a root the loader
already scans** — a symlink a view tree carries, not a new read root. Order: decide ownership → mint
addresses in a scanned root → verify each one resolves a `SKILL.md` → only then collapse anything.
