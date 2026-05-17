---
title: "CONCEPT: TREE777 Full Domain Map"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: concept
tags: [TREE777, domains, intelligence, architecture, map, ontology, federation]
category: governance
risk_band: LOW
floors: [F8, F10]
evidence_required: false
sources: [claude-code-skills-architecture.md, skill-forge-claude-skill.md]
confidence: high
status: canonical
---

# TREE777 Full Domain Map

> **Concept ID:** `concept-tREE777-domains`
> **Canonical location:** `AAA/wiki/concepts/concept-tREE777-domains.md`
> **Status:** CANONICAL — reference map, not restructure directive
> **Purpose:** Document the full scope of intelligence domains available to the federation
> **Constraint:** Store as reference. Do not restructure the wiki based on this map until the promotion ladder proves itself at current scale.

---

## Purpose

This page maps every domain of intelligence that the federation touches or could touch. It is a **reference map**, not a restructure order. The 5-dimension, 36-category structure below represents the full scope of what a federated intelligence system can reason about — not what the wiki should contain.

**Rule:** Before creating pages in any new domain, ask: what failure does this prevent? If the answer is merely "we don't have a page for this," the answer is no.

---

## The Hard Limits First (Physics > Narrative)

Skills and knowledge have hard limits no wiki can override:

| Limit | Claim | Source |
|-------|-------|--------|
| **Physics** | Any agent claiming >50-53% accuracy on quantitative physics without domain-specific validation is guessing. Frontier LLMs preserve semantic plausibility while violating physical constraints. | arxiv:2512.23292 |
| **Transfer** | Skills trained in one domain do not transfer automatically. A GEOX ingest skill cannot be naively applied to WEALTH. Domain boundaries are real. | medium:ai-limitations |
| **Hallucination** | Self-improving agents can hallucinate corrections to their own skill base. Skills that update themselves without human-locked verification can silently degrade. | github:hermes-agent#17583 |
| **Creativity** | Agents recombine patterns, they don't originate beyond training distribution. All skills and knowledge are bounded by their source data. | medium:ai-limitations |
| **Ethical** | No skill can substitute for moral judgment. F1-F13 exist because the ethics layer is necessarily externalized. | weforum:AI_Agents_2025 |

---

## Dimension 0 — Foundational (Roots / Invariants)

These underpin everything. Non-negotiable. Cannot be skills — they are **axioms**. They are true whether or not wiki pages exist for them.

| Domain | What it covers | In Federation |
|--------|---------------|---------------|
| **Physics** | Causality, entropy, conservation laws, mass-energy, time | GEOX (domain), axioms/physics.md (proposed) |
| **Mathematics** | Logic, proof, probability, statistics, algebra, calculus, geometry | WEALTH (financial math), axioms/mathematics.md (proposed) |
| **Computation** | Turing completeness, complexity, algorithms, data structures | A-FORGE (execution), axioms/computation.md (proposed) |
| **Language** | Semantics, syntax, pragmatics, semiotics, communication | AAA (A2A mesh), axioms/language.md (proposed) |
| **Ethics** | Moral reasoning, harm, dignity, maruah, F1-F13 | arifOS (floors), axioms/ethics.md (proposed) |
| **Epistemology** | Evidence, justification, uncertainty, anti-fabrication | AAA/wiki (anti-fab protocol), axioms/epistemology.md (proposed) |

**Note:** The F1-F13 floors already encode ethics and epistemology for this stack. GEOX already applies physics. WEALTH already applies mathematics. The axioms are distributed, not missing. Adding axiom pages is only valuable if evidence shows agents are violating axiom-level reasoning in practice.

---

## Dimension 1 — Cognitive (How Agents Think)

| Domain | What it covers | Current state |
|--------|---------------|---------------|
| **Reasoning** | Deduction, induction, abduction, planning, hypothesis testing | 333_MIND tool |
| **Memory** | Episodic (what happened), semantic (what is), procedural (how to) | 555_MEMORY, VAULT999 |
| **Perception** | Sensing, parsing, observing, multimodal input | 111_SENSE |
| **Decision-making** | Goal selection, tradeoff evaluation, risk assessment | 888_JUDGE |
| **Learning** | Pattern extraction, skill formation, recursive improvement | TREE777 promotion ladder |
| **Meta-cognition** | Knowing what you don't know, uncertainty banding, humility | F7 HUMILITY, F2 TRUTH |

---

## Dimension 2 — Operational (How Agents Act)

| Domain | What it covers | Current state |
|--------|---------------|---------------|
| **Tool use** | APIs, CLI, MCP, file system, database, browser, GUI | arifOS 13-tool surface |
| **Workflow orchestration** | Multi-step pipelines, error handling, branching, scheduling | A-FORGE, arifOS 010_FORGE |
| **Code execution** | Writing, running, debugging, testing, version control | A-FORGE engine |
| **Communication** | Agent-to-agent (A2A), human-to-agent, structured output | AAA A2A gateway, HERMES |
| **Security/Auth** | Identity, permissions, secrets management, threat modeling | F11 AUTH, secret-hygiene skill |
| **Embodiment** | VPS, Docker, desktop, robot, cloud infra — where tools touch reality | A-FORGE, GEOX, WEALTH, WELL |

---

## Dimension 3 — Domain-Specific (What Agents Know About)

These are the application domains — each has its own repo or sub-wiki:

