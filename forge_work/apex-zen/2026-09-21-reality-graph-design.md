# Reality Graph — Design + Projection

> **Status:** DRAFT 2026-09-21 (design + projection primitive)
> **Operator:** FI-008 kimi-code @ forge VPS (KVM8) (OBSERVE_ONLY)
> **Time:** 2026-09-21 ~02:00 MYT
> **Trigger:** "Reality Graph is the missing connective tissue"

---

## The Invariant

> **Reality Graph ≠ Reality.**

It is the federation's time-indexed, provenance-bound, **challengeable** MAP of reality.

```
REALITY  >  OBSERVATION  >  EVIDENCE  >  REALITY GRAPH
       >  DERIVED STATE  >  MODEL  >  NARRATIVE
```

If the graph disagrees with a fresh observation: **GRAPH LOSES.**
Never alter reality interpretation to preserve graph consistency.

---

## The Canonical Object

Every persistent claim about reality is a `RealityAssertion`:

```python
RealityAssertion {
    assertion_id         # uuid
    subject              # what is this about
    predicate            # the property
    object               # the value

    epistemic_class      # OBS / DER / INT / SPEC / SEAL
    confidence           # 0.0 - 1.0

    # BITEMPORAL — both required
    valid_from           # when became true in world
    valid_until          # when stopped being true (None = still valid)
    observed_at          # when observed
    recorded_at          # when written to graph

    source_refs          # URLs/paths/refs (no values, only refs)
    evidence_refs        # evidence (logs, hashes, snapshots)
    actor_id             # who recorded

    authority_scope      # OBSERVE_ONLY / MUTATE / SEAL

    falsifier            # how to falsify this assertion
    supersedes           # assertion_ids this replaces
    contradicted_by      # assertion_ids that contradict this

    freshness            # fresh / aging / stale / unknown
    privacy_scope        # internal / shared / public
    trace_id
}
```

---

## Minimum Node Ontology (12)

```
ENTITY           # something that exists
ACTOR            # something that acts
ARTIFACT         # something made/manipulated

OBSERVATION      # captured measurement
CLAIM            # asserted proposition
EVENT            # something that happened
STATE            # snapshot of attributes at time T

EXPECTATION      # forward-looking claim
ACTION           # performed change
OUTCOME          # observed result of action

DECISION         # chosen path
RECEIPT          # proof of consequence
```

---

## Minimum Edge Ontology (16)

```
ABOUT
OBSERVED_BY
ASSERTED_BY
SUPPORTED_BY
DERIVED_FROM

PRECEDES
SUPERSEDES
CONTRADICTS

TRIGGERED
ACTED_ON
CAUSED
RESULTED_IN

EXPECTED
VERIFIED_BY
FALSIFIED_BY

AUTHORIZED_BY
EXECUTED_BY
WITNESSED_BY
```

---

## The Critical Edge Data Rule

Every edge answers:

```
WHO says this?
WHAT evidence?
WHEN observed?
HOW fresh?
WITH what uncertainty?
UNDER what authority?
CAN it be falsified?
```

So an edge isn't merely:

```
A --CAUSES--> B
```

It should behave like:

```
A --CAUSES--> B
  claim_class = DERIVED
  confidence = 0.71
  observed_at = ...
  source_refs = [...]
  falsifier = ...
  valid_from = ...
  valid_until = ...
```

> "An unqualified edge becomes dogma very quickly."

---

## What Exists Already (the JOIN candidates)

| Federation record | becomes RealityAssertion |
|---|---|
| arifOS /health response | per-attribute OBS (status, source_commit, built_commit, deployed_commit, drift) |
| git HEAD per repo | OBS (subject=repo, predicate=git_head) |
| git status --porcelain count | OBS (subject=repo, predicate=dirty_count) |
| CHRON predictions.jsonl | OBS (subject=prediction:ID, predicate=status) |
| canary receipts | OUTCOME (subject=canary:SVC, predicate=verdict) |
| federated receipts (JSON) | RECEIPT |
| drift_log.jsonl entries | OBS (subject=organ, predicate=drift) |

**The mapping is mechanical. The graph becomes the JOIN.**

---

## The Live Drift Regression (the worked example)

Two RealityAssertions:

