---
name: chart-artifact-render-qa
description: "Use when rendering a chart or PDF artifact for a human."
version: 1.0.0
author: hermes
license: MIT
tags: [matplotlib, chart, pdf, dark-theme, render-qa, vision-verify, yfinance, gemini, image-generation]
metadata:
  hermes:
    category: creative
    related: [trading-signal-chart, rendered-document-audit, visual-artifact-delivery, forge-pdf-delivery]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Chart / PDF Artifact — Render & Verify QA

Covers producing a static data-visual artifact (PNG or PDF) and confirming it is actually readable
before it reaches the human. Trading-signal charts add their own methodology on top; this skill is
the rendering and QA layer underneath any chart.

## Procedure

1. **Write the script to a file, run it with `terminal()`.** Do not build matplotlib/reportlab
   inside `execute_code` — keep generation in a script so it is re-runnable after a fix.
2. **Assert the file exists and is non-trivial before delivering.** `ls -lh` the output; a 0-byte or
   missing PNG means the render failed silently.
3. **Vision-read the rendered PNG and ask about LAYOUT specifically** — overlap, clipping, cut-off
   labels, unreadable axes. Then fix and re-render.
4. **Deliver** with `MEDIA:/abs/path`. Convert PNG→JPEG first when the payload is large.

### Step 3 is the step people skip, and it is the one that catches real defects

A chart's code cannot see its own layout. Auto-placed annotations stack on the title; the last
label jams into the right frame; two callouts land on the same point. Ask the vision read directly:
*"does any annotation overlap a title? is any label clipped at the edge? are the axes legible?"*
Generic "describe this chart" returns prose and misses the collision.

Then fix deterministically: give every annotation an explicit `xytext` offset in data units rather
than letting matplotlib choose, and pull the axis limit out to leave headroom.

## Dark-theme house style

Arif's artifacts are dark, high-contrast, and quiet. Reuse this palette instead of inventing one:

```
Background  #0d0d0d    Primary text  #f5f0e8
Gold accent #d4a843    Red (bear)    #c0392b
Green       #27ae60    Grey (dim)    #888888
Blue        #4a6fa5    Purple        #7b2d8e
```

Layout: `fig.text()` for the title block and footer, `fig.add_axes([l, b, w, h])` for each panel, and
a small gold `DITEMPA BUKAN DIBERI` mark top-right. Close with a source/caveat line in italic grey
whenever figures were reconstructed rather than fetched.

## Pitfalls

- **When `plt.savefig()` produces corrupted PNG dimensions (e.g. width=285,643 px), the bytes write
  successfully, the script exits 0, and downstream tools crash with `DecompressionBombError`.** The
  root cause is usually a stale `*.mplstyle` in `~/.config/matplotlib/stylelib/` (e.g. `pyrolite.mplstyle`)
  whose malformed directive (`legend.bbox_to_anchor : (1, 1)`) silently inflates the rendered width.
  Switch to direct `Figure()` + `FigureCanvasAgg()` construction to bypass the pyplot state machine:
  ```python
  fig = Figure(figsize=(13, 8))
  canvas = FigureCanvasAgg(fig)
  ax = fig.add_axes([0.05, 0.05, 0.90, 0.85])
  ax.plot([0, 1, 2], [0, 1, 4])
  canvas.print_png(out)
  ```
  Then verify on-disk dimensions with `PIL.Image.open(out).size` before downstream use. Full recipe:
  `references/matplotlib-direct-figure-pattern.md`.

- **tz-aware pandas index vs naive `datetime` throws.** yfinance history on Bursa/KL tickers returns
  tz-aware (`datetime64[s, Asia/Kuala_Lumpur]`); comparing it to `datetime(...)` raises
  `Invalid comparison between dtype=datetime64[s, Asia/Kuala_Lumpur] and datetime`. Strip once at
  load — `dates = h.index.tz_localize(None)` — before any mask, `axvspan`, or `set_xlim` bound.
