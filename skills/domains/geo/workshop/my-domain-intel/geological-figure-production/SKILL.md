---
name: geological-figure-production
version: 1.0.0-2026.08.20
owner: GEOX
description: Use when producing geological figures — pipeline with a vision-QA verification loop.
autonomy_tier: T1
risk_tier: low
floor_scope: [F2, F7, F9]
author: Hermes Edge Bridge (GEOX Federation)
license: DITEMPA BUKAN DIBERI
host_compatibility: [openclaw-gateway, claude-code, codex, opencode]
hermes:
  tags: [geology, basin-analysis, vision-QA, weasyprint]
  related_skills:
    - scientific-pdf-generation
    - domains/geo/geox-production-cockpit
dependencies:
  skills:
    - scientific-pdf-generation
    - domains/geo/geox-production-cockpit
  tools: [terminal, vision_analyze, write_file, patch]
tags: [geological, figures, matplotlib, vision-QA, session-workflow]
---

# Geological Figure Production — Vision-Driven Pipeline

> **DITEMPA BUKAN DIBERI**

## When to Use

When the user asks for any of the following for a petroleum basin or geological province:
- Generalized stratigraphic column (table-formatted, not bar chart)
- Schematic basin cross-section (with salt, faults, traps)
- Burial history + thermal maturity (Ro profile + depth-time curve)
- PSC block / location map with wells
- Risk heatmap (P × S matrix)
- Petroleum System events chart (chronological)
- Discovery / exploration timeline

Output is a multi-figure dark-theme intelligence PDF assembly (weasyprint HTML → PDF), with one figure per page + description + epistemic band tag per claim.

## Version Note (2026-08-20, second session)

This skill's pipeline describes the **v2 figures** (schematic block map,
weasyprint assembly). The same day's later session produced **v3** —
governed figures with real basemaps and physics. When the deliverable must
hold under F2 audit, apply these upgrades instead of the v2 schematic
patterns:

