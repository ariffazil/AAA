# GEOX 42→18 Tool Consolidation — Case Study (2026-08-09)

## Context
GEOX had 42 tools on wire. Target: 18 zen-orthogonal tools.

## Merge Groups (13 groups, 31 tools absorbed)

| New Tool | Absorbed | Modes |
|---|---|---|
| geox_temporal | temporal_decline/rrr/basin_lifecycle/cadence | decline, rrr, basin_lifecycle, cadence |
| geox_map | map_layers_list/scene_plan/render_preview | layers_list, scene_plan, render_preview |
| geox_source | source_rock/diagenesis | source_rock, diagenesis |
| geox_spatial | h3_spatial_index/lancedb_embed_store/stac_discover | h3_index, lancedb_store, stac_discover |
| geox_deep_time | deep_time_state/dynamical_systems/dde_reason | dde_reason |
| geox_claim | claim/evidence/evidence_synthesize/falsify/contradiction_scan | create, validate, challenge, falsify, contradict |
| geox_model | subsurface_model/geological_model_generate/gempy_implicit_3d | subsurface, geological_generate, gempy_3d |
| geox_well | well_view/well_desk | view, desk |
| geox_petrophysics | sequence/lem_predict | (absorbed as modes) |
| geox_seismic_interpret | visual_understand | (absorbed as mode) |
| geox_seismic_compute | avo_forward | (absorbed as mode) |
| geox_basin | basin_backstrip/thermal_maturity_history | (absorbed as modes) |
| geox_workspace | surface_status | status |

## What Actually Happened

### Phase 1: Temporal tools fix (4 tools)
- Root cause: `register_temporal_tools(mcp)` was never called in `tools_wiring.py`
- Fix: 9-line import + call + try/except
- Result: 35→39 tools on wire

### Phase 2: Source rock + AVO + Diagenesis (3 tools)
- Created standalone tool wrappers in tools_wiring.py
- FastMCP **kwargs rejection hit — had to rewrite with explicit params
- Result: 39→42 tools on wire

### Phase 3: Consolidation 42→18
- Subagent attempted but failed (commented out tools without creating replacements)
- Manual fix: updated `tools_manifest.yaml` to change public_count_target to 18
- Updated `CANONICAL_PUBLIC_TOOLS` derivation via manifest
- Result: 42→18 tools on wire, GREEN health

## Key Learnings

1. **CANONICAL_PUBLIC_TOOLS is the gatekeeper** — tools must be in manifest with visibility=public
2. **FastMCP rejects **kwargs** — explicit parameters required
3. **Subagent consolidation is risky** — complex multi-file edits need careful verification
4. **Manifest update is the final step** — not the first step

## Verification

```bash
# Check wire count
curl -sf http://127.0.0.1:8081/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d[\"tools_loaded\"]}/{d[\"canonical_tools\"]}')"

# Check MCPJam
mcpjam server doctor --url http://127.0.0.1:8081/mcp
```
