---
name: chart-artifact-render-qa
description: "Use when rendering a chart or PDF artifact for a human."
version: 1.0.0
author: hermes
license: MIT
tags: [matplotlib, chart, pdf, dark-theme, render-qa, vision-verify, yfinance]
metadata:
  hermes:
    category: creative
    related: [trading-signal-chart, rendered-document-audit, visual-artifact-delivery, forge-pdf-delivery]
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
- **A single `$` in a label renders literally; a second `$` in the same string starts mathtext** and
  can swallow the rest of the line. Write `USD`/`RM`/`EUR` in text rather than relying on the symbol.
- **Do not claim a figure is delivered without checking the file.** Generate, `ls -lh`, then send.
