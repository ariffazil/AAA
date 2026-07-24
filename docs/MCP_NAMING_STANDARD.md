# MCP Tool Naming Convention — Federation Standard

> **SOT:** 2026-07-24 | **seal_seq:** fed-phase-4
> **Authority:** F13 SOVEREIGN — arifOS Federation

## Rule

Every MCP tool in the arifOS Federation MUST use the organ-specific prefix. No exceptions.

| Organ | Prefix | Example | Count |
|-------|--------|---------|-------|
| arifOS | `arif_` | `arif_init`, `arif_judge`, `arif_seal` | 8 |
| A-FORGE | `forge_` | `forge_execute`, `forge_shell`, `forge_git` | dynamic |
| GEOX | `geox_` | `geox_basin`, `geox_petrophysics`, `geox_claim` | 32 |
| WEALTH | `capital_` | `capital_primitive`, `capital_market`, `capital_wisdom` | 12 |
| WELL | `well_` | `well_assess_homeostasis`, `well_validate_vitality` | 8 |

## Cross-Organ Routing

Tools from one organ MUST NOT be directly called by another organ without going through `arif_route`:

```
Agent → arif_route(intent="analyze basin X") → GEOX geox_basin()
Agent → arif_route(intent="calculate NPV")   → WEALTH capital_primitive(mode="npv")
Agent → arif_route(intent="check readiness") → WELL well_validate_vitality()
```

## Enforcement

- New tools MUST follow the prefix convention at registration time
- `tools/list` on each organ MUST only return tools with its prefix
- Cross-prefix tools = constitutional violation (F11 AUDIT)

## Verification

```bash
# Check each organ's tools/list for prefix violations
curl -s localhost:8088/health | jq '.canonical_tools_loaded'  # all arif_*
curl -s localhost:8081/health | jq '.tools_loaded'             # all geox_*
curl -s localhost:18082/health | jq '.tools_loaded'            # all capital_*
curl -s localhost:18083/health | jq '.tool_count'              # all well_*
```
