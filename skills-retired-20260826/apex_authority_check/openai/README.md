# Parallel Authority Detection — OpenAI / Codex Adapter

> **Canonical:** `skills/parallel-authority-detection/SKILL.md`  
> **Risk tier:** high | Tools: github-search, file-read

Detect when two or more repos claim the same authority, responsibility, or canonical source of truth. Resolve conflicts through ROOT_CANON.yaml precedence.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "parallel_authority_detection",
    "description": "Detect when two or more repos claim the same authority, responsibility, or canonical source of truth. Resolve conflicts through ROOT_CANON.yaml precedence.",
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
