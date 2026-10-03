# Governed Geospatial Figures — GeoDataFrame Pipeline

> Mode B / Mode C for geological/basin deliverables. Real basemaps, real wells, real block polygons, real physics. Schematic grids and bezier curves are NOT acceptable for a working geologist. Proven 2026-08-20, Senegal Basin Forensic Figures v3 (9 pages, 2.2 MB, vision-QA passed).

## When to Use

When the user delivers a geological artifact to a working geologist or a federation auditor and the deliverable must hold up under F2 TRUTH scrutiny. Concretely:

- "Give me geological artifacts", "real geology not bar charts"
- "Why is this a schematic? show me the real map"
- Any Mode B/C geoscience deliverable that previously used cartoon grids, colored rectangles, or hard-coded lat/lon coordinates
- Audit defense for a sealed artifact — every coordinate, every polygon, every horizon must be traceable

**Three rejected patterns to retire (proven 2026-08-20 session):**

1. Schematic block grids — colored rectangles in an 8×10 schematic layout that look like geography but contain zero geospatial anchor. Any well or block can be moved without invalidating the figure. User quote: "No full map. Redo again."
2. Approximate depth contours for bathymetry when GEBCO / ETOPO rasters are trivially obtainable. Even a low-resolution raster beats schematic depth lines.
3. Bezier burial curves plotted as visual aesthetics. If the curve is not governed by Sclater-Christie (1980) porosity-depth or McKenzie (1978) thermal subsidence with declared parameters (phi_0, c, beta, T_s, grad), label it SCHEMATIC explicitly — do not claim it as a predictive model.

## Pipeline — 6 Layers, Each Anchored

```
1. GeoDataFrame (BLOCKS, WELLS) — authoritative tabular anchor
2. Natural Earth 50m coastlines — vector base via GeoPandas (NOT matplotlib.patches)
3. Rasterio GeoTIFF bathymetry — depth in real grid cells, NOT line contours
4. McKenzie (1978) thermal subsidence — beta factor declared
5. Sclater-Christie (1980) porosity-depth — phi_0, c declared
6. Reportlab PDF assembly — figures inherit spatial provenance via shared anchors
```

All six layers reference the same BLOCKS and WELLS GeoDataFrames. One change in the anchor → entire figure set re-renders consistently. This is what makes the artifact *governed* rather than *illustrated*.

## Critical Anti-Patterns (proved by user rejection 2026-08-20)

### 1. Never use shapefile.Reader for multipolygons

Cartopy add_feature() fails on Natural Earth 110m shapefiles due to NaN points in LinearRing coordinates. Symptom: `shapely.errors.GEOSException: IllegalArgumentException: Points of LinearRing do not form a closed linestring`. Fix: load via geopandas.read_file() and iterate geom.geoms for MultiPolygon, geom.xy for LineString. Then .cx[bbox] to clip to the view extent.

```python
import geopandas as gpd
land_gdf = gpd.read_file(
    '/root/.local/share/cartopy/shapefiles/natural_earth/physical/ne_50m_land.shp'
)
land_view = land_gdf.cx[-24:-10, 9:21]
for geom in land_view.geometry:
    if geom.geom_type == 'Polygon':
        xs, ys = geom.exterior.xy
        ax.fill(xs, ys, facecolor='#3d2e1f', edgecolor='#5a4828', linewidth=0.3, zorder=2)
    elif geom.geom_type == 'MultiPolygon':
        for poly in geom.geoms:
            xs, ys = poly.exterior.xy
            ax.fill(xs, ys, facecolor='#3d2e1f', edgecolor='#5a4828', linewidth=0.3, zorder=2)
```

### 2. Never extend view to schematic-only fragments

If drawing Senegal Basin, the view MUST include Mauritania (N), Guinea-Bissau (S), The Gambia, Cape Verde islands, and 250+ km of Atlantic offshore. The cropped view that excludes land was the user's "Fail. No full map." Reason: it makes the deliverable look like a cartoon, not a regional geology product. Use extent `-24°W, 9°N, -10°W, 21°N` for Senegal-Mauritania, or larger for transboundary basins.

### 3. Never render labels on top of overlapping features

Three labels overlapping a single dense area looks like the map is broken. Allocate a label offset per well manually, draw connector line from label-box to actual marker:

```python
label_offsets = {
    'SNE-1':           (-17.20, 14.95, 'ne'),
    'Sangomar FID':    (-16.85, 14.55, 'ne'),
    'Yakaar-1':        (-16.60, 13.95, 'ne'),
    'Teranga-1':       (-17.30, 13.55, 'nw'),   # opposite side to break the column
    'Orca-1':          (-16.40, 13.55, 'ne'),
}
for wname, (tx, ty, dirn) in label_offsets.items():
    r = WELLS[WELLS.name == wname].iloc[0]
    ax.annotate('', xy=(r.geometry.x, r.geometry.y), xytext=(tx, ty),
                arrowprops=dict(arrowstyle='-', color=AMBER, lw=1, alpha=0.6), zorder=9)
    ax.text(tx, ty, f"{wname}\n({r.year}, {r.operator})\n{r.status}",
            fontsize=7, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', fc=BG, ec=AMBER, alpha=0.92),
            zorder=10, path_effects=[withStroke(linewidth=1, foreground=BG)])
```