- **`datetime(2018, 6)` is a `TypeError`.** The constructor needs all three args; use
  `datetime(2018, 6, 1)`. Bites when hand-writing milestone dates.
- **Delisted tickers return 0 rows, not an error.** `yf.Ticker(...).history(period='max')` gives an
  empty frame plus a `possibly delisted` notice. For bankrupt/absorbed entities, reconstruct the
  series from *reported closing prices* in the press and case-study literature, plot those points,
  and list the sources in the footer — never silently drop the entity or interpolate a fake path.
- **`add_axes` with a list `rect` works at runtime** even when the type checker flags it. Multi-panel
  `fig.add_axes([0.06, 0.11, 0.90, 0.30])` layouts are fine; LSP complaints here are noise. Do not
  rewrite a working layout to silence them.
- **A non-fatal `Bad key legend.bbox_to_anchor in .../pyrolite.mplstyle` warning** appears on every
  render. Ignore it — the artifact is unaffected.
- **A stale `*.mplstyle` under `~/.config/matplotlib/stylelib/` silently corrupts output PNG dimensions** —
  e.g. a `pyrolite.mplstyle` shipped with a malformed `legend.bbox_to_anchor : (1, 1)` makes
  `savefig` write a PNG whose width is the figure-width-in-PIXELS × dpi × an inflated multiplier,
  producing files like `285643 x 622` instead of `1100 x 700`, blowing past `PIL.Image.MAX_IMAGE_PIXELS`
  and crashing downstream converters with a `DecompressionBombError`. `figsize=(W, H)` and `dpi=N` look
  correct in source but the rendered PNG is 250× too wide. The non-fatal warning is the
  canary — fix by deleting the offending style file (`rm ~/.config/matplotlib/stylelib/<name>.mplstyle`),
  re-render, then verify with `python3 -c "from PIL import Image; print(Image.open(<out>).size)"`. **Never
  trust the on-disk size before checking it** — this is the failure shape where the bytes write
  successfully and the script exits 0, while the artifact is unusable.
- **A single `$` in a label renders literally; a second `$` in the same string starts mathtext** and
  can swallow the rest of the line. Write `USD`/`RM`/`EUR` in text rather than relying on the symbol.
- **Do not claim a figure is delivered without checking the file.** Generate, `ls -lh`, then send.
- **Matplotlib Rectangle import from pyplot is flagged by LSP but works at runtime.** Use `from matplotlib.patches import Rectangle` for clean code; `plt.Rectangle(...)` triggers type-checker warnings but runs fine.
- **Geological cross-sections MUST invert Y-axis.** Surface at top, depth increasing downward. `ax.set_ylim(max_depth, -offset)` reverses the axis. If user says "terbalik" (reversed), this is the cause — check Y-axis direction first. Never use `plt.gca().invert_yaxis()` after `fill_between` — set ylim directly in the plotting code.
- **When overlaying annotation lines (anchor lines, price markers, target zones) on a user-supplied chart, the price-to-y transform MUST be derived from the chart's own visible price ladder, not from a different data source.** A captured MT5/TradingView screenshot has its own price axis; if the live API quote (e.g. yfinance GC=F) is $20+ away from the chart's stated price, the chart's price ladder ticks (the labels printed on the right edge) are the ground truth for placement. Build `price_to_y(p)` from those ticks (top tick → y=1.0, bottom tick → y=0.0) and verify the lines land *on the labeled prices*, not at some offset you only spot-check. Vision-verify must specifically ask "are the anchor lines at the correct price levels on the chart?" — a generic "describe the image" prompt returns prose about the chart and misses the positional defect. The defect is silent in code: matplotlib happily draws the line where you told it to, and only the visual diff between chart label and overlay line reveals it.

