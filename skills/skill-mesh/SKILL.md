---
name: skill-mesh
id: skill-mesh
version: 2.0.0
owner: AAA
risk_tier: medium
autonomy_tier: T1
organ_domain: aaa
floor_scope: [F1, F2, F3, F4, F7, F8, F9, F10, F11]
capability_tier: fed-long-context
ecology_state: WARM
description: "Use when a skill won't load, a capability vanished, skills diverge, or the library needs audit, merge, taxonomy or freeze. One FLOW lands you on the exact reference."
merged_cluster: skill-mesh (meta-skills governing the skill library itself)
merged_at: "2026-09-20"
merged_from:
  - aaa-skill-governor-runtime
  - skill-audit-methodology
  - skill-creator
  - skill-drift
  - skill-inventory
  - skill-library-integrity
  - skill-taxonomy-reclassification
  - skills-cold-storage-ops
triggers:
  - "skill validation"
  - "runtime governance"
  - "collision resolution"
  - "deprecation sweep"
  - "skill promotion review"
  - "audit skills"
  - "skill redundancy"
  - "skill quality"
  - "skill naming"
  - "zen skills"
  - "skill library health"
  - "federated skills"
  - "skill consolidation"
  - "archive skills"
  - "skill duplicates"
  - "engine variants"
  - "hermes variant"
  - "skill gap analysis"
  - "agent card skills missing"
  - "eureka zen"
  - "skill inventory"
  - "layer classification"
  - "substrate knowledge domain"
  - "map all skills"
  - "cross-repo skill comparison"
  - "HERMES vs AAA skills"
  - "cross-registry prefix mapping"
  - "AAA prefix taxonomy"
  - "aaa prefix mapping"
  - "map to AAA"
  - "prefix classification"
  - "zen hermes skills"
  - "collapse hermes skills"
  - "hermes skill deduplication"
  - "hermes-vs-aaa collapse"
  - "a skill won't load, a capability vanished silently, trees diverge, or one capability has accumulated several identities — one-writer/many-views consolidation, namespace collapse, with a live entropy sensor"
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
  - "a skill library needs taxonomy or a merge plan"
  - "a skill is missing"
  - "skill atlas"
  - "unified skill inventory"
  - "unified inventory"
  - "skill mesh sync"
  - "check skill mesh sync"
  - "skill mesh"
  - "find drift across surfaces"
  - "find drift"
  - "drift detector"
  - "skill won't load"
  - "skill fails to load"
  - "skill not found"
  - "ambiguous skill name"
  - "where did skill X go"
  - "duplicate skill"
  - "skill missing"
  - "thaw skill"
  - "freeze skill"
  - "prune skills"
  - "archive skill"
  - "dead pointer"
  - "ghost audit"
  - "living corpse"
  - "skill mesh health"
  - "skill merge"
  - "merge skills into one with flow"
  - "skill library integrity"
  - "skill portfolio audit"
  - "tombstone skill"
  - "namespace collapse"
  - "one writer many views"
  - "skill resolution"
  - "skill-creator"
  - "skill-linter"
  - "create-skill"
  - "skill-binding"
  - "skill-atlas"
  - "gap-detection"
  - "multi-harness"
# tags: union of every member's tags, preserved verbatim (member tag sets are the routing vocabulary
# of the 8 folded skills; generic one-word tags live here rather than in `triggers:` to avoid over-firing)
tags: [skill-creator, skill-linter, create-skill, bootstrap, lint, trigger, package, drift, audit, registry, manifest, binding, architecture, federation, skill-binding, federated, F2, F11, meta, skill-atlas, gap-detection, routing, inventory, multi-harness, mesh, sync, version, divergence, unification, alias, skills, hygiene, symlink, resolution, curation]
retired_names: [AUDIT-skill-atlas, AUDIT-agent-skill-mesh, AUDIT-drift-detector, skill-portfolio-audit]
---

# skill-mesh — one umbrella for every skill about skills

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
> **Motto for this lane:** *the library is an actuator, not documentation.* Many may read a
> capability; few may write it; someone must judge it.
>
> Eight meta-skills were folded into this one on 2026-09-20 (`merge-20260920`). Their bodies are
> preserved **byte-for-byte** under `references/` and their original directories are in
> `/root/AAA/skills/.archive/merge-20260920/skill-mesh/`. Nothing was summarised, nothing deleted.
> This file holds the **routing** and the **hard rules**; the references hold the **procedures** and
> the **full scar sets**.

