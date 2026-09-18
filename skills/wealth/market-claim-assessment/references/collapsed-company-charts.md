# Charting a Collapsed Company

For requests like *"bagi chart company yang dah bankrap"* — Enron, Wirecard, Serba
Dinamik. The deliverable is a chart of a dead symbol, built to be honest about how it
was built. Different job from a signal chart: here the payload is the SHAPE and the
event sequence, not a level to trade.

---

## Step 1 — Probe, then reconstruct

A delisted ticker returns an **empty frame from every quote API**, not an error:

```python
yf.Ticker("SERBADK.KL").history(period="max")   # 0 rows, "possibly delisted; no timezone found"
```

That is a not-found, not a block. Do not report the chart as unavailable, and do not
substitute a live successor or merged entity — a successor's history is a different
instrument. Reconstruct from documented prices:

| Source | Useful for |
|---|---|
| Regulator filings (e.g. SEC 8-K accession numbers) | the dated, citable event |
| Exchange / regulator coverage of the listing | suspension, resumption, delisting dates |
| Audited case studies and academic write-ups | the event sequence and magnitudes |
| Price-history archives (companiesmarketcap, publications) | reported closes at milestones |

Stooq and similar CSV endpoints are JS-gated from a server — do not spend calls there.

---

## Step 2 — Build the candles

- Anchor each candle to an **event** (peak, audit flag, suspension, resumption,
  insolvency, final trade, delisting), not to even spacing. Uneven spacing is honest:
  the events were uneven.
- body = open→close; wick = reported range. Where only a close is documented, apply a
  minimum body height so the candle stays visible.
- Green/red by up/down period. Do **not** colour by trend direction — the alternating
  colour is what makes the roll-over legible.
- For monthly-scale collapses a sparse, event-anchored series reads better than a dense
  fake daily one. Sparse but true beats dense but invented.

---

## Step 3 — MANDATORY: disclose the method on the artifact

A reconstructed chart that does not disclose its provenance **is a fabricated chart**.
Put a footer on the image itself, not only in the chat message:

> METHOD — daily OHLC is no longer paginated for delisted tickers, so candles are
> RECONSTRUCTED from reported closing prices at documented event dates and reported
> intraday ranges: <named sources>. Built for reading SHAPE, not a tick-data feed.

The PNG is what gets forwarded; the chat text scrolls away. Name the sources.

---

## Step 4 — Annotate the event sequence

The event labels are the payload. One callout per inflection, pointing at the candle it
belongs to: IPO, peak, the audit/qualification event, suspension, resumption (with the
single-day drop), last trade, delisting. Carry the headline arithmetic in one box
(`PEAK X → Y = −Z%`).

---

## The pre-collapse signature (companies only)

Same structure across bankruptcies decades and continents apart:

```
support breaks  →  rally fails at the old support, now resistance
                →  breaks again, lower high each time
                →  vertical collapse
```

**Mechanism:** buyers trapped at the old support are not selling to profit — they are
exiting at break-even. Each rally therefore meets fresh supply and fails. Four
successive lower highs in a row is the visual read.

**Read it as "who is leaving", never as "the company is bad".** Insiders know and retail
does not, so the pattern shows informed holders exiting. It is a reason to ask, never
proof of fraud — a genuine sector decline produces the same chart. Do not try to
distinguish them from the chart; exit first, because the cost of a false alarm is a
missed gain and the cost of staying is the whole position.

**The corollary that matters more:** the chart looks *healthiest* closest to death,
because when everyone believes, nobody checks. Enron at $90, Serba at RM2.42 and
Wirecard at €226 all had neutral RSI, aligned EMAs and healthy volume right up to the
audit candle. A company dies at a cliff edge, not a slope — the news arrives at once,
which is exactly why the chart cannot warn you.

---

## Stacked comparison recipe

The visual argument is the **shared silhouette**, not the levels. Two or more panels
stacked, one per collapse, each with its own accent colour and the same dark theme.
Subtitle states the thesis (*"two industries, two markets, two peaks — one identical
silhouette"*).

Layout that survives a vision check:

- Two full-width panels, generous vertical gap so annotation boxes never reach the
  panel titles.
- Shade the decline window, and darken the post-suspension region separately.
- Put the headline arithmetic in an outlined box in the **empty right-hand margin**
  (by then the series has flatlined near zero, so nothing is obscured).
- Keep leader-line offsets per-annotation and expect to iterate once — check the render
  with a vision pass for overlap and clipping before delivering.
- Footer carries the METHOD note for every panel's data.

---

## Do not

- Do not present a reconstructed series as tick data.
- Do not name the successor entity on a failed symbol's chart.
- Do not grade a company from its chart alone — it has books, and the chart cannot see
  them. Only a commodity has no hidden books for the chart to miss.
