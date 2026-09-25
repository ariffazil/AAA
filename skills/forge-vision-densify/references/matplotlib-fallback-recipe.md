# Matplotlib Fallback for Technical Diagrams

> Why this exists: when the user asks for a diagram with technical labels
> (chemistry formulas, molecular structures, anatomy, math notation), diffusion
> models fabricate plausible-but-wrong labels even with explicit prompts and
> re-runs. The defect is structural across the diffusion class — not a tuning
> artifact, not fixable by prompt engineering. The canonical fallback is to
> bypass the diffusion class entirely and render with matplotlib, where every
> pixel is determined by code.

## When to use

Use this fallback whenever the artifact must contain technical labels the
user will read: chemistry formulas, molecular structures (atoms as nodes,
bonds as edges), anatomical diagrams, electrical schematics, taxonomy trees,
math equations, taxonomic trees, etc. Trigger conditions from
`SKILL.md` §Scientific/Technical Diagram Sub-Rule.

## Canonical recipe (chemistry worked example)

The recipe below is a working example for a sulfur-compounds diagram (H₂S,
CH₃SH, NH₃). It demonstrates the pattern: **explicit atomic coordinates,
explicit bond endpoints, unicode subscripts in labels, custom matplotlib
backend, deterministic render**.

```python
import matplotlib
matplotlib.use("Agg")  # headless — no display required
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Circle, FancyBboxPatch, Wedge
import os

# === Step 1: define color palette + page geometry ===
BG, INK, GOLD, GREY, RED, BLUE = (
    "#f5f1e8", "#1c1c1c", "#a8884a", "#7a7a7a", "#a3180f", "#2a4d7d"
)
PAGE_W, PAGE_H = 8, 6  # inches

fig = Figure(figsize=(PAGE_W, PAGE_H), facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_facecolor(BG)

# === Step 2: place atoms at explicit coordinates ===
# Atoms are (x, y, radius, face_color, edge_color, label, label_size)
atoms = [
    (0.13, 0.66, 0.025, "white", INK, "H", 11),   # left H of H2S
    (0.27, 0.66, 0.025, "white", INK, "H", 11),   # right H of H2S
    (0.20, 0.61, 0.030, GOLD, INK, "S", 12),       # central S
]

# Draw atoms
for (x, y, r, fc, ec, lbl, sz) in atoms:
    ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, linewidth=1.5))
    ax.text(x, y, lbl, fontsize=sz, color=fc if fc == "white" else ec,
            family="serif", ha="center", va="center", weight="bold")

# === Step 3: draw bonds as line segments ===
# Bonds are explicit (x1, y1, x2, y2) pairs with known geometry
bonds = [
    (0.155, 0.65, 0.175, 0.62),  # H-S left
    (0.245, 0.65, 0.225, 0.62),  # H-S right
]
for (x1, y1, x2, y2) in bonds:
    ax.plot([x1, x2], [y1, y2], color=INK, linewidth=1.5)

# === Step 4: labels with unicode subscripts ===
# Unicode subscripts: ₀₁₂₃₄₅₆₇₈₉ (0x2080-0x2089)
# Always test these render — some matplotlib fonts fall back to tofu boxes
ax.text(0.20, 0.84, "1. HYDROGEN SULFIDE", fontsize=11,
        color=INK, family="serif", weight="bold", ha="center")
ax.text(0.20, 0.80, "(H\u2082S)",  # H₂S via unicode
        fontsize=9, color=GREY, family="serif", ha="center", style="italic")

# === Step 5: render to PNG ===
out = "/path/to/output.png"
canvas = FigureCanvasAgg(fig)
canvas.print_png(out)
plt.close(fig)
```

## Pitfalls the recipe addresses

| Pitfall | Mechanism | Mitigation |
|---|---|---|
| Atoms drift from declared positions | Diffusion prior fabricates layout from text prompt | Use explicit `(x, y)` tuples — never descriptive English |
| Unicode subscripts render as tofu | Font fallback fails for U+2080–U+2089 | Test-render first; pick a font with full Unicode coverage, or use `$\mathrm{H_2S}$` with mathtext |
| Bond angles wrong | Diffusion does not honor chemistry | Specify bond endpoints in `(x1,y1,x2,y2)` tuples with computed angles |
| Visual VLM audit fails | VLM misreads subscripts as plain digits | Ask VLM to read back labels with `vision_analyze(question="...")`; verify every character |
| Atomic labels corrupted | Diffusion invents plausible-but-wrong compound names ("methanethol" vs "methanethiol") | Diffuse only an empty cloud, gas, or background — labels go in matplotlib code |

## Why not use a real chemistry library (RDKit, Open Babel)?

If RDKit or Open Babel is available, prefer it: they know chemistry, including
correct bond geometry, stereochemistry, and SMILES parsing. The matplotlib
recipe above is the fallback when those libraries are not installed or when
the diagram is not strictly chemistry (e.g. anatomy, taxonomy, electrical
schematics). Use the appropriate library for the domain if it exists; the
matplotlib pattern is the universal last-resort.

## After-render verification

Run a vision pass before declaring the artifact done:

```python
from hermes_tools import vision_analyze  # or equivalent
result = vision_analyze(
    image_url="/path/to/output.png",
    question="Read every label verbatim. Are compound names spelled correctly? "
             "Are all atoms and bonds present? Any missing or corrupted text?",
)
```

If the vision pass reports defects, **fix the matplotlib code**, not the
prompt. matplotlib is deterministic — if it produced garbage, the source code
is wrong, not a model artifact.

## Decision tree

```
User asks for technical diagram with labels
  │
  ├── Is RDKit/Open Babel available and is this chemistry?
  │     └── Yes → use RDKit; render with rdkit.Chem.Draw
  │     └── No ↓
  │
  ├── Can the diagram be expressed as matplotlib primitives
  │   (circles, lines, text)?
  │     └── Yes → use the recipe above
  │     └── No ↓
  │
  └── Last resort: pure ASCII / markdown table
      (always available, never wrong)
```
