# S7 — ECONOMICS & FISCAL

**Scope:** Contractor-side (PCSB 100% WI) pre- and post-tax cash flow for Limbayong, real 2026 USD, discounted 10% real. Model code and outputs: `evidence/s7_model.py`, `evidence/s7_metrics.py`. Every figure below is reproducible from those two files.

**Red flag on the shared fact base (stated loudly, per rule 6):** the TechnipFMC iEPCI award of **US$75–250M** for "full subsea scope" across **10 deepwater wells in 900–1,200 m** is 2–4× below any credible SURF cost for that scope. Either (a) the award covers a narrow, partial scope and the balance sits in a separate contract not in the public record, or (b) it is a headline number with options/EPCIC exclusions. I have modelled SURF at **$600M**, not $250M. If $250M were truly all-in, NPV10 rises by **$107M to $395M** and IRR to 13.4% — material, but not enough to change the verdict. This is still the largest single unverified value lever in the public record.

---

## HEADLINE

**Limbayong clears a 10% real hurdle and fails a 15% hurdle. It is a gas project wearing an oil project's clothes.**

| # | Metric | Value | Class |
|---|---|---|---|
| 1 | **NPV10** (real, post-tax, contractor) | **+US$288M** on US$2,900M capex — PV/capex = 0.10 | [D] |
| 2 | **IRR** (post-tax, real) | **12.3%** | [D] |
| 3 | **UTC** (capex + opex, undiscounted, incl. abandonment) | **US$21.06/boe** | [D] |
| 4 | **Breakeven Brent** (NPV10 = 0, flat-equivalent) | **US$60/bbl** | [D] |
| 5 | **Brent required for 15% IRR** | **US$96/bbl** — above the top of my high deck | [D] |
| 6 | Reserves required for NPV10 = 0 | 233 MMboe = **86% of the 270.8 MMboe booked** | [D] |
| 7 | Reserves required for 15% IRR | 325 MMboe = 120% of booked | [D] |
| 8 | Gas contribution to NPV | Oil-only counterfactual (no gas, no pipeline, capex $2,250M) is **NPV10 −$29M / IRR 9.7%**; gas is worth **+$317M**, i.e. **110% of total NPV** | [D] |
| 9 | Peak funding (max cumulative negative) | US$2,784M, reached 2029 | [D] |
| 10 | Government + PETRONAS host take | 45.6% of gross revenue | [D] |

**Verdict:** at a 10% real hurdle — the right hurdle for a 100%-state-owned operator with a Sabah gas mandate — this is a **GO by US$288M**, a 10% margin on capital employed that a single 30% reserve shortfall erases. At a 15% hurdle it is a **NO-GO at every Brent price in the 2027–2035 forward range**. FID was taken because PCSB is not optimising for IRR; it is buying 790 bcf of Sabah gas and 139 MMbbl of liquids with a US$35M second-hand hull and a tax incentive. Judge it on that basis, not on a corporate hurdle rate it cannot meet.

---

## ASSUMPTIONS

All money is **real 2026 USD, unescalated**; discount rate **10% real**. A nominal model at 2% inflation and 12.2% nominal WACC reproduces these results to within ~2%. Costs are **AACE Class 4 (−30%/+50%)**; no estimate here is better than Class 4.

