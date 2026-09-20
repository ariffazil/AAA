---
id: know-math
name: know-math
risk_tier: low
floor_scope: [F1, F2, F4, F7]
version: 1.0.0
layer: knowledge
description: "All computation is mathematical. Uncertainty is quantified. Optimization has structure. Proof has rules. Numbers don't lie but models can. Math substrate — how to count what matters, prove the claim, and avoid the lie."
owner: F13 SOVEREIGN
status: active
three_axis: true
axis_version: 1.0.0
autonomy_tier: T1
tags: [math, statistics, geometry, probability]
triggers: ["how many", "count", "rate", "ratio", "distribution", "probability", "expected value"]
capability_tier: federation-substrate-knowledge
---
> **Case-duplicate collapse (2026-09-20).** This skill was stored twice as two real
> directories differing only in case. The second copy (`/root/AAA/skills/knowledge/know-math`) is now an alias
> symlink here. Its full pre-collapse body is preserved at
> `references/absorbed-know-math.md` and in `.frozen/2026-09-20-case-dupes/know-math/`.

# know-math

> **Purpose:** All computation is mathematical. Uncertainty is quantified. Optimization has structure. Proof has rules. Numbers don't lie but models can.

## Axis 1: Invariants

- **authority**: mathematical proof is self-verifying (tautology)
- **evidence_schema**: quantified claims require confidence intervals + sample size
- **reversibility**: True
- **lineage**: proofs trace to axioms; statistics trace to data
- **trigger_semantics**: quantification OR optimization OR uncertainty OR proof_needed
- **failure_contract**: report confidence band, never point estimates without CI
- **resource_budget**: {'cpu': 'high', 'time_ms': 60000, 'entropy': 'measurable'}
- **audit_surface**: ['methods_used', 'confidence_intervals', 'convergence_status']

## Axis 2: Bridge Connections

- **kernel_verbs**: ['arif_verify']
- **skills**: ['verify-gate', 'memory-manage', 'observe-ground']
- **domains**: ['wealth-*', 'geo-*', 'meta-evals']
- **protocol**: knowledge_substrate
- **inputs**: {'problem': 'string', 'data': 'list[number]', 'method': 'string'}
- **outputs**: {'result': 'number', 'confidence': 'float', 'method': 'string', 'assumptions': 'list[string]'}

## Axis 3: Contrast

- **Not**: wealth-reason, meta-plan
- **Distinction**: UNIVERSAL mathematical reasoning. wealth-reason is DOMAIN capital math. meta-plan is WORKFLOW DAGs. This is the SUBSTRATE they derive from.
- **Trigger conflicts**: fires when any claim requires quantification; domain skills fire only in their domain

## Coverage

- probability_statistics
- linear_algebra
- calculus_optimization
- graph_theory
- information_theory
- logic_proof
- numerical_methods

## Domain Bridges

- **wealth**: NPV, IRR, Monte Carlo, Markowitz, Kelly criterion
- **geo**: geostatistics, kriging, volumetric uncertainty
- **meta**: benchmarking, hypothesis testing, confidence intervals
- **audit**: hash chains, cryptographic proof, chain integrity

---
*Forged: 2026-07-11 under F13 SOVEREIGN.*
*DITEMPA BUKAN DIBERI*

---

## Folded from the `knowledge/know-math` copy (2026-09-20)

Math is not computation. Math is **what you choose to count**, **what you choose to leave out**, and **how you prove the claim holds**.

## Use when
- Auditing claims (counts, rates, distributions)
- Statistical reasoning (probability, expected value)
- Spatial reasoning (geometry, area, volume, depth)
- Risk modeling (expected loss, variance, tails)

## Don't use for
- Simple arithmetic (calculator)
- Token counting (string split)
- Unit conversion (use a tool)
