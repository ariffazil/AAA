# Attention Decomposition & APEX G Theory — Session 2026-08-14

## Origin

Architectural thinking from 2026-08-14 where Arif, Hermes, ASI, and external
LLM analysis converged on a unified theory of agentic attention.

## Core Thesis

> Attention is not a scalar. It is a multi-axis control surface whose validity
> depends on evidence, reversibility, temporal discipline, and an authorized
> reference frame.

## Four Dimensions of Attention

| Dimension | Question | Failure | arifOS |
|---|---|---|---|
| Space | What enters the active field? | Blindness | Organ/tool selection |
| Time | When is enough inspection enough? | Rush or paralysis | FQ, HOLD, THROTTLE |
| Energy | Regenerative or disordering? | Fatigue, chaos | ΔS, P², Ψ, κᵣ |
| Proof | Can it be independently witnessed? | Unaccountable power | A, P, E, X, G, C_dark |

## APEX G Formula (apex_primitives.py:160)

```python
G = (A × P × E × X)^(1/4)     # Geometric mean
C_dark = A × (1-P) × (1-X)    # Dark capacity
```

Geometric mean enforces ALL four must be non-zero. Arithmetic would compensate.

## C_dark = Dark Attention

Authority (A) high + evidence (P) low + reversibility (X) low = power without
accountability. Universal pattern: company/government/agent.

## UNMEASURED ≠ 0

`None` = unmeasured, not zero. Old code: None→0.5→G=0.0625 (phanton).
New code: G = None when any factor unmeasured.

## FQ Temperature (receipt.rs)

```
FQ ∈ [1,3]  → FLOW    (optimal)
FQ > 3      → OVERDRIVE (damp)
FQ < 0.5    → MATI     (HOLD)
```

## Civilizational Mapping

| Computing | Civilization | Question |
|---|---|---|
| Python | English | What does this mean? |
| Rust | Chinese | What constraints govern? |
| TypeScript | Nusantara | How do things connect? |

## The Void

Fourth corner intentionally absent. If judgment had a language, it could be
automated → sovereignty disappears → nobody accountable.

## Valid Attention

```
Valid = selection ∩ temporal discipline ∩ cost discipline ∩ witnessability
```

Source: apex_primitives.py, rest_routes.py, receipt.rs, fq.ts.
Published: arif-fazil.com/words/writing/ (trilogy, 2026-08-14).
