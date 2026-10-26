# S2 — RESERVOIR ENGINEERING & PRODUCTION FORECAST

**Project:** Limbayong Deepwater Development (Limbayong + Bestari), Block G/J/R, ~120 km offshore Sabah
**Water depth:** 900–1,200 m · **Operator:** PCSB 100% · **FID:** 28 Aug 2026
**Purpose:** production forecast for the economics section (S5). AACE Class 4 screening — not a reserves report.

> **CONFLICT WITH FACT_BASE — READ FIRST.** FACT_BASE records the design capacity as "[M: GEM, design year 2027]". A 2027 design year is **impossible**: FID was 28 Aug 2026, the hull was only sold to MISC on 20 Aug 2026, and the subsea iEPCI was awarded 15 Sep 2026. There is no path to first production in 2027. GEM's capacity fields are therefore **desk-derived, not operator FDP values** — I treat them as [M-weak] and re-derive what they must mean. Everything downstream of that decision is stated below.

---

## HEADLINE

The published capacities are **nameplate daily rates — 40,000 bopd and 150 mmscfd — annualised at ~99.5% utilisation** (14.53 MMbbl ÷ 40,000 = 363.25 days exactly; 1,550.4 MMm³ ÷ 365 = 150.00 mmscfd exactly), not expected production. The reserve base cannot support either number for more than 9.5 years (oil) and 14.4 years (gas) at 100% uptime with zero decline, so the forecast must sit **below** nameplate: base case **35 kbopd oil and 135 mmscfd gas, five-year oil plateau (2031–2035), 14.6%/yr oil decline, 9.0%/yr gas decline, economic limit ~2048/49, 254 MMboe recovered of 271 MMboe booked**. The controlling constraint on this field is **not deliverability — it is drainage**: ten wells, of which at most six can be oil producers, cannot simultaneously hold 35 kbopd, replace 43 kbwpd of voidage and drain a 30 km × 2.5 km faulted ridge with only four appraisal penetrations.

---

## NUMBERS

