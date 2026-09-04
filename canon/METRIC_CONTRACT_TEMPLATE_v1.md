# Metric Contract Template (v1)

> **Status:** CANON — SEALED by F13 directive 2026-09-04 (Arif Fazil)
> **Forged:** 2026-09-04 by FI-003 (Qwen Code) under F13 directive (D7)
> **Ratified:** 2026-09-04 by F13 directive (Arif Fazil) — see git commit for trace
> **Binding upstream:** `/root/AAA/canon/HERMES_OPENCLAW_ROLE_SPLIT_CONTRACT.md` AMENDMENT-002 §10 (canon hierarchy)
> **Pair with:** ARCANUM_FLOOR_DEFINITIONS.json (canonical F1-F13 sources), arifFlow receipts
> **DITEMPA BUKAN DIBERI** — Forged, not given.

---

## 1. Objective

This template specifies the required structure for every metric (floor score, scalar, ratio, vector dimension) in the arifOS federation. Per audit gap #1 ("Pass is not evidence — every scalar needs a machine-readable metric contract").

**Why:** Until this template existed, scalar values displayed in the federation UI (/cockpit/, /hud/) were black-box — no definition, no calibration, no anti-gaming, no independent recompute. After this template: every metric declares its full provenance, and FRAME can independently verify.

---

## 2. Required Schema (YAML)

Every metric MUST declare the following fields. Missing field = metric is INVALID.

```yaml
metric_id: F2_TRUTH                   # unique canonical ID
metric_name: "Truth (F2 Floor)"       # human-readable
version: "1.0.0"                      # semantic version

definition: >
  Proportion of externally verifiable factual claims supported by valid provenance
  in externally-facing outputs.

owner: "F13 / arifOS kernel"          # named human role + system
owner_signature_required: true        # if true, owner must sign each contract update

formula: "verified_claims / total_claims"

inputs:
  - name: total_claims
    source: "arifFlow receipts over window"
    type: integer
  - name: verified_claims
    source: "FRAME verification of receipts"
    type: integer

window: "rolling_7d"                   # rolling, fixed, daily, weekly, monthly, custom
window_size: 604800                    # seconds (7d = 604800)
emit_frequency: "1h"                   # how often to recompute

population: >
  All externally-facing answers from Hermes + A-FORGE with factual claims in window.

denominator_protection: "min_n=200"    # require minimum sample before reporting

confidence_interval: "Wilson 95%"      # Wilson / Clopper-Pearson / Bootstrap / none

thresholds:
  pass: 0.99
  warning: 0.97
  block: 0.93                          # below this = 888_HOLD

independent_recompute: "FRAME"         # which organ can re-compute independently
independent_recompute_period: "daily"  # how often

anti_gaming_control: >
  Stratified blind audit. FRAME pulls random 5% sample, verifies independently,
  computes variance vs kernel-reported value. Variance > 0.15 = escalation.

last_calibrated_at: "2026-09-04T00:00:00Z"
next_calibration_at: "2026-10-04T00:00:00Z"  # monthly cadence

calibration_history: "/root/AAA/canon/calibration_history/{metric_id}.jsonl"

deprecation_policy: >
  If metric is unused for 90 consecutive days, owner is notified.
  If unused for 180 days, metric is marked DEPRECATED but retained.
  If unused for 365 days, metric may be removed (after F13 sign-off).

audit:
  schema_version: "metric-contract/v1.0"
  signed_by: "F13 directive 2026-09-04"
  signed_at: "2026-09-04T17:30:00Z"
  signature: "ed25519:..."             # not literal — actual signature here
```

---

## 3. Validation Rules

1. **All fields required.** Linter at `/root/AAA/scripts/metric_contract_lint.py` enforces schema.
2. **Thresholds monotonic:** block < warning < pass.
3. **Window vs emit_frequency consistent:** emit_frequency ≤ window / 10 (no point emitting more often than 10% of window).
4. **Sample n realistic:** denominator_protection should be ≥ 30 for statistical validity; ≥ 200 preferred.
5. **Anti-gaming required:** every metric must have anti_gaming_control field.
6. **Owner must be named:** no anonymous metrics.

---

## 4. Worked Example (F2_TRUTH)

See section 2 above — that's the example.

---

## 5. Worked Example (F1_AMANAH)