**The failure mode this lane exists for (F13, 2026-09-19):** *the most common skill-store failure is
not a missing capability — it is the same capability accumulating multiple identities.* A library can
be byte-perfect and still incoherent, and a merge can remove all duplication and still destroy the
capability, because a capability that can no longer be **found** is gone.

```
Identity Inflation = Taxonomy Entropy        identities may scale, capabilities must not multiply
PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED   (every claim in this lane is a transition)
```

## FLOW

Walk this ladder top-down. **Branch on the observable in column 2, not on the topic word in the
request.** Step 0 is a gate, not a branch: if it fails, every later finding is unsound.

| # | Situation / observable (what you can actually see) | Open this reference | What it produces |
|---|---|---|---|
| **0** | **GATE.** `skill_view(name=X)` returns *not found* or *Ambiguous skill name*; `skill-view` resolves to a path you did not expect; a directory basename ≠ its frontmatter `name:`; a name resolves to two physical files | `references/skill-library-integrity.md` → §1 `scripts/skill_resolution_audit.py` | A **resolvable name** — a verified `{name → realpath → SKILL.md}` triple. Nothing else may proceed until this exists. *An unloadable skill cannot be audited.* |
| **1** | A body existed and now doesn't: link resolves to a directory with no `SKILL.md` (**phantom view**), a tombstone claims a move, a stub says `ALIAS →`, an `.archive*` is still offered by the loader | `references/skill-library-integrity.md` → §§4b, 6–8, `references/skill-library-integrity/quarantine-runbook.md`, `twin-collapse-runbook.md`, `namespace-collapse-runbook.md` | A classified defect (dead view link · phantom view · dead internal pointer · headless shell · living corpse · ghost) **plus the recovered body** and a reversal ledger |
| **2** | "How many skills are there?", "are the agents in sync?", "which skill should I load for X?", which surface owns a body | `references/skill-inventory.md` (§0–§4) · census `python3 /root/scripts/skills-census.py` | A count **with the command that produced it**, `SYNC/DIVERGED/MISSING_FROM_X` rows, and a routing target verified with `[ -d ]` |
| **3** | Two surfaces disagree (AAA vs harness vs profile vs organ), a registry/manifest/agent-card contradicts disk, a baseline is stale, an instrument reports `drift: 0` | `references/skill-drift.md` (§1, pitfalls 1–14) | A **dimension-by-dimension** drift report; `UNKNOWN` where both sides are `null` — never `degraded` |
| **4** | Content question: redundancy, quality score, description length, prefix/naming alignment, prune plan, "extract wisdom before deleting" | `references/skill-audit-methodology.md` (3-loop zen · prune checklist · `references/skill-audit-methodology/*`) | Ranked KEEP/MERGE/DOC/KILL classes, overlap scores, per-skill quality tier, and **usage evidence** before any kill |
| **5** | Shape question: uncategorised bucket, coordinate/taxonomy design, "merge these N into one", a `domains/<d>/<o>/<c>/<skill>` restructure | `references/skill-taxonomy-reclassification.md` + `scripts/skill-taxonomy-classifier.py`, `scripts/verify-skill-tree-integrity.py` | A **map artifact** (CSV one-row-per-skill + REPORT.md), the merge-mandate recipe, and a row-by-row reconcile against disk |
| **6** | The capability genuinely does not exist yet (and step 0 proves no owner is hiding it) | `references/skill-creator.md` §1–§3 — **but run `references/skill-library-integrity.md` LAW 1 first** | A staged `SKILL.md`, L1–L3 lint verdict, floor-tier SEAL gate, packaging |
| **7** | Loading-time governance: which gates a skill must pass before load, load order, token cost class (C0–C4), collision class (DUPLICATE/OVERLAP/CHAINED/ALIAS/ORTHOGONAL), weekly deprecation sweep | `references/aaa-skill-governor-runtime.md` | A gate verdict + collision class + `KEEP/MERGE/DEPRECATE/HOLD/VOID` disposition |
| **8** | A skill is missing from the live index and may be frozen; or you must freeze untouched skills | `references/skills-cold-storage-ops.md` | Thaw/freeze receipt — `mv` only, never `rm` |