| Parameter | Value | Unit | Class | Basis |
|---|---|---|---|---|
| Liquids, remaining recoverable | 139.0 | MMbbl | [M] | GEM tracker, data year 2023 |
| Gas, remaining reserves | 790.9 (22,399) | bcf (MMm³) | [M] | GEM tracker, data year 2023 |
| Total reserves | 270.8 | MMboe | [D] | 139.0 + 790.9/6 (6 Mcf/bbl) |
| Design capacity, liquids (published) | 14.53 | MMbbl/y | [M-weak] | GEM, "design year 2027" — see conflict note |
| → Implied daily rate | 39,808 | bopd | [D] | 14.53e6 ÷ 365 |
| → Implied design basis | **40,000** | bopd | [D] | 14.53e6 ÷ 40,000 = 363.25 days (99.5% availability) |
| Design capacity, gas (published) | 1,550.4 | MMm³/y | [M-weak] | GEM |
| → Implied daily rate | 150.0 | mmscfd | [D] | 1,550.4e6 × 35.3147 ÷ 365 ÷ 1e6 = 150.005 |
| → Annual gas equivalent | 54.75 | bcf/y | [D] | 150 × 365 |
| Years to drain oil reserves at 40 kbopd, 100% uptime, no decline | 9.52 | yr | [D] | 139.0 ÷ (40,000 × 365) |
| Years to drain gas reserves at 150 mmscfd, 100% uptime, no decline | 14.45 | yr | [D] | 790.9e9 ÷ (150e6 × 365) |
| Years at combined nameplate (65,000 boe/d) | 11.41 | yr | [D] | 270.8e6 ÷ 65,000 ÷ 365 |
| Field design oil rate (FDP basis, third-party) | 40,000 | bopd | [M] | Offshore-Technology / WER 2021 (via S4) |
| Field design gas rate | 150 | mmscfd | [M] | Offshore-Technology / TechnipFMC 2026 (via S4) |
| Field design water injection | 75,000 | bwpd | [M] | Marine Technology News / WER 2021 (via S4) |
| Host vessel (Excalibur, ex-Sevan Hummingbird) | 2007/08, 60–70 m cylinder | — | [M] | DNeX Bursa filing 20 Aug 2026; OE Digital 4 Jul 2022 |
| As-built oil process (Chestnut service) | 30,000 | bopd | [M] | Sevan Marine release 22 Sep 2008 |
| As-built water injection | 20,000 | bwpd | [M] | Sevan Marine release 22 Sep 2008 |
| Storage as-built | 270,000–300,000 | bbl | [M] | OE Digital (270k) / DNeX filing (300k) |
| Cargo cycle at 35 kbopd, 85% working | 6.6–7.3 | days | [D] | 270–300 kbbl × 0.85 ÷ 35,000 |
| Development well count | 10 | wells | [M] | PETRONAS release 1 Jun 2021 |
| Appraisal penetrations since 2002 | 4 | wells | [M] | SPE 210079-MS abstract |
| Structural extent | 75 | km² | [M] | 30 km × 2.5 km elongated ridge, SPE 210079-MS abstract |
| Areal well density (10 wells) | 7.5 | km²/well | [D] | 75 ÷ 10 |
| Areal reserves density | 1.85 | MMbbl/km² | [D] | 139 ÷ 75 (productive area < gross extent; see KJ-6) |
| Base allocation: oil producers | 6 | wells | [A] | Allocation judgement — see KJ-4 |
| Base allocation: gas producers | 2 | wells | [A] | As above |
| Base allocation: water injectors | 2 | wells | [A] | As above |
| Reservoir pressure support | Required | — | [M] | SPE 210079: compartmentalisation "impend[s]… pressure maintenance" |
| Oil rate per producer at plateau | 5,833 | bopd | [D] | 35,000 ÷ 6 |
| Gas rate per gas well at plateau | 67.5 | mmscfd | [A] | 135 ÷ 2 — at the top of the analogue range |
| Water injection per injector | 21,875 | bwpd | [D] | 43,750 rb/d voidage ÷ 2 |
| Voidage requirement at 35 kbopd (Bo 1.25) | 43,750 | rb/d | [D] | 35,000 × 1.25 |
| Productivity index, deepwater turbidite (analogue) | 10–40 (base 20) | stb/d/psi | [A] | Sabah/NW Borneo turbidite wells; frac-pack completions |
| Drawdown at 5,833 bopd, PI 20 | 292 | psi | [D] | q ÷ PI |
| Drawdown at 5,833 bopd, PI 10 | 583 | psi | [D] | q ÷ PI — upper limit for sand-control integrity |
| Uptime (calendar availability) | 92 (88–95) | % | [A] | N. Sea FPSO 90–94%; subsea tieback penalty |
| Process efficiency | 97 | % | [A] | Fuel/flare/derate allowance |
| Deliverable plateau = nameplate × uptime × efficiency | 35,700 → **35,000** | bopd | [D] | 40,000 × 0.92 × 0.97 = 35,696, rounded down for turndown |
| Gas plateau = 150 × 0.92 (less 2% fuel) | 135 | mmscfd | [D] | 150 × 0.92 × 0.98 = 135.2 |
| Oil decline (solved to 139.0 MMbbl) | 14.6 | %/yr | [D] | Exponential, from end-2035, to 2052 |
| Gas decline (solved to 790.9 bcf) | 9.0 | %/yr | [D] | Exponential, from end-2038, to 2053 |
| Oil plateau duration | 5 (2031–2035) | yr | [A] | Deepwater turbidite 3–6 yr; set by facility, not reservoir |
| Gas plateau duration | 8 (2031–2038) | yr | [A] | Gas-long field; compression-led plateau |
| First oil | 2030 Q2 | — | [A] | FID Aug 2026 + 44 months (conversion + 10 wells, 2 rigs) |
| Economic limit | ~2048/49 (4–5 kbopd oil) | — | [D] | FPSO opex vs 4 kbopd + 50 mmscfd revenue |
| Field life | 2030–2053 (23 yr) | — | [D] | Technical potential; commercial case ends 2048/49 |
| Recovery at economic limit | 254.2 | MMboe | [D] | Cum. to 2048 |
| Tail below economic limit | 16.6 (4.5 MMbbl + 72.7 bcf) | MMboe | [D] | 270.8 − 254.2 — at-risk, needs low-cost late-life host |
| EUR per oil producer | 23.2 | MMbbl | [D] | 139.0 ÷ 6 — top-quartile requirement |
| EUR per gas well | 396 | bcf | [D] | 790.9 ÷ 2 — **1.3–4× analogue range: not credible** |
| Gas share of reserves (boe) | 48.7 | % | [D] | 131.8 ÷ 270.8 |
| Gas share of undiscounted revenue @ $70/bbl, $3/MMBtu | 19.6 | % | [D] | 2.37 ÷ (2.37 + 9.73) US$bn |
| GOR / condensate yield / CO₂ / H₂S / OOIP / RF / k·h / net pay | [U] | — | [U] | **No public well test, PVT, core or log exists. Do not fabricate.** |

