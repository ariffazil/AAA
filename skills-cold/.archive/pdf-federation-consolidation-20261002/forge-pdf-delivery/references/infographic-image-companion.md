# Infographic & Image Companion Pipeline

When the user wants a PDF **plus** visual summary images (timeline, do/don't, checklist, donut chart), generate both in parallel and deliver as a bundle.

## When to use

Trigger phrases: "guide + image", "infographic", "bagi visual sekali", "do video and image", or any time a structured how-to/decision document benefits from a visual aid alongside the PDF.

## Pipeline (parallel to forge-pdf-delivery)

### Step 1: Generate the PDF first

Follow `forge-pdf-delivery/SKILL.md` exactly — markdown → HTML → weasyprint → verify with `file`.

### Step 2: Generate infographic images via matplotlib

```python
import matplotlib
matplotlib.use('Agg')  # critical — no display
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Pattern: 1 figure per visual
fig, ax = plt.subplots(figsize=(10, 14))
ax.set_xlim(0, 10); ax.set_ylim(0, 14); ax.axis('off')
fig.patch.set_facecolor('#ffffff')

# Use FancyBboxPatch for cards/badges (rounded corners)
badge = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                       facecolor=color, edgecolor='none')
ax.add_patch(badge)
ax.text(cx, cy, label, fontsize=..., fontweight='bold', ha='center', color='#ffffff')

# Color palette (proven works with Malay content)
DARK_RED = '#c0392b'  # urgent / title
RED = '#e74c3c'        # accent
GOLD = '#f39c12'       # warning
GREEN = '#27ae60'      # success
DARK_BLUE = '#2c3e50'  # section header
LIGHT_GRAY = '#f8f9fa' # alt row
WHITE = '#ffffff'

plt.savefig('/tmp/<slug>.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
```

### Step 3: Pitfalls

- **AVOID Unicode emoji glyphs in matplotlib text.** DejaVu Sans does NOT have glyphs for 🔥 ✅ ❌ 💪 — they'll render as boxes/squares with `UserWarning: Glyph X missing`. Use ASCII substitutes instead:
  - ✅ → `>` or `[ ]` or `[x]`
  - ❌ → `x`
  - 🔥 → omit, use bold red title
  - 💪 → omit
- **For pie/donut chart with small slices** (<5%), the autotext overlaps. Use `pctdistance=0.85` and skip labels on smallest slices.
- **Avoid emoji in titles** even if it looks fine in console — they'll fail in matplotlib. Strip them before rendering.
- **Verify with vision_analyze** before delivering — load each PNG and confirm layout/text actually renders cleanly.

### Step 4: Bundle delivery

```bash
mkdir -p /root/AAA/forge_work/<date>-<slug>/
cp /tmp/<slug>.pdf /root/AAA/forge_work/<date>-<slug>/
cp /tmp/<slug>_*.png /root/AAA/forge_work/<date>-<slug>/
ls -la /root/AAA/forge_work/<date>-<slug>/
```

Then deliver ALL files via MEDIA: in the same Telegram reply — PDF for the document, PNG for visuals.

## Proven recipe (spray tan guide, 2026-08-26)

Generated 4 images in one Python script:
1. `timeline.png` — vertical timeline with day badges
2. `dos_donts.png` — two-column green/red comparison
3. `checklist.png` — 4-section checklist (morning, pre-stage, pack, emergency)
4. `cost_chart.png` — donut chart with center total

All delivered alongside the PDF in one Telegram reply. User feedback: "bersih" (clean).

## Bundling rule

When the user asks for "guide + image" or "video and image", always deliver a SINGLE Telegram message containing:
1. Short text summary (1-2 sentences)
2. All `MEDIA:/path/...` lines (PDF + all PNGs)
3. Critical callout (single line, no markdown)

Never deliver the PDF first and ask "now you want images?". The bundle is the unit.