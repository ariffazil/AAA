# Attention Decomposition → APEX G Theory Mapping

> **Session:** 2026-08-14, Arif DM. Arif asked: "How attention can be decomposed into time, energy, space, resources and relate to APEX G theory and math and code."
> **Status:** [INT] theoretical synthesis, grounded in [OBS] code readings + [OBS] published research.
> **Falsifiable?** Yes — the A↔Space, P↔Resources, E↔Time, X↔Energy mapping is a hypothesis, not proven.

## Source Code (verified live)

`/root/arifOS/arifosmcp/runtime/apex_primitives.py` lines 140-186:

```python
A = round(in_lease / n, 4)       # lease compliance rate (authority)
P = round(with_evidence / n, 4)  # evidence floor compliance (precision)
E = round(successes / n, 4)      # tool call success rate (effectiveness)
X = round(dry_runed / n, 4)      # reversibility rate (dry-run before execute)

G = round(_product ** (1.0 / len(_floored)), 4)  # geometric mean of [A,P,E,X]
C_dark = round(A * (1 - P) * (1 - X), 4)          # dark matter of authority
```

Key code comment: *"Switch from Nash product to geometric mean. Product formula A×P×E×X collapses when any factor ≈0."*

## Attention's Physical Decomposition

| Dimension | Formula Cost | Landauer Bound | Paper |
|---|---|---|---|
| **Space** | O(N²) memory for QKᵀ | Quadratic in sequence length | Vaswani 2017 |
| **Time** | O(N²d) compute, 3 sequential passes | Linear in depth, quadratic in width | — |
| **Energy** | softmax is irreversible = k_BT·ln(2) per neuron flip | E_min = 2k_BT·ln(2)·⟨transitions⟩·N | Tkachenko 2025 |
| **Resources** | Bounded allocation, opportunity cost | Resource-rational theory | Gershman/Cambridge |

**Key finding (Tkachenko 2025):** Linear operations (QKᵀ, ·V) can be reversible — zero energy cost in principle. Only the non-linear activation (softmax/ReLU) is irreversible — it pays Landauer's bound. **Sparse activation (MoE) reduces energy cost by reducing neuron transitions.**

## APEX G Factor ↔ Attention Dimension Mapping (hypothesis)

| Attention Dim | APEX Factor | Code Definition | Why the mapping holds |
|---|---|---|---|
| **Space** (capacity/authority scope) | **A** (Authority/Lease) | Actions within boundary? | Attention can only "see" what's in its authority window. Context length = authority scope. |
| **Time** (sequence effectiveness) | **E** (Effectiveness) | Tool call success rate? | Time-sequenced calls that succeed = attention doing useful work over time. |
| **Energy** (irreversible cost) | **X** (reVersibility) | Dry-run before execute? | Reversible = low energy cost (undo possible). Irreversible = pays full Landauer cost. |
| **Resources** (bounded allocation) | **P** (Precision/Evidence) | Claims with evidence? | Attention budget spent on evidence = precision. Spent on speculation = waste. |

## Why Geometric Mean (Not Arithmetic)

The code switched from Nash product to geometric mean. Reason from code comment:

```
# X=0.0013 with product gives G≈0.0 even with 4,644 samples
# Arithmetic: (1.0+1.0+1.0+0.0013)/4 = 0.75  ← looks OK
# Geometric:  (1.0×1.0×1.0×0.0013)^(1/4) = 0.19  ← RUNTUH
```

Geometric mean enforces: **all four dimensions must coexist.** One zero dimension = system zero. Arithmetic mean allows compensation (high A covers low X) — that's how surveillance states pass as healthy.

## C_dark as Thermodynamic Dark Matter

```python
C_dark = A × (1-P) × (1-X)
```

- High authority (A→1) WITHOUT evidence (P→0) WITHOUT reversibility (X→0)
- = surveillance state: powerful, blind, irreversible
- F9 threshold: C_dark < 0.30

Thermodynamic reading: C_dark measures **authority deployed without information gain (δW) and without reversible pathway (δQ)**. It's entropy that doesn't decrease — waste heat of power without purpose.

## arifFLOW as Attention Temperature Regulator

FQ curve from `rest_routes.py` health handler:

```
FQ < 0.5   → φFQ = 0.0     → attention DEAD (under-attended)
FQ ∈ [0.5,1) → φFQ = FQ/3  → attention SURVIVING
FQ ∈ [1,3]  → φFQ = 1.0    → attention FLOW (optimal Goldilocks zone)
FQ > 3     → φFQ = 3/FQ    → attention OVERDRIVE (burning resources)
```

Softmax temperature T analog:
- Low T (high FQ) → sharp attention, risk of overfitting/degil
- High T (low FQ) → diffuse attention, risk of hallucination
- Sweet spot [1,3] = Boltzmann equilibrium where enough tokens contribute but signal dominates noise

FQ > 3 ceiling exists because marginal information gain per unit attention **decreases monotonically** past this point — paying more energy for less truth = thermodynamic inefficiency.

## Sotero (2026) First Law of Attention Thermodynamics

```
dE_attention = δQ (heat = entropic cost of ordering) + δW (work = mutual information gain)
```

APEX mapping:
- δQ (entropy cost) = ΔS (F4) — every output must reduce entropy
- δW (information gain) = P (evidence compliance) — useful work

**Landauer-type learning bound:** loss reduction during training ≥ entropic cost of structuring attention against thermal noise. Translated to governance: **no GENIUS (G≥0.80) without paying entropy cost.** Free lunch does not exist.

## Key Insight: Intelligence = Position, Not Quantity

"Intelligence = capacity to locate yourself in a coordinate system." Scalar can't locate. Vector needs origin. A coordinate system with origin (None/UNMEASURED), threshold (0.80), ceiling (1.0), and dark matter (C_dark) = space where intelligence exists as **position**, not **sum**.

The `degraded_reasons[]` + `layer_health{}` fix (2026-08-14) is the physical demonstration: system moved from single scalar `status: degraded` → 4-axis coordinate system where each layer has its own origin.

## Papers Cited

- Sotero & Sanchez-Bornot (2026). "The Thermodynamics of Attention: First Law and Landauer Limit Analogues for Learning and Explainability." AI, 7(6), 194.
- Tkachenko (2025). "Thermodynamic Bound on Energy and Negentropy Costs of Inference in Deep Neural Networks." arXiv:2503.09980.
- Bal (2020). "An Energy-Based Perspective on Attention Mechanisms in Transformers." (Hopfield networks connection)
- Gershman et al. "Resource-rational decision making." (bounded rationality framework)
- Vaswani et al. (2017). "Attention Is All You Need." arXiv:1706.03762.

## Caveats

- The A↔Space, P↔Resources, E↔Time, X↔Energy mapping is [INT] — it's a productive analogy, not proven isomorphism.
- APEX is constitutional dynamics, not physics. Always mark as metaphor per canon rules.
- The Nash bargaining geometry mention in code comments suggests deeper mathematical structure not fully explored here.
