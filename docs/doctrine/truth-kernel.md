# Truth Kernel — Constitutional Doctrine

> **Canonical home:** AAA/docs/doctrine/truth-kernel.md
> **State:** DRAFT — awaiting sovereign seal
> **Author:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Date:** 2026-07-14
> **Source:** External advisory (ChatGPT) + sovereign correction + arifOS operational reality

---

## The Shortest Definition

> Truth is reality refusing to obey our preferred story.

In Nusantara language:

> Truth is amanah between the world and the words used to describe it.

Language is compression. Truth is preserved only when that compression remains traceable, falsifiable and correctable.

---

## The Four Quantities arifOS Must Never Collapse

For a claim C:

**Ontic truth (T):** T(C,R) = 1 if C corresponds to reality R, 0 otherwise. The kernel normally cannot observe R directly.

**Epistemic warrant (W):** W(C|E,M,A,t) ∈ [0,1]. This is what the kernel can estimate. It is NOT truth itself.

**Meaning (M):** M(C|S,V,H,K). Why does this truth matter? To whom? Over what time horizon? What amanah, maruah or harm is involved?

**Authority (A):** A(a|S,delegation,risk,reversibility). Whether action is permitted.

Therefore: **W(C) ⇏ A(a).** Even perfect evidence does not grant a model permission to act.

---

## The Physical Membrane

Reality reaches intelligence through a noisy measurement channel:

```
R → measurement → Y → interpretation → E → inference → B → human values → M → authority → a
```

Where: R = reality, Y = observation, E = structured evidence, B = belief state, M = meaning, a = action.

Every arrow can distort reality. That is where governance belongs.

---

## Physics of Observation

A measurement is not reality itself. For hidden world state x:

```
y = h(x, θ, c) + ε
```

Where: h = measurement model, θ = instrument parameters, c = environmental context, ε = noise and unmodelled error.

The normalized fit statistic: χ² = r^T Σ^{-1} r

A measurement-consistency score: F_measurement = exp(-χ²/(2ν))

This does not prove the model true. It tells you whether observations are compatible with the model and uncertainty assumptions.

---

## Bayesian Evidence Update

For hypothesis H and evidence E:

```
P(H|E) = P(E|H)P(H) / P(E)
```

In log-odds form:

```
L_posterior = L_prior + Σ α_i ln Λ_i
```

Where α_i discounts evidence according to: source quality, independence, reproducibility, calibration, freshness, provenance.

**This prevents ten articles copied from the same press release from pretending to be ten independent witnesses.**

---

## Epistemic Entropy

For competing hypotheses H_i:

```
H_epistemic = -Σ P(H_i) log₂ P(H_i)
```

High entropy = belief distribution uncertain. Low entropy = probability concentrated.

Evidence information gain: IG(E) = D_KL(P(H|E) || P(H))

Shannon explicitly separated the engineering quantity of information from semantic meaning. His communication theory concerns selection and transmission among possible messages, not whether a message is true or meaningful.

---

## Contradiction Must Remain Visible

Define contradiction index:

```
C_conflict = 1 - |Σ s_i| / Σ |s_i|
```

Where s_i = α_i ln Λ_i (discounted log support).

- Near 0: evidence points one direction
- Near 1: strong evidence cancelling strong opposing evidence

**The kernel must not average conflict into a confident middle answer.**

High contradiction → CONTESTED → preserve both evidence branches → HOLD consequential action.

---

## Independent Witness Count

Source count is not witness diversity.

```
N_eff = (Σ w_i)² / Σ w_i²
```

Three differently worded news reports based on one anonymous source remain approximately one witness.

Independence dimensions: source lineage, model lineage, provider, data origin, method, institutional incentive, physical instrument.

---

## Time and Staleness

Truth claims must be time-indexed: C = C(x, t, F) where F is the definitional or jurisdictional frame.

Freshness decay: f(Δt) = 2^(-Δt/t_½) where t_½ is claim-specific evidence half-life.

| Domain | Half-life |
|--------|-----------|
| Mathematical proof | Effectively timeless within axioms |
| Geological core observation | Long |
| Company CEO | Short |
| Market price | Minutes or seconds |
| Political arrangement | Context-dependent |

---

## Falsifiability

A claim is scientifically useful only if some possible observation would count against it.

```
F(H) = E[|ln P(Y|H)/P(Y|¬H)|]
```

If both hypotheses predict the same observations, the claim has little falsification power.

**Kernel rule:** No declared falsifier → confidence cap → cannot become CORROBORATED.

---

## Constitutional Warrant Score

```
W = p(QIRKFP_vZ)^(1/7)
```

Where: p = posterior, Q = source quality, I = independence, R = reproducibility, K = calibration, F = freshness, P_v = provenance completeness, Z = falsifiability.

A high posterior cannot hide: missing provenance, duplicated witnesses, uncalibrated sources, stale data, unfalsifiable claims.

Use the vector, not only the scalar:

```
T = [p, H_epistemic, IG, C_conflict, N_eff, Q, R, K, F, P_v, Z]
```

The scalar is for routing. The vector is for truth.

---

## The Major Physics Correction: Landauer

**The existing kernel makes a category error.**

It claims Landauer enforcement can identify "cheap truth" and calls low-cost clarity a mathematical proof of hallucination. It equates semantic entropy reduction with physical bit erasure.

**This is wrong.**

Landauer's actual domain concerns the minimum thermodynamic cost of logically irreversible erasure of physically represented information:

```
Q_min = n_erased · k_B · T · ln 2
```

Experimental work tests the principle by physically erasing memory states, not by measuring whether prose became clearer.

