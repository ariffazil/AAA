---
name: skill-taxonomy-reclassification
description: "Use when a skill library needs taxonomy or a merge plan."
version: 1.0.0
triggers:
  - "map my skills"
  - "skills are too many"
  - "uncategorised skills"
  - "skills not general"
  - "condense skills"
  - "compress skill library"
  - "categorise skills"
  - "skill taxonomy"
  - "root bucket skills"
  - "skills missing a category"
  - "skill compression plan"
  - "merge these skills"
floors: [F2, F4, F11]
---

# Skill Taxonomy Reclassification

Turning a flat / uncategorised skill library into a real taxonomy, and deciding which skills fold
into which. This is the classification + merge-planning class. Auditing for quality, pruning,
archiving and naming are separate concerns (see `skill-audit-methodology` and
`federated-skill-architecture` — both user-owned; read them, do not rewrite them).

## Always-on rules

**Category is derived from the DIRECTORY PATH, not frontmatter.** The loader reads the parent
directory; the `category:` frontmatter field is inert. Categorising a skill means MOVING its
directory (or symlinking it) under a category dir. Editing frontmatter changes nothing about how
the library is grouped or counted.

**A root-level bucket is not a category.** Skills at the library root report an EMPTY category and
look "general", but they are a mixed population. Split before planning:

- prefix-prefixed (`AAA- AGI- ASI- APEX- AUDIT- FORGE- KERNEL- RSI- FLAME-`) → federation machinery
- third-party product names (`runpod`, `qwencloud`, `minimax`, `firecrawl`) → tool/integration
- the remainder → genuinely general capability

**Hash-compare against the canonical catalog BEFORE planning any merge.** In this federation a
root bucket is mostly mirror drift, not authorship. Four states, not two:

| state | meaning | action |
|---|---|---|
| `IDENTICAL` | same content, other copy exists | safe zero-loss removal |
| `CANON_NEWER` | canonical copy is newer | replace the local copy — never merge it |
| `LOCAL_NEWER` | local copy is ahead | push back to canonical FIRST |
| `CANON_ABSENT` | only exists locally | safe to author/merge, but it is federation surface |

Merging a `CANON_NEWER` entry writes staleness into canonical. Merging a `LOCAL_NEWER` entry
silently deletes the newer authoring. Both are silent — nothing errors.

**More than one axis, never one — and three is the target.** One axis forces federation machinery
and portable capability into the same drawer, which is exactly how a root bucket forms. Two axes is
the floor that stops that, not the destination. Two-axis vocabulary, if a proposal needs it:
general = Productivity, Software Dev, Creative, AI Agents, Research, Media, DevOps, Communication,
Knowledge, Security, Data, Web; federation = Governance, Federation, Domains, Personal, arifOS.

**Who owns the file decides whether you may move it. Split before you restructure.**

Some skills are *bundled* — shipped in the harness repo and re-seeded into the profile by
`hermes update` / `hermes skills repair-official` / `reset` / `opt-in`. The seed always writes the
stock one-level layout (`<name>/` or `<category>/<name>/`). It does not know about your taxonomy and
will not respect it. Measured on this install: of 402 live skills, 282 are listed in
`.bundled_manifest` — a majority the profile does not own.

| class | who owns the path | may you restructure? |
|---|---|---|
| `builtin` — in `.bundled_manifest` | the updater | **No.** It re-seeds. Moving it creates duplicates. |
| agent-authored — not in the manifest | you | Yes, freely. |
| canonical-elsewhere — symlink to `/root/AAA/skills` etc. | that repo | Only the symlink, never the target. |

Get the class from the manifest, never from a guess:
`grep -c "^<skill-name>:" .bundled_manifest` (one line `name:hash` per bundled skill).

**A deep taxonomy must be a GENERATED VIEW, not a storage layout, when most files are updater-owned.**
Measured result of ignoring this: a 4-level `domains/<d>/<o>/<c>/<skill>` move over 399 skills was
~22% reverted within two hours — 116 bundled skills re-seeded outside the tree, 89 coordinates
broken, and 37 names left resolving to TWO different physical files (first-wins, non-deterministic).
Nothing errored. The fix is to leave files where their owner puts them and emit the coordinate as an
index the agent reads, so it survives updates because it is derived rather than stored.

