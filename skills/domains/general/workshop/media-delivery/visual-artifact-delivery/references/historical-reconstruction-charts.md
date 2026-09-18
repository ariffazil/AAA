# Charts for delisted tickers and long-history series

The two asks that break the normal chart pipeline: *"show me the chart of a company that died"* and
*"give me the all-time chart, dividend-adjusted."* In both, the obvious data source returns nothing,
and the work is reconstruction rather than plotting.

## 1. When the feeds come back empty

Price APIs serve live and recently-traded symbols. For a delisted or wound-up issuer they return an
empty frame, not an error — so a naive script plots an empty axis and exits 0. Observed on a mixed
batch of delisted symbols (exchange-suspended, insolvency-filed, wound-up): every one returned
**0 rows**, with only a `possibly delisted; no timezone found` notice on stderr. Free CSV endpoints
gate behind a JS challenge and return an HTML challenge page — which, written to a `.csv`, is the
classic silent failure the verify loop already warns about.

So: **probe the shape before you build.** If the frame is empty, switch to reconstruction
immediately rather than tuning the fetch.

## 2. Reconstructing the candles

1. **Collect documented closes at event dates**, not a daily series. The sources that survive are the
   ones that were published when it mattered: news-archive chronologies of the collapse, the
   company's own regulatory filings, the aggregator page that still shows the historical table for
   the ticker, and academic or professional case studies. Each gives you a *date* and a *price*.
2. **Build monthly (or quarterly) candles**, not daily. Body = open→close between consecutive
   anchor points; wick = the reported intraday range where the source gives one, otherwise
   modelled. Fewer, well-sourced candles beat a dense invented series.
3. **Plot the closed period explicitly.** A shaded band over the suspended/halted stretch and again
   over the post-insolvency stretch makes the flatline legible instead of looking like missing data.
4. **Footprint the peaks and the audit beat.** The two candles that carry the story are the blow-off
   top and the first audit candle. Label them; leave the rest sparse.
5. **Carry a METHOD footer on the artifact.** Name the sources and state in one sentence that the
   candles are reconstructed from documented closing prices because the OHLC history is no longer
   served. Never present a reconstruction as a feed.

## 3. The shape vocabulary (what these charts actually show)

Across independent collapses in different countries and decades the same five phases recur, which is
what makes the chart worth drawing at all:

| Phase | What it looks like |
|---|---|
| Base | Long, low-volatility grind. Nothing in it looks wrong. |
| Parabola | Near-vertical advance; the name enters an index or a "best of" list. |
| Roll-over | Red, green, red, green. Confusing by design — the period where most holders stay. |
| Audit candle | One outsized red body. Not the cause; the moment everyone else finds out. |
| Graveyard | Flat at cents, then a long shaded halt to the delisting. |

**The load-bearing claim, and its limit.** The lower-high / lower-low staircase does carry
information: each failed retest of a broken level is supply from people who are leaving, and a
company that repeats the pattern tends to break again because the underlying cause was never
resolved — only deferred. But the chart cannot distinguish fraud from ordinary sector decline, and
it announces nothing before the audit candle. **Do not resolve that ambiguity with more chart** — a
lower timeframe or an extra overlay re-reads the same belief at finer resolution. The off-chart
question is the one that decides: *can they produce the statements, and who audits them — and who
pays that auditor?* An auditor paid by the entity it audits is the mechanism that makes a
signature worthless, which is a governance fact, not a technical one.

## 4. Domain scope — where technicals do and do not carry the weight

State this when the request straddles both, because the two cases look identical and are not:

- **A commodity has no balance sheet.** No counterparty, no financial statements, no issuer that can
  be misrepresented. Price is the only information that exists, so a technical read there is not
  reading a shadow — there is nothing hidden underneath. Adding indicators adds no information;
  it only trades less. The levers that matter are position size, stop discipline, and knowing where
  other participants' stops sit.
- **A single-company equity is different in kind.** The chart records what participants believe, and
  belief can be manufactured — for years. The statements, the auditor's independence and the
  insider flow are where solvency lives, and none of them is on the chart.

When the same tool is appropriate in one domain and blind in the other, say which domain the answer
belongs to *before* recommending it. Presenting a chart-derived judgement as authoritative in the
blind domain is the failure; so is answering "the chart can't show that" with a richer chart.

## 5. Long-history view on a live issuer — dividend-adjusted

The usual request is a listed company across its whole life, with income included. Two series on one
axis, plus the distributions and volume beneath:

