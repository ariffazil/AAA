---
name: skill-library-integrity
description: "Use when a skill won't load, a capability vanished silently, or trees diverge — one-writer/many-views consolidation with a live entropy sensor."
version: 1.0.0
owner: AAA
category: governance
tags: [skills, hygiene, symlink, resolution, audit, curation]
floors: [F1, F2, F4, F11]
autonomy_tier: T1
---

# Skill Library Integrity

> **Canon:** `/root/AAA/instructions/agi-asi-skills-fundamentals.md` (F13_RATIFIED_CHAT 2026-09-16 — the Seven Laws; C17–C19)
> **One line:** a skill library is an **actuator**, not documentation. Many may read a capability; few may write it; someone must judge it.

**Read Law 4 (consequence class on every capability) as a statement about the GATE, not about each
SKILL.md.** Writing side-effect class / blast radius / reversibility / authority tier into every skill
body is **safety theatre** — it rents index space on every turn, drifts away from the real gate, and
enforces nothing. **Safety is an emergent property of the execution boundary and lives in the kernel
gate, not in the artifact**; that mechanism is already live (a kernel-side check holds a write on a
destructive-statement pattern or a gated lane *before the file is touched*, which is the correct place
for a refusal). What a skill legitimately carries is **reach** — which surface a capability can touch:
outbound to a human · canonical record · shared infrastructure · destruction · local artifact. Reach is
a ROUTING fact (it tells a caller where the check must happen): measure it, publish it as data, do not
stamp it into hundreds of bodies.

**Corollary — the human plane is NOT scrubbed of persona.** "No performed persona, no filler, no
theatre" applies to MACHINE-plane lanes only. Human-facing register, tone, warmth and dignity are a
REQUIREMENT, because a human is a paradox and the bridge is where that is honoured. Classify plane
first (`machine` vs `human`) and apply the anti-theatre rule to one side; a "de-fluff the library"
sweep that reaches a human-plane skill has destroyed the feature it was securing.

## LAW 1 — negative proof before creating a skill (anti-redundancy gate)

**No new skill may be created while an owner exists.** Run the gate first:

```bash
python3 /root/scripts/skill-owner-lookup.py "the capability in plain words"
# OWNER_EXISTS -> patch the owner.  NO_OWNER -> creation permitted.  WEAK_MATCH -> inspect the hits.
```

Order of preference when a capability is missing (the cheapest home wins):

```
owner skill exists   -> patch it (procedure step, pitfall, verification check, kill criterion)
similar exists       -> add an alias, example or pitfall to that owner
repeated workflow    -> patch the owning procedure
one-time fact        -> memory, not a skill
governance rule      -> floor / base / intake, not a skill
new external API     -> tool or MCP contract, not a skill alone
genuinely new domain -> proposal skill, quarantined
```

A duplicate owner is worse than a missing one: both load, both sound right, and they drift apart
where nobody is looking. The gate is a keyword+IDF lookup, so it over-fires on common words by
design — a single shared word is never enough for `OWNER_EXISTS`.

## LAW 3 — one writer, many views, live sensor

This is the doctrine this skill enforces. Breaking it deletes capabilities silently:

```
1 canonical writer  -> /root/AAA/skills            (content, provenance, genealogy)
N harness views     -> /root/.hermes/skills,       (symlinks; /root/AAA/skills is the
                       profiles/*/skills            `skills.create_dir` target so new
                                                    agent-created skills land canonical)
1 live sensor       -> /root/scripts/skill-entropy-gate.py
                       cron 23 4,10,16,22 · exit 1 on FAIL · log /var/log/arifos/skill-entropy.log
1 chaos sensor      -> /root/scripts/hermes-chaos-sweep.py
                       cron 40 4,10,16,22 · skills + bundles + MCPs + capabilities in one verdict
                       · /root/scripts/mcp-health-census.py feeds it the MCP truth table
                       · /root/scripts/skill-owner-lookup.py is the creation gate
                       · /root/scripts/symbol-probe.py guards notation (C20) before intake
                       · /root/scripts/skill-store-converge.py converges intra-store duplicate
                         bodies (dry-run default; mv to quarantine + relative symlink)
```

**Census and gate are not the same instrument, and neither is optional.** The census says what
exists; the sweep says what is broken, stale or duplicated. A profile copy that is an old *copy*
rather than a symlink is drift, not a view: `/root/scripts/hermes-profile-detach.py` relinks them
(backup first) instead of deleting content.


**An upstream-bundled skill can be relocated — but it then FREEZES at your version, silently.** The
manifest (`~/.hermes/skills/.bundled_manifest`) marks ownership, not immovability. Read the sync
before asserting either way: a copy whose hash no longer matches the origin is appended to
`user_modified` and **kept**; a bundled name you deleted is **not re-added**; a same-named local skill
is reported *"yours was kept"*. So a moved or symlinked bundled entry does not "break the sync" — it
stops receiving upstream changes with no message ever printed, which is the quieter failure. Decide
deliberately: keep it harness-native if you want upstream updates, relocate it and own it if you want
the local version. Never state either consequence as a fact about the updater without reading
`tools/skills_sync.py` — *"an inferred blocker is not a measured one"*, and this one was asserted
twice from intuition before the code was opened.

**Repair procedure (reversible, verified):**

```bash
python3 /root/scripts/federation-skill-consolidate.py             # dry-run census
python3 /root/scripts/federation-skill-consolidate.py --apply     # promote + symlink + fill
# git-tag both trees BEFORE applying; rollback manifest -> /root/skill-audit/rollback-manifest.json
python3 /root/scripts/skill-entropy-gate.py                       # must show broken_symlinks: 0
```

**Never measure the view tree with plain `os.walk`/`find`.** Views are symlinks — you must use
`followlinks=True` / `find -L`, or you will count 124 when the true figure is 409 and conclude the
tree collapsed. This mistake has already been made once.

**But the flag is per-question, and saying WHICH you used is part of the answer.** `followlinks=True`
answers "what can the agent load"; `followlinks=False` answers "what bytes are on disk here". The
collapse above and a later false count are the same defect with the flag flipped, so state the choice
alongside every number rather than asserting one form is right.

### ADDRESS vs STORAGE — two trees, one name

Both trees answer to `.../skills/domains/...`:

```
<canonical>/skills/domains/   = STORAGE   real directories, the bytes, ONE writer
<view>/skills/domains/        = ADDRESS   symlinks (hundreds), resolving into storage
```

Reading one and quoting it as the other produces **opposite errors in each direction** from a single
audit: "these paths are missing" (they are addresses) and "these capabilities are already placed"
(that was a link, not a body). Neither is a correction of the other; both are the missing distinction.

Four rules follow, each of which has been violated for real:

- **A depth-bounded `find` cannot refute existence.** `-maxdepth N` cannot see a `SKILL.md` under an
  N+1-deep coordinate. Never write "does not exist" from a bounded walk — test `os.path.isdir()` on
  the exact path, in EVERY root, before asserting absence.
- **`followlinks=False` hides symlinked skill dirs** — a symlinked skill is listed in `dn` but never
  entered, so it vanishes from the census unless top-level links are scanned separately.
- **Publish `{address, storage}` per entry.** An address is a claim about taxonomy; storage is a claim
  about bytes. Two claims, both load-bearing, never interchangeable.
- **An inferred address must NEVER be published as a placement.** A classifier with a default fallback
  bucket mints coordinates that exist in no tree, and a reader cannot tell an invented address from a
  real one. Fix at the GENERATOR: emit `UNRESOLVED`, keep the guess in a separate `hint` field that
  never enters the placement tree, and report `placements` / `hints` / `unresolved` as three numbers —
  one total is a lie. A directory merely *existing* is not evidence a skill belongs in it.

→ Probe recipe + classifier code in `references/address-vs-storage.md`.

### REACHABILITY — the store can be a WRITE surface and not a READ surface

Address and storage answer *where the bytes are*. Reachability is a third question: **can the loader
open them at all.** Probe it against the LIVE install; never infer it from doctrine, a config comment,
or a previous report:

```python
# run in the LIVE install's environment, with HERMES_HOME set — not from a dev checkout
from agent.skill_utils import get_skills_dir, get_external_skills_dirs, get_skill_create_dir
print(get_skills_dir())            # the READ surface, always scanned
print(get_external_skills_dirs())  # every OTHER root that is scanned
print(get_skill_create_dir())      # where NEW skills are written
```

Any three of those can name different trees, and when they do **the create dir may not be on the read
path at all**. A store configured as `skills.create_dir` but absent from `get_external_skills_dirs()`
is **write-only**: every agent-authored skill lands there, loads from nowhere, and raises no error on
any surface. A view tree full of symlinks into that store is the only thing keeping it reachable, so
the store's real reachability is *the links*, not its own existence.

