# Repository Hygiene Audit — OpenAI / Codex Adapter

> **Canonical:** `skills/repo-hygiene-audit/SKILL.md`  
> **Risk tier:** medium | Tools: github-search, file-read, directory-list

Inspect a GitHub repo for structural chaos, authority conflicts, and cleanup needs. Produce an audit report and remediation plan.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "repo_hygiene_audit",
    "description": "Inspect a GitHub repo for structural chaos, authority conflicts, and cleanup needs. Produce an audit report and remediation plan.",
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
