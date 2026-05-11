---
name: arifos-mcp-tool-audit
category: devops
description: Audit tool stage/lane metadata against the arifOS constitutional contracts — prevents wrong pipeline stages (222/500) and incorrect lane assignments (PSI/OMEGA/DELTA).
---

# arifOS MCP Tool Stage/Lane Audit

## Trigger
Auditing or displaying tool metadata (stage, lane, pipeline) for the arifOS MCP server. Useful when building dashboards, auditing constitutional correctness, or debugging tool registry mismatches.

## Key Insight: Dual Naming Layer
External MCP tool names (e.g. `arif_judge_deliberate`) are NOT the same as internal contract keys (e.g. `arifos_judge`). The mapping lives in `rest_routes.py`'s `_get_tool_obj()` function.

**External to Internal mapping:**
```
arif_ping            → arifos_health
arif_selftest        → arifos_health
arif_session_init    → arifos_init
arif_sense_observe   → arifos_sense
arif_evidence_fetch  → arifos_fetch
arif_mind_reason     → arifos_mind
arif_kernel_route    → arifos_kernel
arif_reply_compose   → arifos_reply
arif_memory_recall   → arifos_memory
arif_heart_critique  → arifos_heart
arif_gateway_connect  → arifos_gateway
arif_ops_measure     → arifos_ops
arif_judge_deliberate → arifos_judge
arif_vault_seal      → arifos_vault
arif_forge_execute   → arifos_forge
```

## Canonical Pipeline Stages (10 total)
`000 INIT · 111 SENSE · 333 MIND · 444 ROUTER · 555 MEMORY · 666 HEART · 777 OPS · 888 JUDGE · 999 VAULT · 010 FORGE`

**Stages 222 and 500 do NOT exist in the constitution.** Any dashboard claiming these stages is wrong.

## Stage/Lane Map Per Tool (verified against live container runtime)
```
000: arif_session_init(PSI Ψ)
010: arif_forge_execute(DELTA Δ)
111: arif_ping(DELTA Δ), arif_selftest(DELTA Δ), arif_sense_observe(DELTA Δ)
222: arif_evidence_fetch — NO CONSTITUTIONAL STAGE (null)
333: arif_mind_reason(DELTA Δ)
444: arif_kernel_route(DELTA Δ), arif_reply_compose — NO CONSTITUTIONAL STAGE (null)
555: arif_memory_recall(DELTA Δ)
666: arif_heart_critique(OMEGA Ω)
777: arif_ops_measure(DELTA Δ)
888: arif_gateway_connect(OMEGA Ω), arif_judge_deliberate(PSI Ψ)
999: arif_vault_seal(PSI Ψ)
PROBE: arif_ping, arif_selftest (tools, not constitutional stages — probe only)
```

## How to Audit
Inside the running container:
```bash
docker exec arifosmcp python3 -c "
from arifosmcp.runtime.contracts import AAA_TOOL_STAGE_MAP, TRINITY_BY_TOOL
# Apply the external→internal mapping above, then look up:
print(AAA_TOOL_STAGE_MAP.get('arifos_judge'))   # → 888_JUDGE
print(TRINITY_BY_TOOL.get('arifos_judge'))       # → PSI Ψ
"
```

## Common Mistakes
1. Using external tool name directly as contract key → always returns `None`
2. Hardcoding pipeline stages 222/500 → these don't exist in constitution
3. Assuming `arif_memory_recall` is DELTA → it's PSI (555_MEMORY)
4. Assuming `arif_judge_deliberate` lane is OMEGA → it's PSI (888_JUDGE)

## Container Filesystem: Live vs Source
The running `arifosmcp` container has a **writable overlay layer** at `/usr/src/app/` where patches may have been applied directly (not via rebuild). The canonical source lives at `/opt/arifos/src/arifOS/`. Key paths inside container:
- `/usr/src/app/server.py` — HTTP entrypoint (imports from root `server.py`)
- `/usr/src/app/arifosmcp/runtime/rest_routes.py` — REST endpoints including `/api/constitution`, `/api/status`, `/health`
- `/usr/src/app/arifosmcp/runtime/contracts.py` — `AAA_TOOL_STAGE_MAP`, `TRINITY_BY_TOOL` (the canonical tool metadata)
- `/usr/src/app/arifosmcp/constitutional_map.py` — `CANONICAL_TOOLS`, `ToolStage`, `TrinityLane` enums

`/health` is served from `rest_routes.py` (line ~1800), NOT from `server.py`'s `horizon_health` (line ~456). The FastMCP `mcp.http_app()` is augmented by `register_rest_routes(app, ...)` which adds `/health`, `/api/status`, `/api/constitution`.

## Container Status Detection Bug
`_collect_container_status()` in `rest_routes.py` calls `docker ps` internally but the Docker socket is NOT mounted into the arifosmcp container. Result: always returns `[]`. All "critical containers DOWN" alerts in the dashboard are false positives. The containers are actually running fine — use `docker ps` on the host to check.