# Code Wiki — Codebase Documentation Generator — OpenAI / Codex Adapter

> **Canonical:** `skills/code-wiki/SKILL.md`  
> **Risk tier:** low | Tools: see canonical

Generate structured wiki docs, module maps, and Mermaid diagrams for unfamiliar codebases.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "code_wiki",
    "description": "Generate structured wiki docs, module maps, and Mermaid diagrams for unfamiliar codebases.",
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
