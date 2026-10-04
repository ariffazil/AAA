#!/usr/bin/env python3
"""GEOX MCP Tool Consolidation Script — reference template.

This script was used for GEOX's tool consolidation (50→58 with shims).
Adapt the ABSORBED_TOOLS list and MERGED_CODE block for other organs.

Usage:
    python3 /tmp/gapox_consolidate.py
    cd /root/GEOX && PYTHONPATH=src python3 -c \
      "from geox_mcp.tools_wiring import register_tools_on; from fastmcp import FastMCP; mcp = FastMCP('t'); register_tools_on(mcp); print(f'OK: {len(mcp._local_provider._components)} tools')"
"""
# fmt: off
ABSORBED_TOOLS = [
    # GROUP 1: geox_temporal absorbs these
    "geox_temporal_decline", "geox_temporal_rrr",
    "geox_temporal_basin_lifecycle", "geox_temporal_cadence",
    # GROUP 2: geox_map absorbs these
    "geox_map_layers_list", "geox_map_scene_plan", "geox_map_render_preview",
    # GROUP 3: geox_source absorbs these
    "geox_source_rock", "geox_diagenesis",
    # GROUP 4: geox_spatial absorbs these
    "geox_h3_spatial_index", "geox_lancedb_embed_store", "geox_stac_discover",
    # GROUP 5: geox_deep_time absorbs this
    "geox_dde_reason",
    # GROUP 6: geox_claim absorbs these (including itself)
    "geox_claim", "geox_falsify", "geox_evidence_synthesize",
    "geox_contradiction_scan", "geox_evidence",
    # GROUP 7: geox_model absorbs these
    "geox_subsurface_model", "geox_geological_model_generate",
    "geox_gempy_implicit_3d",
    # GROUP 8: geox_well absorbs these
    "geox_well_view", "geox_well_desk",
    # GROUP 9: geox_petrophysics absorbs these
    "geox_sequence", "geox_lem_predict",
    # GROUP 10: geox_seismic_interpret absorbs this
    "geox_visual_understand",
    # GROUP 11: geox_seismic_compute absorbs this
    "geox_avo_forward",
    # GROUP 12: geox_basin absorbs these
    "geox_basin_backstrip", "geox_thermal_maturity_history",
    # GROUP 13: geox_workspace absorbs this
    "geox_surface_status",
]

# KEY PATTERN: Multi-line decorator commenting fix
# WRONG:  while end < len(lines) and ")" not in lines[end]:  # matches ) inside annotations
# RIGHT:
#     end = i
#     while end < len(lines) - 1:
#         end += 1
#         stripped_end = lines[end].lstrip()
#         if stripped_end.startswith(")") or stripped_end.startswith("),"):
#             break

# MERGED_CODE block: see the full script at /tmp/gapox_consolidate.py
# Contains 9 new merged tools + 29 shims inserted before evidence chain section