**So the create path must mint the address, and by default it does not.** Creating a skill writes the
package into the canonical store and stops — nothing on the write path creates the view symlink. A
skill can therefore be complete, resolvable by path, tracked by nothing, and still return *not found*
to `skill_view`, which is the failure that matters because the loader is what an agent actually uses.
Measured: a newly authored skill was invisible to `skill_view` until the view link was created and the
derived index refreshed; the sibling skills in the same category resolved fine, which is what made the
outlier obvious.

```bash
# after creating ANY skill — resolve it the way the LOADER does, not the way find does
ln -sfn <canonical>/<category>/<name> <view>/<category>/<name>   # if the view link is missing
python3 <view>/../scripts/skill-matrix.py                        # refresh the derived index
```

Verify with `skill_view(name=<new skill>)` **immediately after creating it**, not at the end of the
session. Anything that cites the name — a cron job, a handoff, a later step in the same task — fails
silently on a name that resolves to nothing, and the failure surfaces hours later in an unrelated
lane. Diagnose the outlier by comparison: if every sibling name in a category resolves and yours does
not, you are looking at a missing address, not a malformed skill body.

**Census the diff — the difference is the finding.** Loadable = walk every read root following links;
storage = walk the store without following, plus its own top-level links:

```
loadable    = {basename(dp) for dp in walk(<read roots>, followlinks=True)  if SKILL.md}
storage     = {basename(dp) for dp in walk(<store>,      followlinks=False) if SKILL.md}
            | {top-level links in <store> that carry a SKILL.md}
unreachable = storage - loadable          # written, and readable by nothing
```

Measured on a grown federation: **549 storage, 443 loadable, 204 unreachable.** Live cross-check:
`skill_view(name=<one of the 204>)` returns *not found* for a body that sits on disk, fully formed.

Two consequences, both load-bearing:

- **It silently corrupts the usage metric, and that metric is used for pruning.** A firing count over
the session DB counts *loads*. A body that cannot load is never counted, so "N% of skills never
fired" absorbs the unreachable set and reads as a pruning licence. Always report `never_fired`
**beside** `unreachable`; a kill list drawn from a firing count whose denominator was not first
reduced by this diff deletes capabilities that were merely unreachable.
- **An address minted under a dead read path proves nothing.** Adding a symlink into a tree the loader
  does not scan moves the census, not the capability. Fix reachability first, then addresses — otherwise
  the mesh is tidied while the front door stays locked from outside.
- **The obvious reachability fix is refused by design — `external_dirs` may not shadow.** The sync
  explicitly defers a skill whose name an `external_dirs` root already provides, because the loader
  would see a name collision it refuses: *"a local copy would be a name collision the loader refuses."*
  So populating `external_dirs` with the store is **not** the route out of write-only reachability —
  it collides with every name the two trees share, and it can also **remove a stale local copy** that
  is byte-identical to the external one. Mint an address per skill inside a root the loader already
  scans instead. Read the deferral branch before proposing a read-root change.

**A diverged twin is classified before it is treated — only the genuine two-design case is a HOLD.**
A blanket *"diverged pair → HOLD for the human"* is wrong for most of the population and it files a
mechanical task as a sovereignty question. Bucket by **what actually differs**, not by which side
looks newer:

```
SUPERSET      one side is a strict superset (extra frontmatter / extra section)   -> keep the superset
NEWER         same content, one side a later revision of the same design           -> keep the newer
UNION         each side holds something the other lacks (e.g. a governance block   -> merge, then one home
              on one side, frontmatter keys on the other)
DESIGN FORK   two different designs, neither a revision of the other               -> HOLD, human decides
```

Derive the bucket from measurement, not from the version string: compare the **sets of non-trivial
lines** per side (`set(a) - set(b)` and `set(b) - set(a)`, dropping whitespace-only entries). One side
empty → SUPERSET. Both sides non-empty → UNION or DESIGN FORK, decided by whether the difference is
additive detail or a different method. Report the class, the line counts on each side, and the mtime
of each — a genuine fork is the only one that reaches a person, and the counts are what make that
call possible. Merging a UNION is mechanical and safe: take the primary body, append the
frontmatter keys the other side holds and the primary lacks, and re-verify the body hash.

**Intra-store convergence (one body, many paths).** Consolidation stops the harness trees holding
copies; it does not stop the store holding two bodies for one skill. Measure, then converge:

```bash
python3 /root/scripts/skill-store-converge.py            # dry-run: SYMLINK / HOLD per family
python3 /root/scripts/skill-store-converge.py --apply    # mv to quarantine + relative symlink
```

Converge a pair only when BOTH hold — derive them at run time, never hardcode a family list:

1. **no file exists in the loser that is absent from the survivor** — compare whole directories, not
   just `SKILL.md`; a run-only script or a `references/` file lost here is a silent capability loss;
2. **removing the loser changes no routing** — normally that means the routing `name:` is identical
   on both sides. **The exception is a rename the federation already recorded**: if the alias
   registry (`SKILL_ALIAS_TABLE.json`) says the loser's routing name was retired in favour of the
   survivor's (`renamed_from` → `v3_name`, or a tombstoned `related[].note` of the form
   "LEGACY — renamed A→B", applied as a token substitution), then the routing question is already
   answered and converging it is executing a recorded decision, not making one.

Anything else is HELD with the reason named, and the two reasons are always one of: *routing would
change* (a rename with no registry record, so it is a live naming decision) or *content exists only
in the loser* (a merge).

**Collapsing a CONTAINER is not collapsing a pair — guard per ARTIFACT, never per container.** A
package that holds child skills (`substrate/`, `warga/`, any family directory) can contain children
whose bodies live **elsewhere**, so `os.path.exists(<store>/<container>/<child>)` returns true for a
thin placeholder holding only a `liveness.json` while the real body sits at a different path. That
guard passes, the container is replaced by a link, and the children disappear from the load surface
— measured: **six always-first, every-agent skills vanished**, with the container check reporting
success. The guard's predicate must be the thing you are protecting:

```
GUARD ON:  os.path.exists(os.path.join(store_child, 'SKILL.md'))     # the artifact
NEVER ON:  os.path.exists(store_child)                                # the container
```

Before collapsing a container, resolve **every** child to a real `SKILL.md` and reconcile the two
shapes first: the body and its address should agree on which path is the home (a child whose body sits
at the top level while its declared home is the container path is the defect that produces the
vanishing). Then verify the collapse by **set-diffing the load surface**, not by counting files.

**Check the registry before escalating a HOLD.** "Name choice is routing is agent behaviour, so a
human must decide" is true only while the decision is unmade on disk. Read the alias table first —
several HOLDs are renames that were recorded months ago and never executed, and reporting those as
pending human decisions is the same class of error as the false cause above: the label picks the
wrong remedy. What genuinely remains for a human is a pair of *live* routing names with no registry
record, or content that exists on only one side. See `references/multi-root-entropy-audit.md` §8 for
the recorded-decision table and the overlay-promotion rule.

**The action is always the same shape** — `mv` to quarantine plus a **relative** symlink: path count
is preserved so mutators resolve wherever they did before, the body count becomes one, and nothing is
deleted.

Verify with two invariants, and ignore the third number:

```
find -L <store> -name SKILL.md | wc -l     # MUST be unchanged — no path was lost
<loader> _find_all_skills()                # MUST be unchanged — no capability was lost
find <store> -name SKILL.md | wc -l        # WILL drop — the converged paths are views now
```

The third number dropping is expected, not damage — it is the harness-root trap, newly created
*inside* the store. Record it explicitly, because the next agent measuring the store without `-L`
will read a smaller total than yesterday and conclude that content was deleted. Commit the
convergence to the store's own repo and confirm git recorded the paths as symlinks (mode `120000`),
so a fresh checkout reproduces the shape rather than resurrecting the duplicate bodies.

