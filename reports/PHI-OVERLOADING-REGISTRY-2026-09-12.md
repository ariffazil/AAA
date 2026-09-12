# PHI-OVERLOADING REGISTRY — 2026-09-12

> **Status:** DRAFT (evidence base for D-05 semantic migration)
> **Forged:** 2026-09-12 by kimi-code/FI-008, from live source grep across arifOS + A-FORGE
> **Authority:** Arif Fazil (F13) — D-05 "retire bare Φ"
> **Law:** *A shared symbol is not a shared ontology.* Identity must be governed before measurement can be trusted.

---

## Principle

Bare `Φ` (and `Phi`/`phi`) has been found denoting **≥12 non-equivalent objects** across the federation. A value crossing an organ boundary under the same glyph silently changes meaning. This registry is the evidence base for the D-05 rename.

**Qualified names (D-05, F13-directed):** `scarPressure`, `triWitness` (W³), `textToGPV`, `entropyBuffer`, `paradoxConductance`.

**Exempt (bounded-domain / already-qualified — do NOT rename):** `φ` = porosity (GEOX `PHYSICS_9_SPEC.md`), `φ` = variational free-energy latent (K777), `φFQ/φZ/φE` (FLOOR_TABLE — already namespaced).

---

## Registry

| # | Surface | Location | Meaning | Correct name | Status |
|---|---|---|---|---|---|
| 1 | `apex_canonical.py compute_Phi` | arifOS runtime | tri-witness ∛(H·AI·Ext) | `triWitness` / `W³` | **RENAMED** (`compute_tri_witness`, alias kept) |
| 2 | `evaluate.ts estimatePhi` | A-FORGE | scar pressure 1−Σ(scar·severity) | `scarPressure` | **RENAMED** (`estimateScarPressure`) |
| 3 | `decisionField.ts` G=Q·V·Ψ·Φ | A-FORGE | wisdom (scar-adjusted) | `scarPressure`/`wisdom` | OPEN (separate instrument) |
| 4 | `okf/apex-flow.md`, `ZEN.md` | arifOS okf | falsification rate (hyperedge, arity 3) | `falsificationRate` | OPEN (documentation) |
| 5 | `GENESIS/INVARIANTS.md` | arifOS | Φ_SEAL / Φ_SABAR decision functions | `sealScore`/`sabarScore` | OPEN (documentation) |
| 6 | `GENESIS/045` | arifOS | Kernel/law layer (Ψ/Δ/Φ) | `lawLayer` | OPEN (documentation) |
| 7 | `K111_PHYSICS.md`, `CANONICAL_SPEC.yaml` | arifOS | paradox conductance Φ_P = (∫ΨP dt)/(ΔP·Ω₀) | `paradoxConductance` | OPEN (documentation) |
| 8 | `FLOOR_TABLE.json` | arifOS | φFQ/φZ/φE metabolic gates | (already qualified) | EXEMPT |
| 9 | `K777_APEX.md` | arifOS | φ free-energy latent q(φ) | (domain) | EXEMPT |
| 10 | `PHYSICS_9_SPEC.md` | A-FORGE/GEOX | φ porosity (0–1 void) | (domain) | EXEMPT |
| 11 | `agentic-ci.yml` | A-FORGE | Φ CI clarity/build-health % | `buildClarity` | OPEN |
| 12 | `okf/atlas333/router.md` | arifOS | Φ(text)→GPV transform | `textToGPV` | OPEN (documentation) |

---

## Enforcement

- **CI guardrail:** `arifOS/.pre-commit-config.yaml` (commit `a14e0d529`) blocks bare `Phi`/`phi` in governance paths; allows qualified names + historical/domain markers.
- **Residual (arifOS runtime):** 0 bare `Phi` identifiers, 3 historical Greek `Φ` (lines 68, 469, 661 of `apex_canonical.py` — all `HISTORICAL`/`LEGACY`).
- **Remaining:** items #3–8, #11, #12 are documentation or separate-instrument Φ, deferred to a follow-on D-05 pass (or F13 direction).

---

*DITEMPA BUKAN DIBERI — identity precedes governance.*
