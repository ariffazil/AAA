"""v3 — Premium diagrams with text actually rendering.
Key fix: use data coords for all positioning (matching xlim/ylim),
drop set_aspect('equal') to avoid coordinate warping.
"""

import os

os.environ["MPLCONFIGDIR"] = "/tmp/.mpl"
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np

# Color system
BG = "#0a1226"
PANEL = "#121a33"
PANEL2 = "#1a2342"
GOLD = "#e6b954"
GOLD_DIM = "#a8884a"
TEAL = "#4dc4c4"
RED = "#e86565"
AMBER = "#f0a04a"
WHITE = "#f5f7ff"
DIM = "#9aa5bf"
BORDER = "#2a3658"

plt.rcParams.update(
    {
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "text.color": WHITE,
        "axes.labelcolor": WHITE,
        "xtick.color": DIM,
        "ytick.color": DIM,
        "axes.edgecolor": BORDER,
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": False,
    }
)

OUT = "/root/forge_work/marketing-pack-arifos/figs"


def save(fig, name, dpi=200):
    fig.savefig(f"{OUT}/{name}.png", dpi=dpi, facecolor=BG, pad_inches=0.15)
    plt.close(fig)


def panel(ax, x, y, w, h, color=PANEL, border=BORDER, lw=1.2):
    """Panel in DATA coords (matching ax xlim/ylim)."""
    rect = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.06", facecolor=color, edgecolor=border, linewidth=lw
    )
    ax.add_patch(rect)


def t(ax, x, y, text, size=12.0, color=WHITE, weight="normal", ha="center", va="center"):
    """Text in DATA coords (matching ax xlim/ylim). Readability scale 1.15 for phone legibility (revB)."""
    ax.text(x, y, text, fontsize=size * 1.15, color=color, ha=ha, va=va, weight=weight, family="DejaVu Sans")


# ───────────────────────────────────────────────────────────────────
# FIG 1 — COVER
# ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")

t(ax, 6.0, 6.4, "REALITY INTELLIGENCE", 38, GOLD, "bold")
t(ax, 6.0, 5.75, "A new category for AI that remains aligned with changing reality", 14, DIM)

panel(ax, 0.5, 1.0, 5.4, 4.4, color=PANEL, border=BORDER)
panel(ax, 6.1, 1.0, 5.4, 4.4, color=PANEL2, border=GOLD, lw=2.5)

t(ax, 3.2, 5.0, "KNOWLEDGE SYSTEMS", 14, DIM, "bold")
t(ax, 3.2, 4.55, "Most AI today", 11, DIM)
left_items = [
    ("Model weights", "stored patterns"),
    ("Retrieval (RAG)", "static knowledge"),
    ("Generated reasoning", "inference only"),
    ("Pattern matching", "no ground truth"),
    ("Statistical recall", "no consequence"),
]
for i, (n, sub) in enumerate(left_items):
    y = 3.95 - i * 0.55
    t(ax, 0.85, y, ">", 14, DIM, ha="left")
    t(ax, 1.15, y, n, 13, WHITE, ha="left", weight="bold")
    t(ax, 1.15, y - 0.28, sub, 9.5, DIM, ha="left")

t(ax, 8.8, 5.0, "REALITY INTELLIGENCE", 14, GOLD, "bold")
t(ax, 8.8, 4.55, "ARIF / arifOS", 11, GOLD)
right_items = [
    ("Reality probing", "live evidence"),
    ("Authority routing", "capability != permission"),
    ("Consequence tracking", "receipted outcomes"),
    ("Verification loops", "independent witness"),
    ("Adaptive memory", "reality may revise"),
]
for i, (n, sub) in enumerate(right_items):
    y = 3.95 - i * 0.55
    t(ax, 6.45, y, ">", 14, GOLD, ha="left")
    t(ax, 6.75, y, n, 13, WHITE, ha="left", weight="bold")
    t(ax, 6.75, y - 0.28, sub, 9.5, DIM, ha="left")

arrow = FancyArrowPatch((5.95, 3.2), (6.05, 3.2), arrowstyle="->", mutation_scale=30, color=GOLD, lw=4)
ax.add_patch(arrow)
t(ax, 6.0, 3.7, "SHIFT", 12, GOLD, "bold")

