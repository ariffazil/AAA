# GEOX Federation Wire-Up — Calling geox_mcp Tools from External Sessions

> Proven 2026-08-20 (Senegal audit + Sabah dossier). The `geox_mcp` tools are
> importable directly from external sessions via `sys.path.insert`. This file
> is the reference for that pattern + the related bug-classes that broke
> before the wire-up was proven.

## The pattern (5 lines)

```python
import sys
sys.path.insert(0, '/root/GEOX/src')

from geox_mcp.tools.segy_horizon_bridge import geox_segy_horizon_bridge
from geox_mcp.tools.gempy_implicit_3d import geox_gempy_implicit_3d
from geox_mcp.tools.gempy_section_renderer import geox_gempy_section_renderer
```

That's it. The three tools cover the **Bridge → GemPy → Renderer** chain end-to-end.
Each is `async def` (MCP-friendly), accepts session_id/actor_id/trace_id
parameters, and returns JSON-safe dicts.

## Pipeline call (proven for Senegal + Sabah)

```python
import asyncio, csv, io
import numpy as np

# 1. Synthesize or load OBS-grade horizon picks
csv_buf = io.StringIO()
writer = csv.writer(csv_buf)
writer.writerow(['x','y','z','formation'])
for fm in ['Sangomar_Turbidites', 'Cenomanian_Turonian', 'Basement_Top']:
    for x in [15000, 50000, 100000, 130000, 165000, 185000]:
        for y in [30000, 50000, 75000]:
            writer.writerow([x, y, abs(depth(fm, x, y)), fm])

# 2. Bridge → GemPy → Renderer
async def run():
    bridge = await geox_segy_horizon_bridge(
        horizon_picks=csv_buf.getvalue(),
        picks_tag='SYNTHETIC',   # or 'OBS' when real
        y_slice_frac=0.5,
    )
    inner = bridge['gempy_result']
    if not inner['ok']:
        return

    block = np.array(inner['lithology_block'])
    extent = inner['extent']
    formations = inner['formations']

    ny = block.shape[1]
    for label, y_idx in [('shallow', 3), ('mid', ny//2), ('deep', ny-3)]:
        render_gempy_section(
            lithology_block=block, extent=extent, formations=formations,
            section_axis='y', section_index=y_idx,
            save_path=f'/tmp/federation_{label}.png',
        )

asyncio.run(run())
```

The bridge **auto-derives model_extent** from picks when caller doesn't
provide it (this is a fix from commit 9b36d532). It detects depth_positive_down
vs elevation and produces an extent covering all picks with 1 km buffer.

## Tool signatures

### geox_segy_horizon_bridge
```python
async def geox_segy_horizon_bridge(
    horizon_picks: str | list[dict] | None = None,  # CSV/JSON string or list of dicts
    picks_tag: str = "SYNTHETIC",  # OBS / DER / INT / SYNTHETIC
    z_convention: str = "depth_positive_down",  # or "elevation"
    dip_hint_deg: float = 2.0,
    azimuth_hint_deg: float = 90.0,
    grid_resolution: tuple | list | None = None,  # default (50,50,50)
    model_extent: tuple | list | None = None,  # auto-derived if None
    compute_uncertainty: bool = True,
    y_slice_frac: float = 0.5,
    output_format: str = "json",
    session_id: str | None = None,
    actor_id: str | None = None,
    trace_id: str | None = None,
) -> dict
```

Returns: `ok`, `pick_count`, `picks_tag`, `derived_tag`, `tag_rule`, `formations`,
`section` (Y-slice of lithology_block), `gempy_result` (nested gempy_implicit_3d output).