### 4. Burial curves without decompaction are illustration, not science

A geometric exponential decay curve labeled "burial history" is illustration. Use the real Sclater-Christie iterative decompaction with declared parameters:

```python
# Sclater-Christie (1980) porosity-depth
# phi(z) = phi_0 * exp(-z / c)
PHI_0 = 0.56   # surface porosity for typical marine sediments
C = 2.8         # characteristic decay depth (km)

def decompact_curve(z_thick, phi_0=PHI_0, c=C):
    """Iterative decompaction: dz_new = dz / (1 - phi(z))."""
    z = np.zeros_like(z_thick)
    cum_por = 0.0
    for i in range(len(z_thick)):
        dz = z_thick[i]
        z[i] = dz / (1.0 - phi_0 * np.exp(-(cum_por + dz*0.5) / c))
        cum_por += z[i]
    return z

# McKenzie (1978) thermal subsidence
def mckenzie_subsidence(t_ma, beta=1.3, tau=62.5, L=125.0):
    """y(t) = E0 * (1 - exp(-t/tau)) where E0 = L(rho_m - rho_c) / (rho_m - rho_w) * (1 - 1/beta)."""
    rho_m, rho_c, rho_w = 3300.0, 2800.0, 1030.0
    E0 = L * (rho_m - rho_c) / (rho_m - rho_w) * (1 - 1/beta)
    return E0 * (1 - np.exp(-t_ma / tau)) / 1000  # km
```

**Always caption with the parameters used.** `[INT — phi_0=0.56, c=2.8 km, beta=1.3 shelf (calibrated to Sangomar); beta=1.8 deepwater (uncalibrated). Sclater-Christie (1980) porosity-depth + McKenzie (1978) thermal subsidence.]`

### 5. Bathymetry via raster, not lines

Even a low-res modeled bathymetry raster is more honest than approximated depth contours:

```python
from rasterio.transform import from_bounds
with rasterio.open('/tmp/bathy_senegal.tif', 'w', driver='GTiff',
                    height=500, width=500, count=1, dtype='float32',
                    crs='EPSG:4326', transform=from_bounds(-25, 9, -10, 22, 500, 500)) as dst:
    bathy = modeled_continental_margin(coast_lon, dist_offshore)
    dst.write(bathy.astype(np.float32), 1)

# Then display
cmap_bathy = LinearSegmentedColormap.from_list(
    'bathy', ['#0a1a2a','#0d2a4a','#1a3a5a','#2a5a7a','#3a7a9a'], N=256
)
ax.imshow(bathy_masked, extent=extent, origin='upper',
          cmap=cmap_bathy, alpha=0.55, vmin=0, vmax=3000, zorder=1)
```

## Provenance Card — Always Append as Final Figure

Every Mode B/C geoscience deliverable should end with a self-referential provenance card listing epistemic tags per figure, tech stack (EPSG:4326, Sclater-Christie parameters, McKenzie beta, GeoDataFrame schemas), and confidence score with breakdown. This is F2 TRUTH architecture — the artifact asserts its own audit trail visibly.

## Vision-QA Loop (essential for this class)

Matplotlib "renders successfully" does NOT mean it renders correctly. Visual failures (overlapping text, NaN curves, label collisions, wrong projection alignment) cannot be caught from code review. After every figure batch:

1. Open the assembled PDF with the vision tool — page-by-page
2. For each figure, ask honestly: "Would a working geologist take this seriously? Any obvious errors (overlaps, NaN, wrong projection, label collisions)?"
3. Document failures, route fixes back to the matplotlib script, re-render ONLY the failing figure (incremental, not full re-render)
4. Cost: ~3-4 vision calls per figure, ~60s total QA budget per 7-figure deliverable

This pattern was added to the umbrella's main Pitfalls section 2026-08-20 after the Senegal session.

## Files

- Proven reference workspace: `/root/.hermes/cache/geox_v3.py` (Senegal Basin)
- Output PDFs:
  - `GEOX_Senegal_Basin_Petroleum_System_2026.pdf` (21 pages, Mode B dossier)
  - `GEOX_Senegal_Basin_Geological_Figures_v3.pdf` (9 pages, 2.2 MB — governed figures pipeline)
- Natural Earth 50m shapefiles: `/root/.local/share/cartopy/shapefiles/natural_earth/`
- Bathymetry raster (modeled, downloadable etopo1 alternative): `/tmp/bathy_senegal.tif`
- Output figures dir: `/root/.hermes/cache/geox_figures/`

## Stack Versioning (as of 2026-08-20)

```
geopandas 1.1.4
rasterio 1.5.0
shapely 2.1.2
scipy 1.18.0
numpy 2.4.6
matplotlib (Agg backend with MPLCONFIGDIR=/tmp/.mpl)
reportlab (A4 portrait)
```

If a future session finds a different version pattern breaks the pipeline, patch this file with the new diagnostic.

## Cross-References

- See umbrella: `scientific-pdf-generation` — Modes A/B/C reference
- Companion reference: `geological-dossier-figures.md` — simpler figure patterns without the GeoDataFrame rigour (use when full pipeline is overkill)
- Companion reference: `geological-artifact-figures.md` — well correlation, petrophysical log panels, structural cross-sections (still applies for those deliverables)