**The working shape: storage follows ownership, coordinate is derived.**

| class | lives at | coordinate comes from |
|---|---|---|
| authored (not in `.bundled_manifest`) | the taxonomy tree | its own path |
| bundled (in `.bundled_manifest`) | the updater's one-level path | a generated index (`.matrix-index.json`) |

Generate with a standalone re-runnable script, read it from `_get_category_from_path()` with an
mtime-keyed cache, and fall back to upstream behaviour when the file is absent — never let the
reader fail. Cron it (a few times a day is plenty; a harness update is the only event that changes
the answer). Prove it three ways: run the generator twice (identical sha256), simulate a bundled
re-seed and confirm the coordinate still resolves, and delete the index and confirm the library
still works with degraded labels.

**One-level category is the only depth the writer supports.** `_resolve_skill_dir` in
`tools/skill_manager_tool.py` builds `base / (category or "") / name`, and `_validate_category`
rejects `/` outright. So a skill created through the normal tool path lands one level deep no matter
what the tree around it looks like. Either patch the writer to resolve a category name to a
coordinate, or keep the authored layer one level deep and generate the deeper axis on read.

**No `Other` category.** Unclassifiable is a merge-or-archive signal, not a parking space. Parking
it guarantees it leaks back into the root bucket next sweep.

**A citation to a skill is itself a claim that needs verifying.** The reference implementation: a
prompt or doc says *"Skill: `foo` (5 capabilities)"* and no artifact named `foo` exists anywhere.
That is how `governed-uncertainty` sat as a dead pointer — named in the runtime persona and in a
sealed doctrine, promised with a capability list, never built. Nothing errored; the promise just
quietly did nothing. Sweep for this class instead of waiting to trip over it:
`~/.hermes/scripts/dead-pointer-sweep.py` (cron weekly) writes
`~/.hermes/docs/skills-matrix/dead-pointers.json` + `DEAD_POINTERS.md`.

**Ground truth for a citation check is the LOADER'S EXPOSED NAME SET, not the directory tree.**
`skills_list()` returns frontmatter `name:`, and `skill_view` matches both the directory name and
the frontmatter name. So `mmx-h3-video` is a *correct* citation even though its directory is
`h3-video`. A first sweep compared citations against directory basenames and reported two false
dead pointers — a diagnostic that cries wolf is worse than no diagnostic. Build the reference set
from `skills_list()`, then add the directory basenames as a tolerance. Triage each hit:

| class | meaning | action |
|---|---|---|
| `ALIAS` | cited name is a live skill's frontmatter name | not a bug — resolves fine |
| `EXTERNAL` | real skill in another home (profile / bundled / optional) | profile gap, not a bad citation |
| `STALE` | no artifact in any installed home | the real finding |

Split `SKILL.md` citations from `references/` citations. An operational citation sends an agent to
load something that is not there; a reference file recording what was cited at the time is doing its
job, and rewriting history to satisfy a linter is corruption, not hygiene. **Fix on touch, not in
bulk.**

**Symlinked mounts need a trust allowlist, or the security warning becomes noise.** The untrusted-
source guard resolves the skill path, so mounting a canonical catalog by symlink makes every load
warn "outside the trusted skills directory". Measured here: 53 of 406 live skills — every AAA-*,
substrate and WELL skill — warned on every load. A warning that fires on the majority of legitimate
loads teaches the reader to ignore it. Allowlist the first-party roots; keep the guard's teeth by
requiring BOTH that the lexical path sits inside the profile skills dir AND that the resolved target
is in the allowlist. Prove it with a negative control (a symlink to `/tmp` must still warn) —
without the control you have only tested that the warning can be silenced.

**Three axes: the coordinate that survives contact with F13.** The shape is an orthogonal path:

```
domains/<domain>/<organ>/<capability>/<skill>/SKILL.md
        general | geo | wealth | well | my-reality
                  aaa | apex | court | forge | workshop
                        ~60 families: mcp-ops, voice-stack, seal-ritual, court-audit, ...
```

