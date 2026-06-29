# Federation Health Scan — OpenAI / Codex Adapter

> **Canonical:** `skills/federation-health-scan/SKILL.md`  
> **Risk tier:** low | Tools: see canonical

Legacy single-command federation health diagnostic (organs, NATS, drift, vault). Superseded by service-health-triage.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "federation_health_scan",
    "description": "Legacy single-command federation health diagnostic (organs, NATS, drift, vault). Superseded by service-health-triage.",
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
