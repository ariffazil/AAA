# S1 — SUBSURFACE & STATIC MODEL

**Field:** Limbayong (PSC: Limbayong + Bestari), Block G/J/R, NW Sabah, 5.888°N 114.510°E, water depth 900–1,200 m.
**Purpose:** test whether the 28 Aug 2026 sanction was right, on the static model alone.
**Data regime:** four appraisal wells since 2002 [M: SPE 210079-MS]; **no public seismic, no public logs, no public core, no public PVT.** Everything below is either the operator's published words, arithmetic on those words, or a named-analogue benchmark. Nothing is measured by me.

## HEADLINE

The operator has itself published the two numbers that decide this project: the trap is a **30 km × 2.5 km elongate toe-thrust ridge** (aspect ratio 12:1) with "**varying faults frequency, vertical intercalation of thin-bed, thick sand reservoir and lateral compartmentalization**", and IPA has graded it **industry top-decile reservoir complexity** — that is not an analyst's opinion, it is the sanctioning basis in PETRONAS Carigali's own SPE paper. My independent geometric rebuild lands at a P50 STOIIP of **517 MMbbl** and, at a 26% recovery factor, **134 MMbbl recoverable**, which reproduces the booked 139 MMbbl to within 4% — so the number is *internally honest* but sits exactly at P50, with a P90 downside of **51 MMbbl**. The static case is not wrong; it is **unhedged**: a 12:1 faulted ridge drained by 10 wells cannot deliver P50 recovery without lateral continuity that the same paper says is impaired.

## NUMBERS

### Table 1 — Static model, structure and rock

| Parameter | Value | Unit | Class | Basis |
|---|---|---|---|---|
| Structural province | NW Borneo Fold-Thrust Belt, deepwater toe-thrust trend | — | [M] | Khamis, Jong & Barker 2018, GSM Bull. 65, pp.1–12 — "L-B-P structural trend" (Limbayong–Bestari–P) |
| Trap type | Elongate thrust-cored anticline / hanging-wall culmination, dip-closed, fault-bounded at least one flank | — | [M] | SPE 210079-MS: "severe elongated structure … with varying faults frequency"; toe-thrust kinematics per GSM Bull. 65 |
| Structure length | 30 | km | [M] | SPE 210079-MS, 2022, abstract |
| Structure width | 2.5 | km | [M] | SPE 210079-MS, 2022, abstract |
| Aspect ratio | 12 : 1 | — | [D] | 30 ÷ 2.5 |
| Structural footprint | 75 | km² | [D] | 30 × 2.5 |
| Trap area at contact — P90 / P50 / P10 | 22 / 30 / 40 | km² | [A] | 29% / 40% / 53% of footprint; closure fraction for a faulted elongate ridge (analogue: Malikai, Gumusut-Kakap crestal areas) |
| Gross hydrocarbon interval — P90 / P50 / P10 | 70 / 80 / 110 | m | [A] | Stacked Upper Miocene Cycle V / Kinarut sands; analogue columns 60–150 m (Kikeh, GK) |
| Depositional model | Ponded turbidites between thrust ridges (syn-/post-kinematic) grading to unconfined fan sands (pre-kinematic) | — | [M] | GSM Bull. 65: syn- and post-kinematic deposition "deflect turbidite sand fairways, and trap turbiditic sand in between ridges forming ponded turbidites" |
| Reservoir age / interval | Upper Miocene Cycle V, Kinarut and younger | — | [M] | Block R basin-modelling study: "oils are trapped at the lower Kinarut"; S&P Global: >45% of deepwater Sabah discoveries in Upper Miocene Cycle V |
| Net-to-gross — P90 / P50 / P10 | 0.24 / 0.28 / 0.34 | frac | [A] | Thin-bed/thick-sand intercalation (SPE 210079-MS); analogue range 0.20–0.40 |
| Porosity (net) | 0.22 | frac | [A] | NW Borneo Miocene clastic reservoirs 20–25% (published regional range); 2,500–3,500 m burial |
| Water saturation (Sw) | 0.25 | frac | [A] | Deepwater turbidite, 22% φ, oil-wet-to-mixed; range 0.18–0.32 |
| Formation volume factor (Bo) | 1.35 | rm³/m³ | [A] | 30–35 °API live oil, GOR 800–1,200 scf/bbl |
| Net pay — P50 | 22.4 | m | [D] | 80 m × 0.28 |
| Oil API gravity | 30–35 | °API | [A] | NW Sabah deepwater analogue range; **not published for Limbayong** |
| GOR (oil leg) | 800–1,200 | scf/bbl | [A] | Analogous undersaturated-to-saturated black oil |

