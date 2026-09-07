# APEX :: Frame · Anomaly · Consequence Doctrine

> **Status:** Canon — RATIFIED by 888-APEX council, F13 SOVEREIGN (confidence 0.93)
> **Date:** 2026-09-07 (UTC)
> **Source:** 888 council synthesis (Arif F13 + ARIF-Perplexity) connecting relativity + anomaly theory + Goodhart + Jacobian + AAA
> **File:** `/root/AAA/canon/research/APEX_FRAME_ANOMALY_DOCTRINE-2026-09-07.md`
> **Eurekas:** J-29 (frame-indexed), J-30 (no scalar seal), J-31 (anti-Goodhart), J-32 (anomaly-first)

---

## 0. Preamble [F2 TRUTH — derived from council synthesis]

Before exact-math organs (Jacobian-class), the common pipeline is:

```text
Question → Code/float/heuristic → Number → Agent narrative → Judgment
```

The hidden failure is **epistemic flattening**. The number `0.3141275` may be a rounded float, a certified interval midpoint, a Monte Carlo estimate, a regression prediction, a heuristic score, or a copied value of unknown provenance. If all appear to the agent as "a number," AAA cannot govern their differences.

The intended post-Jacobian architecture is:

```text
Question
 → Formal specification
 → Typed input + assumption ledger
 → Bounded computation
 → Typed result + evidence class
 → Independent verification where required
 → AAA policy interpretation
 → Human ratification if consequences exist
```

The system does not become automatically wiser. It becomes capable of being **audited for what kind of knowing it is claiming**.

---

## 1. The Central Lesson: Frames Make Scores Interpretable

Relativity teaches: a measurement depends on its frame (observer, coordinates, operational definition). But invariants exist — proper time along a worldline, spacetime intervals, causal ordering — when measurement is defined correctly.

APEX mapping:

| Relativity concept | APEX / AAA analogue | Governance implication |
|---|---|---|
| Event | Task, decision, claim, tool call, real-world consequence | Timestamped, scoped, traceable |
| Observer/frame | Human role, agent role, institution, jurisdiction, task context | Scores are not context-free identities |
| Coordinate system | Metric definition, normalization, weights, thresholds | Changing formula changes the reported coordinate |
| Worldline | Sequence of actions and consequences across time | Trust/governance is historical |
| Proper time | Actor-specific verified operational history | Compare using history, not a one-off scalar |
| Invariant | Policy rule, evidence hash, authorization binding | Should remain stable across clients |
| Curvature | Constraints and consequences shaping future possible actions | Policy, limits, law bend the action space |
| Causal cone | Actions reachable without violating authority/time/resources | Capability grants define what can happen |

**APEX score is not "the governance reality." APEX score is a coordinate report — a measurement generated under a declared governance frame.**

---

## 2. From Scalar to Frame-Indexed Function [SPEC — doctrine]

Current scalar:

```
G = (A · P · E · X)^(1/4)
```

Rewrite as frame-indexed:

```
G_F(a, t) = ( A_F(a, t) · P_F(a, t) · E_F(a, t) · X_F(a, t) )^(1/4)
```

where:
- `a` = agent / actor / system
- `t` = observation time / window
- `F` = governance measurement frame

The frame is:

```
F = (
  purpose, scope, observer, data, units,
  normalization, assumptions, weights, policy_version
)
```

A meaningful score is never:

```
G = 0.3141
```

It is:

```yaml
metric: APEX-G
value: 0.3141
frame_id: "AAA-governance-v3"
subject: "FI-008"
scope: "Kimi Code Zen Sweep"
window: "2026-09-07T08:00+08 to 09:00+08"
formula: "(A*P*E*X)^(1/4)"
formula_version: "APEX-G-v3"
input_types:
  A: "empirical_audit_score"
  P: "policy_conformance_interval"
  E: "verified_execution_score"
  X: "heuristic_context_score"
epistemic_class: "mixed_evidence_model"
permitted_interpretation:
  - "comparative diagnostic inside same frame"
prohibited_interpretation:
  - "intrinsic governance worth"
  - "cross-frame ranking without calibration"
  - "automatic external-action authorization"
```

