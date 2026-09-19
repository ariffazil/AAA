# FastMCP 4.x Compatibility Caveats

> Captured 2026-09-19 from the federation-wide upgrade to fastmcp 4.0.5.
> This file exists because FORGE-fastmcp is bundled (read-only).

## Tasks Extension Removed

FastMCP 4.x removed the `io.modelcontextprotocol/tasks` extension entirely.
`pip install 'fastmcp[tasks]'` is a no-op in 4.x — it installs nothing extra.

**Impact:** Any organ with task-enabled tools (tools using `@mcp.tool()` that rely on
`ctx.report_progress()`, `ctx.read_resource()`, or the tasks lifecycle) will crash on
startup with:

```
RuntimeError: Task-enabled tools (...) require the tasks extension,
but no extension with identifier 'io.modelcontextprotocol/tasks' is registered.
```

**Affected organs (2026-09-19):**
- **GEOX** — 86 tools, several task-enabled (geox_claim, geox_falsify, etc.)
- **WELL** — 3 task-enabled tools (well_999_vault, well_assess_sovereign_entropy, well_seal_vault)

**Resolution:** Pin to `fastmcp==3.4.7` (latest 3.x). Do NOT upgrade these organs
to 4.x until the task-enabled tools are migrated.

**Migration path (not yet implemented):** FastMCP 4.x may reintroduce tasks via
`mcp.add_extension(TasksExtension(...))` in a future release. Monitor PyPI changelog.

## Middleware API Unchanged

FastMCP 4.x retains:
- `fastmcp.server.middleware.middleware.Middleware` — base class
- `CallNext`, `MiddlewareContext`, `ToolResult` — all importable
- `mcp.add_middleware(instance)` — registration unchanged

No code changes needed for middleware in 4.x.

## Version Detection

A flag like `IS_FASTMCP_3 = VERSION_MAJOR >= 3` will be True for 4.x (4 >= 3).
If your code has a runtime fallback that overrides this flag on ImportError, verify
that the imports actually fail — in 4.0.5 they succeed, so the fallback never triggers.

## Organs on 4.0.5 (no issues)

- arifOS (production venv: `/opt/arifos/current/venv`)
- arifflow (`/opt/arifflow/venv`)
- WEALTH (`/root/WEALTH/.venv` — recreated from scratch)

## Organs pinned to 3.4.7

- GEOX (`/opt/geox/.venv`)
- WELL (`/root/WELL/.venv`)
