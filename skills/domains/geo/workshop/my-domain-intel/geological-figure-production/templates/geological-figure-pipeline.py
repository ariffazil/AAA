#!/usr/bin/env python3
"""
geological-figure-pipeline.py — Starter template for the GEOX 7-figure basin deliverable.

Use as a starting point. Replace basin-specific data tables with the basin being worked on.

Proven 2026-08-20 with Senegal Basin. Iterate with vision_analyze-driven QA loop.
"""
import os
os.environ['MPLCONFIGDIR'] = '/tmp/.mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Polygon, Ellipse
from pathlib import Path
import numpy as np

# === PALETTE (GEOX dark) ===
BG       = '#0d1117'
BG2      = '#161b22'
GOLD     = '#f0a500'
AMBER    = '#ffa657'
GREEN    = '#3fb950'
RED      = '#f85149'
BLUE     = '#58a6ff'
TEAL     = '#39d2c0'
PURPLE   = '#bc8cff'
TEXT     = '#e6edf3'
DIM      = '#8b949e'
BORDER   = '#30363d'
YELLOW   = '#e3b341'
ORANGE   = '#db6d28'

# Lithology swatches (sedimentology convention)
LIT_SAND       = '#fde2b3'
LIT_SANDSTONE  = '#fcd180'
LIT_SHALE      = '#5a5a5a'
LIT_MARL       = '#7a9e9e'
LIT_LIMESTONE  = '#bce0d2'
LIT_DOLOMITE   = '#a4c8b8'
LIT_EVAPORITE  = '#cfb6e3'
LIT_BASALT     = '#3b3b3b'

# Lithology swatch label dict — keeps sed labels readable in PDF
LITH_LABEL = {
    LIT_SAND: 'SAND', LIT_SANDSTONE: 'SS', LIT_SHALE: 'SH', LIT_MARL: 'MARL',
    LIT_LIMESTONE: 'LS', LIT_DOLOMITE: 'DOL', LIT_EVAPORITE: 'EVAP', LIT_BASALT: 'BAS'
}

OUT = Path('/tmp/<basin>_figs')
OUT.mkdir(exist_ok=True)


