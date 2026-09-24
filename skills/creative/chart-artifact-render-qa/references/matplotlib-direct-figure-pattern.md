# Matplotlib Direct Figure Pattern — When `plt.savefig()` Corrupts Output

When `matplotlib.pyplot.savefig()` produces a PNG whose dimensions are wildly larger than expected (e.g. width=285,643 px when figsize=(11, 7) and dpi=100), the bytes write successfully, the script exits 0, and the artifact is unusable — downstream tools like `pdftoppm` or `PIL.Image` crash with `DecompressionBombError`.

**Root cause:** the matplotlib config cascade is loading a stale `*.mplstyle` from `~/.config/matplotlib/stylelib/`. The offender shipped with a malformed directive (e.g. `legend.bbox_to_anchor : (1, 1)` without a tuple of 4 numbers), and `savefig` silently inflates the figure's width by an unbounded multiplier. The on-disk PNG dimensions no longer match `figsize × dpi`.

## Procedure

When you suspect dimension corruption (or have hit it before):

1. **Switch to explicit `Figure()` + `FigureCanvasAgg()` direct construction.** This bypasses the pyplot global state machine and any cascading `mplstyle` interference.

   ```python
   import matplotlib
   matplotlib.use("Agg")  # non-interactive backend
   from matplotlib.figure import Figure
   from matplotlib.backends.backend_agg import FigureCanvasAgg

   # Build figure directly — no pyplot
   fig = Figure(figsize=(13, 8))
   canvas = FigureCanvasAgg(fig)  # required so renderer is wired

   ax = fig.add_axes([0.05, 0.05, 0.90, 0.85])
   ax.plot([0, 1, 2], [0, 1, 4])
   ax.set_title("Direct figure — no pyplot state")

   out = "/path/to/output.png"
   canvas.print_png(out)
   print(f"WROTE {out} {os.path.getsize(out)} bytes")
   ```

2. **Always verify on-disk dimensions before downstream use.**

   ```python
   from PIL import Image
   img = Image.open(out)
   expected_w = int(13 * dpi_factor)  # actual factor depends on backend
   actual_w, actual_h = img.size
   assert actual_w < 5000, f"corrupted dimensions {img.size}; suspected mplstyle contamination"
   ```

3. **If a corrupt `mplstyle` exists, delete it then re-render.**

   ```bash
   rm ~/.config/matplotlib/stylelib/<name>.mplstyle
   python3 /tmp/script.py  # re-render
   python3 -c "from PIL import Image; print(Image.open(out).size)"
   ```

4. **After render, sanity-check size on disk** — `ls -lh output.png` and verify the byte count is consistent with expected dimension × dpi × bytes/pixel. A 200 KB file at 1100×700 is healthy. A 2 MB file at 1100×700 means matplotlib rendered at higher resolution than expected — investigate.

## Why `plt.savefig()` is fragile in multi-session work

`matplotlib.pyplot` keeps a global figure manager. Once `plt.figure()` is called in one cell, the figure registry persists across `clear_output` or new cell boundaries. Subsequent calls inherit state — including any contaminated style — without warning. The direct `Figure()` + `FigureCanvasAgg()` pattern constructs an isolated renderer with no shared state, which is the safe default for any production-grade chart pipeline.

## When to use direct Figure vs plt.figure

| Situation | Pattern |
|---|---|
| One-off exploratory plot | `plt.figure()` + `plt.show()` (interactive only) |
| Chart for Telegram/PDF delivery | `Figure()` + `FigureCanvasAgg()` direct |
| Multi-panel layout with explicit axes positions | `Figure()` + `add_axes([l, b, w, h])` |
| Animation / live updates | `plt.ion()` + `plt.draw()` |
| Anything that gets archived to `forge_work/` | `Figure()` + `FigureCanvasAgg()` direct |

## Pair with vision-verify

After saving, always run a vision verify that asks specifically about layout defects:

> "Does any annotation overlap a title? Is any label clipped at the edge? Are the axes legible?"

A generic "describe this chart" returns prose and misses collisions. Layout-level QA is the only QA that catches the matplotlib-silent defects.

## Reference implementation

See `/root/.hermes/workspace/` for working examples that use this pattern:
- `ONE_DAY_2026-09-22.png` — full-page timeline with two yin-yang circles
- `ALPHA_GUIDE_cover_v2.png` — single-subject editorial cover with overlay
- `syed_position_analysis.png` — multi-panel trade waterfall with annotation arrows

All three saved via `canvas.print_png(out)` and verified with `PIL.Image.open(out).size`.
