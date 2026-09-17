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


**Do not let an upstream-bundled skill move.** Skills named in `~/.hermes/skills/.bundled_manifest`
belong to `hermes update` and must stay harness-native — relocating them breaks the sync.

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

**Never auto-merge diverged twins.** A diverged pair is a judgement call; HOLD it and report.

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
1. symlink dependents   find -L <roots> -type l | xargs -I{} sh -c 'readlink {} | grep <dir>'
2. AGENTS.md refs       grep -rn "<name>" /root/AGENTS.md /root/AAA/AGENTS.md
3. bundle refs          grep -rn "<name>" /root/.hermes/skill-bundles/
4. registry refs        grep -rn "<name>" /root/AAA/skills/*.yaml /root/AAA/skills/*.json
5. alias refs           grep -rn "<name>" /root/AAA/skills/SKILL_ALIAS_TABLE.json
6. loader path refs     grep -rn "<name>" /root/.hermes/skills/.matrix-index.json
```

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
| Dead internal pointer | SKILL.md cites a file under `references/` (or `templates/`, `assets/`) **and the package HAS that folder** but not the file | the body instructs a load that cannot succeed |
| Headless shell | canonical top-level dir with no `SKILL.md` anywhere beneath | looks like a capability, loads nothing |

The gate's `dead_internal_pointers` check covers class 2 (FAIL-class). Two predicates keep it
honest, and both were needed on the first run: a mention is a **real pointer only when the top
folder exists in that package** (otherwise the cited path is prose or an example), and a match
truncated by a following character (a prefix such as `assets/index-`) is a **glob, not a pointer** —
drop it. Without those two filters the check fires on hundreds of doc examples and is switched off
within a week. Measured: 397 candidate mentions across 845 packages → 74 real dead pointers in 21
packages.

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
a mechanical repair. Print what you deliberately left out. Verify with
`git ls-tree -r HEAD <store> | grep ^120000` that the paths are recorded as **mode 120000**; a fresh
checkout then reproduces the shape instead of resurrecting the duplicate bodies. Then state which
**branch** the commit landed on — a store whose worktree sits on a long-lived proposal branch has a
repair that a later `git checkout main` will revert, and that is a fact the next agent needs.

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
- **Classify emptiness structurally, not from a top-level listing.** A store directory holding no
  `SKILL.md` may be a container of sub-skills, and a directory whose only children are
  `references/`, `__pycache__`, or fixtures is a live skill whose body sits one level up. Decide
  with a recursive body check plus an inbound-link check, never from one directory level.

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

- **A new check must be proven able to fire before its verdict is trusted.** Two shapes of
  decoration pass every code review. The check that *reads* a value it never compares — a loader
  index loaded into a variable that no branch ever uses — announces an invariant that nothing tests,
  and still emits a verdict, so the missing comparison is invisible. And the check whose two sides
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

## Support files

- `scripts/skill_resolution_audit.py` — the resolution detector. Reports (a) names mapping to
  >1 distinct file and (b) directories whose basename disagrees with the frontmatter `name:`.
  Skips `.archive-*`/backup trees; treats symlink mirrors of one physical file as one copy.
  Exit 1 when anything is unreachable.
- `scripts/mirror_or_duplicate.py` — classifies every colliding skill name as `MIRROR_DRIFT`
  (one authored path + flat migration leftover → re-sync) or `DUPLICATE_OWNER` (two authored
  paths with differing hashes → HOLD for the human), read-only, exit 1 on any real duplicate
  owner. Run it before acting on any "duplicate owner" line in a report.
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