### Table 2 — GRV → STOIIP → recoverable, with arithmetic (P50 worked line, then P90/P10)

**Constants [A]:** φ = 0.22; Sw = 0.25; Bo = 1.35; 1 m³ = 6.2898 bbl.

**P50 line:**
1. GRV = 30.0 × 10⁶ m² × 80 m = **2.400 × 10⁹ m³**
2. GRV in barrels = 2.400 × 10⁹ × 6.2898 = **15.095 × 10⁹ bbl bulk**
3. NPV = 15.095 × 10⁹ × 0.28 (NTG) = **4.227 × 10⁹ bbl**
4. HCPV = 4.227 × 10⁹ × 0.22 × (1 − 0.25) = 4.227 × 10⁹ × 0.165 = **0.6974 × 10⁹ bbl**
5. STOIIP = 0.6974 × 10⁹ ÷ 1.35 (Bo) = **516.6 MMbbl → 517 MMbbl**
6. Recoverable = 517 × 0.26 = **134.3 MMbbl**

| Step | P90 (low) | P50 | P10 (high) | Unit | Class |
|---|---|---|---|---|---|
| Trap area | 22 | 30 | 40 | km² | [A] |
| Gross interval | 70 | 80 | 110 | m | [A] |
| **GRV** | **1.540** | **2.400** | **4.400** | **10⁹ m³** | [D] |
| GRV | 9.686 | 15.095 | 27.675 | 10⁹ bbl | [D] |
| Net-to-gross | 0.24 | 0.28 | 0.34 | frac | [A] |
| Net rock volume | 2.325 | 4.227 | 9.410 | 10⁹ bbl | [D] |
| φ × (1−Sw) | 0.165 | 0.165 | 0.165 | — | [A/D] |
| HCPV | 0.3836 | 0.6974 | 1.5526 | 10⁹ bbl | [D] |
| **STOIIP (÷Bo 1.35)** | **284** | **517** | **1,150** | **MMbbl** | [D] |
| Oil recovery factor | 0.18 | 0.26 | 0.34 | frac | [A] |
| **Recoverable oil** | **51.2** | **134.3** | **391** | **MMbbl** | [D] |
| Booked (GEM, 2023 data year) | — | 139.0 | — | MMbbl | [M] |
| Swanson expected value | (51.2 + 4×134.3 + 391) ÷ 6 = **163.2** | | | MMbbl | [D] |
| Recoverable per well (10 wells) | 5.1 | 13.4 | 39.1 | MMbbl/well | [D] |
| STOIIP per unit trap area | 12.9 | 17.2 | 28.8 | MMbbl/km² | [D] |
| Implied RF at booked 139 | — | **26.9%** | — | frac | [D] |

### Table 3 — Oil rim vs gas cap vs non-associated gas (explicitly separated)

| Stream | Volume | Unit | Class | Basis |
|---|---|---|---|---|
| **Crude oil, recoverable** | 123.2 | MMbbl | [D] | 139.0 total liquids [M] − 15.8 condensate |
| **Condensate, recoverable** | 15.8 | MMbbl | [D/A] | 790.9 bcf × 20 bbl/MMscf (CGR 15–25 → 11.9–19.8 MMbbl) |
| **Total liquids booked** | 139.0 | MMbbl | [M] | GEM, data year 2023 (crude + condensate commingled in source) |
| **Non-associated gas, remaining** | 790.9 | bcf | [M] | GEM, data year 2023 |
| Gas GIIP at RF 0.70 | 1,130 | bcf | [D] | 790.9 ÷ 0.70 (RF 0.60/0.70/0.80 → 1,318/1,130/989 bcf) |
| Gas Bg at 250 bar, 90 °C, z=0.88 | 0.00644 | rm³/rm³ | [D] | Bg = 0.00504·zT/p = 0.00504×0.88×363/250; expansion 155 rm³/rm³ |
| Gas HCPV required | 206 | 10⁶ m³ | [D] | 1,130 bcf = 32.0×10⁹ rm³ × 0.00644 |
| Gas GRV required | 4.46 | km³ | [D] | 206×10⁶ ÷ 0.0462 (=NTG 0.28 × φ 0.22 × 0.75) |
| Gas GRV ÷ oil GRV | 1.86 | × | [D] | 4.46 ÷ 2.40 |
| Combined GRV (oil + gas) | 6.86 | km³ | [D] | 2.40 + 4.46; equals 30 km² × 229 m gross fill |
| Associated gas in oil leg (solution) | ~100–150 | bcf | [A] | 123 MMbbl × 800–1,200 scf/bbl = 98–148 bcf, recovered over life — **not** part of the 790.9 |
| Gas cap vs NAG split | [U] | — | [U] | **Not public.** Operator describes "oil and non-associated gas"; a 1.86× rock-volume requirement for gas versus oil implies most of the 790.9 bcf is free gas in separate blocks/culminations (likely Bestari), not a thin cap |