- **`fill_between` array-shape mismatch.** When `fill_between(x, p10, p90)` raises `ValueError: 'x' has size 24, but 'y1' has an unequal size of 25`, the cause is that the percentile computation produced one extra point than the candle count. If you compute percentiles over `n` Monte Carlo paths each of length `T` (so `arr.shape == (n, T+1)` because each path includes the starting price), then `arr[:, k]` has shape `(n,)`, giving percentile arrays of length `T+1`, but the x-axis `np.linspace(start, end, T+1)` is the right length — the mismatch comes from mixing them. Fix by aligning x to the percentile array length, or drop the starting point from the percentile series before plotting. Verified (2026-09-25).

- **Right-edge percentile/label clipping despite `xlim` headroom.** Right-edge text annotations placed at `x = xlim_max - epsilon` still get clipped because matplotlib text rendering extends past the x-coordinate by the text width + bbox padding. Two fixes that survive: (a) explicitly use `ha='right'` AND wrap the text in `bbox=dict(facecolor='#1a1a1a', edgecolor='none', pad=1.5, alpha=0.9)` so a coloured background mask hides any overflow into the spine; (b) OR place labels INSIDE the plot area at `x = xlim_max - 4` (well inside the data zone). The bbox-mask approach is preferable when the chart already has a dense right edge and pulling the labels inward would collide with the fan-chart lines. Verified (2026-09-25).

- **Multi-column header overlap in info panels.** When the bottom info panel needs N column headers (e.g. QUALITATIVE / QUANTITATIVE / QUANTUM / CHRON / PROTOCOL), placing them too close causes matplotlib text to render as garbled letter-collision ("PRADDICEOL"-style). Rule: each column header must occupy a non-overlapping x-range with **at least 1.5x the text width** of headroom. For 5 columns in a 0–54 x-space, use x-positions `[5, 16, 27, 38, 49]` (separation of 11 units, ~5x the typical 9pt header width). Then keep body content of each column strictly within that x-range — `ax.text(col_x[i] + 2, y, ...)` for left-aligned body, not the column header x-position itself. Verified (2026-09-25).

- **Bottom info panel clipped at y=0.** When the bottom info panel is drawn with `FancyBboxPatch((x0, 0), width, height)` and the panel content extends below `y=0`, the bottom rows get clipped silently. Mitigation: set `ax.set_ylim(ylim_min, ylim_max)` with `ylim_min` BELOW 0 (e.g. `ylim(4150, 4400)` for a 4400–4150 vertical span) and place the panel at a y-coordinate well within the ylim range (e.g. `y0=4190` for a panel spanning 4190 to 4220). Vision-verify MUST specifically ask "is the bottom panel's bottom row visible (not clipped at y=0)?" — a generic "describe this image" misses this entirely because the panel still has a visible border, just without its bottom content. Verified (2026-09-25).

- **Vision-verify must request LAYOUT questions specifically, not generic description.** A chart's code cannot see its own layout. Auto-placed annotations stack on the title; the last label jams into the right frame; two callouts land on the same point. Ask the vision read directly: *"does any annotation overlap a title? is any label clipped at the edge? are the axes legible? are all column headers distinct with no overlapping text? is the bottom info panel fully visible?"* Generic "describe this chart" returns prose and misses the collision. Verified (2026-09-25) — three separate chart re-renders converged only after explicit layout-fragmentation questions were added to the vision prompt.

- **Vision reads PNGs in image-native coordinates (origin top-left, Y increases downward), but matplotlib's default Y axis grows upward.** When you `ax.imshow()` a user-supplied photo and overlay `ax.text()` annotations, the two coordinate systems disagree silently — vision may report "title at bottom" when matplotlib says "title at top", because vision reports pixel positions, not data positions. Three viable fixes, pick one and stay consistent: (a) `ax.set_ylim(ylim_max, ylim_min)` to flip matplotlib's Y to match image coordinates; (b) place text at `y_pixel` directly where `y_pixel = 0..H` is image-native top-down, ignoring matplotlib's coordinate frame; (c) `ax.imshow(img, origin='lower')` but this visually flips the image — only viable when image orientation doesn't matter. The defect is silent in code: matplotlib draws the title at the data position you specified, and only the visual diff between data frame and image frame reveals it. Three re-renders converged on this in one pass (seismic annotation, 2026-09-25). Recipe for the full pattern: `references/image-overlay-annotation-pattern.md`.

