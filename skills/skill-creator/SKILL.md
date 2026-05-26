---
name: skill-creator
description: Bootstrap, design, and package new skills. Load when capturing user intent for a new skill or drafting its initial instruction framework.
---

# skill-creator (O_Ψ Verification Layer)

## Purpose
Bootstrap, design, and package new skills.

## Use When
1. Capturing user intent for a brand new skill from conversation history.
2. Conducting interviews to identify edge cases, input/output requirements, and dependencies for a new skill.
3. Drafting the initial structure, frontmatter, and instructions for a new `SKILL.md` file.
4. Packaging finished skill folders into `.skill` distributables.

## Do Not Use When
1. Auditing the active skill portfolio for collisions or stale documentation (use `arifos-recursive-audit` instead).
2. Running quantitative benchmarks or evaluating prompt traces (use `arifos-evals` instead).
3. Linting trigger names or checking vague verb usage (use `skill-trigger-linter` instead).

## Inputs
*   **User Concept:** The high-level intent or workflow specified by the user.
*   **System Target:** The proposed skill workspace directory.

## Procedure
1.  **Capture Intent:** Analyze the user request and extract target tools, sequence steps, and expected outputs.
2.  **Define Trigger Boundaries:** Design preliminary "Use when" and "Do not use when" rules.
3.  **Draft SKILL.md:** Compose the frontmatter, purpose, triggers, inputs, procedure, postconditions, failure modes, and telemetry structure.
4.  **Verification Setup:** Propose 2-3 realistic test prompts for verification.
5.  **Package Skill:** Run `scripts/package_skill.py` to compile the folder structure into a distributable package.

## Postconditions
1.  A valid skill structure (including `SKILL.md`) is successfully staged in the target folder.
2.  The skill complies with the baseline structural layout standards.
3.  The package is compiled without system compile errors.

## Failure Modes & Escalation
*   **Intent Ambiguity:** The user request is too vague to extract structured boundaries. *Action:* Pause generation and present clarifying questions regarding concrete tools and expected formats.

## Telemetry per Run
```json
{
  "skill_name": "skill-creator",
  "version": "1.0.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "commands_run": 0,
  "artifacts_written": 1,
  "postcondition_pass": false,
  "human_approval_required": false,
  "hold_code": "{{hold_code}}"
}
```

## Recursive Scorecard
*   **Activation Precision:** [0.0 - 1.0] (Target: >0.95)
*   **Task Completion Rate:** [0.0 - 1.0] (Target: >0.95)
*   **Rollback Safety:** [0.0 - 1.0] (Target: 1.00)
*   **Context Efficiency:** [0.0 - 1.0] (Target: >0.90)
*   **Doc Freshness:** [0.0 - 1.0] (Target: 1.00)
*   **Cross-Skill Collision Rate:** [0.0 - 1.0] (Target: 0.00)
*   **Human Trust Score:** [0.0 - 1.0] (Target: >0.98)
