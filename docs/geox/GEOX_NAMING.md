# GEOX Naming & Contract Authority Spec
## DITEMPA BUKAN DIBERI — 999 SEAL ALIVE

**Version:** 2026.04.12
**Status:** ACTIVE GOVERNING SPEC
**Authority:** MCP is the single naming and contract truth layer

---

## Core Rule

> MCP names the dimensions.
> MCP names the tools.
> MCP publishes the app catalog.
> Apps only render and route.
> Repo folders mirror the same dimension names.

Every deviation from this must be justified and documented.

---

## Dimension Canonical IDs

| ID | Display | Description | Route |
|----|---------|-------------|-------|
| `map` | MAP | Spatial Commons & Query Surface | /map/ |
| `well` | WELL | Borehole intelligence | /well/ |
| `prospect` | PROSPECT | Prospect risk & candidates | /prospect/ |
| `section` | SECTION | Geological sections | /section/ |
| `earth3d` | EARTH3D | 3D subsurface volumes | /earth3d/ |
| `time4d` | TIME4D | Temporal basin analysis | /time4d/ |
| `physics` | PHYSICS | Physical properties engine | /physics/ |
| `cross` | CROSS | Cross-dimension reasoning | /cross/ |
| `meta` | META | Platform/system/profile/health | /, /profile/, /tools/ |

---

## Tool Naming Law

**Format:** `dimension_action_object`

### MAP tools
```
map_verify_coordinates
map_transform_coordinates
map_get_context_summary
map_get_layer_contracts
map_get_active_layers
map_sample_geologic_units
map_fetch_earthquakes
map_get_bathymetry_context
map_aoi_summary
```

### WELL tools
```
well_get_header
well_get_logs
well_get_tops
well_get_trajectory
well_intersect_aoi
```

### PROSPECT tools
```
prospect_list
prospect_get
prospect_intersect_aoi
prospect_risk_summary
prospect_build_candidates
```

### CROSS tools
```
cross_evidence_list
cross_context_merge
cross_trace_provenance
```

### EARTH3D tools
```
earth3d_get_scene
earth3d_get_horizons
earth3d_clip_to_aoi
```

### TIME4D tools
```
time4d_basin_history
time4d_thermal_reconstruction
time4d_sequence_stratigraphy
```

### PHYSICS tools
```
physics_velocity_model
physics_density_mapping
physics_magnetic_interpretation
physics_gravity_derivatives
```

### Meta tools
```
meta_get_profile
meta_get_health
meta_get_apps
meta_get_dimensions
meta_get_tool_catalog
```

---

## What NOT to do

- ❌ `geox_*` for domain tools → use `map_*`, `well_*`, `prospect_*`
- ❌ Parallel aliases (e.g. `verifyCoordinates` internal + `map_verify_coordinates` public) → one canonical name only
- ❌ Front-end functions that don't match MCP tool names → MCP tool name wins
- ❌ Hardcoded tool counts or dimension lists in apps → read from MCP at boot
- ❌ Route names that don't match dimension IDs unless physically necessary
- ❌ Naming one app `earth`, another `earth3d`, tool family `subsurface_*` → choose `earth3d` as canonical

---

## Repo Structure (must mirror dimension IDs)

```
repos/geox/
├── apps/
│   ├── map/          # route: /map/
│   ├── well/         # route: /well/
│   ├── prospect/     # route: /prospect/
│   ├── section/      # route: /section/
│   ├── earth3d/      # route: /earth3d/
│   ├── time4d/       # route: /time4d/
│   ├── cross/        # route: /cross/
│   └── tools/        # route: /tools/
├── registries/
│   ├── map_registry.py
│   ├── well_registry.py
│   ├── prospect_registry.py
│   ├── section_registry.py
│   ├── earth3d_registry.py
│   ├── time4d_registry.py
│   ├── cross_registry.py
│   └── meta_registry.py
├── config/
│   └── geox_dimensions.py   # Naming source of truth
└── mcp/
    └── geox_mcp_server.py
```