### geox_gempy_implicit_3d
```python
async def geox_gempy_implicit_3d(
    surface_points: list[dict] | str | None = None,  # [{x,y,z,formation}]
    orientations: list[dict] | str | None = None,    # [{x,y,z,dip,azimuth,formation}]
    grid_resolution: tuple | list | str | None = None,
    model_extent: tuple | list | str | None = None,
    compute_uncertainty: bool = True,
    uncertainty_realizations: int = 10,
    fault_groups: list[str] | str | None = None,
    output_format: str = "json",
    session_id: str | None = None,
    actor_id: str | None = None,
    trace_id: str | None = None,
) -> dict
```

Returns: `ok`, `model_id`, `lithology_block` (np.ndarray, may need reshape), `lithology_block_shape`,
`extent`, `formations`, `lithology_unique`, `sections` (dict of PNG paths), `volume_stats`,
`formation_volumes`, `uncertainty`, `epistemic: "PHYSICAL_MODEL"`.

### geox_gempy_section_renderer
```python
async def geox_gempy_section_renderer(
    lithology_block: list | str | np.ndarray | None = None,
    extent: list | str | None = None,
    formations: list | str | None = None,
    section_axis: str = "y",  # "x" or "y"
    section_index: int | None = None,
    layer_color_map: dict | None = None,
    title: str | None = None,
    save_path: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    trace_id: str | None = None,
) -> dict
```

Returns: `ok`, `image_path`, `image_bytes`, `section_axis`, `section_index`,
`section_index_world` (km), `lith_ids_seen`, `n_cells`, `epistemic`.

## Output artifact paths (from federation)

- Default output dir: `/opt/geox/data/gempy_outputs/` (created on first call)
- Section PNGs: `<output_dir>/gempy_section_<model_id>_<name>.png`
- Renderer output: `<output_dir>/gempy_render_ysec_<idx>_<model_id>.png` or `gempy_render_xsec_<idx>_<model_id>.png`

## Truth class propagation (the audit gate)

The federation enforces **F2 TRUTH** at the bridge level via
`derive_epistemic_tag()`. The rule: truth class only descends, never upgrades.

| Picks input | Bridge output | Reason |
|---|---|---|
| `picks_tag="OBS"` | `derived_tag="DER"` | GemPy interpolation is a derivation from observation |
| `picks_tag="DER"` | `derived_tag="DER"` | Already derived; stays derived |
| `picks_tag="INT"` | `derived_tag="INT"` | Interpretation; stays interpretation |
| `picks_tag="SYNTHETIC"` | `derived_tag="SYNTHETIC"` | Synthetic stays synthetic |

**Critical for audit:** when synthetic fixtures are used (e.g. no real SEGY
in the box), call with `picks_tag="SYNTHETIC"`. The renderer's epistemic
watermark reflects this. Never rebrand SYNTHETIC → OBS in a downstream
report without changing the picks.

## Bug classes that bit during wire-up (now documented)

### Bug A: bridge auto-extent for elevation picks
The first version of `geox_gempy_implicit_3d` had a broken auto-extent:
```python
zmin = 0.0
zmax_val = max(zs) + 500  # if zs are negative (elevation), max returns the shallowest!
zmax = zmax_val
```
For elevation picks (negative z), `max(zs)` returns the shallowest (e.g. -3700
m for Sangomar), giving zmax = -3200. Combined with zmin = 0, the extent
was inverted (zmin > zmax) — GemPy rendered basement-only.

**Fix (commit 9b36d532):** bridge auto-detects convention (max_z > 0 →
depth_positive_down) and produces correct extent.

**Workaround in caller code (pre-fix):** always pass explicit `model_extent`
with z bounds covering the picks in elevation form (e.g. extent_z_min =
-max_depth - 500, extent_z_max = -min_depth + 500 for depth-mode picks).

### Bug B: gempy.probability module not in 2026.0.3
The federation's uncertainty compute imports `gempy.probability` which
doesn't exist in 2026.0.3. The MC block is non-functional; uncertainty
returns `{"error": "No module named 'gempy.probability'"}`.

**Workaround:** set `compute_uncertainty=False` in the bridge call. The
section rendering works fine without MC; uncertainty is a nice-to-have.

