# arifOS Observability — OpenCode Adapter

> **Canonical:** `skills/arifos-observability/SKILL.md` | **Risk:** low

Generate structured telemetry for skill runs, including trigger source, chosen branch, command count, runtime, and postcondition checks. Load when you need to parse run logs, compile dashboards, or audit execution performance.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "arifos-observability": {
      "description": "Generate structured telemetry for skill runs, including trigger source, chosen branch, command count, runtime, and postcondition checks. Load when you need to parse run logs, compile dashboards, or audit execution performance.",
      "risk_tier": "low",
      "canonical_skill": "skills/arifos-observability/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