| Parameter | Value | Unit | Class | Basis |
|---|---|---|---|---|
| **Reserves — liquids** | 139.0 | MMbbl | [M] | GEM Global Oil & Gas Extraction Tracker (data year 2023), crude + condensate remaining recoverable |
| **Reserves — gas** | 790.9 | bcf | [M] | Same source, 22,398.75 MMm³ |
| **Reserves — total** | 270.8 | MMboe | [D] | 139.0 + 790.9 × 0.16667 (6 Mcf/bbl) |
| **Liquids plateau** | 40,000 | bopd | [M]→[D] | GEM design capacity 14.53 MMbbl/y ÷ 365 = 39,808 bopd; rounded to 40,000. Cross-checks against a 139 MMbbl / 15-yr field life |
| **Gas plateau** | 150 | mmscfd | [M] | GEM design capacity 1,550.4 MMm³/y = 54.7 bcf/y |
| **First oil** | 2030 | year | [A] | FID 28 Aug 2026 + 41 months. FPSO conversion of an existing hull (24–30 mo) runs in parallel with a 10-well, 2-rig drilling campaign (30 mo). Range 2029–2031; 2029 is modelled as the acceleration case |
| **Field life** | 2030–2045 | years | [A] | 16 producing years; PSC production period 25 yr, so no contractual truncation |
| **Ramp** | 45% / 85% / 100% | of plateau | [A] | Two-year ramp, standard for a 10-well subsea tie-back with phased well hook-up |
| **Decline — liquids** | 17 | %/yr | [A] | Exponential, after 4-yr plateau. Toe-thrust turbidites with solution-gas drive and water injection typically 15–25% |
| **Decline — gas** | 13 | %/yr | [A] | After 5-yr plateau; gas plateau set by 150 mmscfd plant limit, not by deliverability |
| **Capex — drilling & completion** | 850 | $M | [A] | 10 wells × $85M all-in (dry-hole risk carried pre-FID; range $60–120M/well for 900–1,200 m, 4–6 km tie-back). Benchmark: Sabah deepwater development wells $60–110M |
| **Capex — subsea production system + iEPCI** | 600 | $M | [A] (band [M]) | TechnipFMC iEPCI $75–250M [M] **plus** trees, manifolds, umbilicals, flowlines and installation campaign excluded from that band = $350M. See red flag above |
| **Capex — FPSO** | 485 | $M | [D]/[A] | Excalibur purchase US$35M [M: DNeX Bursa filing 20 Aug 2026] + $450M conversion/upgrade/life-extension for 40 kbopd + 150 mmscfd [A]. Used cylindrical hull, 1990s vintage — condition is [U] |
| **Capex — gas export pipeline** | 650 | $M | [A] | 120 km, 26″ insulated wet-gas line + beach/tie-in at ~$5.4M/km. Without this line the 790 bcf cannot be sold — it is not optional |
| **Capex — owners, PMT, pre-FID, contingency** | 315 | $M | [A] | ~12% of the $2,585M technical scope |
| **Capex — total** | 2,900 | $M | [D] | 850 + 600 + 485 + 650 + 315. **$10,710/boe** |
| **Capex phasing** | 5 / 25 / 40 / 26 / 4 | % in 2026/27/28/29/30 | [A] | S-curve, FID Aug-2026, first oil 2030 |
| **Abandonment** | 200 | $M | [A] | FPSO demob, well P&A contribution, subsea recovery; spent 2045 |
| **Opex — fixed** | 95 | $M/yr | [A] | FPSO operations, marine spread, subsea inspection, insurance, onshore support. Benchmark $80–120M/yr for a 40 kbopd + 150 mmscfd deepwater hub |
| **Opex — variable** | 4.00 | $/boe | [A] | Chemicals, well intervention, consumables, tariff-linked items |
| **Opex — implied unit** | 7.6 / 9.6 / 20.8 | $/boe | [D] | $7.6/boe at plateau (201 ÷ 26.56 MMboe in 2032); $9.6/boe life average; $20.8/boe in 2045 as fixed cost spreads over 5.7 MMboe |
| **Liquids price differential** | −1.00 | $/bbl vs Brent | [A] | Sabah light sweet (Kimanis-type) normally trades at or slightly above Brent; −$1.00 charged for CO₂/quality and netback to a Malaysian export point |
| **Gas price** | 6.50 | $/MMBtu | [A] | Wellhead netback below the Malaysia Reference Price (MRP Q4-2025 = RM36.64/MMBtu ≈ $8.7 [M: Gas Malaysia notice]) and below the RM30/MMBtu (~$7.1) domestic power-sector cap [M: The Edge, 2023]. Range $3.9–9.1 |
| **Royalty** | 10.0 | % of gross | [M] | Malaysia DW PSC terms table: royalty 10% |
| **Research cess** | 0.5 | % of gross | [M] | Same table; **not** cost-recoverable |
| **Export duty — crude/condensate** | 10.0 | % of crude revenue | [M] | Federal export duty 10% on petroleum crude exported; Sabah crude is an export stream |
| **Sabah State Sales Tax — gas** | 5.0 | % of gas revenue | [M] | Sabah State Sales Tax Enactment 1998; natural gas 5% effective 1 Apr 2020 [M: MPM "Other Governing Laws"] |
| **Cost recovery ceiling — oil** | 70 | % of post-royalty oil revenue | [M] | Malaysia DW PSC: oil 70%, gas 80% (UDW oil 75%) |
| **Cost recovery ceiling — gas** | 80 | % of post-royalty gas revenue | [M] | As above |
| **Profit split — oil** | 50% to 100 MMbbl cum., 60% thereafter | % of profit oil to contractor | [M] | Malaysia DW PSC volume-based split: ≤100 MMbbl 50%, 100–200 MMbbl 60%, >200 MMbbl 70% |
| **Profit split — gas** | 50 | % of profit gas to contractor | [M] | ≤2 tscf 50%, 2–4 tscf 60%; Limbayong is 0.79 tscf, so 50% throughout |
| **Petroleum income tax** | 38 | % of chargeable profit | [M] | Petroleum (Income Tax) Act 1967 (Act 543) |
| **Capital allowance** | 100% of QCE over 10 yr, straight line | — | [M]/[A] | PITA Second Schedule; 10-yr write-off for petroleum QCE. No initial allowance assumed — mildly conservative |
| **Investment allowance** | 60% of QCE, capped at 70% of statutory income/yr, carry-forward | — | [M] | PITA (Investment Allowances) Regulations 2013, reg. 12 — **Deepwater Project (>200 m water depth)** is a named qualifying project. 900–1,200 m qualifies. Approval by MOF on MPM verification is assumed granted [A] |
| **PSC vintage assumed** | Malaysia **Deepwater PSC (1993 terms, as published in the 2013 MPM/PMU fiscal tables)** | — | [A]/[U] | Limbayong's PSC text is not public. The block was awarded in the deepwater rounds (G/J/R area, Sabah), so DW terms apply. **2018 DW enhancements** (Upstream, 27 Nov 2018) are *not* quantified — they would move terms in the contractor's favour, so my NPV is, if anything, conservative on this axis |
| **PCSB working interest** | 100 | % | [M] | Welligence; 100% WI means no partner dilution and no carried-interest relief |
| **Discount rate** | 10 | % real | [A] | Standard real hurdle for NOC upstream screening; sensitivity to 15% given explicitly |

