# Conceptual Chart Pack Recipe — Reflective / Essay PDFs

For personal-reflection or essay-class PDFs (vs. the data-driven WEALTH/333 SOVEREIGN briefings), the chart pack is **conceptual diagrams**, not data charts. Proven 2026-08-07 on the "Itulah Manusia" 8-chart pack — used in `/root/forge_work/itulah-manusia/charts/build_charts.py` and embedded in the 20-page PDF.

## Eight chart patterns that work

Each is a standalone figure module. Mix and match based on the essay structure.

| # | Pattern | Shape primitives | Anchors |
|---|---|---|---|
| 01 | Persona/Shadow schema | Two `Circle`s + vertical arrow + flanking trait labels | Jung; identity work |
| 02 | Two-policies-in-one-body | Two `FancyBboxPatch`es + diagonal arrow + dashed envelope | Sublimation; internal conflict |
| 03 | Sublimation fork | Source `Circle` + 2 output boxes + branch lines | Freud/Jung; repression |
| 04 | Complementarity matrix | `ax.scatter` grid + axis labels + cross-pair vs diagonal markers | Variance; attraction theory |
| 05 | Timeline of feeling | Linear `ax.scatter` + arrow + band labels + insight box | Affective primacy (Zajonc, Damasio, LeDoux) |
| 06 | Body/heart gap | Two side-by-side boxes + centered label in navy channel + double arrow | Visible/hidden split |
| 07 | Filter fall / projection | Vertical box stack + trigger arrow + projection `Circle` + recognition arrow | Jung projection |
| 08 | The omega | Three `Circle`s (show / gap / hide) + outward arrow + framed question | Open-frontier framing |

## Pattern grammars (recurring)

- **Centered-in-channel label.** When text sits between two colored shapes (chart 06): fontsize 9–11, stacked vertically, place the connecting arrow BELOW the text, NOT through it. Vision-analyse for "left edge of THE touches box" defect.
- **Diagonal-pair vs cross-pair.** When building a matrix (chart 04): diagonal = "same" markers (low pull, gold fill, NAVY text at s=350), cross-pair = "complement" markers (high pull, BLUE fill, CREAM text at s=550). `clip_on=False` everywhere; expand axis headroom by 0.3.
- **Arrow-label pill.** When text labels a curved arrow (chart 02): wrap the label in `bbox=dict(boxstyle="round,pad=0.3", fc=NAVY, ec=ORANGE, lw=1)` so the label masks the arrow stroke behind it. Otherwise the stroke bisects the text.
- **Dashed envelope for "one body, two policies" (chart 02).** `FancyBboxPatch` with `linestyle="--"` and `fc="none"` shows that two boxes live inside one container without imposing a hard border.

## Build discipline

1. **One batch script, one rcParams block, one palette.** `build_charts.py` with `NAVY/GOLD/RED/GREEN/BLUE/ORANGE/CREAM/GREY` constants at the top. Every chart reuses the palette — no per-chart drift.
2. **All charts in one pass.** Don't iterate per chart. ~8 charts ≈ 30s in one Python run vs 3min if serialised.
3. **Import `Circle` directly.** `from matplotlib.patches import Circle, FancyBboxPatch, Wedge, FancyArrowPatch`. `plt.Circle` is not exported — raises `reportPrivateImportUsage` on lint.
4. **`ax.axis("off")` on every diagram.** These are diagrams, not data plots. Grid + spines are noise.

## Verification (mandatory per chart)

Before declaring the pack done, run vision_analyze on EACH rendered PNG:

```bash
python3 -c "
from hermes_tools import vision_analyze
"  # then batch vision_analyze() calls in parallel
```

Vision questions to ask per chart:
- "Is every label fully readable? Any text appearing truncated or clipped?"
- "Does any text overlap onto a colored shape it's not supposed to?"
- "Are all markers inside the chart area, not clipped at edges?"
- "Are titles and figure numbers correct (e.g. '04' not '06')?"

## When to skip this pattern

If the user asks for a data report (NOC, energy, fiscal), use the data chart pack instead. Conceptual diagrams are for essays/reflections, not briefings.