- **Block/location map**: schematic colored grids are REJECTED by the user
  ("Can we at least put real map please!!!!" → "Fail. No full map. Redo
  again."). Use GeoPandas + Natural Earth 50m + Rasterio bathymetry, full
  regional extent, real lat/lon only. See `scientific-pdf-generation` →
  `references/governed-geospatial-figures.md` (supersedes the v2 block-map
  pattern in Phase 2 above).
- **Cross-section / burial curves**: bezier/aesthetic curves are rejected.
  Sclater-Christie decompaction + McKenzie subsidence with declared
  parameters; true scale 1:1. Same reference file.
- **Structural model integration**: GemPy 2026.0.3 API has drifted — see
  `references/gempy-2026-api-and-segy-bridge.md` before touching
  `gempy_implicit_3d.py`.

Keep this skill's vision-QA loop, working-style rules, and weasyprint
assembly — they remain valid for all versions.

## The Pipeline (5 phases — proven 2026-08-20)

### Phase 1 — Setup

1. Work in a dedicated folder, e.g. `/tmp/<basin>_figs_v3/`.
2. Single Python script per session. Do not split — multi-script split causes version drift.
3. Set MPLCONFIGDIR to silence pyrolite warnings: `os.environ['MPLCONFIGDIR'] = '/tmp/.mpl'`
4. Set matplotlib backend to `Agg` BEFORE pyplot import.
5. Use system Python via `terminal()`, not `execute_code` — sandbox lacks matplotlib.

### Phase 2 — Generate Figures

Use these proven matplotlib patterns (model after `scientific-pdf-generation` references):

- **Strat column** — Rectangle-based table, period banding, lithology swatch (`barh()` with `color=hex`), explicit geometry columns.
- **Cross-section** — `fill_between()` for stacked layers; top boundary = layer above. Salt diapir = translucent polygon overlay. Growth faults = solid lines + labels.
- **Burial history + Ro** — twin panel; horizons marked as scatter on the curve; Ro curve = `depth → Ro` with shaded windows.
- **Block map** — Polygon patches for blocks, scatter for wells, dashed lines for water-depth contours.
- **Heatmap** — quadrant shading with `fill_between`; risk bubbles as scatter with `s` proportional to combined P × S; labels in margin with `arrowprops`.
- **Events chart** — horizontal bars in chronological y-stack; exploration milestones at top with gold scatter markers.
- **Timeline** — scatter bubbles, year on x, color by type, three shaded phase bands.

### Phase 3 — Vision-Driven QA Loop (CRITICAL NEW TECHNIQUE)

This is where previous attempts failed. After generating, do not trust your own visual review — use the vision model:

1. Render PDF to PNGs: `pdftoppm -png -r 110 <pdf> <review>/page`
2. For EACH figure PNG, call `vision_analyze(image_url=<path>, question="honest assessment: would a working geologist take this seriously? any obvious errors?")`
3. Document ALL failures the model reports (overlap, NaN curves, wrong orientation, label collisions).
4. Fix and re-render. Repeat until clean.

This loop matters because: matplotlib renders "successfully" without errors yet produces visually broken output — overlaying text, NaN-driven missing geometry, wrong orientation. A code review cannot catch label collisions; a vision review can.

Cost: 2–4 vision calls per figure × 7 figures = ~20 calls per deliverable. Each call ~3s. Total QA budget ~60s. Cheap for the quality uplift.

### Phase 4 — Fixes Common from This Session

| Issue | Cause | Fix |
|---|---|---|
| Lithology swatches show hex codes instead of labels | `lithology[0]` was passed as raw color hex | Add explicit label dict: `{'#fde2b3':'SAND', '#fcd180':'SS', ...}` |
| Cross-section seabed curve goes missing | `((x-shore)/(slope_end-shore))**1.8` with negative base = NaN | Use `np.sin(np.pi*(x-shore)/range)**2` instead — safe for monotonic curves |
| Block map shows thin strip instead of basin | Coast drawn east-west but PS blocks placed north-south | Redraw coastline matching actual basin orientation (Senegal: WNW-ESE) |
| Risk heatmap labels collide at center | All 7 risks cluster in P=0.4-0.7 region | Place labels in margin with leader lines (`arrowprops`), 4 in left, 3 in right |
| Strat column rows overlap | Multiple units share age_top → same Y | Switch from age-mapped Y to evenly-spaced Y positions |
| Right-edge text clipping on figure pages | `.fig-desc { text-align: justify }` causes overflow | Use `text-align: left; padding-right: 5px; overflow-wrap: break-word; max-width: 100%` |
| Cover title bleeds into body text | No explicit cover page break | `page-break-after: always` on cover div; explicit `min-height: 90vh` |

### Phase 5 — Assemble Multi-Page PDF (weasyprint)

Template structure (proven, 11 pages):

```
Cover (title + subtitle + quote + metadata + classification)
TOC (with epistemic band badges per item)
Fig 1 page (title + description + epistemic tag + image)
Fig 2 page (...)
...
Fig N page
"How to Read" discussion page
Footer (DITEMPA BUKAN DIBERI + arifOS + date + distribution)
```

Implementation notes:
- Inline base64 images, not external file refs. One large HTML (~3.5 MB) but no path issues.
- CSS @page with running header: `top-left`, `top-right`, `bottom-center` — keep minimal.
- First-page suppression: `@page :first { @top-left { content: ""; } }` — keep cover clean.
- `<div class="page-break"></div>` between figures if `page-break-after: always` not honored.

## Working Style — Arif-Specific Override

When producing figures for Arif (F13 SOVEREIGN):

1. No robotic preamble. Skip "I have analyzed the data..." Post directly to Telegram in BM Penang register if delivery is conversational, or formal English if dossier.
2. Use epistemic tags per claim, inline. OBS / INT / SCHEMATIC or SPEC attached to figures and prose.
3. Show the work via one PDF, not a barrage of separate PNGs. Geological deliverables consume in tabbed/printed form.
4. Include a 'how to read' discussion page. Arif skims and iterates, so a 1-page orientation summary prevents repeated clarification questions.
5. Embed DITEMPA BUKAN DIBERI footer + arifOS attribution on every GEOX deliverable.
6. Final MEDIApath delivery: `MEDIA:/tmp/<filename>.pdf` so it arrives as a file in the user's Telegram chat.

## Pitfalls Captured This Session

- **`write_file` rendering of `\n`**: When writing multi-line Python strings via `write_file`, literal `\n` sequences may render as actual newlines mid-string causing syntax errors. Fix: use `terminal` + heredoc OR Python outer with full string template.
- **`execute_code` sandbox lacks matplotlib**: Use `terminal python3 script.py` even when hermes_tools is available. The sandbox interpreter is missing matplotlib; numpy installed via pip works for terminal.
- **`pip install matplotlib` on Debian needs `--break-system-packages`**: PEP 668 blocks system Python installs. Use `pip install --break-system-packages -q matplotlib` for one-shot scripts in `/tmp/`.
- **`plt.matplotlib.colors.to_rgb(hex) * ratio` fails**: `to_rgb` returns a tuple not a list, multiplication produces a tuple not arithmetic. Fix: do hex-to-RGB manually with `int(h[i:i+2], 16)/255.0`, interpolate channels, then `'#{:02x}{:02x}{:02x}'.format(int(r*255),int(g*255),int(b*255))`.
- **`np.sin(...)` shape mismatch with different x grids**: when overlaying a curve on a subgrid (e.g. foam line on top of full wave array), use `np.interp(sub_x, full_x, full_y)` to align, then plot.
- **`mpl.rcParams['animation.embed_limit'] = 50`**: prevents the embed limit warning when saving animation frames.
- **`ax.fill_between()` returns a PolyCollection, NOT a single Patch**: `remove()` works but if you reassign the variable, store the result. `ax.plot()` returns a list of Line2D — `p.remove()` requires iterating the list, not `list.remove()`.
- **Aspect ratio on long landscape diagrams**: matplotlib's `set_aspect('equal')` on a 12-wide × 24-tall canvas produces a vertically-stretched PNG (image height >10× width). Use `set_aspect(0.5)` or set figsize to landscape (16:9 or 18:8) for cross-section diagrams.
- **Vision QA is the difference**: When the user asked for "real geological figures" not "colorful charts," `vision_analyze`-driven QA was the loop that delivered the quality lift.
- **Inline HTML size**: Weasyprint accepts 3.5 MB HTML with embedded base64 images without performance issues (rendered in <2s).
- **Two of seven figures failed first pass** (Strat column overlap, Cross-section NaN curve, Block map orientation) — that is the expected first-pass yield. The vision QA loop is what catches the rest.
- **Duplicate text from copy-paste in code blocks**: when iterating a figure, grep the script for the label text (`grep -n "Cross-Section" file.py`) to find all instances before patching. Easy to leave a duplicate when one block is moved.
- **Swapped (lat, lon) silently explodes `bbox_inches='tight'`**: one `ax.text(lat, lon, ...)` in a (lon, lat) map renders off-axes and the saved PNG grows to ~250 Mpx (PIL aborts with DecompressionBombError). Diagnose by printing `fig.get_tightbbox()` and scanning `ax.get_children()` for window extents > 4000 px. Always sanity-check every saved PNG with `struct.unpack('>II', open(f,'rb').read(40)[16:24])`.
- **Verify the polygon you drew**: computing the MTJDA treaty area from the published turning points with a local equirectangular projection gave 7,112 km² vs a published 7,250 km² — the 2% gap is straight-line-vs-geodesic and is worth stating in the deliverable rather than hiding. Real sanity checks make a figure credible.
- **Verify the write actually landed before telling anyone it is recorded.** A tool reporting `success` on a skill edit is not evidence the bytes persisted: this skill's sibling `geox-production-cockpit` had a new section written, reported success, and was later found absent because a skill-store convergence sweep deleted the file while the symlink and catalog entry survived. After any skill edit, `readlink -f` the path, re-read the resolved target, and `grep` for a distinctive phrase you just added. 42 of 267 symlinked skills in `domains/` currently point at directories holding only `liveness.json` — a broken symlink still renders in the skill catalog.
- **Sweep for broken skills with a loop, not by eye:** `for L in */*/*/*; do [ -L "$L" ] && [ ! -f "$(readlink -f $L)/SKILL.md" ] && echo "$L"; done` from `~/.hermes/skills/domains`.
- **One figure per page, discussion on the NEXT page**: packing `h2 + caption + image + prose` into one `.figpage` div leaves 1–2 orphan lines on a near-blank page. Fix: `.figpage { page-break-before: always; page-break-after: always }` (image only, `max-height: 196mm`) followed by a separate `.figtext` div with the prose. Detect the failure by rendering at 50 dpi and flagging pages under ~3 % ink before delivery.
- **Never let two scripts write the same PNG**: an older build script re-run after a newer one silently overwrites the fixed figure. Remove the figure from the old script's `__main__` and leave a comment naming its new home.
- **Lane-assign labels by MEASURED width, never a guessed gap constant**: a fixed `gap=6.2` data-units threshold let 60-char event labels (≈25 data units wide) overlap on timelines. Draw each label once at a throwaway position, read `t.get_window_extent(renderer=fig.canvas.get_renderer())`, convert through `ax.transData.inverted()`, and pack lanes against real half-widths. Initialise lanes with `[None]*N`, not `[[] for _ in range(N)]` — an empty list is not `None` and unpacking it raises.
- **A later `set_ylim` silently undoes the lane-stack height you just computed**: when adding measured-width lanes, delete or rewrite every subsequent axis-limit call in that function (and grep the function for `set_ylim`/`set_xlim` before trusting the output).
- **Check the sign of every accumulation curve**: `cumulative subsidence` plotted against `time before present` must rise toward the RIGHT edge. If the curve decays toward the present, flip to elapsed-age (`age = 40 - t`) and label the axis "cumulative subsidence since X Ma".
- **Offshore province maps: put each callout where it cannot touch what it labels.** A field of overlapping annotation boxes survives code review and dies in vision QA. Budget the label area first, then draw the geology into the gaps.

## New Techniques Captured 2026-08-27

### Geographic Heatmap (Folium)

For air-quality, hotspot, or geographic density visualizations:

1. **Install**: `pip install folium --break-system-packages -q` (PEP 668).
2. **Pattern**: `folium.Map(location=[lat, lon], zoom_start=N, tiles="cartodbpositron")` for clean look.
3. **Heatmap**: `folium.plugins.HeatMap([[lat, lon, weight], ...], radius=35, blur=25, gradient={0.0:"#2ecc71", 0.3:"#f1c40f", 0.5:"#e67e22", 0.7:"#e74c3c", 1.0:"#7b241c"})`. Weight = normalized metric (e.g. `(ipu - 90) / 110`).
4. **Markers**: `CircleMarker(location, radius=8, color=hex, fill=True, fill_opacity=0.8, popup=folium.Popup(html))` for individual data points with hover tooltips.
5. **Custom HTML overlays**: `m.get_root().html.add_child(folium.Element(html))` for fixed-position title bars and legend boxes. Use `position: fixed` CSS + `z-index: 9999`.
6. **HTML → PNG**: folium saves HTML only. To get a static image: install playwright (`pip install playwright && playwright install chromium`), then `browser.new_page(viewport={'width':1400,'height':1000})` → `goto('file://path.html')` → `wait_for_load_state('networkidle')` → `wait_for_timeout(2000)` (let tiles load) → `screenshot(path=out)`. Verified pattern: `/tmp/folium_capture.py`.

### Animated Process Cross-Section (Matplotlib FuncAnimation)

For event-driven geological visualizations (GLOFs, floods, cascades, eruptions):

1. **Phase-based animation**: split timeline into 4-6 phases (e.g. "Phase 1: trigger → Phase 2: accumulation → Phase 3: breach → Phase 4: cascade → Phase 5: aftermath"). Use `if frame < N:` branching.
2. **Dynamic element management**: keep globals `phase_label`, `wave_patch`, `wave_foam_line`, etc. Clear at start of each `animate()` call: `if wave_foam_line: [p.remove() for p in wave_foam_line]` (iterate, since ax.plot() returns a list).
3. **Phase progress**: `progress = (frame - phase_start) / phase_duration` — drive all motion/scaling from this single value.
4. **Title/subtitle updates**: `title_text.set_text(...)` per phase for narrative flow.
5. **Save as MP4**: requires `ffmpeg` installed. `Writer = animation.writers['ffmpeg']; writer = Writer(fps=15, bitrate=2400); ani.save(path, writer=writer, dpi=120)`. Also save GIF for compat: `ani.save(path, writer='pillow', fps=12, dpi=80)`.
6. **Frame extraction for QA**: `ffmpeg -i video.mp4 -vf "select=eq(n\,60)" -frames:v 1 -update 1 /tmp/frame.png -y` to grab a specific frame, then `vision_analyze` it.
7. **Emoji glyphs missing in DejaVu Sans**: stopwatch ⏱️, skull 💀, clipboard 📋 render as boxes. Either accept or replace with ASCII `[PHASE 1]`, `[X]`, `[NOTES]`.

### Vision QA Loop (proven multiple sessions)

1. **Always verify the rendered output**, not the code. matplotlib returns `verified: true` from write_file but produces visually broken PNGs.
2. **Specific questions to ask vision**: "would a working [geologist/expert] take this seriously?", "any label collisions?", "is the aspect ratio correct?", "any visual issues?".
3. **Common fixes**: duplicate labels (grep for the text to find all instances), text overlapping locations, foam/line elements appearing to float, scale indicators colliding with other labels.
4. **Iterate until clean** — first-pass yield on a 5+ element figure is typically 60-70%. Expect 2-4 iterations.

## Proven: 2026-08-20

GEOX_Senegal_Basin_Geological_Figures_v2.pdf
- 11 pages, 2.5 MB
- 7 artifacts: Strat Column, Burial+Ro, Cross-Section, Block Map, Risk Heatmap, Events Chart, Discovery Timeline
- 3 fix iterations before all 7 figures passed vision QA
- Used `/tmp/build_final_figures_dossier.py` for weasyprint assembly

## Print / Delivery Layout QA (added 2026-09-15)

The vision-QA loop above checks whether a figure is geologically honest. It does **not** catch
layout failure in the assembled PDF, and assembled multi-figure artifacts fail differently
from single PNGs. Before delivering any multi-page geological PDF, run the sweep in
`references/pdf-layout-forensics.md`:

1. **Page count == designed figure count** — a 12-slide deck must not arrive as 24 pages.
2. **No embedded raster rendered below legibility** — check with `pdfimages -list` at native
   aspect ratio, not by eye on the page. A cross-section whose native ratio is 2:1 placed in a
   wide short card becomes a thin strip: the interpreted geology compresses into ~110 px while
   the plot's own top margin stays white. Fix at the source (crop the depth axis, inset the
   deep horizon), never by scaling the page.
