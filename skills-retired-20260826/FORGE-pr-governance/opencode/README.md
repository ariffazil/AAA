# PR Review Governance — OpenCode Adapter

> **Canonical:** `skills/pr-review-governance/SKILL.md` | **Risk:** high

High-level governance layer for pull request review across the federation. Ensures separation of duties, required signers, and constitutional compliance before merge. This is the **policy layer** that decides who must approve. The **checklist** lives in `github-pr-review`; do not duplicate it here.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "pr-review-governance": {
      "description": "High-level governance layer for pull request review across the federation. Ensures separation of duties, required signers, and constitutional compliance before merge. This is the **policy layer** that decides who must approve. The **checklist** lives in `github-pr-review`; do not duplicate it here.",
      "risk_tier": "high",
      "canonical_skill": "skills/pr-review-governance/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
