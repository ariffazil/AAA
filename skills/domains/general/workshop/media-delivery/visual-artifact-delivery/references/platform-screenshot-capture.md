# Capturing a chart from the platform the reader already uses

When the reader tracks the instrument on his own charting surface, **his screenshot is the
authoritative render**. Re-drawing it by hand is slower *and* less honest: you re-derive a series that
you may adjust, scale or overlay differently from the platform he is looking at, which turns a
presentation choice into an apparent disagreement about facts.

## When to pull rather than plot

Pull when:

- the instrument is **listed and live** on a platform he uses;
- he shared a link or a screenshot of his own chart;
- the chart needs indicator overlays he already has configured (EMA stacks, S/R scripts).

Hand-draw when the artifact is something no platform can render: a reconstructed history for a
delisted ticker, a balance-sheet arc, a model output, a two-detector comparison. See
`historical-reconstruction-charts.md`.

## Share link → image URL

A `tradingview.com/x/<ID>` link is a snapshot page. The rendered chart is published as one image on
their CDN, under a directory named by the **first character of the ID**:

```
https://s3.tradingview.com/snapshots/<first-char-of-ID>/<ID>.png
```

The same URL is exposed on the page as `meta[property="og:image"]` — **read the meta tag rather than
constructing the path**, so a CDN convention change does not silently break you.

Workflow (text-first; the page is JS-heavy, so a plain fetch returns only a shell):

1. Open the link in the browser tool.
2. Read `document.title` — it carries the exchange, symbol and author, e.g.
   `MYX_DLY:PCHEM Chart Image by <user>`.
3. Read `meta[property="og:image"]`; fall back to `meta[name="twitter:image"]`, then to the largest
   `<img>` by `naturalWidth`.
4. `curl -sL -o chart.png <url>` and confirm with `file` that it is a PNG — not an HTML error page.
5. Read it with the vision pass, asking for the axes explicitly.

## Reading a tall snapshot

These snapshots come back portrait and tall (observed 1324x2588). Downscaling to fit a read loses
axis text, so **crop into vertical strips at full resolution** and read them individually:

```python
from PIL import Image
im = Image.open("chart.png").convert("RGB")
W, H = im.size
n = 4
step = H // n
for i in range(n):
    im.crop((0, i * step, W, min(H, (i + 1) * step))).save(f"strip{i + 1}.png")
```

**Ask for the axes, not just the shape.** A read that returns only "it goes down then up" is not a
read. Scope it: symbol, exchange, timeframe, current price and change, the price-scale values, the
indicator legends, the date range, and any annotation the author added. Then ask the collision
question from the parent skill before shipping.

## Limits — state these when they matter

- The snapshot carries **the author's** indicators and adjustment basis, not yours. If the series
  spans a corporate action, say which basis the image is on (see the consolidation note in the
  parent skill).
- A chart image is a witness to **what the platform drew**, not to what the exchange printed. It
  resolves "what is on my screen" and not "what is true".
- A share link is the author's saved view — zoom, timeframe and overlays are theirs. Ask him to
  re-share rather than reconstructing a different view and presenting it as the same one.