### Table 4 — Data gaps: what is missing, what it costs, how long

| Missing data | Does the operator have it? | Acquisition route | Cost (US$M, AACE Cl.4/5) | Time | Basis |
|---|---|---|---|---|---|
| 3D seismic (modern, FWI-PSDM) | Yes — used amplitude/spectral decomposition (GSM Bull. 65) | New acquisition, 400 km² | 5.0–10.0 | 18–27 mo | US$8–12k/km² acquisition + US$4–6k/km² depth imaging; 6 mo planning/mobilisation, 4–6 mo acquisition, 9–12 mo imaging |
| — or reprocess existing 3D | Yes | Reimaging only | 1.5–3.0 | 6–9 mo | Benchmark deepwater reprocessing rate |
| Well logs (quad-combo + MDT) | Yes, 4 appraisal wells | One appraisal/development well, 1,000–1,200 m WD | 80–150 | 6–12 mo | Deepwater Malaysia well US$80–200M; operator claims 20–30% below industry average (SPE 210079-MS) |
| Conventional core (60–120 m) | Likely, not public | Add to above well | 3–6 | +2–4 wk rig time | Coring + lab SCAL US$3–6M/well |
| DST / mini-DST | [U] | 2–3 tests in above well | 8–15 per test | +7–14 d/test | Deepwater DST spread rate |
| PVT / fluid samples | [U] | MDT samples + lab PVT | 0.7–1.9 | 3–6 mo lab | US$0.5–1.5M sampling + US$150–400k PVT |
| 4D baseline (for compartment surveillance) | No | Must be shot at/before first oil | 8–15 | 12–18 mo lead | Repeat of 400 km² deepwater 3D |
| Fault-seal / geomechanical core (S_Hmax) | Partly — MEM built (SPE 210549-MS) | Dedicated geomech well + LOT/DFIT | 15–25 | 6–9 mo | Narrow margin <0.5 ppg documented |
| **Total to close static-model gaps** | | | **120–200** | **18–30 mo** | Sum of above, excluding the new well |

## KEY JUDGEMENTS

1. **The trap is real and the trap is the problem.** A 30 km × 2.5 km toe-thrust ridge is a proven NW Borneo trap family (Kikeh, Gumusut-Kakap, Malikai all sit in the same fold-thrust belt), so trap *presence* risk is low. Trap *efficiency* risk is extreme: at 12:1 aspect ratio, the drainage radius of a deviated deepwater well (~1–1.5 km) covers 3–5% of strike length per well. Ten wells at ~3 km spacing is the mathematical minimum for the footprint, and there is no spare well for the compartment that is always wrong in a faulted ridge.

2. **The 139 MMbbl is a P50 number wearing a P90 label.** My geometric rebuild is independent of the operator's model (public dimensions only) and lands at 134 MMbbl at P50, reproducing the booked figure. That is a *consistency* pass, not a *validation*. The sanction case is therefore calibrated to the median outcome, and the median outcome of a top-decile-complexity reservoir is, by construction, the outcome that does not surprise you — half the time it is worse. Downside is 51 MMbbl, i.e. 5.1 MMbbl/well, which cannot carry a US$100M+ well plus its share of a US$4bn facility.