**STOP CONDITION — a lane is closed only when both hold, from disk, not from a summary:**
1. the name resolves the way the **loader** resolves it (`skill_view(name=…)` returns content); and
2. the canonical census reports `broken_symlinks: 0` (`python3 /root/scripts/skills-census.py`).

A file count proves nothing. Write the receipt, then re-probe — a taxonomy is not done when the move
returns; it is done when a **second enumeration agrees**.

**ESCALATE, don't decide:** a merge of unknown-authoring skills, a live-vs-snapshot classification of
a whole tree, or promoting an organ's skills into the catalog changes *where the catalog is* — that is
F13-class. Produce the artifact, take the go/no-go, do not execute unattended.

## CORE RULES

Merged and de-duplicated from all eight members. Each rule survived at least two members; where two
members **disagree**, both positions are kept verbatim under CONTRADICTIONS below — never averaged.

1. **One writer, many views.** `/root/AAA/skills` is the canonical store; `/root/.hermes/skills`,
   `profiles/*/skills` and the organ trees are **views** (symlinks). Content, provenance and
   genealogy are written in exactly one place. Breaking this deletes capabilities silently.
2. **AAA is the catalog; harnesses are views. Do not invent a parallel catalog.**
3. **Diagnose before you treat.** Classify each hit as `BODY · ALIAS · PROJECTION · RENDERING ·
   RETIRED · ARCHIVED · CANONICAL · UNKNOWN` and count bodies by `realpath`/inode. A path is not a
   capability; alias names are transport; retired is not live.
4. **A merge must not lose discovery.** Carry **every** trigger phrase from every source and publish a
   `old name → new mode/section` mapping, or an agent that remembers the old name silently stops
   finding the capability. *This is the rule this very file is obeying.*
5. **Never delete — archive, quarantine, or symlink.** Path count is preserved so mutators resolve
   where they did before; body count becomes one.
6. **Negative proof before creating.** No new skill while an owner exists:
   `python3 /root/scripts/skill-owner-lookup.py "<capability in plain words>"` →
   `OWNER_EXISTS` = patch the owner · `NO_OWNER` = creation permitted · `WEAK_MATCH` = inspect the hits.
   Order of preference: owner exists → patch · similar exists → alias/example/pitfall · repeated
   workflow → patch the procedure · one-time fact → memory · governance rule → floor/base, not a
   skill · new API → tool contract · genuinely new domain → quarantined proposal.
   *A duplicate owner is worse than a missing one: both load, both sound right, and they drift where
   nobody is looking.*
7. **The catalog is a claim, not a measurement.** Every count must name the command that produced it.
   The **only** sanctioned census is `python3 /root/scripts/skills-census.py` (`--write` refreshes
   `disk_reconciliation`); hand-editing a registry's count or witness stamp is fabrication.
8. **Never collapse a whole mesh into one number.** `find` (raw) ≠ physical ≠ canonical ≠ loadable ≠
   whole-mesh. State the question with the number or it is noise.
9. **Walk flags are part of the answer.** `followlinks=True` / `find -L` answers *what can the agent
   load*; the non-following form answers *what bytes are on disk here*. Symlink-blind counting
   manufactures false absences; state which flag produced each figure.
10. **Identity is two fields.** `id:` is the namespace identity; `name:` is the **routing** identity
    (`frontmatter.get("name", <folder>)`) — the one the loader dedupes on. Key every check explicitly.
11. **The loader dedupes FIRST-WINS by routing name.** Two bodies sharing `name:` → exactly one is
    served, chosen by scan order, with no error anywhere. Which one is served **is the finding**.
12. **A sensor that cannot fail is decoration.** Every gate needs `{expected_event, owner, deadline}`
    and `timeout → SYNCHRONIZATION_FAULT`. A check reporting `0` on an empty input space is a broken
    path, not a healthy library — make "cannot witness" an explicit FAIL.
13. **Severity is a three-tier ladder:** `FAIL` = a capability is broken right now · `WARN` = carried
    debt that can be paid · `INFO` = measured, no gate attached (by-design properties live here, or a
    permanently-red gate stops being read).
