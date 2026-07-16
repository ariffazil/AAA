# Truth Kernel — Post-Unification Diagnosis

**Date:** 2026-07-16T20:00Z
**Status:** Architecture correct. Implementation partially compliant. 3 bugs fixed, 4 real drift issues remain.

## Bugs Fixed

| Bug | Fix | File |
|-----|-----|------|
| TypeScript regex missed `tool_name:` pattern | Added `tool_name\s*:\s*` regex + `readonly name =` regex | build_card.py |
| GEOX source path wrong (`/root/geox` → `/root/GEOX`) | Updated ORGANS dict, added `source_paths` multi-path support | build_card.py |
| Dict-in-card tools crashed GEOX | Filter `isinstance(t, str)` before extending | build_card.py + acceptance_test.py |

## Real Drift (Verified)

| Organ | Source | Registry (MCP) | Card | Issue |
|-------|--------|----------------|------|-------|
| arifOS | 59 | 0 (probe fails) | 8 | MCP tools/list returns empty; 59 source includes internal+absorbed tools |
| A-FORGE | 7 | 109 | 20 | Source regex only catches gatewayTools.ts registrations; 102 tools registered elsewhere |
| GEOX | 115 | 0 (probe fails) | 20 | 115 includes public+internal; MCP probe fails |
| WEALTH | 12 | 0 (probe fails) | 12 | Source correct; MCP probe fails |
| WELL | 0 | 29 | 20 | Source uses `mcp_P_well_*` pattern, not `well_*`; probe correct |

## Root Causes

1. **MCP probe format mismatch**: arifOS, GEOX, WEALTH don't respond to standard `tools/list`. Their MCP servers use different transport or endpoint format. The probe function needs organ-specific probing.

2. **Source enumeration too narrow**: A-FORGE tools are registered in multiple files (gatewayTools.ts + individual tool classes + index.ts). The regex only catches one registration pattern.

3. **WELL naming mismatch**: Source code uses `mcp_P_well_*` and `mcp_E_well_*` patterns, not `well_*`. The tool_prefix doesn't match.

4. **GEOX has 115 tools in source but only 20 are public**: The source enumeration picks up all tools (public + internal + test). Need to distinguish public from internal.

## What's NOT broken

- Card genesis script runs without crashes ✅
- Drift detection logic is correct ✅
- Registry receipt hash computation works ✅
- Card emission works ✅
- Acceptance test works ✅
- Dead name detection works ✅ (zero false DEAD NAMEs after fix)
- Schema v2.3.0 is valid ✅
- Boot contract PARTIAL state is defined ✅
- 777-forge is stripped ✅
- Superseding receipt exists ✅

## Next steps

1. Fix MCP probe to use organ-specific endpoints (arifOS: `/health` canonical_tools, GEOX: `CANONICAL_PUBLIC_SURFACE.json`, WEALTH: `capital_registry`)
2. Fix source enumeration for A-FORGE (scan all .ts files in src/, not just tools/)
3. Fix WELL source prefix to match `mcp_P_well_*` pattern
4. Filter GEOX source to public-only tools
