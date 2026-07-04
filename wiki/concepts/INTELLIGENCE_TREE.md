---
title: "INTELLIGENCE TREE — Arif Fazil Federation Ontology"
created: 2026-05-17
updated: 2026-05-17
type: concept
tags: [intelligence, ontology, tree, knowledge, memory, skills, workflow, tools, embodiment, arifOS, kernel, MCP]
sources: [wiki/concepts/AGENT_SKILLS.md, wiki/skills/SKILL_SPATIAL.md, wiki/SCAR_HERMES.md, wiki/concepts/ANTI_FABRICATION.md, wiki/entities/FEDERATION_ENTITIES.md]
confidence: high
---

# INTELLIGENCE TREE — Arif Fazil Federation Ontology

> **Classification:** Federated AI ontology — recursive compilation
> **Authority:** Muhammad Arif bin Fazil (SOVEREIGN)
> **Version:** v2026.05.17-ARIF-TREE

---

## PREAMBLE: WHY THIS TREE EXISTS

This document is the compiled answer to a fundamental question:

> *"Now why skills is not part of memory? So what is memory? What is intelligence? What is workflow? What is knowledge? What is tools application and embodiment?"*

Each term below is defined operationally — what it does, where it lives, how it connects to the others. Not philosophy. Engineering.

---

## THE TREE — Seven Layers

```
INTELLIGENCE (the loop)
├── TOOLS          ← primitives (what the kernel can call)
├── SKILLS         ← structured procedures (how to use tools safely)
├── KNOWLEDGE      ← structured information (what the world looks like)
├── WORKFLOWS      ← orchestrated chains (how skills compose over time)
├── MEMORY         ← persistent traces (what happened before)
├── APPLICATION    ← context-sensitive invocation (when/where to act)
└── EMBODIMENT     ← where the loop runs (the machine surface)
```

---

## 1. TOOLS — Primitive Capabilities

**Definition:** External capabilities the agent can invoke. The atomic actions of the kernel.

**In arifOS MCP:** 13 canonical tools + diagnostics + bridges.

| Tool | Stage | Domain | What it does |
|------|-------|--------|--------------|
| `arif_session_init` | 000 | governance | Session anchor + safety scan |
| `arif_sense_observe` | 111 | reality | 8-stage reality grounding pipeline |
| `arif_evidence_fetch` | 222 | reality | External world data retrieval |
| `arif_mind_reason` | 333 | intelligence | Structured reasoning; branch/merge/audit |
| `arif_reply_compose` | 444r | intelligence | Governed response synthesis |
| `arif_kernel_route` | 444 | intelligence | Routing + risk orthogonality |
| `arif_memory_recall` | 555 | intelligence | Governed memory + skill registry |
| `arif_heart_critique` | 666 | intelligence | Red-team adversarial check (F5/F6/F9) |
| `arif_gateway_connect` | 666g | infra | A2A mesh — agent-to-agent connection |
| `arif_ops_measure` | 777 | infra | Compute/complexity; Landauer cost |
| `arif_judge_deliberate` | 888 | governance | Final constitutional verdict |
| `arif_forge_execute` | 010 | execution | A-FORGE bridge (SEAL-gated only) |
| `arif_vault_seal` | 999 | governance | Immutable Merkle-V3 ledger entry |

**Also in arifOS:** Agent-Zero tools (`arif_agent_zero_list_tools`, `arif_agent_zero_call_tool`, `arif_agent_zero_send_message`).

**In the federation:** Docker, git, terminal, file read/write, network calls, database clients.

**Tool ≠ Skill:** A tool is what you CAN call. A skill is when and how to call it safely.

---

## 2. SKILLS — Structured Procedures

**Definition:** Reusable, named packages that encode when and how to use tools safely. The "how" not the "what."

**Why skills ≠ memory:**
- Memory says: "On 2026-05-17, Hermes fabricated load_spatial.sh. Root cause: no verification."
- Skill says: "When working with spatial context, always validate file existence with terminal before claiming."
- Skills consume memory as evidence. Memory is history. Skills are policies built on that history.

**Skills in AAA:**

| Skill | Type | Canonical Location | Adapter Status |
|-------|------|-------------------|----------------|
| `skill-spatial-grounding` | infra | `wiki/skills/SKILL_SPATIAL.md` | ✅ Claude, ✅ OpenClaw |
| `skill-anti-fabrication` | concept | `wiki/concepts/ANTI_FABRICATION.md` | 🔄 embedded in all agents |
| `skill-arif-workflow` | workflow | `wiki/skills/skill-arif-workflow.md` | 🚧 pending |
| `skill-geo-ingest` | domain | `wiki/skills/skill-geo-ingest.md` | 🚧 pending |
| `skill-wealth-analysis` | domain | `wiki/skills/skill-wealth-analysis.md` | 🚧 pending |

