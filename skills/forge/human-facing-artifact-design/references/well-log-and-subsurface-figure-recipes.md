# Well log, basemap and subsurface-figure recipes

Recipes for technical artifacts built from well data and real geography. Every pattern here was
executed against real files; the pitfalls are the ones that produced a broken figure first. Pair this
with §1 of SKILL.md — for a specialist reader the discipline's own figures are part of the argument,
and every schematic element must be labelled `schematic` / `indicative` in subtitle *and* caption.

---

## 1. LAS parsing — the contract the header does not state

A hand-rolled LAS 2.0 reader is ~40 lines and removes a library dependency, but four properties of real
files defeat the naive version. Handle all four or every curve is silently wrong.

```python
# ~CURVE section, one curve per line:  MNEM.UNIT  API  :  INDEX  DESCRIPTION
#   GR.GAPI        -> mnemonic is GR, not GR.GAPI
#   DEPT.M         -> DEPT
#   AC.US/F        -> AC
curves.append(parts[0].strip().split(".")[0].strip().upper())
```

1. **Mnemonics carry unit suffixes.** `GR.GAPI`, `DEPT.M`, `AC.US/F`, `ABDCQF01.g/cm3`. Taking the raw
   first token leaves the unit attached, so a lookup for `GR` misses and the curve reads as empty — and
   an empty curve renders as a blank track, not an error. Split on `.` and keep the head. Newer files
   drop the suffix entirely, so always index from the parsed list rather than assuming either shape.
2. **The data block may carry more columns than the curve header declares.** Compute
   `shift = n_data_cols - n_curves` once and offset every curve index by it. Getting this wrong shifts
   the whole log one channel: the figure renders, looks plausible, and is wrong everywhere. Print the
   reconciliation on every ingest — `print("data cols %d, parsed curves %d, shift %d")` — so the next
   session sees it rather than rediscovering it.
3. **Depth units are mixed across files in one project.** One file in metres and its neighbour in feet
   is normal, and the unit metadata frequently does not survive (`STOP.F` is the only tell and it is
   often absent). Detect from magnitude — `np.nanmax(depth) > 8000` is a metre-vs-feet tell for well
   data — and print the guess. Never assume a suite is uniform.
4. **The null sentinel is per-file and must be read, not assumed.** `-999.25` is conventional but is
   declared in `~WELL`. Compare with a threshold, not equality, and convert to `np.nan` before any
   statistic: one `-999.25` averaged into a porosity series destroys the answer silently.

**`~CURVE` can begin with comment rows** (`#MNEM .UNIT …`). Skip any line whose first token starts with
`#` or that does not yield two parseable tokens.

---

## 2. Log-track and petrophysics panels

### Depth handling
Plot depth positive and `invert_yaxis()`. On a multi-track panel keep the y tick labels on the leftmost
axes only and `set_yticklabels([])` on the rest, so every track shares one depth frame. A depth axis
labelled "depth below sea level" but drawn −25…0 inverts the meaning — the reader parses a negative
depth. A vision pass catches this; a code review does not.

### Two-scale curves in one track (RHOB and NPHI)
Do not put a g/cc curve and a v/v curve on one linear axis; neither can be read off it. Use a twin axis
with a *matched* scale so the curves cross at the porosity crossover:

```python
ax_r = fig.add_subplot(gs[0, 3])
ax_r.plot(RHOB, d, color="#7a3ea1")
ax_r.set_xlim(1.95, 2.75)
ax_n = ax_r.twiny()
ax_n.plot(NPHI, d, color="#1d6b3a", ls="--")
ax_n.set_xlim(-0.80, 0.0)                # reversed, so the two scales align visually
ax_r.set_title("RHOB / NPHI", pad=20)    # pad clears the twin axis's own label
```
Give the twin axis its own coloured tick labels and put both unit strings in the x-labels — the track
title alone cannot say which curve uses which scale.

### Net-pay flag
Draw the flag on **every** track as a translucent band, plus one solid bar in a nominated track:
`fill_betweenx(d, 0, 1, where=pay, transform=ax.get_yaxis_transform(), color=..., alpha=0.14, zorder=0)`
spans the full track width regardless of each track's own x-limits.

---

## 3. Multi-well correlation — one axes, computed track origins

Subplot-per-track plus figure-space connectors is the layout that fails: connectors miss the curves,
and a curve-indexing mismatch leaves whole panels blank while the script still reports success. Use a
single axes and place every track in data coordinates.

```python
W, gap = 100.0, 26.0                     # track width and gutter, in data units
T = [i * (W + gap) for i in range(6)]    # track origins

def draw(d, v, x0, lo, hi, colour):
    mk = np.isfinite(d) & np.isfinite(v) & (d >= zlo) & (d <= zhi)
    xs = x0 + (np.clip(v, lo, hi) - lo) / (hi - lo) * W
    ax.plot(xs[mk], d[mk], color=colour, lw=0.6)
    ax.axvspan(x0, x0 + W, color="#fbfcfd", zorder=0)

ax.set_xticks([])                        # the x axis is a layout, not a scale
ax.set_ylim(zhi, zlo)
```

