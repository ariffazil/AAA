---
name: capability-addressing
description: "Use when skill triggers collide or a selector is needed."
version: 1.0.0
triggers:
  - "skill collision"
  - "trigger collision"
  - "identity collision"
  - "skill selection layer"
  - "which skill should fire"
  - "capability routing"
  - "too many skills"
  - "collision census"
  - "the model picks the wrong skill"
floors: [F2, F4, F7]
---

# Capability Addressing

Collision census (identity vs trigger), owner proof before any router, and the
filter-ladder selection contract.

Capability *abundance* becomes capability *routing entropy*: as the count rises, more
descriptions claim the same request, and the chooser degrades into a model's eye over a
flat description list. The fix is never "another router agent" — it is a measured collision
profile plus a selection CONTRACT.

## Rule 1 — Measure, never quote

A collision percentage that came from a model's own reading of the index is a self-report,
not a measurement. Census it:

→ `scripts/skill-collision-census.py` — re-runnable, deterministic, declared metadata only
(no embeddings, no LLM). Reports file total, distinct names, identity collisions, case-twins,
and trigger-collision count + percent.

```bash
python3 scripts/skill-collision-census.py --out /tmp/census.json
python3 scripts/skill-collision-census.py --root canonical=/path/a --root overlay=/path/b
```

**Dereference to discover, then collapse by realpath before counting bodies.**
Follow symlinks (`os.walk(followlinks=True)`) so a view-tree is not reported empty.
Then count **unique `realpath(SKILL.md)` as BODIES**. Visit count minus unique reals
= ALIAS / PROJECTION names, not extra capabilities.

**NEW — 2026-09-20 (610 → 68 → 0 bodies):** a census that follows links and then
treats every path as a body reports aliases as duplicates. That is false work.
Classification precedes diagnosis: BODY · ALIAS · PROJECTION · RETIRED · CANONICAL.
Do not emit a "collapse N duplicates" task until N is unique inodes, not path visits.

## Rule 2 — De-metadata before extracting triggers

Descriptions in a federated estate often begin with routing metadata, e.g.
`> [fed: tier=… floors=[F1, F2, …]]`. Tokenizing that prefix as trigger text makes EVERY
tagged skill "share" the tokens `fed` / `tier` / `floors` and manufactures a huge phantom
cluster (95 skills in the case that produced this rule). Strip leading bracket metadata first.

Same failure class as the symlink rule above: the probe was reading a **label** and
reporting it as **content**. The first number a census produces is the one to distrust —
including the number this skill's own v1 produced.

## Rule 3 — Two defects, two fixes, never merged

| Defect | Definition | Fix |
|---|---|---|
| **Identity collision** | one concept, ≥2 distinct realpaths | canonicalize / supersede / alias |
| **Trigger collision** | different capabilities claiming one request phrase | disambiguate ownership conditions |

Split the identity count into two reported numbers: a **mirror twin** (one tree reached
through two roots — e.g. a profile dir and a canonical dir) is registry bookkeeping; a
**genuine** duplicate (a compiled copy shadowing canonical, a nested dir-in-dir ghost, or a
`brand-name`/`name` pair inside one tree) is the defect. Quote them separately.

Never merge or archive a trigger collision — those are legitimate neighbours whose trigger
clause is under-specified. Add the discriminating clause to each description instead.

**Special case — the brand × variant matrix.** `<brand>-meta-mesa` / `<brand>-zen-router` /
`<brand>-agentic-state`: if the disk already has `canonical: true` + `supersedes:` +
symlinks (meta-mesa merged 2026-09-19), do **not** re-merge. Remaining fragment is
**consumer memory** storing alias names as separate `skills_used` — fix the observer,
not the tree. HOLD on prune.

Reporting these classes as one "overlap %" makes both undecidable and invites the wrong fix.

## Rule 4 — Owner proof before minting a selector

"There is no selection layer" is a CLAIM and it requires reading the candidate owners first.
Typical partition in a governed estate:

- a capability **loader** owns service/backend capabilities (endpoints, authority mode, rank)
- an **identity resolver** owns identity-bound capabilities (voice / image / biometric handles)
- an **inventory census** owns counts and staleness only

None of those owns skill selection. Record that proof in the same artifact as the finding —
it is a read, not an impression. Only then build, and build a contract, not an agent.

## The selection contract (deterministic first, model last)

```
intent
  → consequence class + authority tier      (existing envelope machinery)
  → domain filter         (derived from path band)           N → ~N_domain
  → authority filter      (derived from declared risk tier)   → ~N_authority
  → health / host filter  (live service state)                → ~N_live
  → intent candidates     (trigger index, collision-aware)    → 2–5
  → model resolves the last mile                              → 1
```

Metadata must be **derived** by the census (brand prefix, path band, declared risk tier),
never hand-written across hundreds of files. Collapse identity collisions FIRST, or the
trigger index simply inherits the duplicates.

Do not start with embeddings or an LLM classifier. Cheap deterministic information resolves
almost everything; the model should resolve the last mile, not the entire routing universe.

## Kill criterion

If the derived index cannot narrow a real intent query from the whole library down to ≤5
candidates, it is decoration. Measure that before claiming it works, and say so plainly when
it fails.

## Pitfalls

- **A census that reports one combined number has not done the work.** The split IS the finding.
- **Do not re-mint a per-harness copy of a capability that already has an owner.** Patch the
owner — a branded duplicate per harness re-creates the very identity collision being fixed.
- **A nested `<name>/<name>/SKILL.md` is a ghost, not a scoped variant.** Flag it; do not count
it as a second skill.
- **Census output carries a timestamp.** Re-run rather than quoting a stale count, and never
carry yesterday's collision figure into today's decision.

*DITEMPA BUKAN DIBERI*
