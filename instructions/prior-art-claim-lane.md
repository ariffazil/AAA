# PRIOR-ART CLAIM LANE — NOV / PRIORITY

Status: DRAFT_AWAITING_F13 (2026-10-20). Owner: GEOX (555_COMPUTE_ONLY). Scope: any artifact claiming novelty, priority or "first".

## 1. Why this lane exists

Every other claim lane in the federation answers *"is it true?"* (observed / derived / interpreted / hypothesis).
None answers *"is it ours first?"* — so novelty assertions travel with zero evidence, because no field exists to fail.

A novelty claim is a claim about the state of the literature, not about the rock. It needs its own lane, its own
default, and its own regime of failure.

## 2. Lane definition

`claim_type: novelty` — carries a mandatory `prior_art` object:

```
prior_art:
  status: UNSEARCHED | PARTIAL | EXHAUSTIVE
  searched_sources: [ ... ]     # named databases/indexes actually queried
  exhaustive: false             # true only when sources list is defended, not merely long
```

Default on creation: `status: UNSEARCHED`, `confidence: UNKNOWN`.

## 3. Three states, three permissions

- **UNSEARCHED** (default) — claim may exist internally. Any "first ever", "nobody has proposed", "novel method"
  is FORBIDDEN in every artifact, public or internal. Formulation may still be described on its own merits.
- **PARTIAL** — sources named, gaps named. Wording allowed: "no prior test of this specific configuration was
  found in <sources>". Wording forbidden: "first", "nobody".
- **EXHAUSTIVE** — sources and closure argument are defensible. "First" still requires the closure argument
  (what was searched, why that set is sufficient), not the length of the list.

## 4. What is never a novelty claim

- The existence of a geological feature ("igneous exists in Sabah") — that is a regional fact claim.
- A broad possibility ("intrusions may exist in the deep section") — too wide to carry priority.
- Universal methodology (multi-hypothesis testing, falsification, inversion) — predates us by decades.
- A specific parameterised, falsifiable configuration tested against named independent observations on a named
  transect — THIS is claimable, and only as provenance of the artifact, not as geological truth.

## 5. Two verdicts, never merged

HOLD on geological truth · SEAL on provenance of the formulation.
A novelty claim can never upgrade a truth class. A truth class can never license a novelty claim.

## 6. Gate

Bind with GEOX `geox_claim` and the basin claim registries (`/root/GEOX/resources/basins/*/claims.json`).
Any public artifact asserting priority without a `novelty` claim at PARTIAL or better = defect, not style.