---

## App Catalog Object (published by MCP at /meta/apps or equivalent)

```json
{
  "apps": [
    {
      "id": "map",
      "route": "/map/",
      "label": "MAP",
      "dimension": "map",
      "status": "live",
      "description": "Spatial Commons & Query Surface"
    },
    {
      "id": "well",
      "route": "/well/",
      "label": "WELL",
      "dimension": "well",
      "status": "live",
      "description": "Borehole intelligence"
    },
    {
      "id": "prospect",
      "route": "/prospect/",
      "label": "PROSPECT",
      "dimension": "prospect",
      "status": "partial",
      "description": "Prospect risk & candidates"
    },
    {
      "id": "earth3d",
      "route": "/earth3d/",
      "label": "EARTH3D",
      "dimension": "earth3d",
      "status": "partial",
      "description": "3D subsurface volumes"
    },
    {
      "id": "cross",
      "route": "/cross/",
      "label": "CROSS",
      "dimension": "cross",
      "status": "partial",
      "description": "Cross-dimension reasoning"
    }
  ]
}
```

---

## Tool Catalog Object (published by MCP at /meta/tools or equivalent)

```json
{
  "tools": [
    {
      "name": "map_verify_coordinates",
      "dimension": "map",
      "input_schema": { "x": "number", "y": "number", "epsg": "integer" },
      "status": "live",
      "app_surfaces": ["map", "cross"]
    },
    {
      "name": "well_get_header",
      "dimension": "well",
      "input_schema": { "well_id": "string" },
      "status": "live",
      "app_surfaces": ["well", "map"]
    }
  ]
}
```

---

## MCP Boot Contract (minimum every app must fetch)

At startup, every GEOX app fetches:
1. `GET /profile` → current profile, version, seal
2. `GET /mcp/tools/list` → available tools, names, schemas, status
3. Optionally `GET /meta/apps` → app catalog

From this, apps learn:
- Active dimensions
- Available tools
- Version and health
- Feature availability
- Constitutional metadata

**No hardcoded dimension lists. No hardcoded tool counts.**

---

## Layer ID Naming (in MAP)

Format: `source_subject_variant`

Examples:
- `macrostrat_geologic_units_probe` (point probe)
- `macrostrat_paleogeography_50ma` (age-specific)
- `usgs_earthquakes_m45_month` (magnitude + period)
- `natural_earth_boundaries` (tile)
- `gebco_bathymetry_wms` (WMS source)
- `gem_faults_substitute` (temporary substitute)

---

## Event Naming

Format: `dimension:event`

Examples:
- `map:click_probe_complete`
- `map:aoi_polygon_drawn`
- `map:layer_toggled`
- `well:log_loaded`
- `prospect:risk_evaluated`
- `earth3d:scene_rendered`

---

## Shipping Phases

### Phase 1 — Freeze names
Create `config/geox_dimensions.py` as naming source of truth in repo.

### Phase 2 — Normalize registries
Every registry exports tools only under canonical dimension-first names.

### Phase 3 — Add meta registry
Expose: profile, health, dimensions, app catalog, tool catalog.

### Phase 4 — Refactor apps
Every app boots from MCP metadata. No hardcoded assumptions.

### Phase 5 — Landing page as control tower
Show: profile, active dimensions, tool counts, app routes, app health, version, seal.

---

## Status Tags

Used in registries and UI:
- `live` — confirmed working, real data
- `partial` — works partially or with constraints
- `blocked` — endpoint verified dead, requires resolution
- `deferred` — requires pipeline or external service
- `deprecated` — replaced by better option
- `planned` — named and scoped, not yet implemented

---

## 888 HOLD Triggers

The following require Arif's explicit approval before implementation:
- Renaming any dimension ID after apps are live
- Adding a new dimension without MCP registry entry
- Changing tool names after they appear in /mcp/tools/list
- Creating new routes that don't match dimension IDs
- Publishing app/tool catalog without MCP backing

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