def fig1_strat_column(units, title='Generalized Stratigraphic Column', subtitle=''):
    """units = list of (period, age_str, formation, lit_color, thick, role_code, notes, eps)"""
    fig, ax = plt.subplots(figsize=(16, 19))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

    col_x = [0.5, 9, 17, 41, 50, 59, 72, 91]
    col_w = [8, 7, 23, 8, 8, 12, 18, 8]
    headers = ['Period', 'Age (Ma)', 'Formation / Unit', 'Lith.', 'Thickness', 'Role', 'Notes', 'Epistemic']
    period_colors = {'NEOGENE': '#1f3a5a', 'PALEOGENE': '#1f3a5a',
                     'UPPER CRET': '#2a3a2a', 'M-L CRET': '#2a3a2a', 'JURASSIC': '#3a2a2a'}
    role_color_map = {'SEAL': TEAL, 'SOURCE': RED, 'RESERVOIR': ORANGE,
                      'SRC/Rsv': AMBER, 'SRC?': AMBER, '-': DIM}
    ep_color_map = {'OBS': GREEN, 'INT': AMBER, 'SPEC': RED}

    # Header
    ax.add_patch(Rectangle((0, 95.5), 100, 3.5, facecolor=BG2, edgecolor=GOLD, lw=1.5))
    for i, h in enumerate(headers):
        ax.text(col_x[i] + col_w[i]/2, 97.3, h, fontsize=10.5, fontweight='bold',
                color=GOLD, ha='center', va='center')

    n = len(units)
    y_top, y_bot = 92, 22
    spacing = (y_top - y_bot) / max(1, n - 1)
    y_positions = [y_top - i * spacing for i in range(n)]

    for i, u in enumerate(units):
        period, age_str, formation, lit_color, thick, role_code, notes, eps = u
        y = y_positions[i]

        ax.add_patch(Rectangle((col_x[0], y-1.5), col_w[0], 3,
                                facecolor=period_colors.get(period, BG2), edgecolor=BORDER, lw=0.5))
        ax.text(col_x[0] + col_w[0]/2, y, period, fontsize=9, ha='center', va='center',
                color=TEXT, fontweight='bold')
        ax.text(col_x[1] + col_w[1]/2, y, age_str, fontsize=9.5, ha='center', va='center', color=TEXT)
        ax.text(col_x[2] + col_w[2]/2, y, formation, fontsize=9.5, ha='center', va='center', color=TEXT, fontweight='bold')

        sx, sw = col_x[3], col_w[3]
        ax.barh(y, sw-0.3, left=sx+0.15, height=2.4, color=lit_color, edgecolor=BORDER, lw=0.5)
        lit_label = LITH_LABEL.get(lit_color, '?')
        text_color = '#1a1a1a' if lit_color in [LIT_SAND, LIT_LIMESTONE, LIT_DOLOMITE] else TEXT
        ax.text(sx + sw/2, y, lit_label, fontsize=9, ha='center', va='center',
                color=text_color, fontweight='bold')

        ax.text(col_x[4] + col_w[4]/2, y, thick, fontsize=8.5, ha='center', va='center', color=TEXT)
        role_c = role_color_map.get(role_code, TEXT)
        ax.text(col_x[5] + col_w[5]/2, y, role_code, fontsize=9, ha='center', va='center',
                color=role_c, fontweight='bold')
        ax.text(col_x[6] + col_w[6]/2, y, notes, fontsize=8, ha='center', va='center',
                color=DIM, style='italic')
        ep_c = ep_color_map[eps]
        ax.text(col_x[7] + col_w[7]/2, y, eps, fontsize=9, ha='center', va='center',
                color=ep_c, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', fc=BG2, ec=ep_c, alpha=0.7))

        if i < n-1:
            ax.plot([0.5, 99.5], [y - spacing/2, y - spacing/2], '-', color=BORDER, lw=0.5, alpha=0.5)

    ax.add_patch(Rectangle((0, 0), 100, 16, facecolor=BG2))
    ax.text(50, 11.5, f'Fig. 1 - {title}', fontsize=16, fontweight='bold', ha='center', va='center', color=GOLD)
    ax.text(50, 6, subtitle, fontsize=9, ha='center', va='center', color=TEXT)
    ax.text(50, 2, 'Epistemic bands per row. Source references in dossier text.',
            fontsize=8, ha='center', va='center', color=DIM, style='italic')
    plt.tight_layout()
    plt.savefig(OUT / 'fig1_strat_column.png', dpi=200, facecolor=BG, bbox_inches='tight')
    plt.close()


def fig2_burial_history(ages_ma, depths_present, horizons, sources_in_window):
    """Twin panel: depth vs time burial curve + Ro vs depth with windows."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [1.3, 1]})

    ax1.fill_between(-ages_ma, depths_present, [0]*len(depths_present), color=BLUE, alpha=0.15, step='mid')
    ax1.plot(-ages_ma, depths_present, '-', color=BLUE, lw=2)

    for age, depth, lbl, col in horizons:
        ax1.scatter(-age, depth, s=50, c=col, edgecolors='white', lw=1, zorder=10)
        ax1.annotate(lbl, (-age, depth), xytext=(-age + 3, depth - 100),
                     fontsize=7, color=col, fontweight='bold',
                     path_effects=[pe.withStroke(linewidth=2.5, foreground=BG)])
    # Phase bands
    ax1.axvspan(-200, -150, alpha=0.06, color=RED); ax1.text(-175, 5500, 'RIFT', fontsize=8, color=RED, ha='center', fontweight='bold')
    ax1.axvspan(-150, -66, alpha=0.06, color=GOLD); ax1.text(-105, 5500, 'THERMAL SUBSIDENCE / DRIFT', fontsize=8, color=GOLD, ha='center', fontweight='bold')
    ax1.axvspan(-66, 0, alpha=0.06, color=BLUE); ax1.text(-33, 5500, 'CENOZOIC DRIFT', fontsize=8, color=BLUE, ha='center', fontweight='bold')

    ax1.set_xlabel('Age (Ma)  PRESENT <-', fontsize=10); ax1.set_ylabel('Depth below seafloor (m)', fontsize=10)
    ax1.set_title('Burial History', fontsize=11, fontweight='bold', color=GOLD)
    ax1.invert_xaxis(); ax1.invert_yaxis(); ax1.set_xlim(-205, 5); ax1.set_ylim(6000, 0); ax1.grid(True, alpha=0.15)

    depths = np.linspace(0, 6000, 100)
    ro = 0.2 + 0.0008 * depths + 0.00000012 * depths**2
    ro = np.clip(ro, 0.1, 4.0)
    ax2.fill_betweenx(depths, 0.6, 1.2, color=ORANGE, alpha=0.18)
    ax2.fill_betweenx(depths, 1.2, 4.0, color=AMBER, alpha=0.18)
    ax2.fill_betweenx(depths, 0, 0.6, color=GREEN, alpha=0.10)
    ax2.plot(ro, depths, '-', color=GOLD, lw=2.5)

    ax2.text(0.4, 3000, 'IMMATURE (Ro<0.6)', fontsize=7, color=GREEN, fontweight='bold', ha='center')
    ax2.text(0.9, 4500, 'OIL WINDOW (Ro 0.6-1.2)', fontsize=7, color=ORANGE, fontweight='bold', ha='center')
    ax2.text(2.5, 5200, 'GAS WINDOW (Ro>1.2)', fontsize=7, color=AMBER, fontweight='bold', ha='center')

    ax2.set_xlabel('Vitrinite Reflectance (Ro %)', fontsize=10); ax2.set_ylabel('Depth (m TVDSS)', fontsize=10)
    ax2.set_title('Thermal Maturity Profile (Present-Day)', fontsize=11, fontweight='bold', color=GOLD)
    ax2.set_xlim(0, 4); ax2.set_ylim(0, 6000); ax2.invert_yaxis(); ax2.grid(True, alpha=0.15)
    plt.tight_layout()
    plt.savefig(OUT / 'fig2_burial_history.png', dpi=200, facecolor=BG, bbox_inches='tight')
    plt.close()


def fig3_cross_section(x, seabed, layers, salt_diapir=None, fields=None, source_kitchen=None):
    """layers = [(top, bot, color, label), ...] where top/bot are negative depths downward."""
    fig, ax = plt.subplots(figsize=(16, 10))
    for top, bot, color, label in layers:
        ax.fill_between(x, top, bot, color=color, edgecolor=DIM, linewidth=0.3,
                        label=label, alpha=0.85)

    if salt_diapir is not None:
        salt_x, salt_w, salt_top, salt_bot, base_top = salt_diapir
        mask = (x > salt_x - salt_w) & (x < salt_x + salt_w)
        if np.any(mask):
            ax.fill_between(x[mask], salt_top, salt_bot[mask], color='#cfb6e3',
                            edgecolor=PURPLE, linewidth=1, alpha=0.7)

    if fields is not None:
        for name, x_pos, color, label in fields:
            y = None  # caller determines
            ax.scatter(x_pos, y, s=200, c=color, edgecolors='white', linewidths=2, zorder=20, marker='*')

    ax.set_xlim(0, max(x) + 10); ax.set_ylim(-4500, 100)
    ax.set_xlabel('Distance W -> E (km)', fontsize=11); ax.set_ylabel('Depth below sea level (m)', fontsize=11)
    ax.set_title('Fig. 3 - Schematic Basin Cross-Section [SCHEMATIC]', fontsize=12, fontweight='bold', color=GOLD, pad=10)
    ax.legend(loc='upper left', fontsize=7, facecolor=BG2, edgecolor=BORDER, labelcolor=TEXT, ncol=2)
    ax.grid(True, alpha=0.1)
    plt.tight_layout()
    plt.savefig(OUT / 'fig3_cross_section.png', dpi=200, facecolor=BG, bbox_inches='tight')
    plt.close()


def fig4_block_map(coast_lons, coast_lats, blocks, wells):
    """blocks: [(name, polygon, color, status_str), ...]
    wells: [(lon, lat, name, year, color, size), ...]"""
    fig, ax = plt.subplots(figsize=(15, 11))

    # Land
    land_polygon = np.column_stack([
        list(coast_lons) + list(reversed(coast_lons)),
        list(coast_lats) + [11.5] * len(coast_lons)
    ])
    ax.fill(land_polygon[:, 0], land_polygon[:, 1], color='#1a2332', alpha=0.85)
    ax.plot(coast_lons, coast_lats, color=AMBER, lw=2.5)

    # Blocks
    for name, poly, col, status in blocks:
        ax.add_patch(Polygon(poly, closed=True, facecolor=col, alpha=0.25,
                              edgecolor=col, linewidth=2))
        cx = np.mean([p[0] for p in poly])
        cy = np.mean([p[1] for p in poly])
        ax.text(cx, cy + 0.15, name, fontsize=9, color=TEXT, ha='center',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', fc=BG2, ec=col, alpha=0.9))
        ax.text(cx, cy - 0.25, status, fontsize=8, color=col, ha='center', fontweight='bold')

    # Wells
    for lon, lat, name, year, col, size in wells:
        ax.scatter(lon, lat, s=size, c=col, edgecolors='white', linewidths=1, zorder=15, marker='^')
        ax.annotate(f'{name} {year}', (lon, lat), xytext=(lon+0.15, lat+0.15),
                     fontsize=7, color=col, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUT / 'fig4_block_map.png', dpi=200, facecolor=BG, bbox_inches='tight')
    plt.close()


def fig5_risk_heatmap(risks, risk_register):
    """risks: [(prob, impact, color, name, note, side, note_y), ...]"""
    fig, ax = plt.subplots(figsize=(14, 11))

    ax.fill_between([0.5, 1.0], 0.5, 1.0, color=RED, alpha=0.18, zorder=0)
    ax.fill_between([0.3, 1.0], 0.3, 0.7, color=AMBER, alpha=0.15, zorder=0)
    ax.fill_between([0, 0.5], 0, 0.5, color=GREEN, alpha=0.10, zorder=0)

    for prob, impact, col, name, note, side, note_y in risks:
        size = (prob * impact + 0.3) * 600
        ax.scatter(prob, impact, s=size, c=col, edgecolors='white', linewidths=2.5, zorder=10)

        x_align = 'right' if side == 'right' else 'left'
        x_pos = 0.95 if side == 'right' else 0.05
        ax.annotate(name, (prob, impact), xytext=(x_pos, impact + 0.05),
                     fontsize=9, color=TEXT, fontweight='bold', ha=x_align,
                     bbox=dict(boxstyle='round,pad=0.4', fc=BG2, ec=col, alpha=0.85),
                     arrowprops=dict(arrowstyle='-', color=col, lw=1.2, alpha=0.6))

    ax.text(0.05, 0.96, 'CRITICAL ZONE', fontsize=12, color=RED, fontweight='bold', alpha=0.55, ha='left', va='top')
    ax.text(0.95, 0.04, 'LOW RISK ZONE', fontsize=12, color=GREEN, fontweight='bold', alpha=0.55, ha='right', va='bottom')
    ax.set_xlabel('Probability', fontsize=11); ax.set_ylabel('Severity / Impact', fontsize=11)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    ax.set_yticklabels(['Negligible', 'Minor', 'Moderate', 'Major', 'Severe'])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / 'fig5_risk_heatmap.png', dpi=200, facecolor=BG, bbox_inches='tight')
    plt.close()


def fig6_events_chart(events, exploration_milestones, epochs):
    """events: [(name, t_start, t_end, color), ...]
    exploration_milestones: [(yr, label, desc), ...]
    epochs: [(start, end, label, color), ...]"""
    fig, ax = plt.subplots(figsize=(15, 9))
    for i, (name, t_start, t_end, color) in enumerate(events):
        ax.barh(i, t_start - t_end, left=t_end, height=0.55, color=color, alpha=0.65,
                 edgecolor=color, linewidth=1.2)
        if (t_start - t_end) > 15:
            ax.text((t_start+t_end)/2, i, name, fontsize=8.5, ha='center', va='center',
                    color=TEXT, fontweight='bold',
                    path_effects=[pe.withStroke(linewidth=2, foreground=BG)])
        else:
            ax.text(t_end + (t_start-t_end) + 1.5, i, name, fontsize=7, ha='left',
                    va='center', color=color, fontweight='bold')

    ax.invert_xaxis()
    ax.set_xlim(210, -10)
    ax.set_xticks([200, 150, 100, 50, 0])
    ax.set_xticklabels(['200 Ma', '150 Ma', '100 Ma', '50 Ma', 'Present'])
    ax.set_xlabel('Age (Ma) - PRESENT <- <- <- <- Deep Time', fontsize=11)
    ax.set_yticks([])
    plt.tight_layout()
    plt.savefig(OUT / 'fig6_events_chart.png', dpi=200, facecolor=BG, bbox_inches='tight')
    plt.close()


def fig7_discovery_timeline(discoveries, y_pos_map=None):
    """discoveries: [(year, name, op, type, res, color, status, size), ...]"""
    if y_pos_map is None:
        y_pos_map = {'OIL': 1.5, 'GAS': 0.5, 'OIL/GAS': 2.5}
    fig, ax = plt.subplots(figsize=(14, 9))
    for yr, name, op, typ, res, col, status, size in discoveries:
        y = y_pos_map.get(typ, 1.5)
        ax.scatter(yr, y, s=size, c=col, edgecolors='white', linewidths=1.5, zorder=10, alpha=0.9)
        ax.annotate(f'{name} {res}', (yr, y), xytext=(yr, y + 0.08),
                     fontsize=7, color=col, ha='center', fontweight='bold')
    ax.set_yticks([])
    ax.set_xlim(2013, 2026.5)
    ax.set_xlabel('Year', fontsize=10)
    plt.tight_layout()
    plt.savefig(OUT / 'fig7_discovery_timeline.png', dpi=200, facecolor=BG, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    # See /tmp/senegal_geological_figures_session/ for the data tables for each basin.
    # For your basin: replace these placeholder values with real geology.
    print("Stub template — populate data tables before calling each figure function.")