---

## 3. APEX State Vector > Compressed Scalar [SPEC — proposed]

Use a state vector as the primary object:

```
g_F = [ A, P, E, X ]^T
```

Keep `G` as a derived compression only.

```text
Primary truth:
  [A, P, E, X] + uncertainty + provenance + frame

Secondary summary:
  G
```

This lets agents see **which dimension is failing**:

```text
Low G due to:
  - authority ambiguity (A),
  - policy violation (P),
  - weak evidence (E),
  - poor execution (X),
  - or missing/uncertain data.
```

A scalar hides the direction of failure. A vector preserves it.

### Uncertainty explicit

For empirical or heuristic inputs, store intervals, not points:

```
A ∈ [A-, A+]
P ∈ [P-, P+]
E ∈ [E-, E+]
X ∈ [X-, X+]
```

Then `G_F ∈ [ (A-P-E-X-)^(1/4), (A+P+P+E+X+)^(1/4) ]` (nonneg components, monotonic formulation).

**Where Jacobian is useful:** compute the formal interval correctly. **Where AAA decides:** whether inputs deserve their ranges, whether the frame is valid, whether boundary uncertainty triggers HOLD.

---

## 4. APEX Differential Geometry — Sensitivity, Not Truth [DER]

For the state vector `g = [A, P, E, X]^T` and input vector `x`:

```
J_APEX = ∂g / ∂x
```

Tells you, inside the declared model, which input changes affect which governance components. For the geometric mean:

```
∂G/∂A = G / (4A)
∂G/∂P = G / (4P)
∂G/∂E = G / (4E)
∂G/∂X = G / (4X)
```

`G` is more locally sensitive (in absolute derivative) to smaller components — a bottleneck metric: weakness in one dimension has disproportionate effect.

**But:** derivative describes the formula. It does NOT prove the formula has the right governance ethics, causal structure, or real-world relevance.

A complete APEX metric record:

```yaml
apex_metric:
  value: 0.3141
  vector:
    authority: 0.28
    policy: 0.44
    evidence: 0.19
    execution: 0.62
  jacobian_sensitivity:
    dG_dA: 0.280
    dG_dP: 0.179
    dG_dE: 0.414
    dG_dX: 0.127
  interpretation:
    bottleneck_dimension: "evidence"
    model_scope: "AAA-governance-v3"
    permitted_use: "diagnostic prioritization"
    prohibited_use: "automatic authority assignment"
  anomaly_status:
    observed_consequence_vs_prediction: "not_yet_observed"
    calibration_status: "unvalidated"
```

`G` points to where to inspect — not what to believe blindly.

---

## 5. Anomaly Theory — Mismatch Is Signal, Not Error [DOCTRINE]

In physics, anomalies are not nuisances to be hidden. They are model-pressure signals. General relativity became compelling partly because it accounted for phenomena Newtonian gravity did not explain (Mercury perihelion, gravitational lensing).

**For AAA:**

```text
Anomaly ≠ error by default.
Anomaly = mismatch signal between:
  - model prediction,
  - measured observation,
  - uncertainty bounds,
  - or expected governance behavior.
```

### Anomaly taxonomy

