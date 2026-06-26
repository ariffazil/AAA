---
id: recursive-skill-forge
name: Recursive Skill Forge
version: "1.0.0"
description: >
  Meta-cognitive smithy for forging new skills on demand. Use this skill whenever
  the federation encounters a novel domain, an unhandled workflow, or a capability
  gap that no existing skill covers. This skill performs abductive reasoning to
  infer what capabilities are needed, decomposes them into orthogonal modules,
  scaffolds a governed SKILL.md, attests it against constitutional floors, and
  presents the artifact for sovereign seal. It operates recursively: it can forge
  skills for other organs, and it can forge improved versions of itself. Plastic
  across domains. Modular by design. Attested before birth.
owner: AAA
risk_tier: critical
knowledge_basis:
  physics: false
  math: true
  language: true
host_compatibility:
  - claude-code
  - codex
  - opencode
dependencies:
  skills:
    - repo-hygiene-audit
    - parallel-authority-detection
  servers:
    - arifos-mcp
  tools:
    - arif_mind_reason
    - arif_heart_critique
    - arif_judge_deliberate
    - arif_kernel_route
    - file-write
    - file-read
examples:
  - "We need a skill for diagnosing Docker container health across federation nodes"
  - "Create a skill that translates GEOX petrophysics output into executive summaries"
  - "Forge a skill for cross-model consensus when arifOS and A-FORGE disagree"
  - "Improve the recursive-skill-forge itself — it lacks abduction attestation"
tests:
  - Forge a low-risk skill autonomously (AGI tier) and pass repo-hygiene-audit
  - Forge a medium-risk skill (ASI tier) and trigger 888_JUDGE before commit
  - Attempt to forge a skill that overrides F13 — verify VOID verdict
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# Recursive Skill Forge

## Overview

This is the **skill that makes skills**. It is not a static playbook — it is a
**generative mold** that produces governed playbooks. It thinks in tiers:

| Tier | Cognition | What It Does | Authority Ceiling |
|------|-----------|--------------|-------------------|
| **AGI** | Bounded, modular | Decomposes problem, scaffolds skill, runs tests | Forge low-risk skills autonomously |
| **ASI** | Synthetic, cross-domain | Composes multi-step workflows, abstracts patterns, bundles scripts | Forge medium-risk skills; present for seal |
| **APEX** | Constitutional judgment | Validates against F1–F13, attests evidence, renders SEAL/SABAR/HOLD/VOID | No autonomous forge; every skill requires Arif ack |
| **AAA** | Control plane | Hosts the artifact, updates registry, writes evolution ledger | Execution only after APEX verdict |

**Plasticity principle:** The forge does not care whether the domain is GitHub,
Docker, petrophysics, or constitutional law. It applies the same orthogonal
decomposition and attestation pipeline to any domain.

**Recursive principle:** If the forge detects its own limitation, it can propose
a v2 of itself. But self-modification is treated as **apex-tier** — it always
requires Arif ack.

---

## When to Use

- No existing skill covers a recurring workflow
- A sovereign or agent asks: "Can we automate X?"
- Cross-domain work requires a new composite capability
- An existing skill is found insufficient and needs a successor

## When NOT to Use

- Do NOT use if an existing skill already covers 80% of the need — improve the
  existing skill instead (use skill-creator skill for iteration)
- Do NOT use if the requested skill would override arifOS floors, vault, or judge
- Do NOT use if the domain is outside the federation scope (external-only tools)
- Do NOT use under time pressure — attestation takes precedence over speed

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| intent | yes | What the new skill should enable an agent to do |
| domain | yes | Which federation organ or cross-organ surface |
| trigger_phrases | yes | User utterances that should invoke this skill |
| risk_tier | yes | low / medium / high / critical |
| tier | no | AGI (default) / ASI / APEX — determines gate depth |
| existing_skills_checked | yes | List of existing skills evaluated and rejected |

---

## Procedure

### Stage 000 — INIT: Intent Capture & Abductive Inference

