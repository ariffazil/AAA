# GEOX | Spatial Commons

> *"Ditempa Bukan Diberi"* — Forged, not given.

**Live:** `https://geox.arif-fazil.com/map/index.html`

---

## What is GEOX?

GEOX is a **spatial reasoning surface** for exploration geoscience — not a map viewer, not a demo. It provides provenance-tracked, layer-transparent Earth science data overlays with a formal governance layer (arifOS) backing every claim.

**Core thesis:** Without a spatial substrate, WELL / PROSPECT / EARTH3D / TIME4D / CROSS remain fragmented by geometry and interface. GEOX creates one truth-bearing spatial substrate. Tools become workflows. Provenance is always visible.

---

## Current Release — v4 (2026-04-12)

**Map Portal** at `/map/index.html`

### Live Layers

| Layer | Source | Method | Status |
|-------|--------|--------|--------|
| OpenStreetMap | OpenStreetMap | xyz_tile | ✅ LIVE |
| Satellite Imagery | Esri | arcgis_tile | ✅ LIVE |
| GEBCO Bathymetry | GEBCO 2024 | WMS `GEBCO_LATEST` | ✅ LIVE |
| USGS Earthquakes M4.5+ | USGS | GeoJSON (init) | ✅ LIVE |
| Paleogeography 50Ma | MacroSTRAT | GeoJSON (toggle) | ✅ LIVE |
| Geologic Units | MacroSTRAT | Point-probe on click | ✅ LIVE |
| Natural Earth Boundaries | Natural Earth | ArcGIS tiles | ⚠️ PARTIAL |

### Blocked / Deferred

| Layer | Status | Reason |
|-------|--------|--------|
| USGS Quaternary Faults | 🔴 BLOCKED | No stable public GeoJSON path found |
| GEM Global Active Faults | 🔴 BLOCKED | No stable public GeoJSON path found |
| SRTM Hillshade | ⚫ DEFERRED | Requires terrain tile pipeline |

### Architecture

```
LLM (fluency) → GEOX (grounding) → arifOS (governance)
```

- **GEOX** forces Earth reasoning through physics, material constraints, real data, uncertainty, explicit OBS/DER/INT/SPEC
- **arifOS** decides what may be claimed, held, or executed
- **VERDICT before FORCE** — every action tendency judged before execution

---

## Platform Pages

| Path | Description | Status |
|------|-------------|--------|
| `/map/` | Spatial Commons map portal | ✅ v4 LIVE |
| `/index.html` | Platform home | ✅ Updated |
| `/prospect/` | Prospect analysis | ⚠️ Needs audit |
| `/wiki/` | Architecture wiki | ⚠️ Needs audit |
| `/status/` | System status | ✅ Needs 888 HOLD check |
| `/tools/` | Tools registry | ⚠️ Needs audit |
| `/skills/` | Skills catalog | ⚠️ Stub, needs wiring |
| `/workspaces/` | Workspaces | ✅ Static |

---

## Governance

Every layer carries explicit provenance:
- `source_name` / `source_url` / `license`
- `status`: live · partial · blocked · deferred
- `failure_mode` when not live
- `crs` / `serving_method` / `geometry_type`

No fake "LIVE" labels. If it isn't confirmed, it's labelled honestly.

**888 HOLD triggers:**
- Borehole spacing > 10km → continuity claims unreliable
- Unit correlation confidence < 0.6
- Vertical exaggeration > 2x but not disclosed
- Fault geometry not seismic-constrained
- Pinchout/truncation in interpreted zone
- Interval of interest has zero well control

---

## Tiered Ingestion Policy

| Tier | Definition | Examples |
|------|------------|----------|
| **Tier 1** | Always live, global coverage | OSM, Natural Earth, USGS Earthquakes |
| **Tier 2** | Operational geoscience | GEBCO, MacroSTRAT, SRTM, active faults |
| **Tier 3** | Strategic / heavy | IRIS seismic metadata, high-res bathymetry |

Rule: **Federate don't mirror** — prefer BBOX queries, tiles, WMS, STAC/COG patterns.

---

## Dimension Tags

All GEOX content tagged with one or more:

`map` · `well` · `prospect` · `section` · `earth3d` · `time4d` · `physics` · `cross`

---

## Related

- [arifOS](../arifOS/) — constitutional governance kernel
- [GEOX_ROADMAP.md](./GEOX_ROADMAP.md) — full horizon map
- [TODO.md](./TODO.md) — current action items
- [GEOX_NAMING_SPEC.md](./GEOX_NAMING_SPEC.md) — naming conventions

---

*Ditempa Bukan Diberi* · **999 SEAL ALIVE**
