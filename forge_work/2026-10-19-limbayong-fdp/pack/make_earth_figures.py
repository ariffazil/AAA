#!/usr/bin/env python3
"""Earth figures for Part 5 — real bathymetry, real coordinates, schematic structure."""
import json, math
from pathlib import Path
import numpy as np
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import LightSource, LinearSegmentedColormap
from matplotlib.patches import Polygon, FancyArrow
import cartopy.crs as ccrs
import cartopy.feature as cfeature

PACK = Path("/root/AAA/forge_work/2026-10-19-limbayong-fdp/pack")
FIG = PACK / "fig"
L = {r["id"]: r for r in json.load(open(PACK / "ledger.json"))["rows"]}

PAL = dict(navy="#1F3A5F", steel="#4A6FA5", teal="#2E7D7B", amber="#C08A2E",
           red="#A32E2E", grey="#6B6B6B", ink="#1A1A1A", green="#2E7D32")
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8.0,
    "axes.edgecolor": "#8A8A8A", "axes.linewidth": 0.6,
    "axes.labelcolor": PAL["ink"], "text.color": PAL["ink"],
    "xtick.color": PAL["grey"], "ytick.color": PAL["grey"],
    "figure.dpi": 300, "savefig.dpi": 300,
    "axes.grid": True, "grid.color": "#DDDDDD", "grid.linewidth": 0.35,
})

QA = []


def gate(fig, name):
    fig.canvas.draw()
    W, H = fig.canvas.get_width_height()
    boxes, labels = [], []
    for ax in fig.axes:
        for t in ax.texts:
            lab = t.get_text()
            if not lab.strip():
                continue
            boxes.append(t.get_window_extent(fig.canvas.get_renderer()))
            labels.append(lab)
    out = over = 0
    for bb, lab in zip(boxes, labels):
        if bb.x0 < -2 or bb.y0 < -2 or bb.x1 > W + 2 or bb.y1 > H + 2:
            QA.append(f"{name}: outside canvas -> {lab!r}")
            out += 1
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            ix = max(0, min(a.x1, b.x1) - max(a.x0, b.x0))
            iy = max(0, min(a.y1, b.y1) - max(a.y0, b.y0))
            if ix > 3 and iy > 3 and ix * iy > 24:
                QA.append(f"{name}: overlap {labels[i]!r} / {labels[j]!r}")
                over += 1
    return dict(figure=name, texts=len(boxes), outside=out, overlaps=over)


