# GemPy 2026.0.3 API Notes & SEGY→GemPy Horizon Bridge

> Forged 2026-08-20, GEOX Senegal Basin session. The GEOX GemPy engine
> (`/root/GEOX/src/geox_mcp/tools/gempy_implicit_3d.py`) had silently broken
> against GemPy 2026.0.3 (upstream renamed/removed several APIs). This file
> records the verified-working patterns and the bridge module that now sits
> between interpreted seismic picks and the implicit model.

## GemPy 2026.0.3 — What Changed (probe before you write)

| Old assumption | GemPy 2026.0.3 reality |
|---|---|
| `structural_frame.elements_df["element_name"]` | **REMOVED.** Use `structural_frame.elements_names` (list property) |
| Build StructuralFrame manually via `StructuralElement(name=, color=, is_fault=)` constructors + `append_group()` | Constructor signature changed (`surface_points`/`orientations` args are `SurfacePoints`/`Orientations` objects); hand-building is fragile — **use the ImporterHelper CSV path instead** |
| `ImporterHelper(surface_points=df, orientations=df)` | **Wrong kwargs.** Takes `path_to_surface_points=` / `path_to_orientations=` (CSV file paths), plus optional column-name overrides |
| `geo_model = gp.compute_model(...)` then `geo_model.solutions` | **`gp.compute_model()` returns the `Solutions` object DIRECTLY.** Chaining `.solutions` on its return raises `AttributeError: 'Solutions' object has no attribute 'solutions'` |
| `solutions.raw_arrays.lith_block` is 3-D | May arrive **flattened 1-D** (octree output). Reshape to `(nx, ny, nz)` when `size == nx*ny*nz` |

### Verified-working minimal flow (probe3, 2026-08-20)

```python
import gempy as gp, pandas as pd, numpy as np

sp = pd.DataFrame({'X': [...], 'Y': [...], 'Z': [...], 'formation': [...]})  # Z-up elevations
ori = pd.DataFrame({'X': [...], 'Y': [...], 'Z': [...],
                    'dip': [...], 'azimuth': [...], 'polarity': [1.],
                    'formation': [...]})
sp.to_csv('/tmp/gp_sp.csv', index=False)
ori.to_csv('/tmp/gp_ori.csv', index=False)

helper = gp.data.ImporterHelper(
    path_to_surface_points='/tmp/gp_sp.csv',
    path_to_orientations='/tmp/gp_ori.csv',
)
model = gp.create_geomodel(
    project_name='x', extent=[xmin, xmax, ymin, ymax, zmin, zmax],
    resolution=[nx, ny, nz], importer_helper=helper,
)
solutions = gp.compute_model(          # ← returns Solutions directly
    gempy_model=model,
    engine_config=gp.data.GemPyEngineConfig(backend=gp.data.AvailableBackends.numpy),
)
lith = solutions.raw_arrays.lith_block
if lith.ndim == 1 and lith.size == nx*ny*nz:
    lith = lith.reshape(nx, ny, nz)
```

API surface probe one-liners that settled the arguments:

```python
inspect.signature(gp.create_geomodel)            # shows importer_helper kwarg
inspect.signature(ImporterHelper.__init__)       # shows path_to_* kwargs
dir(StructuralFrame)                             # elements_names, no elements_df
# after compute: type(m) == gempy_engine.core.data.solutions.Solutions
```

## The SEGY Horizon Bridge (new module, 2026-08-20)

`/root/GEOX/src/geox_mcp/tools/segy_horizon_bridge.py` — additive, registry
untouched. Chain:

```
horizon picks {x, y, z, formation} (CSV / JSON / list)
  → validate_picks()            (falsification gate)
  → picks_to_gempy_inputs()     (z flip + orientation seeds)
  → geox_gempy_implicit_3d()    (fixed engine)
  → extract_section_from_block()(x–z slice, VE = 1.0 contract)
  → epistemic-tagged artifact
```

### Design rules baked into the bridge

1. **Truth class propagates DOWN, never up.** `derive_epistemic_tag()`:
   OBS picks → DER model; SYNTHETIC stays SYNTHETIC. A bridge may never
   upgrade the epistemic class of its input. This is the F2 rule that
   stopped a false "empirical" claim when no real Senegal SEGY existed.
2. **Duplicate (x,y) check is per-formation, not global.** The same (x,y)
   across DIFFERENT formations is normal stacked-horizon geometry; only
   duplicates WITHIN one formation are degenerate. (The first gate version
   flagged legitimate stacked picks — caught by its own test.)
3. **Section slices carry `vertical_exaggeration: 1.0`** as a hard contract.
4. **Engine must expose the block array**, not just its shape, or downstream
   slicing is impossible (added `lithology_block` to the engine response).

### Falsification-first scope discipline

Before wiring any "ingest real SEGY" request: scan the box for actual SEGY
first (`find / -name "*.sgy" -o -name "*.segy"`). If none exists, build the
bridge anyway, prove it with clearly-tagged SYNTHETIC picks, and state the
data gap — never relabel theory as empirical.

## Test transcript (2026-08-20, end state)

```
tag propagation: PASS (OBS→DER, SYNTHETIC→SYNTHETIC)
csv parse + gate: PASS {'Reservoir': 3, 'Source': 3}
deficient-picks gate: PASS
FULL PIPELINE: PASS
  picks: 72 | formations: {'Seabed': 24, 'Reservoir': 24, 'Source_CT': 24}
  tag: picks = SYNTHETIC → artifact = SYNTHETIC
  section shape: [30, 18] | y_world: 4000.0 m | VE: 1.0
  near-coast lith histogram vs far-basin differ correctly
    (overburden thins basinward, horizons track the dip)
```

Uncommitted at session end (F13 hold): `segy_horizon_bridge.py` (new) and
`gempy_implicit_3d.py` (API-drift repair) on branch
`chore/surface-regen-20260818`.