```python
import yfinance as yf, numpy as np, pandas as pd

h = yf.Ticker("5183.KL").history(period="max")
divs = yf.Ticker("5183.KL").dividends

dates = h.index.tz_localize(None)          # strip zone ONCE, up front
raw = h["Close"].values.astype(float)

# cumulative additive adjustment: total return = price + all dividends paid while held
cum = np.zeros(len(dates))
for dt, amt in divs.items():
    cum[dates >= pd.Timestamp(dt).tz_localize(None)] += float(amt)
adj = raw + cum                            # plot `adj` as the total-return line
```

- **Plot BOTH lines.** The raw close and the dividend-adjusted total return diverge sharply over a
  decade; a single line hides the whole point, because the difference *is* the dividend
  contribution.
- **A dividend bar strip under the price axis** shows when the distributions stopped growing, which
  is usually the real story.
- **Report the annualised figure, not the cumulative.** Raw change and adjusted change on a 15-year
  series describe different instruments. Give both, plus the annualised rate, so a "+" can be read
  against inflation rather than admired.
- **Say what the instrument is when the numbers say so.** A long series whose raw return is small
  and whose total return is carried by distributions is an income holding, not a growth one; deliver
  it with that sentence rather than leaving the reader to infer it from the curve.

## 6. Render checks specific to these charts

- **Annotation crowding is the failure mode.** Event labels cluster exactly where the series is
  densest (the collapse). Give each label an explicit pixel offset from its point, then run the
  collision QC pass from the parent skill — title overlap and edge clipping are both common here and
  neither raises an error.
- **A summary panel on the right must sit where the series has already flatlined.** On a collapse
  chart that is near zero, so a high-right placement is clean; on a parabola chart it lands on the
  candles.
- **Keep the shaded closed-period band behind the candles** (`zorder` below the bodies) or the price
  action disappears inside it.
- **Filter the matplotlib stylesheet warning** (`Bad key legend.bbox_to_anchor ...` from a user-level
  `matplotlibrc`) when reading script output, so a real traceback is not lost in the noise.

## 7. The fundamentals lane — when the chart is the wrong instrument

Section 4 above says solvency lives in the statements, not on the chart. Here is the lane that
carries them, and the trap inside it.

**Price history for delisted issuers is generally gone; filed statements are not.** A company that
filed for bankruptcy has accounts on record, and those records are still served. This is the only
lane that lets a solvency test be validated against companies that actually died — the difference
between a calibrated instrument and a plausible one. Do not burn the budget re-probing price feeds
for a wound-up ticker: probe once, then switch lanes. The probe result is itself worth recording,
because "the feed returns an empty frame rather than an error" is what tempts a script into plotting
an empty axis and exiting 0.

**The trap: regulatory identifiers are REUSED after a filer dies.** A dead company's identifier keeps
serving data for whoever holds it now, and the numbers can look entirely plausible for the wrong
entity — right shape, right magnitude, wrong company. Observed reuse: a home-goods retailer's
identifier now serves an unrelated data company; a luxury department store's now serves an Asian
data firm; a snack-food baker's now serves a biotech. So **read the entity name from the same
response and reject any identifier that does not match the expected filer** — a substring match on
one distinctive word from the original name, never equality, because a post-bankruptcy entity files
under a successor name that may bear no relation to the brand. In one acquisition pass roughly half
the candidate identifiers were rejected on this test. That rejection rate is normal, not a sign the
lane is broken.

Two consequences for artifacts built from this lane:

- **A reconstructed series and a reconstructed balance sheet are the same class of artifact.** Both
  need the METHOD footer naming sources and stating the figures are a reconstruction rather than a
  feed. An unchecked identifier is the balance-sheet form of the unstamped diagram: a plausible
  surface acquiring authority nothing granted it.
- **A model validated only on live issuers is validated on the easy population.** Where the dead ones
  are absent, say which way the bias pushes. And an "infinite runway" reading on a company whose
  identifier was never verified is more likely a wrong entity than a finding.

Full recipe — endpoint, tag alternatives, annual-figure filter, failure modes, and the entity-check
test: `company-solvency-forensics` → `references/edgar-xbrl-lane.md`.

## 8. Rendering a two-detector result

When a solvency artifact carries both a distance-to-barrier figure and a cash figure, they must be
plotted as **separate panels with the shared time axis**, never combined into one score — the whole
finding is that the two can disagree, and a blended index destroys exactly the disagreement that is
the point. Label the panel that fired and the panel that went blind; a reader who sees only the
composite will take the optimistic half.
