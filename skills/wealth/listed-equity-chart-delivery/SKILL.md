---
name: listed-equity-chart-delivery
description: "Use when asked for a listed stock's chart."
version: 1.0.0
author: Hermes
license: arifOS
tags: [trading, chart, equity, bursa, tradingview, dilution, delivery]
metadata:
  hermes:
    category: wealth
    tags: [trading, chart, equity, delivery]
    related: [trading-signal-chart, market-analysis-scope]
triggers:
  - asked for a chart of a listed company (Bursa, NYSE, any exchange)
  - asked to show a stock's history, peak, fall, or "since <event>"
  - asked about a delisted or renamed ticker
  - asked to evaluate a company from its price chart
---

# Listed Equity Chart Delivery

Producing a stock chart for a human. **This is not the gold/FX lane.** Gold and FX have a live signal
API and a dedicated render path (`trading-signal-chart`); a company does not. Keep the domain rule
they already know: for a commodity the chart IS the signal, for a company the chart is other people's
belief and the books decide. This skill governs the *artifact*; it does not decide the thesis.

## Rule 1 — Source the platform render. Do not hand-draw. (Arif, verbatim)

> *"kalau chart stock, hg screenshot trading view ja. Senang. Hang plot buruk."*

The correction is not about aesthetics. A platform render already carries the author's own annotations,
the indicator set, the volume panel, the adjusted-price basis, and a timestamp — and it is checkable
against the page the requester is looking at. A hand-drawn matplotlib candlestick carries none of that
and **silently re-derives** the prices from whatever feed you had, so a corporate action or a data gap
becomes *your* error instead of a property of the chart.

- Reach for the platform render FIRST, even when you have a price API that would work.
- Hand-draw only when no platform page exists (delisted, private, never-listed) — and then see Rule 5.
- Do not overlay your own lines on a sourced render. Deliver it as-is, or draw your own artifact.

## Rule 2 — Pull the chart from the link he shares (recipe)

A TradingView share link (`https://www.tradingview.com/x/<id>`) serves a full-resolution static PNG
behind its own meta tags. No scraping, no auth:

1. Open the link in the browser lane. `meta[property="og:image"]` points at
   `https://s3.tradingview.com/snapshots/<first char of the id>/<id>.png`
2. `curl -sL -o chart.png '<that url>'` — a dark-theme render with symbol, timeframe, indicator
   legends, the author's watermark and a creation timestamp.
3. `meta[property="og:title"]` / the page title carries symbol + exchange (`MYX_DLY:VANTNRG`, or
   `MYX_DLY:PCHEM`). **Read it before you say anything about the ticker** — it is how you confirm you
   are looking at the company he means.
4. Deliver as `MEDIA:/abs/chart.png`. Verify the file exists and is non-zero before claiming delivery.

**Crops beat zoom for reading it.** The snapshot is a tall portrait image; split it into vertical
strips (or crop the header band) before OCR/vision, or the ticker line and the axis labels are lost.

**Free-platform limits are real and worth answering.** A free TradingView plan cannot select a yearly
interval — pressing `12M` falls back to daily, and the gate is on the *interval*, not on the symbol.
The working answer is **monthly + pinch-zoom out**; say that instead of sending him to buy a plan. For
a full corporate life, monthly gives 12 bars a year and still shows the arc.

## Rule 3 — Adjusted history: a corporate action rewrites the OLD prices

TradingView plots adjusted prices. A consolidation therefore makes ancient bars look enormous:

- Vantris/Sapura shows a peak near **RM99** because of a **20-to-1 share consolidation** (Aug 2025) —
  RM4.96 × 20 = RM99.20. **Both numbers are correct**; only one is on the chart.
- When a chart's price scale contradicts your recorded share price by a clean ratio, look for a
  consolidation, subdivision, or capital reduction **before** concluding either figure is wrong.
- Always say which basis you are quoting (as-traded then, or consolidation-adjusted now). Two correct
  numbers presented as a contradiction is a self-inflicted credibility loss.

## Rule 4 — Market cap and per-share fall by different amounts. The gap IS the dilution.

Sapura worked example: market cap RM28.5b → ~RM0.7b is **−97%**; the share price RM4.96 → RM0.34 is
**−99.7%**. The 2.7-point gap is *shares issued* — rights issue, RCUIDS, debt-to-equity handed to the
lenders — not worse operating performance.

- State both numbers, then **name the difference** as dilution. The gap is the finding; a −97% chart
  alone hides it completely.
- A company can survive while its holders are wiped out. "The company died" and "the equity died" are
  different claims and usually only the second is true. Say which one happened.

## Rule 5 — A delisted ticker has no price history on the free lanes

Probed and confirmed: `yfinance` returns **EMPTY** for a dead ticker *and* for its post-rename
successor, and stooq is blocked. Do not burn turns re-trying lanes.

- Plot **documented points only** — merger value, a dated high, a rights-issue price, today's quote —
  and leave the gaps visually open.
- **Never interpolate a price line or a balance sheet to make the shape continuous.** A smooth line over
  missing years is fabrication with a nice gradient; an openly broken line is the honest artifact and
  reads as more credible, not less.
- Label what each point is and where it came from, in the figure itself.

## Pitfalls

| Pitfall | Fix |
|---|---|
| Hand-drawing a listed stock's chart | Source the platform render (Rule 1). Rejected on sight otherwise |
| Recording a peak that contradicts the chart by a clean ratio | Think corporate action first (Rule 3), not data error |
| Quoting a market-cap fall and a share-price fall interchangeably | They differ; the gap is dilution (Rule 4) |
| Chasing delisted price history across data providers | Points + open gaps (Rule 5); the lanes are empty by design |
| Re-overlaying your own levels on a sourced render | Deliver as-is, or draw a separate artifact |
| Claiming delivery without checking the file | `ls -lh` the path; `MEDIA:` is not a receipt |

DITEMPA BUKAN DIBERI.
