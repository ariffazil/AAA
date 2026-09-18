# Postmortem candle render — data harvest, recipe, layout

## 1. Data — the feed is gone, rebuild from documents

`yfinance.history(period="max")` returns **zero rows** for a delisted symbol and logs
`possibly delisted; no timezone found`. The series is absent from the vendor, not merely delayed —
do not retry or tune the call. Also dead from a datacenter host: `stooq.com/q/d/l/?s=…` CSV
(Cloudflare interstitial on every symbol).

**Working path:**

1. Search per company for the two anchors plus the intermediate events:
   `<company> stock price history <peak month year> collapse <ticker>` and
   `<company> closed <price> <date> bankruptcy`.
2. Harvest closes at *event dates* only — not every day. Filings and press archives hold the sticky
   numbers: the wire service for the final tradable print, the regulator filing for the bankruptcy
   date, investor boards or investing.com historical tables for earlier closes, and
   `companiesmarketcap.com/<company>/stock-price-history/` for peak/trough plus annual performance
   percentages.
3. Build one candle per documented event: open/close from the reported pair, high/low from the
   reported intraday range where available, else ±1–2% modelled.
4. **State the method on the artifact.** A footer line naming the sources and reading
   "reconstructed for reading SHAPE, not a tick feed" is mandatory — reconstructed candles
   presented as exchange OHLC is a fabrication.

Deprecated-equity price tables for the 1997–2002 era (ticker suffixed `Q` for OTC) are still found
in archived regulatory filings and academic exhibits; they carry real daily OHLC and are worth
searching before falling back to event-date reconstruction.

## 2. matplotlib recipe

Write the generator to a file and run it with bare `python3` via the terminal tool — not through a
sandboxed code runner (matplotlib is not available there).

```python
from matplotlib.patches import Rectangle   # NOT plt.Rectangle — it is not exported
import matplotlib.dates as mdates

for dt, o, h, l, c in rows:
    col = GREEN if c >= o else RED
    ax.plot([dt, dt], [l, h], color=col, linewidth=1.0, solid_capstyle="round", zorder=3)
    bottom = min(o, c)
    height = max(abs(c - o), 0.012 * price_range)   # minimum visible body height
    ax.add_patch(Rectangle((mdates.date2num(dt) - width_days / 2, bottom),
                           width_days, height,
                           facecolor=col, edgecolor=col, linewidth=0.6, zorder=4))
```

- `width_days`: ~16 for monthly candles, ~46 for quarterly, ~120 for multi-year spacing.
- Height floor matters: a near-zero close with no floor renders as an invisible sliver and the
  graveyard phase disappears.
- Keep `$` out of every string — write `USD`, `RM`, `EUR`. LaTeX parsing crashes the render.
- Shade the death window with a faint `axvspan`; use a near-opaque dark span for the
  suspended/delisted period so the dead zone reads as dead.
- `pandas` index from a vendor carries a timezone — call `tz_localize(None)` before comparing
  against naive `datetime(...)` literals, else
  `Invalid comparison between dtype=datetime64[s, Asia/Kuala_Lumpur] and datetime`.
- `fig.add_axes((l, b, w, h))` requires a tuple; a list trips the type checker.
- The pyrolite `legend.bbox_to_anchor` warning is harmless — the figure still renders.
- Set an explicit `ax.set_ylim` low enough for the death phase; autoscaling to a parabola flattens
  everything after it.

## 3. Layout that reads for a non-trader

- Header: title, a one-line thesis, the motto.
- One panel per company when comparing; identical y-scale treatment is not required but identical
  *annotation style* is — the point is the shared silhouette.
- **Annotate every event** as a callout box with a leader line:
  `xytext=<offset in points>`, `textcoords="offset points"`,
  `arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9)`,
  `bbox=dict(boxstyle="round,pad=0.38", fc="#161628", ec=<accent>, lw=0.9)`.
  Store the per-point offset in the data row itself so collisions are fixed by editing one number.
- **Summary box in dead space.** Place a large accent-bordered box reading `PEAK X → Y` plus the
  percentage in the empty margin — by the end of the series price is near zero, so the upper right
  is free. Use `transform=ax.transAxes` with `ha="right"`.
- Two stacked panels (top: the Malaysian case, bottom: the international one) read better than one
  dense chart when the request is comparative.
- Footer: the source/method note in small italic type, below the axes, clear of the tick labels.

## 4. Verify before delivering

Render → `vision_analyze` the PNG with an explicit layout question ("does any annotation overlap
 the title, does any label run off an edge, is the footer clear of the bottom chart?") → adjust the
stored offsets → re-render. This catches real defects: a peak callout landing on the panel title,
and a floor label dropping below the plot into the year-tick strip. Adjusting `xytext` in the data
row is a one-number fix.

Convert to JPEG (`PIL`, quality 94) before `MEDIA:` delivery — these PNGs run 1–2 MB and the chat
render is more reliable around 300 KB.
