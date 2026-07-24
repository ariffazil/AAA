---
name: FORGE-fastmcp
description: Build, test, inspect, install, and deploy MCP servers with FastMCP in Python
version: 1.2.0
author: arifOS (based on Hermes official/mcp/fastmcp)
tags: MCP, FastMCP, Python, Tools, Deployment
agents: claude | opencode | kimi | codex
---

# FastMCP — Build & Deploy MCP Servers in Python

> **Current stable:** `fastmcp[tasks]==3.4.2` (PyPI latest as of 2026-06-12).
> **arifOS federation target:** all Python MCP organs run FastMCP 3.4.2.
> arifOS convention: `streamable_http` transport, Pydantic v2 output schemas, `fastmcp[tasks]` extra.

---

## When to Use

- Create a new MCP server in Python.
- Wrap an API, database, or CLI as MCP tools.
- Add tools, resources, prompts, or tasks to an existing MCP server.
- Deploy an MCP server as an HTTP endpoint behind Caddy/Cloudflare.
- Test an MCP server locally before wiring it into Codex, Claude Code, Cursor, or another client.

---

## Quick Start

### 1. Install

```bash
# Runtime / production (use uv in federation repos)
uv add "fastmcp[tasks]==3.4.2"

# System CLI (af-forge)
pip install --break-system-packages "fastmcp[tasks]==3.4.2"
fastmcp --version   # should print 3.4.2
```

### 2. Scaffold

```bash
fastmcp scaffold \
  --template api_wrapper \
  --name "My API" \
  --output ./my_server.py
```

Templates: `api_wrapper`, `database_server`, `file_processor`.

### 3. Implement Tools

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def search_products(query: str, limit: int = 10) -> list[dict]:
    """Search product catalog."""
    ...
```

### 4. Test Locally

```bash
fastmcp inspect my_server.py:mcp
fastmcp list my_server.py:mcp --json
fastmcp call my_server.py:mcp search_products query=oil --json
```

### 5. Deploy

```bash
# Local HTTP test
fastmcp run my_server.py:mcp --transport streamable_http --host 127.0.0.1 --port 8000

# Production: bind to 127.0.0.1 and expose via Caddy/Cloudflare Tunnel
python my_server.py  # if the script calls mcp.run(...)
```

### 6. Wire into a Client

```bash
# Codex / Claude Code / Cursor / Gemini CLI — use the public HTTPS endpoint
codex mcp add my-server \
  --type http \
  --url https://my-server.arif-fazil.com/mcp \
  --description "Product search API"
```

---

## arifOS Federation Tool Naming

| Pattern | Example |
|---------|---------|
| `{service}_{action}_{resource}` | `geox_well_analyze_log` |
| `{service}_{noun_verb}` | `wealth_npv_calculate` |
| Read-only tools | `get_`, `list_`, `search_`, `fetch_` |

---

## Output Schema Convention (arifOS)

All tools return Pydantic v2 `BaseModel` instances or plain dicts:

```python
from pydantic import BaseModel

class CustomerOutput(BaseModel):
    id: str
    name: str
    segment: str
    confidence: float

@mcp.tool()
def get_customer(customer_id: str) -> CustomerOutput:
    """Fetch customer by ID with confidence score."""
    ...
```

---

## HTTP Transport (arifOS Standard)

All federation Python MCP servers use the **Streamable HTTP** transport:

```python
mcp.run(transport="streamable_http", host="127.0.0.1", port=8000)
```

- Bind to `127.0.0.1` internally.
- Let Caddy 2 terminate TLS; use Cloudflare Tunnel for public MCP subdomains.
- Do **not** expose the raw backend port publicly.

---

## Background Tasks (`fastmcp[tasks]`)

Use the `tasks` extra for long-running operations with progress reporting:

```python
from fastmcp import Context

@mcp.tool()
async def ingest_large_file(path: str, ctx: Context) -> dict:
    """Ingest a large file with progress updates."""
    await ctx.report_progress(0, 100)
    ...
    await ctx.report_progress(100, 100)
    return {"status": "done"}
