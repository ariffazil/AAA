# PR Review Governance — OpenAI / Codex Adapter

> **Canonical:** `skills/pr-review-governance/SKILL.md`  
> **Risk tier:** high | Tools: github-pr-fetch, github-pr-review

High-level governance layer for pull request review across the federation. Ensures separation of duties, required signers, and constitutional compliance before merge.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "pr_review_governance",
    "description": "High-level governance layer for pull request review across the federation. Ensures separation of duties, required signers, and constitutional compliance before merge.",
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
