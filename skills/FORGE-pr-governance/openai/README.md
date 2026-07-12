# PR Review Governance — OpenAI / Codex Adapter

> **Canonical:** `skills/pr-review-governance/SKILL.md`  
> **Risk tier:** high | Tools: forge_github_pr, forge_github_search

High-level governance layer for pull request review across the federation. Ensures separation of duties, required signers, and constitutional compliance before merge. This is the **policy layer** that decides who must approve. The **checklist** lives in `github-pr-review`; do not duplicate it here.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "pr_review_governance",
    "description": "High-level governance layer for pull request review across the federation. Ensures separation of duties, required signers, and constitutional compliance before merge. This is the **policy layer** that decides who must approve. The **checklist** lives in `github-pr-review`; do not duplicate it here.",
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
