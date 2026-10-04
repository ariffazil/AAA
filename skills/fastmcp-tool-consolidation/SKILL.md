---
name: fastmcp-tool-consolidation
description: Consolidate multiple FastMCP tools into merged mode-dispatch tools with backwards-compat shims. Pattern for reducing MCP tool surface by absorbing related tools under a single unified tool with a `mode` parameter. Covers the multi-line decorator commenting pitfall, verification approach, and interaction with unified server tool registration.
tags: [mcp, fastmcp, consolidation, tool-surface, arifos]
---

# FastMCP Tool Consolidation

Consolidate multiple MCP tools into merged mode-dispatch tools. Reduces tool surface count, improves discoverability, and maintains backwards compatibility via shims.

## When to Use

- User asks to consolidate/merge/reduce MCP tool count
- Multiple related tools should share a single entry point with mode dispatch
- Tool surface is bloated and needs streamlining
- Any organ (GEOX, WEALTH, etc.) has 10+ small tools that could be grouped

## The Pattern

### 1. Identify Merge Groups

Group related tools by domain. Each group produces ONE new merged tool:
- **Absorber tools** (already have `mode` param): just add shims, don't create new tool
- **New merged tools**: create with mode dispatch, comment out old registrations

### 2. Comment Out Old Registrations

For each absorbed tool, find and comment out the `@mcp.tool(...)` decorator:

```python
# Before:
@mcp.tool(name="geox_temporal_decline", annotations=_geox_annotations("geox_temporal_decline"))
async def _temporal_decline(...): ...

# After:
# ZEN-CONSOLIDATED — @mcp.tool(name="geox_temporal_decline", annotations=_geox_annotations("geox_temporal_decline"))
async def _temporal_decline(...): ...
```

**CRITICAL: Do NOT remove the function body.** The old implementations stay as plain async functions — they just don't get `@mcp.tool` anymore. New merged tools call them directly.

### 3. Create Merged Tools

Insert before the evidence chain section (or equivalent end-of-registration marker):

```python
@mcp.tool(
    name="geox_temporal",
    description="Temporal analytics. Modes: decline, rrr, basin_lifecycle, cadence.",
    annotations=_geox_annotations("geox_temporal"),
)
async def _temporal_unified(
    mode: str = "decline",
    # Union of all absorbed tools' parameters (all optional/None)
    production_data: list[dict[str, Any]] | None = None,
    forecast_years: int = 5,
    reserves_start: float | None = None,
    ...
    session_id: str | None = None,
    actor_id: str | None = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    if mode == "decline":
        return await _temporal_decline(production_data=production_data, ...)
    elif mode == "rrr":
        return await _temporal_rrr(reserves_start=reserves_start, ...)
    else:
        return {"error": f"Unknown mode: {mode}. Valid: decline, rrr, ..."}
```

