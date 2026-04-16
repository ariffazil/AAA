# GEOX_ROADMAP.md — 2026-04-12 · v4 SEALED

## Version History
| Version | Date | Status |
|---------|------|--------|
| v1.0 | ~Mar 2026 | Static pages |
| v2.0 | ~Mar 2026 | Map portal + draw/measure |
| v3.0 | ~Apr 2026 | Layer system + inspector + tray |
| **v4.0** | **2026-04-12** | **GEBCO WMS fixed · MacroSTRAT probe · mobile CSS · visual polish** |

---

## GEOX Platform — Horizon Map

```
HORIZON A — SPATIAL COMMONS (current, SEALED v4)
├── MAP v4 ✅
│   ├── OSM / Satellite basemap ✅
│   ├── GEBCO Bathymetry WMS (tileLayer.wms, 131KB tile confirmed) ✅
│   ├── USGS Earthquakes M4.5+ (GeoJSON on init) ✅
│   ├── MacroSTRAT Paleogeography 50Ma (toggled GeoJSON) ✅
│   ├── MacroSTRAT Geologic Units (point-probe on click, LIVE data) ✅
│   ├── Natural Earth Boundaries (ArcGIS tiles, partial) ✅
│   ├── Drawing + Measure tools (marker/line/area/clear) ✅
│   ├── Inspector panel (7 sections: point/geology/quakes/verify/chain/provenance/handoff) ✅
│   ├── Bottom tray (3 tabs: query log / fetch status / errors) ✅
│   ├── MCP chains wired (verify / context / signals → callTool JSON-RPC) ✅
│   └── Mobile responsive CSS (≤768px / ≤480px, map 55vh) ✅
│
├── PROSPECT ⚠️  [needs audit]
├── WIKI ⚠️  [needs audit]
├── STATUS ✅  [needs 888 HOLD check]
└── TOOLS ⚠️  [needs audit]

HORIZON B — PROVENANCE ENGINE
├── Layer contract registry (JSON schema, per-layer source/license/CRS/status)
├── Fetch status auto-logging (bottom tray)
├── GEBCO WMS tile verification on toggle
└── Provenance export (inspector provenance section)

HORIZON C — AOI + CROSS SECTION
├── Polygon AOI → MCP chain
├── CROSS section tool (2D slice)
├── EARTH3D volume viewer
└── Well/section correlation panel

HORIZON D — FAULT + SUBSURFACE
├── USGS Quaternary Faults — BLOCKED (no stable public GeoJSON)
├── GEM Global Active Faults — BLOCKED (no stable public GeoJSON)
├── SRTM Hillshade — DEFERRED (needs tile pipeline)
├── IRIS seismic metadata — Tier 3
└── High-res bathymetry — Tier 3

HORIZON E — CRS + TRANSFORM
├── proj4 wiring for EPSG transform utility
├── Explicit EPSG surface in inspector
├── Coord transform panel (input any CRS → output target CRS)
└── Layer CRS auto-detection + on-the-fly reproject

HORIZON F — SEO + DISCOVERABILITY
├── sitemap.xml for geox-site
├── robots.txt
├── canonical URLs
├── /llms.txt for LLM ingestion
└── OpenGraph meta tags

HORIZON G — AUTONOMOUS MONITORING
├── Cron-layer health checks
├── Auto-alert on layer failure
├── status.json auto-generation
└── Traefik routing health monitor

HORIZON H — GEOSCIENCE WORKFLOWS
├── Well stratigraphy cross-correlation
├── P10/P50/P90 volume estimation
├── Play fairway scoring
├── Charge risk assessment
└── Seal/fault trap analysis
```

---

## Done This Session (2026-04-12)
- [x] GEOX MAP v4 deployed — GEBCO WMS fixed, probe working, real geology data showing
- [x] Mobile CSS for Android (≤768px / ≤480px) — map 55vh, sidebar top bar, inspector bottom
- [x] Inspector panel (7 sections) live
- [x] Bottom tray (3 tabs) live — GEBCO tile confirmed, USGS loaded, MacroSTRAT confirmed
- [x] MCP chains wired (verify / context / signals)
- [x] Layer catalog (10 entries, status honest: live/partial/blocked/deferred)
- [x] Visual polish — margins, spacing, active tab green underline, tray 110px
- [x] Commits: f7b04819 (polish) + c9dc827c (mobile fix)

## In Progress
- [ ] GEOX_ROADMAP.md / TODO.md / README.md files (writing now)
- [ ] Wiki update

## Next Up
1. Click chain end-to-end test (user interaction — probe confirmed working in screenshot)
2. arifosmcp server.json regeneration (tool count + version mismatch)
3. /prospect and /wiki pages audit
4. SEO layer (sitemap.xml, robots.txt)
5. status.json generation for geox-site

---

## Principles
- **DITEMPA BUKAN DIBERI** — forged, not given
- GEOX dimension tags: `map`, `well`, `prospect`, `section`, `earth3d`, `time4d`, `physics`, `cross`
- Federate don't mirror — prefer BBOX queries, tiles, WMS, STAC/COG patterns
- Provenance always visible — no fake "LIVE" labels
- arifOS governance: **VERDICT before FORCE**