3. **Compartmentalisation is not a risk to be modelled; it is stated as a fact in the sanctioning paper.** "Lateral compartmentalization which impend effectiveness of well drainage and pressure maintenance" is PETRONAS Carigali's own sentence. The mitigation described is *modelling* — "incorporated faults re-interpretation, refined grid resolution, and change of facies prediction, **increasing the stratigraphic compartments**". The operator's response to more compartments was to add more compartments to the model and then to "focus assessment on low realization case". That is intellectually honest and operationally dangerous: it means the FDP is designed around a distribution it cannot yet measure.

4. **The oil rim and the gas are two different projects sharing one hull.** The 790.9 bcf needs a gas GRV of ~4.46 km³ at 250 bar / 90 °C — **1.86× the rock volume of the oil leg**. A gas cap that large above a 123 MMbbl oil rim would imply a column the seal would not hold; the volume arithmetic therefore says most of the booked gas is *non-associated*, in separate fault blocks or at Bestari. Consequence: gas deliverability (150 mmscfd design [M: GEM]) is a **separate subsurface bet with separate compartments**, and it is being tied back across the same 10-well subsea architecture. If gas is one accumulation and oil is another, there is no shared pressure support and no shared upside.

5. **Four appraisal wells in 24 years is the entire static database, and the model has not been refreshed since 2022.** SPE 210549-MS (Sep 2022) states "the first phase of development is to start in Q1 2023". The subsurface work published in 2022 was already FID-ready; the 2023–2026 delay was commercial and facilities (FPSO process cancelled Aug 2022, "commercially unviable" Mar 2023), not geological. On the public record, **no new subsurface data has been acquired between the 2022 papers and the Aug 2026 FID.** The sanction is being taken on a four-year-old static model with the same four wells. (Falsifier in next section.)

6. **Recovery factor 26% is the optimistic end of what this geology supports.** Deepwater turbidite waterfloods globally run 25–40%; the NW Sabah analogue behaviour is the low end of that — Kikeh (1,330 m WD, same belt, same thin-bed/thick-sand problem) required re-drilling after early well failures and sand production, and needed dedicated high-angle thin-bed wells to chase bypassed oil (IPTC-17694-MS). Limbayong stacks *more* complexity onto that template. I would not underwrite 26% without a DST and a 4D baseline; 18–22% is the honest planning number for the low case.

7. **The narrow drilling margin is a static-model symptom, not just a drilling problem.** SPE 210549-MS reports a window "less than 0.5 ppg even at the surface section", wells drilled toward S_hmin, and MPD as mandatory. That is a stress-state statement: the reservoir is being depleted-adjacent or the ridge is critically stressed. Critically stressed faults in a compartmentalised ridge means **faults that are both seals and leaks depending on production-induced stress change** — the exact mechanism that killed Kikeh injectors through poroelastic effects (SPE 122018-MS). Injector count and injector life are therefore static-model outputs, not facilities assumptions.

8. **The 10-well / 270 MMboe configuration is a bet that the ridge is one connected tank.** If it is (best case), 26% RF and 139 MMbbl is achievable and the project works. If it is five tanks — which the operator's own "increasing the stratigraphic compartments" language implies — then either recovery falls to ~18% (51 MMbbl P90) or well count must rise by 50–100% at US$80–150M each. **There is no version of this field where the static model does not set the well count, and no version where the well count is settled.**

## WHAT WOULD CHANGE MY MIND

| My claim | Falsifier |
|---|---|
| Trap area P50 30 km² is right | A published depth map or operator statement showing closure area >50 km² (would push STOIIP toward 900+ and make 139 MMbbl clearly conservative) |
| NTG 0.28 | Core or log data showing NTG >0.40 in the main Kinarut sands; or <0.18, which would kill the project outright |
| RF 26% P50 / 18% P90 | A DST with sustained productivity plus a 4D baseline showing pressure communication across >10 km of strike — that would justify 32–36% |
| Most gas is non-associated | A gas-gradation or contact log proving a single gas cap over the oil rim; or a GSA structured around a single accumulation |
| No new subsurface data 2022–2026 | Any 2023–2026 appraisal well, new 3D, or OBN survey in the public record. I would then withdraw judgement 5 entirely |
| 10 wells is the minimum | An operator statement that wells are dual-zone intelligent completions draining 3+ stacked intervals each, which would cut required well count |
| Compartmentalisation dominates | Interference testing between two well pairs across a mapped fault showing communication (would raise RF and cut well count) |

