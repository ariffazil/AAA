# Witness Object Specification v1

**Sealed:** 2026-09-10T02:00+08
**Status:** SEAL (canonical specification)
**Classification:** Constitutional — atomic unit for all reality operations

---

## Purpose

The Witness Object is the atomic unit of reality representation in arifOS.

All operations — research, memory, governance, judgment — produce, consume, or transform Witness Objects.

This is not a research output format.
This is the substrate through which reality becomes governable.

---

## Specification

```yaml
witness_object:
  # Identity
  witness_id: "wo-<uuid>"                    # Unique identifier
  version: 1                                  # Schema version
  created_at: <ISO-8601 UTC>                  # When witnessed
  created_by: <agent_id | human_id>           # Who witnessed

  # Content
  claim:                                      # What is being witnessed
    statement: "<natural language>"
    truth_class: OBS | DER | INT | SPEC        # Evidence discipline tag
    confidence: 0.0-1.0                       # Epistemic confidence
    confidence_basis: "<why this confidence>"  # Never naked number

  # Provenance
  source_chain:                               # Where did this come from
    - source_id: "<id>"
      source_type: web | document | memory | sensor | agent | human | system
      retrieved_at: <ISO-8601 UTC>
      url_or_path: "<if applicable>"
      reliability: 0.0-1.0                    # Source reliability estimate

  # Relationship to other witnesses
  supporting_witnesses: []                    # IDs of witnesses that support this claim
  contradicting_witnesses: []                 # IDs of witnesses that contradict this claim
  dependent_witnesses: []                     # IDs of witnesses this one depends on
  extends_witnesses: []                       # IDs of witnesses this one builds on

  # Contradiction mapping
  contradictions:                             # Internal contradiction record
    - dimension: <what is contradicted>
      counterclaim: "<opposing statement>"
      counter_source: <source of counterclaim>
      resolution_status: UNRESOLVED | PARTIALLY_RESOLVED | RESOLVED
      resolution_note: "<if resolved, how>"

  # Re-examination protocol
  reexamination:
    required: true                            # Always true — all witnesses are re-examinable
    falsification_criteria:                   # What would disprove this witness
      - "<criterion 1>"
      - "<criterion 2>"
    missing_evidence: []                      # What evidence is absent
    reexamination_scheduled: <ISO-8601 UTC | null>  # When to re-check
    challenge_path:                           # How to challenge this witness
      method: "submit contradicting witness object"
      authority_required: null                 # No special authority needed to challenge
      evidence_required: true                 # Must provide evidence to challenge

  # Shared reality status
  shared_reality:
    status: UNVALIDATED | PARTIAL_CONSENSUS | FULL_CONSENSUS | CONTESTED
    validating_agents: []                     # Which agents have validated
    contesting_agents: []                     # Which agents have contested
    last_validation: <ISO-8601 UTC | null>

  # Dimension coverage
  reality_dimensions:
    historical: PRESENT | ABSENT | INFERRED
    legal: PRESENT | ABSENT | INFERRED
    political: PRESENT | ABSENT | INFERRED
    economic: PRESENT | ABSENT | INFERRED
    operational: PRESENT | ABSENT | INFERRED

  # Research coverage
  possibility_space:
    paths_explored: 0                         # RCI numerator
    paths_estimated: 0                        # RCI denominator
    rci: 0.0                                  # Research Coverage Index

  # Decision linkage
  decision_dependencies: []                   # Decisions that depend on this witness
  action_dependencies: []                     # Actions already taken based on this witness

  # Capability linkage
  capability_test:
    survives_implementation_change: null       # Not yet tested
    survives_adversarial_review: null          # Not yet tested
    survives_witness_loss: null                # Not yet tested

  # Integrity
  hash: "<sha256>"                            # Content hash for tamper detection
  previous_hash: "<sha256 of previous witness in chain | genesis>"
  chain_position: <integer>                   # Position in witness chain
```

---

## Lifecycle

```
DRAFT
  ↓ (validation)
VALIDATED
  ↓ (challenge)
CONTESTED → RESOLVED → VALIDATED
         → SUPERSEDED → replaced by new witness
  ↓ (time decay)
STALE → re-examination triggered
  ↓ (persistence)
SEALED → immutable but still re-examinable
```

A SEALED witness cannot be modified.
A SEALED witness CAN be challenged.
Challenge produces a NEW witness that references the SEALED one.

---

## What Makes It Different From Existing Artifacts

```
Memory Entry:
  "Store this for later reference"
  → passive, no challenge protocol

Evidence:
  "This supports a claim"
  → directional, not bidirectional

Research Report:
  "Here is what we found"
  → narrative, not traversable

Witness Object:
  "Here is what was observed, where it came from,
   what contradicts it, what would disprove it,
   and how to challenge it"
  → re-examinable, bidirectional, traversable, challengeable
```

---

## Conversion Protocol

Existing artifacts can be upgraded:

```
Memory Entry → add challenge_protocol, contradictions, provenance
Evidence → add contradicting_witnesses, falsification_criteria
Research Output → decompose into individual witness objects
Receipt → add reexamination protocol, shared_reality status
```

Not all artifacts need conversion.
Only artifacts that participate in governance decisions.

---

## Anti-Patterns

DO NOT:
- Create witness objects without source_chain (unprovenanced claims)
- Set confidence without confidence_basis (naked numbers)
- Leave contradictions array empty when contradictions exist
- Set shared_reality.status = FULL_CONSENSUS without multi-agent validation
- Seal a witness without reexamination protocol

DO:
- Accept low confidence when evidence is thin
- Preserve contradictions even when uncomfortable
- Mark reality_dimensions as ABSENT when coverage is missing
- Set rci = 0.0 when possibility space is unexplored
- Challenge any witness including the most senior

---

## Schema Versioning

v1 = current (2026-09-10)
Schema changes require F13 approval.
Additive fields: approved by 888.
Structural changes: require full re-examination of all consuming organs.

---

DITEMPA BUKAN DIBERI.