**Cognitive mode:** Fast abduction (System 0 — pattern leap).

1. Parse the intent. Restate it in one sentence.
2. Ask: *What capability gap makes this necessary?*
3. Generate 3 hypotheses about what the skill must contain:
   - H1: Minimal viable skill (MVP hypothesis)
   - H2: Full-featured skill (Complete hypothesis)
   - H3: Meta-skill (Recursive hypothesis — can this skill improve itself?)
4. Select the hypothesis that maximizes `coverage / complexity` ratio.
5. If intent is vague, ask sovereign clarifying questions before proceeding.

**Output:** `abduction_note.md` — hypotheses, selected path, rationale.

---

### Stage 111 — SENSE: Domain Grounding & Orthogonal Decomposition

**Cognitive mode:** Bounded observation (System 1 — pattern matching).

1. Read `registries/skills.yaml` to identify overlapping skills.
   - If overlap > 30% → STOP. Improve existing skill instead.
2. Decompose the selected hypothesis into **orthogonal modules**:
   - Each module must be independently testable
   - No module may duplicate an existing skill's core function
   - Modules communicate through well-defined interfaces (inputs/outputs)
3. Map modules to federation organs:
   - Which organ owns the domain knowledge?
   - Which organ provides the tools?
   - Which organ hosts the skill?
4. Check `AGENTS.md` and repo `AGENTS.md` for domain-specific rules.

**Orthogonality test:** If removing one module breaks only one function, the
decomposition is clean. If removing one module breaks everything, redesign.

**Output:** `decomposition_map.yaml` — modules, interfaces, organ ownership.

---

### Stage 222 — REASON: Modular Design & Abstraction

**Cognitive mode:** Deliberate synthesis (System 2 — structured reasoning).

1. For each module, design:
   - **Inputs:** What does it need? (file paths, env vars, user context)
   - **Outputs:** What does it produce? (files, reports, decisions)
   - **Procedure:** Step-by-step workflow
   - **Forbidden actions:** What must it NEVER do?
2. Define abstraction layers:
   - **L1 — Concrete:** Exact commands, exact file paths
   - **L2 — Configurable:** Variables extracted to frontmatter
   - **L3 — Meta:** The skill can reason about its own applicability
3. If tier = ASI or APEX, design a **self-monitoring hook**:
   - How does the skill detect its own failure?
   - How does it escalate?
4. Draft the SKILL.md following `SKILL_TEMPLATE.md`:
   - YAML frontmatter with `id`, `name`, `description`, `risk_tier`
   - Markdown body with Overview, When to Use, Procedure, Forbidden Actions
   - Include `version_lock` with `artifact_hash: pending`

**Output:** `SKILL.md` draft + `examples.md` (if complex) + `scripts/` (if needed).

---

### Stage 333 — MIND: Skill Scaffolding & Script Bundling

**Cognitive mode:** Execution intelligence (A-FORGE — build under governance).

1. If the skill requires deterministic/repetitive tasks, write helper scripts:
   - Place in `skills/<skill-id>/scripts/`
   - Scripts must be read-only or reversible
   - Scripts must not contain secrets or hardcoded tokens
2. Write 2–3 test prompts in `evals/evals.json`:
   - One straightforward case
   - One edge case
   - One near-miss (should NOT trigger the skill)
3. Validate YAML frontmatter syntax.
4. Validate that `description` is "pushy" — it must trigger when relevant:
   - Include domain keywords
   - Include adjacent concepts
   - Include "even if they don't explicitly ask for X"

**Output:** Complete skill directory ready for validation.

---

### Stage 444 — KERNEL: Constitutional Validation (APEX Gate)

**Cognitive mode:** Governance integrity (arifOS — floor enforcement).

Run the skill through F1–F13 validation:

