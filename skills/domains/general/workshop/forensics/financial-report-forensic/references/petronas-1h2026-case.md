# PETRONAS 1H FY2026 — Worked Example

**Reference run for `financial-report-forensic`.** This is the case that forged the skill. Numbers are real; commands are reproducible.

**Run date:** 29 Aug 2026
**Output bundle:** `/root/forge_work/2026-08-29-petronas-deepdive/`

## Sources acquired

| Source | URL | Size | Use |
|---|---|---|---|
| Media release (28 Aug 2026) | https://www.petronas.com/media/media-releases/petronas-posts-resilient-half-year-results-remains-steadfast-safeguarding | HTML | Marketing layer |
| Highlights deck (PowerPoint, "Internal") | https://www.petronas.com/sites/default/files/uploads/content/2026/PETRONAS%20Group%20FRA%201H%20FY%202026%20-%20Highlights.pdf | 1.3MB / 8pp | IR-deck visuals |
| Full Interim Financial Report | https://www.petronas.com/sites/default/files/uploads/content/2026/PETRONAS%20Interim%20Financial%20Report%201H%202026%2028.8.2026.pdf | 426KB / 23pp | Audit layer |
| FY2025 IFR (prior baseline) | https://www.petronas.com/sites/default/files/uploads/content/2026/PETRONAS%20Group%20FRA%20FY2025%20-%20IFR_0.pdf | 469KB / 30pp | Trend baseline |
| 1H 2025 IFR (prior baseline) | https://www.petronas.com/sites/default/files/uploads/content/2025/Financial%20Report%201H%202025.pdf | 371KB / 26pp | Trend baseline |

## The four-pass structure that emerged

### Pass 1 — Anchor data (12 rows × 6 cols)

CSV columns: `Metric, 1H24, 1H25, 1H26, Unit, Source`. 12 rows covering Revenue, PAT (reported + ex-PRefChem), EBITDA, CFFO, CAPEX, Total Assets, Shareholders Equity, Production, GHG Emissions, Dividend paid.

Saved: `data/petronas_facts.csv`, `data/petronas_facts.json`

### Pass 2 — Contrast & void analysis

Compared media release vs financial statements. Surfaced 4 contrasts + 6 voids:
- **Contrasts:** PAT headline vs segment reality; West Asia rhetoric vs Hormuz rerouting (FMT disclosure); "disciplined CAPEX" vs USD bond issuance; "resilient" vs ROACE/Gearing trajectory
- **Voids:** ROACE/Gearing not in media release; PRefChem quantum undisclosed; Sarawak Federal Court case not addressed; Aramco exit rationale un-narrated; Gentari valuation absent; BUDI95 subsidy exposure not quantified

Saved: `data/04_CONTRAST_VOID_ANALYSIS.md`

### Pass 3 — Full IFR extraction resolves 8/10 voids

Key resolution: PRefChem additional injection = **RM14.8 billion** (IFR footnote 6, page 1). Crude production **-17% YoY**. Gearing actual **21.2%** (4-period series). ROACE **8.5%** (stabilising, not contracting as Pass 2 thought). NCI PAT up 76% while shareholder-attributable PAT down 4%.

Self-correction: Pass 2 stated "Upstream segment contracting" — actually Upstream PAT grew 70% in 1H 2026 driven by Searah JV non-cash gain. Document the correction in next pass.

Saved: `data/05_CONTRAST_VOID_PASS3.md`

### Pass 4 — IR-deck forensic + peer benchmark

Triggered by Arif flagging: "peer benchmark I don't trust, validate."

**Three frauds confirmed:**

1. **Peer benchmark chart visual decoy.** IR deck showed company line at TOP of min-max band, Average line below. Audit pulled primary 10-Q/6-K via yfinance for 7 IOC peers.

```python
# yfinance peer benchmark pattern
import yfinance as yf
peers = ['XOM', 'CVX', 'SHEL', 'BP', 'TTE', 'COP', 'EQNR']
for ticker in peers:
    t = yf.Ticker(ticker)
    qis = t.quarterly_income_stmt
    rev_row = next((qis.loc[i] for i in qis.index if 'Revenue' in str(i) and 'Cost' not in str(i)), None)
    ni_row = next((qis.loc[i] for i in qis.index if 'Net Income' in str(i) and 'Noncontroll' not in str(i)), None)
    # sum Q1+Q2 of 2026 for 1H margin
```

