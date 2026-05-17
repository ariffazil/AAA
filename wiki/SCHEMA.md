---
title: AAA Wiki Schema
created: 2026-05-17
updated: 2026-05-17
type: schema
tags: [federation, wiki, governance, learning]
sources: []
confidence: high
---

# AAA Wiki — Federation Knowledge Base Schema

> **Authority:** Muhammad Arif bin Fazil — Sovereign
> **Purpose:** Public compounding layer for arifOS federation agents
> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.

---

## Domain

This wiki covers the arifOS Constitutional Federation — its agents, services, governance rules, operational learnings, scars, and skill compilations. The audience is both human operators and AI agents working on VPS 72.62.71.199.

---

## Architecture: Three Layers

```
wiki/
├── SCHEMA.md           ← This file — conventions, structure, tag taxonomy
├── index.md            ← Sectioned catalog of all pages with one-line summaries
├── log.md              ← Chronological append-only action record
├── raw/                ← Layer 1: Immutable source material
│   ├── papers/         │   Academic papers, technical references
│   ├── repos/          │   Source code configs, git diffs, architecture docs
│   └── notes/          │   Meeting notes, Telegram captures, raw observations
├── entities/           ← Layer 2: Federation nodes, agents, services
├── concepts/           ← Layer 2: Governance concepts, patterns, anti-patterns
├── skills/             ← Layer 2: Reusable capability documents
├── workflows/          ← Layer 2: Multi-step orchestrations (see §Workflows)
├── comparisons/         ← Layer 2: Side-by-side analyses
└── queries/            ← Layer 2: Filed Q&A worth preserving
```

**Layer 1 — Raw Sources:** Immutable. Agents read but never modify. Source of truth.
**Layer 2 — Wiki:** Agent-owned markdown. Created, updated, cross-referenced by agents.
**Layer 3 — Schema:** This file. Governs all agent behavior in the wiki.

---

## Conventions

### File naming
- lowercase, hyphens, no spaces: `hermes-fabrication-incident.md`
- Entity pages: `geox.md`, `arifos.md`, `hermes-agent.md`
- Skill pages: `skill-spatial-grounding.md`, `skill-arif-workflow.md`
- Scar pages: `scar-hermes-fabrication-2026-05-17.md`
- Concept pages: `grounding-evidence.md`, `anti-fabrication-protocol.md`