```python
O1 = observation(
    subject="arifOS-runtime", predicate="convergence", object="ALIGNED",
    actor_id="arif_init",
    source_refs=("curl http://127.0.0.1:8088/health",),
    evidence_refs=("source_commit=e8e6f93", "built_commit=e8e6f93",
                   "deployed_commit=e8e6f93", "drift=false"),
    observed_at="2026-09-21T01:37:00+08:00",
)
O2 = observation(
    subject="arifOS-runtime", predicate="convergence", object="DRIFTED",
    actor_id="arif_init",
    source_refs=("curl http://127.0.0.1:8088/health",),
    evidence_refs=("source_commit=e8e6f93", "built_commit=eeed6ce",
                   "deployed_commit=e8e6f93", "drift=true"),
    observed_at="2026-09-21T01:51:00+08:00",
)
```

With edges:
- `O2 --PRECEDES--> O1` (reversed: O1 precedes O2 in time)
- `O2 --CONTRADICTS--> O1`

The graph then answers automatically:

> "What changed between 01:37 and 01:51 that caused the convergence assertion to flip from ALIGNED to DRIFTED?"

Answer is derivable from the bitemporal trail + the source_refs pointing at `/health` response + the evidence_refs pointing at the build_commit change.

No paradox. **Reality simply changed.**

---

## Files Produced

| path | purpose |
|---|---|
| `/root/AAA/lib/reality_graph.py` | canonical dataclass + graph + reconcile |
| `/root/AAA/lib/reality_graph_projection.py` | existing federation → RealityAssertions |
| `/root/forge_work/reality-graph-projection.json` | 37 assertions + 9 edges (live snapshot) |

---

## Live Test Results

```
arifOS /health:       5 assertions (status, source_commit, built_commit, deployed_commit, drift)
git state (4 repos):  8 assertions (git_head + dirty_count per repo)
CHRON predictions:    20 assertions (per-prediction status projection)
Recent canary:         4 assertions (per-receipt verdict projection)

Total: 37 assertions, 9 PRECEDES edges
```

Self-test:
- RealityAssertion dataclass: PASS
- RealityEdge dataclass: PASS
- RealityGraph: PASS
- observation() factory: PASS
- reconcile() — graph loses to fresh observation: PASS
- contradiction marking: PASS
- predecessor walk: PASS
- bitemporal valid_from/valid_until: PASS

---

## The Five Future Emergences (now substrate-ready)

### 1. Contradiction becomes computable
Today: detector A says HEALTHY, detector B says DRIFT — agent reasons manually.
Reality Graph: CONTRADICTS edge with bitemporal provenance — queryable, falsifiable.

### 2. Impact propagation
SECRET_X compromised → traverse USED_BY → service → EXPOSES → external → ENABLES → capability. Blast radius = reachable subgraph.

### 3. Causal learning
ACTION → OUTCOME → DELAYED OUTCOME → SECOND-ORDER CONSEQUENCE — CHRON adds time, FRAME adds witness, HERMES prevents interpretation inflation.

### 4. Counterfactual reasoning
Disable reconciler X → which downstream observations disappear? Grounded in actual dependency edges, not LLM speculation.

### 5. Attention routing
event → affected objects → blast radius → authority required → reversibility → materiality. A0/A1/A2/A3 as graph routing consequence.

---

## What's NOT yet built (correctly held)

| capability | status | next step |
|---|---|---|
| Persistent storage | ✓ in-memory + JSON dump | migrate to Postgres + FalkorDB graph |
| Auto-derive assertions from organ outputs | ✓ projection primitive built | wire each organ to emit assertions on /health |
| Query language | ✗ | design a small graph query DSL |
| Bitemporal join logic | partial (predecessor walk only) | implement full supersession/contradiction traversal |
| Federation-wide ingestion | ✗ | one organ at a time, after canary substrate ready |
| Graph-aware canary contracts | ✗ | canary contracts should read from graph, not static URLs |
| Graph-aware drift-check | ✗ | drift-check should consume graph, not duplicate observations |

---

## The Architectural Leap

```
Before: many observations, few joins
After:  many observations + time + receipts + witness + contradiction + authority = JOIN possible
Future: agents query projections of the same evidence graph; federation stops passing prose between intelligent organs
```

DITEMPA BUKAN DIBERI ⚒️
