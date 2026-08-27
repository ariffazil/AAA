# Skill Trigger Linter — OpenCode Adapter

> **Canonical:** `skills/skill-trigger-linter/SKILL.md` | **Risk:** low

Check every skill’s “use when” and “do not use when” clauses for collisions, missing negatives, and vague verbs like “help,” “assist,” or “improve.” Load when linting, reviewing, or validating trigger boundaries.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "skill-trigger-linter": {
      "description": "Check every skill\u2019s \u201cuse when\u201d and \u201cdo not use when\u201d clauses for collisions, missing negatives, and vague verbs like \u201chelp,\u201d \u201cassist,\u201d or \u201cimprove.\u201d Load when linting, reviewing, or validating trigger boundaries.",
      "risk_tier": "low",
      "canonical_skill": "skills/skill-trigger-linter/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
