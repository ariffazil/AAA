# GitHub CI Diagnose — OpenAI / Codex Adapter

> **Canonical:** `skills/github-ci-diagnose/SKILL.md`  
> **Risk tier:** medium | Tools: forge_filesystem_read, forge_shell_dryrun, forge_log_tail

Parse failing GitHub Actions logs, identify root cause patterns, and propose fixes without executing irreversible changes. Use this skill whenever a federation repo shows a red CI status, a workflow fails, or a build/test/lint gate breaks. This skill reads logs, classifies failure modes, and outputs a diagnostic report — it does not re-run CI, edit workflows, or dismiss security findings without sovereign approval.

## Trigger Conditions

See canonical skill → *When to Use* section.

## Tool Definition Stub

```json
{
  "type": "function",
  "function": {
    "name": "github_ci_diagnose",
    "description": "Parse failing GitHub Actions logs, identify root cause patterns, and propose fixes without executing irreversible changes. Use this skill whenever a federation repo shows a red CI status, a workflow fails, or a build/test/lint gate breaks. This skill reads logs, classifies failure modes, and outputs a diagnostic report \u2014 it does not re-run CI, edit workflows, or dismiss security findings without sovereign approval.",
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