- **Seismic horizon overlay MUST follow real reflector geometry — never parallel-flat lines.** When overlaying interpretation markers on a seismic section, drawing horizon H1, H2, H3, H4 as equispaced flat horizontal lines parallel across the section is the BANGANG shape. Real seismic reflectors have variable spacing (intervals expand/compress across the section), wavy geometry (follow dip, structural curvature, facies change), and amplitude variation (bright/dim bands). The rules: (1) trace each horizon's actual reflector position from the image — variable spacing between successive horizons, NOT equal gaps; (2) wavy geometry that follows structural dip — if there's an anticline crest, the horizon curves up there; (3) no horizon should cross another — if geometry forces it, the model is wrong, not the data; (4) horizons deeper in section are typically more continuous (regional seal), shallower are more disrupted (tectonic overprint). Quick acceptance test: if H1/H2/H3/H4 look like railroad tracks — equally spaced, perfectly horizontal — the overlay is fake. V1 was rejected for this exact reason; V2 was accepted after spacing became depth-dependent. If a `geox_seismic_interpret` `classical_section` or `interpret_section` mode is available, prefer the GEOX candidate output over hand-drawn placeholder lines — GEOX runs K-DIP/K-THROW/K-DL gates so the proposed geometry is at least physics-plausible, while matplotlib hand-draw is just a graphic, not evidence.

## References

- `references/matplotlib-direct-figure-pattern.md` — bypass the pyplot state machine
  with `Figure()` + `FigureCanvasAgg()` to dodge stale `*.mplstyle` corruption.
- `references/gemini-api-image-generation.md` — Gemini image-gen recipe.
- `references/wealth-mcp-tool-schemas.md` — verified schemas for the two
  `mcp__wealth__capital_market` / `mcp__wealth__capital_indicator` MCP tools, plus
  the call pattern that anchors Monte Carlo fan-chart inputs without triggering
  argument-validation errors. Use whenever the deliverable depends on a live
  WEALTH snapshot (gold 24H probability bands, multi-indicator panels).
- `references/monte-carlo-fan-chart-pattern.md` — full recipe for the
  quantitative 24H prediction fan chart: ATR-scaled GBM with EMA20 drift,
  percentile bands (P10/P25/P50/P75/P90), 5-column intelligence panel layout,
  and vision-verify checklist targeting the specific failure modes of this
  layout. Use when the deliverable is a "WEALTH CHRON intelligence"-style
  probability reading over a horizon (not a single-point price prediction).
- `references/lightweight-charts-fan-overlay-pattern.md` — the web-widget
  counterpart to the matplotlib variant above. For drawing a probability
  fan directly on the lightweight-charts v4 widget extending past the last
  candle (not a static PNG). Covers the 4-area-series band trick, native
  setMarkers for endpoint labels, HTML overlay workaround for vertical time
  line (not natively supported), and clamped linear interpolation between
  supplied quantiles. Use when the deliverable is a live HTML page rather
  than a chart artifact.
- `references/image-overlay-annotation-pattern.md` — overlaying interpretation
  markers on a user-supplied photo (seismic sections, x-rays, chart screenshots,
  mockups). The user is the domain expert; the overlay is a conversation
  prompt, not a professional deliverable. Covers the matplotlib Y-flip trap
  (vision reads image-native coordinates, matplotlib's default is inverted),
  generic color/symbol convention, ellipse-dashed-for-interpretation,
  mandatory disclaimer pattern, and the vision-verify checklist targeting
  the specific failure modes of overlay-on-photo (annotation overflow, garbled
  column headers, image covering annotations, hallucinated extra text).
  Seismic-specific addendum covers horizon geometry (variable spacing +
  structural curvature — railroad-track horizons rejected), GEOX
  `classical_section` mode integration for actual structural picks, and the
  vision-verify question that catches railroad-track horizons specifically.
