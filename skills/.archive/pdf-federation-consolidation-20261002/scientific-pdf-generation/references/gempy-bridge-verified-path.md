# GemPy Horizon Bridge — Verified Path (gempy 2026.0.3)

> Picks → GemPy implicit 3D → true-scale 2D section. Proven 2026-08-20 Senegal session.
> Deployed: `/root/GEOX/src/geox_mcp/tools/segy_horizon_bridge.py` (commit 03340327).

## Epistemic tag propagation (the core rule)

Truth class **only descends, never upgrades**:
- OBS picks → DER model (interpolation is derived from observation)
- DER → DER, INT → INT, SYNTHETIC → SYNTHETIC

`derive_epistemic_tag()` enforces this. A bridge that upgrades tags is a false-receipt machine.

## Picks validation gate

- ≥3 picks per formation (GemPy needs 3 to constrain a surface)
- Duplicate (x,y) **within** a formation = degenerate → reject
- Same (x,y) across DIFFERENT formations = normal stacked-horizon geometry → allow

First implementation of the gate used a global duplicate check and rejected its own valid stacked-horizon test data. Per-formation is correct.

## Verified gempy 2026.0.3 recipe

```python
import gempy as gp

# 1. CSVs with exact column names
#    surface_points: X,Y,Z,formation
#    orientations:   X,Y,Z,dip,azimuth,polarity,formation
helper = gp.data.ImporterHelper(
    path_to_surface_points="sp.csv",
    path_to_orientations="ori.csv",
)
m = gp.create_geomodel(
    project_name="x",
    extent=[xmin, xmax, ymin, ymax, zmin, zmax],  # z-up
    resolution=[nx, ny, nz],
    importer_helper=helper,
)
# 2. compute_model returns Solutions DIRECTLY — do not reassign to m
solutions = gp.compute_model(
    gempy_model=m,
    engine_config=gp.data.GemPyEngineConfig(backend=gp.data.AvailableBackends.numpy),
)
# 3. lith_block arrives FLATTENED — reshape when sizes match
lb = solutions.raw_arrays.lith_block
if lb.ndim == 1 and lb.size == nx * ny * nz:
    lb = lb.reshape(nx, ny, nz)   # else: octree ran at different res; skip slicing
```

**Dead paths (API drift — do not retry):**
- `structural_frame.elements_df` — attribute removed upstream
- Manual `StructuralFrame` + `StructuralElement` construction — fragile, unsupported
- `m = gp.compute_model(...)` then `m.solutions` — wrong object, compute returns Solutions
- `ImporterHelper(surface_points=DataFrame)` — kwarg renamed; it takes PATHS

## Section slice contract

- Slice (nx, nz) at fixed y-index: `section = lb[:, j, :]`
- **vertical_exaggeration = 1.0 locked** in the returned contract
- y_world = ymin + y_slice_frac × (ymax − ymin)

## z-convention

Picks may arrive depth-positive-down (driller's convention). GemPy is z-up. Flip: `z_gempy = -z_pick`. Caller declares via `z_convention="depth_positive_down" | "elevation"`.

## Dip/azimuth → pole vector

```python
dip, az = np.radians(d), np.radians(a)
G = (sin(d)*sin(az), sin(d)*cos(az), cos(d))
```

Orientations can be seeded with a regional dip hint (e.g. 2° basinward) at each formation centroid when sparse picks carry no measured orientation.

## Smoke test result (72 picks, 3 formations, 30×20×18 grid)

Section [30×18], lith IDs {1,2,3,4}, near-coast vs far-basin lith histograms differ correctly — reservoir band deepens basinward. Physics honoured. SYNTHETIC tag preserved end-to-end.

## Falsification-first deployment note

Before wiring any "empirical data" pipeline, scan the box for the data. This session: no Senegal SEGY existed — only synthetic fixtures. Correct move was to ship the bridge + clearly-tagged synthetic demo, NOT to rebrand theoretical McKenzie curves as empirical. Tag stays SCHEMATIC/INT until real picks arrive; then `picks_tag="OBS"` upgrades output to DER automatically.
