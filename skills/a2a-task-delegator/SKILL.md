---
name: a2a-task-delegator
description: Standardized JSON-RPC state machine, task queue delegation, and precondition contract manager for cross-vendor multi-agent swarms.
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Agent-to-Agent (A2A) Task Delegator Skill (`a2a-task-delegator`)

Establishes standardized task delegation RPC schemas, precondition locks, and output attestation contracts for multi-agent swarms (Claude Code, Antigravity, OpenCode, Kimi, Codex).

## JSON-RPC Task Schema

```json
{
  "jsonrpc": "2.0",
  "method": "a2a.delegate_task",
  "params": {
    "task_id": "task-20260825-001",
    "assignee": "warga_ui_auditor",
    "preconditions": [
      "dist/index.html built successfully",
      "Caddy proxy active"
    ],
    "action": "run_playwright_e2e_test",
    "input_payload": {
      "target_url": "https://arif-fazil.com/earth/"
    },
    "expected_output_schema": {
      "errors_count": "number",
      "screenshot_path": "string"
    }
  },
  "id": 1
}
```

---

## Best Practices for Federation Agents

1. **State Locking**: Acquire state lock before starting a task to prevent race conditions across parallel agent runs.
2. **Attestation Receipt**: Output completed task receipt with execution hash and status (`SEAL`, `HOLD`, `FAIL`).
