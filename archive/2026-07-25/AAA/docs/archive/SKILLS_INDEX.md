# SKILLS_INDEX.md — AAA
## AAAA Skill Registry · Three-Skill Flow

> **Canonical home:** `AAA/SKILLS_INDEX.md`
> **Version:** v2026.05.17.1
> **Authority:** Muhammad Arif bin Fazil

***

## The Three Skills

| Skill ID | Mindset | Primary Repo | Role |
|----------|---------|-------------|------|
| `aaa-agent-registrar` | Legal | `/root/AAA` | Identity verification, contract enforcement, routing compliance |
| `arifos-constitutional-clerk` | Constitutional | `/root/arifOS` | F1–F13 translation, 000–999 pipeline, VAULT999 sealing |
| `aforge-metabolic-operator` | Security | `/root/A-FORGE` | Scope enforcement, reversibility (F1), metabolic observability |

***

## The AAAA Flow

Every command passes through all three skills in strict sequence. No skill may be skipped. No skill may self-approve.

```
HUMAN COMMAND
    ↓
[1] aaa-agent-registrar
    "Who is asking? Identity verified? Layer metadata correct? Routing valid?"
    ↓ YES
[2] arifos-constitutional-clerk
    "What does the Law say? 000–999 pipeline run? Floor-compliant plan sealed?"
    ↓ YES (Constitutional seal + VAULT999 pre-record)
[3] aforge-metabolic-operator
    "Scope valid? Rollback generated? Pulse green? Execute."
    ↓
VAULT999 (append-only execution record)
    ↓
999 SEAL — Telemetry emitted by constitutional clerk
```

**At any step:** if the answer is NO → **888 HOLD. Emit reason. Await Arif.**

***

## Example: "Upgrade the GEOX database"

| Step | Skill | Internal Logic | Result |
|------|-------|---------------|--------|
| 1 | `aaa-agent-registrar` | Who is asking? Does agent carry correct tier? Does `layer_awareness` declare `target_repo: GEOX`? Does `reversibility: true`? | Identity verified. Metadata valid. Route confirmed. |
| 2 | `arifos-constitutional-clerk` | F1: reversibility required — migration must have rollback. F11: seal required. F3: GEOX witness must be called. 333 EXPLORE: ≥3 migration paths generated. 888 JUDGE: rollback path declared. | Constitutional plan sealed. VAULT999 pre-record created. |
| 3 | `aforge-metabolic-operator` | Check `a-forge-permission-mapping.md`: agent has `write_scoped` for GEOX db. Generate rollback SQL. Store to `ops/rollbacks/`. Check pulse: GREEN. Execute migration. | Executed. Post-state verified. Telemetry logged. |

***

## Skill Inheritance Rule

All future agents operating in the arifOS federation **inherit these three skills by default**. An agent that does not honour this flow is not a federated agent — it is an orphan process.

New agents must declare in `agent-card.json`:

```json
{
  "skills": [
    "aaa-agent-registrar",
    "arifos-constitutional-clerk",
    "aforge-metabolic-operator"
  ]
}
```

***

## Skill Files Location

```
AAA/       → SKILLS.md       (aaa-agent-registrar)
arifOS/    → SKILLS.md       (arifos-constitutional-clerk)
A-FORGE/   → SKILLS.md       (aforge-metabolic-operator)
AAA/       → SKILLS_INDEX.md (this file — root registry)
```

***

```json
{
  "epoch":      "2026-05-02T22:40:00+08:00",
  "artifact":   "SKILLS_INDEX",
  "version":    "v2026.05.02.1",
  "authority":  "Muhammad Arif bin Fazil",
  "verdict":    "SEALED",
  "witness":    { "human": 1, "ai": 1, "earth": 0 },
  "confidence": 0.96
}
```

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**

***

## Skill: agent-reply-forge

