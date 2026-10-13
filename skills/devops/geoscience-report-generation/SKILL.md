---
name: geoscience-report-generation
description: "Geoscience PDF reports with matplotlib geological plots."
owner: curator
risk_tier: low
floor_scope: [F1, F2, F7, F13]
autonomy_tier: T1
version: 1.0.0
tags: [geology, matplotlib, pdf, visualization, cross-section, report]
capability_tier: fed-long-context
ecology_state: WARM
owned_by: curator
authority_of: AAA
---

# Geoscience Report Generation

Generate professional-grade PDF reports with embedded geological visualizations.

## §1 — Report Architecture

1. Cover page — title, classification, hero image
2. Executive summary — verdict upfront, key numbers
3. Geological evaluation — facies, stratigraphy, petroleum system
4. Technical assessment — reservoir quality, injectivity, risk
5. Commercial evaluation — NPV, sensitivity, breakeven
6. Risk matrix — probability x impact x mitigation
7. Recommendation — clear verdict with conditions

### Design Rules
- Location map MANDATORY for offshore projects. Never skip.
- Cross-section: show water, overburden, caprock, reservoir, basement, well, CO2 plume
- Clean layout — no cluttered/crowded visualizations
- Professional geological colors

## §2 — Matplotlib Geological Visualization

### Cross-Section Pattern
```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(16, 10))
gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1], hspace=0.15)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax2.axis('off')
```

### Layer Order (bottom to top)
1. Basement (gray) 2. Source rock (dark green) 3. Reservoir (yellow/orange)
4. Caprock (dark red) 5. Overburden (tan) 6. Water (blue)
7. CO2 plume (orange) 8. Injection well (gold) 9. Faults (red dashed)

### Depth: Y-axis INVERTED (surface at top), label in km/m, add scale bar

### Pitfalls
- PIL DecompressionBombError at dpi>200. Fix: save dpi=150, resize >5MB before embed.
- numpy float in ax.text(): cast to float() first.
- tight_layout fails with colorbars: use bbox_inches='tight' in savefig.
- plt.Rectangle not in pyplot: use matplotlib.patches.Rectangle.

## §3 — PDF Assembly

### Path A — ReportLab (default, for image-heavy reports)

```python
import os
from reportlab.platypus import Image
img_size = os.path.getsize(img_path)
if img_size > 5_000_000:
    from PIL import Image as PILImage
    img = PILImage.open(img_path)
    img.thumbnail((2000, 2000))
    img.save(img_path.replace('.png', '_small.png'))
els.append(Image(img_path, width=170*mm, height=106*mm))
```

Pipeline: matplotlib PNG (dpi=150) -> check ls -lh -> resize if >5MB -> reportlab PDF -> pymupdf verify pages

### Path B — SVG + rsvg-convert + pandoc (for asset dossiers, PSC reports, joint-venture intelligence)

When the deliverable is a *dossier* (operator intelligence, PSC briefs, MBR bid round screening) rather than an academic figure-heavy report, this pipeline outperforms Path A:

```bash
# 1. Hand-build or generate SVG (location maps, strat columns, cross-sections)
#    Inkscape-compatible; patterns + bezier curves + arrows work cleanly
# 2. Render to PNG at high resolution
rsvg-convert -w 1600 map.svg -o map.png
rsvg-convert -w 1200 strat-column.svg -o strat-column.png
# 3. Write the dossier as Markdown with image refs + provenance tables
# 4. Compile to PDF via pandoc with xelatex
pandoc DOSSIER.md -o DOSSIER.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=2cm \
  -V mainfont="DejaVu Sans" \
  --resource-path=.
```

**Why Path B is better for PSC / operator dossiers:**
- Pandoc + xelatex handles long structured Markdown (tables, footnotes, provenance) more cleanly than reportlab Flowables
- SVG gives vector quality at any zoom for maps and cross-sections
- `rsvg-convert` is a one-liner; no Python imaging dependency chain
- `MEDIA:/absolute/path/REPORT.pdf` delivery works identically

**Pitfalls — Path B:**
- `xelatex` default font (Computer Modern / lmmono) lacks Unicode box-drawing chars (═ ╝ ░ ▒ ▓). Use `-V mainfont="DejaVu Sans"` to avoid silent character drop.
- `--resource-path=.` is required for relative image paths in Markdown to resolve
- For very long reports (>50 pages), pandoc may run out of memory; chunk or use `weasyprint` fallback
- No reportlab-style dynamic tables; pre-render tables as Markdown

### Two-Layer Provenance Pattern (mandatory for operator/PSC dossiers)

Every claim in a geoscience dossier must carry a provenance tag identifying its source class. The two layers:

| Layer | Tag | Meaning | Example |
|---|---|---|---|
| **Primary issuer** | `JSE-AR25` / `MPM-2024` / `RNS-2024-07-26` / `arifOS-SOT-2026-10-07` | Direct from operator/regulator/issuer's audited public document | Jadestone 2025 Annual Report, MPM press release, RNS announcement |
| **Industry consensus** | `INDUSTRY CONSENSUS` / `Madon 1994` / `PETRONAS Atlas 2019` | Published petroleum geology literature, textbook framework, multiple-source agreement | Malay Basin stratigraphic framework, source rock TOC ranges, regional play concepts |
| **Operator-specific** | `JSE-AR25 p.49` | Direct from operator, page-cited | PM428 area = 6,676 km² (JSE-AR25 p.49) |
| **Hypothesis** | `HYPOTHESIS — labeled` | Agent synthesis, not in any source | "Trap style likely inversion anticline" |
| **Unknown** | `UNKNOWN — typed explicitly` | No public source, explicitly flagged | Specific prospect names within PM428 |

**Rendering rule:** Every table, every bullet, every figure caption in the dossier carries one of these tags. The reader can see, line by line, what is verified, what is consensus, and what is reading. The voice protocol (`aaa-pdf-voice-protocol`) translates the brackets into prose for human-readable PDFs — keep both forms in the working draft, translate at the end.

### The "Go Signal" Workflow (for sovereign-class requesters)

When the requester gives a "go" or "do" signal after initial probing, do not block again — execute with what you have, then upgrade.

```
User:  "Build me a PM428 Jadestone PDF"
Agent: probes -> "Jadeston is typo, confirm?"  [probe]
User:  "Buat pdf"  [GO signal]
Agent: render with what you have, mark unknowns typed explicitly
User:  "Use full pdf intelligence"  [UPGRADE signal]
Agent: re-render with audited primary sources + industry consensus
User:  "Do full geological insight in pdf. Visual intelligence"  [DEEPEN signal]
Agent: re-render with SVG maps, strat column, trap section cross-section
```

Each iteration upgrades the dossier. Don't ask "do you want me to upgrade?" — when the user explicitly widens scope, execute. The first render is the floor, never the ceiling.

## §4 — Geological Colors

Water=#4A90D9 | Overburden=#DEB887 | Sandstone=#E8A838 | Shale=#006400
Caprock=#8B0000 | Basement=#2F4F4F | CO2=#FF4500 | Well=#FFD700 | Fault=#FF0000

## §5 — CCS Visualizations

Rotliegend 7-panel: Location, Cross-section, Porosity, Permeability, Phi-K, Summary, Quality
NPV 7-panel: Cash flow, Cumulative, Discount sensitivity, Carbon price, Revenue, Cost, Metrics

## §6 — Verification

Location map included | Inverted Y-axis | All layers labeled | DPI<=150 | Images ls -lh | PDF pages verified | Footer+classification | Sources cited | Verdict in summary