**Skill spec fields (canonical):**
- `name` — canonical identifier
- `version` — semantic versioning
- `summary` — one-line description
- `category` — domain: geo, wealth, infra, governance
- `risk_band` — aligned to F1-F13 floors
- `trigger_conditions` — when to activate
- `procedure` — numbered steps
- `preconditions` — required tools/data/auth
- `expected_outputs` — what it produces
- `failure_modes` — what can go wrong + mitigations
- `verification` — how to confirm it worked
- `sources` — raw evidence references
- `scars` — incidents where this skill failed

---

## 3. KNOWLEDGE — Structured Information

**Definition:** Structured information about the world and system that agents can fetch and use. Both embedded (in model weights) and externalized (in files, wikis, databases).

**Two layers:**

| Layer | Form | Changeable at runtime? |
|-------|------|------------------------|
| **Embedded knowledge** | Patterns packed into LLM weights | No (requires retraining) |
| **Externalized knowledge** | Documents, wikis, SOPs, policies | Yes (via tools) |

**Externalized knowledge in AAA:**

```
wiki/
├── concepts/              ← governance patterns, anti-patterns
│   ├── AGENT_SKILLS.md
│   ├── ANTI_FABRICATION.md
│   └── FEDERATION_ENTITIES.md
├── entities/             ← federation nodes, agents, services
├── skills/               ← reusable capability documents
├── raw/                  ← immutable source evidence
│   ├── repos/           ← architecture configs, audits
│   └── notes/           ← research, dossiers
└── LOG_MD.md               ← append-only action history
```

**Knowledge ≠ Memory:** Knowledge says what IS. Memory says what HAPPENED. Knowledge can be general (geophysics, economics). Memory is specific and temporal (this session, this decision, this scar).

**Knowledge ≠ Skill:** Knowledge says what the world looks like. Skill says how to act given that structure.

---

## 4. WORKFLOWS — Orchestrated Chains

**Definition:** Sequenced sets of steps across tools and systems that transform inputs into outputs. Composed of skills (or tools) as building blocks, orchestrated over time.

**Example — GEOX Daily Ingest:**
```
1. SENSE: arif_sense_observe → load new well logs
2. INGEST: skill-geo-ingest → parse LAS files, quality check
3. EVAL: skill-eval-quality → check depth, curve completeness
4. STORE: arif_memory_recall → write to vector DB
5. DASHBOARD: arif_reply_compose → update status page
6. SEAL: arif_vault_seal → log outcome to VAULT999
```

**Example — Hermes Pagi Brief:**
```
1. SENSE: arif_sense_observe → scan news sources, VAULT999, wiki
2. REASON: arif_mind_reason → apply World Model primer, filter for relevance
3. CRITIQUE: arif_heart_critique → F5 peace check, F9 anti-hallucination
4. COMPOSE: arif_reply_compose → Bahasa Melayu executive brief
5. DELIVER: arif_gateway_connect → send to Telegram DM
6. SEAL: arif_vault_seal → log to VAULT999 outcomes
```

**Workflow ≠ Skill:** A workflow is a composed sequence. A skill is a single reusable procedure. Workflows call skills.

**In AAA:** Workflows live in `wiki/skills/` as multi-step skill pages with stage orchestration.

---

## 5. MEMORY — Persistent Traces

**Definition:** Persistent traces that let the system remember what happened so future sessions can build on it. The historical layer.

**Forms in the federation:**

| Form | Location | What it stores |
|------|----------|----------------|
| **VAULT999** | `vault999/outcomes.jsonl` | Immutable constitutional verdicts, epoch seals |
| **Scar pages** | `wiki/scar-*.md` | Failure incidents with root cause + mitigation |
| **Daily logs** | `memory/YYYY-MM-DD.md` | Raw session events, decisions, open loops |
| **Curated memory** | `MEMORY.md` | Durable truths — preferences, stable facts |
| **Wiki log** | `wiki/LOG_MD.md` | Append-only action history for wiki evolution |
| **Session state** | `arif_session_init` | Per-session anchor + safety scan |

**Memory pattern (operational):**
```
AFTER meaningful event → write to appropriate memory layer
BEFORE significant action → consult memory layers
PERIODICALLY → lint/compact memory (remove transient, preserve durable)
```

**Memory ≠ Skill:** Memory records WHAT HAPPENED. Skill encodes HOW TO ACT to avoid repeating failures.

**Memory ≠ Knowledge:** Memory is temporal (this happened at this time). Knowledge is structural (this is how things work).

---

## 6. APPLICATION — Context-Sensitive Invocation