14. **Two independent witnesses.** Executor ≠ verifier. A verification lane that inherits the
    executor's conclusions, or measures its success log, is echo reporting. Nothing is closed on
    `exit 0` through a pipe — that is `tail`'s status.
15. **Archive must be a wall, not a curtain.** A body inside a walked tree is still offered by the
    loader; discovery is a capability, and pruning the file is not pruning the capability.
16. **Move is a migration.** After any move/rename/archive: repoint dependents, sweep the views, sweep
    downstream inventory files that still *name* the dead path, re-run the census (`broken_symlinks: 0`).
17. **Re-probe after acting, not only before.** Re-verify the audit's own load-bearing numbers before
    executing on it, and correct the audit in place afterwards rather than appending a second report.
18. **Idempotent or it will half-run.** Frozen map/CSV first, skip anything already placed, archive
    stragglers instead of deleting; re-running the finisher must report `newly placed 0`.
    Diff `applied` against the dry-run plan — a mismatch is a failed run, not a partial success.
19. **Reversibility is part of the mutation.** Snapshot before the first bulk write, write an
    accumulating (never truncated) rollback manifest, and never cite a rollback artifact you have not
    `test -f`'d in the same breath.
20. **Name the plane before applying an anti-theatre rule.** "No performed persona, no filler" applies
    to *machine* lanes. Human-facing register, tone and warmth are a **requirement**; a "de-fluff"
    sweep that reaches a human-plane skill has destroyed the feature it was securing.

## CONTRADICTIONS — FLAGGED, BOTH POSITIONS KEPT

These members come from different doctrine generations and **disagree**. Both are preserved; the
choice is made per run and recorded. Do not average them, and do not silently pick one.

| # | Question | Position A (member) | Position B (member) | Why they differ / what decides |
|---|---|---|---|---|
| C-1 | May a skill be **created** freely? | `skill-creator` §1/§3: capture intent → draft → scaffold → SEAL gate. No owner lookup anywhere in the procedure. | `skill-library-integrity` LAW 1: **"No new skill may be created while an owner exists."** Run `skill-owner-lookup.py` first. | Different generations: creator predates the anti-redundancy gate. **Binding in this umbrella:** LAW 1 runs first; the creator's procedure runs only on `NO_OWNER`. |
| C-2 | Where does an archived skill go? | `skill-audit-methodology`: `mv` to `.archive-YYYY-MM-DD/` **inside the skills root**, with a `PRUNE_LEDGER_<date>.md`. | `skill-library-integrity` / `skill-inventory`: an `.archive-*` inside a scanned tree is `archive-void-rot` and makes `skill_view(name=…)` **ambiguous**; move it outside every scanned root. | Audit-methodology's pattern predates the index-hygiene finding. **Binding:** archive to `/root/AAA/skills/.archive/merge-<date>/<cluster>/` and then verify the loader no longer offers it. |
| C-3 | May a stub/body ever be deleted? | `skill-taxonomy-reclassification`: **"Delete nothing, ever — alias everything."** | `skill-library-integrity` §6: *"Never leave a dead pointer, and never leave a lying stub… Delete the stub; keep the directory when it holds real children."* | "Never delete" guards *authored content*; the integrity rule guards *lying markers* (a body saying "archived, do not use" rents index space and answers nothing). **Binding:** content is never deleted; only a stub whose content is proven to live in the successor may go, and it goes to the archive first. |
| C-4 | What is cold storage? | `skills-cold-storage-ops`: `/root/.hermes/skills-cold/`, `mv`, `/reload_skills`, ~179 live / ~328 cold. | `skill-library-integrity` / `taxonomy`: freeze to `<store>-retired/<date>-<reason>/` with a `{original_path, frozen_path, sha256-of-every-file}` ledger; `skills.external_dirs` still injects into the index and is **not** a zen lever. | Cold-storage's numbers are a dated witness (2026-08-24) and its root is a *harness* path, not the canonical store. **Binding:** freeze outside every walked tree, hash before the move, ledger the undo; verify with a fresh census, not with `/reload_skills` faith. |
| C-5 | Is `-maxdepth N` / a one-level scan admissible? | `skill-inventory` §2 shows a bounded `find` as the compare command. | Same member, next paragraph: *"`-maxdepth 2` is also wrong now — skill dirs nest up to 8 levels."* Plus `library-integrity`: an audit scoped one level deep reported an **11% compliance rate over 55% of the library**. | Kept as-is because the contradiction is *inside one member* and is the member's own correction. **Binding:** unbounded recursive walk; a published rate names its denominator's scope (`root — flat\|recursive; N dirs`). |
| C-6 | Which census figure is the library's size? | `skill-inventory` (2026-09-18): `629` raw find · `706` canonical / `634` physical · `801` whole-mesh. | `skill-library-integrity` (2026-09-18): *"canonical census of 587 on disk / 451 loadable"*; and 641 identities / 561 bodies = 1.14 in the store. | **Two members quote different figures for the same date**, which is exactly the rot both warn about. Neither is adopted here: run the census and quote its numbers with the command. Recorded as a live contradiction, `UNKNOWN` until re-measured. |
| C-7 | May a duplicate owner be collapsed without a human? | `skill-taxonomy-reclassification`: P1 (zero-loss dedupe) may run unattended; P2 (bulk merges) needs F13. | `skill-library-integrity`: `MIRROR_DRIFT` (flat leftover + authored owner) is a **mechanical re-sync**; `DUPLICATE_OWNER` (two authored paths, differing hashes) is a **HOLD for the human**. | Not a true conflict once classified: taxonomy's P1 = the integrity member's mirror case. **Binding:** classify by path shape first (`scripts/mirror_or_duplicate.py`), then apply taxonomy's P1/P2 gate. |