panel(ax, 0.5, 0.15, 11.0, 0.6, color=PANEL, border=GOLD, lw=1.5)
t(
    ax,
    6.0,
    0.45,
    "Most AI answers questions.  Reality Intelligence discovers what is true before acting.",
    13,
    WHITE,
    "bold",
)

save(fig, "fig01_cover_reality_vs_knowledge")

# ───────────────────────────────────────────────────────────────────
# FIG 2 — Reality Navigation 8-Stage Architecture
# ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6))
ax.set_xlim(0, 13)
ax.set_ylim(0, 6)
ax.axis("off")

t(ax, 6.5, 5.55, "REALITY NAVIGATION", 24, GOLD, "bold")
t(ax, 6.5, 5.10, "Eight stages. Each action observes reality before it touches anything consequential.", 11, DIM)

stages = [
    ("QUESTION", "What must be\nverified next?", GOLD),
    ("REALITY PROBE", "Live evidence\nnot memory", TEAL),
    ("AUTHORITY CHECK", "Capability is\nnot permission", GOLD),
    ("CONSTRAINT CHECK", "Scar-tested\nboundaries", GOLD),
    ("VERIFICATION", "Independent\nwitness", TEAL),
    ("ACTION", "Reversible\nsmallest move", GOLD),
    ("CONSEQUENCE", "Receipted\noutcome", TEAL),
    ("ADAPTATION", "Memory rewritable\nby reality", GOLD),
]

x_positions = np.linspace(1.10, 11.90, len(stages))
box_w, box_h = 1.55, 2.7

for i, (title, sub, color) in enumerate(stages):
    x = x_positions[i]
    panel(ax, x - box_w / 2, 1.5, box_w, box_h, color=PANEL, border=color, lw=2.5)
    badge = Circle((x, 3.7), 0.3, facecolor=color, edgecolor="none")
    ax.add_patch(badge)
    t(ax, x, 3.7, str(i + 1), 16, BG, "bold")
    # Force-wrap titles >12 chars
    if len(title) > 12 and " " in title:
        # Wrap on first space
        idx = title.index(" ")
        line1 = title[:idx]
        line2 = title[idx + 1 :]
        t(ax, x, 3.05, line1, 9.5, WHITE, "bold")
        t(ax, x, 2.72, line2, 9.5, WHITE, "bold")
    else:
        t(ax, x, 2.9, title, 9.5, WHITE, "bold")
    t(ax, x, 2.15, sub, 7.5, DIM)
    if i < len(stages) - 1:
        ax.annotate(
            "",
            xy=(x + box_w / 2 + 0.22, 2.85),
            xytext=(x + box_w / 2 + 0.02, 2.85),
            arrowprops=dict(arrowstyle="->", color=GOLD_DIM, lw=2),
        )

t(ax, 6.5, 0.85, "Memory serves reality.  Reality does not serve memory.", 13, GOLD, "bold")
t(ax, 6.5, 0.4, "Wrong answer: stored data.   Right answer: verified present.", 11, DIM)

save(fig, "fig02_navigation_architecture")

# ───────────────────────────────────────────────────────────────────
# FIG 3 — Seven Failure Modes
# ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

t(ax, 6.0, 7.5, "WHY TODAY's AI CANNOT BE TRUSTED IN PRODUCTION", 19, GOLD, "bold")
t(ax, 6.0, 6.95, "Seven recurring failure modes. Each has caused real-world damage.", 13, DIM)

failures = [
    ("HALLUCINATION", "Confident fabrication.\nNo grounding in reality.", RED),
    ("CONTEXT ROT", "Memory degrades\nunder scale and time.", AMBER),
    ("MEMORY POISONING", "False data ingested\nas truth, never corrected.", RED),
    ("TOOL SPRAWL", "Capability added\nwithout governance.", AMBER),
    ("AGENT DRIFT", "Goals diverge\nfrom intent over time.", RED),
    ("GOVERNANCE FAILURES", "Authority collapses\nunder consequence.", RED),
    ("MISALIGNED AUTONOMY", "Action with no\nreceipted consequence.", AMBER),
]

