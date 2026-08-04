# arifOS Observability — OpenAI / Codex Adapter

> **Canonical:** `skills/arifos-observability/SKILL.md`  
> **Risk tier:** low | Tools: see canonical

Generate structured telemetry for skill runs, including trigger source, chosen branch, command count, runtime, and postcondition checks. Load when you need to parse run logs, compile dashboards, or audit execution performance.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "arifos_observability",
    "description": "Generate structured telemetry for skill runs, including trigger source, chosen branch, command count, runtime, and postcondition checks. Load when you need to parse run logs, compile dashboards, or audit execution performance.",
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
