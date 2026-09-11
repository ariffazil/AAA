# Supersession Chain, Expiry, and Calibration — Memory Architecture Extension

> **Status:** DRAFT — extends MEMORY_ENGINEERING_SPEC_v2
> **Origin:** Hermes epistemic infrastructure directive (2026-09-12)
> **Problem:** Memory is append-heavy, expiry-light. Contradictory beliefs coexist. No calibration tracking.
> **Relationship:** Implements the open loops from SRO Spec

---

## 1. Supersession Chain

### Problem

Claim A is stored. Claim B (more accurate) is stored. Both exist. Neither is marked as superseded. Contradictory beliefs coexist in the same context.

### Solution

Every claim in arif_memory MUST have a supersession index:

```json
{
  "claim_id": "wo-CLAIM-001",
  "supersedes": null,
  "superseded_by": "wo-CLAIM-002",
  "supersession_reason": "Updated with 2027 MOF data",
  "supersession_date": "2027-04-01",
  "status": "SUPERSEDED"
}
```

### Rules

1. **Supersession is NOT deletion.** Old claim remains in chain. Status changes to SUPERSEDED.
2. **Bidirectional link.** Both the old and new claim must reference each other.
3. **Propagation required.** Any claim that `depends_on` a superseded claim must be re-evaluated.
4. **Chain traversal.** Given claim X, `X.supersedes` → older version, `X.superseded_by` → newer version.

### Implementation

**arif_memory store:**
```yaml
# Add to arif_memory payload
supersession_index:
  - claim_id: "wo-CLAIM-001"
    superseded_by: "wo-CLAIM-002"
    reason: "Updated data"
    date: "2027-04-01"
```

**On recall:**
1. Return claim
2. Check `superseded_by` — if not null, return warning: "This claim has been superseded by [new_id]"
3. If caller requests latest: traverse chain to newest non-SUPERSEDED claim

**On store:**
1. If new claim supersedes existing: update both objects
2. If existing claim has `superseded_by` set: reject store (cannot supersede already-superseded claim without chain traversal)

### Propagation Protocol

When claim X is superseded:
1. Find all claims where `depends_on` contains X
2. Mark those claims as STALE
3. Trigger re-examination for each
4. Log propagation event with timestamp

---

## 2. Expiry Fields

### Problem

Claims without expiry live forever. Including wrong ones. No systematic review.

### Solution

Every claim MUST have `expires_at`. Default expiry by truth class:

| Truth Class | Default Expiry | Rationale |
|---|---|---|
| OBS (observed) | 1 year | Observations age slowly |
| DER (derived) | 6 months | Derivations depend on source data |
| INT (interpreted) | 3 months | Interpretations are fragile |
| SPEC (speculation) | 1 month | Speculations need frequent review |

Domain-specific overrides:
- Fiscal data: 6 months (budget cycles)
- Legal data: 1 year or until next court ruling
- Market data: 1 month
- Geological data: 5 years (slow-changing)

### Implementation

**Cron job: expiry_checker**
```bash
# Run daily
# Query arif_memory for claims where expires_at < now AND status != EXPIRED
# Mark as STALE
# Trigger re-examination
# Log to VAULT999
```

**On recall:**
1. Return claim
2. Check `expires_at` — if past, return warning: "This claim expired on [date]"
3. If caller requests: still return, but with STALE flag

**On store:**
1. If `expires_at` not set: compute from truth_class default
2. If `expires_at` is past: reject store (cannot create already-expired claim)

---

## 3. Calibration Tracking

### Problem

Agent confidence 0.8+ is often wrong. No systematic tracking of calibration accuracy. Overconfidence is invisible.

### Solution

Track confidence vs outcome for every claim that makes a prediction:

```yaml
calibration_record:
  claim_id: "wo-CLAIM-001"
  confidence_at_creation: 0.88
  prediction: "DSR will stay 16-18%"
  outcome_observed: true          # Was the prediction correct?
  outcome_date: "2027-03-31"
  calibration_error: 0.12         # |confidence - outcome|
  outcome_source: "MOF Q1 2027 fiscal report"
```

### Aggregation

Per agent:
```yaml
agent_calibration:
  agent_id: "hermes-asi"
  total_predictions: 47
  calibration_errors: [0.12, 0.25, 0.08, ...]
  mean_calibration_error: 0.15
  overconfidence_rate: 0.18       # % of 0.8+ confidence that were wrong
  calibration_band: "ACCEPTABLE"  # <0.2 = GOOD, 0.2-0.3 = ACCEPTABLE, >0.3 = POOR
```

Per domain:
```yaml
domain_calibration:
  domain: "Malaysia fiscal"
  total_predictions: 12
  mean_calibration_error: 0.22
  calibration_band: "ACCEPTABLE"
```

Per truth class:
```yaml
truth_class_calibration:
  truth_class: "DER"
  total_predictions: 30
  mean_calibration_error: 0.18
  calibration_band: "ACCEPTABLE"
```

### Enforcement

- If agent's `overconfidence_rate` > 0.3: agent MUST lower confidence caps
- If domain's `mean_calibration_error` > 0.3: domain claims need more evidence
- If truth class's `mean_calibration_error` > 0.3: that truth class is unreliable

### Implementation

**On outcome observed:**
1. Compare `confidence_at_creation` with actual outcome
2. Compute `calibration_error`
3. Update agent/domain/truth_class aggregates
4. If overconfidence detected: log to VAULT999 as calibration event

**On agent boot:**
1. Load agent's calibration summary
2. If `calibration_band` is POOR: warn agent to lower confidence
3. Feed calibration data into confidence estimation

---

## 4. Correction Propagation Time

### Problem

Correction is received in session N. Related claims in session N+3 still use old data. Propagation is too slow.

### Solution

**Dependency graph + propagation trigger:**

```yaml
propagation_chain:
  corrected_claim: "wo-CLAIM-001"
  affected_claims:
    - "wo-CLAIM-003"  # depends_on wo-CLAIM-001
    - "wo-CLAIM-007"  # depends_on wo-CLAIM-001
  propagation_time: "2 sessions"
  propagation_status: "PROPAGATED"
```

### Rules

1. **Target: <1 session.** Correction should propagate within the same session.
2. **Maximum: 3 sessions.** If propagation takes >3 sessions, it's a failure.
3. **Automatic trigger.** When a claim is superseded, automatically find and flag dependent claims.

### Implementation

**On supersession:**
1. Traverse `depends_on` graph
2. Mark all dependents as STALE
3. Create propagation event
4. Log to VAULT999

**On agent boot:**
1. Check for unpropagated corrections
2. If found: prioritize re-examination
3. Log propagation lag

---

## 5. Integration Points

| Component | Integration |
|---|---|
| arif_memory | Supersession index, expiry fields, calibration records |
| VAULT999 | Calibration events, propagation events |
| Cron | Expiry checker (daily), calibration aggregator (weekly) |
| Agent boot | Load calibration summary, check unpropagated corrections |
| SRO Spec | Supersession chain, expiry, calibration fields |
| Claim-Receipt Binding | Supersession claims need handles (Law 2) |

---

## 6. Open Loops

1. **Schema migration:** Existing claims in arif_memory need supersession/expiry fields added
2. **Cron jobs:** Expiry checker and calibration aggregator need to be scheduled
3. **Agent integration:** Agent boot sequence needs calibration loading
4. **Propagation graph:** `depends_on` relationships need to be indexed for traversal

---

DITEMPA BUKAN DIBERI ⚒️
