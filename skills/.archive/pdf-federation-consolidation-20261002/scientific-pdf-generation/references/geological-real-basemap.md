# Real Geological Basemaps (GeoPandas + Natural Earth + Rasterio)

> Forged 2026-08-20, Senegal Basin dossier session. Two consecutive user
> rejections ("Can we at least put real map please!!!!" then "Fail. No full
> map. Redo again.") produced this pattern. A working geologist will NOT
> accept schematic colored grids, cropped extents, or cartoon coastlines as
> "maps". Real cartography or nothing.

## When to Use

Any geological deliverable figure that shows *geography* — basin overview,
licensing block map, well location map, prospect location. If the figure has
a coastline, a country, or a well position, this pattern applies.

## Hard Rules (user-corrected)

1. **Real coordinates only.** Every coastline, border, city, well, and block
   polygon sits at actual lat/lon in EPSG:4326. Schematic grids are reserved
   for pure topology diagrams and must be labeled SCHEMATIC.
2. **Full regional extent.** Show the whole basin PLUS its neighbors and
   context. Senegal example: Mauritania border (17.5°N) through
   Guinea-Bissau (12°N), offshore past the 2000 m isobath, Cape Verde
   islands included. A cropped "just the blocks" extent was rejected.
3. **Declare provenance** in the figure footer: projection, coastline source,
   data sources. Add `[OBS/DER/INT]` epistemic tag in the caption.

## Working Stack (proven)

```
GeoPandas  → reads Natural Earth shapefiles, handles multipolygons correctly
Rasterio   → bathymetry GeoTIFF (synthetic morphological model if no DEM)
Matplotlib → rendering, dark Mode B theme
```

### Why GeoPandas and not the alternatives

- `cartopy.cfeature` auto-download path failed on this host (`GEOSException:
  Points of LinearRing do not form a closed linestring`) — stale downloaded
  data. `pyshp` (`shapefile.Reader`) only yields the first ring per shape,
  silently dropping multipolygon islands (Cape Verde vanished). **GeoPandas
  `gpd.read_file()` handles both correctly.**
- Local data lives at:
  `/root/.local/share/cartopy/shapefiles/natural_earth/{physical,cultural}/`
  (`ne_50m_land`, `ne_50m_coastline`, `ne_50m_ocean`,
  `ne_50m_admin_0_boundary_lines_land`).

### Core rendering loop

```python
import geopandas as gpd
land_gdf = gpd.read_file(f'{shp_dir}/physical/ne_50m_land.shp')
land_view = land_gdf.cx[-24:-10, 9:21]          # bbox spatial slice
for geom in land_view.geometry:
    polys = geom.geoms if geom.geom_type == 'MultiPolygon' else [geom]
    for poly in polys:
        xs, ys = poly.exterior.xy
        ax.fill(xs, ys, facecolor='#3d2e1f', edgecolor='#5a4828', lw=0.3, zorder=2)
# same pattern for coastlines/borders: iterate .cx-sliced geometry,
# branch on LineString vs MultiLineString
```

### Blocks and wells as GeoDataFrames

Store licensing blocks and wells as `gpd.GeoDataFrame` with `crs='EPSG:4326'`
(Polygon / Point geometry + name/operator/status/year columns). Iterate
`.iterrows()` to render; block centroid = `np.mean(exterior coords)`. This
makes the figure data auditable (F2) instead of freehand decoration.

### Bathymetry without a DEM download

If no internet DEM is reachable, synthesize a GeoTIFF from continental
margin morphology and tag it DER:

```python
dist_km = (coast_lon - X) * 105          # ~105 km per °lon at 15°N
depth = np.where(dist < 80, dist*12, 80*12 + (dist-80)*35)  # shelf then slope
# write with rasterio.open(path,'w',driver='GTiff',crs='EPSG:4326',
#   transform=from_bounds(...), ...) then imshow with a blue LinearSegmentedColormap
```

Prefer real GEBCO/ETOPO tiles when download is possible.

### Label placement

Never stack annotations on top of markers. Use a manual offset dict with
leader lines (`ax.annotate('', xy=well_xy, xytext=label_xy, arrowstyle='-')`
+ offset text box). Spread key-well labels to the four quadrants.

### Scale bar + north arrow

1° longitude ≈ 105 km at 15°N — state the latitude basis. Scale bar with
end ticks and subdivision ticks; north arrow top-right with gold accent.

## Verification (mandatory before PDF assembly)

Run `vision_analyze` on the rendered PNG asking: coastlines visible? all
neighbor countries rendered? bathymetry gradient present? labels readable,
no overlap? Two vision passes caught a dropped landmass and label stacking
in the proven session. Fix, re-render, re-verify.

## Proven

- 2026-08-20: GEOX Senegal Basin figures v3 — Fig 4 real map (Natural Earth
  50m, GeoDataFrame blocks/wells, rasterio bathymetry), user-approved after
  two rejections of earlier schematic versions.