```yaml
metric_id: F1_AMANAH
metric_name: "Amanah (F1 Floor)"
version: "1.0.0"

definition: >
  Proportion of action attempts that respect trust boundaries (data class
  authorization, scope token presence, irreversible-action F13 signoff where
  required).

owner: "F13 / arifOS kernel"
owner_signature_required: true

formula: "trust_respecting_actions / total_action_attempts"

inputs:
  - name: total_action_attempts
    source: "arifFlow Execute + Seal receipts over window"
    type: integer
  - name: trust_respecting_actions
    source: "arifOS kernel + AAA governance decisions"
    type: integer

window: "rolling_7d"
window_size: 604800
emit_frequency: "1h"

population: "All action attempts by all 8 FI agents + organs over window"

denominator_protection: "min_n=200"

confidence_interval: "Wilson 95%"

thresholds:
  pass: 0.95
  warning: 0.90
  block: 0.85

independent_recompute: "FRAME"
independent_recompute_period: "daily"

anti_gaming_control: >
  Cross-check against AAA identity-plane revocation log. Any agent with revoked
  token but continued attempts = AUTOMATIC FAIL on F1.

last_calibrated_at: "2026-09-04T00:00:00Z"
next_calibration_at: "2026-10-04T00:00:00Z"

deprecation_policy: "Same as F2_TRUTH (180d unused = deprecate)"

audit:
  schema_version: "metric-contract/v1.0"
  signed_by: "F13 directive 2026-09-04"
  signed_at: "2026-09-04T17:30:00Z"
```

---

## 6. Worked Example (arifFlow FQ — verify/execute ratio)

```yaml
metric_id: ARIFLOW_FQ
metric_name: "arifFlow FQ (verify/execute ratio)"
version: "1.0.0"

definition: >
  Per-actor ratio of Verify receipts to Execute receipts over a rolling window.
  FQ < 0.5 = STUCK (all agents HOLD); FQ ≥ 0.5 = FLOWING.

owner: "arifFlow lane + FRAME"
owner_signature_required: false

formula: "verify_count / execute_count (per actor, per window)"

inputs:
  - name: execute_count
    source: "arifFlow /ingest with step_type=Execute"
    type: integer
  - name: verify_count
    source: "arifFlow /ingest with step_type=Verify"
    type: integer

window: "rolling_24h"
window_size: 86400
emit_frequency: "10s"

population: "All 8 FI agents"

denominator_protection: "min_n=3 execute (per actor per window)"

confidence_interval: "none (ratio, not proportion)"

thresholds:
  pass: 0.5
  warning: 0.4
  block: 0.3

independent_recompute: "FRAME"
independent_recompute_period: "real-time"

anti_gaming_control: >
  Cross-check that Verify receipts cite real verification actions (not
  fabricated). Variance between Verify claims and observed behavior > 0.20 = escalation.

last_calibrated_at: "2026-08-30T00:00:00Z"  # post-fq-unstick recipe
next_calibration_at: "2026-09-30T00:00:00Z"

deprecation_policy: "FQ is mission-critical — only deprecate if arifFlow itself is retired"

audit:
  schema_version: "metric-contract/v1.0"
  signed_by: "F13 directive 2026-08-30"
  signed_at: "2026-08-30T00:00:00Z"
```

---

## 7. Adoption Path

**Phase 1 (now):** Apply template to F1, F2, F13 metrics. ~3 contracts.
**Phase 2 (D7+1d):** Apply to arifFlow FQ vector (7 dimensions). ~7 contracts.
**Phase 3 (D7+7d):** Apply to all organ health scalars (kernel, GEOX, WEALTH, WELL). ~20 contracts.
**Phase 4 (D7+30d):** Apply to all agent-card declared capabilities + skills (~200+). Audit of coverage.

---

## 8. Cross-References

- `/root/AAA/canon/HERMES_OPENCLAW_ROLE_SPLIT_CONTRACT.md` AMENDMENT-002 §10 (canon hierarchy)
- `/root/AAA/specs/QG_V0_3_VECTOR_SPEC.md` (arifFlow vector — source for FQ + dimensions)
- `/root/AAA/scripts/metric_contract_lint.py` (linter, to be created)
- `/root/forge_work/2026-08-30-PROVIDER_REALITY_AUDIT.md` (capability ledger source)

---

## 9. Open Questions (PENDING F13)

- **Q1**: Cadence for re-calibration — monthly per metric, or per-tier? (Default: monthly per metric)
- **Q2**: Anti-gaming variance threshold — 0.15 too tight or too loose? (Default: 0.15 for proportion metrics)
- **Q3**: Should FRAME re-computation cadence be configurable per metric, or global? (Default: per-metric field, with default = daily)

---

DITEMPA BUKAN DIBERI — v1 SEALED 2026-09-04 by F13 directive (Arif Fazil)