**Design-capacity audit (the arithmetic that matters).** 14.53 MMbbl/y ÷ 40,000 bopd = 363.25 days. That is not a coincidence: the design basis is a **40,000 bopd nameplate**, annualised at 99.5% availability. The gas figure converts to 150.005 mmscfd — also exact. Conclusion: **both numbers are nameplate daily rates stated as annual capacities.** They are not production forecasts, and GEM's presentation of them as annual "design capacity" invites the reader to mistake nameplate for average. Any economics model that uses 40 kbopd × 365 × 0.95 as a plateau is overstating by ~10% before a single well is drilled.

---

## PRODUCTION PROFILE

Base case. Rates are **calendar-year averages, already net of 92% uptime** — do not apply an availability factor again in S5.

| Year | Oil kbopd | Gas mmscfd | Boe/d | Cumulative MMboe |
|---|---|---|---|---|
| 2030 | 15.0 | 55.0 | 24,167 | 8.8 |
| 2031 | 35.0 | 135.0 | 57,500 | 29.8 |
| 2032 | 35.0 | 135.0 | 57,500 | 50.8 |
| 2033 | 35.0 | 135.0 | 57,500 | 71.8 |
| 2034 | 35.0 | 135.0 | 57,500 | 92.8 |
| 2035 | 35.0 | 135.0 | 57,500 | 113.8 |
| 2036 | 29.9 | 135.0 | 52,393 | 132.9 |
| 2037 | 25.5 | 135.0 | 48,030 | 150.4 |
| 2038 | 21.8 | 135.0 | 44,305 | 166.6 |
| 2039 | 18.6 | 122.8 | 39,093 | 180.9 |
| 2040 | 15.9 | 111.7 | 34,529 | 193.5 |
| 2041 | 13.6 | 101.7 | 30,528 | 204.6 |
| 2042 | 11.6 | 92.5 | 27,018 | 214.5 |
| 2043 | 9.9 | 84.2 | 23,934 | 223.2 |
| 2044 | 8.5 | 76.6 | 21,223 | 230.9 |
| 2045 | 7.2 | 69.7 | 18,837 | 237.8 |
| 2046 | 6.2 | 63.4 | 16,735 | 243.9 |
| 2047 | 5.3 | 57.7 | 14,882 | 249.4 |
| 2048 | 4.5 | 52.5 | 13,245 | 254.2 |
| 2049 | 3.8 | 47.7 | 11,800 | 258.5 |
| 2050 | 3.3 | 43.4 | 10,521 | 262.3 |
| 2051 | 2.8 | 39.5 | 9,389 | 265.8 |
| 2052 | 2.4 | 35.9 | 8,386 | 268.8 |
| 2053 | 0.0 | 32.7 | 5,449 | 270.8 |

*Columns are rounded to 1 dp; boe/d and cumulative are computed from unrounded rates, so a hand-check will differ by <0.1%.*

**Annual volumes for the cash-flow model:** oil (MMbbl) 2030 5.5 · 2031–35 12.8/yr · 2036 10.9 · 2037 9.3 · 2038 8.0 · then declining. Gas (bcf) 2030 20.1 · 2031–38 49.3/yr · 2039 44.8 · then declining. Peak year 2031–35 = 57,500 boe/d = 21.0 MMboe/yr.

**Sensitivity (reserves held at 139 MMbbl / 790.9 bcf; decline re-solved):**

| Case | Oil plateau | Gas plateau | Oil decline | Gas decline | Last year >3 kbopd | Peak boe/d |
|---|---|---|---|---|---|---|
| Low — 5 producers, 2 gas wells underperform | 28 kbopd (6 yr) | 110 mmscfd (9 yr) | 11.7%/yr | 7.1%/yr | 2053 | 46,300 |
| **Base** | **35 kbopd (5 yr)** | **135 mmscfd (8 yr)** | **14.6%/yr** | **9.0%/yr** | **2049** | **57,500** |
| High — all 10 wells produce, new topsides at nameplate | 40 kbopd (4 yr) | 150 mmscfd (6 yr) | 16.5%/yr | 10.3%/yr | 2048 | 65,000 |

