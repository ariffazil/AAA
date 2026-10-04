---
name: weekly-sovereign-brief
description: "Produce Arif's weekly 'news I need to know' PDF brief — deep research on current events, verdict-first human language, 10-chart pack, WeasyPrint PDF. Load on 'what's happening this week', 'news I need to know', 'weekly brief', Friday current-events deep-dive requests."
---

# Weekly Sovereign Brief (Arif's Friday News PDF)

Class: recurring current-events intelligence deliverable — research the week's news across Arif's watch domains, synthesize verdict-first in human language, deliver as a polished PDF with chart pack. Proven 2026-08-07 (Week 32, 16 pages / 947KB / 10 charts).

## When to use
- "What news is happening that I need to know?" / "news this week" / "weekly brief" / Friday deep-research requests
- Daily/weekly pulse deliverables (World Model pulse/intel/reckoning cron lineage)
- NOT for single-entity deep dives (Gentari, PETRONAS collapse) → use `deep-research-plus-wealth` instead

## Arif's watch domains (the 8 that matter — all get at least one search)
1. **Gold XAUUSD** (he trades ~0.3 lots, W1+M15) — spot, Fed path, geopolitical premium
2. **USD/MYR ringgit** — 5-year high watch, BNM stance, what it does to his USD-denominated gold trade
3. **Petronas + fuel subsidy paradox** — dividend vs subsidy bill vs Brent, always coupled (see pdf-report-generation subsidy-paradox refs)
4. **Strait of Hormuz / Iran** — the load-bearing geopolitical variable for Malaysian fiscal
5. **US jobs / Fed (NFP)** — the single macro print, framed as Friday's decision event
6. **Bursa KLCI** + banks
7. **Crypto (BTC/ETH)** — one line only; trailing indicator
8. **AI week** — frontier-model security + releases (Arif builds on these models)

## Source map (search targets that deliver)
| Domain | Search/extract target |
|---|---|
| Gold | `tradingeconomics.com/commodity/gold` (spot + end-of-quarter forecasts) |
| Oil | Reuters energy, Vantage Brent/WTI technicals |
| FX | `federalreserve.gov/releases/h10` (official fixes), TradingEconomics MYR |
| Petronas | Reuters, MoF press, thestar.com.my BUDI95 stats |
| Hormuz | Wikipedia "2026 Strait of Hormuz crisis" (timeline), AP/Al Jazeera, Britannica |
| NFP | forexfactory.com calendar (forecast), CNBC preview, tradingeconomics NFP |
| KLCI | bursamalaysia.com market data, investing.com historical |
| Crypto | cryptal.com weekly recap, coindesk, BitPinas daily |
| AI | TechCrunch, WSJ/NYPost, GWU media tip sheets |

Search pattern: ~12 searches in 3–4 parallel batches, one query per domain with date anchors ("August 2026"). Extract 1–2 pages for spot anchors. Budget ≈ 5 min research, then synthesize.

## Content architecture (16 pages proven)
1. **Cover** — dark navy gradient + gold, 3×2 KPI grid (XAUUSD / USD-MYR / Brent / KLCI / BTC / Petronas-div). Set explicit `color:#fff` on `.cover h1` (contrast trap), vision-verify.
2. **Verdict page** — lead paragraph (the 5 moves), KPI hero row, verdict box (OBS/DER/INT/UNKNOWN/BINDING/FALSIFY), five-moves table (what happened / why it matters / source tag), "what you do Monday" per relevant position.
3. **Chart pages** (10 charts, urgency order): subsidy paradox first (biggest live risk), then gold, ringgit, NFP, KLCI, asset-returns YTD, Hormuz scenarios, AI week, Petronas dividend trajectory, week calendar.
4. **Deep dives** (2–3): the binary event (Hormuz — deal vs collapse scenario tables), the fiscal trap (subsidy paradox math table), the macro print (NFP scenario table w/ probabilities + USD/Gold/Sep-cut columns), AI security.
5. **Omega box** — one uncomfortable question, red gradient box, human-language (no frameworks by name).
6. **Appendix** — indicator table w/ epistemic tag column, source table w/ confidence, glossary (XAUUSD, BUDI95, NFP, Hormuz…).

## The 10-chart pack (one build_charts.py, batch all ~30s)
1. Gold weekly line (spot + forward-forecast dashed line + floor)
2. Subsidy paradox: Brent → dividend vs subsidy bill vs net fill (RED where net<0) — Arif doctrine chart, always first
3. Ringgit monthly bars (color-coded by strength, record-low reference line)
4. US jobs: NFP bars + unemployment twin axis
5. KLCI week line
6. Asset-returns YTD barh (Gold/Brent/KLCI/USDMYR/BTC/S&P)
7. Scenario probability ladder (Hormuz outcomes, INT-tagged)
8. AI-week impact barh (score 1–10, RED for security story)
9. Petronas dividend trajectory bars (2018→2026e, red for 9-year low)
10. **Calendar-as-chart technique**: `ax.axis("off")` + `plt.Rectangle((0.02, y-row_h*0.45), 0.04, row_h*0.4, color=..., transform=ax.transAxes)` color chips + 3 text columns (when / what / why) — renders in WeasyPrint as a single image, no HTML table needed. Proven: 10 events × 3 columns clean.

