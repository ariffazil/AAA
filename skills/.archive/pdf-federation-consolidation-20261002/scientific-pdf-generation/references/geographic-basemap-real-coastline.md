# Geographic Basemap from Natural Earth (Real Coastlines)

For any geological deliverable that needs a regional map — PSC block map, basin
location map, field location map, prospect map — the map MUST show real
geography, not fabricated polygons. This is the canonical recipe for producing
a real West African Atlantic-margin basemap with Natural Earth 50m coastline data.

## Source: Natural Earth 50m Land (NOT 110m)

```python
import urllib.request
url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson"
urllib.request.urlretrieve(url, "/tmp/coastline_50m.geojson")
```

**Why 110m FAILS for West Africa:** the 110m data has only ONE polygon for the
entire Africa continent, with vertices at extreme latitudes (Antarctica,
Greenland). bbox filtering on lat/lon within `[10-20N, 10-20W]` returns 0
hits because of how MultiPolygon vertices are distributed.

**Why 50m WORKS:** the 50m dataset has 1420 features, and the Africa polygon
contains 183 vertices within the West Africa lat/lon window — enough to
resolve Cap-Vert peninsula, Casamance coastline, Senegal-Mauritania border.

## Polling for West Africa Vertices

```python
import json
with open('/tmp/coastline_50m.geojson') as f:
    ne = json.load(f)

WA_BBOX = (-22, -8, 9, 23)  # (min_lon, max_lon, min_lat, max_lat)
land_polys = []

for feat in ne['features']:
    geom = feat.get('geometry')
    if not geom: continue
    polys = (geom['coordinates'],) if geom['type'] == 'Polygon' else geom['coordinates']
    for poly in polys:
        for ring in poly:
            in_count = sum(1 for x, y in ring
                          if WA_BBOX[0] <= x <= WA_BBOX[1]
                          and WA_BBOX[2] <= y <= WA_BBOX[3])
            if in_count > 20:
                # Buffer the bbox slightly to capture vertices on its edge
                wa_verts = [(x, y) for x, y in ring
                            if (WA_BBOX[0] - 2) <= x <= (WA_BBOX[1] + 2)
                            and (WA_BBOX[2] - 2) <= y <= (WA_BBOX[3] + 2)]
                if len(wa_verts) > 30:
                    land_polys.append(wa_verts)
```

The `> 20` threshold filters out polygons with only stray touches to the ROI;
`> 30` then drops tiny spurious rings. Buffered bbox prevents edge clipping.

## Rendering the Land Mass

```python
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

map_lon_min, map_lon_max = -19.5, -12.5
map_lat_min, map_lat_max = 11.0, 22.0

patches = []
for poly_verts in land_polys:
    clipped = []
    for x, y in poly_verts:
        cx = max(map_lon_min, min(map_lon_max, x))  # clamp to map extent
        cy = max(map_lat_min, min(map_lat_max, y))
        clipped.append((cx, cy))
    if len(clipped) >= 3:
        patches.append(Polygon(clipped, closed=True))

# Add directly to ax (PatchCollection not needed for closed-loop Coastline)
for p in patches:
    ax.add_patch(p)
```

## Bathymetric Contours (West African Passive Margin)

Real Senegal Basin has a wide continental shelf. Approximate isobath positions
perpendicular to a coastline average ~16.5°N:

```python
coast_estimate = lambda lon: 16.5 - 0.5 * np.sin((lon - (-17)) * 1.2)
# offset = depth-normalized perpendicular distance
offset_lookup = {50: 0.3, 200: 0.5, 1000: 1.3, 2000: 1.8, 3000: 2.5, 4000: 3.3}
for depth_m, offset_deg in offset_lookup.items():
    lons = np.linspace(map_lon_min, map_lon_max, 100)
    lats = coast_estimate(lons) + offset_deg
    ax.plot(lons, lats, '-', color=..., linewidth=1.0, alpha=0.85)
```

## PSC Block Placement (Offshore, Not On Land)

PSC blocks along the West African margin are typically 30-150 km offshore —
position them OUTSIDE the coastline polygon, in the bathymetric depth zone of
50m-2000m. Use simplified hexagonal/irregular polygons (not real registry
shapes, which aren't public).

## Known Failure Mode

A previous run clipped the Africa polygon to the ROI bbox, which **kept inland
Sahara as "land"** because the polygon contains vertices across the continent.
Symptom: PSC blocks appeared clustered in a thin strip inland instead of in the
Atlantic. Fix: clamp coordinates to the map extent so the polygon is bordered
by the map frame, then position PSC blocks based on bathymetric depth zone,
not on the inland polygon edges.

## Reference

- Source: https://www.naturalearthdata.com/ (free, public domain)
- Alternative: GADM (https://gadm.org/) for admin boundaries
- Alternative: OpenStreetMap via osmnx for full road network (heavier)
