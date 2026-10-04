# Report Content Workflow — Research → Model → Deliverable

Method proven 2026-08-06 on the Petronas Brasil sunk-cost brief (WEALTH CEO request). Reusable for any "total cost / sunk cost / how much did X spend in Y" question.

## 1. Paywalled article triangulation
- `web_extract` on a paywalled URL returns headline + lede only. Do NOT invent the body.
- Search the headline's key terms; secondary trade press (BNamericas, Reuters, company press releases, energy-pedia, OilNOW) usually carries the full substance.
- Reconcile facts across 2+ sources before quoting numbers; tag OBS (contracted/disclosed fact), DER (derived from disclosed figures), INT (benchmarked judgement).

## 2. Bottom-up sunk-cost / total-cost ledger
Build categories, each with Low / Mid / High:
- **Acquisitions & signature bonuses** — contracted headline values from company press releases + regulator round results (ANP for Brazil).
- **Verify closure** — a rescinded deal costs only legal/transaction fees. Example: OGX $850M agreed May 2013, rescinded Oct 2013 before payment; OGX filed bankruptcy 30 Oct 2013. Count the avoided $850M as an outcome, not a cost.
- **Minority WI discipline** — count only the working-interest share (Sépia 21%, Água Marinha 20% → 21%/20% of project cost), never the operator's full project cost.
- **Exploration** — benchmark dry-hole cost by water depth: ~$100M+ at 3,000 m ultra-deepwater; add G&G $20–50M and P&A $25–40M per well campaign.
- **Development** — WI share of operator-disclosed EPC contracts: FPSO newbuild ≈ $4B+ each (Seatrium P-84/P-85 twin = $8.16B; Subsea7 SURF > $1.25B; MODEC/Mitsui charter consortia), plus opex via production × netback × holding period.
- **Tax exposure when no company-specific case exists** — model from peer CARF precedents scaled by footprint, label INT, give a range. Brazilian precedents:
  - Shell Brasil CARF 2202-010.938 (Oct 2024): R$437M confirmed — CUP method on intercompany rig charters.
  - Petrobras CARF 16682.721153/2024-88 (Mar 2026): ~R$1.24B partial — rig-charter vs ROACE.
  - Regime: Law 14,596/2023 = OECD arm's-length from FY2024; 75% default penalty; bipartição halves it for cooperative taxpayers.
- **Recoveries** = divestment proceeds AND operating cashflow (production × netback × holding period). A producing asset that repaid its acquisition cost flips the whole account (TV/EM-III: $1.3B in, ~$2.06B cashflow + $450M sale out).
- **Net sunk** = gross − recoveries. **Economic loss** = net sunk − remaining-portfolio NPV.

## 3. Sensitivity conventions
- Oil price dominates: at ~$6.7B gross scale, ±$15/bbl ≈ ±$800M swing. Discount rates 8/12/15%.
- ExxonMobil modeling toolkit (investor.exxonmobil.com/modeling-toolkit): built for XOM's own fiscal regimes (GoM/Permian/Guyana) — NOT suitable for modelling third-party NOCs in Brazil. Borrow only its sensitivity framework (oil ±20%, hurdle 8/12/15%, hyperbolic decline). Brazil needs concession + PSC + ToR-surplus handling from operator business plans (Petrobras 2025–29: $111B, $77B E&P).

## 4. Deliverable shape
- Numbers → visuals in body (waterfall, donut, timeline, tornado); tables → appendix (see umbrella SKILL.md).
- Verdict-first, ranges everywhere, "where I could be wrong" section ranked by swing size.
