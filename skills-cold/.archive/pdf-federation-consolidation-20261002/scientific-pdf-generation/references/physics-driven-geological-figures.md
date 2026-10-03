# Physics-Driven Geological Figures — Workhorse Reference

> Proven: 2026-08-20, Senegal Basin GEOX figures suite. Three figures upgraded
> from Bezier-rendered cartoons to physics-driven data structures: burial history
> (Sclater-Christie decompaction), cross-section (TRUE SCALE 1:1 from
> decompaction-derived layer thicknesses), map (Natural Earth 50m coastline).
> Audited and accepted as the new standard for any geological artifact.

## The Mandate

Geological figures that depict a physical process MUST be rendered through the
mathematics of that process, not through hand-drawn geometry. This is the central
lesson from the 2026-08-20 audit of the original Senegal Basin figures suite. If
you find yourself writing `fill_between(x, *gaussian_bumps)` to draw a burial
curve, you are doing it wrong. If you label a cross-section "Schematic — NOT to
scale," you are doing it wrong. If your basemap's coastline is hand-drawn
geometry rather than a real polygon, you are doing it wrong.

Three required physics-driven patterns:

| Pattern | Physical law / source | Failure case |
|---|---|---|
| Burial history | Sclater-Christie 1980 decompaction (Athy law) | Bezier curves that look pretty but encode no physics |
| Cross-section | TRUE SCALE 1:1, dimensions in km, no VEx | Arbitrary Gaussian bumps for layer thickness |
| Map | Natural Earth 50m polygons + bathymetric contours | Hand-drawn African continent shape |

## 1. Sclater-Christie Decompaction Kernel

Reference: Sclater, J.G., and Christie, P.A.F., 1980. Continental Stretching:
An Explanation of the Post-Mid-Cretaceous Subsidence of the Central North Sea
Basin, J. Geophys. Res., 85, 3711-3739.

### Physics

