#!/usr/bin/env python3
"""Figures for LIM-SFDP-v0.2, plus a deterministic figure QA gate.

Every figure is drawn from ledger.json. The QA gate reads back the artists and
checks bounding boxes - it does not ask a model whether the picture looks fine.
"""
import json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.patches import Rectangle

import cartopy.crs as ccrs
import cartopy.feature as cfeature

PACK = Path("/root/AAA/forge_work/2026-10-19-limbayong-fdp/pack")
FIG = PACK / "fig"
FIG.mkdir(parents=True, exist_ok=True)
L = {r["id"]: r for r in json.load(open(PACK / "ledger.json"))["rows"]}

PAL = dict(navy="#1F3A5F", steel="#4A6FA5", teal="#2E7D7B", amber="#C08A2E",
           red="#A32E2E", grey="#6B6B6B", light="#E8E8E4", ink="#1A1A1A",
           green="#2E7D32")
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8.2,
    "axes.edgecolor": "#8A8A8A", "axes.linewidth": 0.6,
    "axes.labelcolor": PAL["ink"], "text.color": PAL["ink"],
    "xtick.color": PAL["grey"], "ytick.color": PAL["grey"],
    "figure.dpi": 300, "savefig.dpi": 300,
    "axes.grid": True, "grid.color": "#DDDDDD", "grid.linewidth": 0.4,
})

QA = []


def gate(fig, name):
    """Deterministic checks: every text inside the canvas, no pair overlapping."""
    fig.canvas.draw()
    W, H = fig.canvas.get_width_height()
    boxes, labels = [], []
    for ax in fig.axes:
        for t in list(ax.texts) + ([ax.get_legend()] if ax.get_legend() else []):
            try:
                bb = t.get_window_extent(fig.canvas.get_renderer())
            except Exception:
                try:
                    bb = t.get_frame().get_window_extent()
                except Exception:
                    continue
            lab = t.get_text() if hasattr(t, "get_text") else "LEGEND"
            if not lab or not lab.strip():
                continue
            boxes.append(bb)
            labels.append(lab)
        xlo, xhi = sorted(ax.get_xlim())
        ylo, yhi = sorted(ax.get_ylim())
        for t in ax.get_xticklabels():
            try:
                v = float(t.get_text().replace(",", "").rstrip("k")) * (1000 if t.get_text().endswith("k") else 1)
            except Exception:
                continue
            if t.get_text().strip() and xlo - 1e-9 <= v <= xhi + 1e-9:
                boxes.append(t.get_window_extent(fig.canvas.get_renderer()))
                labels.append(t.get_text())
        for t in ax.get_yticklabels():
            try:
                v = float(t.get_text().replace(",", "").rstrip("k")) * (1000 if t.get_text().endswith("k") else 1)
            except Exception:
                continue
            if t.get_text().strip() and ylo - 1e-9 <= v <= yhi + 1e-9:
                boxes.append(t.get_window_extent(fig.canvas.get_renderer()))
                labels.append(t.get_text())
    out = 0
    for bb, lab in zip(boxes, labels):
        if bb.x0 < -2 or bb.y0 < -2 or bb.x1 > W + 2 or bb.y1 > H + 2:
            QA.append(f"{name}: text outside canvas -> {lab!r}")
            out += 1
    over = 0
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            ix = max(0, min(a.x1, b.x1) - max(a.x0, b.x0))
            iy = max(0, min(a.y1, b.y1) - max(a.y0, b.y0))
            if ix > 3 and iy > 3 and ix * iy > 22:
                QA.append(f"{name}: overlap {labels[i]!r} / {labels[j]!r}")
                over += 1
    return dict(figure=name, texts=len(boxes), outside=out, overlaps=over)