Axis 3 (capability) earns its own directory level — do not fold it into the leaf name. Cross-cutting
queries ("every voice-stack skill, any domain") are then a path glob instead of a grep.

**Restructure by path, never by content. F13 constraint 2026-09-15: `all skills must remain`.**
The reform is a MOVE of directories plus SYMLINKs to the canonical catalog — zero merges, zero
folds, one SKILL.md per skill, byte-identical before and after. Merging is a *different* operation
and needs its own mandate; a taxonomy mandate is not a merge mandate. Verify with a sha256 multiset
of every SKILL.md before vs after: `content lost` must equal 0.

### The merge mandate (what to do when the mandate IS a merge)

When the sovereign asks for fragmentation collapsed — *"mcp skills all under one with proper flow,
GitHub skills one, governance one"* — the constraint above inverts: `all skills must remain` becomes
**`all names must resolve, one owner per capability`**. Full recipe, receipt format and grouping
table: `references/cluster-merge-recipe.md`.

Two rules are always-on for any merge, and both failures are silent:

**A merge unloads every skill whose trigger it dropped.** The umbrella's `triggers:` must be the
UNION of every member's, computed by a script that parses frontmatter on both sides — never by eye,
never from a hand-written list. A trigger that vanishes does not error; the skill simply stops
loading on the situation it used to catch, which is the exact situation the merge was supposed to
protect. Same discipline for `description`: its first ~57 chars must stand alone as a trigger.

**The shared indices are single-writer, so workers emit fragments.** `SKILL_ALIAS_TABLE.json`,
`SKILLS_INDEX.json`, `FEDERATED_SKILLS_REGISTRY_V3.yaml` and `PLACEMENT_MANIFEST.json` are read by
the loader and written by one generator. N concurrent merge agents each editing one of them is a
lost-update race that reports success and keeps only the last writer. Every worker writes its own
`alias-<cluster>.json` fragment into the workspace; the orchestrator folds the fragments in once,
after every worker has returned.

**Case-insensitive name collision is the cheapest duplicate detector, and it lies about being
safe.** Find the twins, then confirm they are really twins:

```bash
find <trees> -name SKILL.md -not -path '*/.archive*' \
  | sed 's|.*/\([^/]*\)/SKILL.md|\1|' | tr 'A-Z' 'a-z' | sort | uniq -d
```

A name pair like `FORGE-fastmcp` / `forge-fastmcp` **is not byte-identical**. Measured: every pair
sampled differed by 30-58 bytes, in frontmatter only — so a "safe zero-loss removal" of one copy
silently discards the newer header fields. `cmp -s a b` first; if it differs, `diff` it and fold the
delta into the canonical owner BEFORE any symlink replaces the other. Treat divergence as content,
not as noise to average away.

**Delete nothing, ever — alias everything.** The merge produces one canonical owner directory plus a
symlink at every name it absorbed. Verify by re-enumerating: the pre- and post-merge SKILL.md count
is equal, or every decrement is individually explained.

**A multi-writer git repo needs `flock`, because `index.lock` is not a lock.** Parallel merge agents
on one canonical tree race the index; git's own lock serialises a single command, not a
read-modify-write sequence. Every commit goes through the same lock file:

```bash
flock /root/.git-skill-merge.lock git -C <canonical> add -A skills/
flock /root/.git-skill-merge.lock git -C <canonical> commit -m "skill-merge: <cluster> — <what>"
```

**Genuinely different capabilities are not fragmentation.** Two skills that share a topic but not a
capability (operating a thing vs a procurement/selection reference for it) both stay; say which and
why in the receipt. A wrong merge is as damaging as no merge and is much harder to notice.

**Symlink topology for anything already canonical.** A skill whose physical home is outside the
harness root (`/root/AAA/skills`, `/root/.agents/skills`) gets a symlink leaf at its coordinate.
The harness then routes through the matrix without carrying a second drifting copy.

