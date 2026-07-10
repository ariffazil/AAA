# FALSIFIER-INTERFERENCE — Shared Geometry (Quantum × GEOX)

| Field | Value |
|-------|--------|
| seal_id | `FALSIFIER-INTERFERENCE::v1.0.0::2026-07-09` |
| status | **FORGED — pending F13 batch seal with 048 + AKAL-DICTIONARY** |
| vault999 | PENDING |
| owner | F13 SOVEREIGN — Muhammad Arif bin Fazil |
| forger | grok-build under F13 sequence (move 3) |
| code truth | `geox/src/geox_mcp/tools/biostrat_falsify.py` (8-gate engine) |
| companions | `GENESIS/048` · `QUANTUM_RUNTIME_ARCHITECTURE` · `🜂-qubit-substrate` · `AKAL-DICTIONARY` |

---

## 0. One-line lock

```
Falsifier ensemble = constructive / destructive interference on hypothesis amplitudes.
Popper single-kill  = destructive interference to zero on that claim path.
Quantum language and GEOX 8-gates name the same geometry.
```

Not metaphor shopping. **Shared vocabulary** so agents stop saying “quantum” in one room and “falsify” in another for the same move.

---

## 1. The 8 gates (OBS from live code)

| Gate | Name | What it attacks | Interference role |
|------|------|-----------------|-------------------|
| **G1** | Facies contradiction | Fossil ecology vs lithology/env | Destructive if ecology ⊥ facies |
| **G2** | Stratigraphic impossibility | Age ordering violation | Destructive if order breaks |
| **G3** | Taxonomic audit | Mis-ID, synonymy drift | Destructive / dampen confidence |
| **G4** | Reworking / caving | Transport ≠ in situ | Destructive on “in place” amplitude |
| **G5** | Diachroneity | False basin synchrony | Destructive on time-slice claims |
| **G6** | Seismic mismatch | Age claim vs stratal geometry | Cross-channel interference (earth wire) |
| **G7** | Sequence strat mismatch | Bioevent vs stacking | Destructive on systems-tract story |
| **G8** | Regional tectonic mismatch | Age vs unconformities/events | Destructive on regional narrative |

**Popper rule (code + doctrine):** one FALSIFIED gate → overall **FALSIFIED**, regardless of how many gates PASS.  
Geometry: **one destructive path to amplitude 0 on the claim** — not a soft average.

Verdicts per gate / overall: `PASS` · `FALSIFIED` · `UNFALSIFIABLE` · `HOLD`.

---

## 2. Shared geometric dictionary

| Quantum term | GEOX / arifOS term | Operational meaning |
|--------------|--------------------|---------------------|
| Hypothesis amplitudes \(\alpha_x\) | Competing claims / facies stories | Hold k≥3 when material |
| Superposition | Ensemble of live hypotheses | Do not pick one early |
| Unitary / legal evolution | Physics-bound forward / floor-legal path | No silent unit/CRS loss |
| **Constructive interference** | Independent evidence_for aligned | Raise weight of surviving path |
| **Destructive interference** | Gate FALSIFIED / evidence_against | Kill or collapse path weight |
| Missing amplitude | HOLD / UNFALSIFIABLE / UNKNOWN | Do **not** invent weight (F7) |
| Measurement | Well-tie verdict · claim SEAL · 888 | Classical readout only under AKAL |
| Decoherence | Operator override without witness; scar leak | Re-anchor — don’t “measure harder” |
| Norm preservation (ideal) | Same inputs → same receipt | Deterministic re-run |
| Noise / approx | Mistie RMS, QC flags, uncertainty band | Declare; never hide |

---

## 3. Amplitude update (software geometry, not hardware)

For claim path \(x\) with amplitude \(\alpha_x\):