**Definition:** The decision of WHEN and WHERE to invoke a particular tool, skill, workflow, or knowledge source. The "use it here" layer — where abstraction meets concrete context.

**Examples:**
- When agent exhibits "SSH to localhost" → apply `skill-spatial-grounding` (trigger condition met)
- When briefing time arrives (07:30 MYT) → invoke Hermes Pagi Brief workflow
- When a claim is made → run `arif_evidence_fetch` first (apply knowledge: claims need grounding)
- When F1 irreversible action detected → invoke `arif_judge_deliberate` (apply governance knowledge)

**Application is the judgment call:**
- Not the tool itself (that's TOOLS)
- Not the procedure (that's SKILL)
- Not the sequence (that's WORKFLOW)
- Not the fact (that's KNOWLEDGE)
- Not the history (that's MEMORY)
- **Application = the decision to use tool/skill/workflow here and now, given this context**

**In arifOS:** `arif_kernel_route` (stage 444) handles routing + risk orthogonality — the application decision point.

---

## 7. EMBODIMENT — Where the Loop Runs

**Definition:** The specific machine surface, environment, and tool access that defines what the agent can actually do. The "body" of the intelligence.

**In the federation — three embodiment layers:**

### Layer 1: Physical VPS (Hardware)
```
VPS 72.62.71.199
├── CPU: x86_64 Linux
├── Memory: DDR, SSD
├── Network: Caddy reverse proxy on ports 80/443
└── Access: root user, native filesystem
```

### Layer 2: Container Runtime (Docker)
```
arifOS stack (arifos_core_network)
├── arifOS (port 8080)       ← Constitutional kernel
├── A-FORGE (port 7071)      ← Metabolic shell
├── GEOX (port 8081)          ← Earth coprocessor
├── WEALTH (port 8082)        ← Capital engine
├── WELL (port 8083)          ← Vitality substrate
├── Hermes                    ← Relay agent
├── Agent-Zero               ← A2A mesh
└── Supporting: Postgres, Redis, Qdrant, Ollama, Caddy
```

### Layer 3: Agent Embodiments (Software)
```
Each agent has a specific soft embodiment:
├── OpenClaw (arifOS_bot)   → Telegram DM/group webhook
├── Hermes (ASI relay)      → Telegram polling + cron scheduler
├── Claude Code             → CLI terminal + filesystem
├── Codex                   → CLI terminal + filesystem
├── Gemini                  → API terminal
├── Kimi                    → API terminal
├── Copilot                 → CLI terminal
└── OpenCode                → terminal + filesystem
```

**Embodiment constrains what tools are available.** OpenClaw has Telegram tools. Claude Code has git + terminal. Hermes has cron + file write. The same skill may behave differently across embodiments.

**Embodiment ≠ Application:** Embodiment is WHERE it runs. Application is WHEN/WHAT to invoke.

---

## THE INTELLIGENCE LOOP (How All Seven Connect)

```
┌─────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LOOP                     │
│                                                          │
│  EMBODIMENT → TOOLS → SKILLS → KNOWLEDGE                │
│       ↑           ↑       ↑           ↑                  │
│       │           │       │           │                  │
│    Surface     Atomic   How to    What is                │
│    (where)     actions  safely    true                    │
│       │           │       │           │                  │
│       └───────────┴───────┴───────────┘                  │
│                      ↓                                   │
│              WORKFLOWS (orchestrated sequences)          │
│                      ↓                                   │
│              APPLICATION (when/where to invoke)          │
│                      ↓                                   │
│              MEMORY (persistent traces of outcomes)      │
│                      ↓                                   │
│         Loop back to EMBODIMENT with updated state       │
└─────────────────────────────────────────────────────────┘
```

**INTELLIGENCE = quality of the loop** — how well the system:
- Senses (TOOLS: arif_sense_observe)
- Reasons (TOOLS: arif_mind_reason + KNOWLEDGE)
- Acts (SKILLS + WORKFLOWS)
- Remembers (MEMORY)
- Improves (updates SKILLS + KNOWLEDGE based on MEMORY)

---

## HOW THIS MAPS TO arifOS MCP

| arifOS MCP Stage | Tool | Maps to |
|------------------|------|---------|
| 000 | `arif_session_init` | EMBODIMENT (session anchor) |
| 111 | `arif_sense_observe` | TOOLS (reality grounding) |
| 222 | `arif_evidence_fetch` | KNOWLEDGE (external data) |
| 333 | `arif_mind_reason` | TOOLS + KNOWLEDGE (reasoning) |
| 444r | `arif_reply_compose` | APPLICATION (response decision) |
| 444 | `arif_kernel_route` | APPLICATION (routing + risk) |
| 555 | `arif_memory_recall` | MEMORY (governed recall) |
| 666 | `arif_heart_critique` | SKILLS (adversarial check) |
| 666g | `arif_gateway_connect` | WORKFLOWS (A2A orchestration) |
| 777 | `arif_ops_measure` | TOOLS (compute cost) |
| 888 | `arif_judge_deliberate` | APPLICATION (verdict decision) |
| 999 | `arif_vault_seal` | MEMORY (append-only record) |
| 010 | `arif_forge_execute` | WORKFLOWS (forge bridge) |

---

## AAA WIKI ROLE IN THE TREE

```
AAA/wiki/
├── concepts/          ← KNOWLEDGE (governance patterns)
├── entities/          ← KNOWLEDGE (federation structure)
├── skills/            ← SKILLS (reusable procedures)
├── workflows/         ← WORKFLOWS (orchestrated chains) [pending]
├── raw/               ← KNOWLEDGE (immutable sources)
├── scar-*.md         ← MEMORY (failure incidents)
└── LOG_MD.md            ← MEMORY (action history)
```

AAA is the **structured knowledge + skills layer** — externalized intelligence that all federation agents can query.

---

## RECURSIVE COMPOUNDING LOOP

```
1. Event happens (failure or success)
   → stored in MEMORY (VAULT999, scars, logs)

2. Memory analyzed → pattern extracted
   → written to KNOWLEDGE (concepts, entities)

3. Knowledge operationalized → procedure written
   → becomes SKILL (wiki/skills/)

4. Skills chained → workflow defined
   → becomes WORKFLOW (multi-step orchestration)

5. Workflow invoked via APPLICATION
   → calls TOOLS on EMBODIMENT
   → produces new MEMORY
   → loop repeats
```

**This is the recursive learning engine.** Every loop compounds the intelligence.

---

## THE ARIF TREE — Compiled Skills Registry

### Skills Forged (AAA/wiki/)

| Skill | Forged | Status | Scars |
|-------|--------|--------|-------|
| `skill-spatial-grounding` | 2026-05-17 | ✅ Canonical + adapters | [[scar-hermes-fabrication-2026-05-17]] |
| `skill-anti-fabrication-protocol` | 2026-05-17 | ✅ In all agent configs | [[scar-hermes-fabrication-2026-05-17]] |
| `skill-domain-arif-workflow` | 2026-05-17 | 🚧 pending | — |

### arifOS MCP Skills (kernel tools as skills)

| Skill/Tool | Stage | Domain | Risk |
|-----------|-------|--------|------|
| `arif_session_init` | 000 | governance | F1/F11/F12 |
| `arif_sense_observe` | 111 | reality | F2/F7 |
| `arif_evidence_fetch` | 222 | reality | F2/F3/F5/F12 |
| `arif_mind_reason` | 333 | intelligence | F2/F7/F8/F10 |
| `arif_reply_compose` | 444r | intelligence | F4/F6/F9 |
| `arif_kernel_route` | 444 | intelligence | F1/F3/F4/F10 |
| `arif_memory_recall` | 555 | intelligence | F1/F8 |
| `arif_heart_critique` | 666 | intelligence | F5/F6/F9 |
| `arif_gateway_connect` | 666g | infra | F1/F3 |
| `arif_ops_measure` | 777 | infra | F4 |
| `arif_judge_deliberate` | 888 | governance | F11/F13 |
| `arif_forge_execute` | 010 | execution | F1/F11/F13 |
| `arif_vault_seal` | 999 | governance | F1/F11/F13 |

---

## ONTOLOGICAL DEFINITIONS (One Line Each)

| Term | Definition |
|------|------------|
| **Intelligence** | Quality of the sense→reason→act→remember→improve loop |
| **Tools** | Atomic capabilities the kernel can invoke |
| **Skills** | Structured procedures for when/how to use tools safely |
| **Knowledge** | Structured information about what is (embedded + externalized) |
| **Workflows** | Orchestrated chains of skills over time |
| **Memory** | Persistent traces of what happened (temporal, historical) |
| **Application** | Context-sensitive decision of when/where to invoke |
| **Embodiment** | The machine surface where the loop runs |

---

## RELATED PAGES

- [[agent-skills-architecture]] — cross-platform skills landscape
- [[anti-fabrication-protocol]] — why verification before claim matters
- [[scar-hermes-fabrication-2026-05-17]] — the incident that taught spatial grounding
- [[federation-entities]] — all federation nodes and their embodiment layers
- [[SCHEMA.md]] — wiki governance and agent workflow
- [[concept-tools-and-embodiment]] — **deep research:** philosophical foundations (Clark/Chalmers/Gibson), embodied AI, affordances, and how this tree maps to arifOS kernel stages

---

*DITEMPA BUKAN DIBERI — Intelligence is forged through the loop, not given by the model.*
*999 SEAL ALIVE*