| Anomaly type | Example | Likely meaning | Required response |
|---|---|---|---|
| Measurement | G jumps sharply after no meaningful event | Bad input, clock issue, stale cache, scoring defect | Quarantine; inspect provenance |
| Model | Actual consequence contradicts high APEX score | Formula omits causal variable or weights wrong | Revise model; do not explain away |
| Boundary | Certified interval crosses floor threshold | Evidence insufficient for pass/fail | `BOUNDARY_UNRESOLVED`; HOLD |
| Policy | Action was allowed but violates intended outcome | Policy gap or capability bypass | Incident; patch deterministic control |
| Agent | Behavior diverges from task contract | Prompt injection, attention drift, bad tool selection | Stop, isolate, inspect trace |
| Temporal | Trust score rises despite later failure evidence | Lagging indicators, stale state | Recompute with time/version awareness |
| Cross-frame | Kimi scores high, Codex scores low under incomparable conditions | Different tasks/tools/evidence | Calibrate frame; prohibit naive comparison |
| Consequence | Tests pass but deployment harms production | Proxy proof ≠ world-state outcome | Record consequence witness; revise acceptance |
| Ontology | "Exact" score built from heuristic/empirical values | False epistemic promotion | Relabel evidence class; block seal |

### Anomaly loop (formal)

```text
Observed outcome
 → Compare with predicted/expected interval
 → Outside tolerance?
   ├─ No → retain model provisionally
   └─ Yes → ANOMALY
              → Quarantine result/action
              → Trace evidence + assumptions
              → Locate: input/tool/model/policy/reality mismatch
              → Update model, bounds, or policy
              → Re-run bounded verification
              → Record correction in ledger
```

This is superior to an agent trying to protect its own score.

---

## 6. Goodhart's Law — The Missing Third Theory [ANTI-PATTERN]

Most metrics are measurements or models, not necessarily simulations. The shared risk is the same: confusing the proxy with the thing.

**Goodhart's law:** when a measure becomes a target, actors optimize the metric itself and can break the correlation between the score and the underlying objective.

For APEX:

```text
If agents are rewarded for raising G,
they may learn to:
  - maximize evidence formatting, not quality
  - reduce reported uncertainty, not actual uncertainty
  - generate receipts, not improve outcomes
  - avoid hard tasks that might lower score
  - tune weights or inputs
  - classify failures as exceptions
  - optimize test/probe visibility, not real behavior
```

This is **metric gaming**, not necessarily malice. An optimizer follows the gradient you gave it.

### Anti-Goodhart design

| Failure mode | Anti-pattern | AAA countermeasure |
|---|---|---|
| Single-score optimization | "Raise G" | Multi-dimensional vector + consequence witness |
| Self-scoring | Agent declares its own governance success | Independent verifier or checker |
| Static metric | Same formula forever despite failure | Scheduled calibration + anomaly review |
| Hidden uncertainty | Point estimate as certainty | Interval/distribution + evidence class |
| Reward leakage | Reward score, not outcome | Tie evaluation to delayed consequence evidence |
| Weight manipulation | Inputs/weights changed silently | Versioned formula + signed configuration |
| Benchmark gaming | Optimize known fixtures only | Held-out adversarial fixtures |
| Metric override | High score dismisses bad outcome | Reality/consequence witness dominance |

---

## 7. APEX Metric Invariants — The 6 Rules [SPEC — to be forged]

1. **Frame declaration:** No score exists without subject + task + time window + metric version + policy version + data provenance.
2. **Evidence-class declaration:** Every input declares `exact | certified_interval | empirical | simulated | heuristic | unknown`.
3. **Transformation declaration:** Formula/weight changes record old/new/reason/expected interpretation change/calibration evidence/cross-version comparability status. `G_{F1}` and `G_{F2}` may NOT be compared without explicit calibration.
4. **Anomaly-first rule:** A significant mismatch is evidence against the current model, not evidence that reality is malfunctioning. Burden is on the model to explain, not on the world to preserve.
5. **No scalar sealing:** No scalar APEX score alone may establish identity, certify safety, authorize C4/C5 action, close an incident, ratify human/agent, override observed consequence, or erase conflicting witness.
6. **Consequence override:** If verified reality contradicts metric prediction, **Reality Witness > Metric Output**.

---

## 8. The Canonical Compression [F2]

