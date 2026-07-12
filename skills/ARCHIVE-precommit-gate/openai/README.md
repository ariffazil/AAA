# Precommit Gate — OpenAI / Codex Adapter

> **Canonical:** `skills/precommit-gate/SKILL.md`  
> **Risk tier:** medium | Tools: see canonical

Pre-commit ritual running lint, type-check, tests, constitutional surface scan, and diff review.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "precommit_gate",
    "description": "Pre-commit ritual running lint, type-check, tests, constitutional surface scan, and diff review.",
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
