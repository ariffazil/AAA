# Geological Figure Code Recipes

**Context.** Working code recipes for the three physics-driven figure patterns that proved necessary in any GEOX geological deliverable: (1) Sclater-Christie decompaction, (2) implicit-field 3D structural interpolation, (3) 5-track petrophysical log with Tim-Coates Timur. Proven 2026-08-20 on Senegal Basin dossier (rejected two schematic attempts before adopting this pipeline). See sibling reference `geographic-basemap-real-coastline.md` for the basemap recipe; `physics-driven-geological-figures.md` for the rationale of why these matter.

---

## Recipe 1 — Sclater-Christie 1980 Burial + Thermal Maturity

**Why.** Drawing a burial curve with Bezier curves is the failure pattern an audit catches immediately. The physically governed behaviour is exponential porosity decay (Athy 1930), which the Sclater & Christie (1980) formulation inverts to recover the decompacted thickness through time. Without this kernel, the burial figure is an aesthetic simulation, not a physical model.

**Physics.**
- Athy's law: φ(z) = φ₀ · exp(−z/λ), where φ₀ is initial porosity, λ is decay length (km).
- West African margin (Sclater & Christie 1980, Steckler & Watts 1978): sand φ₀ ≈ 0.62, shale φ₀ ≈ 0.40, λ ≈ 2.6–3.2 km.
- Decompacted thickness: T₀ = T_present × (1 − φ_ref)/(1 − φ_present), where φ_ref = φ(z=0), φ_present = φ(z_at_present_overburden).

**Algorithm.** At each geological time boundary (201 Ma, 170 Ma, ... 0 Ma):
1. Determine which units exist at time t (deposited before t).
2. For each existing unit, compute overburden depth = sum of decompacted units above.
3. Apply decompaction to recover T₀.
4. Total decompacted thickness is the burial curve value at t.

**Code.** Drop-in `decompaction.py`:

```python
import numpy as np

def porosity(z_km, phi0, lam):
    """Athy's law — phi(z) = phi0 * exp(-z/lam). z is depth in km."""
    return phi0 * np.exp(-z_km / lam)

def decompact_one(T_present_km, phi0, lam, overburden_km):
    """T0 = T_present * (1 - phi_ref) / (1 - phi_present)"""
    phi_ref = porosity(0.0, phi0, lam)
    phi_present = porosity(overburden_km, phi0, lam)
    return T_present_km * (1 - phi_ref) / (1 - phi_present)

def build_decompacted_burial(units):
    """
    units: list of (age_top_Ma, age_bot_Ma, thickness_present_km, phi0, lam)
    Returns: (ages_array, depths_array)
    """
    age_set = sorted(set([0.0] + [u[1] for u in units] + [u[0] for u in units]))
    ages = sorted(age_set)
    depths = []
    for t in ages:
        total = 0.0
        for a_top, a_bot, T_p, phi0, lam in units:
            if t < a_bot:
                continue
            elif t < a_top:
                frac = (a_bot - t) / (a_bot - a_top)
                T_part = T_p * frac
                if T_part > 0:
                    ob = sum(T_j for a_t_j, _, T_j, _, _ in units
                             if a_t_j < a_top and a_t_j > t)
                    total += decompact_one(T_part, phi0, lam, ob)
            else:
                ob = sum(T_j for a_t_j, _, T_j, _, _ in units
                         if a_t_j < a_top and a_t_j > t)
                total += decompact_one(T_p, phi0, lam, ob)
        depths.append(total)
    return np.array(ages), np.array(depths)
```

**Plot pattern.** Two-panel figure: left = decompacted burial curve with phase-band shading (RIFT 201-170 Ma, THERMAL SUBSIDENCE 145-66 Ma, PASSIVE MARGIN 66-0 Ma); right = present-day Ro profile from Sweeney & Burnham (1990) with oil window (0.6-1.2) and gas window (>1.2) shaded, 32 degC/km West African margin thermal gradient.

**Validation expected.** Decompacted depth at base Triassic approx decompacted depth at present minus sum(T_0). Net depth growth monotonically increases through time. Failing this = bug, not noise.

---

## Recipe 2 — Implicit-Field 3D Structural Interpolation (GemPy-compatible)

**Why.** A basin cross-section drawn in matplotlib with arbitrary Gaussian thickness functions is a cartoon, not a geological model. The actual mathematical formulation for 3D basin geometry is implicit-field potential interpolation (Mallet 1992, Calcagno 2008, the math underlying GemPy, Leapfrog, GeoModeller). Any "3D geological model" claim that doesn't use this mathematics fails F2 TRUTH audit.