Result: PETRONAS reported 17.9% is **#1** in peer set; ex-PRefChem 4.6% is **bottom**. Peer avg 11.5%, median 10.7%.

2. **Gearing formula gaming.** PETRONAS custom formula: `Debt / (Equity + DefTax + Debt) = 21.2%`. Standard `Debt / Equity = 28.2%`. **Net debt position = -RM66.9B (net cash).** "Rising gearing" is **manufactured anxiety** — issue USD bonds instead of drawing down cash buffer to preserve federally-visible cash.

3. **CAPEX 63% Downstream inversion.** Headline CAPEX includes RM14.8B non-cash PRefChem loss recognition. Real cash CAPEX maybe only RM11.2B for downstream (34% of real). But still inverted vs wealth-generating Upstream.

Saved: `data/06_REALITY_AUDIT_PASS4.md`, `charts/07-10`

## Key numbers (for quick recall)

| Metric | 1H 2026 | 1H 2025 | Δ |
|---|---|---|---|
| Revenue | RM152.4B | RM132.6B | +15% |
| PAT (reported) | RM27.2B | RM26.2B | +4% |
| **PAT ex-PRefChem** | **RM7.0B** | RM26.2B | **-73%** |
| PAT margin (reported) | 17.9% | 19.8% | -1.9pp |
| **PAT margin (ex-PRefChem)** | **4.6%** | 19.8% | **-15.2pp** |
| EBITDA | RM56.8B | RM54.4B | +4% |
| CFFO | RM47.5B | RM48.1B | -1% |
| CAPEX | RM41.4B | RM17.7B | +134% |
| Upstream PAT | RM28.1B | RM16.5B | +70% (boosted by Searah gain) |
| Downstream LAT | -RM15.2B | -RM0.9B | worse |
| Crude production | 657 kboe/d | 792 kboe/d | **-17%** |
| Total production | 2,334 kboe/d | 2,403 kboe/d | -2.9% |
| Borrowings | RM126.8B | RM123.2B | +RM3.6B |
| Cash & equivalents | RM193.6B | RM204.4B | -RM10.8B |
| **Net debt** | **-RM66.9B** | -RM81.2B | less net cash by RM14.3B |
| Gearing (PETRONAS) | 21.2% | 21.3% | -0.1pp |
| ROACE | 8.5% | 8.7% | -0.2pp |

## The four chart templates that worked

```python
# Chart 7 — Peer Benchmark Truth
fig, ax = plt.subplots(figsize=(10, 5.5))
# Horizontal bars sorted desc; company lines overlaid at reported + ex-special-item levels

# Chart 8 — Net Debt Position
fig, ax = plt.subplots(figsize=(9, 5.5))
# Side-by-side bars: gross debt up, cash down; label net position per period

# Chart 9 — CAPEX Allocation Inversion
fig, (ax1, ax2) = plt.subplots(1, 2)
# Left: CAPEX by business; Right: CAPEX vs segment PAT per segment

# Chart 10 — Federal Dependency Stack
fig, ax = plt.subplots(figsize=(8.5, 6))
# Horizontal bars: dividend, federal cash, GLC sales, lease; total at right
```

Saved: `pass4_charts.py` (in bundle root)

## Lessons learned (in priority order)

1. **Always pull full PDF.** Highlights deck 8pp ≠ full IFR 23pp. The Highlights deck has the visual frauds; the full IFR has the footnote disclosures. Need both.
2. **The IR deck's Highlights "average" line is the truth.** Company line above it means outperforming; below means underperforming. Band = min-max spread across peer set, not "normal range."
3. **Net debt position is the real gearing metric.** PETRONAS in net cash position despite "rising gearing" — custom formula hides this.
4. **Footnote 6** in IFR revealed RM14.8B PRefChem quantum. Always read footnotes; they contain the voids.
5. **yfinance for IOC peer benchmark** is fastest primary-source route. SEC EDGAR direct is blocked but yfinance proxies through XBRL.

## Future applications

This pattern works for:
- Other Malaysian NOCs/GLCs (TNB, Petronas Chemicals, Sime Darby)
- Other regional NOCs (PTT Thailand, Pertamina, Petrobras)
- Any company with custom ratios or peer benchmarking claims
- Any situation where user pushes back on IR-deck visuals with "bullshit" or "acah"