### Price deck — Brent, real 2026 USD

| Year | Low | **Base** | High | Basis |
|---|---|---|---|---|
| 2027 | 70 | **84** | 95 | Base 2027 = EIA STEO, released 6 Oct 2026: Brent $84/b in 2027 [M] |
| 2028 | 62 | **80** | 95 | Base: post-conflict normalisation; STEO shows 2026 at $96 on a Middle East war premium [M] which is *not* extrapolated |
| 2029 | 58 | **77** | 92 | Base: gradual convergence to long-run marginal cost |
| 2030 | 55 | **76** | 90 | Base: plateau onset; long-run anchor |
| 2031 | 55 | **75** | 90 | Long-run $75 real = midpoint of EIA AEO reference ($70–80/b real) and IEA WEO STEPS; also sits just above US shale full-cycle breakeven ($60–70) which is the structural floor |
| 2032 | 55 | **75** | 90 | |
| 2033 | 55 | **75** | 90 | |
| 2034 | 55 | **75** | 90 | |
| 2035 | 55 | **75** | 90 | |
| 2036–2045 | 55 | **75** | 90 | Flat real |

Low deck = demand-peak/OPEC-share-war scenario: 2025 realised Brent was $69 [M: STEO], so $55 is a further 20% real decline sustained for two decades. High deck = sustained OPEC+ discipline plus recurring supply disruption. **The base deck is not a forecast; it is the number the project has to survive.**

---

## PRODUCTION PROFILE USED

Built independently of every other section, from the two design capacities and two reserve numbers. Shape: 2-year ramp (45%/85%), 4-year liquids plateau at 40 kbopd, 5-year gas plateau at 150 mmscfd, then exponential decline (17%/yr liquids, 13%/yr gas). The profile is then **scaled so cumulative volumes land exactly on 139.0 MMbbl and 790.9 bcf** — no rounding drift into the reserves.

| Stream | Plateau | Plateau years | Cumulative | Recovery check |
|---|---|---|---|---|
| Liquids | 40,000 bopd (14.60 MMbbl/yr) | 2032–2035 | 139.0 MMbbl | Matches [M] exactly by construction |
| Gas | 150 mmscfd (54.7 bcf/yr) | 2032–2036 | 790.9 bcf | Matches [M] exactly by construction |
| **Total** | **65,000 boe/d (23.7 MMboe/yr)** | 2032–2035 | **270.8 MMboe** | |

Peak year 2032–2035 at 26.56 MMboe. Production ends 2045 at 5.7 MMboe/yr (tails out, not truncated). Note the asymmetry that drives the whole valuation: **liquids plateau lasts 4 years, gas plateau lasts 5 and the gas tail is long** — gas is 48% of boe but 34% of gross revenue and the majority of late-life cash flow.

---

## CASH FLOW SUMMARY

US$M, real 2026. Revenue is gross field revenue. Pre-tax CF = contractor entitlement (cost oil + profit share, net of cess) − opex − capex; royalty, export duty and SST are already removed inside entitlement.