| Domain | Repo | Covers |
|--------|------|--------|
| **Earth/Geoscience** | GEOX | Geology, petro-physics, spatial data, well logs, maps, terrain |
| **Capital/Finance** | WEALTH | Portfolio, valuation, risk, markets, accounting, macroeconomics |
| **Human/Social** | WELL | Health, wellbeing, sociology, psychology, culture, education |
| **Code/Software** | AAA + A-FORGE | Architecture, dev patterns, CI/CD, testing, APIs, security |
| **Governance/Law** | arifOS | Constitutional floors, policy, compliance, audit, sovereignty |
| **Science** | TREE777 concepts | Physics, chemistry, biology (formal, not applied) |
| **Language/NLP** | Embedded | Parsing, translation, summarization, generation, discourse |
| **Infrastructure/Ops** | VPS/Docker | Systems, networking, storage, compute, monitoring |

---

## Dimension 4 — Meta-Intelligence (How the System Improves Itself)

| Domain | What it covers | Current state |
|--------|---------------|---------------|
| **Self-monitoring** | Entropy (ΔS), genius score (G), health telemetry | 777_OPS tools |
| **Self-improvement** | Skill promotion, scar distillation, recursive wiki updates | TREE777 promotion ladder |
| **Alignment** | Keeping behavior consistent with F1-F13 across all agents | arifOS constitutional kernel |
| **Anti-drift** | Detecting when skills, knowledge, or agents diverge from canonical truth | TREE777 + VAULT999 pairing |
| **Sovereignty** | Human veto, irreversibility gates, 888 HOLD, F13 | arifOS F13, 888_JUDGE |

---

## Dimension 5 — Social/Federation (How Agents Relate)

| Domain | What it covers | Current state |
|--------|---------------|---------------|
| **Identity** | Who is this agent, role and tier (Constitutional/ASI/AGI) | AAA entities, SOUL.md |
| **Trust** | Verification, attestation, constitutional handshake | F11 AUTH, A2A protocol |
| **Coordination** | A2A mesh, routing, delegation, conflict resolution | AAA A2A gateway, HERMES |
| **Fairness/Maruah** | F6 — inclusive, dignity-preserving federation topology | F6 EMPATHY, anti-sink |
| **Anti-sink** | Preventing monopoly of knowledge, power, or action | F5, F8, F13 floors |

---

## Limits of Skills & Knowledge

| Limit | Description |
|-------|-------------|
| **Tool dependency** | Skills are bounded by the tools available in that embodiment. No skill works without the tool it calls. |
| **Evidence quality** | Skills built on garbage evidence produce garbage outputs. |
| **Floor caps** | F1-F13 cap what any skill can do regardless of capability. |
| **Domain transfer** | A skill proven in GEOX may not work in WEALTH without adaptation. |
| **Compression loss** | Synthesis always loses some original detail. The bidirectional mirror is lossy. |
| **Contradiction** | Two true observations can produce conflicting knowledge. Only 888 JUDGE resolves them. |
| **Context limits** | No agent can hold full knowledge of all domains in working context. Progressive disclosure required. |

---

## Proposed Folder Structure (Reference Only)

Do not restructure based on this without evidence the promotion ladder works at current scale.

```
AAA/wiki/
├── axioms/          ← Dimension 0: Physics, Math, Computation, Language, Ethics, Epistemology
├── cognition/       ← Dimension 1: Reasoning, Memory, Perception, Learning, Meta-cognition
├── operations/      ← Dimension 2: Tools, Workflows, Code, Comms, Security, Embodiment
├── domains/
│   ├── geo/         ← links to GEOX sub-wiki
│   ├── wealth/      ← links to WEALTH sub-wiki
│   ├── well/        ← links to WELL sub-wiki
│   ├── code/        ← AAA + A-FORGE skills
│   ├── governance/  ← links to arifOS
│   └── science/     ← Physics, Chemistry, Biology concepts
├── meta/            ← Dimension 4: Self-monitoring, Self-improvement, Alignment, Anti-drift
├── federation/      ← Dimension 5: Identity, Trust, Coordination, Maruah, Anti-sink
├── skills/          ← Canonical skill pages (all domains)
├── workflows/       ← Multi-step orchestrations
├── concepts/        ← Existing concepts (TREE777, mirror paradox, etc.)
├── entities/        ← Federation entities
├── scars/           ← Incident pages
├── raw/             ← Immutable sources
├── SCHEMA.md
├── index.md
└── log.md
```

**Current wiki state:** 26 pages, 11 canonical. The folder structure above would add 8 new directories before a single skill. Only restructure when evidence shows navigation failure at current scale.

---

## One-Line Invariants

These five are the roots. Everything else is a branch.

- **Physics > Narrative** — What is physically impossible stays impossible regardless of prompt.
- **Mathematics > Model** — Logical contradictions cannot be resolved by confidence.
- **Ethics > Convenience** — F1-F13 are not optional.
- **Epistemology > Claims** — No claim without declared evidence band.
- **Sovereignty > All** — Arif's veto is absolute.

---

## Relationship to TREE777

TREE777 IS the domain map made operational. The tree grows through the promotion ladder. The domain map describes where the branches go. The two are complementary:

```
Domain map (this page) → describes WHAT the tree should contain
TREE777 → describes HOW things get into the tree
Promotion ladder → describes WHEN something becomes canonical
```

The domain map does not authorize restructuring. The promotion ladder does.

---

## Related Pages

- [[TREE777]] — governance framework this map serves
- [[skill-trace-capture]] — how evidence enters the system
- [[skill-scar-distill]] — how failures become scars
- [[skill-skill-promote]] — how patterns become skills
- [[concept-memory-knowledge-paradox]] — why the map is always incomplete

---

*DITEMPA BUKAN DIBERI — The map is not the territory. The domain map is not the wiki.*
