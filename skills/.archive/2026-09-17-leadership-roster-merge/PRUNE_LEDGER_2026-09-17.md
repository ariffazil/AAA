# PRUNE LEDGER — 2026-09-17 — leadership roster duplicate merge

## What was wrong

A background curator created TWO skills from one session (`20260917_232816_c137d83b`),
four minutes apart, describing the same class of work:

| Skill | Created (UTC) | SKILL.md | Assets | use_count |
|---|---|---|---|---|
| `institutional-leadership-lineage` | 2026-09-17T15:33:26Z | 6,149 B | 1 reference | 0 |
| `leadership-roster-archive` | 2026-09-17T15:37:15Z | 7,669 B | 1 reference + 1 template | 0 |

Trigger text overlapped verbatim — both carried "what did they bring, what did they get".
Two skills sharing one trigger class makes `skill_view` selection a coin flip.

Both also landed in a NEW flat category dir `/root/AAA/skills/research-core/` instead of the
canonical nested tree `/root/AAA/skills/domains/general/workshop/research-core/` where the
siblings they cite (`person-intelligence-dossier`, `executive-intelligence-briefing`) live.
Neither was referenced by `FEDERATED_SKILLS_REGISTRY_V3.yaml`, `SKILL_ALIAS_TABLE.json`,
`GENEALOGY.json`, or any agent card — both were orphans.

## Action taken

1. Merged both bodies + all triggers into ONE skill at the canonical location:
   `/root/AAA/skills/domains/general/workshop/research-core/institutional-leadership-lineage/`
   (SKILL.md 13,541 B, version 2.0.0, union of both trigger lists).
2. Carried across both support assets:
   - `references/office-holder-roster.md` (from `leadership-roster-archive`)
   - `references/petronas-leadership-lineage.md` (from `institutional-leadership-lineage`)
   - `templates/roster_pdf_builder.py` (from `leadership-roster-archive`)
3. Archived the whole flat source dir (move, not delete — F1 reversible-first):
   `/root/AAA/skills/research-core/` → `.../2026-09-17-leadership-roster-merge/research-core/`

`research-core` as a top-level category no longer exists; the nested canonical one is unchanged.

## Revert (move-based, no deletion)

```bash
mv /root/AAA/skills/domains/general/workshop/research-core/institutional-leadership-lineage \
   /tmp/merged-lineage-20260917
mv /root/AAA/skills/.archive/2026-09-17-leadership-roster-merge/research-core \
   /root/AAA/skills/research-core
```

Nothing else was touched. Registry is machine-derived (skills-census.py, 4x/day) — do not hand-edit;
the census will pick up the merged skill on its next pass.