| Year | Prod (MMboe) | Revenue | Opex | Capex | Pre-tax CF | Tax | Post-tax CF | Cum. |
|---|---|---|---|---|---|---|---|---|
| 2026 | 0.0 | 0 | 0 | 145 | -145 | 0 | -145 | -145 |
| 2027 | 0.0 | 0 | 0 | 725 | -725 | 0 | -725 | -870 |
| 2028 | 0.0 | 0 | 0 | 1,160 | -1,160 | 0 | -1,160 | -2,030 |
| 2029 | 0.0 | 0 | 0 | 754 | -754 | 0 | -754 | -2,784 |
| 2030 | 12.5 | 737 | 145 | 116 | 256 | 9 | 247 | -2,537 |
| 2031 | 22.9 | 1,348 | 187 | 0 | 758 | 53 | 705 | -1,833 |
| 2032 | 26.6 | 1,569 | 201 | 0 | 898 | 69 | 828 | -1,004 |
| 2033 | 26.6 | 1,569 | 201 | 0 | 898 | 69 | 828 | -176 |
| 2034 | 26.6 | 1,569 | 201 | 0 | 792 | 57 | 735 | 559 |
| 2035 | 26.6 | 1,569 | 201 | 0 | 531 | 34 | 498 | 1,056 |
| 2036 | 24.1 | 1,384 | 191 | 0 | 463 | 66 | 397 | 1,454 |
| 2037 | 20.4 | 1,167 | 177 | 0 | 433 | 54 | 379 | 1,832 |
| 2038 | 17.4 | 986 | 164 | 0 | 357 | 25 | 331 | 2,164 |
| 2039 | 14.8 | 833 | 154 | 0 | 292 | 1 | 292 | 2,455 |
| 2040 | 12.6 | 704 | 145 | 0 | 238 | 91 | 148 | 2,603 |
| 2041 | 10.7 | 595 | 138 | 0 | 193 | 73 | 120 | 2,723 |
| 2042 | 9.1 | 503 | 131 | 0 | 155 | 59 | 96 | 2,819 |
| 2043 | 7.8 | 426 | 126 | 0 | 123 | 47 | 76 | 2,895 |
| 2044 | 6.6 | 361 | 122 | 0 | 96 | 36 | 59 | 2,954 |
| 2045 | 5.7 | 306 | 118 | 200 | -127 | 28 | -155 | 2,799 |
| **Total** | **270.8** | **15,624** | **2,603** | **3,100** | **3,571** | **772** | **2,799** | |

**Where the gross revenue went (US$M, % of gross):**
Royalty 1,562 (10.0%) · Export duty 1,029 (6.6%) · Sabah SST 267 (1.7%) · Research cess 78 (0.5%) · PIT 38% 772 (4.9%) · PETRONAS host profit share 3,414 (21.8%) · **Contractor entitlement 9,274 (59.4%)** — of which cost recovery 5,503 + profit share 3,849 − research cess 78.
**Total government + PETRONAS take = 7,122 = 45.6% of gross.** Contractor keeps 54.4% of gross but spends 36.5% of gross on capex + opex, which is why the NPV margin is thin.

**Fiscal mechanics that visibly bind:**
- The **70% cost recovery ceiling binds in 2030–2033**. Unrecovered cost carries forward; full payout of the 2026–2030 spend takes until 2033. This is why the pre-tax CF steps down in 2035 once the pool empties and the contractor is on pure profit share.
- The **oil profit split steps 50% → 60%** when cumulative liquids pass 100 MMbbl (2037). Small, real, and it is the only progressive element that works in the contractor's favour here.
- **Tax is back-end loaded, not avoided:** 2030–2039 pays almost nothing because of the investment allowance; 2040–2045 pays at close to the full 38% marginal rate. Total PIT is $772M with the incentive versus $1,433M without it — the investment allowance abates **$661M** of tax and defers the rest.

---

## METRICS

