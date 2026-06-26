# Incident Escalation Protocol — OpenAI / Codex Adapter

> **Canonical:** `skills/incident-escalation/SKILL.md`  
> **Risk tier:** critical | Tools: health-probe, telegram-send, a2a-message

Standard protocol for responding to federation incidents: service outages, security breaches, constitutional violations, or agent misbehavior.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "incident_escalation",
    "description": "Standard protocol for responding to federation incidents: service outages, security breaches, constitutional violations, or agent misbehavior.",
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