# ── 5.1 tectonic setting ─────────────────────────────────────────────────
def fig_tectonic():
    fig = plt.figure(figsize=(7.3, 4.6))
    proj = ccrs.PlateCarree()
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_extent([104, 124, -3, 16], crs=proj)
    ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor="#EFEDE6",
                   edgecolor="#8C8C8C", linewidth=0.4, zorder=2)
    ax.add_feature(cfeature.OCEAN.with_scale("50m"), facecolor="#F3F8FA", zorder=0)

    # approximate Dangerous Grounds / Reed Bank outline (schematic, labelled)
    dg = [(109.5, 12.5), (113.5, 13.6), (116.5, 13.2), (118.5, 12.0),
          (118.0, 9.6), (116.0, 8.4), (113.2, 9.2), (110.0, 10.4)]
    ax.add_patch(Polygon(dg, closed=True, transform=proj, facecolor="#4A6FA5",
                         alpha=0.10, edgecolor="#4A6FA5", lw=0.8,
                         linestyle=(0, (4, 2)), zorder=3))
    ax.text(114.3, 12.6, "DANGEROUS GROUNDS\n(rifted continental block)",
            fontsize=6.2, color="#3A5A85", ha="center", zorder=5)

    # schematic thrust front and belt
    front = [(109.8, 5.6), (111.6, 5.9), (113.4, 6.0), (115.0, 6.3),
             (116.6, 6.9), (117.6, 7.6)]
    ax.plot([p[0] for p in front], [p[1] for p in front], color=PAL["red"],
            lw=1.6, transform=proj, zorder=8)
    ax.text(117.4, 8.0, "deformation front", fontsize=6.0, color=PAL["red"], zorder=9)

    # convergence arrows
    for x, y in [(112.6, 11.2), (114.8, 11.6), (117.0, 10.8)]:
        ax.annotate("", xy=(x, y - 1.5), xytext=(x, y), transform=proj,
                    arrowprops=dict(arrowstyle="-|>", color=PAL["navy"], lw=1.0), zorder=9)
    ax.text(120.0, 12.9, "convergence since ~16 Ma", fontsize=6.0, color=PAL["navy"], zorder=9)

    ax.plot(114.5097, 5.888, "o", ms=6.5, mfc=PAL["red"], mec="white", mew=1.0,
            transform=proj, zorder=10)
    ax.annotate("LIMBAYONG", xy=(114.5097, 5.888), xytext=(115.9, 4.6),
                transform=proj, fontsize=7, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=PAL["red"], lw=0.7), zorder=11)

    for nm, x, y in [("BORNEO", 114.4, 1.2), ("PALAWAN", 118.6, 9.6),
                     ("SULU SEA", 120.6, 6.6), ("SOUTH CHINA SEA", 110.0, 8.0),
                     ("SUNDA SHELF", 106.5, 1.5)]:
        ax.text(x, y, nm, fontsize=6.4, color="#9A9A9A", style="italic",
                ha="center", zorder=6)

    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="#D5D5D5",
                      x_inline=False, y_inline=False)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 5.8}
    gl.ylabel_style = {"size": 5.8}
    gl.xlocator = mtick.MultipleLocator(5)
    gl.ylocator = mtick.MultipleLocator(5)

    fig.text(0.010, 0.010,
             "Plate framework after published NW Borneo syntheses (see Appendix E). Coastline: Natural Earth 1:50m. "
             "Dangerous Grounds outline and deformation front are schematic, drawn for orientation only —\n"
             "they are not surveyed boundaries. Limbayong position: GEM field coordinate, exact to 0.001°.",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.058, right=0.985, top=0.978, bottom=0.105)
    p = FIG / "fig5_tectonic.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 5.1")
    plt.close(fig)
    return p, q


# ── 5.2 bathymetry ───────────────────────────────────────────────────────
def fig_bathy():
    P = "/root/.hermes/cache/scratch/etopo_zoom.tif"
    with rasterio.open(P) as ds:
        z = ds.read(1).astype("float32")
        b = ds.bounds
    ext = (b.left, b.right, b.bottom, b.top)
    cmap = LinearSegmentedColormap.from_list("bathy", [
        (0.00, "#0A2742"), (0.22, "#134A70"), (0.46, "#2E7FA3"),
        (0.66, "#7CB7CB"), (0.82, "#BBDCE4"), (0.92, "#E4EFF1"), (1.0, "#F6F8F6")])
    ls = LightSource(azdeg=318, altdeg=38)
    rgb = ls.shade(z, cmap=cmap, blend_mode="overlay", vert_exag=0.004,
                   dx=60, dy=60, vmin=-2300, vmax=-150)

    fig, ax = plt.subplots(figsize=(7.3, 6.2))
    ax.imshow(rgb, extent=ext, origin="upper")
    ax.contour(np.linspace(ext[0], ext[1], z.shape[1]),
               np.linspace(ext[3], ext[2], z.shape[0]), z,
               levels=[-2000, -1750, -1500, -1250, -1000, -900, -800, -700, -600],
               colors="#FFFFFF", linewidths=0.35, alpha=0.22)

    ax.plot([114.5097], [5.888], "o", ms=8, mfc=PAL["red"], mec="white", mew=1.2, zorder=12)
    ax.annotate("LIMBAYONG\n994 m (DEM)", xy=(114.5097, 5.888), xytext=(114.72, 5.99),
                fontsize=7.2, fontweight="bold", color=PAL["red"], zorder=13,
                arrowprops=dict(arrowstyle="-", color=PAL["red"], lw=0.8))

    for nm, x, y in [("Kikeh", 114.296, 5.875), ("Gumusut-Kakap", 114.4116, 5.8001)]:
        ax.plot(x, y, "s", ms=4.6, mfc=PAL["amber"], mec="white", mew=0.8, zorder=12)
        ax.annotate(nm, (x, y), (x - 0.02, y - 0.075), fontsize=6.4, color=PAL["amber"],
                    ha="center", zorder=13)

    # ridge annotation, aligned with the NE-SW grain
    ax.annotate("", xy=(113.86, 6.28), xytext=(115.30, 5.34),
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.4, alpha=0.75), zorder=11)
    ax.text(113.80, 6.34, "NE–SW structural grain\n(thrust-cored ridges)", fontsize=6.2,
            color="white", alpha=0.9, zorder=11)

    # shelf break line (approximate -200 m contour trace)
    ax.plot([114.95, 115.30], [5.20, 5.62], color=PAL["ink"], lw=1.2, ls=(0, (5, 2)), zorder=11)
    ax.text(115.02, 5.30, "shelf break", fontsize=6.0, color=PAL["ink"], rotation=38, zorder=11)

    ax.set_xlim(ext[0], ext[1])
    ax.set_ylim(ext[2], ext[3])
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    fig.text(0.010, 0.010,
             "Shaded relief from NOAA/ETOPO global DEM, ~450 m cells, resampled for print. Depth at Limbayong read "
             "directly from the grid: 994 m — consistent with the 900–1,200 m reported depth (L-16).\n"
             "Field positions: GEM field coordinates; they may represent block centroids, not well locations. "
             "Ridges are real topography; their structural interpretation is from published seismic, not from this DEM.",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.085, right=0.985, top=0.985, bottom=0.115)
    p = FIG / "fig5_bathy.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 5.2")
    plt.close(fig)
    return p, q