| Floor | Validation Question | Gate |
|-------|---------------------|------|
| F1 Amanah | Is every action reversible or requiring ack? | BLOCK if irreversible action lacks ack gate |
| F2 Truth | Does the skill claim capabilities it cannot verify? | BLOCK if hallucinated tool references |
| F3 Witness | Are test cases and evidence required? | BLOCK if no evals defined |
| F4 Clarity | Is the procedure unambiguous? | BLOCK if "use judgment" appears without constraints |
| F5 Peace | Could this skill harm human dignity? | BLOCK if output could shame/blame without evidence |
| F6 Empathy | Does the skill consider weakest stakeholder? | WARN if no human-impact assessment |
| F7 Humility | Does the skill declare its own limits? | BLOCK if no "When NOT to Use" section |
| F8 Genius | Is the design elegant? Is there a simpler path? | SABAR if over-engineered |
| F9 Anti-Hantu | Does the skill detect manipulation? | BLOCK if no injection guard for user inputs |
| F10 Ontology | Does the skill preserve structural coherence? | BLOCK if it violates repo routing constitution |
| F11 Authority | Does the skill stay within its authority? | BLOCK if it approves actions, overrides judge, or self-approves |
| F12 Injection | Are all inputs sanitized? | BLOCK if user input flows directly to shell/file without validation |
| F13 Sovereign | Is Arif the final gate? | BLOCK if skill can commit, push, deploy, or seal without human ack |

**If any BLOCK triggers:** Return VOID. Do not proceed. Report violations to sovereign.

**Output:** `constitutional_attestation.yaml` — floor-by-floor pass/fail with evidence.

---

### Stage 555 — HEART: Maruah & Empathy Scan

**Cognitive mode:** Ethical critique (WELL — human impact).