Key: new merged tools call old functions by name (they're still in scope).

### 4. Add Backwards-Compat Shims

Thin wrappers that register the old tool names:

```python
@mcp.tool(name="geox_temporal_decline", annotations=_geox_annotations("geox_temporal_decline"))
async def _shim_temporal_decline(production_data, forecast_years=5, ...):
    """[SHIM→geox_temporal(mode=decline)]"""
    return await _temporal_unified(mode="decline", production_data=production_data, ...)
```

Shims preserve backwards compatibility for MCP clients using old tool names.

### 5. Verify

```bash
cd /root/ORGAN && PYTHONPATH=src python3 -c "
from organ_mcp.tools_wiring import register_tools_on
from fastmcp import FastMCP
mcp = FastMCP('t')
register_tools_on(mcp)
print(f'OK: {len(mcp._local_provider._components)} tools')
"
```

## Pitfalls

### CANONICAL_PUBLIC_TOOLS filter (the silent kill)

**THE most common failure mode.** After consolidation, new merged tools are registered in FastMCP but don't appear on the wire. Root cause: `tools_manifest.yaml` still lists old tool names with `visibility: public`.

The wire surface is derived from:
```
tools_manifest.yaml → public_tool_names() → SURFACE_TOOLS → CANONICAL_PUBLIC_TOOLS
```

Only tools in `CANONICAL_PUBLIC_TOOLS` appear in `tools/list`. If you create `geox_temporal` but the manifest still has `geox_temporal_decline` with `visibility: public`, only the old name appears.

**Fix:** After creating merged tools, update `tools_manifest.yaml`:
1. Remove old absorbed tool entries (or change visibility to internal)
2. Add new merged tool entries with `visibility: public`
3. Update `public_count_target` to match new count
4. Restart the organ service

### FastMCP **kwargs rejection (FastMCP ≥ 3.4)

FastMCP 3.4.4 rejects `**kwargs` in tool functions:
```
Functions with **kwargs are not supported as tools
```

**Wrong:**
```python
@mcp.tool(name="geox_temporal")
async def _temporal(**kw):
    return await _impl(**kw)
```

**Right:**
```python
@mcp.tool(name="geox_temporal")
async def _temporal(
    mode: str = "decline",
    production_data: list[dict] | None = None,
    forecast_years: int = 5,
    ...
) -> dict[str, Any]:
    if mode == "decline":
        return await _decline(production_data, forecast_years)
```

Every parameter must be explicitly declared. No `**kwargs`, no `**args`.

### Multi-line `@mcp.tool(` decorator commenting

**THE bug.** When commenting out multi-line decorators:

```python
@mcp.tool(
    name="geox_geological_model_generate",
    annotations=_geox_annotations("geox_geological_model_generate"),
)
```

**WRONG** — searching for `")" in line` stops at the annotations line because `_geox_annotations(...)` contains `)`:

```python
end = i
while end < len(lines) and ")" not in lines[end]:  # BUG: matches ) inside annotations
    end += 1
```

**RIGHT** — search for lines where stripped content STARTS with `)`:

```python
end = i
while end < len(lines) - 1:
    end += 1
    stripped_end = lines[end].lstrip()
    if stripped_end.startswith(")") or stripped_end.startswith("),"):
        break
```

### Unified server tool count

The unified server (server.py/unified.py) independently registers tools. tools_wiring.py changes only affect tools_wiring.py's registrations. The verification command counts ALL FastMCP tools, including unified server's.

- If unified server also registers `geox_temporal_decline`, commenting it out in tools_wiring.py won't remove it from the count
- Shims may overlap with unified server's tools — FastMCP deduplicates by name (last wins, with warning)
- The "42→20" target may not be achievable by tools_wiring.py alone

### Inside try/except blocks

Tools inside try/except blocks (common for LEM, temporal, core tools) — when you comment out the `@mcp.tool` decorator, the function is still defined inside the try block. The new merged tool can call it by name. If the import fails, the function isn't defined, so the merged tool should handle that gracefully.

### Deployment path for React GUI

**CORRECTED 2026-08-10 (was WRONG in earlier revision):** when the MCP server also serves a React SPA (like GEOX), the Caddy config is the ONLY truth for where the SPA is served. For GEOX the Caddyfile says:

```caddy
handle /gui/* {
    uri strip_prefix /gui
    root * /var/www/html/geox/gui     # ← THIS path, not /var/www/html/arif/geox/
    try_files {path} /index.html
    file_server
}
```

**Deploying to the wrong path (e.g. `/var/www/html/arif/geox/`) produces a GHOST bundle:** the HTML file exists but references asset hashes that either don't exist or are stale. Symptom: `curl <url> | grep -o 'index-[A-Za-z0-9]*\.js'` shows a DIFFERENT hash than the built `static/gui/assets/` — the browser loads the OLD bundle with zero errors, and your new components silently never run.

```bash
# 1. Build React SPA
cd geox-gui && npm run build  # outputs to ../static/gui/

# 2. Deploy to the Caddy-served path (verify with grep against Caddyfile)
cp static/gui/index.html /var/www/html/geox/gui/index.html
cp static/gui/assets/* /var/www/html/geox/gui/assets/

# 3. Deploy to runtime (for MCP resource serving)
cp static/gui/index.html /opt/geox/app/static/gui/index.html
cp static/gui/assets/* /opt/geox/app/static/gui/assets/

# 4. ZERO-TRUST verify: served HTML must reference the NEW hash
curl -s https://geox.arif-fazil.com/gui/ | grep -o 'index-[A-Za-z0-9]*\.js'
# Must match the built hash. Browser cache-bust with ?nocache=$(date +%s) during QA.
```

### Zen-orthogonal target (Arif doctrine — "survival of the fittest")

Consolidation is NOT mechanical counting — the target count is the number of **domain verbs** that are genuinely orthogonal. Arif's rule (2026-08-09, ratified for GEOX):

- Group by domain, then ask: is each surviving tool a **verb** with a clear scope, or a **function call**?
- Tools that are modes of one verb (decline/rrr/lifecycle/cadence → `geox_temporal`) must merge.
- Tools that are separate domains (petrophysics vs geomechanics vs prospect) stay separate.
- The honest target may be LESS than the round number you estimated. GEOX 42 tools → 18, not 20 — 18 was the actual orthogonal count (13 merge groups absorbing 31, 5 standalone).
- "No new tools allowed until we migrate to N" (Arif) = freeze the surface, do the merge, THEN allow additions. Never add on top of a bloated surface.

**Verification against a sibling claim of "0 tools on wire":** a sibling agent may report the wire is EMPTY after consolidation. Before trusting it, run the session handshake yourself (see forge-mcp-testing): bare `tools/list` without `Mcp-Session-Id` on a session-required organ returns `-32600 Bad Request: Missing session ID` — a naive counter reads that as 0 tools. Initialize first, THEN count. The "0 tools" claim was REFUTED by live probe in the 2026-08-09 session (18 tools confirmed on both :8081 and the public door).

## Script Template

See `references/consolidation-script.py` for a complete working script that was used for GEOX's 50→58 consolidation (30 absorbed, 9 new merged, 29 shims).
