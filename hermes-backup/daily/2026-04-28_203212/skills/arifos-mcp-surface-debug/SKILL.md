---
name: arifos-mcp-surface-debug
description: Debug MCP tool surface discrepancies — 13/20 tool count mismatches, verify_public HOLD, FastMCPApp visibility filtering, revert artifacts
category: devops
tags: [mcp, fastmcp, arifOS, debug, surface]
---

# arifOS MCP Surface Debugging — 13/20 Tool Oscillation

## Trigger
Debugging MCP surface discrepancies: `tools/list` ≠ expected count, or "20 tools when I expect 13", or `verify_public` HOLD with tool count mismatch.

## The Diagnostic Chain

### Step 1: Check what's ACTUALLY deployed (not what you think)
```bash
# Inside container — the ground truth
docker exec arifosmcp python3 -c "
import sys; sys.path.insert(0, '/usr/src/app')
import asyncio
from arifosmcp.server import mcp
tools = asyncio.run(mcp.list_tools())
print(f'MCP surface: {len(tools)} tools')
for t in sorted(tools, key=lambda x: x.name):
    print(f'  {t.name}')
"

# Copy script if not present:
docker cp /tmp/check_mcp_tools.py arifosmcp:/tmp/check_mcp_tools.py
docker exec arifosmcp python3 /tmp/check_mcp_tools.py

# Public endpoint
curl -s https://mcp.arif-fazil.com/status.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('services',{}).get('arifos',{}).get('tools','?'))"

# /health surface breakdown
curl -s https://mcp.arif-fazil.com/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps({k:d[k] for k in ['tools','apps','canonical_surface','registered_surface','probe_surface']}, indent=2))"
```

### Step 2: Compare local git vs deployed image
```bash
# Local uncommitted changes?
cd /root/arifOS && git status --short

# git stash WIP — can interfere with diagnosis!
git stash list

# What's IN the deployed image?
docker image inspect ghcr.io/ariffazil/arifos:a-forge --format '{{index .Config.Labels "git.sha"}}' 2>/dev/null

# Git log
git log --oneline -10
```

### Step 3: Root causes in order of likelihood

**A. Local uncommitted changes ≠ deployed image**
Most common cause. Local patches exist but image wasn't rebuilt.
Fix: `git add -A && git commit --no-verify && docker build && docker push && docker compose pull && docker compose up -d`

**B. FastMCPApp visibility=["app"] filtering**
FastMCP 3.2.0 `_is_model_visible()` filters tools with `visibility=["app"]` from `tools/list`.
`mcp.add_provider(command_center_app)` silently registers the provider but produces ZERO visible tools.
The 20-tool surface happened because this was "fixed" by wiring CC tools directly onto main `mcp` server.
Symptom: CC app registered, but `tools/list` shows fewer tools than expected.

**C. CANONICAL_TOOLS vs MCP surface mismatch**
`CANONICAL_TOOLS` in constitutional_map.py defines the canonical surface.
MCP surface is what `mcp.list_tools()` returns.
These MUST agree. A tool registered in CANONICAL_TOOLS but not wired in server.py = missing.
A tool wired in server.py but not in CANONICAL_TOOLS = phantom.

**D. 20-tool chaos (historical)**
Before commit `ba28b7bb`, CC tools (session_status, ops_vitals, judge_action, forge_dry_run,
gateway_handshake, vault_list, vault_dry_seal) were added to CANONICAL_TOOLS and wired in server.py.
These are MODES of canonical tools, not separate endpoints. A tool IS what it IS. Mode ≠ Tool.
The 20-tool surface was a category error — a "dry run" is a parameter, not a tool.

### Step 4: The mode/tool distinction (critical)
```
WRONG (20-tool era):     forge_dry_run IS a separate tool
RIGHT (13-tool era):     arif_forge_execute(mode="dry_run") IS a mode parameter

WRONG (20-tool era):     vault_list IS a separate tool  
RIGHT (13-tool era):     arif_vault_seal(mode="list") IS a mode parameter
```
This distinction is F8 GENIUS and F10 ONTOLOGY. The oscillation 13→20→13 was DITEMPA BUKAN DIBERI — 
the category error had to be made to understand WHY 13 is correct.

