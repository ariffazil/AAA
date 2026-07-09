# OpenClaw A2A Bridge — OpenAI / Codex Adapter

> **Canonical:** `skills/openclaw-a2a-bridge/SKILL.md`  
> **Risk tier:** medium | Tools: agent-dispatch, agent-handoff, status-query

Governed A2A bridge skill for OpenClaw-facing handoff and dispatch. Legacy skill — retained for workflow compatibility.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "openclaw_a2a_bridge",
    "description": "Governed A2A bridge skill for OpenClaw-facing handoff and dispatch. Legacy skill \u2014 retained for workflow compatibility.",
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
