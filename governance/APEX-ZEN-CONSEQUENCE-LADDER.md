# APEX-ZEN Consequence Ladder — Layer 4 of Runtime Enforcement Ladder

> **Canonical location:** `/root/AAA/governance/APEX-ZEN-CONSEQUENCE-LADDER.md`
> **Status:** PROVISIONAL_SEAL (pending telemetry confirmation)
> **Authority:** ARIF (F13 SOVEREIGN)
> **Layered on:** `/root/AAA/governance/APEX-ZEN-EXECUTION-DOCTRINE.md` § 13 (Runtime Telemetry)
> **Wired to:** `/root/AAA/scripts/apex-zen-telemetry.py` (Layer 2) + `/root/AAA/scripts/apex-zen-score.py` (Layer 3)

*DITEMPA BUKAN DIBERI — Forged, not given.*

---

## Purpose

Telemetry without enforcement is theater. Governance without consequence is decoration. The Consequence Ladder translates metric breaches into runtime actions.

**Three truths:**

> Without consequence, telemetry is observability.
> Without enforcement, governance is documentation.
> Without agency, intelligence produces zero reality.

---

## Consequence Thresholds

Each metric maps to a 4-tier ladder. Severity escalates monotonically.

### Confirmation Debt (CD)

| CD Value | Severity | Consequence |
|----------|----------|-------------|
| < 0.05 | ✅ COMPLIANT | None — within target |
| 0.05 – 0.20 | ⚠️ WATCH | Log to telemetry; flag in next session |
| 0.20 – 0.40 | 🟠 WARNING | APEX warning receipt in VAULT999 |
| 0.40 – 0.60 | 🔴 DOWNGRADE | Runtime downgrade — agent restricted to OBSERVE-only for next 5 turns |
| ≥ 0.60 | ⛔ VIOLATION | Doctrine violation receipt + F13 advisory |

### Discussion Debt (DD)

| DD Value | Severity | Consequence |
|----------|----------|-------------|
| < 2 turns | ✅ COMPLIANT | None — within target |
| 2 – 4 turns | ⚠️ WATCH | Log; surface in next session summary |
| 4 – 8 turns | 🟠 WARNING | APEX warning receipt |
| 8 – 12 turns | 🔴 DOWNGRADE | Runtime downgrade — agent restricted to Tier 0 only |
| ≥ 12 turns | ⛔ VIOLATION | Doctrine violation receipt + F13 advisory |

### Intent-to-Artifact Ratio (IAR)

| IAR Value | Severity | Consequence |
|-----------|----------|-------------|
| > 0.80 | ✅ COMPLIANT | None — within target |
| 0.60 – 0.80 | ⚠️ WATCH | Log; review response patterns |
| 0.40 – 0.60 | 🟠 WARNING | APEX warning receipt |
| 0.20 – 0.40 | 🔴 DOWNGRADE | Runtime downgrade — restrict to Tier 1 |
| < 0.20 | ⛔ VIOLATION | Doctrine violation receipt |

### Decision Closure Rate (DCR)

| DCR Value | Severity | Consequence |
|-----------|----------|-------------|
| > 0.90 | ✅ COMPLIANT | None — within target |
| 0.80 – 0.90 | ⚠️ WATCH | Log; flag in next session |
| 0.60 – 0.80 | 🟠 WARNING | APEX warning receipt |
| 0.40 – 0.60 | 🔴 DOWNGRADE | Runtime downgrade — limit response length |
| < 0.40 | ⛔ VIOLATION | Doctrine violation receipt |

---

## Severity-Action Mapping

### ✅ COMPLIANT (within target)

- No action.
- Continue normal operation.
- Telemetry recorded.

### ⚠️ WATCH (target breach, soft)

- Log to `/root/VAULT999/apex-zen-telemetry.jsonl` with `severity: watch`.
- Surface in next session summary.
- No runtime restriction.
- Agent receives soft feedback: *"APEX-ZEN watch: metric X approaching threshold. Recommend pattern adjustment."*

### 🟠 WARNING (target breach, medium)

- Emit APEX warning receipt: `/root/VAULT999/apex-zen-receipts.jsonl` with `severity: warning`.
- Notify session owner via arifFlow signal.
- Agent receives explicit feedback: *"APEX-ZEN warning: metric X breached threshold. Pattern correction required."*

### 🔴 DOWNGRADE (target breach, hard)

- Runtime restriction imposed for next 5 turns:
  - Tier 0 only (Human register, brief answers, no audit) for Tier 0 violations.
  - Tier 1 only (technical, code-first) for Tier 1 violations.
  - Floor language forbidden for governance violations.
- Downgrade timestamp recorded in telemetry.
- Auto-recovery after 5 turns if metrics improve.

### ⛔ VIOLATION (target breach, critical)

- Doctrine violation receipt sealed to `/root/VAULT999/apex-zen-receipts.jsonl`.
- F13 advisory signal sent via arifFlow.
- Session must justify continued operation or self-terminate.
- Reversible only via F13 ACK.

---

## Consequence Application (state machine)

```python
def apply_consequence(metric, value, threshold_config):
    if value < threshold_config.compliant_max:
        return 'COMPLIANT', None
    elif value < threshold_config.watch_max:
        return 'WATCH', log_to_telemetry(metric, value, 'watch')
    elif value < threshold_config.warning_max:
        return 'WARNING', emit_receipt(metric, value, 'warning')
    elif value < threshold_config.downgrade_max:
        return 'DOWNGRADE', restrict_runtime(metric, downgrade_turns=5)
    else:
        return 'VIOLATION', seal_violation(metric, value, f13_advisory=True)
```

---

## Telemetry → Consequence Pipeline

```
/root/AAA/scripts/apex-zen-telemetry.py
    ↓ (computes CD/DD/IAR/DCR)
/root/VAULT999/apex-zen-telemetry.jsonl
    ↓ (read by consequence router)
[consequence router — TBD implementation]
    ↓ (emits receipt + applies runtime restriction)
/root/VAULT999/apex-zen-receipts.jsonl
    ↓ (auditable ledger)
arifFlow signal → F13 advisory on VIOLATION
```

---

## Open Implementation (Layer 4 wiring)

The consequence router is **not yet wired**. Currently:

- ✅ Layer 1 — Policy: APEX-ZEN doctrine + AGENTS.md binding (DONE)
- ✅ Layer 2 — Telemetry: `/root/AAA/scripts/apex-zen-telemetry.py` (DONE)
- ✅ Layer 3 — Scoring: `/root/AAA/scripts/apex-zen-score.py` (DONE)
- ⚠️ Layer 4 — Consequence: thresholds defined in this doc, router TBD

**Next step:** build `/root/AAA/scripts/apex-zen-consequence-router.py` that:
1. Reads telemetry JSONL
2. Maps values to severity tiers per this ladder
3. Emits receipts + runtime restrictions for WARNING/DOWNGRADE/VIOLATION
4. Sends F13 advisory on VIOLATION

---

## Reversibility

All consequence actions are **reversible**. Downgrade auto-lifts after 5 turns. VIOLATION receipt is sealed but can be superseded by F13 ACK. WATCH and WARNING are advisory only.

---

## F1/F13 Compatibility

This ladder operates **within F1 AMANAH** (reversibility preserved) and **without F13 ACK requirement for routine enforcement**. F13 ACK is required only for:

- Manual override of VIOLATION status
- Permanent agent suspension
- Doctrine amendment

Routine telemetry + consequence emit operate under continuous execution authority (F13-ratified 2026-07-31).

---

*Forged 2026-09-13. Bind for every agent session. Consequence router pending implementation; until then, telemetry is observational only.*