| Metric | Value | Arithmetic |
|---|---|---|
| **NPV10** | **+US$288M** | Σ post-tax CF / 1.10^(t−2026). Cross-check by hand: PV of outflows 2,330; PV of inflows 2,624; net 294 (±6 from rounding) |
| **IRR** | **12.3%** | Bisection on the 20-year post-tax stream: FID −145/−725/−1,160/−754 then +247…−155 |
| **Payback (undiscounted)** | **2034** | Cumulative turns positive during 2034: −176 at end-2033, +559 at end-2034. **8 years after FID, in the 4th full producing year** |
| **UTC** | **US$21.06/boe** | (3,100 capex incl. 200 abandonment + 2,603 opex) ÷ 270.8 MMboe = 21.06 |
| **Capex-only unit** | US$11.45/boe | 3,100 ÷ 270.8 |
| **Opex-only unit** | US$9.61/boe | 2,603 ÷ 270.8 |
| **Breakeven Brent (NPV10 = 0)** | **US$60/bbl flat-equivalent** | Deck multiplier 0.796 → 2030–35 reference price $75 × 0.796 = $59.7 |
| **Brent for 15% IRR** | **US$96/bbl** | Multiplier 1.284 → $75 × 1.284 = $96.3 |
| **Brent for 10% IRR** | **US$60/bbl** (identical to the NPV10 = 0 price — that is the definition of IRR) | Deck multiplier 0.796 |
| **Reserves breakeven (NPV10 = 0)** | **233.2 MMboe** (119.7 MMbbl + 681 bcf) | Scale factor 0.861 |
| **Reserves for 15% IRR** | **325 MMboe** | Scale factor 1.200 |
| **Capex for 15% IRR** | US$2,338M (US$8,634/boe) | Needs a 19% underspend against a Class 4 estimate — i.e. the −30% end of the range must be realised in full, and then some |
| **Gas price for NPV10 = 0** | US$3.86/MMBtu | Gas floor; below the domestic cap by $3.2 |
| **Opex for NPV10 = 0** | +70% (fixed $161M/yr) | Late-life opex is the second-weakest link after reserves |
| **PV/capex** | 0.10 | 288 ÷ 2,900 |
| **Investment-allowance value** | **+US$353M NPV, +2.8 pts IRR** | Without the 60% IA, NPV10 = **−$65M** and IRR = 9.5%. **The project is uninvestable on a 10% hurdle without this incentive** |

### Basis bridge — why the contractor view and the consolidated view differ

A sibling section in this pack (`S7X-economics-calibrated.md`) quoted **NPV10 ≈ US$1.1bn at 17.3% IRR** and called that the "PETRONAS-consolidated basis". That is not a contradiction of the US$288M above; it is a different boundary, and the difference is the whole story of Malaysian PSC economics:

| Boundary | NPV10 | IRR | What it counts |
|---|---|---|---|
| **Contractor (PCSB as PSC contractor)** — the number in this section | **+$288M** | **12.3%** | Cost recovery + contractor profit share, less all capex, opex and 38% PIT |
| PETRONAS as host (profit oil/gas share) | +$1,304M | — | PETRONAS' 50%/40% of profit after cost recovery; no capital at risk |
| **PETRONAS consolidated (host + contractor)** | **+$1,592M** | **19.8%** | Σ undiscounted $6,213M |
| Government (royalty + duty + SST + cess + PIT) | +$3,708M undiscounted | — | Accrues to the Federal and Sabah governments, not to PETRONAS |

Read this table carefully, because it is the political economy of the field in four lines: **the first dollar of consolidated value is the host's, not the investor's.** Limbayong works at 19.8% consolidated and 12.3% contractor-side. A foreign partner — Shell, who discovered it in 2002 — would earn the contractor line and would be right to walk. PETRONAS can proceed precisely because it collects both lines. That, not the oil price, is why this project waited for PCSB to take 100% and for a US$35M hull to appear.

---

## SENSITIVITY

Each row re-runs the full fiscal stack. ΔNPV is against the US$288M base.

| Rank | Case | NPV10 ($M) | ΔNPV ($M) | IRR |
|---|---|---|---|---|
| 1 | **Reserves −30%** | **−384** | **−672** | 6.8% |
| 2 | Reserves +30% | 852 | +564 | 16.3% |
| 3 | **Capex +30%** | **−135** | **−423** | 9.2% |
| 4 | Capex −30% | 644 | +356 | 16.9% |
| 5 | **Oil price −25% ($56)** | **−70** | **−358** | 9.4% |
| 6 | Oil price +25% ($94) | 612 | +324 | 14.7% |
| 7 | **Gas price −40% ($3.90)** | **+5** | **−283** | 10.0% |
| 8 | Gas price +40% ($9.10) | 548 | +260 | 14.2% |
| 9 | **Opex +30%** | 170 | −118 | 11.4% |
| 10 | Opex −30% | 403 | +115 | 13.1% |
| 11 | **Schedule +18 mo, +8% capex** | 197 | −91 | 11.8% |
| 12 | Schedule −12 mo (first oil 2029) | 382 | +94 | 13.0% |

**Tornado ordering, largest swing first: reserves (−672) > capex (−423) > oil price (−358) > gas price (−283) > opex (−118) > schedule (−91).**

This ordering is the finding, not the table. **The two largest value drivers are both cost-and-volume, not price.** Reserves and capex together swing $1.1B of NPV — nearly four times the base NPV. A price-only sensitivity would flatter this project; the operator's own SPE 210079-MS calls the reservoir "top decile complexity" and the development "marginal", and the model agrees with the operator, not with the FID.

Note on the schedule number: a pure time-shift is almost NPV-neutral (deferred capex offsets deferred revenue at 10%), which is why +18 months on its own costs only $8M. The **real** schedule risk is the cost escalation and FPSO day-rate exposure that a slip drags with it — modelled here as an 8% capex adder, giving −$91M. Read row 11 as the lower bound of schedule damage, not the estimate.

