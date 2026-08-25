# README Truth Check — OpenAI / Codex Adapter

> **Canonical:** `skills/readme-truth-check/SKILL.md`  
> **Risk tier:** low | Tools: file-read, directory-list

Verify that a repo's README accurately describes its current structure, ports, dependencies, and authority boundaries. Detect drift between docs and reality.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "readme_truth_check",
    "description": "Verify that a repo's README accurately describes its current structure, ports, dependencies, and authority boundaries. Detect drift between docs and reality.",
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