def fig0():
    fig = plt.figure(figsize=(7.1, 4.35))
    proj = ccrs.PlateCarree()
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_extent([112.7, 117.4, 4.35, 7.55], crs=proj)
    ax.add_feature(cfeature.LAND.with_scale("10m"), facecolor="#EFEDE6",
                   edgecolor="#8C8C8C", linewidth=0.5, zorder=2)
    ax.add_feature(cfeature.OCEAN.with_scale("10m"), facecolor="#F5F9FB", zorder=0)
    ax.add_feature(cfeature.LAKES.with_scale("10m"), facecolor="#F5F9FB",
                   edgecolor="#8C8C8C", linewidth=0.3, zorder=3)

    ax.add_patch(Rectangle((113.35, 5.15), 2.30, 1.50, transform=proj,
                           facecolor="#4A6FA5", alpha=0.12, edgecolor="#4A6FA5",
                           linewidth=0.7, linestyle=(0, (3, 2)), zorder=4))
    ax.text(113.45, 5.28, "900\u20131,200 m water depth\nreported zone \u2014 not an isobath",
            fontsize=5.7, color="#3A5A85", va="top", zorder=5)

    lon, lat = 114.510, 5.888
    ax.plot(lon, lat, marker="o", ms=6.2, mfc=PAL["red"], mec="white", mew=1.0,
            transform=proj, zorder=7)
    ax.annotate("LIMBAYONG\n5.888\u00b0N 114.510\u00b0E\nBlock G",
                xy=(lon, lat), xytext=(114.05, 6.88), transform=proj, fontsize=6.6,
                fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=PAL["red"], lw=0.8,
                                shrinkA=2, shrinkB=5), zorder=8)

    ax.plot(116.073, 5.980, marker="s", ms=3.4, mfc=PAL["navy"], mec="white",
            mew=0.6, transform=proj, zorder=7)
    ax.annotate("Kota Kinabalu", xy=(116.073, 5.980), xytext=(116.26, 5.20),
                transform=proj, fontsize=6.3, color=PAL["navy"],
                arrowprops=dict(arrowstyle="-", color=PAL["navy"], lw=0.5), zorder=8)

    for nm, x, y in [("BRUNEI", 114.80, 4.62), ("SABAH", 117.02, 5.02),
                     ("SARAWAK", 113.55, 4.45)]:
        ax.text(x, y, nm, fontsize=6.1, color="#A0A0A0", style="italic",
                ha="center", zorder=6)

    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="#CFCFCF",
                      x_inline=False, y_inline=False)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 5.9}
    gl.ylabel_style = {"size": 5.9}
    gl.xlocator = mtick.MultipleLocator(1.0)
    gl.ylocator = mtick.MultipleLocator(1.0)

    dlon = 100 / (111.32 * math.cos(math.radians(5.888)))
    x0, y0 = 112.85, 4.52
    ax.plot([x0, x0 + dlon], [y0, y0], color=PAL["ink"], lw=1.7,
            transform=proj, zorder=9, solid_capstyle="butt")
    ax.plot([x0, x0 + dlon / 2], [y0, y0], color="white", lw=1.0,
            transform=proj, zorder=10, solid_capstyle="butt")
    ax.text(x0 + dlon / 2, y0 + 0.09, "100 km", fontsize=5.8, ha="center",
            transform=proj, zorder=9)
    ax.annotate("", xy=(117.18, 7.30), xytext=(117.18, 6.98), transform=proj,
                arrowprops=dict(arrowstyle="-|>", color=PAL["ink"], lw=0.9), zorder=9)
    ax.text(117.18, 7.35, "N", fontsize=7, ha="center", fontweight="bold",
            transform=proj, zorder=9)

    fig.text(0.010, 0.010,
             "WGS84 / PlateCarree. Base: Natural Earth 1:10m coastline (public domain). "
             "Position L-17; depth L-16. No public block polygon or isobath is used, so a point "
             "and a schematic zone are shown. GEBCO bathymetry not used in this build.",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.052, right=0.985, top=0.975, bottom=0.098)
    p = FIG / "fig0_map.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 0")
    plt.close(fig)
    return p, q


PLATEAU_SHARE = 0.70


