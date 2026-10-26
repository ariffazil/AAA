---
name: upstream-e-p-capital-intelligence
description: Analyze upstream oil & gas news (M&A, exploration results, divestments, tax disputes) into capital-intelligence verdicts and E&P sunk-cost/portfolio models. Covers paywall recovery for trade press (Upstream/BNamericas), deal-ledger building, exploration/development cost benchmarking, Brazil tax-exposure screening, and the WEALTH CEO briefing format. Use when asked to "estimate total/sunk cost", "analyse this deal", "is this an exit?", or given the WEALTH CEO hat on an energy story.
---

# Upstream E&P Capital Intelligence

Class of work: Arif pastes an upstream energy link (Upstream Online, BNamericas, Reuters, company releases) and wants a verdict, a deal teardown, or a total-cost/sunk-cost estimate with real benchmarks and modelling — delivered in WEALTH CEO voice (capital intelligence: NPV/EMV/risk), with GEOX basin context where relevant.

## Workflow

### 1. Extract + paywall recovery
- `web_extract` the URL first. Upstream Online returns headline + one line + "My Alerts is a service for subscribers" boilerplate.
- NEVER stop at the paywall. Recover substance by searching the headline phrase + entity (e.g. `Petronas relinquishes Brazil block Mola prospect`) across:
  - BNamericas — often the same story in full text
  - Trade aggregators: oilnow.gy, offshore-energy.biz, brazilenergyinsight.com, energy-pedia.com, euro-petrole.com, keyfactsenergy.com, oedigital.com, cyprusshippingnews.com
  - Company press releases (petronas.com/media, totalenergies.com/newsroom, qatarenergy.qa)
  - SEC EDGAR 6-K filings for listed partners (Petrobras = sec.gov/Archives/edgar)
  - LinkedIn reposts of the article often carry full text
- A paywall headline alone is [OBS] but insufficient — corroborate every number with a second source before it enters the ledger.

### 2. Build the entry ledger (every dollar in)
Each entry point with actual headline amounts, date, and WI%:
- SPA / acquisition price — verify the deal actually CLOSED (see OGX pitfall)
- Bid-round signature bonuses (ANP rounds): get the TOTAL bonus, multiply by your party's WI%
- ToR Surplus / PSC compensation paid to Petrobras: partners pay pro-rata their share of the 70% non-Petrobras interest — compute `WI/70 × total paid`
- Open-acreage / permanent-offer bonuses (often small)

### 3. Benchmark exploration spend
- Ultra-deepwater (3,000 m WD) dry hole: US$100–140M all-in
- P&A + rig demobilisation: ~US$30M
- G&G / 3D reprocessing per block: US$20–50M
- Permit maintenance on held-undrilled blocks: ~US$5–10M/yr
- Operator well names (e.g. 1-PPBL-1-RJS) let you confirm rig + spud/TD/P&A dates via trade press (Brazil Energy Insight publishes these).

### 4. Development capex = WI-share of operator-disclosed contracts
- FPSO EPC values are public: Seatrium P-84/P-85 S$11bn ≈ US$8.16bn for two 225kbpd units; 180kbpd conversion ≈ US$4.4bn (MODEC Carioca class)
- SURF: Subsea7/TechnipFMC "supermajor contract" thresholds (>US$1.25bn)
- Wells: SLB/operator disclosures (e.g. up to 35 wells for Atapu/Sépia-2)
- Apply the CURRENT WI — dilution happens after entry (Petronas Sépia 21% → 12.7% after Petrobras exercised pre-emption rights).

### 5. Tax exposure screening (Brazil-specific)
- Search CARF/RFB cases by the entity AND by comparable peers — IOCs with intercompany rig/FPSO charters get hit under CUP-vs-ROACE analysis:
  - Shell Brasil: CARF Acórdão 2202-010.938 (Oct 2024), R$437M confirmed, rig-charter CUP
  - Petrobras: CARF 16682.721153/2024-88 (Mar 2026), ~R$1.24bn platform-charter IRPJ/CSLL
- Law 14,596/2023: OECD arm's-length mandatory from FY2024 (IN RFB 2,161/2023); first assessments enter the audit cycle mid-2026
- 75% default penalty; bipartição can halve penalties with cooperation; doc penalties 0.2–3% capped R$5M/yr
- NEVER present modelled exposure as adjudicated — tag it explicitly as modelled.

### 6. Recoveries (every dollar out)
- Divestment proceeds (actual announced values, incl. deferred tranches)
- Operating cashflow from producing assets: production × netback (real US$/bbl net of opex/royalties/taxes) × holding years

