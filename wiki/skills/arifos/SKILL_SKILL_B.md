---
title: "Skill: Skill Creator"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
category: arifos
tags: [skill-creation, meta-skill, evals, benchmark, optimization, tree777, promotion]
confidence: high
contested: false
floors: [F7, F8, F13]
risk_band: MEDIUM
sources: [/root/.agents/skills/skill-creator/SKILL.md]
---

# Skill: Skill Creator (Meta-Skill)

> **Source:** `/root/.agents/skills/skill-creator/SKILL.md`
> **Agent:** All federation agents
> **Forged:** 2026-05-17

---

## Trigger Conditions

Load this skill when the task involves:
- Creating a new skill from scratch
- Editing or optimizing an existing skill
- Running evals to test a skill's performance
- Benchmarking skill performance with variance analysis
- Optimizing a skill's description for better triggering accuracy
- Promoting a skill to canonical status in TREE777

---

## Doctrine

A skill is **not** a script. A skill is **doctrine** — a governed pattern that an agent internalizes and applies with judgment.

### Skill Anatomy

Every canonical skill in TREE777 must have:

```yaml
---
title: "Skill: Name"
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: X.Y.Z
type: skill
category: [arifos|federation|infrastructure|geox|wealth|well]
tags: [tag1, tag2]
confidence: [low|medium|high]
contested: [true|false]
floors: [F1, F2, ...]
risk_band: [LOW|MEDIUM|HIGH]
sources: [file paths]
---
```

And body sections:
1. **Trigger Conditions** — When should an agent load this skill?
2. **Doctrine** — What principles govern this skill?
3. **Workflow** — Step-by-step execution pattern
4. **Anti-Patterns** — What should NOT be done?
5. **Related** — Cross-links to other TREE777 pages

---

## Workflow: Create New Skill

```
1. IDENTIFY — What capability gap exists? Why is a skill needed?
2. DRAFT — Write SKILL.md with all required sections
3. TEST — Run 3-5 test prompts through an agent WITH the skill loaded
4. EVAL — Measure: triggering accuracy, output quality, side effects
5. REFINE — Iterate based on eval results
6. REGISTER — Add to tree-manifest.json with proper metadata
7. PROMOTE — Submit to 888_JUDGE for canonical status (if steel law)
```

---

## Promotion Ladder

| Status | Meaning | Authority |
|--------|---------|-----------|
| `draft` | Agent-created, unverified | Any agent |
| `candidate` | Evaluated, evidence attached | Any agent |
| `canonical` | Ratified, referenced by workflows | 888_JUDGE or sovereign |
| `steel_law` | Mandatory, non-negotiable | Sovereign only |

---

## Related

- [[skill-skill-promote]] — Promotion via 888 deliberation
- [[skill-skill-reflector]] — Skill quality auditing
- [[SCHEMA.md]] — TREE777 schema governing page types
- [[tree-manifest.json]] — Skill registry

---

*DITEMPA BUKAN DIBERI — A skill is doctrine, not a script.*