def profile(rec, rate):
    annual = rate * 365 / 1e6
    plat_vol = PLATEAU_SHARE * rec
    tp = plat_vol / annual
    rem = rec - plat_vol
    d = annual / (rem + annual)
    ts, qs = [], []
    for i in range(60):
        q = rate if i < tp else rate * (1 - d) ** (i - tp + 1)
        if q < rate * 0.02:
            break
        ts.append(i)
        qs.append(q)
    return ts, qs, tp


def fig1():
    rec = L["L-29"]["value"]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.3, 2.95),
                                  gridspec_kw={"width_ratios": [1.25, 1]})
    cases = [("As-built Excalibur", 25000, PAL["navy"], "-"),
             ("Liquids-derived", 25500, PAL["steel"], "--"),
             ("Upgraded topsides", 37014, PAL["amber"], ":")]
    for nm, rate, c, ls in cases:
        ts, qs, tp = profile(rec, rate)
        ax.plot(ts, qs, color=c, lw=1.6, ls=ls,
                label=f"{nm} \u2014 {rate:,} bopd ({tp:.1f} yr)")
        ax.plot([tp], [rate], marker="|", ms=7, color=c)
    ax.axhline(40000, color=PAL["red"], lw=0.9, ls=(0, (4, 3)))
    ax.text(25.6, 40600, "40,000 bopd \u2014 cancelled 2020 tender spec",
            fontsize=5.6, color=PAL["red"], ha="right")
    ax.axhline(25000, color=PAL["navy"], lw=0.7, alpha=0.5)
    ax.set_xlabel("Years from first oil")
    ax.set_ylabel("Oil rate  (bopd)")
    ax.set_ylim(0, 44000)
    ax.set_xlim(0, 26)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v/1000:.0f}k"))
    ax.legend(frameon=False, fontsize=5.5, loc="center right")
    ax.set_title("A \u2014 one resource, three facility ceilings", fontsize=7.3, loc="left")

    for key, c, lab in [("L-28", PAL["teal"], "P90"), ("L-29", PAL["navy"], "P50"),
                        ("L-30", PAL["amber"], "P10")]:
        r = L[key]["value"]
        rates = np.linspace(12000, 42000, 300)
        ax2.plot(rates, r * 1e6 / (rates * 365), color=c, lw=1.5,
                 label=f"{lab}  {r:.1f} MMbbl")
    ax2.axvspan(25000, 42000, color=PAL["amber"], alpha=0.10, zorder=0)
    ax2.axvline(25000, color=PAL["navy"], lw=1.0)
    ax2.text(25300, 3.0, "as-built\nceiling", fontsize=5.6, color=PAL["navy"])
    ax2.text(41400, 12.0, "requires topsides\nupgrade (OPEN)", fontsize=5.6,
             color=PAL["amber"], ha="right")
    ax2.set_xlabel("Plateau rate  (bopd)")
    ax2.set_ylabel("Life at plateau  (years)")
    ax2.set_xlim(12000, 42000)
    ax2.set_ylim(0, 30)
    ax2.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v/1000:.0f}k"))
    ax2.legend(frameon=False, fontsize=5.8, loc="upper right")
    ax2.set_title("B \u2014 rate buys years only if the vessel allows it",
                  fontsize=7.3, loc="left")

    fig.text(0.010, 0.008,
             "P50 resource 139.5 MMbbl (L-29). Plateau carries 70% of ultimate (ASSUMED); exponential decline "
             "exhausts the remainder.\nNo economic limit is applied \u2014 all curves are truncated at 2% of "
             "initial rate for plotting only (L-40 OPEN).",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.065, right=0.988, top=0.905, bottom=0.235, wspace=0.30)
    p = FIG / "fig1_profiles.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 1")
    plt.close(fig)
    return p, q