Note the counter-intuitive but robust result: **higher plateau does not mean more oil — it means a shorter plateau and a steeper decline.** The reserves are fixed. The only things plateau buys you are earlier cash and a shorter facility life. This is why the "plateau 66k → 45k" sensitivity in the CEO memo (−US$683M) is a *timing* sensitivity, not a recovery sensitivity, and should be modelled as such in S5.

---

## KEY JUDGEMENTS

**KJ-1. The published "design capacity" is nameplate, not forecast — and it is arithmetically exact.** 14.53 MMbbl/y ÷ 40,000 bopd = 363.25 days; 1,550.4 MMm³/y = 150.005 mmscfd. *Falsified if:* PCSB's FDP shows a 40 kbopd average year at 92% uptime (it cannot — that requires 43.5 kbopd nameplate).

**KJ-2. No production forecast for this field can hold 40 kbopd for more than ~9.5 years, because that is the entire oil reserve at 100% uptime and zero decline.** 139 MMbbl ÷ (40,000 × 365) = 9.52 years. Any profile showing a decade-long plateau at nameplate is consuming 100% of the reserves during plateau and then stopping dead — physically impossible. *Falsified if:* reserves are restated upward by >40%.

**KJ-3. The 30 kbopd as-built figure is NOT the binding constraint — the binding constraint is deck area and storage.** The Chestnut-era process train (30 kbopd, 20 kbwpd) is being scrapped; S4 sizes 5,500–8,500 t of new topsides onto ~3,500 m² of usable cylindrical deck. 40 kbopd + 150 mmscfd + 75 kbwpd on that footprint is the real question, and it is a *weight and area* problem, not a throughput one. My base case derates to 35 kbopd partly for this reason. *Falsified if:* the conversion contract publishes a topsides weight < 5,500 t with a 40 kbopd / 150 mmscfd train.

**KJ-4. Ten wells cannot do all three jobs. This is the central reservoir-engineering finding.** Holding 35 kbopd requires 6 producers at 5,833 bopd; replacing voidage at Bo 1.25 requires 43,750 rb/d of injection, which needs 2 injectors at ~21,875 bwpd each. That is 8 wells. The remaining 2 must carry 790.9 bcf — **396 bcf per gas well, versus an analogue range of 100–300 bcf.** Limbayong is therefore either (a) a 12–14 well development with a second drilling campaign, (b) a phased development where gas comes later on its own wells, or (c) booking 791 bcf on two wells that will not deliver it. The public "10 wells" number is a 2021 pre-FID figure and should not be used as the well count in the economics. *Falsified if:* the FDP well list shows ≥3 gas wells and ≥2 injectors inside the 10.

**KJ-5. Deliverability is not the risk; drainage is.** 5,833 bopd per producer against a PI of 10–40 stb/d/psi requires only 146–583 psi drawdown — routine for a frac-packed deepwater completion, and comfortably inside sand-control limits at PI ≥ 20. The wells will make the rate. What they will not do is *drain* 75 km² from six points on a 30 km ridge with faults every few kilometres, at 12.5 km² per producer and ~3.5 km equivalent spacing, with four appraisal penetrations in 24 years. SPE 210079 says this in the operator's own words: lateral compartmentalisation "impend[s] effectiveness of well drainage and pressure maintenance." *Falsified if:* interference testing or 4D seismic shows lateral continuity across the fault blocks.

**KJ-6. The reserve density is the tell.** 139 MMbbl over a 30 × 2.5 km structure is 1.85 MMbbl/km² gross. Kikeh (~400 MMbbl) runs roughly 5–10× that density across its productive fault blocks. Either only ~15–25 km² of the 75 km² is productive (pay is concentrated in a few fault blocks and the rest is thin-bed waste), or recovery is being booked at the low end. Both readings say the same thing: this is a **sweet-spot development of a complex field, not a full-field development** — which is precisely what "marginal" means in the paper's title. *Falsified if:* the FDP maps >40 km² of net productive area.

**KJ-7. Gas is sold, not flared, and not primarily re-injected — but it is only ~20% of the revenue.** Zero routine flaring rules out 135 mmscfd to flare; PETRONAS ZEVC and the 2024 Sabah GSA point to monetisation. At $3/MMBtu domestic gas, 790.9 bcf is US$2.37bn undiscounted against US$9.73bn for the oil at $70 — gas is 49% of the boe but 20% of the money. *Falsified if:* a GSA at ≥$5/MMBtu (which would lift gas to ~29% of revenue and is worth +US$370M NPV per the CEO memo) or if the FDP adopts gas re-injection for pressure maintenance, in which case 791 bcf is not Phase 1 revenue at all and the project loses ~US$2.4bn of undiscounted gas sales.

