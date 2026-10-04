# Weekly Sovereign Brief — Pattern & State Bank

Trigger phrases from Arif: "news this week I need to know", "what's happening", "weekly brief", "week in review". Deliverable: 13-page PDF, human language (frameworks invisible), epistemic tags in table cells/captions only, KPI hero row under cover. Render via `pdf-report-generation` skill (WeasyPrint, `/usr/bin/python3.13`).

## Search recipe (proven 2026-08-07 — ~20 searches in 4 parallel rounds)

| Round | Queries (parallel) | Why |
|---|---|---|
| 1 | Malaysia economy, AI breakthroughs, Petronas, global markets weekly, oil Brent/WTI, gold XAUUSD | Core six domains |
| 2 | Fed/Powell, US–Iran conflict, crypto/BTC, ringgit USD/MYR, RON95 subsidy, China trade | Macro + Malaysia-specific |
| 3 | Hormuz shipping, DeepMind/AI leadership, S&P 500 record, NFP jobs data | Week's live stories |
| 4 | Tariff news for the exact date, KLSE/KLCI | Malaysia market + policy |

Always append "August 2026" / "this week" / the exact date to queries — recency filters the noise. Reliable Malaysia sources: BNM (bnm.gov.my), paultan.org (weekly fuel prices), Bursa Malaysia daily commentary, TradingEconomics (KLCI/ringgit/gold quotes).

## Chart pack (6 charts, ONE matplotlib batch script — shared rcParams + palette)

1. **Week moves bar** — gold, WTI, BTC, KLCI, USD/MYR w/w % (green/red by sign).
2. **Gold 6-week OHLC range** — weekly candles over a range box, key levels as dotted lines ($4,100 resistance / $3,900 invalidation), catalyst annotation (NFP/CPI).
3. **Twin-axis physical-vs-price** — tanker throughput (bar, vessels/day) vs oil price (line) on same timeline. This is the week's single most valuable chart.
4. **Subsidy paradox** — Brent (x) → petroleum revenue + subsidy bill + net-to-budget (y), red fill where net < 0, crossover marker. Mandatory for any Malaysia/oil brief (see SKILL.md subsidy-paradox section).
5. **Fed regime timeline** — rate path (range bars) with chair-transition annotations (Powell → Warsh, dissenters).
6. **KLCI sector tape** — horizontal bars (finance/energy/consumer/plantation w/w).

Every chart: source line + [OBS]/[DER] tag in the caption. Verify: `pdfimages -list` = 2N image objects for N charts; vision-check the cover.

## Physical-vs-price verification rule (Kpler lesson, 2026-08-05)

Headline-driven price moves MUST be checked against physical evidence before they go into a brief as fact:
- WTI collapsed to $75.64 on "draft deal to reopen Hormuz" headlines; Kpler vessel-tracking showed **5 tanker transits vs 20+ pre-war baseline** the same morning.
- The price was hope; the strait was still functionally blocked. The deal had not been signed.
- Rule: quote the physical number next to the price ("5 tankers vs 20 baseline" beats "oil fell 2%"). It is the most valuable single line in the brief and the F2-compliant anchor for the verdict. Same pattern: check port throughput, inventory draws, cargo manifests, or border-crossing data against any geopolitics-driven price move.

## State-of-world anchor bank (as of 2026-08-07 — RE-PROBE before reuse)

- **US–Iran war**: started Feb 28, 2026. Hormuz ~75% throughput collapse (5/day vs 20+ baseline; pre-war total ~138 vessels/day). Iran talks via Oman/Qatar, not US; Trump cancel-strike-then-claim-deal pattern; Houthi tanker attacks; Israel strikes southern Lebanon.
- **Gold**: ATH $5,608 (Jan 2026), ~$4,090 (Aug 4), 6-week range $3,960–4,130; JPM Q4 target $4,500; invalidation $3,900.
- **Oil**: WTI peak ~$122 (Jul) → $75.64 (Aug 5). Brent crossovers: subsidy paradox inversion ~$100–110/bbl.
- **Fed**: Powell final meeting Jul 29 (hold 3.50–3.75%, 3 dissenters wanted HIKE); Kevin Warsh incoming chair (Senate hurdle cleared, ~Sep); SEP median 1 cut in 2026, market odds ~zero; cuts expected 2027.
- **BNM / MYR**: OPR 2.75%; USD/MYR ~4.09; reserves $132.1B (Jul 31).
- **Malaysia subsidies**: RON95 BUDI95 RM1.99/L capped; unsubsidised RON95 RM3.77; RON97 RM4.35; diesel Peninsular RM4.57; bill ~RM4B/month vs RM700M pre-war.
- **Petronas**: Malaysia Bid Round 2026 (9 blocks, Feb 10); rightsizing rounds Mar/Aug 2026; Suriname Block 52 (8 successful wells); TriCipta AI 3rd JDA with IBM + Tridiagonal.AI (Jun 30); LNG deals JERA/Hokuriku/Shizuoka.
- **AI**: Hassabis → DeepMind chairman + Alphabet chief scientist (Aug 5), Kavukcuoglu day-to-day; Jeff Dean → Discovery Loop startup; Gemini 4 unreleased; Meta AI model "hacked" in test; AI-designed viruses published; Morgan Stanley: 10x compute ≈ 2x intelligence, recursive self-improvement possible H1 2027.
- **US equities**: S&P 500 record 7,709 (Aug 4), +13% YTD; 86% EPS beat rate (5-yr high); SOX still -17% from Jun peak (AI trade resetting); Palantir +26% on guidance.
- **NFP cadence 2026**: Jun print 57K (Jul 2, miss), Jul print +85K (Aug 7, beat 57K f'cast).
- **China**: Jul exports +23.9% y/y, imports +27.5%, surplus $112.5B; Q2 GDP 4.3% (from 5.0% Q1); AI hardware/chips driving trade.
- **KLCI**: ~1,737 (Aug 6), +11.5% y/y; financials leading (Maybank RM10.84, CIMB RM8.01); 2014 ATH 1,896.

## Delivery shape

KPI hero row (5 cells: gold, oil, USD/MYR, NFP, S&P) → lead verdict paragraph → per-domain chapters with charts inline → next-week event table (date / event / why it matters / Arif impact) → binding-constraint box → Omega question → falsification line. ~13 pages, tables in appendix only (Arif's standing preference).