## CONFIDENCE

| Output | Confidence | Why |
|---|---|---|
| Trap type and structural style | **High (0.90)** | Primary source (SPE 210079-MS) plus peer-reviewed regional geology (GSM Bull. 65) agree exactly, including the L-B-P trend name |
| Structure dimensions (30 × 2.5 km) | **High (0.95)** | Operator's own abstract, verbatim |
| Trap area / gross interval / NTG / φ / Sw | **Low (0.35–0.45)** | Pure analogue benchmarks; no Limbayong-specific measurement exists publicly. This is where the uncertainty lives |
| P50 STOIIP 517 MMbbl | **Low–moderate (0.40)** | ±60% band is honest; the number is a geometry argument, not a measurement |
| P50 recoverable 134 MMbbl | **Moderate (0.55)** | Cross-checks to booked 139 within 4%; the *agreement* is the evidence, not the model |
| P90 downside 51 MMbbl | **Moderate (0.60)** | Driven by RF 18% and 22 km²; both defensible on analogue behaviour |
| Gas GIIP 1.13 Tcf / gas GRV 4.46 km³ | **Low–moderate (0.40)** | Bg depends on assumed P/T ([U]); the 1.86:1 ratio conclusion is robust to ±25% on Bg |
| Condensate 15.8 MMbbl | **Low (0.30)** | CGR entirely assumed; only the commingled 139 is [M] |
| Compartmentalisation is the dominant risk | **High (0.85)** | Operator states it; IPA grades it top-decile; regional literature agrees |
| Model not refreshed since 2022 | **Moderate (0.65)** | Inference from absence in public record; absence of evidence, explicitly flagged |

**Net:** the sanction was defensible on structure and trap, and **under-supported on rock and connectivity**. The static case is a P50 case sold as a base case, with the operator's own complexity grade as the warning label. Nothing here says the field is not there; everything here says the recovery factor and the well count are unmeasured, and those two variables decide the NPV.

## SOURCES