Shared rcParams block + palette constants (NAVY `#0e1a2b` / GOLD `#c9a227` / RED / GREEN / BLUE / ORANGE), dpi 160, one script.

## Pipeline
Research → charts (one batch script) → ONE self-contained HTML (relative `charts/0N_*.png`) → WeasyPrint render → verify → deliver. Full pitfalls (JS-blank, cover traps, python path, pdfimages 2N check) live in `pdf-report-generation` — READ that skill too; this one adds the brief-specific shape only.

## Verification checklist (~1 min)
1. `pdfinfo` — expect 15–17 pages
2. `pdftotext -f 2 -l 2` — verdict page text present
3. `pdfimages -list` — N charts = 2N image objects
4. `pdftoppm -r 110` cover + `vision_analyze` (contrast, KPI legibility)
5. Deliver `MEDIA:/abs/path.pdf` + Telegram summary: verdict table, Friday watchlist, Omega line

## Pitfalls
- **NFP timing**: US jobs land Fri 20:30 MYT — frame Friday's print as the pending decision event, never as done.
- **Forecast anchors**: cite TradingEconomics end-of-quarter forecasts next to spot ("forward forecast $4,420") — gives the "what next" number.
- **Epistemic tags live in tables only** (OBS/DER/INT/UNK), never in prose (Arif doctrine).
- **Subsidy paradox is mandatory** for any Malaysia/Petronas section — high oil ≠ bull case, crossover ~$78 Brent.
- **"Deal imminent" is a claim, not a fact** — tag INT, present both paths with probability bands.
- **Never fabricate paywalled detail** — triangulate secondary sources.
- One chart script per run; never one script per chart (state-drift + 6× slower).
- **"So what?" rule — every brief must end with a human-language sentence of consequence, not a data dump.** Arif's recurring operator-mode correction (2026-08-07): after any deliverable, he asks "So what?" — the answer is the single human-language sentence that says what changes for him personally if the data holds. It is not a summary. It is not an interpretation. It is the one sentence that makes him act or not act. The brief's Omega box serves this function; if the Omega box only asks a question without a consequence sentence, it fails the "So what?" gate.
- **Falsification title/legend collision in charts** — when encoding the falsifier test into a chart title (`Falsify: $60 breach by Sep 1 = ...`), the long title pushes into the legend area and overlaps. Fix: keep the main title under 120 chars, put the falsifier in the `chart-caption` HTML paragraph below the chart image (not in the matplotlib title). Chart titles should be: `C-01 [OBS] · Brent Path — 3-Scenario Fan`. The falsifier goes in the caption text.
- **Verify event vintage before listing it as "this week" (learned 2026-08-15).** Two classes of age drift in one week-brief: (a) a stated "July 2024" acquisition was actually a 28 May 2024 SPA — cite the instrument date, not the completion month; (b) a "this week" item (US LNG $3.4B/yr toll) was an Aug **2025** parliamentary answer — a year old, resurfacing because the obligation is still live. Open the source body and confirm its own dateline (month AND year) before anchoring it to the week. An old-but-live obligation is signal (running cost, not new event) — report the vintage explicitly; silently re-dating it is fabrication.
- **Falsifiable-in-24h items get flagged as such.** When a brief asserts an unbroken claim ("DAP votes Sunday on leaving the unity government"), it is not fact until the vote lands — label it as pending with the resolution date. The follow-up conversation revealed the claim was asserted as settled when the event hadn't happened yet. Anything resolvable inside the brief's own shelf life gets a falsifier date, not a past-tense verb.
- **Ad-hoc Telegram week-briefs (no PDF) inherit the same rules** — the PDF pipeline is one shape of this class; a chat "what's high-signal this week" run is another. Same disciplines apply: cross-check ≥2 sources per critical number, flag single-source rows, vintage-check anchors, cross-check any figure the human's own follow-up asserts before metabolizing it (their claim of e.g. "DAP decided to stay" / "Nurul Izzah resigned" must be re-verified, not adopted — in the 2026-08-15 session both needed correction: vote still pending; resignation was rejected, temporary leave granted instead).

## References
- `references/2026-08-07-week32-numbers-bank.md` — Week 32 data, sources, and the calendar-as-chart snippet (proven run).