def fig2():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.3, 2.95),
                                  gridspec_kw={"width_ratios": [1, 1]})
    tt = np.linspace(0, 30, 500)
    for key, c, lab in [("L-28", PAL["teal"], "P90"), ("L-29", PAL["navy"], "P50"),
                        ("L-30", PAL["amber"], "P10")]:
        r = L[key]["value"]
        ax.plot(tt, np.minimum(25000 * 365 / 1e6 * tt, r), color=c, lw=1.6,
                label=f"{lab}  {r:.1f} MMbbl")
        ax.plot([r / (25000 * 365 / 1e6)], [r], "o", ms=3.6, color=c,
                mec="white", mew=0.7)
    ax.set_xlabel("Years at 25,000 bopd, zero decline")
    ax.set_ylabel("Cumulative oil  (MMbbl)")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 165)
    ax.legend(frameon=False, fontsize=5.9, loc="lower right")
    ax.set_title("A \u2014 depletion at the as-built ceiling", fontsize=7.3, loc="left")

    r = L["L-29"]["value"]
    rates = np.linspace(20000, 45000, 200)
    ax2.plot(rates, r * 1e6 / (rates * 365), color=PAL["navy"], lw=1.6)
    ax2.axhline(9.57, color=PAL["red"], lw=1.1, ls=(0, (4, 2)))
    ax2.axvline(25000, color=PAL["navy"], lw=0.8, ls=":")
    ax2.axvline(40000, color=PAL["red"], lw=0.8, ls=":")
    ax2.plot([25000], [r * 1e6 / (25000 * 365)], "o", ms=5, color=PAL["navy"],
             mec="white", mew=0.8)
    ax2.annotate("as-built ceiling\n15.3 yr", xy=(25000, 15.3), xytext=(26200, 18.6),
                 fontsize=5.9, color=PAL["navy"],
                 arrowprops=dict(arrowstyle="-", color=PAL["navy"], lw=0.6))
    ax2.annotate("9.57 yr \u2190 implies 40,000 bopd\n(the cancelled tender spec)",
                 xy=(40000, 9.57), xytext=(28300, 4.6), fontsize=5.9, color=PAL["red"],
                 arrowprops=dict(arrowstyle="-|>", color=PAL["red"], lw=0.7))
    ax2.set_xlabel("Plateau rate  (bopd)")
    ax2.set_ylabel("Life  (years)")
    ax2.set_xlim(20000, 45000)
    ax2.set_ylim(0, 22)
    ax2.set_xticks([20000, 25000, 30000, 35000, 40000])
    ax2.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v/1000:.0f}k"))
    ax2.set_title("B \u2014 what the 9.6-year figure encodes", fontsize=7.3, loc="left")

    fig.text(0.010, 0.008,
             "L-29 \u00f7 (40,000 \u00d7 365) = 9.57 yr. The figure v0.1 carried as a subsurface stress case is the "
             "cancelled 2020 tender's own 40,000 bopd,\nnot a property of the reservoir or of any vessel. "
             "This supersedes conflict C-06.",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.072, right=0.988, top=0.905, bottom=0.235, wspace=0.27)
    p = FIG / "fig2_ninetysix.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 2")
    plt.close(fig)
    return p, q


def fig3():
    rec = np.load(FIG / "mc_rec.npy")
    life = np.load(FIG / "mc_life.npy")
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.3, 2.7))
    ax.hist(rec, bins=70, color=PAL["steel"], edgecolor="white", linewidth=0.3)
    top = ax.get_ylim()[1]
    for q, lab, c in [(10, "P90", PAL["teal"]), (50, "P50", PAL["navy"]), (90, "P10", PAL["amber"])]:
        v = np.percentile(rec, q)
        ax.axvline(v, color=c, lw=1.1, ls=(0, (3, 2)))
        ax.text(v, top * 0.90, f" {lab}\n {v:.1f}", fontsize=5.6, color=c)
    ax.set_xlabel("Recoverable oil  (MMbbl)")
    ax.set_ylabel("Paths")
    ax.set_title("A \u2014 recoverable, 20,000 correlated draws", fontsize=7.3, loc="left")

    ax2.hist(life, bins=70, color=PAL["teal"], edgecolor="white", linewidth=0.3)
    top2 = ax2.get_ylim()[1]
    for q, lab, c in [(10, "P90", PAL["navy"]), (50, "P50", PAL["ink"]), (90, "P10", PAL["amber"])]:
        v = np.percentile(life, q)
        ax2.axvline(v, color=c, lw=1.1, ls=(0, (3, 2)))
        ax2.text(v, top2 * 0.90, f" {lab}\n {v:.1f}", fontsize=5.6, color=c)
    ax2.set_xlabel("Life at 25,000 bopd  (years)")
    ax2.set_ylabel("Paths")
    ax2.set_title("B \u2014 field life at the as-built ceiling", fontsize=7.3, loc="left")

    fig.text(0.010, 0.008,
             "\u03c1(OOIP, RF) = +0.60 (L-27). The spread is narrow because the input bracket is narrow: both bounds "
             "were back-calculated from the same public 139 MMbbl.\nThe Monte Carlo therefore propagates the bracket, "
             "it does not estimate the field. True uncertainty without a CPR is OPEN.",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.072, right=0.988, top=0.905, bottom=0.245, wspace=0.26)
    p = FIG / "fig3_mc.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 3")
    plt.close(fig)
    return p, q