```text
# After gate i produces polarity s_i ∈ {+1 support, 0 mute, −1 falsify}
# and strength w_i ∈ [0,1]:

α'_x  ←  α_x  ·  ∏_i  (1 + s_i · w_i · g_i)     # g_i = gate reliability ∈ (0,1]

# Popper hard kill:
if any gate verdict == FALSIFIED:
    α'_x  ←  0
    claim_path  ←  FALSIFIED

# Soft HOLD (insufficient test power):
if all gates PASS-or-HOLD and any HOLD:
    do not promote to SEAL; keep superposition

# Normalize surviving ensemble only when comparing peers:
P(x) = |α_x|² / Σ |α_j|²
```

**Notes (F2):**

- This is a **runtime prescription** for agents and tools, not a claim that GEOX stores complex Hilbert RAM.
- Code today returns discrete gate verdicts; continuous \(w_i\) may be DERIVED from gate notes — label DER/INT.
- UNFALSIFIABLE → treat as **zero constructive credit** (too vague to gain amplitude).

---

## 4. Constructive vs destructive — worked patterns

### Destructive (kill path)

```
Claim: "NN zone X in situ in coal facies"
G1 FALSIFIED (marine microfossils vs coal)
→ α = 0 → path dead → do not SEAL story
```

### Constructive (raise path)

```
Claim H1 and H2 both open
Independent: mistie RMS PASS + facies PASS + tectonic PASS on H1
→ constructive boost on H1; H2 unchanged or damped by G6/G7 mismatch
→ still no SEAL until measurement boundary + AKAL
```

### Mute / HOLD (no invention)

```
G3 PASS-with-note "synonymy uncertain"
→ widen Ω₀; do not invent high α for cleanliness of narrative
```

---

## 5. Ensemble as circuit, not checklist theater

```
SUPERPOSE   hypotheses {H1..Hk}
EVOLVE      only physics-legal / floor-legal transforms
INTERFERE   run G1..G8 (or domain-analog gates) as amplitude shapers
MEASURE     emit PASS/FALSIFIED/HOLD/UNFALSIFIABLE + receipt
AKAL        if action beyond report → 4-gate permit required
```

Checklists that always “mostly pass” without single-kill respect are **classical additive theater** — same failure mode as mean-scoring G.

---

## 6. Domain generalization (not only biostrat)

Biostrat 8-gates are the **reference ensemble**. Other GEOX domains map the *roles*, not necessarily the same names:

| Role | Biostrat example | Well-tie / seismic analog |
|------|------------------|---------------------------|
| Facies/physics fit | G1 | Log–synth polarity, Vp bounds |
| Order / time | G2, G5 | T-D law, mistie RMS gate |
| ID integrity | G3 | Horizon naming lineage |
| Transport / artifact | G4 | Multiples, acquisition footprint |
| Cross-geometry | G6 | Stratal termination vs pick |
| Stacking / systems | G7 | Sequence template match |
| Regional frame | G8 | Tectonostrat chart |

New ensembles must declare gate list + Popper/AND rule **before** first SEAL-grade use.

---

## 7. Anti-patterns

| Pattern | Why VOID |
|---------|----------|
| Average of 8 gates as “score 7/8 = SEAL” | Breaks Popper / destructive zero |
| Collapse to favorite facies before gates | Premature measurement |
| Treat UNFALSIFIABLE as soft PASS | Vague claims gain illegal amplitude |
| Call interference without evidence_for/against | Language without geometry |
| SEAL after interference without AKAL | Measurement without authority |
| Equate gate fail with “decoherence” | Fail = destructive measure channel; decoherence = drift |

---

## 8. Cross-links

| Doc | Role |
|-----|------|
| `geox/.../biostrat_falsify.py` | Executable 8-gate engine |
| `GENESIS/048` §3 Interference row | Doctrine map |
| `AKAL-DICTIONARY.md` | Commit gate after interference |
| `quantum-kernel-runtime` / `🜂-qubit-substrate` | Agent procedure |
| `QUANTUM_REALITY.md` | Corrections 1–3 |

---

## 9. Attestation

```
falsifier_interference=v1.0.0
gates=G1..G8
popper_single_kill=on
shared_vocab=quantum×geox
amplitude_model=software_geometry
```

---

*Forged 2026-07-09 — one geometry, two names, zero theater.*
