# Sovereign Reality Object (SRO) — Extension to Witness Object v1

> **Status:** DRAFT — extends WITNESS_OBJECT_SPEC_v1 (SEAL 2026-09-10)
> **Origin:** Hermes epistemic infrastructure directive (2026-09-12)
> **Relationship:** SRO = Witness Object + scenarios + signposts + causal links + permissions + jurisdiction + expiry
> **Authority:** Additive fields to WITNESS_OBJECT_SPEC_v1 — requires F13 ratification for schema change

---

## Purpose

The Witness Object captures *what was observed*. The SRO adds *what it means for decisions* — scenarios, monitoring signals, causal mechanisms, and action permissions.

Not every Witness Object needs SRO extension. Only objects that:
- Participate in governance decisions
- Have causal implications across domains
- Require scenario planning
- Need monitoring signposts

---

## Extension Schema

```yaml
sovereign_reality_object:
  # Inherits all Witness Object fields
  # (witness_id, version, created_at, created_by, claim, source_chain,
  #  supporting/contradicting/dependent/extends witnesses, contradictions,
  #  reexamination, shared_reality, reality_dimensions, possibility_space,
  #  decision_dependencies, capability_test, hash, previous_hash, chain_position)

  # === SRO EXTENSIONS ===

  # Jurisdiction
  jurisdiction: "<country | region | domain>"    # Where this claim applies

  # Temporal bounds
  observed_at: <ISO-8601>                        # When the observation was made
  expires_at: <ISO-8601>                         # When this claim must be re-examined
  review_by: <ISO-8601>                          # Soft deadline for review

  # Causal mechanism
  causal_link:
    from: "<upstream factor>"                    # What causes
    to: "<downstream effect>"                    # What is caused
    status: plausible | demonstrated | refuted   # Causal confidence
    strength: none | weak | medium | strong      # Causal strength
    assumptions: []                              # What must hold for causation
    disconfirmers: []                            # What would break the causal link

  # Scenario planning
  scenarios:
    baseline: "<most likely outcome>"            # Default trajectory
    adverse: "<credible negative outcome>"       # Downside case
    tail: "<low-probability high-impact>"        # Tail risk
    # Optional: named scenarios for complex domains
    # scenario_<name>:
    #   probability: 0.0-1.0
    #   description: "<what happens>"
    #   triggers: ["<what activates this scenario>"]

  # Monitoring signals
  signposts:
    - id: "<signpost-id>"
      description: "<what to watch>"
      source: "<where to observe>"
      frequency: "<how often to check>"
      threshold: "<what value triggers concern>"
      direction: increasing | decreasing | stable

  # Action permissions
  permissions:
    recommend: agent | human_only                # Who can recommend action
    prepare_reversible_action: agent | human_only # Who can prepare
    execute_irreversible_action: agent | human_only # Who can execute

  # Supersession chain
  supersession:
    supersedes: "<witness_id | null>"            # What this replaces
    superseded_by: "<witness_id | null>"         # What replaces this
    supersession_reason: "<why>"                 # Why the change
    supersession_date: <ISO-8601 | null>         # When superseded

  # Calibration metadata
  calibration:
    confidence_at_creation: 0.0-1.0              # Confidence when created
    outcome_observed: true | false | null        # Was the prediction correct?
    outcome_date: <ISO-8601 | null>              # When outcome was observed
    calibration_error: <float | null>            # |confidence - outcome|
```

---

## Lifecycle (extends Witness Object lifecycle)

```
DRAFT
  ↓ (validation)
VALIDATED
  ↓ (challenge)
CONTESTED → RESOLVED → VALIDATED
         → SUPERSEDED → replaced by new SRO (supersession chain updated)
  ↓ (time decay / expiry)
STALE → re-examination triggered
  ↓ (calibration)
CALIBRATED → outcome observed → calibration_error computed
  ↓ (persistence)
SEALED → immutable but still re-examinable
```

**New transitions:**
- VALIDATED → CALIBRATED: when outcome is observed
- STALE → SUPERSEDED: when new evidence replaces old claim
- Any → EXPIRED: when `expires_at` passes without re-examination

---

## Supersession Protocol

When claim A is superseded by claim B:

1. Create claim B with `supersession.supersedes = A.witness_id`
2. Update claim A with `supersession.superseded_by = B.witness_id`
3. Set claim A status to SUPERSEDED (do NOT delete)
4. Record `supersession_reason` in both objects
5. Propagate: any object that `depends_on` A must be re-evaluated

**Supersession is NOT deletion.** The old claim remains in the chain for audit. Its status changes, not its existence.

