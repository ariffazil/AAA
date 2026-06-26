# GitHub Issue Triage — OpenCode Adapter

> **Canonical:** `skills/github-issue-triage/SKILL.md` | **Risk:** medium

Governed triage workflow for GitHub issues across the arifOS federation. Use this skill whenever a new issue is opened, an issue lacks labels, or an agent needs to determine if an issue belongs in a different repo or federation organ. This skill classifies, routes, labels, and drafts responses — but never closes, never assigns to Arif, and never promises code fixes without sovereign approval.


## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "github-issue-triage": {
      "description": "Governed triage workflow for GitHub issues across the arifOS federation. Use this skill whenever a new issue is opened, an issue lacks labels, or an agent needs to determine if an issue belongs in a different repo or federation organ. This skill classifies, routes, labels, and drafts responses \u2014 but never closes, never assigns to Arif, and never promises code fixes without sovereign approval.\n",
      "risk_tier": "medium",
      "canonical_skill": "skills/github-issue-triage/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
