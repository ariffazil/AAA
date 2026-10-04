# GEOX Tool Consolidation: 42→20 — Reference

> Two sessions attempted this. Session 1 (2026-08-09) got to 18 tools (no shims) but was interrupted. Session 2 (2026-08-10) completed with shims (58 tools). Target remains 20 core tools.

## Session 2 Result (2026-08-10)

58 tools after consolidation (30 absorbed, 9 new merged, 29 shims).
The increase from 50→58 is because:
- Unified server independently registers 96+ tools (tools_wiring.py can't suppress these)
- Shims add back old tool names as thin wrappers
- The 9 new consolidated tools are genuinely new

**To reach 20:** Remove shims and also suppress absorbed tools in the unified server (server.py/unified.py), not just tools_wiring.py.

## Session 1 Result (2026-08-09)

18 tools on wire after fixing 39 broken comment lines.
Syntax errors from orphaned `name=`/`annotations=` lines after partial commenting.
This was the "no shims" approach — cleaner count but no backwards compat.

## The Multi-Line Decorator Bug (CRITICAL)

When commenting out multi-line `@mcp.tool(` decorators:

```python
@mcp.tool(
    name="geox_geological_model_generate",
    annotations=_geox_annotations("geox_geological_model_generate"),
)
```

**WRONG:** `while ")" not in lines[end]` — stops at annotations line because `_geox_annotations(...)` contains `)`.

**RIGHT:** `while not lines[end].lstrip().startswith(")")` — looks for the actual closing paren line.

This caused syntax errors in both sessions. Session 1 fixed 39 broken lines. Session 2 avoided it with the correct pattern.

## Target: 20 Consolidated Tools

| # | Tool Name | Status | Modes (absorbed old tools) |
|---|-----------|--------|---------------------------|
| 1 | geox_well | NEW | view, desk |
| 2 | geox_well_ingest | UNCHANGED | — |
| 3 | geox_well_qc | UNCHANGED | — |
| 4 | geox_petrophysics | MODIFY | +sequence, +lem_predict |
| 5 | geox_seismic_ingest | UNCHANGED | — |
| 6 | geox_seismic_interpret | MODIFY | +visual_understand |
| 7 | geox_seismic_compute | NEW | avo_forward |
| 8 | geox_prospect | UNCHANGED | — |
| 9 | geox_basin | MODIFY | +backstrip, +thermal_maturity |
| 10 | geox_claim | NEW | create/validate/challenge/seal/attach + falsify + evidence + scan |
| 11 | geox_temporal | NEW | decline, rrr, basin_lifecycle, cadence |
| 12 | geox_source | NEW | source_rock, diagenesis |
| 13 | geox_model | NEW | subsurface, geological_generate, gempy_3d |
| 14 | geox_spatial | NEW | h3_index, lancedb_store, stac_discover |
| 15 | geox_map | NEW | layers_list, scene_plan, render_preview |
| 16 | geox_deep_time | NEW | dde_reason |
| 17 | geox_workspace | MODIFY | +surface_status |
| 18 | geox_physical_reality_interpret | UNCHANGED | — |
| 19 | geox_simulate_routing | UNCHANGED | — |
| 20 | geox_biostrat_calibrate | UNCHANGED | — |

## Implementation Files

| New Tool | Primary Implementation File |
|----------|---------------------------|
| geox_well | inline (well_desk, well_view) |
| geox_seismic_compute | geox_core.avo.avo_forward + castagna |
| geox_temporal | geox.egs.tools.temporal |
| geox_source | geox_core.source_rock.parameters + diagenesis.compaction |
| geox_model | subsurface_model.py, gempy_implicit_3d.py, inline geological_model |
| geox_spatial | h3_spatial_index.py, lancedb_embed_store.py, stac_discover.py |
| geox_map | earth_map.py |
| geox_deep_time | dde_reason.py |

## What Works (Session 2)

1. Consolidation script at `/tmp/gapox_consolidate.py` — working, syntax-valid
2. 9 new merged tools registered successfully
3. 29 backwards-compat shims registered
4. GEOX service unaffected (not restarted)
5. Verification command passes

## What Remains for 20-Tool Target

1. Remove shims (29 tools) → count drops to 29
2. Suppress absorbed tools in unified server (server.py) → count drops to ~20
3. Alternatively: don't add shims at all (Session 1 approach) → 18 tools

## Test Command

```bash
cd /root/GEOX && PYTHONPATH=src:/usr/local/lib/python3.13/dist-packages python3 -c "
from geox_mcp.tools_wiring import register_tools_on
from fastmcp import FastMCP
mcp = FastMCP('t')
register_tools_on(mcp)
print(f'OK: {len(mcp._local_provider._components)} tools')
"
```

FastMCP 3.4.4 API — no `_tool_manager`. Use `_local_provider._components`.