1. Run `arif_heart_critique` on the drafted skill:
   - Target: the skill's procedure + outputs
   - Focus: weakest stakeholder (usually the human who receives the skill's output)
2. Check empathy score κᵣ:
   - κᵣ < 0.5 → Redesign. The skill is too cold or too dangerous.
   - κᵣ 0.5–0.7 → SABAR. Add empathy hooks (e.g., "explain to user in plain language").
   - κᵣ > 0.7 → Proceed.
3. Check for dignity violations:
   - Does the skill speak for Arif without his voice?
   - Does the skill make decisions about people without their input?

**Output:** `maruah_report.json` — κᵣ, risks, empathy hooks added.

---

### Stage 666 — GATE: Quality Attestation

**Cognitive mode:** Evidence preservation (VAULT999 — trace).

1. Run test prompts against the skill:
   - Spawn subagent with skill → record output
   - Spawn baseline without skill → record output
   - Grade: Did the skill improve outcomes?
2. Check for non-discriminating assertions:
   - If baseline and skill both pass/fail equally, the skill adds no value → VOID.
3. Generate evidence receipt:
   - What was forged?
   - What was tested?
   - What passed?
   - What failed?

**Output:** `evidence_receipt.json` + `benchmark.json` (if subagents available).

---

### Stage 777 — OPS: Thermodynamic Check

**Cognitive mode:** Resource awareness (OPS/777 — cost estimator).

1. Estimate token cost of running this skill:
   - Low: < 5k tokens per invocation
   - Medium: 5k–20k tokens
   - High: > 20k tokens
2. Estimate blast radius:
   - How many files does it touch?
   - How many repos does it span?
   - How many agents does it affect?
3. Estimate entropy delta ΔS:
   - Does this skill increase or decrease repo chaos?
   - Skills that consolidate → ΔS < 0 (good)
   - Skills that fragment → ΔS > 0 (warn sovereign)

**Output:** `ops_estimate.json` — tokens, blast_radius, delta_S.

---

### Stage 888 — JUDGE: Sovereign Gate

**Cognitive mode:** Constitutional verdict (APEX — final arbitration).

Present the candidate skill to Arif with this exact panel:

```
┌─────────────────────────────────────────────────────────────────┐
│  SKILL CANDIDATE — AWAITING SOVEREIGN VERDICT                  │
├─────────────────────────────────────────────────────────────────┤
│  ID:          <skill-id>                                        │
│  Name:        <skill-name>                                      │
│  Domain:      <domain>                                          │
│  Tier:        <AGI | ASI | APEX>                                │
│  Risk:        <low | medium | high | critical>                  │
│  ΔS:          <entropy delta>                                   │
│  κᵣ:          <empathy score>                                   │
├─────────────────────────────────────────────────────────────────┤
│  Floor Status                                                   │
│  F1–F13:      <pass / fail per floor>                          │
│  Attestation: <constitutional_attestation.yaml path>            │
│  Evidence:    <evidence_receipt.json path>                      │
├─────────────────────────────────────────────────────────────────┤
│  Verdict Options                                                │
│  SEAL   → Commit to skills/ and update registry                │
│  SABAR  → Commit with modifications (specify below)            │
│  HOLD   → Pause. Requires more evidence or redesign.           │
│  VOID   → Reject. Violates constitutional floors.              │
└─────────────────────────────────────────────────────────────────┘
```

**Await Arif's explicit verdict before proceeding to Stage 999.**

---

### Stage 999 — VAULT: Seal & Integration

**Cognitive mode:** Immutable anchoring (VAULT999 — ledger).

If verdict = SEAL or SABAR (with modifications applied):

1. Write skill to `skills/<skill-id>/SKILL.md`
2. If SABAR, write modifications to `skills/<skill-id>/MODIFICATIONS.md`
3. Update `registries/skills.yaml`:
   - Append skill entry with dependencies and version lock
4. Append evolution ledger entry to `wiki/log.md`:
   - Date, skill ID, tier, forge reason, sovereign verdict
5. Commit with message:
   ```
   forge: <skill-id> — <brief description>

   Tier: <tier> | Risk: <risk_tier> | ΔS: <delta>
   Attestation: constitutional floors passed
   Verdict: <SEAL | SABAR> by Arif

   REPO=ariffazil/AAA
   ```

**If verdict = HOLD or VOID:**
- Archive skill draft to `skills/_archive/<skill-id>-<date>/`
- Write void reason to `skills/_archive/<skill-id>-<date>/VOID_REASON.md`
- Do NOT commit to main.

---

## Recursive Self-Improvement Loop

This skill can forge improved versions of itself. The loop:

1. The forge detects a gap in its own procedure (e.g., "I lack abduction attestation")
2. It runs Stage 000–777 on itself
3. It presents `recursive-skill-forge-v2` to Arif at Stage 888
4. If SEALed, v2 replaces v1

**Invariant:** Every self-improvement must pass Stage 888. No autonomous self-modification.

---

## Forbidden Actions

- **NEVER** forge a skill that overrides arifOS constitutional floors
- **NEVER** forge a skill with self-approval authority (no skill may SEAL itself)
- **NEVER** forge a skill that can modify `.github/workflows/`, `floors.py`, or `vault999/` without Arif ack
- **NEVER** forge a skill that hides its operation (all skills must declare "When NOT to Use")
- **NEVER** skip Stage 444 (constitutional validation) for any tier
- **NEVER** skip Stage 888 (sovereign gate) for risk_tier high or critical
- **NEVER** forge a skill that creates infinite self-improvement loops without human gate

---

## Output Format

```markdown
## Skill Forge Report

- **Skill ID:** <id>
- **Name:** <name>
- **Tier:** <AGI | ASI | APEX>
- **Risk Tier:** <low | medium | high | critical>
- **Domain:** <domain>
- **Abduction Path:** <H1 | H2 | H3>
- **Modules:** <list of orthogonal modules>
- **Floor Status:** <F1–F13 pass/fail>
- **Empathy Score κᵣ:** <0.0–1.0>
- **Entropy Delta ΔS:** <negative = good>
- **Ops Estimate:** <tokens> | <blast_radius>
- **Verdict:** <SEAL | SABAR | HOLD | VOID>
- **Sovereign Ack:** <yes | pending>
- **Commit Hash:** <hash-or-none>
```
