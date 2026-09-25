# Scientific Diagram with Text Labels — Fallback Rule

## Why AI image generators fail for labeled diagrams

Tried multiple AI image generators for scientific cross-sections, geological diagrams, charts with annotations, and WhatsApp-style message walls. **Every time the labels are corrupted.** Examples observed:

- "Penerusuan" rendered as "Peneruuan"
- "Miocene" rendered as "Miace?ne"  
- "Eocene-Oligocene" rendered as "Ecosone-Oligocena"
- "Pekaka Well" rendered as "PluéAkns"
- Title "Cross-section" rendered as "Cross-ction"
- Scientific labels show up as phonetic-approximation gibberish, missing characters, or repeated characters
- Numbers frequently corrupted ("0km" appearing twice in depth scale)
- AI also adds hallucinated elements not in prompt (kangaroo on mountain top)

## The rule

**For any diagram that needs labeled text (depth scales, axis labels, callouts, headers, legends): render with matplotlib programmatically, not via AI image generation.**

Two-stage workflow when delivering a labeled scientific diagram:

1. **Generate aesthetic/visual base** with AI image generator (optional, only if visual quality matters)
2. **Render labels programmatically** with matplotlib (`text()`, `annotate()`, `bbox`) on top of either the AI base or a clean programmatic background

If step 1 produces garbage labels, **discard step 1 entirely** and render the whole thing programmatically. Don't waste iteration cycles trying to coax AI into spelling "Eocene-Oligocene" correctly.

## When AI image generator IS the right call

Use AI image generation when:
- Pure visual / aesthetic content (no text)
- Hand-drawn or painterly style needed
- Background or scenery
- Mood boards, hero images

Do NOT use for:
- Scientific diagrams with labels
- Cross-sections, stratigraphic columns, maps with annotations
- Charts with axis labels and legends
- Any image where specific words must appear correctly

## Programmatic matplotlib pattern (verified working)

```python
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import FancyBboxPatch

# Bigger figsize + bigger dpi + right axis range prevents label clipping
fig = Figure(figsize=(22, 14), facecolor=BG, dpi=180)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 24)  # Account for leftmost element like depth scale
ax.set_ylim(0, 18)  # Account for bottom legend/validation boxes
ax.set_facecolor(BG)
ax.axis('off')

# Save with explicit CanvasAgg, not plt.savefig
canvas = FigureCanvasAgg(fig)
canvas.print_png(out_path)
```

**Three pitfalls when rendering with matplotlib:**

1. **Y-flip issue:** `ax.imshow()` displays image in standard orientation, but `ax.text()` uses math convention (y-up from origin). If you set `ax.set_ylim(H, 0)` to flip, the TEXT position is now inverted. Test with a single label before committing.

2. **Right-edge clipping:** Labels placed near `x = ax.get_xlim()[1]` get cropped because matplotlib draws text outside the figure bbox but PNG rasterization includes only inside. Either pull labels inward or extend axis range.

3. **Bottom-edge clipping:** Same for y. If you place legend at `y = 0`, it's right at the edge. Either extend `ax.set_ylim(0, -2)` or place legend higher.

## Verification step after every render

Vision-check the rendered image BEFORE delivering. Read every label. The agent's own text-rendering code passes its own parser but PNG rasterization can clip, overlap, or render fallback characters when fonts don't have specific glyphs.

## Sources (sessions that taught this)

- arifOS Federation session 2026-09-25: ARIF_SABAH_HYPOTHESIS cross-section (matplotlib version clean, AGY/Qwen-PAYG version had garbled text "Low Peaalu", "PluéAkns", "Miace?ne", kangaroo hallucination)
- Similar pattern observed in 6+ prior image-generation attempts across other sessions

DITEMPA BUKAN DIBERI.
