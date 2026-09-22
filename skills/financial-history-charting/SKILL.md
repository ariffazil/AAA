---
name: financial-history-charting
description: "Chart a security's price history or a dead ticker."
version: 1.0.0
tags: [charting, matplotlib, equity, history, forensic, delisted, candlestick, provenance]
triggers:
  - "all time chart"
  - "all-time chart"
  - "dividend adjusted chart"
  - "chart since listing"
  - "company bankrupt chart"
  - "chart before it went bankrupt"
  - "candlestick chart"
  - "how a company dies"
  - "delisted stock chart"
  - "give me chart for X"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Financial History Charting

For charts that answer **"what did this security actually do over its life"** — an all-time line
for a listed name, a dividend-adjusted total-return series, or the death chart of a company that
no longer trades. No S/R zones, no buy/sell levels, no R:R: the deliverable is a historical
record, so **provenance discipline replaces signal discipline**.

**Not this skill:** live trading signals with entry/SL/TP levels and mobile-first zone layouts —
that is `trading-signal-chart` (user-owned; do not edit it autonomously). This skill is the
historical/forensic side: no trade recommendation is ever produced here.

---

## Procedure

### 1. Establish what data path actually works

Run the ladder before writing any chart code. Delisted tickers are the normal case here, not the
exception.

| Subject | Path |
|---|---|
| Live listing | `yfinance` — `Ticker("<sym>").history(period="max")` for all-time |
| Malaysian listing | append `.KL` (e.g. `5183.KL` = PETRONAS Chemicals) |
| **Delisted / bankrupt / suspended** | `yfinance` returns an **empty frame with a warning**, not an exception: `possibly delisted; no timezone found`. Exchange CSV endpoints answer with a JS browser challenge instead of CSV. **Do not report "no data"** — rebuild it (step 2). |

### 2. Rebuild a dead ticker from documented sources

1. **`firecrawl_scrape` with `formats:["markdown"]` on an investing.com historical-data page.**
   Returns the real OHLC + volume table and works for dead tickers.
   `https://www.investing.com/equities/<slug>-historical-data` or
   `https://ng.investing.com/equities/<slug>-historical-data`.
2. **`companiesmarketcap.com/<slug>/stock-price-history/`** — all-time-high end-of-day price and
   date, all-time low, delisting reason, last recorded trade, and an **annual % performance
   table**. Cheapest route to the peak and the overall arc.
3. **Exa / web search for the event chronology with the price at each date** — audit flag,
   suspension, resume, resignation, restatement, credit downgrade, insolvency, last trading day.
   Trade press (Reuters, The Edge, FT, CNN timelines) gives the milestone closes.
4. **Regulator filings for dates that must be exact** — an SEC Form 8-K pins a Chapter 11 filing
   date precisely. Cite it.

### 3. Build the candles

- One candle per **documented event**, plus enough filler to make the base readable. Label the
  x-axis by year; never imply daily precision.
- Body = open→close with `matplotlib.patches.Rectangle`; wick = `ax.plot([dt,dt],[low,high])`.
- Enforce a **minimum body height** (a few tenths of a percent of the y-range) so a 2-cent session
  stays visible beside a $200 one.
- Shade the death window with `axvspan` — light tint for the roll-over, darker block for the
  suspended/delisted tail.
- **Annotate the EVENTS, not the prices.** Peak, audit flag, suspension, resume, resignation,
  restatement, insolvency, last trade. On a collapse chart the annotations *are* the content;
  the candle series only supplies the slope.
- Put the summary block (peak → final, % destroyed) in the **empty margin where the series has
  already flatlined** — right-middle, `transform=ax.transAxes`, `va="center"`. Set the axis
  ceiling with headroom for the label, not just for the price.

### 4. Label the method — MANDATORY

Every reconstructed series carries a footer naming its sources and stating plainly that it is a
reconstruction built for reading **SHAPE**, not a tick feed. Never present rebuilt candles as
exchange OHLC.

