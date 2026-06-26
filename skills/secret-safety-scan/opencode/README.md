# Secret Safety Scan — OpenCode Adapter

> **Canonical:** `skills/secret-safety-scan/SKILL.md` | **Risk:** high

Scan a repo or workspace for exposed secrets, tokens, keys, and credentials. Produce a findings report with remediation steps.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "secret-safety-scan": {
      "description": "Scan a repo or workspace for exposed secrets, tokens, keys, and credentials. Produce a findings report with remediation steps.",
      "risk_tier": "high",
      "canonical_skill": "skills/secret-safety-scan/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