### Frontmatter (required on all Layer 2 pages)
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: X.Y.Z         # Semantic version — increment on meaningful change
type: entity | concept | skill | comparison | query | scar | schema | log
tags: [from taxonomy below]
sources: [raw/notes/filename.md, raw/repos/config.md]
confidence: high | medium | low
contested: true | false
contradictions: [other-page-slug]
---
```

### Wikilinks (mandatory cross-referencing)
- Every page must link to at least 2 other pages via `[[pagename]]`
- Orphan pages (no inbound links) are flagged in lint
- Link format: `[[hermes-agent]]`, `[[skill-spatial-grounding]]`

### Provenance markers
- On pages synthesizing 3+ sources: append `^[raw/repos/config-name.md]` to paragraphs
- Single-source pages: `sources:` frontmatter is sufficient

### Confidence levels
- `high`: well-supported across multiple sources or long operational track record
- `medium`: plausible, single source, or under active observation
- `low`: speculative, contested, or early-stage learning

### Contested pages
- Set `contested: true` in frontmatter when there are unresolved contradictions
- List conflicting pages in `contradictions: [slug, slug]`

---

## Tag Taxonomy

**Federation nodes:** arifOS, A-FORGE, GEOX, WEALTH, WELL, Hermes, AAA, APEX, HERMES
**Agent types:** openclaw, gemini, kimi, claude, opencode, copilot, codex
**Concepts:** grounding, evidence, fabrication, spatial-awareness, governance, constitutional
**Patterns:** scar, skill, workflow, anti-pattern, incident, discovery
**Meta:** comparison, timeline, architecture, configuration
**Operations:** mcp, a2a, docker, deployment, security, audit

---

## Page Thresholds

| Action | Threshold |
|--------|-----------|
| Create entity page | Appears in 2+ sources OR is a federation node |
| Create concept page | Central to governance, architecture, or operational pattern |
| Create skill page | Reusable capability that 2+ agents benefit from |
| Create scar page | Any failure, fabrication, or repeated mistake |
| Create comparison | Side-by-side analysis useful for architectural decisions |
| Create query page | Answer painful to re-derive, worth preserving |

**DON'T create pages for:** passing mentions, minor details, transient state

---

## Update Policy

When new information conflicts with existing content:
1. Check dates — newer sources generally supersede older
2. If genuinely contradictory: note both with dates and sources
3. Mark `contested: true`, list in `contradictions:`
4. Flag for human review in weekly lint

---

## Agent Workflow (Recursive Learning Loop)

```
AFTER any novel fix → write back one reusable artifact (skill or concept page)
AFTER any failure/fabrication → file a scar page + append log.md
AFTER any repo/tool change → attach evidence to raw/ + link from synthesized page
BEFORE any non-trivial work → query wiki/index.md + relevant skill pages first
```

This loop IS the recursive learning mechanism. Not optional.

---

## F1 Rule Set (Federation-Wide)

1. **Read before act:** `wiki/index.md` before non-trivial work
2. **Write on novel fix:** one reusable artifact per new discovery
3. **File on failure:** scar page + log entry on any failed claim or fabrication
4. **Source capture:** attach evidence to `raw/` before synthesizing
5. **Query first:** index + skill pages before starting new work
6. **Redact before publish:** remove secrets, credentials, internal topology from scars

---

## Scars (Incident Record)

Scars are the most important learning artifacts. A scar page must include:
- **What happened** — factual description, no spin
- **Evidence** — logs, config, timestamps proving it occurred
- **Root cause** — why it happened (not just what went wrong)
- **Lesson** — what every future agent must do differently
- **Countermeasure** — specific procedural or architectural fix applied

---

## Workflows (Multi-Step Orchestrations)

A workflow is a **composed sequence of skills** executed over time, with governance checkpoints.

### When to create a workflow page
- Multi-step process involving 3+ skills
- Human-in-the-loop checkpoints required
- Cross-agent coordination
- Temporal sequencing (schedule, cron, event-driven)

### Workflow page frontmatter
```yaml
---
title: Workflow Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: X.Y.Z
type: workflow
tags: [workflow, orchestration, domain]
risk_band: HIGH | MEDIUM | LOW
prerequisites: [skill-spatial-grounding, skill-anti-fabrication]
stages:
  - id: sense
    skill: skill-geo-ingest
    checkpoint: arif_judge_deliberate
  - id: eval
    skill: skill-eval-quality
  - id: store
    tool: arif_memory_recall
  - id: seal
    tool: arif_vault_seal
sources: []
confidence: high
---
```

### Workflow ≠ Skill
- **Skill:** single reusable procedure (e.g., "how to patch an agent config")
- **Workflow:** orchestrated chain of skills over time (e.g., "daily geoscience ingest pipeline")

### Skill-driven vs event-driven workflows
- **Skill-driven:** invoked by name when a task matches trigger conditions
- **Event-driven:** triggered by cron, webhook, or A2A message

---

## Skills (Canonical Spec)

A skill page in `wiki/skills/` is the **platform-neutral canonical source**. Per-platform adapters are generated from it, not hand-maintained.

### Required skill frontmatter fields
```yaml
---
title: SKILL: Skill Name
type: skill
version: X.Y.Z              # Semantic version
category: infra | geo | wealth | governance
risk_band: HIGH | MEDIUM | LOW
floors: [F1, F7, F9]       # Constitutional floors this skill implicates
evidence_required: true     # Whether this skill requires evidence before claiming success
sources: [scar-*.md, raw/...]  # Incidents and sources that produced this skill
confidence: high
---
```

### evidence_required field
When `evidence_required: true`, the skill procedure **must** include explicit verification steps. The agent must run terminal/database/API checks before claiming success. This field is mandatory for all skills that produce artifacts (files, DB entries, configs, deployments).

---

## Lint Schedule

- **Weekly:** Run lint check — orphans, broken wikilinks, stale content
- **Monthly:** Review contested pages, update confidence levels
- **Quarterly:** Schema review — update tag taxonomy, page thresholds

---

## Privacy Boundaries

- **Public (wiki/):** Skills, scars, architecture, concepts, comparisons, queries
- **Private (vault/):** Secrets, credentials, personal data, sovereign decisions
- **Redact before publish:** Never expose internal IPs, tokens, keys, or topology in wiki

---

*DITEMPA BUKAN DIBERI — Wiki governs itself via this schema.*