# arifOS Recursive Audit — OpenCode Adapter

> **Canonical:** `skills/arifos-recursive-audit/SKILL.md` | **Risk:** medium

Audit all installed skills for overlap, stale docs, prompt bloat, trigger ambiguity, and broken references. Load when reviewing the skill portfolio or after modifying or adding new skills.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "arifos-recursive-audit": {
      "description": "Audit all installed skills for overlap, stale docs, prompt bloat, trigger ambiguity, and broken references. Load when reviewing the skill portfolio or after modifying or adding new skills.",
      "risk_tier": "medium",
      "canonical_skill": "skills/arifos-recursive-audit/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
