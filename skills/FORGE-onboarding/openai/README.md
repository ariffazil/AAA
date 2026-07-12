# Agent Onboarding — OpenAI / Codex Adapter

> **Canonical:** `skills/agent-onboarding/SKILL.md`  
> **Risk tier:** medium | Tools: file-write, directory-create, registry-update

Standard procedure for registering a new agent in the AAA federation. Creates agent identity directory, agent card, registry entry, and SOUL.md.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "agent_onboarding",
    "description": "Standard procedure for registering a new agent in the AAA federation. Creates agent identity directory, agent card, registry entry, and SOUL.md.",
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
