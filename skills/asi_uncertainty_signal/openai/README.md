# Drift Response — OpenAI / Codex Adapter

> **Canonical:** `skills/drift-response/SKILL.md`  
> **Risk tier:** medium | Tools: see canonical

Legacy 5-step drift response protocol. Superseded by service-health-triage.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "drift_response",
    "description": "Legacy 5-step drift response protocol. Superseded by service-health-triage.",
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