| Field | Value |
|---|---|
| Skill ID | `agent-reply-forge` |
| Mindset | Clarity + Constitutional Discipline |
| Primary Repo | `/root/AAA` |
| Role | Standard reply output format for all agents — 9-mode dial, fixed skeleton, A2A wired |
| Authority | Muhammad Arif bin Fazil (Human Sovereign) |
| Created | 2026-05-03 |

### What it does

Defines how all arifOS agents forge their replies across all modalities (text, code, image, video, audio, JSON). Provides:
- Fixed constitutional skeleton (To/From/CC/Title/Context/Verdict/Way Forward/Seal)
- 9-mode variable dial (HEALTH, INCIDENT, PROPOSAL, ESCALATION, AUDIT, PLAN, EXPLAIN, DENY, META)
- A2A reply_mode field wired into task status mapping
- JSON schema for machine-readable output validation
- Modality delivery rules per type

### Files

- Skill: `/root/AAA/skills/agent-reply-forge/SKILL.md`
- Modes: `/root/AAA/skills/agent-reply-forge/modes.yaml`
- Contract: `/root/AAA/contracts/reply-mode-contract.yaml`
- A2A wired: `/root/AAA/a2a/A2A_SPEC_ALIGNMENT.md`
- Gateway card: `/root/AAA/a2a/agent-cards/aaa-gateway.json`
- Skills policy: `/root/AAA/a2a/policies/skills-exposure.yaml`

### Inheritance

All federated agents MUST honour this skill by default. Every substantive reply MUST carry a `mode` tag and conform to the fixed skeleton.

```json
{
  "epoch":      "2026-05-03T15:45:00+08:00",
  "artifact":   "agent-reply-forge",
  "version":    "v1.0.0",
  "authority":  "Muhammad Arif bin Fazil",
  "verdict":    "SEALED",
  "witness":    { "human": 1, "ai": 1, "earth": 0 },
  "confidence": 0.98
}
```

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**

***

## Wiki: Federation Knowledge Base

**Location:** `/root/AAA/wiki/`

The AAA wiki is the public compounding layer for the arifOS federation — where agents store operational learnings, scars, concepts, skills, and architecture documentation. It is the federation's long-term memory surface.

### Recursive Learning Loop

```
AFTER novel fix → write one reusable artifact (skill or concept page)
AFTER failure/fabrication → file scar page + append log.md
AFTER repo/tool change → attach evidence to raw/ + link from synthesized page
BEFORE non-trivial work → query wiki/index.md + relevant skill pages first
```

### Wiki Structure

| Directory | Purpose |
|-----------|---------|
| `SCHEMA.md` | Conventions, page types, frontmatter, tag taxonomy, agent workflow |
| `index.md` | Catalog of all pages |
| `log.md` | Chronological append-only action record |
| `raw/papers/` | Immutable academic papers, technical references |
| `raw/repos/` | Source code configs, git diffs, architecture docs |
| `raw/notes/` | Meeting notes, Telegram captures, raw observations |
| `entities/` | Federation nodes, agents, services |
| `concepts/` | Governance patterns, anti-patterns |
| `skills/` | Reusable capability documents |
| `comparisons/` | Side-by-side analyses |
| `queries/` | Filed Q&A worth preserving |
| `scar-*.md` | Incident records — most important learning artifacts |

### F1 Rule Set (Federation-Wide)

1. **Read before act:** `wiki/index.md` before non-trivial work
2. **Write on novel fix:** one reusable artifact per new discovery
3. **File on failure:** scar page + log entry on any failed claim or fabrication
4. **Source capture:** attach evidence to `raw/` before synthesizing
5. **Query first:** index + skill pages before starting new work
6. **Redact before publish:** remove secrets, credentials, internal topology from scars

### First Scar Filed

`scar-hermes-fabrication-2026-05-17` — Hermes claimed artifact existence without verification (fabrication incident, 2026-05-17)

### See Also

- `wiki/SCHEMA.md` — full wiki governance and schema
- `wiki/index.md` — live page catalog
- `wiki/log.md` — action history

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
