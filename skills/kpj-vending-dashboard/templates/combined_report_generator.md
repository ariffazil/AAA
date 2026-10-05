# Combined-Report Generator Template

Use `/tmp/sep2026_combined_4sites_v2_gen.py` as the working reference — it has the validated layout (1x4 vertical strip, figure-level border, 18pt site labels, 14pt tile values) that survived Izzu's review.

## Skeleton

```python
SITES = [
    {
        "code": "KPJXX",           # 4-letter site code
        "name": "KPJ Xxxxx",       # Display name (short — Izzu renames long ones)
        "xlsx": "/path/to/sep2026_kpjxx.xlsx",
        "gp": 1234.56,            # Hardcoded from latest individual site report
    },
    # add 2-4 sites
]
```

## Layout (4-site, validated)

| Layer | Y position | Notes |
|---|---|---|
| Suptitle | y=0.98, 22pt bold | Title format: `"<Month> <Year> · Combined"` — do NOT list site names |
| Site label band | y=0.92, 0.045 high, 18pt bold | Dark-blue 2.5pt border, light-blue (#d0d9e6) bg |
| 6 KPI tiles | y=0.87 down, each 0.13 high | White bg, dark-blue 1.8pt borders |
| Combined TOTAL footer | y=0.005-0.02 | Above page bottom, not overlapping last row of tiles |

## KPI tile dimensions (4-site strip)

- Strip width: `strip_w = 0.225` (each site ~22.5% of page width)
- Gap: `0.005`
- Site label: `0.04 + s_idx * (strip_w + gap)` x position
- Tile values: 14pt (slightly smaller than single-site 18pt because 4 columns)

## Outer box border (critical)

```python
from matplotlib.patches import Rectangle
rect = Rectangle(
    (x0 - 0.003, 0.02), strip_w + 0.006, 0.955,
    fill=False, edgecolor="#1a3a5c", linewidth=2.0,
    transform=fig.transFigure, zorder=10,  # <- figure-level, NOT axes
)
fig.add_artist(rect)
```

Drawing the border at axes level (without `transform=fig.transFigure`) gets clipped by the axes bounding box and produces broken/invisible lines.

## GP column (per site)

The combined report does NOT recompute GP. It uses the value from the latest individual site report. If rates change, re-run individual sites first, then re-run the combined.

## Pages layout (6 pages for 4 sites)

1. Header + 4 site strips + Combined TOTAL footer
2. Revenue + Avg/TX bar charts
3. GP + Margin bar charts
4. Daily Revenue Trend (line, 4 series overlaid)
5. Payment Method Split (4 horizontal bars, one per site)
6. Per-Site Summary Table (Txns / Revenue / GP / Margin / Avg / Days / Best Day)
```

## Things that broke and how to fix

| Symptom | Cause | Fix |
|---|---|---|
| 4-site 2x2 grid unreadable | Each tile 145pt×75pt, fonts can't fit | Use 1x4 vertical strip only |
| Site label overlaps with top row of tiles | `y_top - s_idx * 0.32` was too tight | Use `0.34` step and add 0.045 buffer for label band |
| Box border broken or invisible | Drawn at axes level | Use `transform=fig.transFigure, zorder=10` |
| Footer overlaps last row of tiles | Footer at y=0.04 with last row ending y=0.025 | Move footer to y=0.005, reduce height to 0.035 |
| GP values in combined report stale | Rates changed in single site, combined not regenerated | Always re-run combined after single site rate changes |

## What NOT to put in the title

- ❌ `(KPJAP + KPJD + KPJR + KPJT)` — Izzu stripped this
- ❌ `4-Site Combined` — Izzu stripped this too
- ❌ "Monthly Report" or "Performance Summary" — Izzu terse, prefers just the period + "Combined"

✅ `"September 2026 · Combined"` — the pattern that survived
