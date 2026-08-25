---
name: skill-creator
id: skill-creator
version: 2.0.0
description: >
  Create, lint, and package new skills. Bootstrap skill design from user intent,
  validate trigger clauses for collisions/missing negatives/vague verbs, and
  interactively scaffold SKILL.md files. Use when creating a skill, scaffolding
  a skill, linting skill triggers, or packaging skills for distribution.
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F1, F2, F4, F7, F9, F10, F11]
tags: [skill-creator, skill-linter, create-skill, bootstrap, lint, trigger, package]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Skill Creator — Create, Lint & Package Skills

> **DITEMPA BUKAN DIBERI** — Skills are forged through intent, lint, and seal.

## What This Skill Is

A unified skill covering three concerns:

1. **Create** — Bootstrap, design, and package new skills from user intent
2. **Lint** — Check trigger clauses for collisions, missing negatives, and vague verbs
3. **Scaffold** — Interactively create SKILL.md files with proper frontmatter

## When to Use

- Capturing user intent for a brand new skill from conversation history
- Conducting interviews to identify edge cases, input/output requirements, and dependencies
- Drafting the initial structure, frontmatter, and instructions for a new SKILL.md
- Validating frontmatter descriptions and target boundaries of any skill
- Trigger drift is observed (e.g. `wrangler` activated for generic coding)
- Linting a newly forged skill prior to production staging
- Packaging finished skill folders into distributables
- User wants to create a skill, scaffold a skill, or runs /create-skill

## When NOT to Use

- Auditing the active skill portfolio for collisions or stale documentation (use `skill-inventory`)
- Running quantitative benchmarks or evaluating prompt traces
- Performing programmatic runtime execution benchmark testing

## §1. CREATE — Bootstrap & Design

### Procedure

1. **Capture Intent:** Analyze the user request and extract target tools, sequence steps, and expected outputs
2. **Define Trigger Boundaries:** Design preliminary "Use when" and "Do not use when" rules
3. **Draft SKILL.md:** Compose the frontmatter, purpose, triggers, inputs, procedure, postconditions, failure modes, and telemetry structure
4. **Verification Setup:** Propose 2-3 realistic test prompts for verification
5. **Floor-Tier SEAL Gate (MANDATORY):** Classify the drafted skill by primary floor touch
6. **Package Skill:** Run `scripts/package_skill.py` to compile the folder structure

### Floor-Tier SEAL Gate

| Primary floor | SEAL authority | Action |
|---|---|---|
| **F1**, **F8**, **F13** | **888 mandatory** | Emit `hold_code`. Pause. Await Arif acknowledgment. |
| **F2**, **F4**, **F11** | **Grader PASS + human sign-off** | Present grading.json to human. Await sign-off. |
| **F5**, **F6**, **F7**, **F9**, **F10** | **Grader PASS → autonomous SEAL** | Proceed. Log the tier in telemetry. |

**Grader output requirement:** `pass_rate ≥ 0.95` for any SEAL path. Skills with `pass_rate < 0.95` → return to draft.

## §2. LINT — Trigger Validation

### Lint Level Classification

*   **`L1: Stylistic` (Wording Clarity):**
    *   Descriptions slightly wordy or triggers phrased passively.
    *   *Result:* Warning issued; suggestion provided.

*   **`L2: Behavioral Risk` (Missing Negatives):**
    *   Skill lacks a robust "Do not use when" block with at least 3 exclusion boundaries.
    *   *Result:* Block validation; requires prompt adjustments.

*   **`L3: Safety Risk` (Constitutional Breaches):**
    *   Skill performs irreversible state writes, manages sensitive secrets, or coordinates destructive operations without declaring an integration path to arifos-governance and 888_HOLD gates.
    *   *Result:* **HARD BLOCK**. Requires arifos-governance human release (888 HOLD) to override.

### Lint Procedure

1. **Strict Trigger Parsing:** Extract the `Use When` and `Do Not Use When` blocks
2. **Vague Verb Scanning:** Scan for banned words: *"help"*, *"assist"*, *"improve"*, *"manage"*, *"optimize"*, *"support"*. Require explicit action verbs.
3. **Trigger Count Validation:** `Use when` must have 3-7 concrete triggers; `Do not use when` must have ≥3 exclusion rules
4. **Lint Level Classification:** Assess for L1, L2, or L3 violations
5. **888 HOLD Enforcement:** If L3 violation found, lock the build pipeline, generate `ERR_LINT_L3_VIOLATION` ticket
6. **Lint Status Output:** Output failures, warnings, and recommended revisions with exact line references

## §3. SCAFFOLD — Interactive Creation

### Step 1: Gather Information

Ask the user one at a time:
1. **Skill name** — lowercase letters, digits, hyphens only. 2-64 characters.
2. **Scope** — Project (`<repo-root>/.grok/skills/<name>/SKILL.md`) or User (`~/.grok/skills/<name>/SKILL.md`)
3. **What it should do** — describe the workflow, paste an example prompt, or explain the task

### Step 2: Draft Description

Write a `description` frontmatter value that includes:
- What the skill does (1-2 sentences)
- Trigger phrases and keywords for auto-invocation
- The slash command name

### Step 3: Create Directory & Write SKILL.md

```bash
mkdir -p <SKILL_DIR>
```

Write SKILL.md following the exact format:
```
---
name: <skill-name>
description: <the description>
---

<markdown body with instructions, steps, code blocks>
```

### Step 4: Verify and Confirm

1. Verify the file was written correctly
2. Tell the user how to use it: slash command, TUI menu, or automatic invocation

## Guidelines

- Keep the SKILL.md body focused and actionable — it is a prompt for the agent, not documentation
- The `description` field is critical — it controls auto-invocation
- Prefer referencing existing CLI tools over writing custom scripts
- Always use absolute paths when creating files
- Do NOT skip creating the directory

## Postconditions

1. A valid skill structure (including SKILL.md) is staged in the target folder
2. The skill complies with baseline structural layout standards
3. The Floor-Tier SEAL Gate was observed
4. All trigger clauses pass L1-L3 compliance

## Failure Modes & Escalation

*   **Intent Ambiguity:** User request too vague. *Action:* Pause and present clarifying questions.
*   **Missing Exclusion Block:** Skill lacks "Do Not Use When" section. *Action:* Flag L2, suggest 3 templates, block merging.
*   **Verbal Overload:** Triggers in vague prose. *Action:* Auto-format into short, bulleted imperative clauses.

## Telemetry per Run

```json
{
  "skill_name": "skill-creator",
  "version": "2.0.0",
  "floor_tier_reached": "<F1|F2|F5>",
  "sealing_authority": "<888|human|autonomous>",
  "grader_pass_rate": 0.0,
  "lint_level": "<L1|L2|L3|PASS>",
  "human_approval_required": false,
  "hold_code": "<if applicable>"
}
```