**KJ-8. There is a gas-export infrastructure gap that the disclosed contract scope does not cover.** 790.9 bcf must reach either the Sabah grid (Kimanis/SSGP, ~140–180 km) or an LNG route. The disclosed awards are subsea iEPCI (TechnipFMC, US$75–250M) and a US$35M hull. No export pipeline, no gas-processing module, no GSA has been disclosed. Either the gas is stranded behind an unfunded 150 km pipeline, or it is re-injected, or the scope is undisclosed. S4 and S7 must price this; S5 must not book gas revenue before 2032 without a GSA. *Falsified if:* a pipeline EPCIC or GSA is published.

**KJ-9. Uptime 92% is achievable but the field life is the bigger facility risk.** A cylindrical hull has good motion behaviour (Sevan's selling point) and the 92% base sits mid-range for North Sea FPSOs at 90–94%; a 19-year-old converted hull on a 30 km subsea tieback with a validated turndown limit justifies the 88% low case. Each 1% of uptime over the 5-year plateau is worth ~0.64 MMbbl. The harder issue: the **economic limit lands around 2049, when the hull is 42 years old.** A 23-year field life on a 2007-built redeployed cylinder implies either a life extension capex in the 2040s or a late-life host swap — neither is in the FID scope. *Falsified if:* the conversion includes a 25-year design-life certification.

**KJ-10. About 16.6 MMboe (6.1%) of the booked reserves will not be produced commercially.** Below ~4 kbopd the FPSO's opex exceeds revenue; the 2049–2053 tail (4.5 MMbbl + 72.7 bcf) needs a low-cost late-life host to happen. S5 should carry **254 MMboe as the commercial case** and treat the balance as contingent. *Falsified if:* opex falls below ~US$8/boe or a third-party tie-back shares the facility cost.

---

## WHAT WOULD CHANGE MY MIND

1. **A published FDP production profile.** Any single operator document with year-by-year rates supersedes this entire section. My numbers are an envelope, not a prediction.
2. **The well list with well types.** If the 10 wells are e.g. 7 producers + 3 gas and injection is deferred, my voidage argument collapses and plateau is credible; if they are 6 + 2 + 2, KJ-4 stands.
3. **A DST or RFT/MDT from Limbayong-2 or any appraisal well.** A measured PI above 30 stb/d/psi with kh > 5,000 md-ft would move me from "drainage-limited" to "rate-limited" and lift the plateau case toward 40 kbopd.
4. **Interference or compartment-pressure data.** Proof that the fault blocks are in communication would raise recovery per well and validate 6 producers for 139 MMbbl.
5. **A signed GSA with volume, price and start date.** This converts KJ-7 from judgement to fact and is the single largest swing in the economics.
6. **Evidence of a strong water drive or gas-cap support** that reduces injection need to <20 kbwpd — that would free a well slot for gas or oil and fix the KJ-4 arithmetic.
7. **Reserves restatement.** If 2P is truly 139 MMbbl, the 9.5-year nameplate ceiling is unarguable. If the booked number is a conservative FID-case subset of a larger 800 MMboe trend resource, the plateau could run longer.

---

## CONFIDENCE

| Claim | Confidence | Why |
|---|---|---|
| Design capacity is nameplate daily rate (40 kbopd / 150 mmscfd), not average | **High (0.9)** | Exact arithmetic: 363.25 days and 150.005 mmscfd are not random |
| Reserves support ≤9.5 yr oil / ≤14.4 yr gas at nameplate | **High (0.95)** | Pure arithmetic on [M] reserves |
| Base plateau 35 kbopd / 135 mmscfd | **Medium (0.55)** | Depends on facility derate and well allocation; range 28–40 kbopd |
| Oil decline 14.6%/yr, gas 9.0%/yr | **Medium-low (0.45)** | Shape is analogue-driven (deepwater turbidite 10–25%); cumulative is pinned to reserves, so *shape* is the uncertain part, not the total |
| 6 oil / 2 gas / 2 WI allocation | **Low (0.3)** | No public well list. Structurally reasoned, not sourced |
| 92% uptime | **Medium (0.6)** | North Sea FPSO benchmark 90–94%; converted 19-yr hull argues 88% |
| First oil 2030 | **Medium (0.5)** | 44 months from FID is achievable for a converted hull but this project has slipped three times |
| Economic limit ~2048/49, commercial recovery 254.2 MMboe | **Medium (0.55)** | Highly sensitive to opex and gas price |
| Gas sold (not flared) | **High (0.85)** | Regulatory and commercial logic; 135 mmscfd cannot be flared |
| Gas sold at ≥$5/MMBtu | **Low (0.25)** | Malaysian domestic gas is regulated low; no GSA public |

**Overall confidence in the production forecast: medium-low.** The cumulative (271 MMboe) is solid because it is [M] reserves. The *path* — plateau height, plateau length, decline — is a Class 4 envelope with ±35% on annual rates in any given year and ±20% on peak rate. That is appropriate for a screening study and inappropriate for a sanction decision.

---

## SOURCES

| # | Source | Used for |
|---|---|---|
| 1 | **SPE 210079-MS**, Najib, Phoon, Shamshudin, Mustapa, Khalid, Yusof (PCSB), *"Limbayong: Decoding Industry Top Decile Reservoir Complexity for Marginal Deepwater Development"*, ADIPEC 2022, DOI 10.2118/210079-ms — abstract via Semantic Scholar record | 30 km × 2.5 km elongated structure; thin-bed/thick-sand intercalation; lateral compartmentalisation impeding drainage and pressure maintenance; **four appraisal wells since 2002**; validated turndown limit; 20–30% well/facility cost advantage; ~800 MMboe scattered deepwater Sabah resource |
| 2 | GEM Global Oil & Gas Extraction Tracker, data year 2023 (per FACT_BASE) | 139.0 MMbbl, 790.9 bcf; "design capacity" 14.53 MMbbl/y, 1,550.4 MMm³/y (re-classed [M-weak], see conflict note) |
| 3 | Sevan Marine ASA press release, 22 Sep 2008 (ship.gr mirror) | Sevan Hummingbird as-built: 30,000 bopd oil, 20,000 bwpd water injection, 300,000 bbl storage |
| 4 | Offshore Engineer (OE Digital), 4 Jul 2022 — "Teekay Sells Sevan Hummingbird FPSO to Ping Petroleum" | 60 m diameter, 270,000 bbl storage, commissioned 2008, 13 years at Chestnut; renamed Excalibur |
| 5 | DNeX Bursa announcement, 20 Aug 2026 (via S4) | Excalibur 70 m × 27 m, 300,000 bbl design storage, built 2007, US$35M sale to MISC |
| 6 | Offshore Technology, 15 Jun 2021 — Limbayong project profile | 10 deepwater wells tied back to FPSO; Block G; 900–1,200 m |
| 7 | Offshore Magazine, 3 Oct 2022 — FPU redeployments | Redeployed FPUs "tend to be smaller — 50,000 bopd or less"; as-is US$10–80M with upgrades 5–10× |
| 8 | OTC-19481-MS, *Kikeh Development: Project Overview* | Kikeh analogue: >400 MMbbl, 120,000 bopd plateau, ~1,300 m |
| 9 | Shell Malaysia / Ocean News / OGA Malikai project page | Malikai analogue: 60,000 bopd nameplate, 17 wells, actual ~25,000 bopd (2026), Phase 3 +4 wells → ~40,000 bopd |
| 10 | PETRONAS media release, 1 Jun 2021 | 900–1,200 m water depth; SURF EPCIC award |

**Analogue set used for per-well performance (all [A]):** Kikeh (~5,000 bopd/well average at plateau), Gumusut-Kakap (~6,300 bopd/well implied), Malikai (~1,800–3,750 bopd/well actual — the cautionary case: 42% of nameplate for nine years). Gas wells: Sabah deepwater big-bore completions 40–90 mmscfd/well, EUR 100–300 bcf/well.

**What is NOT in this section, because it does not exist in public domain:** well test rates, PVT/fluid composition, GOR, condensate yield, CO₂/H₂S, core, net pay, porosity/permeability, OOIP, recovery factor, fault-transmissibility, aquifer strength, DST-derived PI, and the actual FDP production forecast. Everything above the [M] rows is an envelope built from the operator's own public framing plus named analogues. **Do not let S5 treat any [A] row as measured.**