## PITFALLS

Union of the eight members' scars, grouped by what they cost. Each keeps its **command, path and
symptom** — this is the part a summariser would destroy. The full, unabridged scar set for each member
is in its reference body.

**Resolution and loadability**
- A skill that cannot load produces **no error** — the agent believes the procedure is available and
  re-derives it from priors, which is worse than a missing skill. This is why step 0 is a gate.
- **"Ambiguous skill name" is a filesystem fault, not a frontmatter fault.** Linting cannot see it.
  Two files claiming one loaded name break **both** names.
- A **phantom view** (link resolves, target dir holds no `SKILL.md`) passes both the broken-link test
  and the dead-pointer test. Measured: 24 instances, 82 view symlinks pointing into one container whose
  children held no body.
- The body may have been **deleted, not retired** — a bulk housekeeping commit removed 79 `SKILL.md`
  bodies and 15 were never restored. Match names **case-insensitively** (a case-sensitive matcher
  reported 41 gone; the true figure was 15) and exclude names that already carry a body elsewhere.
- A cited `scripts/` path is often **not missing** — resolve in three steps (package-relative → shared
  script root → elsewhere) before calling it dead. Measured: 151 raw misses, **103 genuine**.
- A `.bak` / `<shell>.bak-<ts>` written beside the file it backs up is counted by the next census and
  can register as a dead internal pointer. Backups belong **outside every scanned root**.
- A backup left inside the tree pollutes the instrument that measures it — write the inverse op to a
  manifest and move the backup out.

**Counting and instruments**
- `skill-view` / `skills_list` is an **advertised catalog, not existence**: it can name a skill that
  no longer resolves, and (reverse direction) a body under a nested path can be absent from both while
  sitting on disk. Resolve by path and say which of the two failures you found.
- `os.walk` / `find` **do not descend symlinked dirs**: after a tree becomes symlink views, the
  resolvable count appears to collapse and an intact tree reads as destroyed. Measured: 124 vs 409.
- Dedupe by `realpath` before mutating and before quoting a corpus size. Measured: 11 roots returned
  **1741** `SKILL.md` hits for **1050** unique physical files.
- A hand-rolled diff of `<store>/<category>/<name>` vs `<harness>/<category>/<name>` reports as
  unreachable every skill whose category path differs — resolution is by **name**, not path. Measured
  overcount: 192 vs a census of 587 on disk.
- A check that reads an index into a variable no branch uses, a declaration referenced only on its
  definition line, or two sides computed from the same expression differing only by `isfile` vs
  `exists`: none can ever fire. **A predicate with no reachable failing branch is not a check.**
