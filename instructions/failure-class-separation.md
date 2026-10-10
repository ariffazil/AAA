<!-- F13_SAHH_2026-10-06 23:5x MYT · CONSTITUTIONAL · TIER A -->
<!-- DITEMPA BUKAN DIBERI — forged, not given -->
<!-- Companion to apex-geometry-substrate (canonized same session): semantics precede geometry -->

# Failure-Class Separation — Diagnosis Semantics Law

> **Status:** F13_RATIFIED_CANON · Tier A · 2026-10-06
> **Author:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Compiler:** FI-003 (333-AGI, DECODER)
> **Full canon:** `/root/AAA/canon/FAILURE-CLASS-SEPARATION-2026-10-06.md`
> **Cross-ref:** apex-geometry-substrate · apex_theory SABAR · evidence-hierarchy

## 0 · TL;DR (3 baris)

**Schema failure ≠ Authorization failure ≠ Execution failure. Malformed ≠ Denied ≠ Absent.** A malformed request cannot be used as evidence of an authorization boundary, just as a HOLD verdict cannot be used as evidence of operational failure. **Before improving geometry, verify that the semantics of the observables are clean.**

## 1 · The three failure classes (never collapse)

| Class | Meaning | A rejection proves |
|---|---|---|
| **Schema failure** | malformed request, validation reject | only that the request failed validation |
| **Authorization failure** | policy denial (lease/authority/band) | that policy said no — not that capability is absent |
| **Execution failure** | capability attempted and errored | a real defect or absence |

Collapsing them into one bucket called "denied" is the diagnosis-layer form of verdict-pollution: same category error, different layer. It manufactures false correlations and false architecture conclusions.

## 2 · Probe discipline (one narrow probe)

- A probe with a **tiny result space** (validation / policy / execution / success) is a clean falsifier.
- **Bundled probes mix assumptions** (filesystem + cache + bus + path + auth) — when the bundle fails, you learn almost nothing.
- One narrow probe is better science. Escalate to wider probes only after each class is separated.

## 3 · Bootstrap semantics (demonstrate, never infer)

```text
identity bootstrap → session issuance → execution lease
```

These are separable powers. A genuine circular dependency ("need SCT to obtain SCT") must be **demonstrated by probe**, not inferred from a rejection. Until demonstrated, classify as `POSSIBLE CIRCULAR BOOTSTRAP GATE` — never `CONFIRMED DEFECT`.

## 4 · SABAR, mathematically

"Measurement quality is insufficient to support the proposed action" IS SABAR — not "nothing works" but **residual too large for confident projection** (see apex-geometry-substrate: r = s_observed − s_predicted). Scope stays limited until semantics are known; operator diagnosis precedes infrastructure change.

## 5 · Provenance (2026-10-06)

- Verdict-pollution (arifOS): all 1,292 evidence-"failures" were HOLD/SABAR verdicts, zero errors → outcome-semantics split, commit `eede91678`, deployed live (E 0.803→0.9842).
- Same day, diagnosis layer: schema-reject misread as authorization boundary caught before it became architecture. One law, two layers: **observables must mean what they say before they are correlated, projected, or acted on.**

DITEMPA BUKAN DIBERI.
