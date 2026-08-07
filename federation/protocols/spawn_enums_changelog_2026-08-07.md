---
name: federation-spawn-enums-changelog
status: SEALED — derived from sovereign PARTIAL-SEAL+ directive
date: 2026-08-07
source: /root/AAA/federation/protocols/spawn_enums.json
---

# Federation Spawn Enums — Changelog 2026-08-07

> Source-of-truth: `/root/AAA/federation/protocols/spawn_enums.json`
> Version: 0.1.0 (PARTIAL_SEAL)
> Authority: F13 SOVEREIGN (Arif) — PARTIAL-SEAL+ directive

---

## Federation Invariant (one sentence, sealed)

> **Governance is measured per spawn, never solely per task.**

Aggregate telemetry may summarize for dashboard. Aggregate telemetry may not replace spawn-level telemetry.

Consequence: in parallel-spawn sessions, **each spawn gets its own coverage/debt/audit record**, then aggregate is *derived_only* for dashboard purposes. A single low-coverage spawn is governance leak — aggregate cannot hide it.

Example (from directive):
```
spawn_1: coverage: 1.0
spawn_2: coverage: 0.4   <- governance leak
spawn_3: coverage: 1.0
aggregate: derived_only: true, coverage: 0.8   <- hides spawn_2 leak
```

Per-spawn for audit. Aggregate for dashboard.

---

## Tri-State Seal Status (separates constitutional from infrastructure)

| State | Meaning | Action |
|---|---|---|
| `SEALED` | Constitutional seal applied; receipt in VAULT999 | Normal path |
| `UNSEALED_INFRA` | Receipt valid but vault unavailable (downtime, quota) | Retry seal when vault recovers. **NOT** a governance leak. |
| `FAILED_VALIDATION` | Receipt rejected by constitutional validation | **IS** a governance leak. Must be investigated. |

Rule: **Do not punish governance for infrastructure failure.** Vault downtime ≠ seal failure. Audit must distinguish.

---

## Per-Spawn Telemetry Schema (canonical fields)

```yaml
spawn:
  id: <uuid>
  parent_spawn_id: <uuid or null>
  archetype: <from archetype_ceilings>
  spawn_reason: <from spawn_reason enum>
  risk_tier: [T1 | T2 | T3]
  expected_entropy_reduction: <string>

telemetry:
  mutations_taken: int
  recommendations_made: int
  conclusions_reached: int
  risky_actions_taken: int         # mutations + recommendations + conclusions
  apex_verdicts_sought: int        # restricted to T2+T3
  judgment_coverage: float         # clamped [0.0, 1.0]
  judgment_debt: int               # raw, not clamped

seal:
  status: [SEALED | UNSEALED_INFRA | FAILED_VALIDATION]
  vault_receipt_id: <sha256-hex or null>

receipt:
  parent_spawn_hash: <sha256-hex or null>
  receipt_hash: <sha256-hex>
```

---

## Judgment Coverage Formula (clamped, per Arif)

```
judgment_coverage = min(
  apex_verdicts_sought / max(risky_actions_taken, 1),
  1.0
)
```

`coverage > 1.0` is physically impossible. `coverage = 1.0` means all risky actions judged. `coverage < threshold` = constitutionally insolvent session.

Companion raw metric: `judgment_debt = risky_actions_taken - apex_verdicts_sought` (unclamped, integer).

---

## Archetype Confidence Caps (per-archetype, audited)

| Archetype | Cap |
|---|---|
| af-explore | 0.60 |
| af-reviewer | 0.70 |
| af-plan | 0.75 |
| af-worker | 0.80 |
| af-fix | 0.85 |
| af-coordinator | 0.85 |
| af-forge | 0.90 |
| SCOUT | 0.70 |
| CRITIC | 0.70 |
| SYNTHESIZER | 0.75 |
| AUDITOR | 0.80 |
| 333-AGI | 0.90 |
| 555-ASI / 555-ASI-VISION / image-analyzer | 0.75–0.80 |
| 888-APEX / dispatch | 0.80–0.90 |

Read-only archetypes have lower caps. Execution archetypes have higher caps. **Non-negotiable.** Cross-harness consistency enforced via `federation/protocols/spawn_enums.json` as canonical source.

---

## Parallel Spawn Rule

Allowed. Per-spawn telemetry **mandatory**. Aggregate seal **derived-only**.

```
allowed: true
max_parallel: 3
per_spawn_telemetry: required
aggregate_seal: dashboard_only
```

Flat-tree invariant preserved (no nesting, max_spawn_depth=1 across all harnesses).

---

## Open Audit Items (NOT yet sealed)

| Area | Status |
|---|---|
| Hermes draft delegation-context.md | HOLD (15 failures, see audit-2026-08-07.md) |
| Kimi protocol v0.1.0 schema | PARTIAL-SEAL+ |
| Capability model | SEAL (per-archetype ceilings defined) |
| Provenance chaining | SEAL (parent_spawn_hash chain) |
| Parallel spawn model | SEAL with per-spawn telemetry |
| Enforcement implementation | HOLD |
| Hook verification | HOLD |
| Tool capability stripping at runtime | HOLD |
| forge_vault failure handling | SEAL (tri-state status) |
| Cross-harness enum authority | SEAL (spawn_enums.json canonical) |

**The risk now is no longer schema design. The risk is the gap between what spec says and what runtime enforces.** Audit focus shifts there next.

---

**Ω₀ ≈ 0.04. Confidence: 0.90.**
**Sealed:** 2026-08-07 by Hermes, derived from Arif PARTIAL-SEAL+ directive.
**DITEMPA BUKAN DIBERI.**

Spawn does not transfer power. Aggregate does not replace spawn. Infrastructure failure is not governance leak.