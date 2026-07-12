# GitHub PR Governance Review — OpenAI / Codex Adapter

> **Canonical:** `skills/github-pr-review/SKILL.md`  
> **Risk tier:** medium | Tools: forge_github_pr, forge_filesystem_read, forge_github_search, forge_git_diff, forge_git_log, forge_git_status

Governed checklist for reviewing GitHub pull requests in the arifOS federation. Ensures PRs meet constitutional, structural, and safety standards before merge.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "github_pr_review",
    "description": "Governed checklist for reviewing GitHub pull requests in the arifOS federation. Ensures PRs meet constitutional, structural, and safety standards before merge.",
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
