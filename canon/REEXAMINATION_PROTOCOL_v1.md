# Re-examination Protocol v1

**Sealed:** 2026-09-10T02:00+08
**Status:** SEAL (canonical specification)
**Classification:** Constitutional — rights of examination over all witness objects

---

## Purpose

Re-examination is the primary function of the witness system.
Trust is a side effect. Correction is the function.

This protocol defines how any entity — human, agent, or system — can challenge any witness object in arifOS.

---

## Core Principle

```
No authority, no interpretation, and no institution
becomes immune to re-examination.
```

This is not optional.
This is a floor.

---

## The Right

Every witness object is subject to re-examination by:
- Any agent in the federation
- Any human with access
- Any future system that inherits the witness graph

No special authority is required to CHALLENGE.
Evidence IS required to challenge successfully.

---

## Re-examination Methods

### Method 1: Direct Challenge

Produce a new witness object that contradicts the target.

```yaml
challenge:
  target_witness_id: "wo-<uuid>"
  challenge_type: DIRECT
  new_witness:
    claim:
      statement: "<contradicting claim>"
      truth_class: OBS | DER | INT | SPEC
      confidence: <0.0-1.0>
    source_chain:
      - source_type: <type>
        reliability: <0.0-1.0>
    contradiction_record:
      dimension: "<what is contradicted>"
      counterclaim: "<the original claim being challenged>"
```

### Method 2: Evidence Gap

Identify missing evidence that the original witness requires.

```yaml
challenge:
  target_witness_id: "wo-<uuid>"
  challenge_type: EVIDENCE_GAP
  missing_evidence:
    - description: "<what evidence is absent>"
      significance: "<why its absence matters>"
      acquisition_path: "<how to obtain it>"
```

### Method 3: Falsification Test

Apply the falsification criteria already defined in the witness object.

```yaml
challenge:
  target_witness_id: "wo-<uuid>"
  challenge_type: FALSIFICATION
  criterion_applied: "<which criterion from reexamination.falsification_criteria>"
  result: CONFIRMED_FALSIFIED | NOT_FALSIFIED | INCONCLUSIVE
  evidence: "<supporting evidence for the test result>"
```

### Method 4: Dimensional Gap

Identify that the witness lacks coverage in a required reality dimension.

```yaml
challenge:
  target_witness_id: "wo-<uuid>"
  challenge_type: DIMENSIONAL_GAP
  missing_dimensions:
    - dimension: historical | legal | political | economic | operational
      significance: "<why absence of this dimension matters>"
```

### Method 5: Temporal Decay

Assert that the witness may no longer reflect current reality.

```yaml
challenge:
  target_witness_id: "wo-<uuid>"
  challenge_type: TEMPORAL_DECAY
  last_validated: <ISO-8601 UTC>
  current_time: <ISO-8601 UTC>
  decay_reason: "<what may have changed>"
```

---

## Response Protocol

When a challenge is issued:

```
1. Original witness status → CONTESTED
2. Challenge witness recorded as contradicting_witnesses entry
3. Both witnesses enter shared reality evaluation
4. Resolution status updated:
   - RESOLVED: one witness supersedes the other
   - PARTIALLY_RESOLVED: both contain valid elements
   - UNRESOLVED: insufficient evidence to determine
5. Resolution recorded in both witness objects
```

---

## Escalation Path

```
Challenge issued
  ↓
Agent-level examination
  ↓ (if unresolved)
Multi-agent examination (forge_parallel or forge_witness)
  ↓ (if unresolved)
Human examination required
  ↓ (if unresolved)
Mark UNRESOLVED + attach to reality model as open question
```

UNRESOLVED is a valid state.
It is preferable to FALSE RESOLUTION.

---

## Time-Based Re-examination

Witness objects can have scheduled re-examination:

```yaml
reexamination:
  reexamination_scheduled: <ISO-8601 UTC>
  reexamination_trigger:
    type: SCHEDULED | EVENT_BASED | THRESHOLD
    event: "<if event_based>"
    threshold: "<if threshold_based>"
```

When triggered, re-examination produces:
- VALIDATED: witness still holds
- UPDATED: witness modified with new evidence
- SUPERSEDED: new witness replaces this one

---

## Anti-Patterns

DO NOT:
- Challenge without evidence (noise, not governance)
- Suppress challenges from lower-authority entities
- Auto-validate without re-examination
- Treat re-examination as hostile (it is maintenance)
- Allow SEALED status to prevent challenge

DO:
- Welcome challenges as system health signal
- Record all challenges even if unsuccessful
- Treat UNRESOLVED as progress, not failure
- Schedule re-examination for high-stakes witnesses
- Preserve challenge history in witness graph

---

## Relationship to arifOS Floors

```
F2 TRUTH    → re-examination ensures truth stays current
F7 HUMILITY → no witness immune from challenge
F8 LAW      → re-examination protocol IS the law
F11 AUDIT   → every re-examination is logged
F13 SOVEREIGN → sovereign can accelerate but not suppress re-examination
```

---

DITEMPA BUKAN DIBERI.
