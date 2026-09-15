# ADDENDUM 2 — Interior reconciliation, first pass (evidence-led)

**Authority:** F13 ARIF · **Executor:** Hermes (edge bridge) · 2026-09-15

---

## A. The reviewer's third path — already live, and now sharpened

Proposal: register H1–H4 as claims **with the KT-7 PENDING state written in as a constraint**,
so nothing is sold as runnable and the record self-upgrades when velocity is published.

**Status: done before the proposal arrived, now complete.**
`CLM-NWS-004..007` each carry `KT_7_depth_conversion_BLOCKED_velocity_unresolved` in
`missing_tests`, the blocked test in `falsifier`, and the H1 residual ambiguity stated explicitly.

**Added now:** `CLM-NWS-008` — the decision test itself, as a first-class claim record. It carries
the blockers, the partial discrimination power, the downstream confidence effect, and an explicit
`auto_upgrade_condition`.

---

## B. Granite age — RESOLVED. My earlier call was too strong; correction below.

**What I told ARIF earlier:** "granite age bercanggah tiga hala" (three-way contradiction).
**What the evidence now shows:** it is **one orphan string**, not a three-way split.

| Source | Value | Status |
|---|---|---|
| `thermal_history.py` (GEOX code) | Zircon U-Pb **7.85 Ma**, Cottam et al. 2013 | **Correct** |
| External literature (Cottam 2013; Gilligan 2026) | crystallisation **7.85–7.22 Ma** | **Correct** |
| Dossier Act 4 | **9.5–7.0 Ma** | **Coherent** — spans melt-onset to crystallisation |
| Ledger chronology | 9.5 = decompression melting *begins*; 7.0 = emplacement | **Coherent** |
| `sabah_prospect_discriminator.py:369` | "Kinabalu Granite **10-13.7 Ma** intrusion" | **ORPHAN — no source** |

`10-13.7` occurs **exactly once in the entire federation** — a free-text note string. No dataset,
no citation, no sibling file. Its own sibling module contradicts it, and so does the literature.

**Verdict:** the dossier and ledger are consistent with each other and with published
thermochronology. The defect is a single unsourced string in the discriminator's notes list.
That is a one-line correction, not a modelling dispute — and materially smaller than I first said.

**Not applied.** It is a GEOX production-code string; the repo is git-tracked and reversible but
this was outside the approved scope. Fix ready, held for one word from ARIF.

---

## C. KT-7 geometry — the "12–21 km" figure has no home in the federation

Searched all of `geox/`, `src/`, `resources/`, `okf/`: **zero** occurrences of `12–21 km`.

| Source | Geometry | Vp |
|---|---|---|
| `sabah_prospect_discriminator.py` | high-Vp body at **6–8 km** | unresolved (PENDING) |
| `CLM-NWS-002` (pre-existing claim) | **6.5–7.0 km/s** at basinward edge | 6.5–7.0 km/s |
| Franke et al. 2008 (via Sidek 2016) | crustal profile, **Moho ~22 km** | — |
| External dossier | KT-7 at **12–21 km** | 5.0–6.5 km/s |

Reading, held at INTERPRETATION: the federation's supported geometry is a shallow high-Vp body
(6–8 km) with Moho ~22 km from Franke's own refraction profile. The dossier's 12–21 km is
unsourced internally and its Vp range also disagrees with the code that cites the same paper.

**Not resolved** — resolving it needs Franke et al. 2008 full text, which is paywalled. What is
established: **the contradiction is dossier-vs-federation, not federation-internal.** Two
federation sources agree with each other; one external document disagrees with both.

---

## D. Corrected defect register (supersedes D6 in `01_`)

| # | Defect | Was | Now |
|---|---|---|---|
| D6 | Granite age | "three-way contradiction" | **One orphan string** (discriminator :369) — dossier+ledger+literature+thermal_history all agree |
| D10 | `10-13.7 Ma` orphan note | undiscovered | **NEW** — single unsourced string, one-line fix ready |

---

## E. Sequencing — accepted, with one amendment

Reviewer votes **1 → 2 → 3**, ledgers last so caveats absorb today's findings. Reasoning is sound.

Amendment: **2 is largely done already** (see §C). What remains of it is a literature fetch on
Franke 2008, not an analysis task. So the live order is:

1. Reconciliation patch (held — sealed ledger, F13)
2. KT-7 geometry resolution (evidence gathered; needs Franke 2008 full text)
3. Mag/grav reprocess for H3 (the only test that can start clean today)
4. Ledger consolidation — last, absorbing everything above ✅

---

DITEMPA BUKAN DIBERI ⚒️
