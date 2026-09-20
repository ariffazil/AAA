<!-- PROVENANCE: member "skill-creator" folded into umbrella "skill-mesh" (merge-20260920, 2026-09-20) -->
<!-- original path: /root/AAA/skills/engineering/skill-creator/SKILL.md -->
<!-- archived at: /root/AAA/skills/.archive/merge-20260920/skill-mesh/skill-creator/ (body below is byte-identical to the archived original) -->
<!-- sha256 of the body below: 078dd236cf5f7cdf05d08a032ee8331e44e845db588a2eafbe0c0bb202ac6cb4 -->
---
name: skill-creator
id: skill-creator
version: 2.0.0
description: "Create, lint, and package new skills."
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

## Federation Write Gate — critical-variable vocabulary (arifOS)

A pre-tool hook intercepts calls before they run. It does not read intent — it greps the serialized
tool input. Reference source: `/root/AAA/federation/protocols/arifos-hermes-gate-hook.py`
(verify the live file with `git log --oneline -3 --` on that path; a `.bak-<date>-pre-jitu` sibling
means the gate was recently edited).

**Rule:** the gate extracts a **claim surface** (only the text a human would read as an assertion),
strips URLs / receipt ids / evidence paths out of it first, and then matches the critical-variable
patterns against what remains. No match → no block. Match and no admissible evidence → **BLOCKED**,
returned as `W_SCAR HOLD`.

| Critical vocabulary (matched) |
|---|
| duit · money · bayar · bayaran · transfer · rm + digits · price · cost · budget |
| nyawa · health · ubat · dosis · medical · hospital · doktor · sakit |
| reputasi · legal · law · laws · saman · polis · court · undang |
| invest · investment · trading · xauusd · forex · leverage |

**What actually clears a HOLD — evidence, not vocabulary.** Exactly three things qualify:

1. a **URL** anywhere in the payload;
2. a **receipt / trace / envelope id** (`receipt_id: <6+ chars>` — other keys are ignored);
3. an **on-disk path that exists**, ending in `.json .jsonl .log .md .csv .parquet .db .yaml .yml`.

Note (3) carefully: the file must **exist**, and `.py` / `.sh` / `.txt` do **not** count. A path
that merely contains a trigger word is no longer scanned — that defect was fixed 2026-09-18.

**Correct response: fix the payload, never shop for an unguarded tool.** Attach a real URL or cite a
live evidence file. The gate asserts exactly the law this skill already requires: a claim about a
consequential variable carries its provenance in the same breath.

**Read-only terminal commands are exempt** — a command beginning with `ls`/`cat`/`grep`/`git status`/
`curl`/`jq`/`systemctl status` routes as a probe, not a claim. That is why inspection keeps working
during a HOLD.

**Pitfalls observed 2026-09-18.** A skill patch containing `court`, `undang` and `RM` figures but no
URL was refused three times — across `patch`, `skill_manage` and a shell command. A `Sources:` line
with real URLs to the identical content cleared it in one attempt. Separately, naming a monitor
`apex-court` made *every later command referencing it* fail, because the id itself carried the trigger
substring; renaming the id was the fix. **Do not retry the same payload** — the check is
deterministic; only the payload changed. And do not name artefacts after trigger words: prefer
`apex-pda` over anything containing the word the gate hunts.

**This gate is under active development.** It was rewritten in place at 08:57 on 2026-09-18 —
mid-session, while this very note was being written — moving from word-level source indicators to the
claim-surface + existing-evidence model above. Before relying on any of this, re-read the live file
`/root/AAA/federation/protocols/arifos-hermes-gate-hook.py`, and check its mtime against the present
time. Live state that the gate itself consults: `/root/.hermes/cron/sentinel/state.json`.

**Name resolution trap:** when two skills share a name in different roots, `skill_manage` resolves by
NAME across all roots, not by the path you read. Patching "the file you just read" can therefore fail
with a no-match error against an entirely different file. Resolve the path with
`find /root/.hermes/skills /root/AAA/skills -name SKILL.md -path '*<name>*'` before editing.

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
