---
name: FORGE-skill-creator
description: Bootstrap, design, and package new skills
version: 1.1.0
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
2. Running quantitative benchmarks or evaluating prompt traces (use `080-eval-benchmark-test` instead).
3. Linting trigger names or checking vague verb usage (use `skill-trigger-linter` instead).

## Inputs
*   **User Concept:** The high-level intent or workflow specified by the user.
*   **System Target:** The proposed skill workspace directory.

## Procedure
1.  **Capture Intent:** Analyze the user request and extract target tools, sequence steps, and expected outputs.
2.  **Define Trigger Boundaries:** Design preliminary "Use when" and "Do not use when" rules.
3.  **Draft SKILL.md:** Compose the frontmatter, purpose, triggers, inputs, procedure, postconditions, failure modes, and telemetry structure.
4.  **Verification Setup:** Propose 2-3 realistic test prompts for verification.
5.  **Floor-Tier SEAL Gate (MANDATORY — see §Floor-Tier SEAL Gate below):** Classify the drafted skill by primary floor touch. Route to the correct SEAL authority before proceeding.
6.  **Package Skill:** Run `scripts/package_skill.py` to compile the folder structure into a distributable package.

## Floor-Tier SEAL Gate (MANDATORY)

Before any newly drafted skill is sealed into the live meta-mesa-skill-atlas, the creator MUST classify the primary floor touch and route to the correct authority:

| Primary floor | SEAL authority | Action |
|---|---|---|
| **F1** (AMANAH), **F8** (GENIUS), **F13** (SOVEREIGN) | **888 mandatory** | Emit `hold_code: F1/F8/F13`. Pause. Await Arif acknowledgment. Do NOT proceed to Package without explicit "go" signal. |
| **F2** (TRUTH), **F4** (CLARITY), **F11** (AUDIT) | **Grader PASS + human sign-off** | Emit `human_approval_required: true`. Present grading.json to human. Await explicit sign-off. |
| **F5** (PEACE²), **F6** (MARUAH), **F7** (HUMILITY), **F9** (ANTI-HANTU), **F10** (ONTOLOGY) | **Grader PASS → autonomous SEAL** | Proceed to Step 6 without additional gate. Log the tier in telemetry. |

**Floor classification rule:** Use the `floor_scope` declared in the skill's own frontmatter. If no frontmatter, default to F2. If the skill touches multiple floors, use the **highest-numbered floor** as the governing tier.

**Grader output requirement:** The Grader must emit `pass_rate ≥ 0.95` for the skill to qualify for any SEAL path. Skills with `pass_rate < 0.95` → return to Step 3 (redraft).

**Verification of the Grader:** The Grader agent evaluates the skill against realistic test prompts and outputs `grading.json`. The Grader does NOT have SEAL authority. It is a quality gate, not a verdict authority. Verdict authority stays with the floor tier above.

**Telemetry update:** On reaching the Floor-Tier SEAL Gate, update the running telemetry:
```json
{
  "floor_tier_reached": "<F1|F2|F5>",
  "sealing_authority": "<888|human|autonomous>",
  "grader_pass_rate": <0.0-1.0>,
  "hold_code": "<if applicable>"
}
```

## Postconditions
1.  A valid skill structure (including `SKILL.md`) is successfully staged in the target folder.
2.  The skill complies with the baseline structural layout standards.
3.  The package is compiled without system compile errors.
4.  The Floor-Tier SEAL Gate was observed and the correct authority was used.

## Failure Modes & Escalation
*   **Intent Ambiguity:** The user request is too vague to extract structured boundaries. *Action:* Pause generation and present clarifying questions regarding concrete tools and expected formats.

## Telemetry per Run
```json
{
  "skill_name": "skill-creator",
  "version": "1.1.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "commands_run": 0,
  "artifacts_written": 1,
  "postcondition_pass": false,
  "floor_tier_reached": "{{F1|F2|F5}}",
  "sealing_authority": "{{888|human|autonomous}}",
  "grader_pass_rate": 0.0,
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