cols = 4
rows = 2
cw, rh = 2.65, 2.05
x0, y0 = 0.45, 0.9
for idx, (title, sub, color) in enumerate(failures):
    r = idx // cols
    c = idx % cols
    x = x0 + c * (cw + 0.2)
    y = y0 + (rows - 1 - r) * (rh + 0.25)
    panel(ax, x, y, cw, rh, color=PANEL, border=color, lw=2)
    # Small numbered badge, top-left corner — no collision with centred title
    num_c = Circle((x + 0.38, y + rh - 0.38), 0.20, facecolor=color, edgecolor="none")
    ax.add_patch(num_c)
    t(ax, x + 0.38, y + rh - 0.38, f"{idx + 1}", 11, BG, "bold")
    # Title centred; wrap long titles onto two lines to stay inside the card
    if len(title) > 13 and " " in title:
        i_sp = title.index(" ")
        t(ax, x + cw / 2, y + rh - 0.78, title[:i_sp], 11, WHITE, "bold")
        t(ax, x + cw / 2, y + rh - 1.10, title[i_sp + 1 :], 11, WHITE, "bold")
    else:
        t(ax, x + cw / 2, y + rh - 0.85, title, 11.5, WHITE, "bold")
    t(ax, x + cw / 2, y + 0.48, sub, 9, DIM)

save(fig, "fig03_seven_failures")

# ───────────────────────────────────────────────────────────────────
# FIG 4 — Quadrant Landscape
# ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 9))
ax.set_xlim(0, 11)
ax.set_ylim(0, 10)
ax.axis("off")

t(ax, 5.5, 9.5, "COMPETITIVE LANDSCAPE", 21, GOLD, "bold")
t(ax, 5.5, 9.05, "Capability  x  Reality Alignment", 12, DIM)

# Plot area
panel(ax, 1.6, 1.6, 7.6, 6.9, color=PANEL, border=BORDER)

# Axes
ax.plot([1.6, 9.2], [4.9, 4.9], color=BORDER, lw=2)
ax.plot([5.4, 5.4], [1.6, 8.5], color=BORDER, lw=2)

# Axis labels — outside the plot, no collision
t(ax, 5.4, 8.82, "REALITY ALIGNMENT", 11, WHITE, "bold")
t(ax, 1.15, 4.9, "CAPABILITY", 11, WHITE, "bold", ha="center")

# Quadrant labels — well inside each quadrant, clear of axes
t(ax, 3.5, 7.85, "HIGH ALIGNMENT\nLOW CAPABILITY", 9, DIM, "bold")
t(ax, 7.3, 7.85, "HIGH ALIGNMENT\nHIGH CAPABILITY", 9, GOLD, "bold")
t(ax, 3.5, 1.95, "LOW ALIGNMENT\nLOW CAPABILITY", 9, DIM, "bold")
t(ax, 7.3, 1.95, "LOW ALIGNMENT\nHIGH CAPABILITY", 9, AMBER, "bold")

# Ideal zone — top-right, labelled beneath the ARIF point
panel(ax, 6.6, 5.9, 2.5, 2.3, color=PANEL2, border=GOLD, lw=1.8)
t(ax, 7.85, 6.25, "INTEGRATION ZONE", 8.5, GOLD, "bold")

# Competitor dots — labels offset clear of both axes
players = [
    ("LLM", 3.0, 3.1, DIM, 0),
    ("RAG", 4.3, 3.85, DIM, 0),
    ("Agents", 7.1, 3.3, AMBER, 0),
    ("Governance", 2.9, 6.5, DIM, 0),
    ("Sovereign AI", 7.0, 5.3, DIM, 0),
    ("ARIF", 7.85, 7.5, GOLD, 0),
]

for name, x, y, color, _off in players:
    is_arif = color == GOLD
    c = Circle(
        (x, y),
        0.30 if is_arif else 0.19,
        facecolor=color,
        edgecolor=WHITE if is_arif else color,
        linewidth=2.5,
        alpha=1.0,
    )
    ax.add_patch(c)
    label_y = y - 0.62 if name == "ARIF" else y - 0.48
    t(ax, x, label_y, name, 11.5 if is_arif else 10, WHITE if not is_arif else GOLD, "bold" if is_arif else "normal")
    if is_arif:
        t(ax, x, y, "A", 11, BG, "bold")

panel(ax, 0.5, 0.15, 10.0, 0.7, color=PANEL, border=GOLD, lw=1.5)
t(
    ax,
    5.5,
    0.5,
    "The integration quadrant is sparsely occupied: most categories supply one part, not the joined loop.",
    12,
    GOLD,
    "bold",
)

save(fig, "fig04_quadrant_landscape")