# ── 5.3 bathymetric section ──────────────────────────────────────────────
def fig_section():
    d, zz = np.load("/root/.hermes/cache/scratch/transect.npy")
    fig, ax = plt.subplots(figsize=(7.3, 3.2))
    ax.fill_between(d, zz, 60, color="#BFD7E2", alpha=0.65, zorder=2)
    ax.plot(d, zz, color=PAL["navy"], lw=1.4, zorder=3)
    ax.axhline(0, color=PAL["ink"], lw=0.8)

    # province boundaries read off the transect
    for km, lab in [(144, "shelf break\n−200 m"), (196, "−2,000 m")]:
        ax.axvline(km, color=PAL["grey"], lw=0.8, ls=(0, (3, 2)))
        ax.text(km - 2, -2600, lab, fontsize=5.8, color=PAL["grey"], va="bottom", ha="right")

    for x0, x1, lab, y in [(0, 144, "SHELF\nBaram–Champion delta system", 120),
                           (144, 196, "SLOPE AND FOLD–THRUST BELT", 120),
                           (196, 283, "DEEP BASIN", 120)]:
        ax.text((x0 + x1) / 2, y, lab, fontsize=6.2, color=PAL["navy"],
                ha="center", va="top", fontweight="bold")

    ax.annotate("Limbayong\n(994 m)", xy=(158, -994), xytext=(104, -1750),
                fontsize=6.6, color=PAL["red"], fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=PAL["red"], lw=0.9))
    ax.plot([158], [-994], "o", ms=6, mfc=PAL["red"], mec="white", mew=1.0, zorder=8)

    ax.set_xlabel("Distance along section A–A′  (km)")
    ax.set_ylabel("Elevation  (m)")
    ax.set_xlim(0, 283)
    ax.set_ylim(-2900, 260)
    ax.grid(alpha=0.3)
    fig.text(0.010, 0.010,
             "Section A–A′ traced on the real DEM from 115.55°E 4.95°N to 113.55°E 6.55°N, i.e. from the shelf, "
             "across the slope and fold belt, into the basin.\nVertical exaggeration ≈ 32× at this aspect. "
             "The 1,800 m of relief between the shelf break and the basin is real; the ridges between them are "
             "the folds the fields sit on.",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.085, right=0.985, top=0.965, bottom=0.225)
    p = FIG / "fig5_section.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 5.3")
    plt.close(fig)
    return p, q


if __name__ == "__main__":
    res = []
    for fn in (fig_tectonic, fig_bathy, fig_section):
        p, q = fn()
        res.append(q)
        print(f"{p.name:26s} {p.stat().st_size:>8d}  texts={q['texts']:3d} "
              f"outside={q['outside']} overlaps={q['overlaps']}")
    json.dump(res, open(PACK / "figure_qa_earth.json", "w"), indent=2)
    print()
    print("QA:", "clean" if not QA else QA)