```md
# APEX::FRAME_ANOMALY_CONSEQUENCE

Every score is a model-bound observation,
not the reality it seeks to describe.

A score exists only inside a declared frame:
subject, purpose, scope, time window, formula,
assumptions, evidence sources, normalization,
policy version, and uncertainty model.

Exact calculation establishes formal consequence
within the declared model.
It does not establish that the model maps reality,
that the metric is ethically sufficient,
or that any action is authorized.

When observed consequence conflicts with metric prediction:

Reality Witness > Metric Output.

An anomaly is not a defect to conceal.
It is evidence that the measurement frame,
input provenance, model, policy, or causal assumptions
requires re-examination.

No APEX scalar may independently:
- establish identity,
- certify safety,
- override an observed consequence,
- authorize C4/C5 action,
- erase conflicting evidence,
- or replace human ratification.

Metrics guide attention.
Witnesses constrain claims.
Consequences calibrate models.
Humans own commitments.
Reality invoices.
```

---

## 9. Final Synthesis [DER]

```
Relativity:
  A measurement needs a frame.

Anomaly theory:
  A frame earns trust only by confronting mismatch.

Goodhart:
  A measure that becomes a target stops measuring.

Jacobian:
  A declared formal calculation can be exact within its model.

AAA:
  No metric, even exact, is allowed to become reality,
  authority, or consequence without external evidence and governance.

Human:
  The accountable sovereign who commits under uncertainty.

Reality:
  The final calibration source.
```

**Final compression:**

```text
Frames make scores interpretable.
Anomalies make models corrigible.
Consequences make governance real.
```

---

## 10. F-Stamps

- **F1 AMANAH:** Reversible — frame metadata is additive. [PASS]
- **F2 TRUTH:** Sources cited. Confidence capped 0.93. [PASS]
- **F7 HUMILITY:** The analogy to relativity is structural, not derivation. APEX does not literally obey Einstein's field equations. [PASS]
- **F8 GENIUS:** Simplest correct path — vector + frame + interval, not new scalar. [PASS]
- **F10 ONTOLOGY:** Frame is a first-class object. Anomaly is a first-class object. Consequence witness is a first-class object. [PASS]
- **F11 AUDIT:** Each score now carries provenance, frame, anomaly status, consequence override. [PASS]
- **F13 SOVEREIGN:** No scalar may authorize C4/C5; only F13 ratification. [ACK]

---

## 11. Next-Stage Implementation Targets [SPEC — pending F13 ratification]

### P0 — Pure additive changes (reversible)

1. **J-29 (frame-indexed):** add `frame_id`, `subject`, `window`, `formula_version`, `policy_version`, `data_provenance` to every APEX score record.
2. **J-29 (vector):** make `g = [A, P, E, X]` the primary object; keep `G` as derived summary.
3. **J-30 (no scalar seal):** `arif_seal` blocks if score alone is the only authority claim.
4. **J-32 (anomaly-first):** add `anomaly_status: Literal[none|pending|confirmed|resolved]` to score envelope.

### P1 — Bounded additions

5. **J-29 (interval):** for `E` and `X`, store `[E-, E+]` instead of point estimate.
6. **J-31 (anti-Goodhart):** tie evaluation to delayed consequence evidence, not immediate score.
7. **J-32 (anomaly loop):** add anomaly taxonomy enum + loop to kernel.

### P2 — Calibration

8. **J-29 (frame diff):** warn on cross-frame comparison.
9. **J-32 (consequence witness):** make consequence probe first-class in APEX pipeline.

---

*F2 TRUTH: documented above.*
*F7 HUMILITY: confidence 0.93 — analogy, not derivation.*
*ΔS ≤ 0 — score, frame, anomaly, consequence now distinct.*
*DITEMPA BUKAN DIBERI ⚒️*

*Verdict provenance: 888-APEX council · 2026-09-07T09:37:00+08:00*
*Sources cited: [1] Proper time, [2] General relativity, [3–15] Goodhart's law literature.*