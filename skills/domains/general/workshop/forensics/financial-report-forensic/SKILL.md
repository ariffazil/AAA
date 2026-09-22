---
name: financial-report-forensic
description: "Audit IR-deck visuals, custom ratios, non-cash recognition."
author: hermes-asi
license: MIT
version: 1.0.0
tags: [finance, forensic, peer-benchmark, ir-deck, gearing, sec-edgar, yfinance]
metadata:
  hermes:
    tags: [finance, audit, peer-benchmark, ir-deck]
    related_skills: [petronas-petros-shell-dispute, malaysia-reality-stack-primary-source-routing]
capability_tier: fed-long-context
ecology_state: WARM
---

# Financial Report Forensic — IR-Deck X-Ray

When a company publishes "resilient", "in line with peers", "steady gearing", or "disciplined CAPEX" framing and the user smells marketing, run this audit. Three concrete lessons from the PETRONAS 1H FY2026 case (29 Aug 2026):

1. **Peer benchmark visuals are decoys.** Company-published "Peer Group" bands show **min-max range**, with the company line aligned to the **top of the band**, while the "Average" line sits well below. Audit by pulling each peer's primary 10-Q/6-K from SEC EDGAR.

2. **Custom gearing formulas suppress standard ratios.** Companies use Debt / (Equity + Debt + adjustments) instead of standard Debt / Equity. Recalculate standard gearing and net debt position. Often the company is in **net cash position** and the "rising gearing" framing is **manufactured anxiety**.

3. **CAPEX-by-business hides accounting recognition.** Headline CAPEX includes **non-cash items** (e.g. accumulated loss recognition from JV acquisition). Separate real cash CAPEX from accounting composition. Allocation inversion (most CAPEX to loss-making segment) is the signature of late-cycle NOC harvesting.

## When to Trigger

- User pushes back on a specific visual, table, or framing in a company IR deck
- User asks "is this real?" or "x kena" about an apparent anomaly
- User says "bullshit" or "acah" on any IR/marketing narrative
- User requests peer benchmarking against a specific company

## Required Inputs

- Company IR materials (media release + PDF financial report + Highlights deck if available)
- Peer list (IOC majors typically: BP, Shell, ExxonMobil, Chevron, TotalEnergies, ConocoPhillips, Eni, Equinor; NOC if comparable: PTT, Saudi Aramco, Petrobras, Petronas)
- Reference period (typically most recent quarterly/half-year/full-year)

## Output Shape

A multi-pass audit, each pass producing one artifact:

| Pass | Output | Purpose |
|---|---|---|
| 1 | Anchor data table (CSV + JSON) | Source of truth for all metrics |
| 2 | Markdown contrast + void analysis | Surface what media release omits |
| 3 | Void resolution via full IFR/PDF extraction | Close each gap with primary source |
| 4 | Peer benchmark forensic + custom ratio recalc | Verify visual claims against primary data |

Always tag every claim with `[OBS]` / `[DER]` / `[INT]` internally, strip labels from human output per SOUL.md.

## Workflow

### Step 1: Primary Source Acquisition

For Malaysian NOCs (PETRONAS, etc.):
```
# 1a. Media release — petronas.com/media/media-releases/
curl -sL -A "Mozilla/5.0 Chrome/124" "https://www.petronas.com/media/media-releases/<slug>" -o /tmp/mr.html

# 1b. Highlights deck (PowerPoint, marked "Internal") — /investor-relations/financial-results listing
curl -sL -A "Mozilla/5.0 Chrome/124" "https://www.petronas.com/investor-relations/financial-results" -o /tmp/listing.html
# Look for: /sites/default/files/...FRA...Highlights.pdf AND ...Interim Financial Report...pdf
# Both files usually exist; download both.

# 1c. Full IFR PDF — extract text
pdftotext -layout /tmp/petronas_ifr_1h2026.pdf /tmp/petronas_ifr_1h2026.txt
```

For IOC majors (XOM, CVX, SHEL, BP, TTE, COP, EQNR):
```python
# Use yfinance — pulls from SEC EDGAR XBRL filings
import yfinance as yf
t = yf.Ticker("XOM")
qis = t.quarterly_income_stmt
# Sum Q1+Q2 of each year for 1H aggregation
```

### Step 2: Peer Benchmark Forensic (4-step)

1. **Identify the visual trick.** Does the chart show min-max band, IQR, or single-peer line? Where does the company line sit relative to the band's top/bottom/middle?
2. **Pull primary data.** `yfinance` for IOC, direct IR PDFs for NOC. Aggregate Q1+Q2 for half-year periods.
3. **Compute peer median + average + max + min.** Plot as horizontal bar with company line overlaid at both reported and ex-special-items levels.
4. **Identify the special item.** Read footnote disclosures in the full IFR. Common patterns: PRefChem-style JV loss recognition, asset impairment, divestment gains.

