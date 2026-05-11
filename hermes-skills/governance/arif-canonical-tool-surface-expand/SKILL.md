---
name: arif-canonical-tool-surface-expand
category: governance
description: Add a new canonical tool to arifOS — handler, constitutional_map, surface mode rename, and all test fixture updates in the correct order.
---

# arifOS Canonical Tool Surface Expansion

## Trigger
When adding a new canonical tool to arifOS — whether a new `arif_*` capability or an `mcp_*` diagnostic tool. Specifically when:
- Adding a handler to `tools.py`
- Adding the tool name to `constitutional_map.py`
- Any change affecting `CANONICAL_TOOLS` count (e.g., 13→14)

## The 6-Step Expansion Protocol

### Step 1 — Add the handler
In `arifosmcp/runtime/tools.py`:
1. Implement the `_tool_name()` function
2. Add to `_CANONICAL_HANDLERS` dict at the bottom of the file
3. Add to `register_tools()` function if it wraps there

### Step 2 — Add to constitutional_map
In `arifosmcp/constitutional_map.py`:
- Add to `CANONICAL_TOOLS` tuple (13 tools = constitutional, 1 probe = `arif_command_center`)
- Add to `CONSTITUTIONAL_FLOOR_MAP` if it has floor enforcement
- If tool is a probe/diagnostic (not a capability), add to `PROBE_TOOLS` instead

### Step 3 — Update surface mode name (if count changes)
If the canonical tool count changes (e.g., 13→14), the surface mode name must be updated:
1. `arifosmcp/runtime/public_surface.py`:
   - `VALID_PUBLIC_SURFACE_MODES`: rename `canonical13` → `canonical14` (keep alias for backward compat)
   - `normalize_public_surface_mode()`: update default and profile map
   - `public_tool_names_for_mode()`: update field name (e.g., `canonical14_count`)
2. `arifosmcp/runtime/public_registry.py`:
   - Add both `canonical13` and `canonical14` to the routing condition
3. `arifosmcp/runtime/tools.py`:
   - Update `_arif_ping()` `"kernel"` field: `"canonical13"` → `"canonical14"`

### Step 4 — Fix all test files
Find files needing updates:
```bash
grep -rln "canonical13\|== 13\|== 14\|13 tool\|14 tool" tests/ --include="*.py"
```

Common files to update:
- `tests/test_surface_lock.py` — tool count assertions + probe_tools count
- `tests/test_canonical.py` — `assert len(CANONICAL_TOOLS) == 14`, expected tool list, register_tools count
- `tests/test_canonical.py::test_tool_naming_convention` — add `("arif_", "mcp_")` tuple if new tool uses `mcp_` prefix
- `tests/runtime/test_tools_advanced.py` — `tools_registered == 14`, `kernel_tools == 14`
- `tests/runtime/test_mega_tool_audit.py` — HTTP discovery `count == 14`
- `tests/runtime/test_mega_audit.py` — surface count
- `tests/test_public_registry.py` — surface count
- `tests/test_11_mega_tools_gates.py` — surface count
- `tests/test_floors_ci.py` — surface count
- `tests/conftest.py` — docstring "13-tool" → "14-tool"

### Step 5 — Naming convention exception (if needed)
If the new tool doesn't follow `arif_<noun>_<verb>` (e.g., `mcp_health_check`):
```python
# In test_surface_lock.py::test_tool_naming_convention
assert name.startswith(("arif_", "mcp_"))
```

### Step 6 — Verify then commit
```bash
# Quick verification
python3 -c "
from arifosmcp.runtime.tools import _CANONICAL_HANDLERS
from arifosmcp.constitutional_map import CANONICAL_TOOLS
from arifosmcp.runtime.public_surface import public_tool_names_for_mode
print(f'Handlers: {len(_CANONICAL_HANDLERS)}, Canonical: {len(CANONICAL_TOOLS)}, Public: {len(public_tool_names_for_mode(\"canonical14\"))}')
"

# Run tests
python3 -m pytest tests/test_canonical.py tests/test_surface_lock.py -v

# If pre-commit fails on E501 long lines in public_registry.py:
# These are pre-existing formatting debt in CONSTITUTIONAL_TOOL_DESCRIPTIONS, NOT caused by your changes
# Fix by trimming the specific long strings (lines 49, 51, 66, 74, 81, 87, 106)
```

## Key Insight: canonical13 vs canonical14
The surface mode was named `canonical13` when arifOS had 13 tools. When a 14th tool was added (`mcp_health_check`), the surface was renamed `canonical14` with `canonical13` kept as a backward-compat alias. This was NOT an automatic rename — it required manual updates across 4 source files and ~10 test files.

## Canonical Registry (as of 2026-05-01)
```
arif_session_init       arif_sense_observe    arif_evidence_fetch
arif_mind_reason       arif_kernel_route     arif_reply_compose
arif_memory_recall     arif_heart_critique   arif_gateway_connect
arif_judge_deliberate  arif_vault_seal       arif_forge_execute
arif_ops_measure       mcp_health_check
```

## Known Pre-Existing Issues
- `public_registry.py` E501 long-line violations in CONSTITUTIONAL_TOOL_DESCRIPTIONS (pre-existing)
- `public_surface.py` E402 import-order warning for `get_build_info` (pre-existing)
- These should NOT be fixed as part of a tool expansion task