- For a matcher/similarity detector, prove it fires on a pair you already know matches, *inside the
  same run*; a scan returning zero is indistinguishable from a broken scan. Measured: a sweep reported
  **0** overlaps while a 0.88 pair was present (pair key built from a different collection).
- A loose regex manufactures catastrophe: `"?verdict"?` matched the tail of `overall_verdict` and
  produced 29,886 hits; with a negative lookbehind (`(?<![A-Za-z0-9_])`) it was 856. Anchor the key
  boundary and sample one raw line before believing any detector count.
- Read the **input count** beside the verdict: `tombstones: 0` next to `count: 0` is a broken path.
- One census, many consumers — **never fork a second counter.** A registry carried `drift: 0` for weeks
  because a hand-era counter sat beside the real one.
- A report generator can carry a stale path for years and print a confident zero: `skill-sync.sh audit`
  grepped `FEDERATED_SKILLS_REGISTRY.yaml` (the file is `…_V3.yaml`) **and** read counts from `id:`
  lines the registry does not use. Two fixes, both required: resolve with a fallback, read the real
  field, and **print which file you read**.

**Merging, collapsing, retiring**
- **A tombstone is a claim, not a move.** Measured: 14 Wave-2 tombstones, **0 of 14** targets carried
  their source's content. Prove it per tombstone: recover the pre-merge body from the tag the tombstone
  names, then require its H2 headings to appear in the successor **package** (SKILL.md *or*
  `references/` — testing SKILL.md alone reports a correct merge as defective).
- **A collapse is not complete until both directions are verified.** A stub written while the body
  stayed put is a live duplicate: the loader serves exactly one, and *which* one is the finding.
- **TERTIB — recover, then remove.** An `.archive/<date>-<name>/<skill>` entry was a symlink whose
  target **was the live body it claimed to archive** (circular). Resolve every archive link with
  `realpath` and require it to land outside the live path.
- **Collapsing a container is not collapsing a pair — guard per ARTIFACT.** `os.path.exists(<child>)`
  passed on a thin placeholder while the body lived elsewhere; the container was replaced by a link and
  **six always-first, every-agent skills vanished**. Guard on `os.path.join(store_child,'SKILL.md')`.
- **Renaming a directory in the canonical tree silently deletes the capability in every harness.**
  Measured: 1,568 rename events, zero propagated, 7 skills dead with no error.
- `SUPERSET / NEWER / UNION / DESIGN FORK` — bucket diverged twins by comparing **sets of non-trivial
  lines**, never by version string or mtime. Only `DESIGN FORK` reaches a human.
- A claim of "both load" cannot distinguish which body is served and files the worse defect as the
  milder one. Replicate `get_scan_ordered_skills_dirs()` + first-wins.

**Symlinks and dependents**
- **Never evict on appearance.** 52 canonical dirs with no `SKILL.md` of their own were archived; 26
  were the live body behind view links and eviction broke **82 links**.
- **`find -L … -type l` is inverted** as a dependent test (it follows links, so a link to a directory
  is reported as a directory). Three live dirs were declared dependent-free; **100 view links broke**.
  Walk with `followlinks=False`, test `os.path.islink`, resolve with `realpath`.
- `find … -xtype l` finds broken links but **not one byte of it is a defect** until you check whether
  the link points at a pruned shell. Classify: link→pruned shell = delete; link whose body lives
  elsewhere = repoint.
- A relative symlink computed at the wrong depth yields a dangling link that still carries the right
  **name** — it reads as "repointed" in a listing and fails only when a loader touches it.
- Resolution must consult the **tombstone registry** or a repair undoes a recorded merge: measured,
  `forge-cross-agent-handoff` was tombstoned and the repair ladder re-pointed the canonical name back
  at the old body.

**Mutation discipline**
- Patch a JSON inventory as a **targeted text edit**, never a load/dump round-trip: a two-entry change
  produced a **5,477-line** diff. Assert `text.count(old) == 1` before replacing.
- `shutil.copy2` is **files-only** and raises `Is a directory` — a promotion pass reported
  `applied=1` against a plan of `4`, with the failures swallowed into a manifest nobody reads.
- **Stage and commit in the same breath**, scoped to the paths your own manifests produced — never
  `git add -A`, which sweeps other writers' in-flight work into a commit that claims to be yours.
  Verify the shape landed as symlinks: `git ls-tree -r HEAD <store> | grep ^120000`.
