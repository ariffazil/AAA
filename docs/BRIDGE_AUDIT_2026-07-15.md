# Cross-organ bridge audit — 2026-07-15

| Direction | Canonical path(s) | Notes |
|-----------|-------------------|--------|
| GEOX → WEALTH | `GEOX/adapters/wealth_bridge.py` · `src/geox_core/seismic_pipeline/geox_wealth_bridge.py` | Public MCP wealth tools deregistered; adapter/feed only |
| WEALTH → GEOX schemas | `WEALTH/wealth_mcp/resources/translation/` (if present) | Translation only |
| WELL → GEOX | `WELL/well_mcp/resources/bridge_geox.py` | No geology authority |
| WELL → WEALTH | `WELL/well_mcp/resources/bridge_wealth.py` + `well_handoff_livelihood_to_wealth` | Session_id gap open |
| WELL → arifOS | `bridge_arifos_kernel.py` · dignity handoff | Prefer arif_init session |
| WEALTH → arifOS | `wealth_arifos_bridge/` | Judge envelope |

**Verdict:** Bridge set is singular-enough for zen; do not add new cross-organ compute paths without BOUNDARY update.
