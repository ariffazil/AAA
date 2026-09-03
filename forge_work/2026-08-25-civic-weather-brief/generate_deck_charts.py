#!/usr/bin/env python3
"""Generate arifOS Federation deck visuals — slides for Kernel / AAA STATE / A-FORGE."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
import numpy as np
import os

os.makedirs("deck_charts", exist_ok=True)

ACCENT = "#1B5E7B"
ACCENT_LIGHT = "#5BA8C9"
ACCENT_BG = "#E8F4F8"
TEXT_PRIMARY = "#1A1A2E"
TEXT_SECONDARY = "#5C5C6D"
TEXT_CAPTION = "#8A8A9A"
LIGHT_BG = "#F5F5F7"
DIVIDER = "#E8E8EE"
TAG_OBS = "#2E7D32"
TAG_DER = "#1565C0"
TAG_INT = "#6A1B9A"
TAG_SPEC = "#E65100"
ACCENT_DARK = "#0D3B4F"
ACCENT_GOLD = "#C9A961"

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica Neue', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# ============================================================
# SLIDE 2: 13 Constitutional Floors (F1-F13)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)
fig.patch.set_facecolor('white')

floors = [
    ("F1", "Safety", "Reversibility, no harm"),
    ("F2", "Evidence", "Every claim sourced"),
    ("F3", "Scope", "Stay within declared boundary"),
    ("F4", "Reversibility", "Backout before commit"),
    ("F5", "Privacy", "Sovereign data integrity"),
    ("F6", "Auditability", "Every decision logged"),
    ("F7", "Confidence", "Cap certainty by evidence"),
    ("F8", "Authority", "Right person decides"),
    ("F9", "Anti-Hantu", "No voice/persona without consent"),
    ("F10", "Ontology", "Reality-first claims"),
    ("F11", "Consent", "Human sovereignty preserved"),
    ("F12", "Witness", "Tri-witness consensus"),
    ("F13", "Sovereign", "Arif's final veto"),
]

# Grid 5x3 (last col has 3 empty or center)
cols, rows = 5, 3
box_w, box_h = 1.7, 1.4
gap = 0.15
x_start = 0.4
y_start = 5.0

for i, (code, name, desc) in enumerate(floors):
    col = i % cols
    row = i // cols
    x = x_start + col * (box_w + gap)
    y = y_start - row * (box_h + gap)

    # Card
    card = FancyBboxPatch((x, y), box_w, box_h,
                          boxstyle="round,pad=0.02,rounding_size=0.08",
                          facecolor=ACCENT_BG, edgecolor=ACCENT, linewidth=1)
    ax.add_patch(card)

    # Code
    ax.text(x + box_w/2, y + box_h - 0.25, code,
            ha='center', va='center', fontsize=14, fontweight='700', color=ACCENT)
    # Name
    ax.text(x + box_w/2, y + box_h/2 + 0.05, name,
            ha='center', va='center', fontsize=9, fontweight='600', color=TEXT_PRIMARY)
    # Description
    ax.text(x + box_w/2, y + 0.25, desc,
            ha='center', va='center', fontsize=7, color=TEXT_SECONDARY, wrap=True)

ax.set_xlim(0, 11)
ax.set_ylim(-0.5, 7)
ax.axis('off')
ax.set_title('F1–F13 Constitutional Floors', fontsize=13, color=TEXT_PRIMARY, fontweight='700', loc='left', pad=10)

plt.tight_layout()
plt.savefig('deck_charts/02-floors.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Slide 2: 13 Constitutional Floors")

# ============================================================
# SLIDE 3: AAA State — Trinity of Self
# ============================================================
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)
fig.patch.set_facecolor('white')

# Three concentric triangles or stacked layers
center_x, center_y = 5, 3.2

# AGI layer (bottom — broadest)
agi_box = FancyBboxPatch((1.5, 0.5), 7, 4.5,
                          boxstyle="round,pad=0.02,rounding_size=0.15",
                          facecolor='#E8F5E9', edgecolor=TAG_OBS, linewidth=1.2, alpha=0.5)
ax.add_patch(agi_box)
ax.text(2, 4.7, 'AGI — 333', fontsize=11, fontweight='700', color=TAG_OBS)
ax.text(2, 4.35, 'Agent Layer', fontsize=8, color=TEXT_SECONDARY)
ax.text(2, 0.85, 'Autonomy · Skill binding\nSub-agent lifecycle', fontsize=7.5, color=TEXT_SECONDARY)

# ASI layer (middle)
asi_box = FancyBboxPatch((2.5, 1.5), 5, 3,
                          boxstyle="round,pad=0.02,rounding_size=0.12",
                          facecolor='#E3F2FD', edgecolor=TAG_DER, linewidth=1.2, alpha=0.7)
ax.add_patch(asi_box)
ax.text(3, 4.2, 'ASI — 555', fontsize=11, fontweight='700', color=TAG_DER)
ax.text(3, 3.85, 'Symbiotic Layer', fontsize=8, color=TEXT_SECONDARY)
ax.text(3, 2.85, 'Causal inference\nMultimodal cognition\nA2A protocol', fontsize=7.5, color=TEXT_SECONDARY)

# APEX layer (top — sovereign)
apex_box = FancyBboxPatch((3.5, 2.5), 3, 1.5,
                           boxstyle="round,pad=0.02,rounding_size=0.1",
                           facecolor='#F3E5F5', edgecolor=TAG_INT, linewidth=1.5)
ax.add_patch(apex_box)
ax.text(5, 3.7, 'APEX — 888', fontsize=11, fontweight='700', color=TAG_INT, ha='center')
ax.text(5, 3.4, 'Constitutional Reflex', fontsize=8, color=TEXT_SECONDARY, ha='center')
ax.text(5, 2.85, 'SEAL · HOLD · ROUTE', fontsize=8, color=TEXT_PRIMARY, ha='center', fontweight='600')

# Arrow from APEX down
ax.annotate('', xy=(6.5, 1.5), xytext=(6.5, 2.5),
            arrowprops=dict(arrowstyle='->', color=TEXT_PRIMARY, lw=1.5))
ax.text(6.8, 2.0, 'F13 seal\nflows to\nall layers', fontsize=7, color=TEXT_SECONDARY, va='center')

# Side annotations
ax.text(0.3, 6.0, 'HUMAN', fontsize=10, fontweight='700', color=ACCENT)
ax.text(0.3, 5.65, 'F13 SOVEREIGN', fontsize=8, color=ACCENT)
ax.text(0.3, 5.4, '────────────', fontsize=8, color=ACCENT)
ax.text(0.3, 5.15, 'Arif Fazil\nPenang', fontsize=7.5, color=TEXT_SECONDARY)

ax.text(9.2, 6.0, 'KERNEL', fontsize=10, fontweight='700', color=ACCENT)
ax.text(9.2, 5.65, 'CONSTITUTIONAL', fontsize=8, color=ACCENT)
ax.text(9.2, 5.4, '────────────', fontsize=8, color=ACCENT)
ax.text(9.2, 5.15, 'F1–F12\nenforced', fontsize=7.5, color=TEXT_SECONDARY)

ax.set_xlim(0, 10)
ax.set_ylim(0, 6.5)
ax.axis('off')
ax.set_title('AAA STATE — Three Layers of Self', fontsize=13, color=TEXT_PRIMARY, fontweight='700', loc='left', pad=10)

plt.tight_layout()
plt.savefig('deck_charts/03-aaa-state.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Slide 3: AAA State Trinity")

# ============================================================
# SLIDE 4: A-FORGE Execution Loop
# ============================================================
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=150)
fig.patch.set_facecolor('white')

stages = [
    ("OBSERVE", "Ground-truth\ndata ingest", TAG_OBS),
    ("THINK", "Plan DAG\nfalsify", TAG_DER),
    ("ROUTE", "Skill bind\nagent spawn", TAG_INT),
    ("ACT", "Tool execute\nfile write", TAG_SPEC),
    ("VERIFY", "Tri-witness\nseal or reject", TAG_OBS),
    ("LEARN", "Scar log\nself-mutate", ACCENT),
]

# Circular layout
import math
n = len(stages)
radius = 2.3
center_x, center_y = 5, 2.8

for i, (label, desc, color) in enumerate(stages):
    angle = (i / n) * 2 * math.pi - math.pi / 2
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

    # Node circle
    circle = Circle((x, y), 0.55, facecolor=color, alpha=0.85, edgecolor='white', linewidth=2)
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='700', color='white')
    ax.text(x, y - 0.85, desc, ha='center', va='center', fontsize=7.5, color=TEXT_SECONDARY)

    # Arrow to next
    next_angle = ((i + 1) / n) * 2 * math.pi - math.pi / 2
    nx = center_x + radius * math.cos(next_angle)
    ny = center_y + radius * math.sin(next_angle)
    ax.annotate('', xy=(nx, ny), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.8,
                                connectionstyle='arc3,rad=0.2'))

# Center
center_circle = Circle((center_x, center_y), 1.0, facecolor=ACCENT_DARK, edgecolor='white', linewidth=2)
ax.add_patch(center_circle)
ax.text(center_x, center_y + 0.25, 'A-FORGE', ha='center', va='center',
        fontsize=12, fontweight='700', color='white')
ax.text(center_x, center_y - 0.2, 'Execution', ha='center', va='center', fontsize=9, color='white')
ax.text(center_x, center_y - 0.45, 'Engine', ha='center', va='center', fontsize=9, color='white')

ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('A-FORGE — Perpetual Execution Loop', fontsize=13, color=TEXT_PRIMARY, fontweight='700', loc='left', pad=10)

plt.tight_layout()
plt.savefig('deck_charts/04-aforge-loop.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Slide 4: A-FORGE Loop")

# ============================================================
# SLIDE 5: Federation Map — 7 Repos + 12 Organs
# ============================================================
fig, ax = plt.subplots(figsize=(11, 5), dpi=150)
fig.patch.set_facecolor('white')

# 7 repos as primary nodes
repos = [
    ("arifOS", 1.5, 4.5, ACCENT_DARK, "Sovereign OS\nconstitution"),
    ("A-FORGE", 1.5, 3.0, ACCENT, "Execution engine\nforge loop"),
    ("AAA", 1.5, 1.5, ACCENT_LIGHT, "Agent stack\nskills + memory"),
    ("GEOX", 5.5, 4.5, "#1B5E7B", "Geological\nagentic reasoning"),
    ("WEALTH", 5.5, 3.0, "#5BA8C9", "Capital state\ntrading"),
    ("WELL", 5.5, 1.5, "#90CAF9", "Human readiness\nvitality"),
    ("arif-fazil.com", 9.5, 3.0, ACCENT_GOLD, "Public surface\nSOT manifest"),
]

for name, x, y, color, desc in repos:
    box = FancyBboxPatch((x - 0.85, y - 0.5), 1.7, 1.0,
                          boxstyle="round,pad=0.02,rounding_size=0.08",
                          facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
    ax.add_patch(box)
    ax.text(x, y + 0.15, name, ha='center', va='center',
            fontsize=10, fontweight='700', color='white')
    ax.text(x, y - 0.25, desc, ha='center', va='center',
            fontsize=7, color='white', alpha=0.9)

# Connecting lines (fractal mesh)
connections = [
    (0, 1), (1, 2), (0, 3), (0, 4), (0, 5), (3, 4), (3, 5), (4, 5),
    (0, 6), (2, 6), (3, 6), (4, 6), (5, 6),
]
for a, b in connections:
    ax.plot([repos[a][1], repos[b][1]], [repos[a][2], repos[b][2]],
            color=ACCENT, alpha=0.15, linewidth=0.8, zorder=0)

# Docker organs (small nodes around)
organs = [
    ("postgres", 3.5, 5.6), ("qdrant", 3.5, 0.4), ("falkordb", 7.5, 5.6),
    ("minio", 7.5, 0.4), ("searxng", 8.0, 2.3), ("langfuse", 2.5, 2.3),
    ("clickhouse", 10.0, 1.5), ("mcpjam", 10.0, 4.5),
]
for name, x, y in organs:
    circle = Circle((x, y), 0.25, facecolor=LIGHT_BG, edgecolor=ACCENT, linewidth=1)
    ax.add_patch(circle)
    ax.text(x, y, name, ha='center', va='center', fontsize=6.5, color=TEXT_PRIMARY)

ax.set_xlim(-0.5, 11.5)
ax.set_ylim(-0.3, 6.8)
ax.axis('off')
ax.set_title('Federation Topology — 7 Repos + 12 Organs', fontsize=13, color=TEXT_PRIMARY, fontweight='700', loc='left', pad=10)

# Legend
ax.text(0.5, -0.1, '■ Repos (source code)   ○ Organs (running services)', fontsize=8, color=TEXT_SECONDARY)

plt.tight_layout()
plt.savefig('deck_charts/05-federation-map.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Slide 5: Federation Map")

# ============================================================
# SLIDE 6: Domain Orthogonal Grid (the "fractal/orthogonal" ask)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)
fig.patch.set_facecolor('white')

# 5 domain x 5 phase matrix (orthogonal — each axis independent)
domains = ["Audio\nIntelligence", "Geological\nReasoning", "Capital\nMarkets", "Human\nVitality", "Civic\nShadow"]
phases = ["Observe\n(333)", "Think\n(555)", "Act\n(888)", "Verify\n(SEAL)", "Learn\n(SCAR)"]

cells = [
    # domains x phases — what lives at each intersection
    # Audio
    ["STT/TTS\nDSP pipeline", "Waveform\nfalsify", "Voice\ndeliver", "Ear\nverify", "Voice\nscar"],
    # Geological
    ["Seismic\ningest", "Basin\nmodel", "Drill\nplan", "Cross-section\nverify", "Geology\nscar"],
    # Capital
    ["Market\ndata", "Signal\nthink", "Trade\nexecute", "P&L\nverify", "Risk\nscar"],
    # Human (WELL)
    ["Vitality\nintake", "Body\nstate", "Rec.\ndeliver", "Outcome\nverify", "Health\nscar"],
    # Civic
    ["News\ningest", "Shadow\nthink", "Brief\ndeliver", "Source\nverify", "Public\nscar"],
]

cell_w, cell_h = 1.6, 0.9
x_start, y_start = 2.2, 5.0

# Header row (phases)
for j, phase in enumerate(phases):
    x = x_start + j * cell_w
    ax.text(x + cell_w/2, y_start + 0.3, phase, ha='center', va='center',
            fontsize=8, fontweight='700', color=ACCENT)

# Header column (domains)
for i, domain in enumerate(domains):
    y = y_start - i * cell_h - cell_h/2 - 0.1
    ax.text(x_start - 0.2, y, domain, ha='right', va='center',
            fontsize=8, fontweight='700', color=ACCENT)

# Cells
for i in range(5):
    for j in range(5):
        x = x_start + j * cell_w
        y = y_start - i * cell_h - cell_h
        color = ACCENT_BG if (i + j) % 2 == 0 else 'white'
        rect = Rectangle((x, y), cell_w, cell_h, facecolor=color, edgecolor=DIVIDER, linewidth=0.8)
        ax.add_patch(rect)
        ax.text(x + cell_w/2, y + cell_h/2, cells[i][j],
                ha='center', va='center', fontsize=6.5, color=TEXT_PRIMARY, linespacing=1.2)

# Highlight diagonal (orthogonal truth)
ax.plot([x_start, x_start + 5 * cell_w],
        [y_start, y_start - 5 * cell_h],
        color=ACCENT_GOLD, linewidth=2, linestyle='--', alpha=0.4, zorder=0)

ax.set_xlim(0, 11)
ax.set_ylim(0, 6.2)
ax.axis('off')
ax.set_title('Orthogonal Fractal — 5 Domains × 5 Phases', fontsize=13, color=TEXT_PRIMARY, fontweight='700', loc='left', pad=10)

ax.text(11, 0.2, 'Same EMD reflex,\napplied fractally', fontsize=8, color=ACCENT_GOLD, ha='right', style='italic', fontweight='600')

plt.tight_layout()
plt.savefig('deck_charts/06-orthogonal-grid.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Slide 6: Orthogonal Grid")

# ============================================================
# SLIDE 7: Skills Mesh — 347 Skills
# ============================================================
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)
fig.patch.set_facecolor('white')

# Category bubbles
categories = [
    ("Apex / Judge", 32, 2.0, 5.0, TAG_INT),
    ("Forge / Build", 58, 3.5, 5.0, ACCENT),
    ("Observe / Search", 41, 5.0, 5.0, TAG_OBS),
    ("Think / Plan", 27, 6.5, 5.0, TAG_DER),
    ("Memory / Verify", 35, 8.0, 5.0, "#C9A961"),
    ("Warga / Domains", 89, 5.0, 2.0, "#1B5E7B"),
    ("Media / Creative", 38, 5.0, 0.5, "#90CAF9"),
    ("Capital / Trading", 12, 8.5, 0.5, "#2E7D32"),
    ("Productivity", 15, 1.5, 0.5, "#5C5C6D"),
]

for label, count, x, y, color in categories:
    size = np.sqrt(count) * 70
    circle = Circle((x, y), 0.18 + size / 200, facecolor=color, alpha=0.6, edgecolor=color, linewidth=1.5)
    ax.add_patch(circle)
    ax.text(x, y + 0.05, label, ha='center', va='center',
            fontsize=8.5, fontweight='700', color='white')
    ax.text(x, y - 0.18, f'{count}', ha='center', va='center',
            fontsize=10, fontweight='700', color='white')

# Center hub
ax.text(5, 3.0, '347\nSKILLS', ha='center', va='center',
        fontsize=18, fontweight='700', color=ACCENT_DARK)
ax.text(5, 2.4, 'arifOS Skill Mesh', ha='center', va='center',
        fontsize=9, color=ACCENT, fontweight='600')

ax.set_xlim(0, 10)
ax.set_ylim(-0.5, 6.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Skill Mesh — 347 Skills, 9 Categories', fontsize=13, color=TEXT_PRIMARY, fontweight='700', loc='left', pad=10)

plt.tight_layout()
plt.savefig('deck_charts/07-skill-mesh.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Slide 7: Skill Mesh")

# ============================================================
# SLIDE 8: Key Metrics Dashboard
# ============================================================
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)
fig.patch.set_facecolor('white')

metrics = [
    ("347", "Skills", TAG_OBS),
    ("13", "Constitutional Floors", TAG_DER),
    ("7", "Federation Repos", TAG_INT),
    ("12", "Docker Organs", "#1B5E7B"),
    ("82", "Governance Docs", "#5BA8C9"),
    ("97M", "MCP SDK Downloads\n(industry)", "#90CAF9"),
    ("10K+", "MCP Servers\n(industry)", "#C9A961"),
    ("∞", "Flywheel Loops", "#1B5E7B"),
]

cols, rows = 4, 2
box_w, box_h = 2.1, 1.7
x_start, y_start = 1.0, 4.5

for i, (val, label, color) in enumerate(metrics):
    col = i % cols
    row = i // cols
    x = x_start + col * box_w
    y = y_start - row * box_h

    card = FancyBboxPatch((x + 0.1, y), box_w - 0.2, box_h - 0.1,
                          boxstyle="round,pad=0.02,rounding_size=0.08",
                          facecolor=ACCENT_BG, edgecolor=color, linewidth=1.5)
    ax.add_patch(card)
    ax.text(x + box_w/2, y + box_h - 0.5, val,
            ha='center', va='center', fontsize=20, fontweight='700', color=color)
    ax.text(x + box_w/2, y + 0.4, label,
            ha='center', va='center', fontsize=8.5, color=TEXT_SECONDARY, linespacing=1.2)

ax.set_xlim(0, 10)
ax.set_ylim(-0.5, 6.5)
ax.axis('off')
ax.set_title('By the Numbers — arifOS Federation', fontsize=13, color=TEXT_PRIMARY, fontweight='700', loc='left', pad=10)

plt.tight_layout()
plt.savefig('deck_charts/08-metrics.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Slide 8: Metrics Dashboard")

print("\nAll deck charts generated.")