```

---

## FastMCP Apps (3.4+)

FastMCP 3.4 introduces **Apps** — interactive UIs rendered in the conversation:

- `FastMCPApp` / `@mcp.app()` for managed UI wiring.
- Prefab providers: `approval`, `choice`, `file_upload`, `form`.
- Generative UI: let the LLM build custom Prefab UIs on the fly.

Use these for human-in-the-loop gates inside MCP clients that support them. Federation organs remain headless by default; Apps are optional UI sugar.

---

## MCP Apps Hardening (SEP-1865 + ChatGPT 2026)

> Authoritative contract: `/root/forge_work/2026-07-20/GEOX-CHATGPT-MCP-GUI-BLUEPRINT.md`
> (F13 sovereign directive, 2026-07-20). Applies to any federation server that exposes
> tools to ChatGPT / MCP Apps hosts. GEOX is the first consolidation target.

### 1. Explicit 4-annotation taxonomy on every public tool

Set **ALL FOUR** annotations explicitly on every public tool — wire format is camelCase.
**Annotation silence inherits risky defaults:** `readOnlyHint=false`,
`destructiveHint=true`, `idempotentHint=false`, `openWorldHint=true`. A tool that
forgets annotations looks dangerous-by-default to the host. Annotations are *hints*,
not enforcement — server-side auth is still required.

| Tool class | `readOnlyHint` | `destructiveHint` | `idempotentHint` | `openWorldHint` | GEOX example |
|---|---|---|---|---|---|
| Pure compute | `true` | `false` | `true` | `false` | `geox_petrophysics` |
| Ingest | `false` | `false` | `false` | `false` | `geox_well_ingest` |
| External fetch | `true` | `false` | `false` | `true` | deep-time / macrostrat fetchers |
| Destructive export | `false` | `true` | `false` | `false` | SEG-Y export (overwrite) |

Display-name precedence: `title` → `annotations.title` → `name`.

### 2. outputSchema families

Treat `outputSchema` as **mandatory for every tool returning `structuredContent`**:

- Declare per tool, grouped into named families (GEOX families: `GeoxStatusResult`,
  `GeoxArtifactResult`, `GeoxWellResult`, `GeoxSeismicResult`, `GeoxMapResult`,
  `GeoxProspectResult`, `GeoxClaimResult`, `GeoxEvidenceResult`).
- `additionalProperties: false`, required fields pinned.
- **Never** put secrets, trace IDs, or dense arrays in `structuredContent` — it is
  model-visible. Dense data goes into a `ui://` resource or artifact reference.

Reference shape (condensed from the blueprint):

```json
{
  "type": "object",
  "title": "GeoxWellResult",
  "additionalProperties": false,
  "required": ["status", "well_ref", "summary", "artifacts"],
  "properties": {
    "status": { "type": "string", "enum": ["ok", "partial", "failed"] },
    "well_ref": { "type": "string" },
    "summary": { "type": "string", "description": "≤3 sentence model-facing summary" },
    "artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["kind", "ref"],
        "properties": {
          "kind": { "type": "string", "enum": ["log_panel", "segy", "table"] },
          "ref": { "type": "string", "description": "ui:// or artifact URI" }
        }
      }
    }
  }
}
```

### 3. Tool `_meta` wiring for UI tools

Every UI-bound tool needs, on the tool definition:

- `_meta.ui.resourceUri` — **primary** binding, e.g. `ui://geox/workbench-v1.html`
  (version URIs; they are host cache keys).
- `_meta["openai/outputTemplate"]` — the ChatGPT alias, emitted **alongside** (not
  instead of) the primary key, with the same URI value.
- Optional `_meta["openai/toolInvocation/invoking"]` and
  `_meta["openai/toolInvocation/invoked"]` status strings.
- The served resource MIME MUST be `text/html;profile=mcp-app` (hosts only enable
  the app bridge for that profile).