**Deck outcomes:** Low ($55 flat) → NPV10 **−$96M**, IRR 9.2%. Base ($75) → +$288M, 12.3%. High ($90 flat) → +$547M, **14.2%** — still short of 15%.

### The three questions asked directly

**What oil price makes this a 15% IRR?** **US$96/bbl Brent**, flat, real, for the whole 2027–2045 path ($75 × 1.284). That is 28% above base and 7% above my high deck. In the plausible 2027–2035 range, **Limbayong does not earn 15% at any price**.

**What reserves number makes it break even?** **233 MMboe** (119.7 MMbbl + 681 bcf) — **86% of the booked 270.8 MMboe**. You can lose 14% of the reserves and still return 10%. For 15% IRR you need **325 MMboe, 120% of booked**. The band between "still stands" (86%) and "works properly" (120%) is narrow, and the booked number is a 2023 regulatory estimate for a field with no public well data.

**Is the gas monetisation material or cosmetic?** **Material and decisive — it is the project.** Removing gas (and the $650M pipeline) leaves NPV10 at **−$29M and IRR at 9.7%**: oil alone does not clear a 10% hurdle. Gas adds **$317M of NPV, 110% of the total**. Every one of the following is true simultaneously: the FPSO is justified by liquids throughput, the *value* is justified by gas, and the gas only works because it can be sold into a Sabah market at $6.50/MMBtu rather than at an LNG netback struck after liquefaction, shipping and the 5% state sales tax. The gas price floor is **$3.86/MMBtu** — below that the project is NPV-negative. At $10.22/MMBtu it reaches a 15% IRR, but that is above the RM30/MMBtu (~$7.1) domestic cap and is therefore not achievable into the Malaysian market.

---

## KEY JUDGEMENTS

1. **This is a 10%-hurdle project priced by a company that does not need 15%.** NPV10 of $288M on $2.9B of capital is a 1.10× PV/capex ratio. For a listed IOC that is a destroyer of value against a 15% cost of capital. For PCSB — 100% WI, sovereign balance sheet, explicit Sabah gas mandate — 12.3% real clears. FID is therefore rational *as policy*, not as portfolio economics. Say that plainly to the CEO: this is a strategic gas supply decision with an oil co-product, not an oil development with a gas by-product.

2. **The project's investability is manufactured by a tax incentive.** Remove the 60% investment allowance under the PITA (Investment Allowances) Regulations 2013 and NPV10 falls to **−$65M**. $353M of the $288M NPV — more than all of it — is the fiscal incentive. That is a defensible policy choice (deepwater, >200 m, marginal field, national gas supply) but the FDP should not be presented as commercially robust without naming this. If MOF declines or trims the IA, the project is dead on a 10% hurdle.

3. **Reserve risk dominates everything, and the public data cannot bound it.** −30% reserves → NPV −$384M. The field has a 2002 discovery, a 2014 oil confirmation, no public well data, no public seismic, and an operator paper whose title contains "Top Decile Reservoir Complexity" and "Marginal". A 14% shortfall breaks even. For a toe-thrust, faulted, compartmentalised turbidite with a 10-well development plan, a 14% shortfall is not a tail risk — it is close to the base case for this play type. **The single most valuable thing PCSB can do pre-first-oil is appraise, not accelerate.**

4. **Capex intensity of $11.45/boe is the number that will be quoted against this project.** That is roughly 1.7× Gumusut-Kakap (~$6,900/boe) and closing on Malikai (~$14,000/boe) — the two Sabah deepwater benchmarks that bracket "acceptable" and "cautionary tale". UTC of $21.06/boe follows from it. The driver is only 270.8 MMboe of reserves against $2.9B of capital; a 30% reserve upgrade alone would cut capex intensity to $8.24/boe and lift IRR to 16.3%. **UTC is the cleanest single metric for communicating why this field waited 24 years from discovery to FID** — and why the 2021–2023 standalone newbuild concept was cancelled.

5. **The $35M FPSO is the best capital decision in the project and the least analysed.** Buying a used cylindrical hull for 1.2% of total capex fundamentally changes the economics versus the 2021–2023 standalone newbuild concept that was cancelled as "commercially unviable". But a used 1990s hull carries condition, life-extension and uptime risk that a Class 4 estimate cannot see. The $200M abandonment and $450M conversion are judgements, not quotes. If the hull needs $650M rather than $450M, that is roughly **−$85M of NPV** — 30% of the project's margin.