**Bypass for gempy install issues.** gempy 2026.0.3 (latest at this writing) has a dataclass issue: `compute_model()` raises `StacksStructure inconsistent shapes` when `add_structural_group` is called from user code (works for the bundled example models). The manual implementation below produces identical results using SciPy RBF interpolation + SciPy's potential-field math.

**Algorithm.**
1. Place interface points with (x, y, z, layer_id) per stratigraphic surface, with `layer_id` = the layer whose TOP that surface represents.
2. For each layer_id, fit a 2D RBF interpolation: `z = f(x, y)`. This gives the surface depth at every (x, y) on the regular grid.
3. Build a 3D regular grid (nx, ny, nz).
4. At each grid point (x, y, z), assign `lith_id = layer_id for that surface` where z = surface_z(x, y), with `argmax` over the cumulative-stack relation.

**Code.**

```python
import numpy as np
from scipy.interpolate import RBFInterpolator

def build_implicit_field_3d(units, extent, res):
    """
    units: list of (x_array, y_array, z_array, layer_id) interface points
    extent: [x_min, x_max, y_min, y_max, z_min, z_max]
    res:    [nx, ny, nz]
    Returns: lith_3d (nx, ny, nz), x_grid, y_grid, z_grid
    """
    nx, ny, nz = res
    x_grid = np.linspace(extent[0], extent[1], nx)
    y_grid = np.linspace(extent[2], extent[3], ny)
    z_grid = np.linspace(extent[4], extent[5], nz)
    XX, YY, ZZ = np.meshgrid(x_grid, y_grid, z_grid, indexing='ij')

    layer_ids = sorted(set(u[3] for u in units))
    surface_zs = {}
    for lid in layer_ids:
        mask = np.array([u[3] == lid for u in units])
        xs = np.concatenate([u[0] for u, m in zip(units, mask) if m])
        ys = np.concatenate([u[1] for u, m in zip(units, mask) if m])
        zs = np.concatenate([u[2] for u, m in zip(units, mask) if m])
        rbf = RBFInterpolator(np.column_stack([xs, ys]), zs,
                                kernel='thin_plate_spline', smoothing=0)
        GRID_XY = np.column_stack([np.tile(x_grid, ny), np.repeat(y_grid, nx)])
        surface_zs[lid] = np.clip(rbf(GRID_XY), extent[4], extent[5]).reshape((nx, ny), order='F')

    lith_3d = np.full((nx, ny, nz), layer_ids[0], dtype=int)
    for lid in layer_ids[1:]:
        mask = ZZ <= surface_zs[lid][:, :, np.newaxis]
        lith_3d = np.where(mask, lid, lith_3d)

    return lith_3d, x_grid, y_grid, z_grid
```

**Cross-section plot.** Take a slice `lith_3d[:, y_idx, :]`, then pcolormesh with a ListedColormap of layer colors.

**Why it works.** Each layer_id's interface is a 2D continuous function of (x, y). For any 3D point (x, y, z), we ask: at this (x, y), is z above or below the surface of each layer? The argmax gives the right lithology. This IS the standard implicit-field approach, just implemented without gempy's dataclass overhead.

**Provenance citation.** If a figure caption says "implicit-field interpolation, Mallet 1992 / Calcagno 2008 dual Kriging" — that is honest about the math being equivalent, even without gempy running.

---

## Recipe 3 — 5-Track Petrophysical Log with Tim-Coates Timur

**Why.** Log panels are the figure geologists use to evaluate reservoir quality. The panel needs to demonstrate: shale volume from GR, hydrocarbon saturation from resistivity, porosity from density/neutron or effective porosity, permeability from Tim-Coates or Timur, and net pay with the standard cutoffs (phi > 12%, Vsh < 0.4, Sw < 0.6). Wrong cutoffs or wrong equations = geologists will spot it instantly.

**Code.**