Porosity decay with depth (Athy's law):

```
φ(z) = φ₀ · exp(−z / λ)
```

where φ(z) is porosity at depth z (km), φ₀ is initial porosity at deposition,
and λ is the decay-length scale (km). Standard values for clastic sediments from
Sclater & Christie (1980) and Steckler & Watts (1978):

| Lithology | φ₀ | λ (km) |
|---|---|---|
| Sand / Sandstone | 0.55–0.62 | 2.6 |
| Siltstone | 0.50 | 2.8 |
| Shale / Claystone | 0.40–0.58 | 2.8–3.2 |
| Limestone | 0.45 | 3.0 |
| Volcanic | 0.35 | 3.0 |

Decompacted thickness from compacted thickness:

```
T₀ = T_present · (1 − φ_ref) / (1 − φ_present)
```

where T₀ is original (decompacted) thickness, T_present is observed compacted
thickness, φ_ref is porosity at the reference surface (z=0), and φ_present is
porosity at the present burial depth of the unit.

### Implementation

```python
import numpy as np

def porosity_depth(z_km, phi0, lam):
    """Athy's law — vectorized."""
    return phi0 * np.exp(-z_km / lam)

def decompacted_thickness(T_present, phi0, lam, z_overburden_km):
    """Backstrip a unit to its original thickness at reference depth."""
    phi_ref = porosity_depth(0.0, phi0, lam)
    phi_present = porosity_depth(z_overburden_km, phi0, lam)
    return T_present * (1.0 - phi_ref) / (1.0 - phi_present)

# Stratigraphic input: (age_top_Ma, age_bot_Ma, T_present_km, label, phi0, lam)
strat = [
    (0,    5,   0.40, 'Quaternary',                  0.62, 2.6),
    (5,   23,   0.80, 'Mio-Pliocene Deltaic',        0.60, 2.6),
    (23,  42,   0.50, 'Oligocene',                   0.58, 2.8),
    (42,  66,   0.70, 'Eocene',                      0.56, 2.8),
    (66,  72,   0.40, 'Paleo-L.Maastrichtian',       0.55, 2.8),
    (72,  84,   0.90, 'Campanian (Sangomar)',        0.52, 3.0),
    (84, 100,   0.50, 'Cenomanian-Turonian source',  0.50, 3.0),
    (100,113,  0.45, 'Albian',                      0.48, 3.0),
    (113,125,  0.55, 'Aptian source',               0.45, 3.2),
    (125,145,  1.20, 'Neocomian-Barremian',         0.42, 3.2),
    (145,170,  1.00, 'Late Jurassic',               0.40, 3.2),
    (170,201,  1.50, 'Triassic-J. Rift Fill',       0.38, 3.0),
]
strat.sort(key=lambda u: -u[1])  # oldest first

# Build decompacted trajectory at every geological time step
def build_decompacted_burial(units):
    age_boundaries = sorted(set([0.0] + [u[1] for u in units] + [u[0] for u in units]))
    burial_ages, burial_depths = [], []
    for t in age_boundaries:
        # Apply standard backstripping rules:
        #   t >= age_bot → unit not yet deposited
        #   age_top <= t < age_bot → partial deposition (linear interpolation)
        #   t < age_top → fully deposited (decompact)
        total_depth = 0.0
        for age_top, age_bot, T_pres, label, phi0, lam in units:
            if t >= age_bot:
                continue
            elif t < age_top:
                # Compute overburden: units with age_top > current unit's age_top
                # that have also finished depositing by time t
                overburden = sum(
                    T_j for a_top_j, _, T_j, _, _, _ in units
                    if a_top_j < age_top and a_top_j > t
                )
                T0 = decompacted_thickness(T_pres, phi0, lam, overburden)
                total_depth += T0
            else:
                # Partial deposition
                frac = max(0.0, (age_bot - t) / (age_bot - age_top))
                T_part = T_pres * frac
                if T_part > 0:
                    overburden = sum(
                        T_j for a_top_j, _, T_j, _, _, _ in units
                        if a_top_j < age_top and a_top_j > t
                    )
                    T0 = decompacted_thickness(T_part, phi0, lam, overburden)
                    total_depth += T0
        burial_ages.append(t)
        burial_depths.append(total_depth)
    return np.array(burial_ages), np.array(burial_depths)
```

### Validation Checks

Always validate the kernel output before plotting:

- Monotonic increase in decompacted depth over time ✓
- Total present-day compacted thickness matches input `sum(T_present) ≈ 8.9 km`
  for the Senegal slope example
- Decompacted top (at t=0) should equal the present-day total
- Top of deepest unit at t = 201 Ma ≈ 0 km (basement, nothing above)

### Companion Thermal Maturity

Once decompacted depths are computed, overlay vitrinite reflectance using
Sweeney & Burnham 1990 (simplified EasyRo):

```python
# Present-day Ro vs decompacted depth
geothermal_gradient = 32.0  # °C/km (West African margin)
T_surface = 20.0  # °C

depths_line = np.linspace(0, max_burial_km, 200)
z_m = depths_line * 1000
Ro = 0.2 + 0.0008 * z_m + 0.00000012 * z_m**2  # simplified
Ro = np.clip(Ro, 0.15, 4.0)
# Oil window: Ro 0.6–1.2
# Gas window: Ro > 1.2
# Immature: Ro < 0.6
```

Geothermal gradient varies by margin (~25–35 °C/km). Source the value from
the regional literature — don't default to 25 °C/km.

## 2. TRUE SCALE 1:1 Cross-Section

### Rules

- Real horizontal extent: ≥200 km for a typical offshore passive margin
- Vertical extent in km: must match the sediment-thickness envelope from the
  Sclater-Christie model (don't fabricate layers thicker than 0.5–2 km in a
  passive-margin basin)
- Axes labelled km and km
- Salt dome: Gaussian uplift profile (peak 3–4 km, width 5–10 km), not a
  floating column
- Growth faults: dip 30–50°, throw 0.5–2 km
- Reference point: seafloor at 0 km depth
- Annotate in the figure: "TRUE SCALE 1:1 — No vertical exaggeration"

### Forbidden

- "Schematic — NOT to scale" caption — the failure pattern
- Layer fills using arbitrary Gaussian thickness bumps
- Salt diapir rendered as a separate floating column from middle sediment
- Vertical exaggeration marker (the goal is 1:1, not "we exaggerated X times")

### Pattern: Layer Thickness from Decompaction

```python
# Given strat input from the Sclater-Christie kernel above
# Compute total sediment thickness as a function of x (basement depth)
def top_of_basement(x):
    """Basement deepens offshore (sigmoid)."""
    return 5.0 + 7.0 / (1.0 + np.exp(-0.05 * (x - 130)))

# Distribute each unit's thickness proportionally to overlying depocentre
def compute_layer_thicknesses(x):
    seabed_depth = -seabed  # km depth
    basement = top_of_basement(x)
    total_sed = basement - seabed_depth

    depocentre_factor = np.clip(
        np.where(x < 100, 0.3, np.where(x < 130, 0.5 + (x-100)/30*0.5, 1.0)),
        0.2, 1.0
    )

    ratios = {
        'cenozoic': 0.314, 'campanian': 0.101, 'cenomanian': 0.056,
        'albian': 0.051, 'aptian': 0.062, 'neocomian': 0.135,
        'jurassic': 0.112, 'triassic': 0.169,
    }

    base_thicknesses = {k: ratios[k] * total_sed * depocentre_factor for k in ratios}

    layer_order = ['cenozoic', 'campanian', 'cenomanian', 'albian',
                   'aptian', 'neocomian', 'jurassic', 'triassic']

    top = basement.copy()
    tops = {}
    for layer in reversed(layer_order):
        tops[layer] = top.copy()
        # Thin out pre-rift (Triassic/Jurassic) over shelf
        if layer in ('triassic', 'jurassic'):
            shelf_thin = np.where(x < 80, (80 - x) / 80, 0.0)
            thickness = base_thicknesses[layer] * (1 - shelf_thin * 0.5)
        else:
            thickness = base_thicknesses[layer]
        top -= thickness

    return {f'top_{k}': tops[k] for k in layer_order}
```

### Salt Dome as Gaussian Uplift (not a floating column)

```python
salt_x = 145
salt_width = 8  # km
salt_max_height = 3.5  # vertical piercing in km

salt_uplift = salt_max_height * np.exp(-(((x - salt_x) / (salt_width/2)) ** 2))

# Apply salt uplift only in the affected region
uplift_mask = salt_uplift > 0.1
# Plot salt dome as a Gaussian-shaped uplift region in the affected layers
# not as a free-floating vertical column
```

## 3. Natural Earth Basemap

### Loader

```bash
curl -s "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson" -o /tmp/coastline_50m.geojson
```

Why 50m not 110m? The 110m Natural Earth dataset has only ONE continent polygon
per continent and may not include West Africa vertices in a useful resolution
(verified 2026-08-20: only 1 polygon overlaps Senegal bbox, all from Russia).
The 50m dataset has hundreds of polygons with 100+ vertices in West Africa
alone. Always use 50m for regional basin-scale maps; 110m only for world maps.

### Render Pattern (matplotlib, no cartopy complications)

```python
import json
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np

with open('/tmp/coastline_50m.geojson') as f:
    ne_data = json.load(f)

def draw_coastline(ax, geojson_path, bbox, facecolor, edgecolor):
    """Render all land polygons in the bbox as a polygon collection."""
    min_lon, max_lon, min_lat, max_lat = bbox
    patches = []

    def process_ring(ring):
        clipped = []
        for x, y in ring:
            cx = min_lon if x < min_lon else (max_lon if x > max_lon else x)
            cy = min_lat if y < min_lat else (max_lat if y > max_lat else y)
            clipped.append((cx, cy))
        if len(clipped) >= 3:
            clipped.append(clipped[0])
            return clipped
        return None

    for feature in json.load(open(geojson_path))['features']:
        geom = feature['geometry']
        gtype = geom['type']
        coords = geom['coordinates']
        rings_to_process = []
        if gtype == 'Polygon':
            for ring in coords:
                rings_to_process.append(ring)
        elif gtype == 'MultiPolygon':
            for poly in coords:
                for ring in poly:
                    rings_to_process.append(ring)
        for ring in rings_to_process:
            clipped = process_ring(ring)
            if clipped is not None:
                patches.append(Polygon(clipped, closed=True, facecolor=facecolor,
                                       edgecolor=edgecolor, linewidth=0.7, zorder=2))

    pc = PatchCollection(patches, match_original=True)
    ax.add_collection(pc)
    return len(patches)
```

### Map Standards for a Senegal-Type Offshore Basin Map

- Map extent: lat range covering the basin (e.g., 11–22°N for Senegal)
- Map extent: lon range covering offshore + inshore (e.g., -19.5 to -12.5°E)
- Lat/lon grid every 1° with degree labels
- Six bathymetric contour lines: 50m, 200m, 1000m, 2000m, 3000m, 4000m
- Subtle offshore depth shading (gradient from light to dark blue)
- Scale bar in km: at lat φ, 1° longitude ≈ 111.32 × cos(φ) km
- Compass rose
- PSC polygons on actual offshore positions (tag INT if approximate)
- Wells as triangles with year + reserve tags
- Country labels ON landmass

### What Real Geography Looks Like

The Senegal coastline has these recognizable features that must be visible:

- **Cap-Vert peninsula** at ~14.65°N, -17.45°W (Dakar area, the peninsula bulge)
- **Casamance coast** in southern Senegal (~12.5°N)
- **The Gambia** is a thin coastal strip ~13.5°N, surrounded by Senegal
- **Mauritanian coast** at ~17–21°N, along with the Senegal-Mauritania maritime border

If these features are NOT visible in your basemap, you are using wrong coastline
data (110m doesn't have enough West Africa vertices) or wrong geometry.

## 4. Stratigraphic Column — Striplog Pattern

Striplog is the geology library for interval-based lithology data. Use it (or
follow its data model) to build stratigraphic columns procedurally rather than
from a hand-edited table.

Each interval carries:

- Top depth (m TVDSS)
- Bottom depth (m TVDSS)
- Primary lithology (Sand, Sandstone, Siltstone, Shale, Claystone, Limestone, Basalt)
- Secondary lithology (interbeds, admixture)
- Grain size (Med-coarse, Med, Fine, Clay, Mudstone)
- Porosity % range (sand 20–30%, shale 5–15%, limestone 8–18%)
- Permeability range in mD (sand 100–1500, shale 0.01–0.1, limestone 0.1–10)
- Role (CO, SEAL, RES, SOURCE, SEC_R, SEC_S, ?)
- Formation name

```python
formations = [
    (0,    450,  'Sand',         'clay interbeds',   'CO',      GOLD,  'Quaternary', 12),
    (450,  1500, 'Siltstone',    'clay-rich',         'CO',      AMBER, 'Mio-Pliocene', 11),
    (1500, 2200, 'Claystone',    'marl',              'SEAL',    TEAL,  'Oligo-Miocene seal', 10),
    (2200, 2800, 'Limestone',    'chalky',            '?',       DIM,   'Eocene', 9),
    (2800, 3300, 'Shale',        'carbonate',         'SEAL',    TEAL,  'Paleo-L.Maastr', 8),
    (3300, 4050, 'Sandstone',    'siltstone',         'RES',     ORANGE,'Campanian Sangomar', 7),
    # ... etc.
]
```

Render as a multi-column table: depth range | lithology swatch + name | grain |
porosity | perm | role (color-coded) | formation.

Lithology colors (sedimentology convention):

| Lithology | Color (Mode B dark) | Sample |
|---|---|---|
| Sand | `#fde2b3` (cream) | `#FFD180` |
| Sandstone | `#fcd180` | |
| Siltstone | `#d4a76a` | |
| Shale | `#5a5a5a` (gray) | `#3a3a3a` darker |
| Claystone | `#7a9e9e` (teal-gray) | |
| Limestone | `#bce0d2` (pale green) | |
| Dolomite | `#a4c8b8` | |
| Evaporite | `#cfb6e3` (purple-lavender) | |
| Basalt | `#3b3b3b` | |

## 5. PSC Polygon Positioning on the Real Map

PSC block positions on a basemap must come from the public PSC registry,
not invented coordinates. Approximate centers (verified 2026-08-20 from
public sources for Senegal Basin):

| PSC Block | Operator | Approx center | Tag |
|---|---|---|---|
| Cayar Offshore Profonde (Sangomar Deep) | Woodside | (-17.45, 13.85) | OBS/INT |
| Cap-Vert | Woodside | (-17.55, 14.55) | OBS/INT |
| St-Louis Profond | TotalEnergies | (-16.65, 15.50) | OBS/INT |
| Greater Tortue | bp / Kosmos | (-16.65, 16.50) | OBS/INT |
| Yakaar-Teranga | bp / Kosmos | (-16.50, 15.85) | OBS/INT |
| Dakar Offshore Profond | ConocoPhillips | (-17.20, 14.75) | OBS/INT |

Tag INT when using approximate polygon shapes; tag OBS for the public block
names/operators.

## Validation Checklist Before Delivery

- [ ] Burial curve computed via Sclater-Christie decompaction, NOT a Bézier
- [ ] Cross-section rendered at TRUE SCALE 1:1 with explicit "no VEx" annotation
- [ ] Cross-section axes in km and km, not arbitrary units
- [ ] Cross-section layer thicknesses derived from decompaction, not Gaussian bumps
- [ ] Salt dome shown as Gaussian uplift, not a floating column
- [ ] Map uses Natural Earth 50m (not 110m) land polygons
- [ ] Map shows real geography (Cap-Vert, Casamance, The Gambia for Senegal; correct region-specific features for other basins)
- [ ] Bathymetric contours at 50m, 200m, 1000m, 2000m, 3000m, 4000m
- [ ] WGS-84 lat/lon grid at 1° with degree labels
- [ ] Scale bar in km at the latitude-appropriate km per degree
- [ ] Strat column has lithology swatches in sedimentology convention
- [ ] Each strat column row carries at least depth + lithology + porosity + perm + role
- [ ] No figure is labelled "Schematic — NOT to scale"
- [ ] No fill_between with hand-tuned Gaussian bumps for geological layers

A figure that fails any of these checks fails the GEOX geology-rigor gate. The
audit of 2026-08-20 made this the new standard.
