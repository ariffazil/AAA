# arifOS Plan DAG — OpenAI / Codex Adapter

> **Canonical:** `skills/arifos-plan-dag/SKILL.md`  
> **Risk tier:** medium | Tools: see canonical

Build multi-step execution graphs, dependency-aware subtasks, checkpoints, and rollback points. Load when tasks exceed one-shot prompting and need subagent or staged execution.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "arifos_plan_dag",
    "description": "Build multi-step execution graphs, dependency-aware subtasks, checkpoints, and rollback points. Load when tasks exceed one-shot prompting and need subagent or staged execution.",
    "parameters": {
      "type": "object",
      "properties": {
        "context": {
          "type": "string",
          "description": "Brief context for this skill invocation"
        }
      },
      "required": []
    }
  }
}
```

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
