# arifOS Evals — OpenCode Adapter

> **Canonical:** `skills/arifos-evals/SKILL.md` | **Risk:** low

Run benchmark prompts, collect pass/fail traces, latency, token cost, and false activation rates for each skill. Load when a skill changes behavior or a new version is proposed.

## OpenCode Agent Config Fragment

```json
{
  "agents": {
    "arifos-evals": {
      "description": "Run benchmark prompts, collect pass/fail traces, latency, token cost, and false activation rates for each skill. Load when a skill changes behavior or a new version is proposed.",
      "risk_tier": "low",
      "canonical_skill": "skills/arifos-evals/SKILL.md"
    }
  }
}
```

Trigger conditions and full procedure: `skills/{sid}/SKILL.md`

---
*DITEMPA BUKAN DIBERI — arifOS Federation*