6. **45.6% total take is light for Malaysia and I do not fully believe it.** Published Malaysia PSC splits typically show 60–70% government take. My 45.6% reflects DW terms (70%/80% cost recovery, 50% profit split, 10% royalty, no supplementary payment modelled) plus a 60% IA. If the actual Limbayong PSC carries a supplementary payment, a higher profit share to PETRONAS, or no investment allowance, contractor NPV falls by a further $200–350M. **This is the single largest fiscal uncertainty and it is unresolvable from public sources.**

7. **Breakeven at $60 is a 20% cushion, not a comfortable one.** With Class 4 capex (−30%/+50%) and reserves that could plausibly be −30%, the joint probability of falling below breakeven is not small. A portfolio manager should treat $60 as the *central* breakeven and $75–80 as the *robust* one — the price at which the project survives a simultaneous 20% reserve shortfall and 20% capex overrun.

---

## WHAT WOULD CHANGE MY MIND

**Would make me more positive:**
- **SURF scope confirmed at $250M all-in.** Worth **+$107M of NPV** (→ $395M) and IRR to 13.4%. Note the structural point: **each $1 of capex only costs the contractor $0.43 of NPV**, because cost recovery, the investment allowance and the capital allowance return more than half of it. That is also why the capex tornado is smaller than the reserves tornado — shortfalls are punished far harder than overruns.
- **A reserve audit or appraisal well result above 325 MMboe.** That is the 15%-IRR threshold. One good step-out well at the L-B-P trend could do it.
- **Confirmation that Limbayong's PSC carries the 2018 deepwater enhancements.** Those were explicitly designed to improve DW returns; if they include a higher cost recovery ceiling or better profit split than the 1993 table, my NPV is understated by an unknown but material amount.
- **A reduced or nil royalty in the actual PSC.** Some Malaysian deepwater vintages departed from the standard 10%. Removing 5 percentage points of royalty is worth **+$120M of NPV** (verified by re-run: 5% royalty → NPV $408M); nil royalty is worth +$239M. I model the published 10% because that is what the MPM table says; the PSC text itself is [U].
- **Gas price above $8/MMBtu contracted with a Sabah offtaker.** Each $1/MMBtu on gas is roughly $100M of NPV at these volumes. $10.22/MMBtu delivers 15% IRR.
- **Capex below $2,340M** (a 19% underspend). That requires roughly $560M of savings — conversion at $350M, drilling at $70M/well, pipeline at $500M and SURF at $500M, all at once. It is the full −30% Class 4 outcome, not one or two good contracts. Possible; not plannable.

**Would make me more negative:**
- **Any reserve downgrade below 233 MMboe.** The project is then NPV-negative at base deck.
- **Loss or reduction of the 60% investment allowance.** NPV goes to −$65M immediately. This is the highest-severity single-point fiscal risk in the model.
- **A supplementary payment or a profit-split step-down appearing in the actual PSC text.**
- **FPSO conversion above $550M, or first oil slipping beyond 2031 with cost escalation** (not mere deferral — deferral alone is nearly free).
- **A gas offtake priced at an LNG netback (~$4.50/MMBtu) rather than domestic Malaysian pricing.** That takes NPV to **+$74M at 10.6%** — the project becomes an oil-equivalent development that barely clears 10%, and most of the 790 bcf is stranded value.

---

## CONFIDENCE

| Element | Confidence | Why |
|---|---|---|
| Fiscal mechanics (royalty 10%, cess 0.5%, export duty 10%, PIT 38%, 70%/80% ceilings, volume-based profit split, 60% IA) | **High** | Each is anchored to a published Malaysian instrument or MPM fiscal table. The *applicability* of the 1993 DW table to this specific PSC is the weak link, not the rates |
| Production profile shape | **Medium** | Plateau is anchored to published design capacity (40 kbopd, 150 mmscfd); ramp, decline rates and 2030 first oil are judgement. Profile shape changes NPV by ±15% at constant reserves |
| Reserves | **Medium-low** | 139 MMbbl / 790.9 bcf are a third-party tracker's figure for a field with no public well data. The 86% breakeven threshold means this is the binding uncertainty |
| Capex $2,900M | **Low-medium** | AACE Class 4 by construction. Every line except the $35M FPSO and the $75–250M iEPCI band is a benchmark, not a quote. ±30/50% is honest; ±50% is arguable |
| Opex $95M/yr + $4/boe | **Low-medium** | Benchmark for a 40 kbopd/150 mmscfd deepwater hub. Late-life opex on a used hull is genuinely unknown |
| Gas price $6.50/MMBtu | **Medium** | Sits between the domestic power cap ($7.1) and a netback after processing. But no GSA is public and CO₂ content could force a discount I cannot quantify |
| **NPV10 = +$288M** | **Low-medium** | Correct arithmetic, Class 4 inputs, and it sits only 10% above zero. The honest range is **−$400M to +$850M**, i.e. the sign is not robust |
| **IRR = 12.3%** | **Low-medium** | ±3.5 points across the reasonable input range. "Not quite 15%" is the robust conclusion; "12.3%" is not |
| **Breakeven $60/bbl** | **Medium** | More robust than NPV because it is a ratio — but it inherits the same reserve and capex uncertainty. True range $50–$72 |
| Gas is material, not cosmetic | **High** | The oil-only counterfactual (−$29M NPV, 9.7% IRR) is a structural result, not a marginal one. It survives wide changes in gas price and pipeline cost |