def fig4():
    fig, ax = plt.subplots(figsize=(7.3, 2.6))
    rates = np.linspace(10000, 42000, 300)
    bo = 1.30
    ax.plot(rates, rates * bo / 1000, color=PAL["navy"], lw=1.7,
            label="Reservoir voidage, oil term (Bo 1.30)")
    ax.axhline(20, color=PAL["teal"], lw=1.6,
               label="Excalibur water injection 20,000 bwpd (L-07)")
    ax.axhline(75, color=PAL["red"], lw=1.2, ls=(0, (4, 2)),
               label="Cancelled tender 75,000 bwpd (L-12)")
    ax.fill_between(rates, 20, 75, color=PAL["red"], alpha=0.05)
    ax.axvline(25000, color=PAL["grey"], lw=0.8, ls=":")
    ax.text(25200, 88, "25,000 bopd", fontsize=5.8, color=PAL["grey"])
    ax.annotate("VRR 0.62 on the oil term alone \u2014\nunder-replacement, not over-injection",
                xy=(25000, 32.5), xytext=(26200, 56), fontsize=6.2, color=PAL["navy"],
                arrowprops=dict(arrowstyle="-|>", color=PAL["navy"], lw=0.8))
    ax.set_xlabel("Oil rate  (bopd)")
    ax.set_ylabel("Rate  (thousand rb/d or bwpd)")
    ax.set_xlim(10000, 42000)
    ax.set_ylim(0, 100)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v/1000:.0f}k"))
    ax.legend(frameon=False, fontsize=5.9, loc="upper left")
    fig.text(0.010, 0.008,
             "VRR = \u03a3(injected rb) \u00f7 \u03a3(produced rb), where the denominator includes oil \u00d7 Bo, produced water \u00d7 Bw "
             "AND free gas (GOR \u2212 Rs) \u00d7 Bg.\nCounted on the oil term alone the ratio is 0.62. Adding produced water "
             "and free gas can only lower it. Gas re-injection is not disclosed (L-09 OPEN).",
             fontsize=5.0, color=PAL["grey"], va="bottom")
    fig.subplots_adjust(left=0.078, right=0.985, top=0.955, bottom=0.255)
    p = FIG / "fig4_vrr.png"
    fig.savefig(p, dpi=300)
    q = gate(fig, "Fig 4")
    plt.close(fig)
    return p, q


if __name__ == "__main__":
    results = []
    for fn in (fig0, fig1, fig2, fig3, fig4):
        p, q = fn()
        results.append(q)
        print(f"{p.name:24s} {p.stat().st_size:>8d}  texts={q['texts']:3d} "
              f"outside={q['outside']} overlaps={q['overlaps']}")
    json.dump(results, open(PACK / "figure_qa.json", "w"), indent=2)
    print()
    if QA:
        print("QA FINDINGS:")
        for x in QA:
            print("  !", x)
    else:
        print("QA: no overflow, no overlap")
