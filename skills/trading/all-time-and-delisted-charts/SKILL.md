---
name: all-time-and-delisted-charts
description: "Use when asked for an all-time or delisted-company chart."
version: 1.0.0
tags: [charting, matplotlib, yfinance, all-time, delisted, bankruptcy, dividend-adjusted]
triggers:
  - "all-time chart"
  - "since inception"
  - "dividend adjusted"
  - "chart of a company that went bankrupt"
  - "show the chart before it died"
  - "chart before bankruptcy"
  - candlestick history request for a dead ticker
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# All-Time and Delisted-Company Charts

Two data situations under one class of request: a live ticker whose full history should be
plotted, and a dead one whose history is no longer served by any feed. The second requires
reconstruction, and the reconstruction must be declared on the artifact.

## Procedure

1. **Decide the situation.** Live ticker → `yfinance.Ticker(<code>).history(period="max")`
   works and returns everything from listing. Do not hand-collect annual closes.
2. **Strip the timezone once, at the top.** The yfinance index is tz-aware
   (`datetime64[s, Asia/Kuala_Lumpur]`), so a comparison against a naive `datetime` raises
   `TypeError: Invalid comparison between dtype=datetime64[s, Asia/Kuala_Lumpur] and
   datetime`, and slicing by that mask can yield an empty array that then blows up inside
   `max()`/`min()` with a misleading "missing argument `day`" error.

   ```python
   dates = h.index.tz_localize(None)
   ```

3. **Dividend-adjusted total return, computed forward.** Add cumulative dividends onto the
   close; do not scale each row by its own dividend.

   ```python
   cum = np.zeros(len(dates))
   for dt_val, amount in divs.items():
       cum[dates >= pd.Timestamp(dt_val).tz_localize(None)] += float(amount)
   prices_adj = raw_close + cum
   ```

   Plot BOTH lines — adjusted in the accent colour, raw grey at ~0.5 alpha — because the gap
   between them is the dividend story. Report raw return, total return, dividends summed, and
   annualised return in the header strip. A company whose raw return trails inflation while
   total return looks healthy is a **yield stock, not a growth stock**; say that in the text.
4. **If the ticker is delisted, stop fighting the feed and reconstruct.** See below.
5. **Annotate milestones, not just the line.** IPO, peak, the audit flag / first fatal
   disclosure, suspension, final trade, delisting — each with its value. Add a peak→trough %
   callout in a bordered box, and shade the "death zone" from the first fatal disclosure
   rightward with a darker band for the post-suspension flatline.
6. **Verify the render with a vision read before sending**, then convert to JPG and deliver.

## Reconstructing a delisted ticker

`yfinance` returns **0 rows** for delisted tickers and prints `possibly delisted; no timezone
found` / `no price data found`. CSV mirrors are JS-gated and return a challenge page. The data
is genuinely not served — do not burn turns on it.

Build candles at documented event dates from reported closes:

```python
# (date, open, high, low, close, label, label_offset_in_points)
rows = [ (datetime(2020, 1, 15), 2.25, 2.50, 2.20, 2.42, "PEAK", (0, 55)), ... ]
```

- Body = documented open→close. Wick = reported intraday range where the source gives one;
  model it when it does not.
- Monthly or event-frequency is correct. Daily is unavailable, and fabricating it is an F2
  failure.
- **Search the event, not the ticker.** Reported closes at the milestones; the peak and
  trough; the last traded price; the suspension and delisting dates. Sources that work: wire
  copy from the day, exchange and business-press archives, investor-forum historical price
  tables, market-cap history sites (they publish highest/lowest close plus annual
  performance), and regulator filings — a bankruptcy or delisting filing gives the date
  exactly. Cross-check the peak against two independent sources before annotating it.

**Print a METHOD note on the chart itself.** Small, italic, grey, in the footer:

> METHOD — daily OHLC is no longer paginated for delisted tickers, so candles are
> RECONSTRUCTED from reported closing prices at documented event dates and reported intraday
> ranges: <sources>. Built for reading SHAPE, not a tick feed.

This is required, not polite: a reconstructed candle series that LOOKS like market data must
say what it is. Repeat a one-line version of the caveat in the chat delivery message.

## Make the comparison the point

A single dead company reads as an anecdote. Two stacked in one figure, with a two-line header
naming the shared shape, reads as a pattern — and that is the deliverable when the ask is
"show me what a collapse looks like". The silhouette is the payload: a long flat base, a
vertical peak, a cliff, then a flatline at cents. The chart is at its most attractive
immediately before the fatal disclosure; that observation is usually the insight the requester
is actually reaching for.

## Render and verify

- `write_file()` the script, then run it with bare `python3` (matplotlib is system-wide).
- `add_axes` accepts a list of four floats, and `axvspan` / `set_xlim` accept datetimes — the
  Pyright "no overloads match" complaints on these are lint noise, not runtime errors.
- The `pyrolite` style emits a non-fatal `legend.bbox_to_anchor` warning. Ignore it.
- **Convert PNG → JPG before delivery**: `Image.open(png).convert("RGB").save(jpg, quality=94)`.
- **Vision-verify the render before sending.** Ask specifically about overlap and clipping:
  *"does any annotation box overlap the chart titles? is any label clipped at an edge? is the
  footer legible and clear of the bottom chart?"* This catches the defects these figures
  actually have — a peak label colliding with the panel title, two annotations stacked on each
  other in a corner, a tag pushed below the plot floor into the tick labels. Fix by moving the
  annotation's `xytext` offset; do not re-lay-out the whole figure.
- Spread labels by offset sign, not by hope: high annotations go up, low ones go down, and
  milestones near each other get opposing offsets. Two figures in a row needed an offset fix
  after the vision pass.

## Pitfalls

- **Do not present a reconstructed series as market data.** The METHOD footer and the chat
  caveat are the difference between a shape illustration and a fabrication.
- **Do not plot a delisted ticker and report it as empty/failed.** Zero rows is the expected
  signature, not an error to debug.
- **Do not skip the tz strip.** The failure looks like a broken data fetch and is actually a
  dtype comparison.
- **Do not compute the adjusted series by scaling each row.** It produces a curve that is
  wrong in a way that still looks plausible.
