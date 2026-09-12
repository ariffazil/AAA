# Φ Overloading Registry — Federation-wide Naming Audit

> **Status:** EVIDENCE_RECEIPT (not a ratification, not a migration)
> **Forged:** 2026-09-12 by 333-AGI Δ MIND — read-only source audit
> **Request:** sovereign migration-sequence step 2 — "Create a Φ registry"
> **Method:** grep across `arifOS/arifosmcp`, `arifOS/core`, `A-FORGE/src` (non-build, non-doc)
> **DITEMPA BUKAN DIBERI**

---

## Two corrected facts (supersede prior turn)

### F-1 · D-04 (constitutional 4-vs-5-factor split) is REFUTED

The live constitutional path is **already 4-factor**, not 5-factor.

- `arifOS/arifosmcp/runtime/apex_canonical.py:527` → `G = (A * P * E * X) ** (1 / 4)`
- `apex_canonical.py:639-647` → `compute_G` returns `(a*p*e*x) ** (1/4)`, Φ excluded
- Git: `303cb8ad8 fix(apex): W-12 canonical G formula — 4-factor geometric mean (A·P·E·X)^(1/4)` (2026-08-05)
- `arif_init` runtime_verify: source == built == deployed == `f375f910af53`, drift: false

The shim's cross-organ drift notice (`apex_c_dark.py:14-20`, "arifOS still computes 5-factor A·P·E·X·Φ") is **stale** — it predates commit 303cb8ad8 and was never updated. Turn-1 propagated this stale comment as fact; it is not fact.

**What Φ actually is in the constitutional path now:** a *separate verdict gate*, not a dial. `compute_Phi` (line 243-270) computes tri-witness `∛(H·AI·Ext)`; it is never multiplied into G; it only forces VOID when zero (`_determine_verdict:597`).

**Remaining real issue:** `apex_canonical.py` carries stale *metadata* that still narrates the 5-factor world:
- `:67` `APEX_EQUATION = "G = A · P · E · X · Φ"`
- `:463` docstring `G_raw = A · P · E · X · Φ`
- `:546` axiom `# 2. Five-sufficient — we have exactly 5 primitives`
- `:13` `Sealed: 2026-07-13` (pre-dates the 08-05 fix)

### F-2 · Φ overloading is real and LARGER than claimed (≈10 meanings, not 4)

The sovereign's 4-way taxonomy is correct in spirit, wrong in detail. Two of the four claimed meanings are confirmed; one does not exist; ~6 additional meanings were found.

---

## The Registry

| # | Meaning | Evidence | Verdict influence? |
|---|---|---|---|
| 1 | **Φ = tri-witness** `∛(H·AI·Ext)` | `apex_canonical.py:243-270` (`compute_Phi`) | YES — zero ⇒ VOID |
| 2 | **Φ = "scar pressure gate"** (label) | `apex_canonical.py:9` header | *labels #1; conflicts with it* |
| 3 | **Φ = wisdom / scar-law alignment** | `kernel/apex_decision_field.py:27` → `G34 = Q·V·Ψ·Φ` | YES — decision-field G |
| 4 | **Φ = "Integration"** (5th factor) | `runtime/apex_c_dark.py:137,384` → `G = A·P·E·X·Phi` | DEAD shim only |
| 5 | **Φ = text→GPV transform** `Φ = Θ∘Λ` | `core/shared/atlas.py:8,25`; `runtime/mind_reason.py:272` `Phi(query)` | NO (cognitive) |
| 6 | **φ = ATLAS philosophy selector** | `runtime/kernel_core.py:522-528` `select_atlas_philosophy` | NO (quote object) |
| 7 | **Φₚ = paradox conductance** | `core/judgment.py:77,163-167` `Φₚ=(Δₚ·Ωₚ·Ψₚ·κᵣ·Amanah)/(Lₚ+Rₘₐ+Λ+ε)` | YES (deliberative) |
| 8 | **φ_external = Gödel-lock external witness** | `runtime/godel_lock_gate.py:177,228+`; `godel_lock_enforcement.py:157-175` | YES — Q9a/Q9c anti-self-cert |
| 9 | **φ = porosity** (geoscience) | `runtime/geox_bridge.py:376-381` `"key":"phi", max 0.4 v/v` | NO (petrophysics) |
| 10 | **φ = marginal-clarity conductance** | `runtime/marginal_clarity_gate.py:70,211` `_compute_phi(state)` | YES (clarity gate) |
| 11 | **Φ = scar wisdom factor** (membrane) | `runtime/membrane.py:73` `phi: float = 1.0 # scar wisdom` | YES (membrane) |
| 12 | **Φ = apex primitives scalar** (dashboard) | `runtime/apex_primitives.py:193,239` `"Phi": PHI` | NO (telemetry) |

### Claimed but NOT found

- **"Φ = thermodynamics entropy buffer"** — no Φ/phi/entropy-buffer symbol exists in `thermo_estimator.py`, `thermodynamics_hardened.py`, `thermo_budget.py`, or `entropy_gate.py`. This mapping does not exist in source. (Nearest real analog: #10, marginal-clarity conductance — a different thing.)

### The sharpest finding — an internal label conflict in the constitutional file itself

`apex_canonical.py` cannot agree on what its own Φ is:
- Header `:9` → "Φ = scar pressure gate"
- `compute_Phi` `:249` → "Φ — Witness (Tri-Witness): Φ = ∛(H · AI · Ext)"

Scar pressure (historical caution) and tri-witness (present consensus) are **different categories**. The same file labels Φ as both. This is the naming-doctrine violation in its purest form — inside the canonical source.

---

## Verdict (this artifact)

- **D-04 constitutional split:** REFUTED — 4-factor is the deployed canonical G. No F13 branch needed for *which formula*; that was sealed 2026-08-05.
- **Φ ontology collision:** CONFIRMED, ~10-way. Real, consequential, and the correct F13/HOLD_888 target.
- **D-01 (E sub-dial nesting):** still OPEN — but note it lives in A-FORGE's *local* path (`apexDials.ts`), not the constitutional G.
- **D-02 (squared-drag stale header):** still OPEN, T1 doc fix.
- **D-03 (threshold fragmentation):** still OPEN — now at least *three* profiles (`evaluate.ts` 0.80/0.50, `calculateGeniusFromFloors` 0.80/0.70, `apex_canonical.py` SEAL 0.80 / SABAR 0.50 / DEGRADED 0.30).

---

*Registry is evidence, not authority. Migration remains HOLD_888 pending F13 direction.*
