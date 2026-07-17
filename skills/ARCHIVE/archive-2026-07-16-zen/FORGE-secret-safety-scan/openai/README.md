# Secret Safety Scan — OpenAI / Codex Adapter

> **Canonical:** `skills/secret-safety-scan/SKILL.md`  
> **Risk tier:** critical | Tools: grep, file-read, git-log

Scan a repo or workspace for exposed secrets, tokens, keys, and credentials. Produce a findings report with remediation steps.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "secret_safety_scan",
    "description": "Scan a repo or workspace for exposed secrets, tokens, keys, and credentials. Produce a findings report with remediation steps.",
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