# ───────────────────────────────────────────────────────────────────
# FIG 5 — Traditional vs Reality
# ───────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
for ax in (ax1, ax2):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

panel(ax1, 0.5, 0.5, 9, 7, color=PANEL, border=BORDER, lw=1.5)
t(ax1, 5.0, 7.0, "TRADITIONAL AI", 20, DIM, "bold")
t(ax1, 5.0, 6.3, '"What do I know?"', 14, AMBER)

flow_l = [("Question", 5.4), ("Retrieve memory", 4.4), ("Generate", 3.4), ("Answer", 2.4)]
for n, y in flow_l:
    panel(ax1, 2.0, y - 0.3, 6.0, 0.6, color=PANEL2, border=BORDER, lw=1.0)
    t(ax1, 5.0, y, n, 13, WHITE, "bold")
    if y != 2.4:
        ax1.annotate(
            "", xy=(5.0, y - 0.55), xytext=(5.0, y - 0.85), arrowprops=dict(arrowstyle="->", color=AMBER, lw=2)
        )

panel(ax1, 1.0, 1.0, 8.0, 1.0, color=PANEL2, border=AMBER, lw=1.5)
t(ax1, 5.0, 1.5, "Answer derived from stored knowledge.", 12, AMBER, "bold")

panel(ax2, 0.5, 0.5, 9, 7, color=PANEL2, border=GOLD, lw=2.5)
t(ax2, 5.0, 7.0, "REALITY INTELLIGENCE", 20, GOLD, "bold")
t(ax2, 5.0, 6.3, '"What should be verified next?"', 14, TEAL)

flow_r = [("Question", 5.5), ("Probe reality", 4.5), ("Verify evidence", 3.5), ("Check authority", 2.5)]
for n, y in flow_r:
    panel(ax2, 2.0, y - 0.3, 6.0, 0.6, color=PANEL, border=GOLD, lw=1.0)
    t(ax2, 5.0, y, n, 13, WHITE, "bold")
    if y != 2.5:
        ax2.annotate("", xy=(5.0, y - 0.55), xytext=(5.0, y - 0.85), arrowprops=dict(arrowstyle="->", color=GOLD, lw=2))

panel(ax2, 1.0, 1.0, 8.0, 1.0, color=PANEL, border=GOLD, lw=2)
t(ax2, 5.0, 1.5, "Action grounded in verified, current reality.", 12, GOLD, "bold")

save(fig, "fig05_traditional_vs_reality")

# ───────────────────────────────────────────────────────────────────
# FIG 6 — Moat Components
# ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")

t(ax, 6.0, 6.55, "THE MOAT", 28, GOLD, "bold")
t(ax, 6.0, 5.95, "Six assets that cannot be downloaded — only earned through operation", 12, DIM)

hub_x, hub_y = 6.0, 3.3
hub = Circle((hub_x, hub_y), 0.85, facecolor=GOLD, edgecolor=WHITE, linewidth=3)
ax.add_patch(hub)
t(ax, hub_x, hub_y + 0.15, "REALITY", 14, BG, "bold")
t(ax, hub_x, hub_y - 0.20, "MOAT", 14, BG, "bold")

components = [
    ("SCAR\nACCUMULATION", "Failures that bind\nfuture behaviour", 1.8, 4.4),
    ("CONSEQUENCE-BEARING\nMEMORY", "Learning tied to\nreal outcomes", 6.0, 5.05),
    ("REALITY VERIFICATION\nINFRASTRUCTURE", "Independent witness\nsystems", 10.2, 4.4),
    ("AUTHORITY\nGRAPH", "Capability separated\nfrom permission", 10.2, 2.2),
    ("RECOVERY\nINTELLIGENCE", "Correction speed\nbeats certainty", 6.0, 1.6),
    ("REALITY NAVIGATION\nWORKFLOWS", "8-stage loops\napplied to real work", 1.8, 2.2),
]

import math

for title, sub, x, y in components:
    panel(ax, x - 1.5, y - 0.7, 3.0, 1.4, color=PANEL, border=GOLD, lw=2)
    t(ax, x, y + 0.25, title, 11.5, WHITE, "bold")
    t(ax, x, y - 0.32, sub, 9.5, DIM)
    dx, dy = hub_x - x, hub_y - y
    dist = math.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    sx = x + ux * 1.6
    sy = y + uy * 0.75
    ex = hub_x - ux * 1.05
    ey = hub_y - uy * 1.05
    ax.annotate("", xy=(ex, ey), xytext=(sx, sy), arrowprops=dict(arrowstyle="-", color=GOLD_DIM, lw=1.5, alpha=0.6))

