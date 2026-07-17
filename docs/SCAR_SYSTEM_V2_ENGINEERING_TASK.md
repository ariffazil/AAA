# Scar System v2 — Engineering Task for A-FORGE

> **Source:** `AAA/docs/SCAR_SHADOW_PROFILING_DOCTRINE.md`
> **Created:** 2026-07-12
> **Priority:** P0 (authority laundering prevention) → P4 (profiler validation)
> **Estimated complexity:** P0-P1 = moderate; P2-P4 = complex

---

## Context

The current scar system (`forge_scar`) supports seal/list/consult modes. It has critical gaps:

1. No disconfirming evidence fields → scars cannot falsify themselves
2. No expiry/retirement → scars become immortal constraints
3. No evaluator profiling → profiler treated as neutral (dangerous)
4. No evidence tiering → exploit sequences leak into governance layer
5. No system-vs-model decomposition → scars misattribute causation
6. No confirmation bias counterfields → scars become self-fulfilling
7. No role separation → authority laundering risk (CRITICAL)

The full doctrine is at `AAA/docs/SCAR_SHADOW_PROFILING_DOCTRINE.md`.

---

## P0 — Prevent Authority Laundering (CRITICAL)

### Task P0.1: Add Immutable Role Fields

Add to scar record schema:

```yaml
roles:
  observer_id: string          # who collected evidence
  experiment_designer_id: string  # who designed the test
  analyst_id: string           # who interpreted results
  adjudicator_id: string       # who approved authority change
```

These fields are immutable once the scar is sealed.

### Task P0.2: Validate Role Independence

On `forge_scar` seal mode, enforce:

```
observer_id != adjudicator_id
analyst_id != adjudicator_id
experiment_designer_id != adjudicator_id
```

If violated → `HOLD` with reason `ROLE_SEPARATION_VIOLATION`.

### Task P0.3: Reject Self-Adjudication

An agent cannot seal a scar it observed or analysed. Check effective identity (not just agent_id — also model family, shared context, organizational role).

### Task P0.4: Require Preregistered Experiment Hash

Before trial execution, the experiment plan must be hashed. The hash is stored in the scar record. If no hash is present → `HOLD` with reason `MISSING_EXPERIMENT_HASH`.

---

## P1 — Repair the Evidence Model

### Task P1.1: Add Evidence Counts

```yaml
evidence:
  confirming: int
  disconfirming: int
  inconclusive: int
  null_results: int
```

### Task P1.2: Add Exposure Denominators

```yaml
trial_summary:
  total_trials: int
  eligible_trials: int
  excluded: int
  exclusion_reasons: [string]
```

If `confirming` is provided without `total_trials` → `HOLD` with reason `MISSING_EXPOSURE_DENOMINATOR`.

### Task P1.3: Add Alternative Hypotheses

```yaml
alternative_explanations: [string]
```

Required field. At least one alternative explanation must be considered.

### Task P1.4: Add Raw Evidence References

```yaml
evidence_references:
  transcripts_ref: string      # sealed, restricted
  tool_logs_ref: string        # sealed, restricted
  postconditions_ref: string   # sealed, restricted
```

### Task P1.5: Separate Public Summary from Restricted Evidence

Tier 1 (public): hazard, conditions, controls, confidence
Tier 2 (restricted): exact prompts, transcripts, exploit sequences

Access to Tier 2 requires specific audit or research capability.

---

## P2 — Add Lifecycle Governance

### Task P2.1: Add State Transitions

Extend lifecycle from `PROVISIONAL → CONFIRMED → RETIRED` to:

```
CANDIDATE → UNDER_TEST → (REJECTED | INCONCLUSIVE | PROVISIONAL)
PROVISIONAL → REPLICATED → ACTIVE
ACTIVE → (MITIGATED | DISPUTED | SUPERSEDED | RETIRED)
MITIGATED → ACTIVE (if mitigation fails)
RETIRED → ACTIVE (only through new evidence event)
```

### Task P2.2: Append-Only Transitions

Every state transition is a new append-only event. Never mutate the original scar record.

### Task P2.3: Add Dispute Mode

```bash
forge_scar --dispute <scar_id> --evidence <ref>
```

Requires credible contradictory evidence. Transitions `ACTIVE → DISPUTED`.

### Task P2.4: Add Retire Mode

```bash
forge_scar --retire <scar_id>
```

Requires:
- F3 tri-witness consensus
- Expiry reached OR retirement criteria satisfied
- Disconfirming evidence > threshold

Retired scars remain in ledger (append-only) but lose routing force.

---

## P3 — Connect Scars to Runtime Safely

### Task P3.1: Policy Projection Generator

```bash
forge_scar --project <scar_id>
```

Generates a policy projection from active scars:

```yaml
policy_projection:
  source_scar: string
  model_profile_hash: string
  tool_changes: {tool: HOLD|DENY}
  retry_ceiling: int
```

The kernel never directly executes prose from a scar.

### Task P3.2: Session Profile Injection

Active scars → policy compiler → model/tool restrictions → arifOS session profile.

This is the runtime connection. Scars influence routing without the kernel reading scar text.

---

## P4 — Validate the Profiler

### Task P4.1: Profiler Metrics

Track per evaluator:
- false-positive rate
- false-negative rate
- replication rate
- inter-evaluator agreement
- severity calibration
- scar retirement rate
- mitigation effectiveness

### Task P4.2: Profiler Authority Adjustment

If an evaluator's false-positive rate exceeds threshold → reduce their authority from `advisory` to `observer_only`.

A profiler that never rejects or retires scars is accumulating accusations, not measuring.

---

## Acceptance Tests

| Test | Input | Expected |
|------|-------|----------|
| Self-sealing rejection | `observer_id == adjudicator_id` | `REJECT` — `ROLE_SEPARATION_VIOLATION` |
| Cherry-picking rejection | `confirming=3`, no `total_trials` | `HOLD` — `MISSING_EXPOSURE_DENOMINATOR` |
| Expiry behaviour | Scar passes review date, no fresh evidence | `DEGRADED` — authority reduced |
| Retirement behaviour | F3 consensus + mitigation effective | `SEALED` + `RETIRED` + `INACTIVE` |
| Exploit-tier protection | Normal agent requests Tier 2 evidence | `DENY` — `EVIDENCE_TIER_RESTRICTED` |
| Profiler calibration | Evaluator false-positive rate elevated | Authority reduced to `observer_only` |

---

## Implementation Notes

- Schema changes go in A-FORGE's scar system
- Role separation enforcement is a governance floor — arifOS enforces, A-FORGE obeys
- Policy projection is generated, never handwritten
- All transitions are append-only events in the scar ledger
- Retired scars remain in ledger for historical audit

---

*Engineering task derived from Scar Shadow Profiling Doctrine.*
*Ready for A-FORGE implementation.*
