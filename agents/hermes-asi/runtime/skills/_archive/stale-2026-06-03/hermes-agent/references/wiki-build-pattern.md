# Federation Wiki Build Pattern — arifOS AAA Wiki

> Reference implementation for building a federation knowledge base using the Karpathy LLM Wiki pattern.
> Built: 2026-05-17 after Hermes fabrication incident exposed need for persistent cross-agent learning.

---

## What Triggered This

Hermes fabricated artifact existence claims (`load_spatial.sh`, `FORGE_SEAL_2026-05-17.md`, `spatial_context_queries` table) — none existed. Arif caught this via validation request. The federation needed a persistent learning surface so future agents don't repeat this.

---

## Build Sequence (10 Steps)

```
Step 1: Create directory structure
Step 2: Write SCHEMA.md (conventions, F1 rules, tag taxonomy)
Step 3: Write index.md (catalog template)
Step 4: Write log.md (initialization entry)
Step 5: File first scar (most important artifact)
Step 6: Create entity pages (federation nodes)
Step 7: Create concept pages (governance patterns)
Step 8: Create skill pages (reusable capabilities)
Step 9: Migrate raw sources from legacy locations
Step 10: Link to SKILLS_INDEX.md
```

---

## Step 1: Directory Structure

```bash
mkdir -p wiki/{raw/{papers,repos,notes},entities,concepts,skills,comparisons,queries,_archive}
```

### Full structure
```
wiki/
├── SCHEMA.md              ← conventions, page types, frontmatter, tag taxonomy, F1 rules
├── index.md               ← catalog of all pages
├── log.md                 ← chronological append-only action record
├── scar-<incident>.md     ← incident records (most important)
├── entities/              ← federation nodes, agents, services
├── concepts/              ← governance patterns, anti-patterns
├── skills/                ← reusable capability documents (class-level)
├── comparisons/           ← side-by-side analyses
├── queries/               ← filed Q&A worth preserving
├── raw/papers/            ← immutable academic papers, technical references
├── raw/repos/             ← source code configs, git diffs, architecture docs
├── raw/notes/             ← meeting notes, Telegram captures, raw observations
└── _archive/              ← superseded pages
```

---

## Step 2: SCHEMA.md — What to Include

**Core sections:**
1. Domain declaration — what the wiki covers, who the audience is
2. Architecture (3 layers): raw/ (immutable) → entities/concepts/skills/ (agent-owned) → SCHEMA.md (governs)
3. Conventions: file naming, frontmatter (required), wikilinks (min 2 per page), provenance markers
4. Tag taxonomy: federation nodes, agent types, concepts, patterns, meta, operations
5. Page thresholds: when to create vs skip creating pages
6. Update policy: handling contradictions, dating, contested flags
7. Agent workflow (recursive learning loop): AFTER/BEFORE rules
8. F1 rule set: federation-wide operational rules
9. Scars: what makes a good scar page
10. Lint schedule: weekly/monthly/quarterly
11. Privacy boundaries: public (wiki/) vs private (vault/)

---

## Step 3-4: index.md + log.md Templates

### index.md
```markdown
---
title: AAA Wiki Index
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: index
tags: [federation, wiki, index]
confidence: high
---

# AAA Wiki — Federation Knowledge Base Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Last updated: YYYY-MM-DD | Total pages: N

---

## Scar (Failure / Incident Record)

| Page | Summary |
|------|---------|
| [[scar-xxx-YYYY-MM-DD]] | What happened |

---

## Entities (Federation Nodes & Agents)
...

## Concepts (Governance, Patterns, Anti-Patterns)
...

## Skills (Reusable Capability Documents)
...

## Comparisons
...

## Queries
...

## Raw Sources (Immutable)
### Repos
### Notes
### Papers
```

