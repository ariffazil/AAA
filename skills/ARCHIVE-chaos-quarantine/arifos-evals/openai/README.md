# arifOS Evals — OpenAI / Codex Adapter

> **Canonical:** `skills/arifos-evals/SKILL.md`  
> **Risk tier:** low | Tools: see canonical

Run benchmark prompts, collect pass/fail traces, latency, token cost, and false activation rates for each skill. Load when a skill changes behavior or a new version is proposed.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "arifos_evals",
    "description": "Run benchmark prompts, collect pass/fail traces, latency, token cost, and false activation rates for each skill. Load when a skill changes behavior or a new version is proposed.",
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