In FastMCP, pass these via the `@mcp.tool(meta={...})` / annotations kwargs if your
pinned version supports arbitrary tool `meta`. **If FastMCP cannot emit arbitrary
`_meta` on tool definitions**, the sanctioned federation workaround is bridge-side
injection — see GEOX at `src/geox_mcp/tools/mcp_apps_bridge.py`, whose
`enrich_response()` injects `_meta.ui.resourceUri` into tool responses at the MCP
boundary (24 tools covered at recon time). Mirror that pattern rather than forking
FastMCP internals.

### 4. Per-tool `securitySchemes`

Declare per tool for ChatGPT: `noauth` for public read-only tools, `oauth2` + scopes
for anything else. GEOX scope map (blueprint): `geox.read`, `geox.compute`,
`geox.ingest`, `geox.export`, `geox.claim.write`, `geox.seal` — withhold `geox.seal`
from v1. OAuth 2.1 resource-server rules (RFC 9728 PRM, `WWW-Authenticate` on 401,
one canonical `resource` identity across endpoint/PRM/OAuth param/audience) belong
to the server auth layer, but the per-tool scheme declaration lives next to the tool
definition so the host can plan step-up auth.

### 5. Tool-originated errors

Tool failures return a CallToolResult with `isError: true` — **never** protocol-level
crashes. A structured error result lets the model read the failure and self-correct;
a transport crash kills the whole conversation turn. In FastMCP: catch domain
exceptions inside the tool body and raise/return an error result with a concise,
actionable message instead of letting the exception escape.

---

## CLI Cheat Sheet

```bash
fastmcp --version
fastmcp inspect server.py:mcp
fastmcp list server.py:mcp --json
fastmcp call server.py:mcp tool_name arg1=val1 --json
fastmcp run server.py:mcp --transport streamable_http --host 127.0.0.1 --port 8000
fastmcp generate-cli server.py:mcp -o ./mycli
```

---

## Quality Checklist

- [ ] `fastmcp inspect <server.py:mcp>` succeeds.
- [ ] `fastmcp list <server> --json` returns all expected tools.
- [ ] At least one `fastmcp call` succeeds against a representative tool.
- [ ] Tool names follow `{service}_{action}_{resource}` pattern.
- [ ] Output schemas are Pydantic v2 models or typed dicts.
- [ ] No hardcoded secrets (use env vars / SOPS).
- [ ] Health endpoint at `/health` when using HTTP transport.
- [ ] Bound to `127.0.0.1` in production.
- [ ] (ChatGPT/MCP Apps) All 4 annotations explicit on every public tool — no annotation silence.
- [ ] (ChatGPT/MCP Apps) `outputSchema` declared for every tool returning `structuredContent`, `additionalProperties: false`.
- [ ] (ChatGPT/MCP Apps) UI tools carry `_meta.ui.resourceUri` + `openai/outputTemplate` alias (bridge injection if FastMCP can't emit `_meta`).

---

## Troubleshooting

```bash
# Wrong / missing fastmcp
pip install --break-system-packages "fastmcp[tasks]==3.4.2"

# Import error
python3 -c "from fastmcp import FastMCP; import fastmcp; print(fastmcp.__version__)"

# Inspect fails
fastmcp inspect my_server.py:mcp --verbose

# HTTP transport not working — check transport spelling
fastmcp run my_server.py:mcp --transport streamable_http --host 127.0.0.1 --port 8000

# FastMCP 2 → 3 migration
# See https://gofastmcp.com/getting-started/upgrading/from-fastmcp-2.md
```

---

## Federation Version Alignment

| Repo | FastMCP Spec | Lock Status |
|------|--------------|-------------|
| arifOS | `==3.4.2` | 3.4.2 |
| geox | `>=3.4.2,<4.0` | 3.4.2 |
| WEALTH | `>=3.3.1,<4` | target 3.4.2 |
| WELL | `>=3.3.1,<4.0` | target 3.4.2 |

If a repo lock drifts below 3.4.2, run `uv lock --upgrade-package fastmcp` and re-run the test suite.
