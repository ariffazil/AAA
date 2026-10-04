# 2026-08-08 Resource Surface Reduction — 48 → 30

Full record of the reduction pass. Reuse the mapping + leak-check when the
surface changes again.

## Removed (18 URIs) → module map

| URI | Module / mechanism |
|---|---|
| `arifos://resources/index` | alias inside `namespace_index.py` `register_namespace_index` (shared handler with `arifos://index`; edit return list) |
| `arifos://resources/audit` | `resources_index.py` `register_resources_index` (already commented in `register_resources`) |
| `arifos://atlas-repo`, `aaa-index`, `a-forge-index`, `vault999-index` | own modules, pure import+call removal |
| `arifos://mcp/surface-map` | `surface_map.py` |
| `arifos://mcp-alignment` | `mcp_alignment.py` |
| `arifos://seal-readiness` | `seal_readiness.py` (concept merged into doctrine) |
| `arifos://atlas333/seal/head` | `atlas333.py` (alias → `arifos://vault/head`) |
| `atlas333/{zones,organs,thresholds,activation/rules,quote/list}` | `atlas333.py` (merged into `paradox/list`) |
| `wisdom/quotes/{disputed,arifos-doctrine,prohibited-uses}` | `wisdom_resources.py` (merged into `quotes/all`) |

## Keep list — 30 URIs by chamber

- IDENTITY (2): identity, human/metabolized
- LAW (5): doctrine, floors, refusal-surface, jurisdiction, civilization
- STATE (5): vitals, carry-forward, flow-state, reality/state, vault/head
- MIND (7): epistemic, loop-engineering, schema, bootstrap, quickstart, init/agent_init, memory
- DEEP (6): atlas333/{index,paradox/list,geometry,flow}, wisdom/{contract,quotes/all}
- DOORS (2): tree777://index, skill://index
- Structural anchors (3): arifos://index, arifos://trinity, arifos://affordances

Note: `carry-forward`, `flow-state`, `init/agent_init`, `skill://index` have NO
handler modules — they exist only as `namespace_index.py` migration-map data.
They stayed in `CANONICAL_RESOURCES` per the keep-list; the enforcement test
excludes them from `CANONICAL_RESOURCE_FILES` so the source-file-exists test
passes.

## Enforcement test sync (`tests/test_canonical_resources_enforcement.py`)

The test locks the surface in 5 places — ALL must be edited together:

1. `EXPECTED_CANONICAL_RESOURCES` frozenset (was 14, now 30; split into
   `_TEXT_RESOURCE_KEYS` + `_NON_TEXT_RESOURCE_KEYS` for clarity)
2. count test (`test_canonical_resources_count_is_13` → `_is_30`, assert 30)
3. `CANONICAL_RESOURCE_FILES` map — add new URIs' source files, drop removed
   ones, omit handler-less URIs
4. `TEXT_BASED_RESOURCE_VARS` — drop removed text resources (`SEAL_TEXT` for
   seal-readiness)
5. allowed-schemes tuple in `test_resource_uri_is_valid` — add `"skill"` for
   `skill://index`
6. `SUPPLEMENTAL_RESOURCES` test — was "must be exactly 2 (mcp-alignment +
   resources/index)", now "must be empty"

First failure run after the sync produced exactly 3 failures:
- `test_canonical_resources_count_is_30` (26 ≠ 30 — the 4 aspirational URIs)
- `test_canonical_resources_match_resource_init` (missing the same 4)
- `test_resource_uri_is_valid[skill://index]` (unknown scheme)

Pattern: run the enforcement test FIRST when the surface changes; it enumerates
every desync precisely.

## Leak-check script (python, run after edit)

```python
from fastmcp import FastMCP
from arifosmcp.resources import register_resources, _RESOURCE_PROVENANCE, CANONICAL_RESOURCES
reg = set(register_resources(FastMCP("t")))
removed = {  # the 18 URIs
    "arifos://resources/index", "arifos://resources/audit", "arifos://atlas-repo",
    "arifos://aaa-index", "arifos://a-forge-index", "arifos://vault999-index",
    "arifos://mcp-alignment", "arifos://mcp/surface-map", "arifos://seal-readiness",
    "arifos://atlas333/seal/head", "arifos://atlas333/zones", "arifos://atlas333/organs",
    "arifos://atlas333/thresholds", "arifos://atlas333/activation/rules",
    "arifos://atlas333/quote/list", "arifos://wisdom/quotes/disputed",
    "arifos://wisdom/quotes/prohibited-uses", "arifos://wisdom/quotes/arifos-doctrine",
}
assert not (reg & removed)
assert not (set(_RESOURCE_PROVENANCE) & removed)
assert len(CANONICAL_RESOURCES) == 30
```

Result observed: 47 total registrations (30 canonical + 16 templates + 1
undeclared `arifos://floor/{fid}` from floor_table.py — expected, keep-list
didn't enumerate it).