### Bug C: bridge picks_to_gempy_inputs over-constrained
Initial implementation had:
```python
overburden = sum(Tp for a_top, _, Tp, _, _, _ in strat if a_top < age_top and a_top > t)
```
At t=0, units with a_top=0 (the shallowest) are EXCLUDED from their own
overburden calculation, making the decompacted burial show only the topmost
unit. Fix: drop the `a_top > t` constraint — overburden is purely
"units DEPOSITED BEFORE this one", i.e., a_top < this_unit_age_top.

### Bug D: Striplog import API drift
The `striplog` library changed its public API in recent versions:
`from striplog import Rock, Component, Legend` no longer works; the
correct imports are `from striplog import Striplog, Layer` and components
are accessed via `Striplog.layers` rather than direct Rock objects.

**Workaround:** don't import the Rock factory. Build the strat column
manually with structured tuples (top_depth, base_depth, lithology,
porosity %, perm, role) and convert to matplotlib barh rectangles
manually. This is what `geox_mcp.tools.gempy_implicit_3d` does internally
for the Sangomar-style strat column.

## The full Sabah federation wire-up (proven 2026-08-20)

GEOX already has a `okf/sabah-basin/` evidence bundle (basin, prospects,
strat, evidence, wells) that this pipeline can be pointed at. The Sabah
forge used:

1. `okf/sabah-basin/stratigraphy/sabah-ladder.md` — Stages I-VI (Cretaceous
   to Plio-Pleist)
2. `docs/analysis/LAYANG_LAYANG_KINABALU_CONTRAST_NOTE.md` — synthesis of
   Layang-Layang (rift-drift + carbonate) vs Kinabalu (compression +
   toe-thrust)
3. `geox/skills/subsurface/petro/sabah_prospect_discriminator.py` + `sabah_kill_matrix.py`
   — badali 2024 hard filters
4. Live federation pipeline (Bridge → GemPy → Renderer)

**Resulting dossier:** 23 pages, 3.0 MB, 10 figures including 3 live federation
GemPy sections at different Y-slice positions.

## Where the artifact lives in the federation

- Source: `/root/GEOX/okf/sabah-basin/`, `/root/GEOX/docs/analysis/`,
  `/root/GEOX/docs/eureka_insights/KL2_KINABALU_2026_06_03.md`
- Tools: `/root/GEOX/src/geox_mcp/tools/gempy_implicit_3d.py`,
  `segy_horizon_bridge.py`, `gempy_section_renderer.py`
- Output: `/opt/geox/data/gempy_outputs/` (production artifacts only;
  debug artifacts in `/tmp/senegal_figs_v2/`, `/tmp/sabah_figs_v1/`)
- History: commits a00dac3b, 856f9243, 39abc872, 03340327, 9b36d532

## Pattern: how to audit a federation tool's output

```bash
# 1. Inspect tool output
ls -la /opt/geox/data/gempy_outputs/

# 2. Verify with downstream render
python3 -c "
import sys; sys.path.insert(0, '/root/GEOX/src')
from geox_mcp.tools.gempy_section_renderer import render_gempy_section
import numpy as np
block = np.load('/tmp/senegal_figs_v2/federation_lith_block.npy')
extent = [0, 200000, 0, 100000, -15000, 0]
render_gempy_section(lithology_block=block, extent=extent,
    formations=['Basement_Top', 'Cenomanian_Turonian', 'Sangomar_Turbidites'],
    section_axis='y', section_index=15,
    save_path='/tmp/audit.png')
"

# 3. VISION QA loop
pdftotext dossier.pdf - | tail    # text extraction
pdftoppm -png -r 100 dossier.pdf /tmp/qa/page    # page → PNG
vision_analyze(image_url='/tmp/qa/page-08.png',
    question="Honest assessment: any obvious visual errors?")
```

The vision QA loop is the only reliable way to catch matplotlib issues like
overlapping text, NaN curves, or wrong geometry. Code review cannot.
