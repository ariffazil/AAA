---
name: arifos-plan-dag
description: Build multi-step execution graphs, dependency-aware subtasks, checkpoints, and rollback points. Load when tasks exceed one-shot prompting and need subagent or staged execution.
---

# arifos-plan-dag (O_Ω Orchestration Layer)

## Purpose
Build multi-step execution graphs, coordinate dependency-aware subtasks, establish checkpoints, and define rollback boundaries.

## Use When
1. A complex user request requires multi-step orchestration that cannot be solved in a single turn.
2. Generating a structured task list (`task.md`) that requires mapping explicit parent-child task nodes.
3. Spawning and coordinating multiple parallel subagent runs (e.g. baseline vs variant evaluations).
4. Defining safe execution checkpoints and rollback points for highly sensitive workspace mutations.
5. Annotating plan nodes with specific L2 skills required and verification criteria expected.

## Do Not Use When
1. Executing a minor, simple task that requires less than 3 sequential commands or edits.
2. Compiling quantitative traces of past executions (use `arifos-evals` or `arifos-observability` instead).
3. The task requires structural changes to a specific tool's internal database code.

## Inputs
*   **Complex Intent:** The user's multi-dimensional request payload.
*   **Skill Registry:** Mapping of active L2 skills and their dependencies.
*   **System Constraints:** Active token envelopes, step counts, and timing budgets.

## Procedure
1.  **DAG Generation:** Breakdown the complex request into discrete task nodes. Map explicit dependencies (edges) between them.
2.  **Node Annotation:** For each task node, specify:
    *   *Assigned Substrate:* The specific tool, script, or L2 skill that will execute this node.
    *   *Inputs/Outputs:* Mapped parameters and expected file schemas.
    *   *Verification Criteria:* Observable postconditions required to pass the node.
3.  **Governance Inspection:** Query `arifos-governance` to scan the planned DAG. Automatically insert `888_HOLD` pause blocks at high-risk nodes (e.g., destructive commands or deployments).
4.  **Sequential/Parallel Execution:** Coordinate execution of independent nodes in parallel, while forcing dependent nodes to execute in order.
5.  **Checkpoint Management:** Before executing a node with a high risk score, create an automatic checkpoint (git branch, database backup, or local directory snapshot).
6.  **Rollback Routing:** If a node verification fails, immediately trigger a rollback to the closest parent checkpoint, log the failure, and degrade to safe mode.

## Postconditions
1.  A complete directed acyclic graph (PlanDAG) is mapped and validated.
2.  High-risk nodes are successfully gated by verified governance approvals.
3.  State transitions are guaranteed to rollback cleanly if subsequent nodes fail.

## Failure Modes & Escalation
*   **Dependency Loop:** The generated DAG contains a circular dependency (e.g. Node A depends on B, which depends on A). *Action:* Break loop immediately, restructure into linear phases, and log warning.
*   **State Drift:** A rollback fails to restore the workspace to the exact checkpoint state. *Action:* Refuse to proceed, enter hard `888_HOLD` mode, write `ERR_DAG_STATE_DRIFT`, and alert the Sovereign.

## Telemetry per Run
```json
{
  "skill_name": "arifos-plan-dag",
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
*   **Task Completion Rate:** [0.0 - 1.0] (Target: >0.98)
*   **Rollback Safety:** [0.0 - 1.0] (Target: 1.00)
*   **Context Efficiency:** [0.0 - 1.0] (Target: >0.90)
*   **Doc Freshness:** [0.0 - 1.0] (Target: 1.00)
*   **Cross-Skill Collision Rate:** [0.0 - 1.0] (Target: <0.02)
*   **Human Trust Score:** [0.0 - 1.0] (Target: >0.98)