panel(ax, 0.5, 0.05, 11.0, 0.45, color=PANEL, border=GOLD, lw=1.5)
t(ax, 6.0, 0.275, "Through operation, consequence, and adaptation across real environments.", 12, GOLD, "bold")

save(fig, "fig06_moat_components")

# ───────────────────────────────────────────────────────────────────
# FIG 7 — Memory Capture Defense timeline
# ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 5.5))
ax.set_xlim(0, 13)
ax.set_ylim(0, 6)
ax.axis("off")

t(ax, 6.5, 5.4, "MEMORY CAPTURE DEFENSE", 24, GOLD, "bold")
t(ax, 6.5, 4.85, "Reality may invalidate any memory. Authority may invalidate any cache.", 13, DIM)

ax.plot([1.0, 12.0], [3, 3], color=GOLD, lw=4, alpha=0.7)

stages_t = [
    (1.2, "0-30d", "Truth\nacquired", GOLD),
    (3.0, "30-90d", "Truth\ntested", GOLD),
    (5.0, "90-365d", "Truth\nvalidated", GOLD),
    (7.5, "1yr+", "Truth challenged\nby new evidence", AMBER),
    (9.8, "Reality verdict", "Memory revised\nor retired", TEAL),
    (11.7, "Live state", "Evidence\nwins", GOLD),
]

for x, age, txt, color in stages_t:
    c = Circle((x, 3), 0.22, facecolor=color, edgecolor=WHITE, linewidth=2.5)
    ax.add_patch(c)
    t(ax, x, 3.95, age, 12, color, "bold")
    t(ax, x, 1.95, txt, 10.5, WHITE, "bold")

panel(ax, 0.5, 0.4, 12.0, 0.7, color=PANEL, border=GOLD, lw=1.5)
t(ax, 6.5, 0.75, "Cached verification is a permit, not a guarantee.", 13, GOLD, "bold")

save(fig, "fig07_memory_capture_defense")

# ───────────────────────────────────────────────────────────────────
# FIG 8 — Dissent Infrastructure
# ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")

t(ax, 6.0, 6.5, "DISSENT INFRASTRUCTURE", 24, GOLD, "bold")
t(ax, 6.0, 5.95, "Three independent observers. Consensus only after reality decides.", 13, DIM)

obs = [
    ("OBSERVER A", "Hypothesis", GOLD, "Proposes a path\nand tests it", 2.2),
    ("OBSERVER B", "Witness", TEAL, "Independently\nverifies", 6.0),
    ("OBSERVER C", "Falsifier", AMBER, "Attempts active\nrefutation", 9.8),
]

for name, role, color, sub, x in obs:
    panel(ax, x - 1.5, 3.4, 3.0, 2.1, color=PANEL, border=color, lw=3)
    t(ax, x, 5.1, name, 11.5, color, "bold")
    t(ax, x, 4.55, role, 15, WHITE, "bold")
    t(ax, x, 3.85, sub, 10, DIM)

arrow_a = FancyArrowPatch((3.3, 3.4), (5.5, 2.0), arrowstyle="->", mutation_scale=24, color=GOLD_DIM, lw=2.5)
arrow_b = FancyArrowPatch((6.8, 3.4), (6.2, 2.0), arrowstyle="->", mutation_scale=24, color=TEAL, lw=2.5)
arrow_c = FancyArrowPatch((9.2, 3.4), (6.7, 2.0), arrowstyle="->", mutation_scale=24, color=AMBER, lw=2.5)
for a in [arrow_a, arrow_b, arrow_c]:
    ax.add_patch(a)

c = Circle((6.0, 1.5), 0.6, facecolor=GOLD, edgecolor=WHITE, linewidth=2.5)
ax.add_patch(c)
t(ax, 6.0, 1.55, "REALITY", 12, BG, "bold")
t(ax, 6.0, 1.18, "verdict", 9, BG, "bold")

panel(ax, 0.5, 0.05, 11.0, 0.5, color=PANEL, border=GOLD, lw=1.5)
t(ax, 6.0, 0.30, "Consensus accelerates execution.  Dissent preserves reality.", 13, GOLD, "bold")