**Phase zero-loss first; the map is the deliverable, the merge is a separate gate.**
P1 (backup, remove byte-identical duplicates, re-verify) is reversible and can run unattended.
P2 (bulk merges, mass moves) is architecture mutation — produce the artifact, take the go/no-go to
F13. Do not collapse the untouched P2 back as an open question, and do not execute it unattended.

## Procedure

1. **Backup first, always.** `tar czf ~/.hermes-backups/skills-pre-taxonomy-<ts>.tar.gz -C ~/.hermes skills`
2. **Take ground truth** from the live sources (`references/inventory-sources.md` has the source
table and the parse gotchas — `hermes skills list` truncates names and wraps long ones onto
continuation rows).
3. **Run the classifier** — `scripts/skill-taxonomy-classifier.py` gives the uncategorised set, a
predicted category per skill, near-duplicate clusters, and the four-state drift map in one pass.
4. **Split the bucket** into federation / tool / general before reading a single skill body.
5. **Write the map artifact**, not a summary in chat: CSV (one row per skill: path, bytes, use_count,
tier, category, action, target) + `REPORT.md` listing every member under its merge target.
6. **Execute P1 only** (zero-loss dedupe), then verify live against the LOADER, not the filesystem:
the uncategorised count moved AND the skill still resolves from its surviving category.
7. **Escalate P2** with the artifact and a fat-first execution proposal.
8. **After any bulk move, run the verifier** — `scripts/verify-skill-tree-integrity.py` — before
   reporting. It proves four things at once: content multiset preserved, every map row resolves on
   disk, no row names a path that does not exist, and no stray SKILL.md escaped the tree. A count
   that moved is not evidence the map is right; only a row-by-row reconcile is.

## Reporting shape

- Give the reduction honestly as `N → M (x% fewer)` and say how many fold into how many mother skills.
- List the fattest merge clusters first (8→1 before 2→1); the shape of the win is what is judged,
  not the full table.
- Flag the drift reality separately from the taxonomy work — "most of this pile is mirror drift, not
  authorship" changes what the user should authorise.
- Offer one clean cluster as a sample before sweeping the rest.
- Deliver artifacts as absolute paths; do not paste the CSV into the reply.

## Pitfalls

- **Do not plan merges from frontmatter `category:`** — it is inert; a skill can declare a category
  and still load as uncategorised.
- **Do not trust a count from the startup banner or a truncated table.** Re-count from disk
  (`find <root> -name SKILL.md | wc -l`) and from the loader's own listing; they disagree, and the
  disagreement is usually the finding.
- **Symlinked skills count once but can appear twice** — the same skill reachable via a symlinked
  category dir and a real dir inflates cluster sizes. Resolve real paths before deduping.
- **Identical content in two places is not automatically removable** — confirm the surviving copy is
  in the loader's scan path, then prove it by loading the skill after removal.
- **`.usage.json` holds entries for skills already deleted from disk.** Usage evidence, not inventory.
- **Never merge a cluster of unknown-authoring skills unattended.** Take the go/no-go with the map in
  hand; the merge is one-way in practice even when technically reversible.
- **Container symlinks are a write hazard, not just a read path.** `skills/domains -> /root/AAA/skills/domains`
  means `makedirs(skills/domains/<new tree>)` writes straight into the canonical catalog. Break every
  container symlink BEFORE building the new tree, and assert `realpath(root) == root` first. The
  mounted skills stay reachable because their leaves are re-created as individual symlinks.
- **A symlink to a whole repo is not a skill mount.** `skills/wellness -> /root/WELL` pulled venvs and
  site-packages in as "skills" (a package named `typer` appeared 4×). Mount the skills dir, not the repo.
- **`_get_category_from_path()` returns `parts[0]` only.** A deep matrix therefore reports ONE
  category (`domains`) for every skill — worse than the flat bucket it replaced. Either put the
  most-queried axis first, or patch the reader: for paths deeper than `category/skill`, return the
  full coordinate with the leaf dropped. Fix the reader, not the ground truth; commit the patch so
  `hermes update` carries it (`local(arifOS):` subject prefix is the house convention).