**Run the dry-run until the plan stops changing.** A converge tool built this session planned three
wrong operations in three successive dry-runs before converging (two of them merges of unrelated
skills, one a merge of two skills' harness variants). Every one was caught by reading the plan; none
reached disk. A destructive tool that has never been dry-run has not been tested.

**Then diff the applied count against the plan count — that comparison is the test.** The plan is the
spec: an `--apply` whose summary disagrees with the dry-run it was built from has failed partially and
silently, because the per-operation handler swallows exceptions into a manifest nobody reads. This is
how a whole class of API misuse is caught — `shutil.copy2` is **files-only** and raises `Is a directory`
on every directory, so a promotion pass reports `applied=1` against a plan of `4` while the three
failures sit in the manifest as `ERROR` entries. Use `shutil.copytree` for directories, and treat any
applied/plan mismatch as a failed run, not a partial success.

**A rollback manifest must accumulate, never be rewritten.** Open the existing manifest and append
before writing; a tool that truncates it on each run silently discards the reverse operation for every
earlier pass, and the earlier pass is the one a rollback would need. Same reason a verify step is part
of the mutation rather than a follow-up.

Keep every skill **loadable**, and keep the tree from silently accumulating skills that look
present but cannot be opened. Two failure classes live here: name resolution (a name that
maps to more than one file) and unsafe mutation (a cleanup that deletes load-bearing
symlinks out of a git-tracked tree).

Both are silent. A skill that cannot load produces no error — the agent simply believes the
procedure is available and re-derives it from priors, which is worse than a missing skill.

## Use when

1. A `skill_view(name=...)` call refuses or returns nothing for a skill that exists on disk.
2. The skills tree appears to hold duplicate copies of one skill, or a nested `<name>/<name>/`.
3. After ANY skills-root cleanup, symlink sweep, archive move, or skill rename.
4. Before trusting a skill-library audit's findings — an unloadable skill cannot be audited.
5. Before repeating any skill count a registry, report, or previous session states. A stated
   count is a claim with a timestamp; compare it to disk or do not repeat it.
6. When skills are missing, stale, or divergent across trees — the failure there is content,
   not resolution, but the root model below is the same.

## Do not use when

1. The task is linting trigger clauses or descriptions (use `FORGE-skill-linter`).
2. The task is content redundancy, quality scoring, or prune planning (use `skill-audit-methodology`).
3. The task is scanning the whole federation for broken symlinks outside the skills tree (use `FORGE-symlink-audit`, but read the deletion rules below first).


## LAW 2 — never evict on appearance (shell/symlink dependency lint)

A directory that *looks* empty is **visual truth, not system truth**. Measured 2026-09-16: 52
canonical directories held no `SKILL.md` of their own and were moved to an archive — 26 of them were
the live body behind view symlinks, and eviction broke **82 links**. The mistake was reasoning from
appearance instead of from dependents.

**Before removing or moving ANY directory in a skill tree, resolve all six dependents:**

```
1. symlink dependents   python3 /root/.hermes/skills/skill-library-integrity/scripts/dependents.py <dir>
2. AGENTS.md refs       grep -rn "<name>" /root/AGENTS.md /root/AAA/AGENTS.md
3. bundle refs          grep -rn "<name>" /root/.hermes/skill-bundles/
4. registry refs        grep -rn "<name>" /root/AAA/skills/*.yaml /root/AAA/skills/*.json
5. alias refs           grep -rn "<name>" /root/AAA/skills/SKILL_ALIAS_TABLE.json
6. loader path refs     grep -rn "<name>" /root/.hermes/skills/.matrix-index.json
```

**Dependents cannot be found with a `find -L` link test — that predicate is inverted.** With `-L`,
find FOLLOWS links, so a symlink pointing at a directory is reported as a *directory* and `-type l`
then matches only links whose target is already unreachable. Run against a live directory, it returns
nothing and reads as *"no dependents"* — the exact answer that is wrong in the exact case the probe
exists for. Measured: three live directories were declared dependent-free and archived; **100 view
symlinks broke**, and the repair took longer than the original audit.

Walk **without** following, test `os.path.islink` on each entry, and resolve with `os.path.realpath`:

```python
for dp, dn, fn in os.walk(root, followlinks=False):      # NOT followlinks=True
    for name in list(dn) + list(fn):
        p = os.path.join(dp, name)
        if os.path.islink(p) and os.path.realpath(p).startswith(target_realpath + os.sep):
            hits.append(p)
```

Then sanity-check the probe itself: run it against a directory you *know* has dependents. A count of
zero from a predicate that can only ever return zero is not a finding — it is the same
"no reachable failing branch" defect this skill warns about elsewhere, and it hides behind looking
like a careful check.

Any hit = the directory is live. Move it only after re-pointing every dependent, and verify with the
census (`broken_symlinks` must stay 0).

**Corollary — moving is a migration, not a cleanup.** A remove that succeeds visually can still delete
a capability. Re-resolve, then move, then re-run the census.

## The one census command (never hand-write a skill count)

```bash
python3 /root/scripts/skills-census.py            # report (+ exit 1 on a structural break)
python3 /root/scripts/skills-census.py --write    # also refresh the registry's witness block
```

It emits `witness_hash` over the claim. The registry's `disk_reconciliation` block is written **only**
by this command — hand-editing it is the defect it exists to prevent. A count quoted from anywhere
else (a doc, a memory, a previous session, an external artifact) is stale by definition.

**A hand-rolled count is not merely stale — it is wrong in a specific direction, and the direction is
predictable.** Resolution is keyed on the skill **name**, matched across every read root; it is *not*
a path comparison. So a hand-written diff of `<store>/<category>/<name>` against
`<harness>/<category>/<name>` reports as unreachable every skill whose category path differs between
the two trees, even though the loader finds it by name. Measured: a directory-by-directory comparison
reported **192** unreachable addresses against a canonical census of **587 on disk / 451 loadable** —
an overcount by roughly half, produced by a method that never consulted the loader. The category path
is a placement claim; *can it load* is answered by name. Diff basenames, never paths, and quote the
census instead of your own arithmetic.

## Procedure

### 1. Audit resolution BEFORE anything else

```bash
python3 /root/.hermes/skills/skill-library-integrity/scripts/skill_resolution_audit.py
```

Exit 1 = at least one name is ambiguous, or a directory basename disagrees with its
frontmatter `name:`. Run this first because an ambiguous skill cannot be loaded at all, so
any content audit of it is wasted work.

### 2. Read the topology before touching anything

```bash
ls -la /root/.hermes/skills/ | head -30     # which entries are symlinks, which are real dirs
ls -la /root/.hermes/skills/<name>/          # a skill dir should hold SKILL.md, not <name>/
```

The mirror relationship is **partial, and assuming it is complete is itself the bug**. Measure
it every time — do not assume a name in one tree implies a link in another:

```bash
find /root/.hermes/skills -maxdepth 1 -type l | wc -l   # symlinks
find /root/.hermes/skills -maxdepth 1 | wc -l           # total entries
```

When the symlink count is a small fraction of the entries, the harness tree is holding its
own **real copies**, not mirroring — and the two trees then hold two independently editable
bodies of the same logical library. Count real `SKILL.md` per tree before reasoning about
sync, because the larger tree is the one actually loaded:

```bash
for r in /root/AAA/skills /root/.hermes/skills /root/.hermes/profiles/*/skills; do
  printf '%5d  %s\n' "$(find "$r" -name SKILL.md 2>/dev/null | wc -l)" "$r"
done
```

Know which side is authoritative before editing: patching a mirror and the real store
separately is how copies drift apart. Mirrors that resolve to the *same physical file* are
correct and expected — one copy, not a duplicate. See
`references/multi-root-entropy-audit.md` for the full root model and the divergence and
index-cost measurements.

### 3. Fix the shape you actually found

| Shape | Symptom | Fix |
|---|---|---|
| Stray duplicate at another depth | `skills/<x>/<name>/SKILL.md` AND `skills/<name>/SKILL.md` both real | Delete the stray REAL copy; keep the symlink as the single entry point |
| Nested self-copy | `skills/<name>/<name>/SKILL.md` | Delete the inner directory (a copy that included its own parent) |
| Dir name ≠ frontmatter | dir `foo/` declares `name: bar` | Rename the DIRECTORY to the declared name |
| Archive tree leaking into the scan | `.archive-*/<name>/SKILL.md` still indexed | Move it outside every scanned root, or exclude `.archive-*` from the scanner |
| Case-drifted harness link | symlink present but `os.path.exists()` is false; target differs from a real path only in letter case | Repoint to the case-correct real path. Do NOT lowercase the harness entry name — the name is the trigger |
| Headless store directory | dir in the authoritative store with no `SKILL.md`, live copy only in a harness/profile tree | Copy the live copy back into the authoritative store; until then the store is a shell and its own canonical claim is false |
| Stale count witness | a registry states a skill total that disagrees with disk | Fix the number from measurement, or record the disagreement; never re-publish the claim |
| Declared store smaller than the runtime tree | store claims `canonical_home` but holds fewer bodies than the harness tree, and shared names are all diverged | Execute the consolidation (references §7): promote what the store lacks, symlink what is identical, HOLD what diverged. Set `skills.create_dir` to the store **first**, or every newly written skill respawns the drift |

**Never rename the skill to match a typo'd directory.** The name is the trigger the agent
matches on; the directory name is only the index key. Rename the key, keep the trigger.

### 4. Prove the repair — a file count proves nothing

```
skill_view(name='<the-skill>')     # must return content, not "Ambiguous skill name"
```

A repaired tree that still refuses to load is not repaired. Same discipline as verifying any
tool change: re-invoke and read the returned fields, never the exit code.

### 4b. The three defect classes a link sweep actually finds (measured 2026-09-17)

A census can report `broken_symlinks: 0` while the library is still losing capabilities, because
there are three separate defect classes. Repair them in this order — each one changes what the
next one sees:

| Class | Symptom | Test |
|---|---|---|
| Dead view link | link resolves to nothing | `os.path.islink(p) and not os.path.exists(p)` |
| **Phantom view** | link **resolves**, but the target directory holds no `SKILL.md` | `os.path.islink(p) and os.path.exists(p) and not os.path.isfile(p/'SKILL.md')` |
| Dead internal pointer | SKILL.md cites a file under `references/` (or `templates/`, `assets/`) **and the package HAS that folder** but not the file | the body instructs a load that cannot succeed |
| Headless shell | canonical top-level dir with no `SKILL.md` anywhere beneath | looks like a capability, loads nothing |

The **phantom view** is the one no existing check sees, and it is the most deceptive of the four: the
broken-link test passes because the link resolves, and the dead-pointer test only reads `SKILL.md`
prose. So the index advertises a capability that loads as nothing, on a surface that reports healthy.
Measured: 24 instances, of which 82 view symlinks pointed into a single container whose children held
no body at all. The gate check `phantom_views` covers this class (FAIL-class). Repair by **name**,
using the same ladder as a dead link — and note the ladder runs in both directions: a view that
dropped the family prefix still matches a package that kept it (`mcp-testing` → `FORGE-mcp-testing`),
which was the majority of the resolvable cases. Where no body carries the name anywhere, the
remaining question is a **naming** decision, not a link cleanup: check each target's other dependents
before removing anything, because these targets are typically the live end of several links across the
profile trees.

**Before calling it a naming decision, ask whether the body was DELETED — the phantom class is
usually a delete, not a retirement, and git holds the body.** A bulk housekeeping commit can remove
`SKILL.md` files across many packages while leaving the directories in place, which reproduces the
phantom shape exactly: the link still resolves, the index still advertises the capability, and the
package looks like a naming question. Measured 2026-09-17: a single consolidate commit deleted 79
`SKILL.md` bodies; 15 were never restored anywhere, and every one of them was reachable from the
deleted path in that commit. The first report offered the principal a *naming* choice between three
options — all three rested on a false premise, because the bodies had never been retired.

```bash
git -C <store> show --name-status <commit> | awk '$1=="D" && /SKILL.md/{print $2}'   # the deleted set
for n in <names>; do ...; done   # does a body exist NOW anywhere, under that name?
```

Two predicates decide the restore list, and both were wrong on the first pass:

- **Match names case-insensitively.** A case-sensitive basename match reported 38 alive and 41 gone;
the same set matched case-insensitively reported 64 alive and **15** gone. The larger "gone" figure was
an artifact of the matcher, and it inflated the recovery work by nearly threefold.
- **Exclude names that already carry a body elsewhere**, or the restore duplicates a live package
rather than repairing a missing one. Run the exclusion as a second pass over the initial candidate
set, then re-run the sensor — the two extras surfaced only because the phantom count would not reach
zero.

Restore each body from the commit with a provenance header naming the commit and the path it came
from, then re-run the gate. Confirm the result on the disk, not in the tool's summary. A phantom count
that drops to zero and a `broken_symlinks: 0` beside it is the proof; the corpus also grows, so state
the index-cost delta — restored bodies re-enter the always-loaded index and are paid for on every
turn, which is the price of the repair.

The gate's `dead_internal_pointers` check covers class 2 (FAIL-class). Two predicates keep it
honest, and both were needed on the first run: a mention is a **real pointer only when the top
folder exists in that package** (otherwise the cited path is prose or an example), and a match
truncated by a following character (a prefix such as `assets/index-`) is a **glob, not a pointer** —
drop it. Same family, and the more expensive one: **a predicate that matches a word near the thing is
not a match on the thing.** Asserting the command form (`/proc/\S*environ`) is a different test from
asserting the token `environ`, which fires on the sentence that merely *names* the owner; a two-token
version (`"/proc/"` and `"environ"`) still fires when the same file reads `/proc/<pid>/status` for an
unrelated probe. When your check disagrees with the file, suspect the check first. Without these
filters the check fires on hundreds of doc examples and is switched off within a week. Measured: 397
candidate mentions across 845 packages → 74 real dead pointers in 21 packages.

**The gate must pass on its own documentation.** Adding this check made it fail on the skill that
documents it, because the examples were written as bare paths under a package that really does have
that folder. Write illustrative pointers in an unmatchable form (`references/<name>.md`) rather than
excluding a documented file from the sensor — an exclusion list is how the next real dead pointer
walks through.

**Repair rule ladder for a dead link — resolve, never guess.** Take the link's own basename and try:
name-identical → case-only → prefix-stripped (`AUDIT-`, `FORGE-`, `APEX-`, `ASI-`, `KERNEL-`). If
several candidates remain, prefer the canonical store, then the default harness view: the rest are
per-profile mirrors of one skill, not competing successors. If nothing resolves, the named
capability has no successor in the forest — remove the link (it already resolves to nothing) and log
it; never invent a mapping, and never delete the directory a link pointed at.

**Repair rule for a dead pointer — three sources, in order:** (a) the file exists in the federation's
own quarantine snapshots → restore it into the package; (b) it exists in a sibling live package →
relative symlink **inside** this package (one body, many paths); (c) the mention names a real file at a
known absolute path → correct the mention. If none, the pointer is aspirational: report it, do not
fabricate the file. Measured: 14 restored, 23 linked, 6 mentions corrected, 0 invented.

**Repair rule for a shell — the four gates, in order (do not reorder).** A shell is a canonical
entry with no body; a *candidate mirror* is a package of the same name elsewhere. Replace only when
all four hold, and resolve rather than guess:

```
1 resolve     basename -> name-identical | case-only | prefix-stripped (AUDIT- FORGE- APEX- ASI- KERNEL-)
2 rank        canonical store first, then the default harness view, then profiles
              (a per-profile copy is a MIRROR of one body, not a competing successor)
3 skill.md    the target must actually carry SKILL.md
4 containment target realpath must lie INSIDE an approved skill root
5 hash        every file in the shell must exist in the mirror with an identical sha256
```

Gate 4 is not decoration. Canonical entries symlinked to an **external plugin checkout**
(`/root/.understand-anything/repo/...`) resolve fine and carry a SKILL.md, so they pass gates 1-3 and
1-5 — they are a *portability* defect (the store's contents depend on a path outside every managed
root), not a broken capability. Deleting them drops a capability; calling them OK hides the
dependency. Give them their own verdict class and one governance call: add the source root to the
approved list, or vendor the skills.

Gate 5 is where the weak predicate shows itself. Comparing *relative-path sets* passes a shell whose
`SKILL.md.bak` — or whose `scripts/`, `assets/` — differ in content; comparing **hashes** catches it.
Then classify the divergence before choosing a remedy: a `__pycache__`/`.bak`/`.tmp` difference is a
build artifact (mechanically mergeable), a `SKILL.md`/`scripts/`/`assets/` difference is content and
is a merge a human owns. Two different defects must never share one label, or the label picks the
wrong remedy. Measured: one non-content pair, one genuine content split (`assets/icon.svg` differed,
two scripts existed only on the shell side), one backup-only pair.

Measured on the full store: 43 shells → 26 mirrored (all five gates), 14 archived (empty, no mirror),
3 held. Never delete a shell: mirroring keeps the path and swaps the body for a relative symlink;
an empty shell is *moved* to `.archive`.

**A backup left inside the scanned root is itself a shell on the next census.** The mirroring pass
keeps each pre-mirror body as `<shell>.bak-<ts>` — correctly, for reversibility — but that remedy
pollutes the instrument measuring it. Move the backups **outside every scanned root** and write the
inverse operation (`mv <dest> <src>`) to a manifest, appending rather than truncating.

**The shape change must be committed, or it evaporates.** Replacing a real directory with a symlink is
a repo mutation: in git it reads as `D` for every file inside plus a new untracked link, so an
uncommitted repair is one `git checkout` away from reverting while the backup bodies now sit outside
the tree. Commit scoped to the paths **your own manifests** produced — never `git add -A`, which
sweeps the learning loop's ledger and other writers' uncommitted work into a commit that claims to be
a mechanical repair. Print what you deliberately left out. **Stage and commit in the same breath** — a
change left staged-but-uncommitted in a shared repo belongs to whoever commits next, and a sibling
session's path-scoped `git add` will carry your files under its own message, where nothing links them
to your work. Verify with
`git ls-tree -r HEAD <store> | grep ^120000` that the paths are recorded as **mode 120000**; a fresh
checkout then reproduces the shape instead of resurrecting the duplicate bodies. Then state which
**branch** the commit landed on — a store whose worktree sits on a long-lived proposal branch has a
repair that a later `git checkout main` will revert, and that is a fact the next agent needs.

**A newly created skill is untracked by default — the write lands on disk, not in git.** Curating
writes files; repository tracking is a separate act, and nothing in the write path performs it. So a
fresh package is fully functional — it loads, it resolves, it appears in every listing — while
`git ls-files <package>/` returns **nothing** and a clone would not contain it. Measured: a skill
created and patched across several edits still had **0 tracked files** until it was staged
explicitly. Treat "a new package exists and loads" as a separate claim from "a new package is
recorded"; after any session that creates or patches skills, run `git status --porcelain <store>` and
stage what your own work produced — new directories show as `??` and will not be committed by a
path-scoped `git add` that names only the files you remember editing. Never `git add -A`, which
sweeps other writers' in-flight work into a commit that claims to be yours, and print what you
deliberately left out.

**Resolution must consult the tombstone registry, or a repair undoes a recorded merge.** The rule
ladder above resolves a dead link by name. A name whose skill was *retired* also fails to resolve —
so the ladder happily re-links it to the surviving body and resurrects a merged skill. Measured
2026-09-17: `forge-cross-agent-handoff` was tombstoned (moved to `handoff-contract`) and the ladder
re-pointed the canonical name at the old body. Read `/root/.hermes/.archive_skills_wave2/**/TOMBSTONE-*.json`
before repointing: if the name is tombstoned, the correct action is to point the *pointer* at the
recorded successor and leave the retired name retired — never to re-mint the routing name.

**A TOMBSTONE IS A CLAIM, NOT A MOVE — verify the content arrived.** A tombstone records
`moved_to`, `sha256_before`, a rollback command and a deprecation window. None of that is evidence the
body moved. Measured 2026-09-17: **14 Wave-2 tombstones, 0 of 14 targets carrying their source's
content** — every target shorter than its source, source headings and schema keys absent (largest:
567 lines → 103). The retirement is silent in one direction (a retired name leaves the index and
nothing errors), so the loss is invisible until an agent re-derives the procedure from priors. The
gate check `merge_completeness` now proves it per tombstone: recover the pre-merge body from the tag
the tombstone itself names, then require its H2 headings to appear in the **package** — SKILL.md *or*
`references/`. Testing only SKILL.md reports a correct merge as defective, because the absorbed body
belongs in a reference (progressive disclosure), not in index tax.

Recovery, when content is missing: write the pre-merge body into the target package as
`references/absorbed-<source>.md` with a provenance header (what was retired, when, by which tombstone,
the original `sha256_before`, and the recovery hash), add one pointer line under a stable heading, and
record the inverse operation. The retirement stands; the content returns. Measured: 14/14 completed,
147,531 bytes recovered, SKILL.md growth 0-3 lines each.

### 5. Deleting anything — the safe rules

Deleting on the same pass you use to *enumerate* destroys your ability to inspect the
candidate set, so never combine them. A blanket `find /root … -delete` is never correct here:
`/root` contains git repos whose **tracked** symlinks are the skill mirrors, so the sweep
mutates worktrees while supposedly cleaning cache.

```bash
# Enumerate only.
find <root> -maxdepth 5 -xtype l 2>/dev/null

# Before unlinking anything under a repo, ask git.
git -C /root/AAA status --porcelain        # a tracked symlink shows as ' D path'
```

**Rule: a symlink is disposable only when it is broken AND no repo tracks it.** "Broken"
alone is never sufficient in this federation. Scope every delete to one cache/archive
prefix; never `/root`.

If a tracked symlink is already gone, restore it from the worktree — never rebuild it by
hand, because the target may live outside the repo and a hand-built link is a wrong link:

```bash
git -C /root/AAA checkout -- skills/
git -C /root/AAA status --porcelain        # must show no deletions before moving on
```

## Pitfalls

- **An organ's entry can be a LINK while the body lives elsewhere — never assume the organ holds what
  it appears to own.** An address published under an organ's band may resolve into the canonical store,
  or into a runtime *profile*, while the organ's own `skills/` directory holds the body the whole time.
  Compare `readlink` against `realpath` on both sides and hash both before deciding which is the home:
  a body borrowed from a profile or a vendor install is the one-writer rule violated with the sign
  flipped, and it is a portability defect, not a broken capability. Record `body_held_here: false` and
  name the borrower; do not re-point it silently, and do not delete the entry.
- **Canonical storage can borrow bodies from outside canonical; count them.** A store that holds N
  entries of which some are symlinks out to a profile tree or a vendor checkout has fewer real bodies
  than it reports. Measure `body_held_here` per entry before quoting any total.
- **Most skills in a grown library are NOT in `.bundled_manifest` — so "tag it as bundled" is false for
  them, and a bulk move into the taxonomy is the wrong action for two independent reasons.** The
  updater re-seeds bundled skills at its own one-level path, so moving those manufactures duplicates it
  keeps undoing; and the remainder are authored, so the bundled label misdescribes them. Check manifest
  membership first, then publish a per-entry placement manifest —
  `{storage, generation, bundled, body_held_here, borrowed_from, address}` — and move one entry at a
  time with its own receipt. One artifact, machine-readable and version-controlled, replaces a bulk
  move that nothing can falsify.
- **Only claim a reversal artifact you actually captured.** If a plan asserts "the before-map is in the
  record" and the run that would have written it was blocked, say so and ENUMERATE the reversal
  instead: which N to remove, which M to re-point at a recorded previous target, which K to leave
  alone. An annotated enumeration beats a missing map; a map you claim but never captured is worst of
  the three, because the next agent will trust it.
- **Re-verify an audit's own load-bearing numbers before executing on it.** Before acting, re-probe
  every number the plan depends on against the live system; after acting, correct the audit document
  IN PLACE rather than appending a second report — a corrected finding is worth far more than a
  defended one.
- **Renaming a directory in the canonical tree silently deletes the capability in every harness.**
  Measured 2026-09-16: 1,568 rename events, zero propagated, 7 skills dead with no error. A rename
  is a migration — re-resolve every reference and run the gate afterwards.
- **A registry that reports `drift: 0` from a stale method is worse than no registry.** If a sensor
  cannot fail, it is decoration; the next agent trusts it. Never re-stamp a witness with a method
  you did not run — that is fabrication, not witness.
- **Over-eager shell eviction.** Directories that hold no SKILL.md of their own may still be the live
  body for a view symlink. Check what references a shell before moving it; moving one breaks every
  link pointing at it.

- **"Ambiguous skill name" is a filesystem fault, not a frontmatter fault.** Frontmatter
  linting cannot see it, so a skill passes every trigger/quality check and is still
  unloadable. Audit resolution with the script, not by reading the description.
- **Two files claiming one loaded name break BOTH names.** The damage is not limited to the
  duplicated skill — the skill whose name was borrowed by the typo'd directory is also
  unreachable. Fix both.
- **Mirror copies are not duplicates.** Symlinks resolving to one realpath are one skill.
  Collapsing them by deleting the wrong side removes the entry point while leaving the store
  behind — the tree then looks intact and loads nothing.
- **A cleanup that deletes a tracked symlink is a repo mutation.** `git status` shows it;
  treat it as an unscheduled change and restore it, do not "fix" it by recreating the link.
- **A rename without a resolve audit deletes capabilities silently.** When the authoritative
  store renames a directory to different letter case, every harness symlink still pointing at
  the old spelling breaks at once, with no error on any surface: `hermes skills list`, the
  index, and the agent all keep working and simply stop knowing that procedure. Any rename,
  reclassification, or retier is therefore incomplete until a resolve audit runs — the sync
  script that maintains the other harness trees may be documented to skip the tree you
  actually run, so it will never catch this for you.
- **A symlink mirror must be excluded from collision counting.** Counting a mirror as a second
  root doubles every skill it serves and manufactures collisions that do not exist, which then
  bury the real ones. Exclude mirror roots before comparing names or content.
- **A collision COUNT and a collision CLASS are different findings, and a quoted overlap rate must be
  re-measured before it is repeated.** Two classes carry opposite remedies: an **identity collision**
  is one capability duplicated across roots or aliases (the mirror farm above inflates it; remove the
  duplicate, no content merge); a **trigger collision** is two different, valid capabilities matching
  the same intent — a routing/selector problem that must never be resolved by merging bodies. Measure
  description-token Jaccard and **state the cutoff you used**; on a 500+ skill corpus genuine semantic
  overlap sits in the **tenths of a percent** at Jaccard >= 0.5, so a quoted figure an order of
  magnitude above your own measurement is identity duplication or a looser metric, not hidden
  redundancy. Report your number, name the difference, and never canonise an arbitrary "optimal N
  skills" target that no measured selector produced — order selection `Consequence/Tier -> canonical
  owner -> authority compatibility -> health -> minimal sufficient set -> semantic last mile`, with
  the semantic step LAST.
- **Two trees sharing a skill name are not in sync.** Names agree while bodies diverge —
  compare content hashes per shared name, and report the diverged fraction, not the shared
  count. A high shared count reads as health and hides the drift completely.
- **Never fork a second copy of the detector.** Run the installed gate by path. A forked copy
  in a skill directory drifts from the wired one and re-creates the exact defect being hunted.
- **A symlink-aware walk is mandatory once views are links.** `os.walk` and `find` do not
  descend into symlinked directories, so after a tree becomes symlink views the resolvable-skill
  count appears to collapse and an intact tree reads as destroyed. Use `os.walk(root,
  followlinks=True)` / `find -L` for anything describing what the agent can actually load;
  reserve the default non-following form for counting real bytes on disk. Mismatched walk flags
  are the most common way a correct repair gets reported as a catastrophe.
- **Never evict a store directory on store-side evidence alone.** A directory with no `SKILL.md`
  of its own can still be load-bearing, because a harness view may symlink to it. Before
  archiving or removing any such directory, resolve inbound links (`find -L <harness roots>
  -maxdepth N -type l -name '<name>'`, then `realpath` each) and refuse the move when one lands
  there. "Empty" has to be decided from the dependents, not from the store.
- **Snapshot the worktree and write a rollback manifest BEFORE the first bulk mutation.** Bulk
  consolidation is reversible only if both exist: a commit in every tree you will touch, and a
  per-operation manifest recording the inverse. The verification step that can trigger that
  rollback is part of the mutation, not a follow-up — the over-reach is *discovered* by the
  verify, and by then the manifest is the only recovery path.
- **Never write a governance stamp with a method you did not run.** When a registry's count or
  refresh stamp is wrong, either recompute it by actually running the producing process, or
  leave the check failing and name it as debt. Hand-editing the number or timestamp to make the
  gate green is fabrication, and it destroys the only signal that would have caught the drift.
- **A repaired link must be re-probed, not assumed.** After repointing, assert
  `os.path.exists(link)` AND that it resolves to a `SKILL.md` — a link that now points at a directory
  without one is still a lost capability, and it will not appear in the broken count again.
- **Dedupe the walk by realpath before mutating.** A sweep across overlapping roots (the store plus a
  profile tree that mirrors it) visits the same physical link twice; the second visit then throws
  `FileNotFoundError` on a link the first visit already removed, aborting the run mid-plan. Keep a seen
  set keyed on `(realpath, path)` — the counted total is otherwise inflated as well.
- **Verify every mutation from its own log, not from the tool's summary.** Re-read the apply manifest
  after the run and stat each destination; a partial apply that reports success is the normal failure
  shape here. The check is `defects == 0`, computed from disk.
- **A new check that reports `0` on an empty input space is the most dangerous shape of decoration.**
  The `merge_completeness` check first shipped reading `/root/.hermes/skills/.archive_skills_wave2` —
  the tombstone registry is at `/root/.hermes/.archive_skills_wave2` (a sibling of the skills root,
  not a child). It found no tombstones and printed a clean `0`. Diagnosis rule: when a check reports
  success, read its **input count** too — `tombstones: 0` beside `count: 0` is a broken path, not a
  healthy library. Make the empty case an explicit FAIL (`cannot witness`), never an implicit pass.
- **Fix the coverage key before trusting the count.** The same check deduped candidates by *target*
  file, and four Wave-2 tombstones share one target (`skill-portfolio-audit`) — so three were never
  examined and the check could not have found their loss. A dedupe key is a coverage decision; when
  several inputs collapse to one key, prove each is still individually checked.
- **A partial apply is the normal failure shape — isolate every operation.** A pointer-repair pass
  wrote 5 of 8 planned edits and then aborted on an `EPERM`, because one edit had no per-item error
  handler; the second run reported the rest as "already applied", which reads like success. Wrap each
  operation, keep going, and report `applied / skipped / failed` as three separate numbers. Compare
  them against the dry-run plan — a mismatch is a failed run, not a partial success.
- **`EPERM` on write is not a permissions bug — check `lsattr`.** `/root/AAA/governance` carries the
  **immutable** attribute (`i`), which refuses writes even for root and by design. Editing a file there
  is a governance mutation, not a cleanup: report it as locked debt and leave the flag alone. Clearing
  an immutability flag to make a pointer edit land inverts the authority order.
- **A `.bak` written beside the file it backs up pollutes the tree it is meant to protect.** Backups
  belong outside every scanned root — the same rule as the mirror backups. A stray `.bak-<ts>` inside
  a skills or instructions tree is counted by the next census and, in a package, can register as a
  dead internal pointer.
- **Classify emptiness structurally, not from a top-level listing.** A store directory holding no
  `SKILL.md` may be a container of sub-skills, and a directory whose only children are
  `references/`, `__pycache__`, or fixtures is a live skill whose body sits one level up. Decide
  with a recursive body check plus an inbound-link check, never from one directory level.

- **Before concluding a rule does not exist, check that its owner skill can actually load.** An
  unreachable governance skill is indistinguishable from a missing one at the point of use: the agent
  re-derives the procedure from priors, gets it subtly wrong, and reports the gap as newly discovered
  knowledge. Measured: a session re-derived a notation-collision doctrine that a skill on disk already
  stated verbatim, because that skill returned `not found` while the catalog advertised it. A settled
  doctrine being "rediscovered" is a reachability symptom first and a doctrine gap second — resolve the
  owner by name, and if it is unreachable, mint the address before doing anything else.
- **One census, many consumers — never fork a second counter.** A checker that re-derives its own count
  beside the canonical one guarantees the two will disagree eventually, and nothing reconciles them:
  a registry carried `drift: 0` for weeks precisely because a hand-era counter sat beside the real one
  with no reconciliation path. Every gate, report, and doc must **read the single census** (its
  `--json` output) rather than count the tree itself; two independent counters is the mechanism by
  which a stale claim survives every audit.
- **Severity is a three-tier ladder, and the third tier is the one that keeps a sensor honest.**
  **FAIL** = a capability is broken right now (a link resolving to nothing — a capability deleted
  silently). **WARN** = carried debt that was already true before the run (shells, diverged twins, case
  drift, name collisions): real, but failing on it makes the gate permanently red and therefore ignored.
  **INFO** = debt measured for the record with **no gate attached**, for a property so pervasive that a
  warning would fire on every run and teach nothing — a declared field covering 0 of ~480 skills, for
  instance. A gate that cannot go green on a healthy system stops being read; the honest response is to
  keep measuring it and let the number move, not to drop the check. Never promote an INFO finding into a
  bulk retro-fit on the strength of the measurement alone: covering hundreds of files is a migration with
  its own blast radius, and it needs its own decision. A **newly added check is calibrated on its first
 run, not shipped red**: FAIL stays reserved for a capability broken right now, and a gate that
 fires on a healthy tree is read once and then ignored. A **by-design property belongs at INFO,
 never WARN** — WARN is for debt that can be paid off, and a deliberate permanent property (a
 harness root that is a symlink farm, reading empty under a plain walk) can never clear, so
 warning on it every cycle is the same decay by a slower route. Keep the instruction text and its
 reason; drop only the level. The verdict line then means something, and every surviving WARN is a
 real decision nobody has taken yet.
- **A bundled skill's directory casing is owned by the updater — never normalise it.** Case-drift
  detection must exclude every name listed in `~/.hermes/skills/.bundled_manifest`, or it reports a
  large false-positive set (53 in one measurement) and invites a "fix" that renames files the next
  `hermes update` will overwrite or re-seed. Casing is drift **only** when the entry is
  federation-authored. Read the manifest before accusing the tree.
- **Resolve a bundle's members against every root before judging it broken — or new.** Bundle files
  live in `/root/.hermes/skill-bundles/*.yaml` and each member name resolves through *any* root the
  loader reads, including nested category paths — a shallow (top-level or two-deep) glob reports most
  members of a fully-live bundle as phantom, inventing a gap that then gets "filled". Collect candidate
  names with a recursive `**/SKILL.md` walk across all roots, then diff. The same check decides whether a
  proposed bundle is genuinely new: one whose members already belong to existing bundles is a **rename**,
  and adopting it multiplies the decision surfaces it claims to reduce.
- **Verify a detector's finding against disk before acting on it.** A gate that reports drift, a
  collision, or a shell is making a claim, not observing one — the finding itself must be probed
  (is this entry bundled? does the target actually differ? is the body really absent?) before any
  repair runs. Acting on a detector's output without re-deriving it turns one wrong predicate into
  dozens of destructive edits.
- **A collision sensor must distinguish CITING a symbol from REDEFINING it.** A probe that fires on
  every mention of `T1`/`C20` flags the documents that agree with canon — measured 2026-09-16: an
  intake artifact that quoted our own floors was reported as a FATAL notation collision. Verdicts now
  depend on what the artifact does with the symbol (assignment markers → redefined; context agreeing
  with the canonical meaning → reference). A sensor that cries wolf gets switched off, and then the
  real collision walks through.
- **Per-harness variant directories are not duplicate owners.** `<skill>/<harness>/SKILL.md` (claude,
  kimi, opencode, openai) are variants of the *parent* skill; keying collision detection on the
  directory basename reported 2 false name collisions. Exclude the variant shape, and key identity on
  frontmatter — never on the folder.
- **But two DIFFERENT skills' variant dirs can share one folder name, and a basename-keyed Grouper
  will merge them.** `<skill>/hermes/` under two different parents puts two unrelated bodies in one
  bucket; a converge tool built that way planned to replace the hold skill's body with a link to the
  seal skill's body. A plain harness-name exclude is the correct test *only if* no real namespace
  directory bears that name — probe for it (`find <store> -type d -name <harness>` and check whether
  the candidate holds a `SKILL.md`) before trusting the name test. Two "smarter" shape tests were
  tried and both leaked on a stale container that held only the variant child and no `SKILL.md`.
- **A basename-keyed index cannot see a case-twin.** On a case-sensitive filesystem `Foo/` and `foo/`
  are two different keys, so a check that groups by `os.path.basename` reports nothing while both
  paths load and carry different bodies. Group case-insensitively *in addition to* the exact key, and
  report the family — this class appeared as 7 families in one store, 5 of them divergent.
- **Identity is TWO fields, and a check must say which one it keys on.** `id:` is the canonical /
  namespace identity; `name:` is the **routing** identity — the field the loader reads
  (`frontmatter.get("name", <folder>)`) and dedupes on. They are legitimately different strings
  (`id: aaa-agent-invariants` vs `name: ASI-agent-invariants`), so a single-field helper is a silent
  mis-key: a parser that returns the FIRST of `id:`/`name:` it sees is keyed on the id whenever `id:`
  comes first, i.e. always, while its message claims to be keyed on the name. **Detector of this bug:
  two implementations of the same check disagreeing on the count** (one said 7, the other 4) — never
  ship a sensor that fails its own cross-check. Return both fields; key each check explicitly.
- **Same `name:`, two bodies = one is dropped in SILENCE.** The loader dedupes FIRST-WINS
  (`if name in seen_names: continue`), so a divergent body that shares a routing name can never load,
  chosen by directory-walk order, with no error on any surface. This is worse than the visible
  duplicate-name case, because a visible duplicate makes an agent hesitate while this one just serves
  whatever the walk reached first. Report it as its own finding, keyed on `name:`.
- **Prove "this is a copy" by inode before calling anything drift.** A path that *resolves into the
  store* through a symlink carries no independent copy: `os.stat(a).st_ino == os.stat(b).st_ino`.
  A comparison that reads such a path and prints "mirror/stale copy differs from the live owner" is
  publishing a false **cause** — and the remedy that cause implies (copy the owner over the mirror
  path) writes *through* the link onto a body inside the store, silencing the warning by overwriting
  canon. Classify by whether the path is a link: a linked view → the divergence is a store defect; a
  real file → mirror drift. Print the inode pair before deciding.
- **A sensor that cannot fail is decoration — but a sensor that fails on purpose must be regression
  tested.** `symbol-probe.py` carries a case file (`/root/scripts/tests/symbol-probe-cases.txt`) and
  the chaos sweep re-runs it (`C12 sensor_regression`), so a future edit that softens the probe is
  caught by the sweep instead of by the next corrupted import. The fix for a false positive is
  precisely the edit that creates a false negative — in one session a probe fix silently cleared two
  genuine symbol redefinitions as "cites canon" until the case file caught them.
- **A capability census must cover every surface, not just the skill tree.** MCP servers have the same
  failure mode as skills: `configured` is not `capable`, and a server listed but unreachable is a
  phantom capability. Derive a `routable` flag from a live probe, keep an explicit
  `disabled_intentional` class with a declared owner so a later agent does not "fix" a server that
  was switched off on purpose, and let the sweep FAIL on any enabled-but-unreachable entry.
- **A bundle that loads more than a dozen skills is a library, not a cockpit.** Measure each bundle's
  member count and approximate token weight; a bundle pulling ~49k tokens into every trigger defeats
  progressive disclosure, which is the reason bundles exist. Split by mission, and keep domain
  verticals out of cross-cutting bundles — they load on their own triggers.
- **A profile copy that is a real file rather than a symlink is drift, not a view.** Relink it to the
  live owner from a script that takes a backup tarball first; never delete the copy, and skip names
  whose owner is ambiguous rather than guessing which body is newer.
- **A drift WARN is routinely summarised as "duplicate owners", and the label picks the wrong remedy.**
  Sweep findings (`profile_stale_mirror`, name collisions) get written up in receipts as *"two live
  owners → merge decision, HOLD for the human"*. Those are different defects with different owners:
  stale mirror = mechanical re-sync the agent may do; duplicate owner = a human judgement. Classify by
  **path shape**, never by the label in the report:
  ```
  flat    …/skills/<name>/SKILL.md                        <- migration leftover (pre-reorg layout)
  authored …/skills/<domain>/<organ>/<name>/SKILL.md      <- a real owner
  one flat + one authored, same name   -> MIRROR_DRIFT    -> re-sync the flat copy
  two authored, differing hashes       -> DUPLICATE_OWNER -> HOLD, human decides
  ```
  Print the pair (`path + sha256 prefix` for both) before deciding — the reading takes seconds, and the
  cost of skipping it is double: a machine task escalated to the sovereign as a decision, while the
  genuine split-sovereignty case sitting beside it goes unnoticed because the whole class was filed as
  "needs a human". `scripts/mirror_or_duplicate.py` does this for every colliding name at once.
- **Re-probe a sibling's receipt before either repeating it or absorbing it.** When another session has
  already written a receipt for the same input, the remaining work is not "do it again" and not "trust
  it" — it is to re-derive its load-bearing numbers yourself (census, regression suite, `witness_hash`,
  `git log -1` times against the artifact's arrival time). Cheapest proof that nothing was duplicated:
  the witness hash and the loadable count are unchanged from before the pass. When the re-probe
  contradicts the receipt, keep the receipt's original sentence standing and append a dated
  **CORRECTION** section — a correction in place, not a new report file, or the correction becomes the
  accumulation the pass was auditing.
- **Before concluding that an artifact or commit does not exist, enumerate the repos that could hold
  it.** Each organ is its own git repository, and the scripts that run a sensor often live outside the
  organ they describe, so `git -C <organ> cat-file -t <sha>` returning `no-such-object` proves only
  that *that* repo lacks it — probe every candidate (`/root/scripts` is a repository of its own)
  before reporting a receipt as fabricated. A "phantom commit" verdict produced from the wrong search
  root is the same class of error as a sensor scoped to the wrong tree.
- **Hold a repair when a second session is writing the same tree.** Two writers on one tree make any
  re-sync unsafe regardless of authority: check for other live kernel runners (`ps -eo pid,etimes,cmd`)
  and for a shared store whose `-wal`/mtime moved inside the last few minutes, then name the hold as
  *timing*, not as a blocked authority. "Authorized but racy" and "not authorized" are different
  verdicts; reporting the second when it is the first teaches the next agent to wait for a human who
  was never needed.

- **A new check must be proven able to fire before its verdict is trusted.** Three shapes of
  decoration pass every code review. The check that *reads* a value it never compares — a loader
  index loaded into a variable that no branch ever uses — announces an invariant that nothing tests,
  and still emits a verdict, so the missing comparison is invisible. The check that **never consults a
  declaration that exists for it** is the same defect from the other side: a taxonomy or allow-list
  constant defined at module scope and referenced only on its own definition line is not a control,
  and without it the check reports structure as damage — measured, a container list declared but never
  read turned 4 real findings into 48, and a gate that is noisy on a healthy tree is switched off long
  before it finds anything. Grep each check for the declarations it ought to use; a name appearing
  exactly once in a file is consulted zero times. And the check whose two sides
  are computed from the **same expression**, differing only by `isfile` vs `exists` on the same
  realpath: no input can ever make them disagree. Extract the predicate verbatim into a throwaway
  script, enumerate the inputs that would take the failing branch, and require at least one; a
  predicate with no reachable failing branch is not a check. Widen the scope in the same pass — a
  detector watching one root cannot catch a false claim about another, so measure every root from a
  single enumerated table on every cycle rather than adding paths ad hoc.

- **An advertised skill index is a claim, not existence.** The prompt-injected catalog (and any
  registry, README or report listing) can name a skill that no longer resolves: `skills_list` shows
  it while `skill_view` returns `not found`. Resolve a skill with `skill_view` before loading it,
  citing it, or concluding it is merely off-limits — a name that cannot be opened is a broken
  pointer to report, and until it is fixed the loader re-derives the procedure from priors while
  every surface looks healthy.
  **The reverse direction is quieter and needs the opposite report.** A body that exists in the
  canonical store under a **nested category path** can be absent from both `skills_list` and
  `skill_view` — every surface says the capability is missing while it sits on disk, editable, being
  loaded by nothing. Before concluding a skill does not exist, resolve it by path
  (`find <store> -name SKILL.md -path '*<name>*'`) and say which of the two failures you found: a
  listed-but-unresolvable name is a broken pointer; an unlisted-but-present body is a resolution gap.
  Mistaking the second for the first is how a real skill gets declared off-limits and left unpatched.
  Measured again on two newly created packages: both were written, both sat on disk with a complete
  body, and `skill_view` returned *not found* for each while every sibling name in the same tree
  resolved. Treat "the create succeeded" and "the skill loads" as two separate claims, and test the
  second one directly.
- **`skill_manage(action='create')` takes a SINGLE directory name for `category`, never a path.** A
  slash-separated coordinate (`domains/general/apex`) is rejected outright — *"Categories must be a
  single directory name"* — and the operations batch is atomic, so the rejection rolls back every
  OTHER operation in the same call, including patches to unrelated skills that had already applied.
  Pass one segment, or omit `category` entirely and settle placement separately.
- **A skill `description` is budgeted for the always-loaded index.** Discovery text must be one short
  sentence, trigger first, ending with a period (~60 chars). Longer text is refused at write time and
  rolls back its batch the same way; the index truncates at ~57 chars and destroys the routing signal
  regardless. Put the detail in the body, not the description.
- **Do not mix a `create` with `patch` operations in one batch.** The two above are write-time
  validation failures that fire on the FIRST operation but abort the WHOLE array, so a malformed
  create silently discards the patch work beside it and reports only the create error. Sequence them:
  create and verify first, then patch.
- **A curator write can be refused for the skill's PATH, not its content.** The federation's pre-tool
  gate trips on the directory name as well as the payload, so a skill under a legal-, medical- or
  trading-worded path (`court/`, `audit/`, `well/`) is held even for a plain read, and `skill_manage`
  against it is held too — deterministically, whatever the patch text says. A retry produces an
  identical receipt, because the hold is a property of the path and not of the edit. The route that
  works is to apply the change with `patch` against the skill's canonical file path, citing the real
  evidence for it. Read the refusal's reason before blaming the content, never reword a payload to
  slip past a HOLD, and never report the skill as unwritable — a held write is blocked, not refused
  on merit.
- **An autonomous curator write is refused for OWNERSHIP, and that is a THIRD refusal class.** A
  skill authored outside the curator reports `created_by=None` and is treated as user-owned: patches
  and file writes are refused no matter how on-topic the change is, and no rewording clears it. This
  is systemic across a hand-authored library — it is not a property of the one skill you tried. Three
  refusals now share a shape and need three different remedies, so read the reason string before
  acting: a **PATH** hold (the pre-tool gate tripping on a directory word) means apply via `patch`
  against the canonical path; a **CONTENT-pattern** hold means report it and stop; an **OWNERSHIP**
  refusal is a request to the human, and the only correct move is to name the topical owner you
  could not write to and ask for `hermes curator adopt <name>` on it.
- **Never re-home a lesson into a writable skill that does not own it.** When the topical owner is
  unreachable, the temptation is to file the finding under the nearest writable neighbour; that is
  how a library grows a second, thinner owner for one doctrine and then drifts. An unroutable lesson
  is reported, not relocated — a curated skill in the wrong package is worse than an unfiled note,
  because the next agent will find it and believe it belongs there.

  **The same gate also refuses on CONTENT PATTERN, and that class can never clear.** A skill whose
  purpose *is* the flagged idiom — a package of `getMe` identity probes, credential-name comparisons,
  token-scoped URLs — trips an exfiltration/supply-chain rule on every write, because the rule matches
  the shape of the idiom rather than a leaked value. Always start from a measurement: grep the package
  for a literal value matching the shape the rule hunts. Measured once: 29 findings, **0 literals**,
  every hit a `${VAR}` reference written the correct way. Two consequences follow, and both matter.
  First, the offered remedy ("retry without the flagged content") is **unsatisfiable** when the flagged
  content is the package's whole reason to exist, so the gate is a wall presenting as a policy — report
  the shape, do not hunt for the exit. Second, the gate is usually **opt-in and documented as
  bypassable by its own author**, which means the escape route exists and taking it is the defect, not
  the fix: bypassing it once, to prove it is loose, is how the auditor becomes the incident. Report
  `BLOCKED_AT_GATE` with the operation, the finding count, and the literal count; leave it for the
  owner. Never rewrite a correct `${VAR}` idiom into a weaker form to satisfy a scanner.

## Support files

- `scripts/skill_resolution_audit.py` — the resolution detector. Reports (a) names mapping to
  >1 distinct file and (b) directories whose basename disagrees with the frontmatter `name:`.
  Skips `.archive-*`/backup trees; treats symlink mirrors of one physical file as one copy.
  Exit 1 when anything is unreachable.
- `scripts/dependents.py` — inbound-dependency resolver for a canonical directory, used before any
  move, archive, or removal. Walks WITHOUT following links and resolves each symlink's target; prints
  the dependent and what it points at. The `find -L … -type l` one-liner it replaces is inverted (see
  LAW 2) and reports zero for a directory that has dozens.
- `scripts/mirror_or_duplicate.py` — classifies every colliding skill name as `MIRROR_DRIFT`
  (one authored path + flat migration leftover → re-sync) or `DUPLICATE_OWNER` (two authored
  paths with differing hashes → HOLD for the human), read-only, exit 1 on any real duplicate
  owner. Run it before acting on any "duplicate owner" line in a report.
- `references/address-vs-storage.md` — the two-tree probe recipe: the link-only and storage-only
  scans, the per-entry classifier (`address` · `body_held_here` · `bundled` · `generation` ·
  `name_ambiguous`), the assertion discipline for absence claims, and the add-an-address ladder.
  Read before any census, move, rename, or re-merge of the skill tree.
- `references/twin-collapse-runbook.md` — collapsing two REAL bodies into one body plus addresses:
  arena probe, backup-and-reversal shape, the classification table (superset / newer / union / design
  fork), the mechanical union merge, container-collapse safety, and verification by load-surface
  delta. Read before reducing any duplicate pair or family to a single body.
- `references/capability-absence-audit.md` — before writing "not implemented", "no capability owns this",
  or a gap table: the three verdicts (**absent** / **built-never-wired** / **present**), the search
  order across layers with prose **last**, the wiring census (scheduled · service · runtime-import ·
  state-file), the index-claim check (listed-but-unresolvable vs present-but-unlisted, plus the
  selector's leading window), and the reporting rules. A false gap gets *built*, which duplicates what
  already existed.
- `references/multi-root-entropy-audit.md` — the multi-root model, the always-on entropy gate
  and its check table, the divergence/index-cost measurements, the source-of-truth decision, and
  §7 the consolidation procedure (census buckets, writer-first ordering, bundled-skill rule, the
  counting and verify rules). Read when the symptom is stale, missing, or divergent content
  across trees rather than an unloadable name.

## Adjacent skills

| Skill | Relationship |
|---|---|
| `FORGE-skill-linter` | Trigger-clause and description linting. Resolution is a pre-check that can invalidate it. Bundled — read-only from here. |
| `skill-audit-methodology` | Content, redundancy, and pruning methodology. User-owned. |
| `FORGE-symlink-audit` | Federation broken-symlink scanning. Bundled — its blanket `-delete` recipe is NOT safe inside a git-tracked skills tree; use the deletion rules above. |