save(fig, "fig08_dissent_infrastructure")

# ───────────────────────────────────────────────────────────────────
# FIG 9 — Recovery Intelligence loop
# ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

t(ax, 5.0, 9.4, "RECOVERY INTELLIGENCE", 24, GOLD, "bold")
t(ax, 5.0, 8.85, "Correction speed  >  apparent certainty", 14, DIM)

center = (5.0, 4.5)
radius = 2.7
n_steps = 6
labels_r = ["OBSERVE", "CORRECT", "WITNESS", "INTEGRATE", "REWEIGH", "ADAPT"]
colors_r = [TEAL, GOLD, TEAL, GOLD, TEAL, GOLD]

for i, (lbl, color) in enumerate(zip(labels_r, colors_r)):
    angle = 90 - i * (360 / n_steps)
    rad = np.deg2rad(angle)
    x = center[0] + radius * np.cos(rad)
    y = center[1] + radius * np.sin(rad)
    c = Circle((x, y), 0.75, facecolor=PANEL, edgecolor=color, linewidth=3)
    ax.add_patch(c)
    t(ax, x, y, lbl, 12, WHITE, "bold")
    next_angle = 90 - ((i + 1) % n_steps) * (360 / n_steps)
    next_rad = np.deg2rad(next_angle)
    nx = center[0] + radius * np.cos(next_rad)
    ny = center[1] + radius * np.sin(next_rad)
    sx = x + 0.78 * np.cos(next_rad)
    sy = y + 0.78 * np.sin(next_rad)
    ex = nx - 0.78 * np.cos(next_rad)
    ey = ny - 0.78 * np.sin(next_rad)
    ax.annotate("", xy=(ex, ey), xytext=(sx, sy), arrowprops=dict(arrowstyle="->", color=GOLD_DIM, lw=2.2))

c_center = Circle(center, 1.3, facecolor=PANEL2, edgecolor=GOLD, linewidth=3)
ax.add_patch(c_center)
t(ax, center[0], center[1] + 0.30, "TRUTH", 17, GOLD, "bold")
t(ax, center[0], center[1] - 0.20, "verified", 11.5, DIM)
t(ax, center[0], center[1] - 0.60, "by reality", 11.5, DIM)

panel(ax, 0.5, 0.1, 9.0, 0.65, color=PANEL, border=GOLD, lw=1.5)
t(ax, 5.0, 0.42, "Belief correction latency is the only metric that survives.", 14, AMBER, "bold")

save(fig, "fig09_recovery_loop")

# ───────────────────────────────────────────────────────────────────
# FIG 10 — Strategic Vision Layer Stack
# ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 7.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 7.5)
ax.axis("off")

t(ax, 5.5, 7.0, "THE MISSING LAYER", 26, GOLD, "bold")
t(ax, 5.5, 6.45, "Between AI capability and real-world deployment.", 13, DIM)

layers = [
    ("REAL-WORLD DEPLOYMENT", "where intelligence must survive", AMBER, 5.4, 0.6, 7.5),
    ("REALITY INTELLIGENCE", "GOVERNANCE & SUBSTRATE  /  ARIF / arifOS", GOLD, 4.0, 1.2, 9.0),
    ("AGENTS & TOOLING", "capability layer", TEAL, 2.7, 0.85, 7.5),
    ("MODELS / RAG / MEMORY", "foundation layer", DIM, 1.5, 0.85, 7.5),
    ("RAW COMPUTE & DATA", "substrate", DIM, 0.3, 0.85, 7.5),
]

for name, role, color, y, h, width in layers:
    x = (11 - width) / 2
    is_arif = name == "REALITY INTELLIGENCE"
    panel(ax, x, y, width, h, color=PANEL2 if is_arif else PANEL, border=color, lw=3.5 if is_arif else 1.5)
    t(ax, 5.5, y + h - 0.27, name, 13, WHITE, "bold")
    t(ax, 5.5, y + 0.22, role.upper(), 9, color)

t(
    ax,
    5.5,
    0.35,
    "Most AI investment sits at the bottom two layers. Reality Intelligence operates the layer that determines whether any of it works.",
    11.5,
    DIM,
)

save(fig, "fig10_strategic_layer_stack")

print("All 10 v3 figures rendered.")