- A **newly created skill is untracked by default**: it loads, it resolves, and `git ls-files`
  returns nothing. "It exists and loads" is a different claim from "it is recorded".
- `EPERM` on write is not a permissions bug — check `lsattr`. `/root/AAA/governance` carries the
  **immutable** attribute by design; clearing it inverts the authority order. Report locked debt.
- **A new skill's address is not minted by the write path.** Creating writes the package into the
  store and stops; a skill can be complete, resolvable by path, and still return *not found* to
  `skill_view`. Resolve the way the **loader** does, immediately after creating it — not at the end of
  the session.
- Hold a repair when a second session is writing the same tree. "Authorized but racy" and "not
  authorized" are different verdicts; check `ps -eo pid,etimes,cmd` and WAL mtime before acting.
- Two pre-tool-gate refusals look like broken commands: a **PATH** hold (the directory word itself —
  `court/`, `audit/`, `well/`) and a **CONTENT-pattern** hold (money/health/legal/trading vocabulary).
  Read the reason, fix the payload (attach a real URL or an existing evidence file), never reword to
  slip past a gate and never retry the identical payload — the check is deterministic.
  An **OWNERSHIP** refusal (`created_by=None`) is the third class and the only correct move is
  `hermes curator adopt <name>`.

**Governance and cost**
- A gate that fires into a log nobody reads has not failed — the **closure** has. `skill-entropy-gate`
  reported the same 4 defects four times a day for days.
- **A registry that reports `drift: 0` from a stale method is worse than no registry.** Never re-stamp
  a witness with a method you did not run — that is fabrication, not witness.
- Blanket `--apply` propagation of 248 missing/drift entries is a **profile-scoping decision**, not a
  sync job: it changes the live loader surface and the per-turn context cost.
- Description text is budgeted for the always-loaded index: over ~110 KB total, the harness truncates
  **silently** and agents keep the names but lose the WHEN. Keep descriptions ~120–200 chars on a large
  library, trigger first.
- A `SKILL.md` over ~100,000 chars **cannot be patched at all** (the whole batch rolls back) while
  still loading fine — a dead skill with no symptom. Sweep with
  `find <skills_root> -name SKILL.md -size +90k`; move the largest section verbatim into `references/`
  behind a `grep -n -i` recipe, never behind a re-listing.
- Glued `---#` frontmatter (closing `---` fused to the first heading) parses as YAML and breaks any
  agent that reads frontmatter — invisible to humans, `yaml.safe_load()` sees it.
- A single skill's directory casing is owned by the updater when it is in `.bundled_manifest` — never
  normalise it, and exclude bundled names from case-drift detection (53 false positives in one run).
- **Never merge a cluster of unknown-authoring skills unattended**, and never resolve the
  *job duplicate* class (N independent write-ups of one procedure — measured: 7 skills, 49,941 bytes,
  pairwise similarity 0.02–0.07) by merging bodies: merging N texts of one job produces text N+1.
  Collapse to one canonical owner and **alias** the rest.

## RETIRED-NAME LANDING (discovery preserved)

Trigger phrases carried forward when earlier identities were retired. These names now route **here**;
nothing is re-forged under them.

| Retired name | Retired trigger phrases (verbatim) | Live home |
|---|---|---|
| `AUDIT-skill-atlas` | "skill atlas", "unified skill inventory", "unified inventory" | `references/skill-inventory.md` §0–§4 |
| `AUDIT-agent-skill-mesh` | "skill mesh sync", "check skill mesh sync", "skill mesh" | `references/skill-inventory.md` §2 MESH SYNC |
| `AUDIT-drift-detector` | "find drift across surfaces", "find drift", "drift detector" | `references/skill-drift.md` §1 |
| `skill-portfolio-audit` | (parent identity of the three above; frozen body at `/root/AAA/skills-retired/2026-09-19-v2-portfolio-audit/`) | this FLOW |
| `skill-inventory` (dir `core/governance/skill-portfolio-audit`, a harness alias) | — | `references/skill-inventory.md` |

## REFERENCES

