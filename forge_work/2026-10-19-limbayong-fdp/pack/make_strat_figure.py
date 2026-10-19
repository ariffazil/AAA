#!/usr/bin/env python3
"""Tectonostratigraphic column, NW Sabah — schematic, after Tan & Lamy (1990) and Cullen et al. (2006)."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

PACK = Path("/root/AAA/forge_work/2026-10-19-limbayong-fdp/pack")
FIG = PACK / "fig"
PAL = dict(navy="#1F3A5F", steel="#4A6FA5", teal="#2E7D7B", amber="#C08A2E",
           red="#A32E2E", grey="#6B6B6B", ink="#1A1A1A", green="#2E7D32")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.6,
                     "figure.dpi": 300, "savefig.dpi": 300})
QA = []


def gate(fig, name):
    fig.canvas.draw()
    W, H = fig.canvas.get_width_height()
    boxes, labels = [], []
    for t in fig.axes[0].texts:
        if t.get_text().strip():
            boxes.append(t.get_window_extent(fig.canvas.get_renderer()))
            labels.append(t.get_text())
    out = over = 0
    for bb, lab in zip(boxes, labels):
        if bb.x0 < -2 or bb.y0 < -2 or bb.x1 > W + 2 or bb.y1 > H + 2:
            QA.append(f"{name}: outside -> {lab!r}"); out += 1
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            ix = max(0, min(a.x1, b.x1) - max(a.x0, b.x0))
            iy = max(0, min(a.y1, b.y1) - max(a.y0, b.y0))
            if ix > 3 and iy > 3 and ix * iy > 24:
                QA.append(f"{name}: overlap {labels[i]!r} / {labels[j]!r}"); over += 1
    return dict(figure=name, texts=len(boxes), outside=out, overlaps=over)


UNITS = [
    # name, top Ma, base Ma, fill, label, tectonic
    ("Stage IV\n(late Middle Miocene – Pliocene)", 0, 11.6, "#D9C79A",
     "shelf/slope clinoforms, deepwater fans\nincl. Kinarut fan (~10.6 Ma)", "progradation; fold belt grows"),
    ("Stage III\n(early Middle Miocene)", 11.6, 16.0, "#B9C6CF",
     "deep-marine clastics; imbrication begins", "collision; DRU"),
    ("Stages I–II\n(Paleogene – Early Miocene)", 16.0, 32.0, "#8FA6B8",
     "deep-marine clastics, accretionary prism", "subduction of SCS crust"),
]


def fig_strat():
    fig, ax = plt.subplots(figsize=(7.3, 3.35))
    x0, w = 0.0, 2.6
    for name, top, base, col, lith, tect in UNITS:
        ax.add_patch(Rectangle((x0, top), w, base - top, facecolor=col,
                               edgecolor="#6B6B6B", lw=0.6, zorder=2))
        ax.text(x0 + w / 2, (top + base) / 2, name, ha="center", va="center",
                fontsize=6.6, fontweight="bold", zorder=3)
        ax.text(x0 + w + 0.15, (top + base) / 2, lith, va="center", fontsize=6.3, zorder=3)
        ax.text(x0 + w + 3.35, (top + base) / 2, tect, va="center", fontsize=5.9,
                color=PAL["grey"], zorder=3)

    # reservoir marker
    ax.plot([x0, x0 + w], [10.6, 10.6], color=PAL["red"], lw=1.2, ls=(0, (2, 1.5)), zorder=6)
    ax.text(x0 + 0.08, 10.9, "Kinarut fan 10.6 Ma (analogue)", fontsize=5.5,
            color=PAL["red"], va="bottom", zorder=6)

    # unconformities
    for y, lab in [(11.6, "Deep Regional Unconformity"), (16.0, "")]:
        ax.plot([x0 - 0.08, x0 + w + 0.02], [y, y], color=PAL["red"], lw=1.0,
                ls=(0, (5, 2)), zorder=4)
        if lab:
            ax.text(x0 - 0.12, y + 0.5, lab, fontsize=5.6, color=PAL["red"],
                    ha="right", va="bottom", zorder=4)

    ax.set_ylim(32, -1)
    ax.set_xlim(-2.9, 8.9)
    ax.set_ylabel("Age  (Ma)")
    ax.set_yticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.grid(axis="y", alpha=0.2)

    fig.text(0.010, 0.012,
             "Schematic, after Tan & Lamy (1990, Bull. Geol. Soc. Malaysia 27) and Cullen et al. (2006, AAPG Search & Discovery #90052).\n"
             "Stage boundaries are approximate; the column is drawn to show order and environment, not thickness. "
             "Reservoir interval at Limbayong is not public — the Kinarut fan is the regional analogue, not a stated Limbayong reservoir.",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.085, right=0.996, top=0.97, bottom=0.20)
    p = FIG / "fig5_strat.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 5.5")
    plt.close(fig)
    return p, q


if __name__ == "__main__":
    p, q = fig_strat()
    print(p.name, p.stat().st_size, q)
    print("QA:", "clean" if not QA else QA)