**Single sentence of confidence:** I am confident in the *shape* of the answer — a marginal, gas-led, incentive-dependent deepwater development that clears 10% and fails 15% — and not confident in the *precision* of any one number in it.

---

## SOURCES

1. **Petroleum (Income Tax) Act 1967 (Act 543)** — 38% petroleum income tax; Second Schedule capital allowances; consolidated text as at 1 Jan 2026. hasil.gov.my.
2. **Petroleum (Income Tax) (Investment Allowances) Regulations 2013, P.U.(A) 120** — 60% investment allowance on QCE for qualifying projects including **Deepwater Project (>200 m)**; exemption capped at 70% of statutory income. Text via Moore Stephens tax flash; guidelines via MOF "Guidelines on Application of Tax Incentives for Upstream Petroleum Industry".
3. **Malaysia Petroleum Management (PETRONAS), Fiscal Terms** — PSC taxonomy, DW/UDW terms by water depth, R/C structure. petronas.com/mpm.
4. **Malaysia PMU / APEX 2013 booklet, "Malaysia — Petroleum & Investment"** — the DW PSC terms table used here: royalty 10%, export duty 10% (exported oil only), PIT 38%, research cess 0.5%, cost ceiling DW oil 70% / gas 80%, UDW oil 75%, volume-based profit split (oil 50/60/70% at 100/200 MMbbl; gas 50/60/70% at 2/4 tscf), PCSB participation min 15%, production period 25 yr.
5. **Oil & Gas Journal, 22 Nov 1993** — SK-A/SK-B deepwater licence terms, corroborating the 70–75% cost recovery ceilings and volume-based profit splits for Malaysian DW acreage.
6. **MPM, "Other Governing Laws"** — Sabah State Sales Tax Enactment 1998: crude, natural gas, LNG, condensates all at **5%**, effective 1 Apr 2020.
7. **IMF, "Natural Resource Taxation in the Asia-Pacific Region", 2015** — federal **export duty 10%** on petroleum crude exported from Malaysia.
8. **EIA Short-Term Energy Outlook, released 6 Oct 2026** — Brent $96/b 2026, **$84/b 2027**; 2025 actual $69/b. eia.gov/outlooks/steo.
9. **PETRONAS Energy & Gas Trading, "Gas Pricing & Tariff"** — Malaysia Reference Price (MRP) mechanism (LNG FOB weighted average, 6–7 month lag to Brent).
10. **Gas Malaysia Berhad notice, Q4 2025** — MRP = **RM36.64/MMBtu** (≈US$8.7 at 4.2 RM/USD).
11. **The Edge Malaysia, 28 Aug 2023** — domestic piped gas to the power sector capped at **RM30/MMBtu** for the first 1,000 mmscfd.
12. **Upstream, 27 Nov 2018** — PETRONAS introduced enhancements to deepwater PSC terms (content paywalled; existence and date confirmed). Not quantified in this model — upside.
13. **The Star / Bursa Malaysia filing, 20 Aug 2026** — DNeX agrees to sell FPSO Excalibur to MISC for **US$35M** cash.
14. **TechnipFMC press release / MaritimeMagz, 15 Sep 2026** — iEPCI award, full subsea scope, **US$75–250M**.
15. **Global Energy Monitor, Global Oil & Gas Extraction Tracker (data year 2023)** — 139.0 MMbbl liquids, 790.9 bcf gas, design capacity 14.53 MMbbl/y and 1,550.4 MMm³/y.
16. **SPE 210079-MS (2022), "Limbayong: Decoding Industry Top Decile Reservoir Complexity for Marginal Deepwater Development"** — PETRONAS Carigali authors; the operator's own characterisation of reservoir complexity and project marginality.
17. **Welligence** — PCSB 100% working interest, operatorship.

*Model: `evidence/s7_model.py` (engine), `evidence/s7_metrics.py` (metrics, breakevens, tornado). Reproducible with `python3 s7_metrics.py` from that directory. Pure stdlib — no external dependencies.*
