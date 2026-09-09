# Contradiction Ledger v1

**Sealed:** 2026-09-10T02:00+08
**Status:** SEAL (canonical specification)
**Classification:** Constitutional — contradiction is signal, not noise

---

## Purpose

Contradictions between witness objects are the highest-value data points in the system.

This ledger tracks, preserves, and manages contradictions.
Contradictions are never deleted.
Contradictions are never suppressed.
Contradictions are never treated as errors.

---

## Core Principle

```
No witness = obvious weakness
Unchallengeable witness = institutionalized weakness

Contradiction between claim and action = highest-value signal
```

---

## Contradiction Entry

```yaml
contradiction_id: "cx-<uuid>"
created_at: <ISO-8601 UTC>

# The witnesses in tension
witness_a:
  id: "wo-<uuid>"
  claim: "<compressed claim>"
  truth_class: OBS | DER | INT | SPEC

witness_b:
  id: "wo-<uuid>"
  claim: "<compressed claim>"
  truth_class: OBS | DER | INT | SPEC

# Nature of contradiction
contradiction_type:
  FACTUAL        # A says X, B says not-X
  TEMPORAL       # A says before, B says after
  CAUSAL         # A says X causes Y, B says X causes Z
  ATTRIBUTION    # A says actor is X, B says actor is Y
  NORMATIVE      # A says should, B says should not
  SURFACE_ACTION # A says "not contemplating", B files lawsuit

# Epistemic assessment
severity: LOW | MEDIUM | HIGH | CRITICAL
  LOW = both could be partially correct
  MEDIUM = one is likely wrong
  HIGH = one must be wrong
  CRITICAL = core system assumption challenged

# Evidence mapping
evidence_for_a:
  - source: <source>
    reliability: <0.0-1.0>
evidence_for_b:
  - source: <source>
    reliability: <0.0-1.0>
missing_evidence:
  - description: "<what would resolve>"
    acquisition_path: "<how to get it>"

# Resolution tracking
resolution_status:
  UNRESOLVED | PARTIALLY_RESOLVED | RESOLVED | SUPERSEDED

resolution_path:
  RESOLVED_BY_EVIDENCE: "<which evidence settled it>"
  RESOLVED_BY_EXPERIENCE: "<reality provided answer>"
  RESOLVED_BY_CONSENSUS: "<agents agreed>"
  PARTIALLY_RESOLVED: "<what was resolved, what remains>"
  SUPERSEDED: "<new contradiction replaced this one>"
  UNRESOLVED_OPEN: "<attached to reality model as open question>"

# Reality dimension impact
dimension_impact:
  historical: AFFECTED | UNAFFECTED | UNKNOWN
  legal: AFFECTED | UNAFFECTED | UNKNOWN
  political: AFFECTED | UNAFFECTED | UNKNOWN
  economic: AFFECTED | UNAFFECTED | UNKNOWN
  operational: AFFECTED | UNAFFECTED | UNKNOWN

# System linkage
discovered_during: <session_id | research_id | judgment_id>
witness_graph_position:
  - "<how this contradiction connects to other contradictions>"
```

---

## Contradiction Types — Detailed

### SURFACE_ACTION (Highest Value)

```
Entity says X.
Entity does Y.
X and Y are incompatible.
```

This type reveals:
- Gap between public narrative and private decision
- Institutional dishonesty or strategic ambiguity
- Hidden force maps
- Real priority signals

### FACTUAL

```
Witness A: "Revenue is RM10B"
Witness B: "Revenue is RM8B"
```

May indicate:
- Different measurement periods
- Different accounting standards
- Data error
- Deliberate misreporting

### TEMPORAL

```
Witness A: "Event occurred in March"
Witness B: "Event occurred in June"
```

May indicate:
- Memory drift
- Different event definitions
- Chronological manipulation

### CAUSAL

```
Witness A: "Policy X caused outcome Y"
Witness B: "Policy X caused outcome Z"
```

May indicate:
- Confounding variables
- Multiple causal chains
- Attribution error

---

## Ledger Operations

### Record

Every contradiction is recorded.
No deletion. No suppression.
Even if later resolved — record preserved.

### Query

```
By witness ID:     find all contradictions involving this witness
By type:           find all SURFACE_ACTION contradictions
By severity:       find all CRITICAL contradictions
By status:         find all UNRESOLVED contradictions
By dimension:      find all contradictions affecting legal dimension
By time:           find all contradictions discovered in last 30 days
```

### Aggregate

```
System-wide contradiction count
Unresolved contradiction count
Critical contradiction count
Most-contradicted witness (highest contradicting_witnesses count)
Most-active contradiction source (entity that generates most contradictions)
Dimension coverage gaps (which dimensions have most unresolved contradictions)
```

---

## Contradiction as Research Driver

When conducting research:

```
1. Discover witness objects
2. Check contradiction ledger for existing contradictions
3. Search for NEW contradictions
4. Record all contradictions found
5. Contradictions guide next research direction
   (highest-severity unresolved = research priority)
```

Contradictions are not obstacles to research completion.
Contradictions are the research compass.

---

## Integration with Other Systems

### With forge_judge

Judgment MUST reference relevant contradictions.
Judgment that ignores known contradictions = unreliable.

### With arif_memory

Memory stores witness objects.
Contradiction ledger provides relationship graph between them.
Memory without contradiction ledger = archive.
Memory with contradiction ledger = living reality model.

### With forge_witness (tri-witness)

Tri-witness consensus can be challenged by contradictions.
If witness A has tri-witness PASS but contradiction ledger shows CRITICAL unresolved contradiction against it — confidence reduced.

### With Reality Model (EUREKA-15)

Unresolved contradictions appear as open questions in Reality Model.
Decision points are often located AT contradictions.

---

## Anti-Patterns

DO NOT:
- Delete contradictions to "clean up"
- Suppress contradictions from low-authority sources
- Auto-resolve contradictions without evidence
- Treat contradiction count as failure metric
- Ignore SURFACE_ACTION contradictions (highest value)

DO:
- Welcome contradictions as system health
- Track contradiction resolution over time
- Use contradictions as research priority signals
- Preserve contradiction history even after resolution
- Feed unresolved contradictions into Reality Model

---

## Metrics

```
Total contradictions recorded
Unresolved count
Critical unresolved count
Mean time to resolution
Contradiction discovery rate (per research session)
Dimension coverage gaps
Most-contested witness count
```

These are HEALTH metrics, not failure metrics.
A system with zero contradictions is not healthy.
A system with zero contradictions is not examining reality.

---

DITEMPA BUKAN DIBERI.