Correlation levels become ordinary `ax.plot` calls across every track plus a curved connector
(`ys = lv + amp * np.sin(np.pi * (xs - x1) / (x2 - x1))`). Because everything shares one transform
nothing can drift. Add a vertical rule between the well groups and put each well's name above its own
group.

**Look at the rendered panel before believing it.** A blank right-hand well means bad curve indexing,
not bad data.

---

## 4. A real basemap without GeoPandas

When cartopy or geopandas is unavailable, or its Natural Earth download is blocked, matplotlib plus
cached GeoJSON is enough for a regional location map:

```python
base = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
for f in ["ne_10m_land.geojson", "ne_10m_coastline.geojson",
          "ne_10m_admin_0_boundary_lines_land.geojson"]:
    urllib.request.urlretrieve(base + f, os.path.join(cache, f))
```

**Use 10m or 50m, never 110m.** At 110m an entire continent is one polygon whose vertices sit at extreme
latitudes, so a bbox filter over a basin-scale window returns nothing.

Clip by bbox with a minimum-vertex threshold, buffering the box slightly so rings that cross the frame
are not dropped:

```python
def rings(fc, lon0, lon1, lat0, lat1, minverts=3, pad=2.0):
    out = []
    for feat in fc["features"]:
        g = feat.get("geometry")
        if not g:
            continue
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in polys:
            for ring in poly:
                a = np.asarray(ring, float)
                if a.ndim != 2 or len(a) < 3:
                    continue
                m = ((a[:, 0] >= lon0 - pad) & (a[:, 0] <= lon1 + pad) &
                     (a[:, 1] >= lat0 - pad) & (a[:, 1] <= lat1 + pad))
                if m.sum() >= minverts:
                    out.append(a[m])
    return out
```

Land as `Polygon` patches; coastline and admin boundaries as `ax.plot` line strings; and
`ax.set_aspect(1.0 / np.cos(np.radians(mean_lat)))` so the geography is not stretched.

**Label every element you did not measure.** Block outlines, isobaths, structural axes and well
positions are `indicative` when the public sources give distance and bearing rather than coordinates.
Say so in the subtitle *and* the legend. Put the legend **below** the map frame
(`bbox_to_anchor=(0.5, -0.055)`), never over the data — an opaque legend box costs map area and reads
as a defect. An unlabelled schematic presented as a licence map is the one error in this genre a
specialist reader will catch.

---

## 5. Subsurface number integrity

These keep a figure admissible. They are rules, not style preferences, and they apply to any artifact
carrying a subsurface number.

- **Report the computed zero.** If the cut-offs return no net pay, print `0.0 m` and say so. Widening a
  cut-off until a pay flag appears converts an evaluation into a sales document, and a reader who
  spot-checks it stops trusting every other number on the page.
- **When an assumed parameter controls the answer, plot its sensitivity instead of hiding it.** Rw,
  matrix density, net-to-gross and cut-offs are usually assumed, not measured. A panel of net pay
  against the assumed value, with the adopted value marked, converts an unverifiable number into a work
  item: *this zone is resolved by a produced-water sample or a Pickett plot, not by tuning cut-offs.*
- **Never claim a tie correlation without the thing you would tie to.** A synthetic seismogram built
  from the logs is a synthetic, not a well tie. A "correlation coefficient" against a seismic volume
  that was never loaded is a number the author could not have measured. State the cross-check that
  *was* performed — e.g. the modelling engine's normal-incidence synthetic agreeing with the Zoeppritz
  intercept at the modelled interface — and state plainly that no field seismic was loaded.
- **An AVO class is not a fluid indicator.** A Class I (hard) response with a near-zero gradient is what
  a clean, fast, low-porosity sand against a slower shale produces. Report the class as a rock-property
  observation, and say what it does not establish, or the label will be read as a hydrocarbon verdict.
- **No published formation tops means the picks are candidates.** Label correlation levels as candidate,
  say they are picked on log shape, and add what would make them real: a well grid, an offset tie, a
  deviation-corrected depth frame.
- **MD is not TVD.** When no deviation survey was supplied, put "measured depth throughout, no TVD
  correction applied" on the figure. A deviated well's depth axis read as true vertical is a systematic
  error the reader cannot see.
- **Declare the petrophysical constants on the figure.** Vsh method and GR endpoints, the porosity model
  with its matrix and fluid densities, and Archie's a / m / n / Rw. A porosity panel with no stated
  matrix density cannot be checked.
- **The tool's own refusal is a finding.** When the evaluation engine returns `INVALID — supply curves
  first`, or the well loader reports its own UWI and curve-count mismatches, print that in the artifact
  beside the successes. A control that reports its own failures is more credible than one that reports
  only success, and the failures are usually real defects worth fixing.