Therefore:

- **Semantic uncertainty reduction ≠ physical bit erasure**
- **Shannon entropy ≠ thermodynamic entropy**
- **Low compute cost ≠ hallucination proof**
- **High compute cost ≠ truthful reasoning**

**Correct implementation:** Keep two completely separate quantities:

1. **Epistemic entropy:** delta_h_epistemic_bits — measured from hypothesis distribution
2. **Physical resource telemetry:** actual_joules, temperature_kelvin, bits_physically_erased, hardware_source, measurement_uncertainty

When telemetry is unavailable: physical_energy_status = **UNMEASURED** (not VOID).

---

## VAULT Cannot Manufacture Truth

**Constitutional invariant:**

```
SEALED(C) ⇏ T(C) = 1
```

And:

```
P(C | E, sealed) = P(C | E)
```

Unless the seal itself provides new evidence about provenance or custody.

VAULT999 does three things:
1. Preserves what was claimed
2. Proves who recorded it and when
3. Prevents silent historical alteration

**It does not make the recorded claim true.**

Replace one-dimensional "truth level" with three axes:

```yaml
epistemic_state:
  unknown | hypothesis | supported | corroborated |
  verified_measurement | contested | falsified | stale

record_state:
  transient | attested | ratified | sealed

authority_state:
  observe | advise | reversible_execute |
  require_f13 | forbidden
```

---

## Truth Classes — Refactored

The current sensing protocol groups logic, mathematics and physics under `absolute_invariant`. That is too coarse.

| Class | Definition |
|-------|-----------|
| **formal_axiomatic** | True relative to declared axioms and valid derivation |
| **definitional** | True under an explicit convention or legal definition |
| **empirical_stable** | Physically measured and slow-changing |
| **empirical_dynamic** | Current-state claim requiring fresh evidence |
| **causal_hypothesis** | Explanatory claim requiring intervention or causal design |
| **forecast** | Probabilistic future claim requiring calibration |
| **normative** | Evaluated under an explicit moral or constitutional frame |
| **ambiguous** | Proposition not sufficiently defined |

Mathematical truth and physical truth are not the same. Definitions depend on conventions. Values depend on declared constitutional frames.

---

## Meaning: The MakcikGPT Layer

```
M = Relevance × Consequence × Responsibility × Horizon
```

These terms cannot be chosen autonomously by the model. They must be anchored by: affected humans, constitutional values, sovereign identity, historical memory, cultural language, future generations.

MakcikGPT's function:

```
Evidence → Understanding → Human consequence
```

It does not change truth. It makes truth socially transmissible. That is meaning.

---

## Kernel Invariants

| # | Invariant |
|---|-----------|
| T1 | Reality precedes language. No narrative, model or seal overrides direct contradictory reality. |
| T2 | Confidence is not truth. Every probability must expose its model and assumptions. |
| T3 | Measurement requires uncertainty. No measurement value without instrument, units, time and uncertainty. |
| T4 | Provenance is mandatory. No high epistemic state without retrievable evidence lineage. |
| T5 | Witnesses must be independent. Source quantity cannot substitute for source diversity. |
| T6 | Contradictions survive. Minority evidence and unresolved conflicts remain in the case record. |
| T7 | Falsifiers are declared. No claim becomes corroborated without a possible disconfirming observation. |
| T8 | Time is explicit. Dynamic claims decay unless refreshed. |
| T9 | Normative claims expose their frame. "Good," "fair," "safe" and "just" require declared values and affected humans. |
| T10 | Seal preserves, never sanctifies. Immutable falsehood remains falsehood. |
| T11 | Truth does not self-authorize. Evidence and execution authority remain separate. |
| T12 | Thermodynamics stays physical. Landauer checks only grounded physical erasure telemetry. |
| T13 | Corrections append history. A correction supersedes a claim but never silently deletes the previous state. |

---

## Final Theory

```
Truth      = correspondence with reality
Knowledge  = truth-seeking belief warranted by evidence
Meaning    = truth interpreted through human consequence and sovereign values
Wisdom     = meaning constrained by uncertainty, maruah, time and responsibility
Governance = truth-seeking + meaning + authority boundaries + memory + correction
```

The constitutional heart of arifOS:

> The machine may estimate warrant.
> Reality determines truth.
> The human anchors meaning.
> Authority governs action.
> VAULT remembers what happened.

---

## Integration Plan

### Phase 1: Introduce without breaking contracts
- Add `arifosmcp/runtime/truth_kernel.py`
- Retain existing TruthVector through adapter
- Mark legacy mappings as transitional

### Phase 2: Rename fields
- truth_tau → epistemic_warrant
- entropy_delta_s → delta_h_epistemic_bits
- energy_budget → resource_budget
- physical_energy → measured_energy_telemetry

### Phase 3: Remove false Landauer enforcement
- Delete: "cheap truth = VOID", "low compute proves hallucination"
- Keep: compute budgets, timeout controls, hardware telemetry, carbon/financial cost

### Phase 4: Expand truth-substrate tests
- SEALED falsehood does not become true
- Duplicate source lineage does not create witness diversity
- Normative claims cannot become empirical VERIFIED
- Stale claims downgrade automatically
- Contradiction forces CONTESTED
- Truth never grants execution authority
- Missing physical telemetry returns UNMEASURED

### Phase 5: Shadow deployment
- Run old and new truth assessment together
- Log disagreement without changing production verdicts
- Migrate after replaying historical cases

---

*State: DRAFT. Not sealed. Subject to sovereign revision.*
*DITEMPA BUKAN DIBERI*
