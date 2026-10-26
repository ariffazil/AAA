#!/usr/bin/env python3
"""Fig 5.6 / 5.7 — the two quantitative Earth arguments."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

PACK = Path("/root/AAA/forge_work/2026-10-19-limbayong-fdp/pack")
FIG = PACK / "fig"
PAL = dict(navy="#1F3A5F", steel="#4A6FA5", teal="#2E7D7B", amber="#C08A2E",
           red="#A32E2E", grey="#6B6B6B", ink="#1A1A1A", green="#2E7D32")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.0,
                     "figure.dpi": 300, "savefig.dpi": 300,
                     "axes.edgecolor": "#8A8A8A", "axes.linewidth": 0.6,
                     "axes.grid": True, "grid.color": "#DDDDDD", "grid.linewidth": 0.35,
                     "xtick.color": PAL["grey"], "ytick.color": PAL["grey"]})
QA = []


def gate(fig, name):
    fig.canvas.draw()
    W, H = fig.canvas.get_width_height()
    boxes, labels = [], []
    for ax in fig.axes:
        for t in ax.texts:
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


def fig_seal():
    """A: what a 250 m capillary seal does to a km-scale trap. B: per-well EUR vs analogue."""
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.3, 3.0),
                                  gridspec_kw={"width_ratios": [1.15, 1]})

    # ── A ────────────────────────────────────────────────
    # structural closure 0-700 m; fill is min(closure, seal capacity)
    closure = np.linspace(0, 700, 400)
    for cap, lab, c, ls in [(250, "P50 capillary seal, deepwater turbidite (250 m)", PAL["navy"], "-"),
                            (30, "P50 capillary seal, deltaic (30 m)", PAL["amber"], "-"),
                            (700, "if seal capacity were unlimited", PAL["grey"], (0, (4, 2)))]:
        fill = np.minimum(closure, cap)
        ax.plot(closure, fill, color=c, lw=1.7, ls=ls, label=lab)
    ax.fill_between(closure, np.minimum(closure, 250), closure,
                    color=PAL["red"], alpha=0.10, zorder=0)
    ax.text(360, 430, "gas that cannot\nbe held", fontsize=6.2, color=PAL["red"])
    ax.axvline(250, color=PAL["navy"], lw=0.8, ls=":")
    ax.set_xlabel("Structural closure available  (m)")
    ax.set_ylabel("Column that can be retained  (m)")
    ax.set_xlim(0, 700); ax.set_ylim(0, 700)
    ax.legend(frameon=False, fontsize=5.6, loc="lower right")
    ax.set_title("A — the trap is not the container", fontsize=7.3, loc="left")

    # ── B ────────────────────────────────────────────────
    rec = 139.5
    wells = np.arange(4, 21)
    ax2.axhspan(20, 100, color=PAL["teal"], alpha=0.12, zorder=0)
    ax2.text(20.5, 96, "Bonga analogue band\n20–100 MMstb/well", fontsize=5.5,
             color=PAL["teal"], ha="right", va="top")
    ax2.plot(wells, rec / wells, color=PAL["navy"], lw=1.7)
    for w, c in [(10, PAL["red"]), (15, PAL["amber"])]:
        ax2.plot([w], [rec / w], "o", ms=5.5, color=c, mec="white", mew=0.9, zorder=6)
        ax2.annotate(f"{w} wells\n{rec/w:.1f} MMbbl/well", xy=(w, rec / w),
                     xytext=(w - 3.2, rec / w + 22), fontsize=5.8, color=c,
                     arrowprops=dict(arrowstyle="-", color=c, lw=0.6))
    ax2.set_xlabel("Number of development wells")
    ax2.set_ylabel("Per-well ultimate  (MMbbl)")
    ax2.set_xlim(4, 20); ax2.set_ylim(0, 120)
    ax2.set_title("B — per-well volume is below the analogue floor", fontsize=7.3, loc="left")

    fig.text(0.010, 0.010,
             "A: DERIVED from L-59 and L-60 — retained column = min(closure, capillary seal capacity). "
             "B: 139.5 MMbbl (L-29) divided by well count, against 20–100 MMstb/well for Bonga (L-61).\n"
             "Read together: the field is not short of wells at 10, it is short of connected volume per well. "
             "Neither panel is a forecast; both bound what the rock can do.",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.072, right=0.987, top=0.905, bottom=0.235, wspace=0.30)
    p = FIG / "fig5_seal.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 5.6")
    plt.close(fig)
    return p, q


def fig_thermal():
    """Temperature vs depth for the two published gradients, with the quartz-cement threshold."""
    fig, ax = plt.subplots(figsize=(7.3, 2.9))
    sub = np.linspace(0, 4000, 300)          # metres below mudline
    seabed = 3.0
    for grad, lab, c, ls in [(66.5, "66.5 °C/km — deepwater belt, along strike (L-64)", PAL["red"], "-"),
                             (31.5, "29–34 °C/km — Baram and Sabah shelf (L-65)", PAL["steel"], "-")]:
        ax.plot(sub / 1000, seabed + grad * sub / 1000, color=c, lw=1.7, ls=ls, label=lab)
    ax.axhline(140, color=PAL["amber"], lw=1.2, ls=(0, (5, 2)))
    ax.text(3.92, 145, "140 °C — onset of quartz cementation", fontsize=6.0,
            color=PAL["amber"], ha="right")
    ax.axvspan(2.0, 3.0, color=PAL["grey"], alpha=0.10, zorder=0)
    ax.text(2.05, 268, "plausible Limbayong\nreservoir depth", fontsize=5.9, color=PAL["grey"])
    for g, c in [(66.5, PAL["red"]), (31.5, PAL["steel"])]:
        for d in (2.0, 3.0):
            t = seabed + g * d
            ax.plot([d], [t], "o", ms=4, color=c, mec="white", mew=0.8, zorder=6)
    ax.set_xlabel("Depth below mudline  (km)")
    ax.set_ylabel("Temperature  (°C)")
    ax.set_xlim(0, 4); ax.set_ylim(0, 300)
    ax.legend(frameon=False, fontsize=5.9, loc="lower right")
    fig.text(0.010, 0.010,
             "DERIVED: T = 3 °C (seabed) + gradient × depth, per L-64, L-65, L-69. The two published gradients "
             "bracket a 100 °C spread at reservoir depth.\nOn the hot gradient the reservoir passes the quartz-cementation "
             "threshold; on the shelf gradient it does not. This is a genuine, unwelcome contradiction — C-10.",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.080, right=0.987, top=0.955, bottom=0.235)
    p = FIG / "fig5_thermal.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 5.7")
    plt.close(fig)
    return p, q


if __name__ == "__main__":
    res = []
    for fn in (fig_seal, fig_thermal):
        p, q = fn()
        res.append(q)
        print(f"{p.name:22s} {p.stat().st_size:>8d}  texts={q['texts']:3d} "
              f"outside={q['outside']} overlaps={q['overlaps']}")
    json.dump(res, open(PACK / "figure_qa_earth2.json", "w"), indent=2)
    print("QA:", "clean" if not QA else QA)
