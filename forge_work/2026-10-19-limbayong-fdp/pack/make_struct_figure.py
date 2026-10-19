#!/usr/bin/env python3
"""Schematic structural cross-section of a thrust-cored anticline, NW Borneo style.

Explicitly schematic: geometry after published descriptions of the deepwater
fold-thrust belt, not digitised from any seismic line.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch

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
            QA.append(f"{name}: outside -> {lab!r}")
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


def fig_struct():
    fig, ax = plt.subplots(figsize=(7.3, 3.9))
    x = np.linspace(0, 30, 400)

    # sea level and seafloor
    ax.axhline(0, color=PAL["ink"], lw=0.8)
    seafloor = -1.0 - 0.02 * x
    ax.fill_between(x, seafloor, 0.35, color="#CFE3EC", alpha=0.75, zorder=1)
    ax.plot(x, seafloor, color=PAL["ink"], lw=1.0, zorder=3)

    # fold geometry: two thrust-cored anticlines
    def fold(x, xc, amp, width):
        return amp * np.exp(-((x - xc) / width) ** 2)

    top_res = -4.6 + 1.9 * fold(x, 12, 1.0, 3.4) + 0.9 * fold(x, 23.5, 1.0, 2.6)
    base_res = top_res - 1.1

    # overburden above reservoir
    ax.fill_between(x, top_res, seafloor, color="#DCD8CB", zorder=2)
    # reservoir body
    ax.fill_between(x, base_res, top_res, color="#E8D9A8", zorder=2)
    ax.plot(x, top_res, color=PAL["ink"], lw=0.7, zorder=4)
    ax.plot(x, base_res, color=PAL["ink"], lw=0.7, zorder=4)

    # hydrocarbons in the left (main) closure
    left = (x > 7.2) & (x < 17.0)
    gas_top = top_res.copy()
    gas_base = np.maximum(top_res - 0.95, base_res)
    ax.fill_between(x[left], gas_base[left], gas_top[left], color="#C0453B", alpha=0.85, zorder=5)
    oil_top = gas_base.copy()
    oil_base = np.maximum(gas_base - 0.35, base_res)
    ax.fill_between(x[left], oil_base[left], oil_top[left], color="#5C8A3C", alpha=0.9, zorder=5)
    ax.fill_between(x[left], base_res[left], oil_base[left], color="#6FA8C7", alpha=0.7, zorder=5)

    # right closure: gas only
    right = (x > 21.0) & (x < 26.0)
    ax.fill_between(x[right], np.maximum(top_res[right] - 0.8, base_res[right]),
                    top_res[right], color="#C0453B", alpha=0.7, zorder=5)

    # detachment
    det = -9.4 + 0.35 * np.sin(x / 6)
    ax.plot(x, det, color=PAL["red"], lw=2.0, zorder=6)
    ax.fill_between(x, det, det - 0.9, color="#8B6F9E", alpha=0.35, zorder=1)
    ax.text(1.0, det[0] - 1.25, "detachment in overpressured shale", fontsize=6.2,
            color=PAL["red"])

    # thrust splays
    for x0, x1 in [(7.4, 6.0), (17.0, 18.6), (21.0, 20.0)]:
        ax.plot([x0, x1], [top_res[np.argmin(abs(x - x0))], det[np.argmin(abs(x - x1))]],
                color=PAL["ink"], lw=1.4, ls=(0, (6, 2)), zorder=7)

    # wells
    for wx in [9.5, 12.0, 15.0, 22.5, 24.5]:
        ax.plot([wx, wx], [seafloor[np.argmin(abs(x - wx))], base_res[np.argmin(abs(x - wx))] - 0.15],
                color=PAL["navy"], lw=1.0, zorder=8)
        ax.plot(wx, seafloor[np.argmin(abs(x - wx))], "v", ms=3.2, color=PAL["navy"], zorder=8)

    # gas chimney at crest (breach)
    ax.annotate("", xy=(12, seafloor[np.argmin(abs(x - 12))] + 0.1), xytext=(12, -4.6),
                arrowprops=dict(arrowstyle="-|>", color=PAL["red"], lw=1.1, ls=(0, (3, 2))), zorder=9)
    ax.text(12.4, -2.2, "crestal faulting /\ngas chimney", fontsize=5.9, color=PAL["red"])

    # labels
    ax.text(12, -0.45, "sea level", fontsize=5.8, color=PAL["ink"])
    ax.text(0.6, -2.6, "water column\n≈1,000 m", fontsize=6.0, color="#3A5A85")
    ax.text(4.2, -3.9, "overburden / top seal", fontsize=6.0, color="#6B6355")
    ax.text(24.6, -6.3, "second closure\n(gas-bearing)", fontsize=5.9, color=PAL["ink"])
    ax.text(10.4, -5.9, "oil rim", fontsize=6.0, color="#3E5B22")
    ax.text(11.2, -6.9, "water", fontsize=6.0, color="#2C5C78")

    ax.set_xlabel("Distance across structure  (km) — schematic")
    ax.set_ylabel("Depth  (km below sea level)")
    ax.set_xlim(0, 30)
    ax.set_ylim(-11.0, 0.35)
    ax.set_yticks([0, -2, -4, -6, -8, -10])
    ax.grid(alpha=0.15)

    ax.text(0.4, 0.2, "A", fontsize=8, fontweight="bold")
    ax.text(29.5, 0.2, "A′", fontsize=8, fontweight="bold", ha="right")

    fig.text(0.010, 0.012,
             "SCHEMATIC. Geometry after published descriptions of thrust-cored anticlines in the NW Borneo "
             "deepwater fold-thrust belt; it is not digitised from any seismic line, and no dimension is a measurement.\n"
             "The point of the figure is topology, not size: one structure, several fault-bounded compartments, "
             "a gas column over an oil rim, and a crest that leaks.",
             fontsize=5.1, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.082, right=0.986, top=0.975, bottom=0.20)
    pth = FIG / "fig5_structure.png"
    fig.savefig(pth, dpi=300)
    q = gate(fig, "Fig 5.4")
    plt.close(fig)
    return pth, q


if __name__ == "__main__":
    p, q = fig_struct()
    print(p.name, p.stat().st_size, q)
    print("QA:", "clean" if not QA else QA)
