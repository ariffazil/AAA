---
name: arifos-drift-detection-false-positives
category: governance
description: "arifOS ΔΩΨ audit can produce false positives when comparing live runtime state against stale manifests or spec artifacts. Always verify live tool registration before flagging namespace/function naming drifts."
---

# arifOS Drift Detection — False Positive Patterns

## The Problem
arifOS ΔΩΨ audit compares live runtime state against specification artifacts (Space manifests, tool_registry.json, Makefile targets). When the spec artifact was updated but never deployed, or when a naming convention exists only in documentation but was never enforced in runtime, the audit flags a "drift" that is actually a phantom.

**Example — D1 NAMESPACE-SPLIT (false positive):**
- Audit compared Space manifest (v2026.05.02.3) against live arifOS runtime
- Space manifest used `arif_<noun>_<verb>` prefix
- Tool registry used `arifos_<noun>_<verb>` prefix
- Audit concluded: "NAMESPACE SPLIT — HIGH severity"
- **Reality:** `arifos_` prefix existed only in `tool_registry.json` spec artifact, never deployed to live runtime. All 13 live tools already used `arif_` prefix. No split existed in the actual running system.

**Rule** — Before flagging any naming, topology, or tool-count drift, verify the spec artifact is actually what is deployed.

## Verification Protocol

### Before flagging tool naming drifts
```bash
# Check what is actually registered in the live FastMCP server
curl -s http://localhost:8080/mcp -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Also check via tool registry file (source of truth for spec)
cat /root/arifOS/arifosmcp/tool_registry.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
for t in d.get('tools', []):
    print(t['name'])
"
```

### Before flagging tool count drifts
- Compare tool_registry.json (spec) against live MCP server output
- If `/mcp` JSON-RPC returns empty tools list, check via `GET /tools` (FastMCP native endpoint) before concluding tools are absent
- Transport issues (HTTP 406, 400, empty results) can look like missing tools

### Before flagging floor/state drifts
- `floors_active` may appear as `null` in Space dashboard metadata even when floor enforcement is wired and functioning
- Dashboard metadata is not the same as live kernel state
- Check `floors.py` source and runtime execution, not just manifest defaults

## Real vs Phantom Drifts (arifOS as of 2026-05-07)

| Drift | Status | Notes |
|-------|--------|-------|
| D1 NAMESPACE-SPLIT | Phantom | `arifos_` prefix spec artifact never deployed |
| D9 COMPUTE-TOOLS-ABSENT | **Real** | `arifos_compute_*` stubs exist in canonical tools file but not in live FastMCP registration |
| D3 FLOORS-ACTIVE-NULL | Ambiguous | `check_floors()` wired and functional; null may be dashboard config default |
| D4 PLANNING-ORGAN-ABSENT | **Real** | `arifos_compute_*` planning tools not registered |
| D6 SOVEREIGN-INTERFACE-ABSENT | **Real** | No `/status` endpoint found in codebase |
| D5 EPOCH-SEALING-INCOMPLETE | **Real** | `arif_vault_seal` exists but no epoch state machine exposed at tool level |

## Lesson
ΔΩΨ audit severity is directional — it correctly identifies areas needing attention but can overstate the current brokenness when comparing against stale specs. Always ground-truth before reporting.
