# GitHub CI Diagnose — OpenCode Adapter

> **Canonical:** `skills/github-ci-diagnose/SKILL.md` | **Risk:** medium

Parse failing GitHub Actions logs, identify root cause patterns, and propose fixes without executing irreversible changes. Use this skill whenever a federation repo shows a red CI status, a workflow fails, or a build/test/lint gate breaks. This skill reads logs, classifies failure modes, and outputs a diagnostic report — it does not re-run CI, edit workflows, or dismiss security findings without sovereign approval.


## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "github-ci-diagnose": {
      "description": "Parse failing GitHub Actions logs, identify root cause patterns, and propose fixes without executing irreversible changes. Use this skill whenever a federation repo shows a red CI status, a workflow fails, or a build/test/lint gate breaks. This skill reads logs, classifies failure modes, and outputs a diagnostic report \u2014 it does not re-run CI, edit workflows, or dismiss security findings without sovereign approval.\n",
      "risk_tier": "medium",
      "canonical_skill": "skills/github-ci-diagnose/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
