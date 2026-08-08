# Parallel Authority Detection — OpenCode Adapter

> **Canonical:** `skills/parallel-authority-detection/SKILL.md` | **Risk:** high

Detect when two or more repos claim the same authority, responsibility, or canonical source of truth. Resolve conflicts through ROOT_CANON.yaml precedence.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "parallel-authority-detection": {
      "description": "Detect when two or more repos claim the same authority, responsibility, or canonical source of truth. Resolve conflicts through ROOT_CANON.yaml precedence.",
      "risk_tier": "high",
      "canonical_skill": "skills/parallel-authority-detection/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