- **Run the migration from a frozen CSV, and make it idempotent.** A 400-move loop dies halfway
  (timeout, OOM, session end) and leaves a half-migrated library. Every step must read the map,
  skip anything already at its target, and archive stragglers instead of deleting. Re-running the
  finisher must be safe; prove it by running it twice and expecting `newly placed 0`.
- **Never trust exit code 0 through a pipe.** `cmd | tail -60` reports the exit status of `tail`.
  A migration died at item 167 of 399 and still reported success. Write the durable artifact (frozen
  CSV) first, or check the artifact, never the pipeline's status.
- **Re-probe after acting, not just before.** The erosion above was found only by re-enumerating the
  live scan path an hour later. A taxonomy is not done when the move returns — it is done when a
  second enumeration agrees.
- **Never read the exit code of a piped command.** `python migrate.py | tail -60` reports `tail`'s
  status, so a job that crashed after 40% of its work reports success and the next session inherits
  a half-migrated tree believing it finished. Redirect to a log and check the real status, or leave
  the command unpiped. This is the reason the idempotent finisher above is mandatory, not optional.
- **A sha256 multiset proves nothing was LOST; it does not prove the map matches the DISK.** The
  content can be intact while rows name target paths that do not exist, because the content sits
  somewhere else. Every such row is a silent landmine: the next sweep reads the map, concludes the
  skill is gone, and re-authors or re-merges it. Reconcile row-by-row — for each row confirm its
  target resolves, and where it does not, report the actual location — then correct the MAP to
  match disk. Never move files to match a wrong map.
- **Some skills are nested INSIDE another skill's directory, not flat leaves.** Harness-profile
  variants (`<skill>/claude/`, `<skill>/kimi/`, `<skill>/opencode/`) and sub-skills
  (`<skill>/constitutional/`) each carry their own SKILL.md. A map that flattens by basename writes
  `.../<variant>`, while the move actually lands at `.../<parent>/<variant>` — and a move that ran
  from the same wrong path killed the whole batch partway. Give nested variants their own row with
  their real nested path, and treat a basename collision between siblings as the signal to look.
- **A tarball of the root is never a complete rollback once symlink topology exists.** Leaves that
  symlink to a canonical catalog outside the root carry no content inside the tarball, so restoring
  it alone leaves broken links. Rollback is three parts: the tarball (for the physically moved dirs)
  + the legacy `old→new` map + the canonical catalog left untouched. Test recoverability by
  extracting several random SKILL.md entries from the tarball, and state the three-part shape in the
  report so nobody assumes the backup alone is enough.

## Support files

- `references/inventory-sources.md` — where each count comes from, parse gotchas, upstream category
  label set location.
- `scripts/skill-taxonomy-classifier.py` — re-runnable: uncategorised bucket, TF-IDF nearest-centroid
  category assignment, near-duplicate clustering, four-state drift map. Emits CSV + JSON + markdown.
- `scripts/verify-skill-tree-integrity.py` — run AFTER any bulk move or dedupe: content multiset
  preserved (optionally against a pre-migration tarball), every map row resolves on disk, rows whose
  target does not exist reported with the real location, strays and flat-layout leftovers listed.
  Non-zero exit on any failure.
- `references/cluster-merge-recipe.md` — the merge mandate end to end: grouping a cluster into a
  real flow, divergent-twin handling, alias-and-verify, the per-cluster subagent brief, and the
  `MERGE_RECEIPT.md` shape (preserved / dropped / left alone).

## Scoring the layer (APEX × ZEN)

Canon: `/root/AAA/docs/APEX_T000_THEOREM.md`. Instruments live beside the generator:
`apex-zen-bridge-score.py` (state) and `apex-zen-paths.py` (future states). Both write to
`~/.hermes/docs/skills-matrix/`.

```
A = GM(F2,F4,F7,F10)      P = GM(F1,F5,F11,F13)
E = GM(F3,F4,F12,E1,E2)   X = GM(F6,F8,F9,Risk)      G = GM(A,P,E,X)
∂G/∂v = G/(4v)            C_dark = A·(1−P)·(1−X)
```