### Step 3: Gearing Ratio Forensic

Standard formulas vs company-adjusted:
```
Gearing_company  = Debt / (Equity + DefTax + Debt)        # custom
Gearing_std      = Debt / Equity                          # standard
Gearing_netdebt  = (Debt - Cash) / Equity                 # net
```

Always compute all three. The company "rising gearing" is often offset by **net cash position** that the custom formula hides. Also check:
- USD exposure (87% of borrowings is common for EM-commodity corporates)
- Refinancing wall (current portion % of total)
- Off-balance-sheet via DSU/guarantees (Note A8 style)

### Step 4: CAPEX Resource Allocation Audit

1. Get segment-level CAPEX and segment PAT (from operating segment notes in IFR).
2. Compute CAPEX/Segment PAT ratio per segment. **Flag segments where CAPEX > PAT** — capital going to loss-makers.
3. Identify non-cash items in CAPEX (footnote disclosures).
4. Compute **real cash CAPEX** = Headline CAPEX − Non-cash recognition.
5. Compute CAPEX by geography (Malaysia % vs international %).

### Step 5: Federal/State Dependency Stack

For NOCs and government-linked entities (GLCs), quantify total dependency:
- Dividend floor (FY-approved)
- Cash payments to government (Note A10 "Federal and State Governments")
- Sales to GLCs / Govt-related entities (Note A10 "Government of Malaysia's related entities")
- Lease income from government
- Tax expense (effective rate vs headline)

Total dependency per annum = sum of all flows TO government. For PETRONAS 1H 2026, = ~RM46.5B annualised (dividend RM20B + cash RM11.7B + GLC sales RM13.8B + lease RM1B).

## Pitfalls

- **Never source a financial number from a news article when the primary report exists.** Reporters compress three distinct metrics — *cash and cash equivalents*, *net cash (cash less borrowings)*, and *cash flow from operations* — into "cash". They are not interchangeable. Pull the FRA/IFR first; cite news only for facts the report does not contain (and label it secondary).
- **Never annualise a balance-sheet delta and call it a burn rate.** A six-month change in net cash can be driven by new borrowings, FX translation, or dividends declared — none of which are operating burn. Check the borrowings line before using any cash delta as a run-rate. (PETRONAS 1H26: net cash fell ~RM16B, but RM5.2B of that was *borrowings rising* RM121.6B → RM126.8B.)
- **Never build a savings-vs-loss comparison on an assumed unit cost.** "Headcount × assumed average cost" produces a number that looks precise and cannot be verified. If the average is assumed, the comparison is not evidence — say so or drop it.
- **Check whether a segment loss is an operating result or an accounting recognition.** JV loss recognition on capital injection is a balance-sheet event, not a period loss. Read the wording: "recognition of accumulated share of losses … previously recorded at the joint venture level" means the segment may have been operationally profitable in the period.
- **Don't trust company peer benchmarks.** They use min-max band to align company with top, average line below. Always pull primary 10-Q/6-K.
- **Don't trust "rising gearing" narrative.** Always check net debt = (Debt − Cash) position. If net cash, gearing is artificial.
- **Don't conflate headline CAPEX with cash deployment.** Read footnote disclosures for non-cash accounting composition.
- **Don't accept custom ratios.** Recalculate using standard formulas: Debt/Equity, Net Debt/EBITDA, current portion % of total borrowings.
- **Don't dismiss IR deck disclaimers.** "PETRONAS is not responsible for errors or omissions" is legal cover for visual manipulation — flag explicitly.
- **Don't skip the full PDF.** Media release is the marketing layer; full IFR is the audit layer. Footnotes contain the voids the press release omits.

## Verification

For each pass, ground at least one claim in a primary source (SEC EDGAR accession, company IFR page reference, official press release URL). Mark primary sources inline. Self-correction note: when prior-pass assumptions turn out wrong (e.g. ROACE "contracting" → actually stabilising), embed the correction in next pass.

## Reusable Outputs

- Anchor table CSV/JSON (12-row × 6-col typical)
- 6-panel chart set: trajectory line, CAPEX vs CFFO, YoY heatmap, production scatter, quantum radar, PRefChem waterfall
- For forensic pass: peer benchmark bar, net debt position, CAPEX allocation inversion, federal dependency stack
- 5-page PDF briefing via reportlab

## Related Skills

- `petronas-petros-shell-dispute` — PETRONAS-specific constitutional/geopolitical layer (does NOT cover financial-report forensic — this skill fills that gap)
- `malaysia-reality-stack-primary-source-routing` — routing rules for Malaysia primary sources (BNM, DOSM, parlimen, etc.) — useful for sovereign/macro context
- `agi-decisions-reflect` — post-task lightweight reflection
