# Spawn Enums — Canonical Cross-Harness Template

> Source: `/root/AAA/federation/protocols/spawn_enums.json`
> Generated from: Kimi spawn_protocol_v0.1.0 + Hermes golden test + Arif PARTIAL-SEAL directive (2026-08-07)
> Purpose: Canonical enum source that all 3 harnesses (OpenCode, Kimi Code, Hermes) MUST reference

## Why this file exists

Before this session, the three harnesses (OpenCode, Kimi Code, Hermes) each drafted their own spawn contract shape. They converged on A1-A7 (spawn_reason + risk_tier + archetype + structured return + adversarial + judgment coverage + provenance + entropy gate), but with **different specifics**:

- Hermes used 5 spawn_reason values
- Kimi used 7 (added implementation, refactor)
- OpenCode had no structured spawn contract at all

Same architecture, three different enums. **Drift waiting to happen.**

This file is the **single source of truth** that all three should load.

## Schema (canonical)

```json
{
  "_meta": { "version": "0.1.0", "status": "PARTIAL_SEAL" },

  "spawn_reason": [
    "verification", "criticism", "synthesis", "reconnaissance",
    "domain_analysis", "implementation", "refactor"
  ],

  "risk_tier": {
    "T1": { "label": "read-only", "judge_required": false, "auto_execute": true },
    "T2": { "label": "recommendation", "judge_required": true, "auto_execute": false },
    "T3": { "label": "mutation", "judge_required": true, "auto_execute": false }
  },

  "archetype_ceilings": {
    "OpenCode_333AGI": { "333-AGI": { "ceiling": "EXECUTE_AFTER_SEAL", "max_confidence": 0.90 } },
    "Kimi_af": { "af-explore": { "ceiling": "OBSERVE_ONLY", "max_confidence": 0.60 } },
    "Hermes": { "SCOUT": { "ceiling": "OBSERVE_ONLY", "max_confidence": 0.70 } }
  },

  "judgment_coverage_formula": {
    "formula": "min(apex_verdicts_sought / max(risky_actions_taken, 1), 1.0)",
    "telemetry_fields": {
      "mutations_taken": "int",
      "recommendations_made": "int",
      "conclusions_reached": "int",
      "risky_actions_taken": "int",
      "apex_verdicts_sought": "int",
      "judgment_coverage": "float clamped [0,1]",
      "judgment_debt": "int raw"
    }
  },

  "parallel_spawn_rule": {
    "allowed": true, "max_parallel": 3,
    "per_spawn_telemetry": true, "aggregate_seal": "dashboard_only"
  },

  "federation_invariant": "Governance is measured per spawn, never solely per task.",

  "seal_status": {
    "SEALED": "normal path",
    "UNSEALED_INFRA": "vault unavailable, NOT governance leak",
    "FAILED_VALIDATION": "constitutional rejection, IS governance leak"
  }
}
```

## Federation invariant (one sentence, sealed)

> **Governance is measured per spawn, never solely per task.**

Aggregate telemetry may summarize for dashboard. Aggregate telemetry may not replace spawn-level telemetry.

## Per-spawn telemetry fields (mandatory)

```yaml
spawn:
  id, parent_spawn_id, archetype, spawn_reason, risk_tier, expected_entropy_reduction

telemetry:
  mutations_taken, recommendations_made, conclusions_reached,
  risky_actions_taken, apex_verdicts_sought,
  judgment_coverage (clamped), judgment_debt (raw)

seal:
  status [SEALED | UNSEALED_INFRA | FAILED_VALIDATION],
  vault_receipt_id

receipt:
  parent_spawn_hash, receipt_hash
```

## Per-archetype confidence caps (canonical)

| Archetype | Cap | Rationale |
|---|---|---|
| af-explore | 0.60 | Read-only, lowest stakes |
| af-reviewer | 0.70 | Read-only review |
| af-plan | 0.75 | Drafts plans, no execution |
| af-worker | 0.80 | Bounded execution |
| af-fix | 0.85 | Reversible execution |
| af-coordinator | 0.85 | Dispatch only |
| af-forge | 0.90 | T2-T3 with seal |
| SCOUT | 0.70 | Read-only |
| CRITIC | 0.70 | Read-only critique |
| SYNTHESIZER | 0.75 | Combines, no new facts |
| AUDITOR | 0.80 | Verifies, no recommendations |
| 333-AGI | 0.90 | Primary reasoning |
| 888-APEX | 0.90 | Constitutional verdict |

Lower for read-only. Higher for execution. **Non-negotiable.**

## Tri-state seal status

| Status | Meaning | Audit treatment |
|---|---|---|
| `SEALED` | Constitutional seal applied | Normal |
| `UNSEALED_INFRA` | Receipt valid, vault unavailable | Infrastructure failure — retry, NOT a leak |
| `FAILED_VALIDATION` | Receipt rejected | **IS a governance leak — investigate** |

Rule: **Do not punish governance for infrastructure failure.**

## What this file is NOT

- Not the spawn validator (that's separate code)
- Not the enforcement hook (that's separate infrastructure)
- Not the telemetry storage (that's separate backend)

This file is **the enum source of truth** that all those other things should reference.

## How to extend

If you add a new archetype or spawn_reason value:
1. Update `spawn_enums.json` (canonical)
2. Re-verify Kimi / Hermes / OpenCode configs match
3. Update cross-harness alignment audit (`federation-level-enforcement-gap.md`)
4. Document in changelog (`spawn_enums_changelog_YYYY-MM-DD.md`)

If you change a confidence cap:
1. Update `archetype_confidence_caps`
2. Confirm reasoning in changelog
3. Update any per-archetype override configs (otherwise they drift)

## Related

- `governance-contract-self-audit/SKILL.md` — how to write the contracts this file references
- `governance-contract-self-audit/references/federation-level-enforcement-gap.md` — full cross-harness alignment status
- `agent-config-validation/SKILL.md` — config schema validation that may surface enum drift
- Canonical file: `/root/AAA/federation/protocols/spawn_enums.json`