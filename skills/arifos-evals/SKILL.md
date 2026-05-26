---
name: arifos-evals
description: Run benchmark prompts, collect pass/fail traces, latency, token cost, and false activation rates for each skill. Load when a skill changes behavior or a new version is proposed.
---

# arifos-evals (O_Ω Constitutional Layer)

## Purpose
Run benchmark prompts, collect pass/fail traces, latency, token cost, and false activation rates for each skill.

## Use When
1. Evaluating a newly proposed skill draft against a baseline (without skill).
2. Benchmarking the performance delta of a modified skill against its original version.
3. Conducting quantitative checks on response times, token efficiency, and execution costs.
4. Running automated trigger evaluation queries to calculate precision and recall.
5. Optimizing a skill's description using programmatic feedback loops.

## Do Not Use When
1. Linting triggers for vague verbs or formatting collisions (use `skill-trigger-linter` instead).
2. Performing generic codebase audits or links validation (use `arifos-recursive-audit` instead).
3. The task requires structural design changes to a skill's logic.

## Inputs
*   **Skill Draft:** The `SKILL.md` file proposed for evaluation.
*   **Test Config:** A JSON file containing benchmark prompts and expected outputs (e.g. `evals.json`).
*   **Baseline Snapshot:** The original skill version or empty state folder.

## Operational Lifecycle Phases

The evaluation flow is split into two explicit operational phases:

### Phase 1: The Design Phase
*   **Intent:** Establish the parameters, axes, and contexts of the test suite.
*   **Actions:**
    *   Define evaluation axes (precision, latency, token drift, rollback safety).
    *   Assemble a curated, diverse set of test queries.
    *   Set up baseline and variant configuration definitions.
    *   Initialize the metrics target directory (`<skill-name>-workspace/iteration-N/`).

### Phase 2: The Execution Phase
*   **Intent:** Trigger the evaluations, record telemetry, programmatically grade the outputs, and generate aggregated benchmarks.
*   **Actions:**
    *   Spawn parallel execution subagent tasks.
    *   Measure and capture timing logs (`timing.json`).
    *   Verify assertions and write the results to `grading.json`.
    *   Aggregate metrics into `benchmark.json` and generate reports.

## DevBench-Aligned Metrics Schema
The output file `benchmark.json` must classify every execution using standardized taxonomy:
*   **`scenario_category`:** The high-level framework class (e.g. `infrastructure_deployment`, `domain_petrophysics`, `governance_verification`).
*   **`context_length`:** Input character/token weight category (`short` < 4K, `medium` 4K-16K, `long` > 16K).
*   **`task_type`:** The reasoning dialect of the prompt (`code_generation`, `ast_parsing`, `decision_reasoning`, `syntactic_lint`).
*   **`metrics`:** Nested performance counts:
    ```json
    {
      "pass_rate": 0.0,
      "latency_ms": 0,
      "token_in": 0,
      "token_out": 0,
      "false_activation": false,
      "rollback_triggered": false
    }
    ```

## Procedure
1.  **Phase 1 (Design):** Establish test configs, select baseline variant, and define standard `scenario_category` tags.
2.  **Phase 2 (Execution):** Trigger the parallel run suite under iteration directories.
3.  **Timing Capture:** Record `timing.json` immediately upon task completion.
4.  **Assertion Grading:** Validate outputs programmatically against expected invariants and write to `grading.json`.
5.  **Benchmark Compilation:** Aggregate results using the **DevBench-Aligned Metrics Schema** and output to `benchmark.json`.

## Postconditions
1.  A valid `benchmark.json` with standardized category tags is generated in the workspace.
2.  Pass/fail comparisons are programmatically graded and saved.
3.  Evaluation results do not mix lab-synthetic data with online field telemetry.

## Failure Modes & Escalation
*   **Execution Timeout:** Parallel subagents hang or fail to return timing data. *Action:* Terminate execution, record a fail grade, and list the step limit as exceeded.
*   **Grader Divergence:** Quantitative grades differ from manual human feedback. *Action:* Flag the assertions as ambiguous and request manual grading override.

## Telemetry per Run
```json
{
  "skill_name": "arifos-evals",
  "version": "1.1.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "selected_branch": "iteration-{{N}}",
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
*   **Activation Precision:** [0.0 - 1.0] (Target: >0.95)
*   **Task Completion Rate:** [0.0 - 1.0] (Target: >0.98)
*   **Rollback Safety:** [0.0 - 1.0] (Target: 1.00)
*   **Context Efficiency:** [0.0 - 1.0] (Target: >0.90)
*   **Doc Freshness:** [0.0 - 1.0] (Target: 1.00)
*   **Cross-Skill Collision Rate:** [0.0 - 1.0] (Target: 0.00)
*   **Human Trust Score:** [0.0 - 1.0] (Target: >0.98)