3. **Directions, ages and scales agree everywhere they appear** — slide title, in-figure title,
   footer, axis labels. One slide labelled `NW–SE`, `NE–SW` and `SE–NW` in three places
   destroys a specialist's trust in the whole pack.
4. **Ink coverage per page** — under ~2 % is a split or blank page from HTML/print overflow.

## Companion files

- `references/senegal-basin-figures-v2-script.md` — annotated session script (final working version with all fixes baked in)
- `references/vision-qa-checklist.md` — per-figure failure checklist
- `references/gempy-2026-api-and-segy-bridge.md` — GemPy 2026.0.3 API drift table (verified-working ImporterHelper CSV flow), the SEGY horizon-picks → GemPy → true-scale section bridge, truth-class propagation rule (OBS→DER, never upgrades), and the falsification-first rule for "ingest real SEGY" requests. Proven 2026-08-20 GEOX session.
- `references/wire-up-execution-2026-08-20.md` — Post-session update: the bridge→gempy→renderer wire-up **executed end-to-end** in the second Senegal session. Documents `gempy_section_renderer` (the missing third leg), the auto-extent fix for the `zmin=0` silent-failure, the section-index off-by-axis bug, the centroid clip pattern, the z-convention contract, and the v1→v4 dossier progression pattern. Read this **before** running the wire-up — saves ~30 minutes of debugging.
- `templates/geological-figure-pipeline.py` — starter script combining all 7 figure generators with vision-QA loop