Same rule for any `-adjusted` series: **name the method.** An additive cumulative-dividend line
(`close + cumsum(divs)`) is a readable approximation, **not** reinvestment-adjusted. Plot the
**raw close alongside** so the reader sees the gap between price return and total return. Never
silently adjust — "adjusted" implies reinvestment, and an unlabelled approximation is a claim you
cannot defend. For Malaysian listings the gap is often the whole story: a name can return roughly
+47% on price and +158% on total return over the same window, i.e. the dividends *are* the
investment case and the chart has to show that.

### 5. Verify the render, then deliver

Read the PNG back with `vision_analyze` **before** delivering and ask explicitly about overlap,
clipping, and axis legibility. Annotation boxes landing on the title, labels clipped at the frame
edge, and a summary box sitting on top of the data line all survive a clean `savefig` — file size
proves nothing. Fix, re-render, re-read once.

Deliver the chart first as `MEDIA:/path`, then a short interpretation. Convert a large PNG to JPG
(`PIL`, quality ~94) when the file is heavy.

---

## Writing the accompanying text

- Lead with the **chronology** — a dated table of price + event. The reader wants to see the
  machine fail step by step, not a summary.
- Use the **five-phase spine**: long base → parabola → roll-over → audit event → flatline. Keep
  the phase names identical across companies so comparison is immediate.
- Close with the **systemic lesson**, not the numbers. After any death chart the natural question
  is "what does this say about how this happens at all" — answer it in one or two sentences tied
  to something the reader can act on.
- Register for this user: BM Penang, short lines, direct. Numbers on the chart; meaning in the
  text. Never repeat a table of figures the chart already shows.

---

## Multi-company comparison

When the argument is "the same shape keeps happening", stack one panel per company on a single
figure with `add_axes((x, y, w, h))`, keeping panel proportions comparable rather than letting one
dominate, and finish with one shared verdict line. Three companies is the point at which a
pattern stops being an anecdote.

---

## Dark-theme chart conventions

```
Background:  #0d0d0d     Text:        #f5f0e8     Gold accent: #d4a843
Bull body:   #27ae60     Bear body:   #c0392b     Dim/grey:    #888888
Panel fill:  #161628 (annotation boxes, summary blocks)
Frame spines:#2a2a2a — set explicitly; the default black frame disappears on a dark canvas
```

The house also uses `#0d1117` / `#f0a500` (GitHub-dark) in other deliverables; either palette is
accepted, but do not mix them inside one figure.

---

## Pitfalls

- **tz-aware pandas index vs naive `datetime`.** `yfinance.history(period="max")` returns a
  tz-aware index on this host (`Asia/Kuala_Lumpur`). Comparing it to a bare `datetime` raises
  `Invalid comparison between dtype=datetime64[s, Asia/Kuala_Lumpur] and datetime`. Strip once
  with `h.index.tz_localize(None)`, then use `pd.Timestamp("YYYY-MM-DD")` for every comparison.
- **`datetime(y, m)` with no day argument** throws `function missing required argument 'day'`.
  Always pass the day, or use `pd.Timestamp("YYYY-MM-01")`.
- **`Rectangle` is not exported from `matplotlib.pyplot`.** Import it from `matplotlib.patches`,
  otherwise the candle bodies never become patch objects.
- **`fig.add_axes` takes a tuple, not a list.** `(0.06, 0.13, 0.88, 0.76)`, not `[0.06, ...]`.
  A list raises a type complaint and is fragile across matplotlib versions.
- **Annotations must respect the axis ceiling.** A peak label anchored to the peak price runs off
  the top unless `ylim` reserves ~40–55 pt of headroom above the peak. Same at the bottom for a
  "suspended" label on a near-zero close.
- **Never `execute_code` for matplotlib.** Use `write_file()` + `terminal()`. Run with bare
  `python3` (system matplotlib is installed); the pyrolite `legend.bbox_to_anchor` warning is
  cosmetic and expected.
- **`$` in matplotlib text is LaTeX and will crash or mangle the label.** Write `USD` / `RM`, not
  `$`, in any string passed to matplotlib. This bites every financial chart without exception.

---

## Related

- `trading-signal-chart` (user-owned) — live signals, entry/SL/TP, mobile-first zone charts.
- `scientific-pdf-generation` (user-owned) — Mode B/C/D PDF assembly; use when the chart must ship
  inside a multi-page report rather than as a standalone image.
