# arifOS Plan DAG — OpenCode Adapter

> **Canonical:** `skills/arifos-plan-dag/SKILL.md` | **Risk:** medium

Build multi-step execution graphs, dependency-aware subtasks, checkpoints, and rollback points. Load when tasks exceed one-shot prompting and need subagent or staged execution.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "arifos-plan-dag": {
      "description": "Build multi-step execution graphs, dependency-aware subtasks, checkpoints, and rollback points. Load when tasks exceed one-shot prompting and need subagent or staged execution.",
      "risk_tier": "medium",
      "canonical_skill": "skills/arifos-plan-dag/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
