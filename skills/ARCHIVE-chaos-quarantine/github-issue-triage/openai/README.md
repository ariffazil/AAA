# GitHub Issue Triage — OpenAI / Codex Adapter

> **Canonical:** `skills/github-issue-triage/SKILL.md`  
> **Risk tier:** medium | Tools: forge_github_search, forge_github_pr, forge_filesystem_read

Governed triage workflow for GitHub issues across the arifOS federation. Use this skill whenever a new issue is opened, an issue lacks labels, or an agent needs to determine if it belongs in a different repo or federation organ. This skill classifies, routes, labels, and drafts responses — but never closes, never assigns to Arif, and never promises code fixes without sovereign approval.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "github_issue_triage",
    "description": "Governed triage workflow for GitHub issues across the arifOS federation. Use this skill whenever a new issue is opened, an issue lacks labels, or an agent needs to determine if it belongs in a different repo or federation organ. This skill classifies, routes, labels, and drafts responses \u2014 but never closes, never assigns to Arif, and never promises code fixes without sovereign approval.",
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
