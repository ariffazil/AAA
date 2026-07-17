---
id: skill-trigger-linter
name: FORGE-skill-linter
version: 1.0.0
description: Check every skill’s “use when” and “do not use when” clauses for collisions,
  missing negatives, and vague verbs like “help,” “assist,” or “improve.” Load when
  linting, reviewing, or validating trigger boundaries.
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
  skills:
  - arifos-recursive-audit
  servers: []
  tools: []
examples:
- Lint a new skill for vague verbs like 'help' or 'improve'
- Validate that a skill has at least 3 'Do not use when' rules
tests:
- Skill missing exclusion block flagged L2
- Skill with irreversible writes and no governance path flagged L3
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Governance
  layer: HEXAGON
  autonomy_tier: T1
floor_scope:
- F2
- F4
- F7
- F9
- F10
- F11
---

# skill-trigger-linter (O_Ψ Verification Layer)

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


## Purpose
Check every skill’s “use when” and “do not use when” clauses for collisions, missing negatives, and vague verbs like “help,” “assist,” or “improve.”

## Use When
1. Validating the frontmatter descriptions and target boundaries of any skill.
2. Trigger drift is observed (e.g. `wrangler` is activated for generic coding, or `cloudflare` conflicts with `durable-objects`).
3. Preparing to optimize a skill's description using the `run_loop.py` evaluator.
4. Integrating or linting a newly forged skill prior to production staging.

## Do Not Use When
1. Performing programmatic runtime execution benchmark testing (use `arifos-evals` instead).
2. Auditing broad system dependency health or links status (use `arifos-recursive-audit` instead).
3. The task requires structural design changes to a skill's workflow.

## Inputs
*   **SKILL.md Text:** The raw contents of the skill markdown contract.
*   **Active Trigger Registry:** A mapping of all currently registered skill frontmatter descriptions.

## Lint Level Classification
The trigger linter categorizes violations into three distinct urgency thresholds:

*   **`L1: Stylistic` (Wording Clarity):**
    *   Occurs when descriptions are slightly wordy or triggers are phrased passively.
    *   *Result:* Warning issued; suggestion provided. Simple correction path.
*   **`L2: Behavioral Risk` (Missing Negatives):**
    *   Occurs when a skill lacks a robust, distinct `"Do not use when"` block containing at least 3 exclusion boundaries.
    *   *Result:* Block validation; requires prompt adjustments before merging.
*   **`L3: Safety Risk` (Constitutional Breaches):**
    *   Occurs when a skill performs irreversible state writes, manages sensitive secrets/credentials, or coordinates destructive VPS operations *without* explicitly declaring an integration path to `arifos-governance` and `888_HOLD` gates.
    *   *Result:* **HARD BLOCK**. The skill cannot be packaged or committed to the active repository. **Requires arifos-governance human release (888 HOLD)** to override and authorize deployment.

## Procedure
1.  **Strict Trigger Parsing:** Extract the `Use When` and `Do Not Use When` blocks from the target skill's body.
2.  **Vague Verb Scanning:** Scan files for banned words including *"help"*, *"assist"*, *"improve"*, *"manage"*, *"optimize"*, and *"support"*. Require explicit action verbs.
3.  **Trigger Count Validation:** Check that `Use when` contains between 3 to 7 concrete triggers, and `Do not use when` contains at least 3 distinct exclusion rules.
4.  **Lint Level Classification tagging:** Assess the parsed contract for L1, L2, or L3 violations.
5.  **888 HOLD Enforcement:** If an unresolved L3 violation is found, automatically lock the build pipeline, generate an `ERR_LINT_L3_VIOLATION` ticket, and escalate to the operator console.
6.  **Lint Status Output:** Output lint failures, warnings, and recommended prompt revisions with exact line references.

## Postconditions
1.  All target skill descriptions are checked for L1-L3 compliance.
2.  Trigger and exclusion boundaries meet the numeric target requirements.
3.  No L3 violation is allowed to pass to packaging without a verified governance key bypass.

## Failure Modes & Escalation
*   **Missing Exclusion Block:** The skill completely lacks a "Do Not Use When" section. *Action:* Flag L2 violation, suggest 3 templates, and block merging.
*   **Verbal Overload:** Triggers are written in vague prose instead of list items. *Action:* Automatically format the triggers into short, bulleted imperative clauses.

## Telemetry per Run
```json
{
  "skill_name": "skill-trigger-linter",
  "version": "1.1.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "commands_run": 0,
  "artifacts_written": 0,
  "postcondition_pass": false,
  "human_approval_required": false,
  "hold_code": "{{hold_code}}"
}
```

## Recursive Scorecard
*   **Activation Precision:** [0.0 - 1.0] (Target: >0.98)
*   **Task Completion Rate:** [0.0 - 1.0] (Target: >0.95)
*   **Rollback Safety:** [0.0 - 1.0] (Target: 1.00)
*   **Context Efficiency:** [0.0 - 1.0] (Target: >0.98)
*   **Doc Freshness:** [0.0 - 1.0] (Target: 1.00)
*   **Cross-Skill Collision Rate:** [0.0 - 1.0] (Target: 0.00)
*   **Human Trust Score:** [0.0 - 1.0] (Target: >0.98)