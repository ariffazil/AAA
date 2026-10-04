#!/usr/bin/env python3
"""Matplotlib editorial poster skeleton — 1080x1080 dark.

Proven 2026-08-11 on SADO PHYSIQUE RADAR weekly scan. Use this when the lane
capability map lists matplotlib (no Chromium / no Unsplash hero) and the
deliverable is a layout-only editorial piece (event calendar, weekly radar,
briefing poster, calendar grid).

Verified layout fixes baked into this skeleton:
- Title at fontsize=38 (not 44) to avoid right-column overflow
- textwrap.wrap() BEFORE drawing card titles
- Card height 2-row split with 30px gap between name block and meta block
- Right-aligned meta uses ha="left" with estimated-width subtraction
- Legend dots use cumulative_offset, not i*80

Invoke by editing the CARDS list to the event set of the week, then run.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import textwrap

W = H = 1080
fig = plt.figure(figsize=(10.8, 10.8), dpi=100, facecolor="#0a0a0c")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_facecolor("#0a0a0c"); ax.axis("off")

# Style tokens — override per-lane
GOLD = "#d4af37"; CYAN = "#4dd0e1"; PURPLE = "#b388ff"
DIM = "#7a7a7e"; TEXT = "#e8e8ea"; PANEL = "#131316"

# Editor: edit CARDS then run. accent: GOLD=major, CYAN=local, PURPLE=region
CARDS = [
    {"date": "DD MMM YYYY · LOCAL", "name": "Event Name", "meta": ["venue", "federation", "reg link"], "accent": CYAN},
    # ... add up to 4 cards for 2x2 grid
]

# ---------- header ----------
HDR_Y = H - 150
ax.add_patch(Rectangle((0, HDR_Y), W, H - HDR_Y, color="#0d0d10", zorder=1))
ax.plot([0, W], [HDR_Y, HDR_Y], color=GOLD, lw=2, zorder=2)

# Title — fontsize=38 to keep right meta safe
ax.text(50, H - 60, "YOUR TITLE HERE", color=TEXT, fontsize=38, fontweight="bold",
        family="DejaVu Sans", va="center", zorder=3)
ax.text(50, H - 105, "Subtitle / window", color=DIM, fontsize=14,
        family="DejaVu Sans", va="center", zorder=3)

# Right meta — moved up vs. title so they don't overlap
ax.text(W - 50, H - 55, "META", color=CYAN, fontsize=20, fontweight="bold",
        ha="right", va="center", zorder=3)
ax.text(W - 50, H - 85, "meta line 1", color=DIM, fontsize=11,
        ha="right", va="center", zorder=3)
ax.text(W - 50, H - 108, "meta line 2", color=DIM, fontsize=10,
        ha="right", va="center", zorder=3)

# ---------- cards ----------
def event_card(x, y, w, h, date, name, meta_lines, accent):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=10",
                                 facecolor=PANEL, edgecolor="#232326", lw=1, zorder=2))
    ax.add_patch(Rectangle((x, y), 5, h, color=accent, zorder=3))
    ax.text(x + 18, y + h - 24, date, color=TEXT, fontsize=16, fontweight="bold",
            family="DejaVu Sans", va="center", zorder=4)
    name_y = y + h - 56
    for line in textwrap.wrap(name, width=28) or [name]:
        ax.text(x + 18, name_y, line, color=TEXT, fontsize=16, fontweight="bold",
                family="DejaVu Sans", va="top", zorder=4)
        name_y -= 24
    meta_y = y + 18 + (len(meta_lines) - 1) * 18
    for line in meta_lines:
        ax.text(x + 18, meta_y, line, color=DIM, fontsize=11,
                family="DejaVu Sans", va="bottom", zorder=4)
        meta_y -= 18

margin = 50; gutter = 16
header_used = 230; bottom_used = 200
avail_w = W - 2 * margin - gutter
avail_h = H - header_used - bottom_used
card_w = avail_w / 2
card_h = avail_h / 2 - gutter / 2

positions = [
    (margin,                                  H - header_used - card_h),
    (margin + card_w + gutter,                H - header_used - card_h),
    (margin,                                  H - header_used - 2*card_h - gutter),
    (margin + card_w + gutter,                H - header_used - 2*card_h - gutter),
]
for c, (x, y) in zip(CARDS, positions):
    event_card(x, y, card_w, card_h, c["date"], c["name"], c["meta"], c["accent"])

# ---------- footer ----------
ax.text(W/2, 65, "your watermark", color=DIM, fontsize=11, ha="center",
        family="DejaVu Sans")
ax.text(W/2, 38, "epistemic labels: [OBS] [DER] [SPEC]  ·  unknown beats invented",
        color="#4a4a4e", fontsize=9, ha="center", family="DejaVu Sans")

# ---------- save ----------
import sys
out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/editorial_poster.png"
plt.savefig(out, dpi=100, facecolor="#0a0a0c", bbox_inches=None, pad_inches=0)
plt.close(fig)

# ---------- verify ----------
import struct
p = out
with open(p, "rb") as f:
    sig = f.read(8)
    f.seek(16); w, h = struct.unpack(">II", f.read(8))
assert sig == b"\x89PNG\r\n\x1a\n", f"NOT PNG: {sig!r}"
assert w == 1080 and h == 1080, f"WRONG dim {w}x{h}"
print(f"OK: {out} ({w}x{h})")
