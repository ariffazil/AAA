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

## §4 — Geological Colors

Water=#4A90D9 | Overburden=#DEB887 | Sandstone=#E8A838 | Shale=#006400
Caprock=#8B0000 | Basement=#2F4F4F | CO2=#FF4500 | Well=#FFD700 | Fault=#FF0000

## §5 — CCS Visualizations

Rotliegend 7-panel: Location, Cross-section, Porosity, Permeability, Phi-K, Summary, Quality
NPV 7-panel: Cash flow, Cumulative, Discount sensitivity, Carbon price, Revenue, Cost, Metrics

## §6 — Verification

Location map included | Inverted Y-axis | All layers labeled | DPI<=150 | Images ls -lh | PDF pages verified | Footer+classification | Sources cited | Verdict in summary