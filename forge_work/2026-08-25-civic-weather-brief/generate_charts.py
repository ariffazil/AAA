#!/usr/bin/env python3
"""Generate analytics visuals for Penang/Kulim brief."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np
import os

os.makedirs("charts", exist_ok=True)

# Color palette (matching v2 PDF)
ACCENT = "#1B5E7B"
TEXT_PRIMARY = "#1A1A2E"
TEXT_SECONDARY = "#5C5C6D"
LIGHT_BG = "#F5F5F7"
DIVIDER = "#E8E8EE"
TAG_OBS = "#2E7D32"
TAG_DER = "#1565C0"
TAG_INT = "#6A1B9A"
TAG_SPEC = "#E65100"

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica Neue', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# ============================================================
# CHART 1: Flood history by month (Penang + Kulim)
# ============================================================
fig, ax = plt.subplots(figsize=(6.5, 3.2), dpi=150)
fig.patch.set_facecolor('white')

months = ['May', 'Jun', 'Jul', 'Aug']
penang = [0, 1, 2, 0]
kulim = [1, 0, 3, 0]

x = np.arange(len(months))
width = 0.35

bars1 = ax.bar(x - width/2, penang, width, label='Penang', color=ACCENT, edgecolor='none')
bars2 = ax.bar(x + width/2, kulim, width, label='Kulim', color='#5BA8C9', edgecolor='none')

ax.set_xlabel('Month 2026', fontsize=8, color=TEXT_SECONDARY)
ax.set_ylabel('Flood Incidents', fontsize=8, color=TEXT_SECONDARY)
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=9, color=TEXT_PRIMARY)
ax.tick_params(axis='y', labelsize=8, colors=TEXT_SECONDARY)
ax.set_ylim(0, 4)
ax.grid(axis='y', linestyle='--', alpha=0.3, color=DIVIDER)
ax.set_axisbelow(True)

# Annotate Jul Kulim peak (flash flood)
ax.annotate('Sedim\nflash flood\n17 Jul',
            xy=(2 + width/2, 3), xytext=(2.7, 3.4),
            fontsize=7, color=ACCENT, ha='center',
            arrowprops=dict(arrowstyle='-', color=ACCENT, lw=0.8))

ax.legend(loc='upper right', fontsize=8, frameon=False)
ax.spines['left'].set_color(DIVIDER)
ax.spines['bottom'].set_color(DIVIDER)

plt.title('Flood Incidents — May to Aug 2026', fontsize=10, color=TEXT_PRIMARY, fontweight='600', loc='left', pad=12)
plt.tight_layout()
plt.savefig('charts/01-flood-history.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 1: flood history")

# ============================================================
# CHART 2: Haze severity gauge / national status
# ============================================================
fig, ax = plt.subplots(figsize=(6.5, 2.8), dpi=150)
fig.patch.set_facecolor('white')

categories = ['Good\n(0–50)', 'Moderate\n(51–100)', 'Unhealthy\n(101–200)', 'Very Unhealthy\n(201–300)', 'Hazardous\n(>300)']
counts = [12, 45, 30, 8, 2]
colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336', '#7B1FA2']

bars = ax.barh(categories, counts, color=colors, edgecolor='none', height=0.7)

for bar, count in zip(bars, counts):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f'{count} stations', va='center', fontsize=8, color=TEXT_PRIMARY)

ax.set_xlim(0, 55)
ax.set_xlabel('Number of Monitoring Stations (n=97)', fontsize=8, color=TEXT_SECONDARY)
ax.tick_params(axis='y', labelsize=8, colors=TEXT_PRIMARY)
ax.tick_params(axis='x', labelsize=7, colors=TEXT_SECONDARY)
ax.grid(axis='x', linestyle='--', alpha=0.3, color=DIVIDER)
ax.set_axisbelow(True)

ax.set_title('National Haze Status — 30 Stations at Unhealthy+', fontsize=10, color=TEXT_PRIMARY, fontweight='600', loc='left', pad=10)
ax.spines['left'].set_color(DIVIDER)
ax.spines['bottom'].set_color(DIVIDER)

# annotation arrow
ax.annotate('Penang stations:\ntypically\n100–150 (Unhealthy)',
            xy=(28, 2), xytext=(35, 1),
            fontsize=7, color=ACCENT, ha='left',
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=0.8))

plt.tight_layout()
plt.savefig('charts/02-haze-status.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 2: haze severity")

# ============================================================
# CHART 3: 7-day forecast — temperature & precipitation
# ============================================================
fig, ax1 = plt.subplots(figsize=(6.5, 3.0), dpi=150)
fig.patch.set_facecolor('white')

dates = ['Aug 26\nTue', 'Aug 27\nWed', 'Aug 28\nThu', 'Aug 29\nFri', 'Aug 30\nSat', 'Aug 31\nSun', 'Sep 1\nMon']
temp_max = [31, 32, 33, 33, 32, 31, 30]
temp_min = [25, 25, 26, 26, 25, 25, 24]
precip = [12, 8, 2, 0, 1, 6, 10]

# Temperature band
ax1.fill_between(range(7), temp_min, temp_max, color=ACCENT, alpha=0.15, label='Temp range (°C)')
ax1.plot(range(7), temp_max, 'o-', color=ACCENT, linewidth=2, markersize=5, label='Max temp')
ax1.plot(range(7), temp_min, 'o-', color='#5BA8C9', linewidth=2, markersize=5, label='Min temp')

ax1.set_xlabel('', fontsize=8)
ax1.set_ylabel('Temperature (°C)', fontsize=8, color=TEXT_SECONDARY)
ax1.set_xticks(range(7))
ax1.set_xticklabels(dates, fontsize=7.5, color=TEXT_PRIMARY)
ax1.set_ylim(20, 36)
ax1.tick_params(axis='y', labelsize=8, colors=TEXT_SECONDARY)
ax1.grid(axis='y', linestyle='--', alpha=0.3, color=DIVIDER)
ax1.set_axisbelow(True)

# Highlight clear window
ax1.axvspan(2, 4.5, alpha=0.08, color=TAG_OBS, zorder=0)
ax1.text(3.2, 34.5, 'Clear window\n28–30 Aug', ha='center', fontsize=7.5, color=TAG_OBS, fontweight='600')

ax2 = ax1.twinx()
ax2.bar(range(7), precip, color='#90CAF9', alpha=0.6, label='Precipitation (mm)', width=0.5, zorder=2)
ax2.set_ylabel('Precipitation (mm)', fontsize=8, color=TEXT_SECONDARY)
ax2.set_ylim(0, 20)
ax2.tick_params(axis='y', labelsize=7, colors=TEXT_SECONDARY)
ax2.spines['top'].set_visible(False)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=7.5, frameon=False, ncol=2)

ax1.spines['left'].set_color(DIVIDER)
ax1.spines['bottom'].set_color(DIVIDER)
ax2.spines['right'].set_color(DIVIDER)

plt.title('7-Day Weather Outlook — Penang / Kulim', fontsize=10, color=TEXT_PRIMARY, fontweight='600', loc='left', pad=10)
plt.tight_layout()
plt.savefig('charts/03-7day-forecast.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 3: 7-day forecast")

# ============================================================
# CHART 4: Data flow / methodology pipeline
# ============================================================
fig, ax = plt.subplots(figsize=(7, 2.5), dpi=150)
fig.patch.set_facecolor('white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.axis('off')

stages = [
    ("SOURCES", "DOA\nOpenWeather\nHAPUA\nNews", '#5BA8C9'),
    ("INGEST", "Fetch\nParse\nTag", ACCENT),
    ("VALIDATE", "Cross-ref\n2+ sources\nEpistemic tag", ACCENT),
    ("SYNTHESIZE", "7 signals\nPage layout\nBudget check", '#1B5E7B'),
    ("DELIVER", "PDF\n5 pages\n~1,231 char/p", TAG_OBS),
]

box_w = 1.6
gap = 0.25
x_start = 0.2

for i, (label, content, color) in enumerate(stages):
    x = x_start + i * (box_w + gap)
    # Title bar
    rect = Rectangle((x, 1.8), box_w, 0.4, facecolor=color, edgecolor='none')
    ax.add_patch(rect)
    ax.text(x + box_w/2, 2.0, label, ha='center', va='center',
            fontsize=9, color='white', fontweight='700')
    # Content box
    rect2 = Rectangle((x, 0.4), box_w, 1.3, facecolor=LIGHT_BG, edgecolor=DIVIDER, linewidth=0.8)
    ax.add_patch(rect2)
    ax.text(x + box_w/2, 1.05, content, ha='center', va='center',
            fontsize=7.5, color=TEXT_PRIMARY, linespacing=1.4)

    # Arrow to next
    if i < len(stages) - 1:
        ax.annotate('', xy=(x + box_w + gap - 0.05, 1.0), xytext=(x + box_w + 0.05, 1.0),
                    arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

# Footer note
ax.text(5, 0.1, 'Each stage must pass before advancing (F1 Safety / F2 Evidence gates)',
        ha='center', fontsize=7, color=TEXT_SECONDARY, style='italic')

plt.tight_layout()
plt.savefig('charts/04-data-pipeline.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 4: data pipeline")

# ============================================================
# CHART 5: Risk matrix (likelihood x impact)
# ============================================================
fig, ax = plt.subplots(figsize=(5.5, 3.5), dpi=150)
fig.patch.set_facecolor('white')

# Background zones
ax.add_patch(Rectangle((1, 1), 1, 1, facecolor='#E8F5E9', edgecolor='none'))   # low/low
ax.add_patch(Rectangle((2, 1), 1, 1, facecolor='#FFF9C4', edgecolor='none'))   # low/med-low
ax.add_patch(Rectangle((1, 2), 1, 1, facecolor='#FFF9C4', edgecolor='none'))   # med/low
ax.add_patch(Rectangle((2, 2), 1, 1, facecolor='#FFE0B2', edgecolor='none'))   # med/med-high
ax.add_patch(Rectangle((1, 3), 1, 1, facecolor='#FFE0B2', edgecolor='none'))   # high/low
ax.add_patch(Rectangle((2, 3), 1, 1, facecolor='#FFCDD2', edgecolor='none'))   # high/med-high

# Grid
for i in range(4):
    ax.axhline(i, color=DIVIDER, linewidth=0.8)
    ax.axvline(i, color=DIVIDER, linewidth=0.8)

# Risk items (x=likelihood 1-4, y=impact 1-4)
risks = [
    ('Flash flood\n(Kulim)', 2, 3.3, TAG_DER),
    ('Haze\nrespiratory', 3.5, 2.2, TAG_OBS),
    ('Storm Narra\ntrack', 2.3, 3, TAG_INT),
    ('Heavy rain\n25–31 Aug', 2.5, 2, TAG_DER),
    ('Reservoir\nlevels', 1.5, 2.5, TAG_SPEC),
]

for label, x, y, color in risks:
    ax.scatter([x], [y], s=400, color=color, alpha=0.7, edgecolors='white', linewidths=2, zorder=3)
    ax.annotate(label, (x, y), fontsize=7, color=TEXT_PRIMARY, ha='center', va='center', zorder=4, fontweight='600')

ax.set_xlim(0.8, 3.5)
ax.set_ylim(0.8, 3.7)
ax.set_xticks([1.5, 2.5])
ax.set_xticklabels(['Lower', 'Higher'], fontsize=8, color=TEXT_SECONDARY)
ax.set_yticks([1.5, 2.5, 3.5])
ax.set_yticklabels(['Low', 'Medium', 'High'], fontsize=8, color=TEXT_SECONDARY)
ax.set_xlabel('LIKELIHOOD →', fontsize=8, color=TEXT_SECONDARY, fontweight='600')
ax.set_ylabel('IMPACT →', fontsize=8, color=TEXT_SECONDARY, fontweight='600')

ax.set_title('Risk Matrix — Penang/Kulim 25 Aug 2026', fontsize=10, color=TEXT_PRIMARY, fontweight='600', loc='left', pad=10)
ax.spines['left'].set_color(DIVIDER)
ax.spines['bottom'].set_color(DIVIDER)

plt.tight_layout()
plt.savefig('charts/05-risk-matrix.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 5: risk matrix")

# ============================================================
# CHART 6: Peninsular Malaysia map (stylized) with haze + locations
# ============================================================
fig, ax = plt.subplots(figsize=(7, 4), dpi=150)
fig.patch.set_facecolor('white')

# Simplified Peninsular Malaysia outline (stylized - not GIS accurate)
# West coast points (rough)
import matplotlib.path as mpath
Path = mpath.Path

peninsular_verts = [
    (1.5, 4.5),  # Perlis
    (2.0, 5.0),  # Langkawi area
    (2.8, 4.7),  # Kedah north
    (3.5, 4.3),  # Penang
    (3.6, 3.5),  # Perak
    (3.5, 2.7),  # Selangor
    (3.6, 2.0),  # Negeri Sembilan
    (3.7, 1.3),  # Malacca
    (4.2, 1.0),  # Johor north
    (4.6, 0.5),  # Johor south
    (4.0, 0.7),  # east coast johor
    (3.5, 1.5),  # east coast pahang
    (3.5, 2.5),  # east coast terengganu
    (3.2, 3.5),  # east coast kelantan
    (2.8, 4.2),  # Kelantan north
    (1.5, 4.5),  # back to Perlis
]

codes = [Path.MOVETO] + [Path.LINETO] * (len(peninsular_verts) - 2) + [Path.CLOSEPOLY]
malaysia_path = Path(peninsular_verts, codes)
patch = mpatches.PathPatch(malaysia_path, facecolor='#E8F4F8', edgecolor=ACCENT, linewidth=1.2)
ax.add_patch(patch)

# Haze plume (west coast smoke from Sumatra)
haze_x = [0.5, 1.5, 2.5, 3.5, 4.0, 4.5]
haze_y = [3.0, 3.5, 3.2, 3.8, 3.0, 2.5]
for i, (hx, hy) in enumerate(zip(haze_x, haze_y)):
    circle = plt.Circle((hx, hy), 0.3 + i*0.05, color='#FFB74D', alpha=0.2 + i*0.02, zorder=2)
    ax.add_patch(circle)

# Sumatra (Indonesia) — left side
sumatra = [(0.0, 3.5), (0.3, 4.0), (0.6, 4.3), (1.0, 4.2), (1.1, 3.8), (0.9, 3.3), (0.5, 3.0), (0.0, 3.5)]
sum_codes = [Path.MOVETO] + [Path.LINETO] * (len(sumatra) - 2) + [Path.CLOSEPOLY]
sum_path = Path(sumatra, sum_codes)
sum_patch = mpatches.PathPatch(sum_path, facecolor='#FFE0B2', edgecolor='#E65100', linewidth=0.8, alpha=0.7)
ax.add_patch(sum_patch)
ax.text(0.4, 3.7, 'Sumatra\n(open burning)', fontsize=7, color='#E65100', ha='center', fontweight='600')

# Key locations
locations = [
    ('Penang', 3.5, 4.3, ACCENT, 'large'),
    ('Kulim', 3.0, 4.5, ACCENT, 'medium'),
    ('KL', 3.5, 2.3, TEXT_SECONDARY, 'small'),
    ('Johor', 4.3, 0.8, TEXT_SECONDARY, 'small'),
]

for name, x, y, color, size in locations:
    if size == 'large':
        ax.scatter([x], [y], s=200, color=color, zorder=5, edgecolors='white', linewidths=2)
        ax.text(x + 0.1, y + 0.05, name, fontsize=9, color=color, fontweight='700')
    elif size == 'medium':
        ax.scatter([x], [y], s=120, color=color, zorder=5, edgecolors='white', linewidths=2)
        ax.text(x + 0.1, y + 0.05, name, fontsize=8, color=color, fontweight='600')
    else:
        ax.scatter([x], [y], s=60, color=color, zorder=5, edgecolors='white', linewidths=1.5)
        ax.text(x + 0.1, y, name, fontsize=7, color=color)

# Storm Narra (Philippine Sea - upper right)
narra_x, narra_y = 6.5, 5.5
circle = plt.Circle((narra_x, narra_y), 0.5, color='#90CAF9', alpha=0.4, zorder=3)
ax.add_patch(circle)
ax.scatter([narra_x], [narra_y], s=250, color='#1565C0', zorder=5, edgecolors='white', linewidths=2, marker='s')
ax.annotate('TS Narra\n(Philippine Sea)', (narra_x, narra_y), xytext=(narra_x - 0.5, narra_y - 0.8),
            fontsize=8, color='#1565C0', fontweight='700', ha='center',
            arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1))

# Uncertain track
ax.annotate('', xy=(4.5, 3.5), xytext=(narra_x - 0.3, narra_y - 0.3),
            arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5, linestyle='--', alpha=0.6))
ax.text(5.5, 4.3, '? track', fontsize=7, color='#1565C0', style='italic')

# Legend
ax.scatter([0.5], [0.5], s=200, color=ACCENT, edgecolors='white', linewidths=2)
ax.text(0.7, 0.5, 'Brief location', fontsize=7, color=TEXT_PRIMARY, va='center')

ax.scatter([2.0], [0.5], s=200, color='#FFB74D', alpha=0.6)
ax.text(2.2, 0.5, 'Haze plume', fontsize=7, color=TEXT_PRIMARY, va='center')

ax.scatter([3.5], [0.5], s=200, color='#1565C0', edgecolors='white', linewidths=2, marker='s')
ax.text(3.7, 0.5, 'Tropical storm', fontsize=7, color=TEXT_PRIMARY, va='center')

# Sea labels
ax.text(0.3, 2.0, 'Strait of\nMalacca', fontsize=7, color='#1565C0', style='italic', alpha=0.6)
ax.text(5.5, 5.8, 'South China Sea', fontsize=7, color='#1565C0', style='italic', alpha=0.6)

ax.set_xlim(-0.3, 7.5)
ax.set_ylim(0, 6.5)
ax.set_aspect('equal')
ax.axis('off')

ax.set_title('Regional Context — Peninsular Malaysia',
             fontsize=10, color=TEXT_PRIMARY, fontweight='600', loc='left', pad=10)
plt.tight_layout()
plt.savefig('charts/06-regional-map.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Chart 6: regional map")

print("\nAll charts generated.")