### 7. Model + deliver
- Gross sunk = entry + exploration + development + G&A + tax exposure
- Net sunk = gross − recoveries
- Economic sunk: exclude committed-but-unspent forward capex — the accounting-vs-economic distinction is usually the headline difference
- Remaining portfolio NPV at hurdle (8/12/15%) vs net sunk → answer "is this actually a loss?"
- BRL→USD: use year-appropriate FX (≈4.0 in 2019, ≈5.0 in 2021+) and state the assumption

## WEALTH CEO deliverable format
1. Verdict first — one line, no preamble, no flattery
2. Methodology snapshot table (approach, currency, discounting, what's out of scope)
3. Cost ledger table: cat / line item / date / mid / low / high / source-basis
4. Bottom line table (gross, recoveries, net; low/mid/high)
5. Thematic deep-dives (tax drama, recoveries story)
6. NPV sensitivity table (price ±, hurdle 8/12/15%)
7. "Where I might be wrong" table with direction + magnitude
8. One-line ledger for the sovereign ("23 years, $X gross, $Y recovered, $Z net, portfolio NPV $W → verdict")

## Pitfalls
- **Rescinded deals are NOT sunk cost**: Petronas–OGX US$850M SPA (May 2013) was rescinded Oct 2013 before close — only legal/BD burn counts. Always verify close before counting an acquisition.
- **ToR compensation math**: Petrobras's Sépia R$14.55bn compensation was the amount PAID by the 70% partners (Petronas share = 21/70 of it, ≈US$873M), not 21% of something else.
- **WI dilution after entry**: use latest disclosed WI for forward capex, not entry WI.
- **Adjudicated vs modelled tax**: Shell/Petrobras CARF cases are precedents for exposure, NOT the target company's liabilities.
- **Don't double count** FPSO build cost vs charter rate — pick one basis (capex share) and note the other.
- **Epistemic labels mandatory**: every number [OBS] (sourced) or [INT] (derived) — F2 binding.
- **Single-case verdicts need a control set.** A score against a tripwire (e.g. "70.5% of PAT as dividend = VOID") is a verdict without meaning unless the panel of comparable NOCs is shown. Default peer set for any NOC capital verdict: **Aramco, Equinor, PTT, Ecopetrol, Petrobras, ADNOC Gas** (and where relevant ADNOC Distribution / ADNOC L&S). Aramco's FY2025 NI/distribution ratio of 91.5% reads as near-extraction; PETRONAS at 70.5% reads as median-of-cluster once the table is in front of the reader. Same rule applies to gearing (Aramco 3.8%, Petrobras ~1.0× net debt/EBITDA, ADNOC Gas ~0.55×, Equinor net debt/capital 17.8%), FCF-after-capex+div, reserve replacement, governance composition. **Build the peer table before the verdict line, not after.** Without peers, every number is a single case — a structural defect the moment it ships publicly.
- **Treat dashboard/briefing outputs the same as the underlying analysis.** A disclaimer at the bottom ("model output, not forensic") does NOT exempt the body from the same base-rate rigor. Apply the same control set to anything you publish as to anything you seal.
- **Constitutional tripwires with exit conditions must score UNMEASURED, not cleared, when inputs are partial.** If the denominator for a ratio isn't yet published (e.g. FY-end PAT not yet announced, only a declared dividend known), score the tripwire **UNMEASURED** — never extrapolate against an unpublished denominator just to claim clearance. Exit conditions typically require `value < threshold sustained over 2 audit periods AND a separate axis above its threshold`; both must be evidenced.
- **ConocoPhillips-style IOC exit is a structural canary**, not a one-line headline. When a major counterparty walks from a jurisdiction citing regulatory uncertainty, it raises the cost of capital for every deal inside that jurisdiction and shifts the SPINE-layer reading of any sovereign-extraction analysis. Record it under reserve-replacement and SPINE-class tripwires.

## References
- `references/petronas-brasil-2026.md` — full Petronas Brasil deal ledger (2003–2026): amounts, dates, sources, cost benchmarks, model mid-points. Worked example of this whole workflow.
- `/root/AAA/skills/pdf-report-generation/references/noc-control-set-fy2025.md` (under pdf-report-generation) — default NOC peer panel for any single-NOC verdict: Aramco, Equinor, PTT, Ecopetrol, Petrobras, ADNOC Gas + PETRONAS FY2025 financials. Always pair verdict lines against this table; single-case scoring = INADMISSIBLE.
