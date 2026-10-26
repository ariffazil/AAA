#!/usr/bin/env python3
"""GEOX Sabah Regional — governed procedural figures (no external images)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np, os

OUT = "/root/AAA/forge_work/2026-10-19-sabah-geoint-slides/fig"
BLUE, BROWN, DARK = "#2D5F8B", "#8B4513", "#0A0A0F"
GOLD, GREY, RED, GREEN = "#FFD54F", "#6B7280", "#C0392B", "#2E8B57"
plt.rcParams.update({"font.size": 10, "text.color": "#E8E6E3",
                     "axes.labelcolor": "#E8E6E3", "xtick.color": "#E8E6E3",
                     "ytick.color": "#E8E6E3", "figure.facecolor": DARK,
                     "axes.facecolor": "#12141A", "savefig.facecolor": DARK})

def save(fig, name):
    fig.savefig(f"{OUT}/{name}", dpi=140, bbox_inches="tight", facecolor=DARK)
    plt.close(fig); print("fig:", name)

# ---------- 1. Regional transect segments ----------
fig, ax = plt.subplots(figsize=(12, 4.2))
segs = [
    ("SEG-1\nEast Sabah\nCONCEPTUAL", 790, 540, GREY, "CB"),
    ("SEG-2\nInterior/Crocker\nDERIVED", 540, 440, "#8B6B4A", "D"),
    ("SEG-3\nW Sabah onshore-off\nCONCEPTUAL", 440, 345, GREY, "CB"),
    ("SEG-4\nInboard/thrust-sheet\nDIRECT", 345, 230, BLUE, "DIR"),
    ("SEG-5\nToe-thrust/Trough\nDIRECT", 230, 150, BLUE, "DIR"),
    ("SEG-6\nNW Sabah Platform\nDIRECT", 150, 0, BLUE, "DIR"),
    ("SEG-7\nDangerous Grounds\nNO DATA", 0, -80, "#2A2D36", "ND"),
]
for label, x0, x1, col, code in segs:
    ax.add_patch(Rectangle((min(x0,x1), -0.35), abs(x1-x0) if abs(x1-x0)>1 else 80, 0.7,
                           facecolor=col, edgecolor="#E8E6E3", lw=1.1, alpha=0.9))
    ax.text((x0+x1)/2, 0, label, ha="center", va="center", fontsize=8, color="white", weight="bold")
# frame stations
stations = [(790,"DG\n8.30N 113.00E"),(540,"Sandakan\n5.85N 118.40E"),(440,"Mt Kinabalu\n4.095 km"),
            (345,"KK coast\n5.98N 116.07E"),(230,"Shelf edge\n6.20N 115.60E"),
            (150,"Trough axis\n6.80N 114.80E"),(0,"Layang-Layang\n7.37N 113.84E")]
for x, lab in stations:
    ax.plot([x,x],[-0.45,-0.35], color=GOLD, lw=1.6)
    ax.text(x, -0.62, lab, ha="center", va="top", fontsize=6.5, color=GOLD)
ax.set_xlim(-120, 860); ax.set_ylim(-1.25, 0.75)
ax.set_yticks([]); ax.set_xlabel("frame km along A–A′ (schematic · not to common scale)")
ax.set_title("REGIONAL TRANSECT · SEGMENT EVIDENCE CLASS · East Sabah (SE) ◄ display ► Dangerous Grounds (NW)\n"
             "Segment widths NOT to common scale · SEG boundaries are GEOX display constructs (RG-01)",
             fontsize=10, color=GOLD, pad=10)
ax.axhline(0, color="#E8E6E3", lw=0.6)
save(fig, "01_transect_segments.png")

# ---------- 2. Nested scales ----------
fig, ax = plt.subplots(figsize=(11, 5.2))
boxes = [
    (0.5, 0.72, 0.86, 0.22, BLUE, "SCALE 1 · REGIONAL SABAH",
     "East Sabah → Dangerous Grounds · frame A–A′\nTransect (this pack) · schematic stations only"),
    (0.5, 0.46, 0.66, 0.20, "#3A6F9B", "SCALE 2 · BASIN / STRUCTURAL DOMAIN",
     "Sabah Trough · toe-thrust · thrust-sheet · inboard · platform\nBIF-KL6 composite · navigation UNVERIFIED"),
    (0.5, 0.22, 0.46, 0.18, BROWN, "SCALE 3 · LOCAL CALIBRATION",
     "KB-KL2 · Rotan-1 / Maligan-1 / Barton-2\nTies: Rotan SRU/H3 FAIL · Maligan SRU FAIL"),
]
for x, y, w, h, col, title, body in boxes:
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.012",
                                facecolor=col, edgecolor="#E8E6E3", lw=1.4, alpha=0.92))
    ax.text(x, y+h*0.28, title, ha="center", va="center", fontsize=10, weight="bold", color="white")
    ax.text(x, y-h*0.22, body, ha="center", va="center", fontsize=8, color="#F0EDE8")
ax.annotate("", xy=(0.5, 0.585), xytext=(0.5, 0.605), arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.5))
ax.annotate("", xy=(0.5, 0.345), xytext=(0.5, 0.365), arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.5))
ax.text(0.5, 0.07, "Object IDs unchanged across scales · Local picks NOT propagated regionally (C20 FAIL ties)\n"
        "Regional concepts NOT inserted into local seismic as picks",
        ha="center", fontsize=8, color=GOLD)
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
ax.set_title("THREE NESTED SCALES · one object namespace", fontsize=12, color=GOLD, pad=8)
save(fig, "02_nested_scales.png")

# ---------- 3. Chronostrat P/L/R ----------
fig, ax = plt.subplots(figsize=(12.5, 6.2))
def age_to_y(a):
    if a <= 24: return a / 24 * 0.72
    return 0.72 + (a - 24) / 42 * 0.28
surfaces = [("SEABED",0.0,0.0,0.0),("H50",2.6,None,None),("H1",2.0,3.8,3.7),("H75",3.6,None,None),
            ("H2",3.1,5.5,5.59),("H3",8.11,6.7,6.7),("H110",8.1,None,None),("H150",9.0,None,None),
            ("SRU",9.53,9.4,9.53),("H300",10.1,None,None),("UIU",10.46,10.6,10.55),("H350",11.1,None,None),
            ("LIU",11.63,12.0,11.9),("H370",13.0,None,None),("DRU",14.2,15.4,14.91),("MMU",16.0,16.0,16.0),
            ("BMU",23.13,21.0,21.0),("BU",30.8,30.8,30.8),("LEU",34.1,34.4,34.4),("ROU",56.0,56.0,56.0)]
for name, p, l, r in surfaces:
    y = age_to_y(p)
    for i, (val, col, mk, lab) in enumerate([(p, GOLD, "o", "P"), (l, "#8FB8DE", "s", "L"), (r, "#E8A87C", "^", "R")]):
        if val is None: continue
        x = 1.0 + i * 0.28
        ax.plot(x, y, mk, color=col, ms=7, zorder=5)
        ax.text(x + 0.07, y, f"{lab} {val}", fontsize=6, va="center", color=col)
    if l is None:
        ax.text(1.35, y, "L/R n/a", fontsize=5.5, va="center", color=GREY)
    ax.text(0.88, y, name, fontsize=7.5, ha="right", va="center", color="white", weight="bold")
ax.axhline(age_to_y(24), color=RED, lw=1.6, ls="--")
ax.text(2.6, age_to_y(24), "SCALE BREAK 24 Ma\n0–24 Ma = 72% · 24–66 Ma = 28%", fontsize=7, color=RED, va="center")
for a in [0,4,8,12,16,20,24,30,40,50,60,66]:
    ax.text(0.55, age_to_y(a), f"{a}", fontsize=7, ha="right", va="center", color="#B0B0B0")
ax.plot([0.6,0.6],[age_to_y(0), age_to_y(66)], color="#B0B0B0", lw=0.8)
ax.text(0.42, 0.5, "Age (Ma)", rotation=90, fontsize=9, color="#B0B0B0", va="center")
# models legend
ax.add_patch(Rectangle((1.0, 1.02), 1.0, 0.10, facecolor="#1A1D26", edgecolor=GOLD, lw=1))
ax.text(1.5, 1.07, "P · PROJECT_2026 (top-of-stage)   L · LEGACY_TB (base-of-stage)   R · LEGACY_RECAL (re-dated)\n"
        "No model is canonical, preferred or closed · P, L and R drawn with equal weight\n"
        "DERIVED MODEL SPREAD — NOT a measured uncertainty interval",
        ha="center", va="center", fontsize=7.5, color=GOLD)
ax.set_xlim(0.3, 3.4); ax.set_ylim(-0.05, 1.15); ax.axis("off")
ax.set_title("CHRONO-STRATIGRAPHIC FRAME · KB-KL2 surfaces · three coequal models",
             fontsize=11, color=GOLD, pad=6)
save(fig, "03_chronostrat.png")

# ---------- 4. Tectonic events timeline ----------
fig, ax = plt.subplots(figsize=(12.5, 5.4))
events = [("EVT-T0", 66, 46, GREY, "Paleogene\nsubstrate"),
          ("EVT-T1", 23, 18, BLUE, "Early Miocene\nbasin init"),
          ("EVT-T2", 18, 13, BLUE, "NSPW\ndevelopment"),
          ("EVT-T3", 13, 13, GOLD, "H400\nboundary"),
          ("EVT-T4", 13, 11.1, BLUE, "Localized\nextension"),
          ("EVT-T5", 13, 10.1, RED, "EVENT-C-S\nkinematic"),
          ("EVT-T6", 10.1, 10, RED, "H300\ncompression"),
          ("EVT-T7", 10, 8, BLUE, "Minibasin\nsystem"),
          ("EVT-T8", 8, 6, BLUE, "Reduced\nconfinement"),
          ("EVT-T9", 9.5, 9.5, GOLD, "SRU\nsystem"),
          ("EVT-T10", 9, 8.1, BLUE, "Reactivation\nburial"),
          ("EVT-T11", 2.6, 2.6, GOLD, "Gravity\noverprint"),
          ("EVT-T12", 0, 0, GREEN, "Present\nday")]
for i, (eid, t0, t1, col, lab) in enumerate(events):
    y = len(events) - i
    x0, x1 = age_to_y(t0)*10, age_to_y(t1)*10
    ax.barh(y, max(abs(x1-x0), 0.25), left=min(x0,x1), height=0.6, color=col, alpha=0.88, edgecolor="white", lw=0.7)
    ax.text(-0.3, y, eid, ha="right", va="center", fontsize=7.5, color="white", weight="bold")
    ax.text(min(x0,x1) + max(abs(x1-x0),0.25) + 0.15, y, lab, va="center", fontsize=6.5, color="#D0D0D0")
ax.barh(len(events)+1, 0.35, left=age_to_y(13)*10, height=0.55, color="#8B0000", alpha=0.85)
ax.text(age_to_y(13)*10+0.5, len(events)+1, "EVT-C-M · Sabah Trough tectono-magmatic · HYPOTHESIS · HOLD · no geometry · no emplacement age (C30)",
        va="center", fontsize=6.5, color="#FF6B6B")
ax.set_yticks([]); ax.set_xlabel("model age scale (piecewise · break at 24 Ma)")
ax.set_title("TECTONIC EVENT FRAME · Block H and regional, as sourced · extent not demonstrated beyond Block H lane",
             fontsize=10, color=GOLD, pad=8)
ax.invert_xaxis()
save(fig, "04_events.png")

# ---------- 5. Evidence strength by segment ----------
fig, ax = plt.subplots(figsize=(11, 4.6))
cats = ["SEG-1\nE Sabah", "SEG-2\nInterior", "SEG-3\nW Sabah", "SEG-4\nInboard", "SEG-5\nToe/Trough", "SEG-6\nPlatform", "SEG-7\nDanger.Gd"]
direct  = [0, 0, 0, 2, 2, 2, 0]
derived = [0, 1, 0, 0, 1, 0, 0]
concept = [1, 0, 1, 0, 0, 0, 0]
nodata  = [0, 0, 0, 0, 0, 0, 1]
x = np.arange(len(cats))
ax.bar(x, direct,  0.55, label="DIRECT",    color=BLUE,  edgecolor="white")
ax.bar(x, derived, 0.55, label="DERIVED",   color="#8B6B4A", bottom=direct, edgecolor="white")
ax.bar(x, concept, 0.55, label="CONCEPTUAL",color=GREY,  bottom=np.add(direct,derived), edgecolor="white")
ax.bar(x, nodata,  0.55, label="NO DATA",   color="#2A2D36", bottom=np.add(np.add(direct,derived),concept), edgecolor="white")
ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=8)
ax.set_ylabel("evidence weight (display construct)")
ax.legend(loc="upper right", fontsize=8, facecolor="#1A1D26", edgecolor=GREY)
ax.set_title("SPATIAL EVIDENCE MATRIX · evidence class by segment\n"
             "Only SEG-4/5/6 carry direct seismic control · SEG-7 is NO DATA · SEG-1/3 conceptual bridges",
             fontsize=10, color=GOLD, pad=8)
save(fig, "05_evidence_matrix.png")

# ---------- 6. What-is-what epistemic pyramid ----------
fig, ax = plt.subplots(figsize=(11, 5.6))
layers = [
    (0.86, GREEN,  "WHAT THE EVIDENCE DIRECTLY SUPPORTS",
     "BIF-KL6 composite: rugose platform seabed · flat trough floor ≈3800 ms ·\nseabed rising SE · offset reflectors in toe-thrust panel"),
    (0.68, BLUE,   "WHAT IS LOCAL TO KB-KL2",
     "Digitised horizons · Rotan-1/Maligan-1/Barton-2 ties (C20 FAIL) ·\nH-series (H400 age unassigned) · restoration chronology behind EVENT-C-S"),
    (0.50, "#8B6B4A", "WHAT MAY BE REGIONAL",
     "Shallowing-to-SE seabed trend · trough → toe-thrust → thrust-sheet → shelf\ndomain order · consistent with public A–A′ frame order"),
    (0.32, GOLD,   "WHAT REMAINS A CORRELATION",
     "DRU/SRU/H-series continuity KB-KL2 → BIF-KL6 · MMU vs DRU across trough (C9) ·\nKL6 panel positions relative to frame A–A′"),
    (0.16, RED,    "WHAT REMAINS A HYPOTHESIS",
     "EVENT-C-M · crustal models R1–R4 · Models A/B/C (SRC-ESDG-MODELS) ·\nonshore–offshore magmatic correlation · 'Mesozoic' attribution of deep SE section"),
]
for y, col, title, body in layers:
    w = 0.92 - (0.86 - y) * 0.55
    ax.add_patch(FancyBboxPatch((0.5-w/2, y-0.055), w, 0.11, boxstyle="round,pad=0.008",
                                facecolor=col, edgecolor="#E8E6E3", lw=1.1, alpha=0.9))
    ax.text(0.5, y+0.022, title, ha="center", fontsize=9, weight="bold", color="white" if col!=GOLD else "#1A1A1A")
    ax.text(0.5, y-0.022, body, ha="center", fontsize=6.8, color="#F0EDE8" if col!=GOLD else "#1A1A1A")
ax.text(0.5, 0.04, "NOT REPRESENTED BY DATA: East Sabah & interior subsurface · mapped surface geology along transect ·\n"
        "Dangerous Grounds below seabed · crust and Moho everywhere · depth everywhere",
        ha="center", fontsize=8, color="#FFB3B3")
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
ax.set_title("EPISTEMIC SEPARATION · what is known where · GEOX renders; ARIF adjudicates",
             fontsize=11, color=GOLD, pad=8)
save(fig, "06_epistemic.png")

print("ALL FIGS DONE")