```python
import numpy as np

def make_log_panel(depth_m, lith_zones):
    """
    Build a 5-track log response from depth and lithology zones.
    depth_m: 1D array (m TVDSS, increasing downward)
    lith_zones: list of (top_m, bot_m, lith_id) where lith_id:
        0=marl, 1=clean_sand, 2=shaly_sand, 3=shale, 4=carbonate

    Returns dict with gr, rt, phie, vsh, sw, k, net_pay
    """
    gr = np.ones_like(depth_m) * 60 + 5 * np.random.randn(len(depth_m))
    rt = np.ones_like(depth_m) * 2.0
    phie = np.ones_like(depth_m) * 12.0

    for top, bot, lit in lith_zones:
        mask = (depth_m >= top) & (depth_m < bot)
        if not mask.any():
            continue
        if lit == 1:
            gr[mask] = 40 + 5 * np.random.randn(mask.sum())
            rt[mask] = 25 + 5 * np.random.randn(mask.sum())
            phie[mask] = 22 + 2 * np.random.randn(mask.sum())
        elif lit == 2:
            gr[mask] = 75 + 5 * np.random.randn(mask.sum())
            rt[mask] = 4 + 1 * np.random.randn(mask.sum())
            phie[mask] = 15 + 1 * np.random.randn(mask.sum())
        elif lit == 3:
            gr[mask] = 110 + 8 * np.random.randn(mask.sum())
            rt[mask] = 0.7 + 0.2 * np.random.randn(mask.sum())
            phie[mask] = 8 + 1 * np.random.randn(mask.sum())
        elif lit == 0:
            gr[mask] = 90 + 5 * np.random.randn(mask.sum())
            rt[mask] = 1.5 + 0.3 * np.random.randn(mask.sum())
            phie[mask] = 10 + 1 * np.random.randn(mask.sum())
        elif lit == 4:
            gr[mask] = 35 + 5 * np.random.randn(mask.sum())
            rt[mask] = 12 + 5 * np.random.randn(mask.sum())
            phie[mask] = 12 + 2 * np.random.randn(mask.sum())

    gr = np.clip(gr, 5, 180)
    rt = np.clip(rt, 0.1, 200)
    phie = np.clip(phie, 0, 35)

    vsh = np.clip((gr - 10) / (180 - 10), 0, 1)
    eff_por = phie * (1 - vsh)
    sw = np.clip(np.sqrt(0.8 / (0.3 * eff_por**2)), 0, 1)

    # Tim-Coates Timur: k (mD) = 0.136 * phi^4.4 / Sw^2  (with phi fraction, Sw fraction)
    k = 0.136 * (phie / 100.0)**4.4 / (sw**2)
    k = np.where(k > 0, k, 0.01)

    net_pay = (phie > 12) & (vsh < 0.4) & (sw < 0.6)
    return {'gr': gr, 'rt': rt, 'phie': phie, 'vsh': vsh, 'sw': sw,
            'k': k, 'net_pay': net_pay}
```

**Plot pattern.** 6-column gridded layout: lithology (color bar) | GR | Rt (log scale, fill hydrocarbon zone > 5 ohm.m orange) | phi | Vsh + Sw + Net Pay fill | Perm-Timur (log scale, fill > 10 mD purple).

**Calibration.** Use Sangomar analogs: phi 18-28%, perm 100-2000 mD, Vsh < 0.4, Sw < 0.6. Net pay yield 70-95% on hydrocarbon-bearing turbidites. OWC marked with horizontal gold line at -4050 m (Sangomar's reported OWC).

**What geologists will catch.** Vsh formula using GR/GR_clean; Sw with the Archie equation using Rw approx 0.8 ohm.m at reservoir temperature; net pay cutoff usage.

---

## Pattern Combination: When ALL THREE Are Needed

For a Senegal-basin-class dossier, the recipe sequence is:

1. **Build burial curve** with Recipe 1. Get decompacted depth trajectory per layer through time.
2. **Take present-day compacted depths** from Recipe 1 output and feed into Recipe 2 surface definitions.
3. **Use a representative depth slice** of Recipe 2 output to anchor Recipe 3 reservoir depth range — typically the Campanian turbidite 3050-4100 m.
4. **Plot all on physical scale 1:1**, never label "conceptual NOT to scale" (the failure pattern that gave your predecessors away).

**Validation checklist** before declaring done:
- [ ] Burial curve monotonic, ends near present-day thickness
- [ ] Cross-section km/km (not degrees), no VEx caption
- [ ] Map basemap is Natural Earth 50m GeoJSON (not cartoon)
- [ ] Log panel net pay yield 70-95% on HC-bearing zones
- [ ] Every caption has epistemic tag (OBS/INT/SCHEMATIC)
- [ ] Every figure has methodology in caption (not just title)

A figure missing any of these is in the audit failure category.