---

## Expiry Protocol

Every SRO must have `expires_at`. Default expiry:

| Truth Class | Default Expiry |
|---|---|
| OBS (observed) | 1 year or domain-specific |
| DER (derived) | 6 months |
| INT (interpreted) | 3 months |
| SPEC (speculation) | 1 month |

**On expiry:**
1. Mark as STALE
2. Trigger re-examination
3. If re-validated: extend expiry
4. If not re-validated: mark as EXPIRED, do NOT delete

---

## Calibration Protocol

After `expires_at` or when outcome is observed:

1. Compare `confidence_at_creation` with actual outcome
2. Compute `calibration_error = |confidence - outcome|`
3. Aggregate calibration errors per agent, per domain, per truth class
4. If calibration_error > 0.2 consistently → agent is overconfident
5. Feed calibration data back to agent's confidence calibration

**Calibration tracking fields:**
```yaml
calibration_history:
  - claim_id: "<witness_id>"
    confidence: 0.88
    outcome: true | false
    error: 0.12
    date: "2026-09-12"
```

---

## Example: MY-FISCAL-2026-DSR (Hermes's first SRO)

```yaml
sovereign_reality_object:
  witness_id: "wo-MY-FISCAL-2026-DSR"
  version: 1
  created_at: "2026-09-12T00:00:00Z"
  created_by: "hermes-asi"

  claim:
    statement: >
      Debt-service burden constrains fiscal room more than headline
      deficit suggests; DSR at 17% exceeds FRA 15% reference limit,
      creating structural vulnerability to commodity/political shocks
    truth_class: DER
    confidence: 0.88
    confidence_basis: "MOF Budget 2026 + FRA 2023 + IMF Article IV cross-validation"

  jurisdiction: "Malaysia federal"
  observed_at: "2026-09-12"
  expires_at: "2027-03-31"

  causal_link:
    from: "weaker_hydrocarbon_buffer"
    to: "higher_adjustment_cost"
    status: plausible
    strength: medium
    assumptions:
      - "STR/SARA transfers remain politically sticky"
      - "Alternative revenue underperforms"
      - "PETRONAS dividends do not recover to RM25B+"
    disconfirmers:
      - "GST restoration broadens revenue base"
      - "PETRONAS FCF recovers above RM15B"
      - "Borneo petroleum bargain frees federal dependency"

  scenarios:
    baseline: "Managed fiscal-federal bargain; DSR 16-18%; deficit narrows slowly"
    adverse: "Prolonged squeeze; DSR >18%; development spending declines"
    tail: "Sarawak legal victory + commodity shock + UMNO-PAS snap election"

  signposts:
    - id: "PETRONAS-DIVIDEND"
      description: "PETRONAS dividend revision announcements"
      source: "MOF / PETRONAS annual report"
      frequency: "quarterly"
      threshold: "< RM15B annual"
      direction: decreasing
    - id: "DSR-TRAJECTORY"
      description: "DSR quarterly trajectory"
      source: "MOF fiscal updates"
      frequency: "quarterly"
      threshold: "> 18%"
      direction: increasing
    - id: "PETROS-EXECUTION"
      description: "PETROS milestones vs Petronas in Sarawak"
      source: "Sarawak government / PETROS"
      frequency: "monthly"
      threshold: "any major milestone"
      direction: stable

  permissions:
    recommend: agent
    prepare_reversible_action: agent
    execute_irreversible_action: human_only

  supersession:
    supersedes: null
    superseded_by: null
    supersession_reason: null
    supersession_date: null

  calibration:
    confidence_at_creation: 0.88
    outcome_observed: null
    outcome_date: null
    calibration_error: null
```

---

## Relationship to Existing Infrastructure

| Component | Relationship |
|---|---|
| Witness Object v1 | SRO extends it (additive fields) |
| Contradiction Ledger | SRO contradictions feed into ledger |
| Claim-Receipt Binding | SRO claims must have handles (Law 2) |
| Memory Promotion Gate | SRO passes through 4-gate promotion |
| Memory Engineering v2 | SRO lives in Layer 4 (Witness Graph) |
| VAULT999 | SRO can be sealed (immutable) |
| arif_memory | SRO stored in semantic layer with supersession index |

---

## Open Loops (from Hermes)

1. **Supersession chain** — specified above, needs wiring into arif_memory
2. **Expiry fields** — specified above, needs cron-based expiry checker
3. **Calibration tracking** — specified above, needs aggregation pipeline
4. **Correction propagation time** — needs dependency graph traversal on supersession

---

DITEMPA BUKAN DIBERI ⚒️
