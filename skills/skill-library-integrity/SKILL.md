---
name: skill-library-integrity
description: "Use when skills won't load, duplicate, or diverge."
version: 1.0.0
owner: AAA
category: governance
tags: [skills, hygiene, symlink, resolution, audit, curation]
floors: [F1, F2, F4, F11]
autonomy_tier: T1
---

# Skill Library Integrity

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

**Never rename the skill to match a typo'd directory.** The name is the trigger the agent
matches on; the directory name is only the index key. Rename the key, keep the trigger.

### 4. Prove the repair — a file count proves nothing

```
skill_view(name='<the-skill>')     # must return content, not "Ambiguous skill name"
```

A repaired tree that still refuses to load is not repaired. Same discipline as verifying any
tool change: re-invoke and read the returned fields, never the exit code.

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
- **Two trees sharing a skill name are not in sync.** Names agree while bodies diverge —
  compare content hashes per shared name, and report the diverged fraction, not the shared
  count. A high shared count reads as health and hides the drift completely.
- **Never fork a second copy of the detector.** Run the installed gate by path. A forked copy
  in a skill directory drifts from the wired one and re-creates the exact defect being hunted.

## Support files

- `scripts/skill_resolution_audit.py` — the resolution detector. Reports (a) names mapping to
  >1 distinct file and (b) directories whose basename disagrees with the frontmatter `name:`.
  Skips `.archive-*`/backup trees; treats symlink mirrors of one physical file as one copy.
  Exit 1 when anything is unreachable.
- `references/multi-root-entropy-audit.md` — the multi-root model, the always-on entropy gate
  and its check table, the divergence/index-cost measurements, and the source-of-truth
  decision. Read when the symptom is stale, missing, or divergent content across trees rather
  than an unloadable name.

## Adjacent skills

| Skill | Relationship |
|---|---|
| `FORGE-skill-linter` | Trigger-clause and description linting. Resolution is a pre-check that can invalidate it. Bundled — read-only from here. |
| `skill-audit-methodology` | Content, redundancy, and pruning methodology. User-owned. |
| `FORGE-symlink-audit` | Federation broken-symlink scanning. Bundled — its blanket `-delete` recipe is NOT safe inside a git-tracked skills tree; use the deletion rules above. |