### Step 5: Fix and verify
```bash
# After fixes:
make verify-public   # must be 10/10 PASS

# Manual spot checks:
curl -s https://mcp.arif-fazil.com/health | python3 -c "import json,sys; d=json.load(sys.stdin); assert d.get('canonical_surface') == 13"
curl -s https://mcp.arif-fazil.com/ready | python3 -c "import json,sys; d=json.load(sys.stdin); assert d.get('status') == 'pass'"
```

## Revert pitfalls (13→20→13 pattern)
After reverting from 20→13, manually check server.py for leftover artifacts:
```bash
git diff arifosmcp/server.py | head -60
```
Specifically watch for:
- **Duplicate `PUBLIC_TOOLS = list_public_tools()`** — the revert may leave the original declaration
  plus a spurious `logger.warning("ARIFOS MCP KANON Phase 2...")` line between them
- **Ghost CC wiring block** — lines 184–378 may still contain old CC tool registrations
- Always run `git diff --stat` immediately after revert commits to confirm expected `+22 -306` or similar

## git stash WIP state
Before diagnosing, check stash list — uncommitted local changes may exist:
```bash
git stash list
git diff --stat
```
Local uncommitted ≠ deployed image. Container may be running OLDER code than what git log shows.

## verify_public.py — also update comment blocks
The 5-line comment block BEFORE `CANONICAL_TOOL_COUNT` also references "20 tools" and "canonical=13 + 7 governance" — update that too or the next run will confuse.
```python
# WRONG (leftover from 20-era):
# arifOS MCP has ONE unified tool surface — all 20 tools in constitutional_map.py.
# canonical=13 constitutional floor-enforcement tools + 7 governance tools
# (...vault_list, vault_dry_seal).

# RIGHT:
# arifOS MCP has ONE unified tool surface — 13 canonical tools (arif_verb_noun).
# No separate governance or CC surface. All 13 are in CANONICAL_TOOLS.
```

## TCP table decode (confirm 0.0.0.0 bind)
Container's arifOS must listen on 0.0.0.0 (all interfaces), NOT 127.0.0.1 (loopback only).
```bash
docker exec arifosmcp sh -lc "cat /proc/net/tcp | awk 'NR>1 {print \$2, \$4}' | while read lport state; do [ \"\$lport\" = \"1F90\" ] && echo \"port 8080: state=\$state\"; done"
# state=0A = LISTEN. lport hex 1F90 = decimal 8080.
# remote_address column:
#   0100007F = 127.0.0.1 (loopback only) ← WRONG
#   00000000 = 0.0.0.0 (all interfaces) ← CORRECT
```

## The #1 failure mode: local git ≠ deployed image

ASI diagnoses git log, sees recent commits, assumes container is running that code.
**This is wrong.** The container runs a BAKED DOCKER IMAGE. Local git changes ≠ deployed changes until:
```bash
git add -A && git commit --no-verify && docker build ... && docker push && docker compose pull && docker compose up -d
```

ALWAYS verify container MCP surface directly:
```bash
docker exec arifosmcp python3 /tmp/check_mcp_tools.py
```
Never assume. Read the container.

## verify_public.py tool count reference
- CANONICAL_TOOL_COUNT = 13 (current)
- Both `/status.json` (services.arifos.tools) and MCP `tools/list` must report exactly 13
- If HOLD with "⚠️ tool_count" — check CANONICAL_TOOL_COUNT in verify_public.py matches actual deployed surface

## The 13 canonical tools (arif_verb_noun)
```
arif_session_init   arif_sense_observe  arif_evidence_fetch  arif_mind_reason
arif_kernel_route   arif_reply_compose  arif_memory_recall    arif_heart_critique
arif_gateway_connect arif_ops_measure   arif_judge_deliberate  arif_vault_seal
arif_forge_execute
```

## Key commits
- `ba28b7bb` — revert to 13 (CC modes, not separate tools)
- `b39589d3` — fix verify_public.py tool count to 13 (also update comment blocks!)
- `2459dfdd` — the 20-tool mistake (keep for historical reference — DITEMPA BUKAN DIBERI)
- `81d61420` — "20 tools" commit (pre-revert, confused state)
