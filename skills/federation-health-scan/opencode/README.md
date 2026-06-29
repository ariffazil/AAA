# Federation Health Scan — OpenCode Adapter

> **Canonical:** `skills/federation-health-scan/SKILL.md` | **Risk:** low

Legacy single-command federation health diagnostic (organs, NATS, drift, vault). Superseded by service-health-triage.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "federation-health-scan": {
      "description": "Legacy single-command federation health diagnostic (organs, NATS, drift, vault). Superseded by service-health-triage.",
      "risk_tier": "low",
      "canonical_skill": "skills/federation-health-scan/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
