# Wire-Up Execution — 2026-08-20 (Senegal Basin)

> Post-session update for the `gempy-2026-api-and-segy-bridge.md` reference.
> Records what was **executed end-to-end** during the second Senegal Basin
> session on 2026-08-20. The earlier reference file described the *anticipated*
> wire-up pattern; this file records the *proven* execution.

## What got added: `gempy_section_renderer` (the missing third leg)

`/root/GEOX/src/geox_mcp/tools/gempy_section_renderer.py` is a new federation
tool that consumes `lithology_block` + `extent` from `geox_gempy_implicit_3d`
output and renders a publication-grade PNG: TRUE SCALE 1:1 dark theme, formation
labels, Sangomar/Tortue fiducial markers, scale bars, domain tags
(COAST/SHELF/SLOPE/DEEPWATER).

Without this tool, the federation's 3D model output stayed as raw tabular
`lithology_block` + 3 generic colored sections from gempy_implicit_3d's
built-in matplotlib sections. With it, the same data becomes a deployable
artifact.

API contract:

```python
render_gempy_section(
    lithology_block,         # (nx, ny, nz) array of lith IDs from gempy
    extent,                   # [xmin, xmax, ymin, ymax, zmin, zmax]
    formations,              # list mapping to IDs 1..N
    section_axis='y',        # 'x' or 'y' -- which axis to slice
    section_index=None,      # defaults to mid of sliced axis
    save_path=None,          # auto-saves to /opt/geox/data/gempy_outputs/
    return_image=False,
)
```

## Auto-extent fix (the silent-failure that broke the bridge)

`geox_gempy_implicit_3d`'s default auto-extent: `zmin=0, zmax=max(z)+500`.
This **fails for elevation-mode picks** (negative z values) -- zmin > zmax,
all picks fall outside the extent, model returns only basement (single
lith ID). The bridge now auto-derives extent from picks:

```python
def auto_extent(picks, x_convention='depth_positive_down'):
    xs = [p['x'] for p in picks]
    ys = [p['y'] for p in picks]
    zs = [p['z'] for p in picks]
    margin = max(100.0, (max(xs) - min(xs)) * 0.2)
    if max(zs) > 0:  # depth_positive_down
        elev_min, elev_max = -max(zs) - 1000, -min(zs) + 1000
    else:  # already elevation
        elev_min, elev_max = min(zs) - 1000, max(zs) + 1000
    return [min(xs) - margin, max(xs) + margin,
            min(ys) - margin, max(ys) + margin,
            elev_min, elev_max]
```

## Z-convention contract (picks_to_gempy_inputs)

The bridge's `z_convention` parameter has a strict contract:

- `depth_positive_down` = user gives positive depth values, bridge negates to negative elevation
- `elevation` = user gives elevation already (negative or positive), bridge passes through unchanged

**Do NOT pass negative-z picks with `depth_positive_down`** -- the bridge
will double-negate, sending picks to +3700 m elevation (above ground),
which falls outside the model extent. The bridge's auto-extent fix above
handles either convention correctly when picks are given in their natural
form (positive depth, or negative elevation).

## Section-index off-by-axis fix

Default `section_index = nx // 2` is wrong for `section_axis='x'` slices
(slice reduces over `nx`, not `ny`). The renderer now uses
`section_index = ny // 2` for both axes -- correct because the slice
reduces over the *other* axis.

## Centroid clip and scope check (Sangomar/Tortue fiducial)

`np.where(section == lid)` returns indices up to `(nx-1, nz-1)`. Without
clip, the `z_arr[yy]` lookup throws index error on small/sparse slices.
The renderer now:

```python
yy = np.clip(yy, 0, len(z_arr) - 1)
xx = np.clip(xx, 0, len(x_arr) - 1)
# Then scope check: only place the fiducial if its centroid is in plot extent
if (z_arr.min() / 1000 - 0.5 <= sang_z_world <= z_arr.max() / 1000 + 0.5 and
        x_arr.min() / 1000 <= sang_x_world <= x_arr.max() / 1000):
    ax.scatter(...)
    ax.annotate(...)
```

## End-to-end wire-up test (2026-08-20, post-fix)

```python
# 120 CSV picks x 3 formations (depth_positive_down convention)
# Bridge auto-derives extent from picks
bridge = await geox_segy_horizon_bridge(
    horizon_picks=synthetic_csv, picks_tag='SYNTHETIC',
    grid_resolution=[80, 35, 50],  # optional -- bridge picks defaults
    y_slice_frac=0.5,
)
# bridge.gempy_result contains:
#   lithology_block: shape (80, 35, 50) = 140,000 voxels
#   formations: ['Basement_Top', 'Cenomanian_Turonian', 'Sangomar_Turbidites']
#   extent: derived from picks with 1 km buffer
#   Unique IDs in block: [1, 2, 3, 4] (all 4 lith IDs computed)
#   truth tag: SYNTHETIC -> SYNTHETIC (preserved)
# render_gempy_section -> 162 KB publication-grade PNG
#   with TRUE SCALE 1:1 watermark, depth axis, formation labels,
#   Sangomar FID marker, domain labels.
```

Committed at session end on branch `chore/surface-regen-20260818`:

- `9b36d532` chore(geox): wire GemPy section renderer end-to-end, fix bridge extent
- `03340327` fix(geox): renderer label axis mapping
- `39abc872` fix(geox): section renderer default index
- `856f9243` feat(geox): gempy section renderer -- publication-grade output
- `a00dac3b` feat(geox): gempy horizon bridge + fix GemPy 2026.0.3 API drift

LSP GATE: PASSED on all 2 staged files.

## v1 -> v4 dossier progression (Senegal Basin case study)

The full audit-driven upgrade that the skill's "Version Note" anticipated:

| Version | What broke | What got added |
|---------|-----------|----------------|
| v1 | Cartoon cross-section labeled "Schematic" | Striplog Rock-object strat column + Sclater-Christie decompaction + TRUE SCALE 1:1 + Natural Earth 50m real coastline |
| v2 | Burial curves drawn as Bezier control points; cross-section not to scale | Sclater-Christie 1980 decompaction kernel (Athy's law + T_0 = T_present * (1-phi_ref)/(1-phi_present)) for true 1D burial history |
| v3 | "INT/SCHEMATIC" 3D model derived from theory, not data | Replaced hand-rolled RBF with `geox_gempy_implicit_3d` federation tool path; section renderer added |
| v4 | Federation tools exist but bridge->gempy->renderer chain not exercised end-to-end | Bridge auto-extent + section renderer fix; **end-to-end verified** with 120 picks -> 4 lith IDs -> 162 KB PNG with TRUE SCALE 1:1 watermark |

**Generalize this pattern:** for any basin artifact, run v1->v4: schematic
-> physics-driven -> federation tool path -> live wire-up end-to-end. Each
step is independently provable (`vision_analyze`, `pdfinfo`, `git log`).
