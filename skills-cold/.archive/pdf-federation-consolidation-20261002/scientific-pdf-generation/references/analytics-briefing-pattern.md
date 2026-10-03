# Analytics-Embedded Briefing Pattern (proven 2026-08-25)

For intelligence briefings that need **data visuals embedded alongside text** — not just text-heavy reports. Generates matplotlib charts as PNGs, embeds in HTML, renders via weasyprint.

**When to use:** User asks for a briefing PDF with charts, maps, risk matrices, data analytics, flow diagrams, or "give me the full picture." NOT for pure text dossiers (Mode B) or academic papers (Mode A).

**Stack:** matplotlib (charts) + HTML template (layout) + weasyprint (render). NOT reportlab — HTML gives better image embedding.

## Chart Types Proven

| Chart | Type | Use Case |
|-------|------|----------|
| Bar (grouped) | Monthly comparison (2 categories) | Historical incident tracking |
| Horizontal bar (stacked) | Categorical distribution | Status by severity band |
| Dual-axis line+bar | Temperature range + precipitation | 7-day forecast with clear window highlight |
| Risk matrix scatter | Likelihood × Impact (2D) | Multi-hazard assessment |
| Pipeline flow diagram | 5-stage horizontal boxes + arrows | Data methodology visualization |
| Stylized regional map | Polygon patches + scatter markers | Geographic context (not GIS-accurate) |

## Pipeline

```python
# Step 1: Generate charts as PNGs to charts/ subdirectory
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import os
os.makedirs("charts", exist_ok=True)
# ... generate fig01.png through fig06.png at dpi=150

# Step 2: Write HTML with <img src="charts/fig01.png"> references
# Step 3: weasyprint input.html output.pdf
```

## Design Tokens (Light-Clean Analytics Theme)

```css
:root {
  --page-bg: #FFFFFF;
  --text-primary: #1A1A2E;
  --text-secondary: #5C5C6D;
  --text-caption: #8A8A9A;
  --accent: #1B5E7B;
  --accent-light: #E8F4F8;
  --verdict-bg: #F0F7FA;
  --verdict-border: #1B5E7B;
  --tag-obs: #2E7D32;
  --tag-der: #1565C0;
  --tag-int: #6A1B9A;
  --tag-spec: #E65100;
  --divider: #E8E8EE;
}
```

Matplotlib must match: `figure.facecolor: white`, `axes.spines.top/right: False`, muted palette.

## Epistemic Tags (Inline in Both HTML and Charts)

```css
.tag { display: inline-block; font-size: 6.5pt; font-weight: 700;
       text-transform: uppercase; padding: 1px 5px; border-radius: 2px; }
.tag-obs { color: #2E7D32; background: #E8F5E9; }
.tag-der { color: #1565C0; background: #E3F2FD; }
.tag-int { color: #6A1B9A; background: #F3E5F5; }
.tag-spec { color: #E65100; background: #FFF3E0; }
```

Every chart: `<div class="chart-caption">FIG N — description. [TAG]</div>`

## Page Layout (5-page analytics briefing)

| Page | Content |
|------|---------|
| 1 | Cover: title, verdict box, KPI metric cards (4 boxes) |
| 2 | Signal section + bar chart |
| 3 | Map + contextual signals |
| 4 | Forecast chart + risk matrix |
| 5 | Pipeline diagram + severity chart + source table |

## Pitfalls

- matplotlib `letterspacing` is not a valid Text property — remove from `ax.text()`
- `plt.Circle` works but import `Circle` from `matplotlib.patches` to satisfy pyright
- `print-color-adjust: exact` ignored by weasyprint — harmless warning
- `fontweight=600` falls back to 700 — cosmetic warning only
- Stylized maps are NOT GIS-accurate — label "stylized schematic" in captions
- Pyrolite mplstyle warning is cosmetic — silence with `MPLCONFIGDIR=/tmp/.mpl`

## USER PREFERENCE (2026-08-25)

Arif explicitly rejected dark backgrounds for briefings. Default = white, clean typography, high contrast. Dark = legacy only. "I hate dark background like this. Less chaos."

## Proven Deliverable

- 2026-08-25: Penang/Kulim Weather/Flood Brief — 5 pages, 6 analytics panels (bar chart, horizontal bar, dual-axis forecast, risk matrix, pipeline flow, stylized regional map), 290KB, light theme, epistemic tags. Full source: `/root/AAA/forge_work/2026-08-25-civic-weather-brief/`
