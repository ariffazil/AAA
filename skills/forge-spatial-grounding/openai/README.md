# Spatial Grounding — OpenAI / Codex Adapter

> **Canonical:** `skills/spatial-grounding/SKILL.md`  
> **Risk tier:** medium | Tools: see canonical

Embed VPS spatial context in agent configs — prevents spatial amnesia and SSH confusion. Grounds agents in af-forge VPS reality.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "spatial_grounding",
    "description": "Embed VPS spatial context in agent configs \u2014 prevents spatial amnesia and SSH confusion. Grounds agents in af-forge VPS reality.",
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
