---
id: asi_position_contrast
name: asi_position_contrast
agent: 555-ASI
namespace: asi_*
cluster: SYNTHESIS
version: 1.0.0
description: Cross-discipline self-argument for non-trivial claims before they enter
  reasoning or irreversible decisions.
owner: AAA
risk_tier: low
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills: []
  servers:
  - arifos-mcp
  tools:
  - mcp__arifos__arif_think
  - mcp__arifos__arif_critique
  - mcp__arifos__arif_judge
examples:
- Challenging a proposed architecture change before it enters a design document
- Stress-testing a geological interpretation before it becomes a recommendation
- Auditing a cost estimate before it informs a capital allocation decision
tests:
- A claim with 3+ independent challenges returns a synthesized verdict and witness
  log
- A claim rejected by ≥2 disciplines triggers an 888 HOLD recommendation
- Disciplines that are too similar are flagged and replaced
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Δ
  functional:
  - Governance
  - Evidence
  layer: HEXAGON
  autonomy_tier: T1
floor_scope:
- F2
- F7
- F8
---

# Multi-Discipline Critique

> **Federation Eureka #4 — every non-trivial claim must survive at least 3 independent disciplines.**
>
> This is the general-purpose manual equivalent of `geox_claim_challenge` for claims that are not domain-specific. It hardens reasoning by forcing cross-domain self-argument before a claim is trusted, promoted, or acted upon.

## Overview

This skill installs a structured cross-discipline argument protocol. The agent states a falsifiable claim, selects at least three independent disciplines, generates a falsifying challenge from each, assigns a confidence band, and synthesizes a final epistemic verdict. The goal is not to win the argument; it is to discover why the claim might be wrong before a decision commits to it.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- Before stating or relying on a non-trivial factual claim.
- Before recommending an architecture, design, or policy change.
- Before any irreversible or seal-bound decision.
- When a single domain could be producing false confidence.
- When the cost of being wrong exceeds the cost of delay.

## When NOT to Use

- **Do not use** for trivial or definitional claims where the overhead exceeds the risk.
- **Do not use** as a substitute for domain-expert review when human expertise is required.
- **Do not use** to rationalize a predetermined conclusion; run skeptical mode if the first pass is too easy.
- **Do not proceed** with a claim that fails ≥2 disciplines without escalating to 888_JUDGE.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| claim | yes | One falsifiable sentence to be challenged |
| claim_type | yes | `CLAIM` / `PLAUSIBLE` / `HYPOTHESIS` / `ESTIMATE` / `UNKNOWN` |
| disciplines | yes | ≥3 independent challenge lenses selected for this claim |
| skeptical_mode | no | If true, assume refuted and force proof otherwise (default false) |

## Procedure

### Step 1: State the Claim

Reduce the claim to one falsifiable sentence. Tag it:

- **CLAIM** — asserted as true
- **PLAUSIBLE** — likely but not proven
- **HYPOTHESIS** — candidate explanation awaiting test
- **ESTIMATE** — quantitative guess with error bars
- **UNKNOWN** — insufficient information to classify

### Step 2: Select ≥3 Independent Disciplines

Choose lenses that cover different failure modes. Examples include:

| Discipline | Challenge question |
|------------|--------------------|
| **Epistemics** | Is the evidence chain intact? What is the source provenance? |
| **Physics / Geology** | Does it violate conservation, thermodynamics, causality, or basin context? |
| **Law / Policy** | Does it conflict with `/root/SECRETS.md`, F1–F13, or stated rules? |
| **Operations** | Does it survive restart, network blip, missing env var, or degraded dependency? |
| **Security** | Does it leak, escalate, bypass a deny rule, or widen blast radius? |
| **Cost / Economics** | Is the resource ask proportional to the expected value? |
| **Ethics / Dignity** | Does it reduce a person to a pattern or coerce a choice? |

Mix domains. `physics + geophysics` is too close; replace one.

### Step 3: Challenge from Each Discipline

For each lens, answer:

1. What would falsify the claim from this perspective?
2. What evidence supports the challenge?
3. What is the confidence band? (`high` / `medium` / `low` / `none`)

Use `mcp__arifos__arif_think` for structured reasoning and `mcp__arifos__arif_critique` mode=redteam as one automatic discipline.

### Step 4: Synthesize

Tally the discipline verdicts:

- **All concur** → promote the claim; log the witness mix.
- **1 rejects** → revise the claim or downgrade its epistemic tag.
- **≥2 reject** → **888 HOLD**; do not use the claim as a premise.

### Step 5: Output Verdict and Witness Log

Return the final tag plus a per-discipline log. If skeptical mode was enabled, note whether the claim still survived.

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `Read` / `Bash` | Inspect evidence, rules, or source material referenced by the claim |
| `mcp__arifos__arif_think` | Structured multi-step reasoning and evidence synthesis |
| `mcp__arifos__arif_critique` | Red-team / empathic challenge as an automatic discipline |
| `mcp__arifos__arif_judge` | Escalate to F1–F13 judgment if the claim feeds an irreversible decision |

## Forbidden Actions

- **NEVER** treat a claim as proven after only one discipline concurs.
- **NEVER** select disciplines that are structurally similar to manufacture false consensus.
- **NEVER** skip the discipline that seems "obvious" — that is the one that usually bites.
- **NEVER** hide a rejecting discipline in the final synthesis.
- **NEVER** promote a claim that ≥2 disciplines reject without 888_JUDGE review.
- **NEVER** run this skill backwards by writing the conclusion first and fitting challenges around it.

## Output Format

```markdown
## Skill Result: multi-discipline-critique

### Summary
One-sentence synthesis of whether the claim survives and under what epistemic tag.

### Claim
<original falsifiable claim>

### Discipline Verdicts
| Discipline | Verdict | Confidence | Falsifying Concern |
|------------|---------|------------|-------------------|
| Epistemics | concur / reject / revise | high / medium / low / none | ... |
| Security | concur / reject / revise | high / medium / low / none | ... |
| Operations | concur / reject / revise | high / medium / low / none | ... |

### Synthesis
- Promote / Revise / Hold
- Final tag: CLAIM / PLAUSIBLE / HYPOTHESIS / ESTIMATE / UNKNOWN
- Reasoning: why the claim does or does not survive

### Recommendations
- Action if the claim is promoted
- Revision if one discipline rejects
- Escalation path if ≥2 reject

### Escalations
- None / 888_JUDGE / human sovereign
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| ≥2 disciplines reject the claim | arifOS 888_JUDGE | A2A / MCP verdict_request |
| Claim feeds an irreversible decision | arifOS 888_JUDGE + human | hold with reason |
| Discipline selection is too narrow | Re-run with broader lens mix | internal loop |
| Source evidence appears fabricated or misattributed | security.agent + arifOS judge | A2A message |

---

*Skill imported from `/root/.claude/skills/multi-discipline-critique.md` — AAA A2A skill registry.*
*Orthogonal tags: Δ | Governance, Evidence | HEXAGON | T1 | F2, F7, F8.*