`G ≥ 0.80` → SEAL, `≥ 0.70` → SABAR, else HOLD. The smallest dial has the largest marginal effect
(Axiom 2) — fix the bottleneck, never the healthy dial.

**Never cite a rollback artifact you have not stat'd.** The migration script wrote its
`legacy-map.json` as the FINAL statement; the run crashed at item 167 of 399 so the file was never
created — and the completion report still listed it as the rollback path. The claim came from the
script's *intent*, not from the disk. A rollback claim is valid only after `test -f <path>` in the
same breath, and the map must be verified to cover every moved item (moved vs covered vs residual;
classify the residual, never leave it unknown).

**A citation to a skill is itself a claim that needs verifying.** A prompt or doctrine saying
*"Skill: `foo` (5 capabilities)"* with no artifact named `foo` anywhere is how `governed-uncertainty`
sat as a dead pointer for months — promised with a capability list, never built. Nothing errored.
Sweep for it: `dead-pointer-sweep.py` (cron weekly). Ground truth is the LOADER's exposed name set
(`skills_list()` returns frontmatter names), never the directory tree — comparing against directory
basenames produced two false dead pointers, and a diagnostic that cries wolf is worse than none.
Split `SKILL.md` citations (real: an agent will try to load it) from `references/` citations
(history — rewriting it to satisfy a linter is corruption). Fix on touch, not in bulk.

**When the instrument and the report disagree, the report loses; when the instrument is
mis-wired, fix the instrument and re-run.** Recorded defects in this instrument's own history, all
found by using it rather than reading it:

| defect | symptom | cause |
|---|---|---|
| wrong artifact path | `F1` understated, `G` 0.790 | cited a rollback map that was never written |
| self-corrections counted in the wrong files | `F7` 0.600 | looked in the artifacts, not the skill body |
| **stale class vocabulary** | **`G` 1.0000 (fake perfect)** | the sweep was rewritten `STALE` → `NOWHERE`/`DELETED`; the scorer still matched `STALE`, so it scored 0 unresolved |
| stale input data | `Energy2` measured before the fixes landed | artifact not regenerated after the repair pass |
| **vacuous truth** | **`G` 0.0000 on a clean layer** | `if op_total else 0.0` treated "nothing to fix" as "nothing produced" |
| substring self-match | a skill "citing itself" | `setup-help` matched inside its own `aaa-setup-help` id — needs word boundaries |

**A perfect score from a proxy instrument is a measurement failure, not a victory.** When every
dial reads 1.0000 the instrument has saturated and can no longer discriminate — say that out loud
rather than reporting 1.0 as governance health. Guard the vocabulary the same way the doctrine
guards floors: assert that the class names the scorer expects still exist in what the sweep emits,
and fail loudly on mismatch instead of silently scoring zero.

**The gates are proxies and must say so.** This layer's `F1`–`F13` are measured from named
artifacts (index resolution counts, commit counts, control counts), not from the kernel's floor
table. Per Axiom 6 (`computed, not asserted`) that makes them computed — but they are not the same
computation arifOS runs. Print the source per floor so the proxy is inspectable, and never present
it as the kernel's own verdict.

**G is not the goal — the breath is.** G measures the inhale (apex). The exhale is separate:
`CD < 0.05`, `DD < 2`, `IAR > 0.80`, `DCR > 0.90`. A layer can score SEAL on G and still be out of
breath — measured here: `G = 1.0000 SEAL` with `breath = 0.7639`. Optimising Energy alone is
permanent apex-mode (S13 scar accumulation); measuring without acting is permanent zen-mode
(Calhoun sink). Both are forbidden. Attack the bottleneck, then pair every enforcement with a
witness object and a held paradox.

**Symlinked mounts need a trust allowlist, or the security warning becomes noise.** The untrusted-
source guard resolves the skill path, so mounting a canonical catalog by symlink makes every load
warn. Measured: 53 of 406 live skills warned on every load. Allowlist the first-party roots but keep
the teeth — the lexical path must sit inside the profile skills dir AND the resolved target must be
in the allowlist. Prove it with a negative control (a symlink to `/tmp` must still warn); without
the control you have only tested that the warning can be silenced.