### log.md
```markdown
---
title: AAA Wiki Log
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: log
tags: [federation, wiki, log]
confidence: high
---

# AAA Wiki — Chronological Action Log

> Append-only record. Format: ## [YYYY-MM-DD] action | subject
> Actions: init, ingest, update, create, archive, delete, lint, query
> When this file exceeds 500 entries, rotate: log-YYYY.md, start fresh.

## [YYYY-MM-DD] init | Wiki initialized — domain description
- Who: agent name
- Domain: what the wiki covers
- Structure created: directories
- Authority: sovereign name
- Motivation: why this wiki exists

## [YYYY-MM-DD] create | Scar filed: incident name
- Page: [[page-name]]
- Event: what happened
- Root cause: why
- Countermeasure: what was fixed
```

---

## Step 5: Scar Page — Minimum Requirements

Every scar must include:
1. **What happened** — factual, no spin, evidence-backed
2. **Evidence** — logs, config, timestamps proving it occurred
3. **Root cause** — why it happened (not just what went wrong)
4. **Lesson** — what every future agent must do differently
5. **Countermeasure** — specific procedural or architectural fix applied
6. **Verification commands** — commands future agents can run to confirm fix

**Scar page frontmatter:**
```yaml
---
title: "INCIDENT NAME — YYYY-MM-DD"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: scar
tags: [incident, root-cause, lesson, federation]
sources: [raw/notes/evidence-file.md]
confidence: high
contested: false
---
```

---

## Step 6-8: Entity/Concept/Skill Pages

### Entity page structure
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references
- VPS context if applicable

### Concept page structure
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])
- Anti-patterns if applicable

### Skill page structure
- Skill ID and when to use (trigger conditions)
- Problem statement
- Solution with exact commands/steps
- Verification commands
- Related pages
- Pitfalls

---

## Step 9: Raw Source Migration

```bash
# From legacy flat wiki to structured wiki
cp /root/wiki/*.md /root/AAA/wiki/raw/repos/
cp /root/wiki/research/*.md /root/AAA/wiki/raw/notes/
cp /root/wiki/dossiers/*.md /root/AAA/wiki/raw/notes/
cp -r /root/wiki/VPS_ARCHITECTURE/* /root/AAA/wiki/raw/repos/
```

**Rule:** Raw is immutable. Do not modify after copying. Corrections go in synthesized pages.

---

## Step 10: Link to SKILLS_INDEX.md

In `/root/AAA/SKILLS_INDEX.md`, add:

```markdown
## Wiki: Federation Knowledge Base

**Location:** `/root/AAA/wiki/`

The AAA wiki is the public compounding layer for the arifOS federation...

### Recursive Learning Loop
[the loop rules]

### F1 Rule Set (Federation-Wide)
[the 6 rules]

### First Scar Filed
`scar-hermes-fabrication-2026-05-17` — Hermes fabricated artifact existence...

**See also:** `wiki/SCHEMA.md` for full wiki governance
```

---

## F1 Rule Set (Encode in SCHEMA.md)

```
1. Read wiki/index.md before non-trivial work
2. Write one reusable artifact per novel fix
3. File scar page + log entry on any failure/fabrication
4. Attach evidence to raw/ before synthesizing
5. Query index + skill pages before starting new work
6. Redact secrets/credentials before publishing scars
```

---

## Recursive Learning Loop

```
AFTER novel fix           → write one reusable artifact (skill or concept page)
AFTER failure/fabrication → file scar page + append log.md
AFTER repo/tool change    → attach evidence to raw/ + link from synthesized page
BEFORE non-trivial work   → query wiki/index.md + relevant skill pages first
```

This IS the recursive learning mechanism. Not optional.

---

## Results

**Wiki built:** `/root/AAA/wiki/` (2026-05-17)
- 10 pages created (SCHEMA, index, log, scar, entities, concepts, skills)
- 16 source files migrated from `/root/wiki/`
- SKILLS_INDEX.md updated with wiki section
- VAULT999 sealed: `AAA-WIKI-BUILD-2026-05-17`

---

*See also: `fabrication-prevention` skill for the anti-fabrication protocol.*
*DITEMPA BUKAN DIBERI — Future agents have better priors.*