1. Mohamed Aiman Mohamed Najib, Yong Ken Phoon, Wan Fatimah Wan Shamshudin, Shazana Mustapa, A. Khalid, Y. Yusof (PETRONAS Carigali), "Limbayong: Decoding Industry Top Decile Reservoir Complexity for Marginal Deepwater Development," **SPE 210079-MS**, SPE Annual Technical Conference & Exhibition, published 26 Sep 2022, presented 4 Oct 2022. DOI 10.2118/210079-MS. Accessed via Crossref API 19 Oct 2026 (full abstract retrieved). — *structure 30×2.5 km, IPA top-decile grade, four appraisal wells since 2002, thin/thick intercalation, lateral compartmentalisation, 20–30% below industry-average cost, 800 MMboe stranded Sabah deepwater analogue pool.*
2. "Limbayong Deepwater Development Well Planning – A Collaboration with Geomechanics with MPD Approach," **SPE 210549-MS**, published 27 Sep 2022. DOI 10.2118/210549-MS. Accessed via Crossref API 19 Oct 2026. — *drilling margin <0.5 ppg, wells toward S_hmin, MPD mandatory, "first phase of development is to start in Q1 2023", Limbayong as PCSB's first operated deepwater asset and Sabah hub.*
3. Mohd Asraf Khamis, John Jong & Steven M. Barker (JX Nippon Oil & Gas Exploration Deepwater Sabah), "Deformation profile analysis of a deepwater toe-thrust structural trend – Implications on structural kinematics and sedimentary patterns," **Bulletin of the Geological Society of Malaysia, Vol. 65, June 2018, pp. 1–12.** DOI 10.7186/bgsm65201801. Full text read 19 Oct 2026. — *L-B-P trend named; SRU timing; syn-/post-kinematic turbidite deflection and ponded turbidites between ridges; line-balance restoration; amplitude and spectral decomposition used.*
4. "A Play-Based Evaluation of a Deepwater Sabah Exploration Area: Prospect Maturation and Implications for Remaining Prospectivity," **OTC-28398-MS**, Offshore Technology Conference Asia, published 14 Mar 2018. DOI 10.4043/28398-MS. — *four risk elements (reservoir presence, structural evolution, top seal integrity, charge timing); dry-hole analysis in the southern NW Sabah fold-thrust belt.*
5. "A Play-Based… / Basin Modeling Study of Deepwater Block R (DWR), Offshore Sabah and Its Correlation with Surface Geochemical Analyses" — ResearchGate/Academia record, accessed 19 Oct 2026. — *"oils are trapped at the lower Kinarut"; Limbayong-2 (2013) and Limbayong-3 (2014) oil discoveries on trend with Gumusut/Kakap.*
6. J. Jong, M.A. Khamis, S.M. Barker, R.C. Shoup & W.M.Z.W. Embong, "Defining Reservoir Compartments and Baffles: A Case Study in Deepwater Sabah, Malaysia," **EAGE/APGCE extended abstract**, DOI 10.3997/2214-4609.202270064 (2022). Abstract read via search index 19 Oct 2026 (full text Cloudflare-blocked). — *basin-floor fans, channels, crevasse splays, ponded turbidites and MTDs as the geometries that cause compartmentalisation and baffling in a shale-dominated deepwater system.*
7. "Malaysia Deepwater Development: Optimizing Kikeh Reservoir Management and Exploitation in a Changing Environment," **IPTC-17694-MS**, published 19 Jan 2014. DOI 10.2523/iptc-17694-ms. — *Kikeh (K field) 1,330 m WD, thin beds (cm) to thick blocky sands, early well failures and sand production, water + gas re-injection, SMART completions and dedicated thin-bed high-angle wells for bypassed oil. Primary analogue for thin-bed recovery inefficiency.*
8. "Overcoming Poroelastic Behaviour in the Water Injector Wells in the Kikeh Deepwater Development," **SPE 122018-MS**, 27 May 2009. — *injector impairment from production-induced poroelastic stress change; analogue for injector life in a critically stressed ridge.*
9. "Overview of the Malikai Project," **OTC-29071-MS**, 24 Apr 2018. — *Malikai: "a marginal field – limited reserves in challenging reservoirs", 500 m WD, discovered 2004, standalone development not economic, saved only as a satellite tie-back to Kebabangan.*
10. S&P Global Commodity Insights, "Potential in Ultra-deepwater Sabah, Malaysia – Can it be Realized?" — *>45% of deepwater Sabah discoveries in Upper Miocene Cycle V reservoirs of the Baram Delta / NW Sabah Province; Kamunsu East-1 as first discovery, late 1990s.*
11. Global Energy Monitor, Global Oil & Gas Extraction Tracker, data year 2023, via FACT_BASE.md (19 Oct 2026). — *139.0 MMbbl crude + condensate remaining recoverable; 790.9 bcf gas remaining; 14.53 MMbbl/y and 1,550.4 million m³/y design capacity.*
12. Hydrocarbon retention in clastic reservoirs of NW Borneo — examples of hydrocarbon trap, reservoir and seal, and implications on hydrocarbon column length (Academia/ResearchGate record), accessed 19 Oct 2026. — *regional porosity 20–25%, permeability <1 D, "poor fault sealing capability"; named Limbayong, Gumusut, Kikeh as affected; column-length limitation.*
13. Welligence, "Malaysia FID Alert — PETRONAS takes FID on Limbayong," Aug 2026 — *PCSB 100% WI, operator; discovery 2002 by Shell.*
14. Upstream, "Petronas finally takes FID," 28 Aug 2026 (headline and date confirmed; body paywalled).

---

### Flagged discrepancies with FACT_BASE.md

1. **Discovery dating.** FACT_BASE says "Limbayong-2 oil confirmed 2014." Source 5 (Block R basin modelling) dates Limbayong-2 to **2013** and Limbayong-3 to **2014**. The 2013/2014 pair is more consistent with two wells one year apart. [Minor; does not change any number.]
2. **Gas vs oil dominance.** FACT_BASE lists "combined ~270 MMboe" using 6 Mcf/bbl. On my arithmetic the gas occupies **1.86× the rock volume of the oil** — this is volumetrically a **gas field with an oil rim**, not an oil field with a gas cap. Any section that treats gas as a by-product (S4/S5 commercial) should be re-read against Table 3 before the GO/NO-GO is framed.
3. **"Marginal" is the operator's word and it survives.** SPE 210079-MS calls it "marginal deepwater development" and "top decile" complexity in the same title, and states the strategy was to "focus assessment on low realization case." The fact base's characterisation is correct and, if anything, understated.