| Reference | Source skill | Original path | Notes |
|---|---|---|---|
| `references/aaa-skill-governor-runtime.md` | `aaa-skill-governor-runtime` | `/root/AAA/skills/aaa-skill-governor-runtime/SKILL.md` | 6 pre-load gates, load order, C0–C4, collision classes |
| `references/skill-audit-methodology.md` | `skill-audit-methodology` | `/root/AAA/skills/domains/general/aaa/skill-mesh/skill-audit-methodology/SKILL.md` | + its 18 support files at `references/skill-audit-methodology/` (**path shift**: the body says `references/<file>.md`; read `references/skill-audit-methodology/<file>.md`) |
| `references/skill-creator.md` | `skill-creator` | `/root/AAA/skills/engineering/skill-creator/SKILL.md` | create / lint / scaffold. **Its own dir `skill-creator/` is separate from the harness-owned `/root/AAA/skills/.system/skill-creator/` — the `.system` one was NOT merged and is out of this cluster.** |
| `references/skill-drift.md` | `skill-drift` | `/root/AAA/skills/engineering/skill-drift/SKILL.md` | 7 drift dimensions, baselines, binding, 14 pitfalls |
| `references/skill-inventory.md` | `skill-inventory` | `/root/AAA/skills/engineering/skill-inventory/SKILL.md` | 16 surfaces, mesh sync, rot classes, routing table, pre-seal checklist |
| `references/skill-library-integrity.md` | `skill-library-integrity` | `/root/AAA/skills/skill-library-integrity/SKILL.md` | LAW 0–3, resolution, ghosts/corpses, namespace collapse + 18 support files at `references/skill-library-integrity/` |
| `references/skill-taxonomy-reclassification.md` | `skill-taxonomy-reclassification` | `/root/AAA/skills/domains/general/aaa/skill-mesh/skill-taxonomy-reclassification/SKILL.md` | taxonomy, merge mandate, classifier + verifier; support file at `references/skill-taxonomy-reclassification/` |
| `references/skills-cold-storage-ops.md` | `skills-cold-storage-ops` | `/root/AAA/skills/domains/general/aaa/skill-mesh/skills-cold-storage-ops/SKILL.md` | thaw / freeze |

**Executable scripts merged into `scripts/` (they are run, not decorative):**

| Script | From | Use |
|---|---|---|
| `scripts/skill-taxonomy-classifier.py` | `skill-taxonomy-reclassification` | uncategorised bucket, nearest-centroid category, near-duplicate clusters, 4-state drift map (CSV+JSON+MD) |
| `scripts/verify-skill-tree-integrity.py` | `skill-taxonomy-reclassification` | run **after** any bulk move: content multiset, row-by-row reconcile, strays. Non-zero exit on failure |
| `scripts/skill_resolution_audit.py` | `skill-library-integrity` | names mapping to >1 file; basename ≠ frontmatter `name:`. Exit 1 = something is unloadable |
| `scripts/dependents.py` | `skill-library-integrity` | inbound-link resolver — run **before** any move/archive/removal |
| `scripts/mirror_or_duplicate.py` | `skill-library-integrity` | `MIRROR_DRIFT` vs `DUPLICATE_OWNER` per colliding name |
| `scripts/corpse_audit.py` · `scripts/collision_audit.py` · `scripts/discovery_guard.py` · `scripts/store_census.py` · `scripts/store-resolution-probe.py` | `skill-library-integrity` | living-corpse sweep · collision audit · post-merge discovery guard · store census · store resolution probe |

**The one census (no hand-written counts):** `python3 /root/scripts/skills-census.py` ·
mesh gate `bash /root/AAA/skills/scripts/skill-mesh-sync.sh --check` ·
entropy gate `python3 /root/scripts/skill-entropy-gate.py` (`/var/log/arifos/skill-entropy.log`).

## Related (not merged here)

| Skill | Relationship |
|---|---|
| `/root/AAA/skills/.system/skill-creator` | Harness-owned (`source: builtin`), re-seeded by `hermes update`. **Deliberately excluded** from this merge. |
| `skill-installer`, `AGI-skill-unification` | Separate clusters owned by other merge lanes. |
| `capabilities/agent-capability-self-audit` | Sits in the same harness container; **not** a member of this cluster. |
| `FORGE-symlink-audit` | Federation-wide broken-link sweep — its blanket `-delete` recipe is **not** safe inside a git-tracked skills tree. |
