---
id: mcp-gui-landscape-2026-09-22
name: MCP GUI landscape
version: 1.0.0
description: "MCP GUI deep-research 2026-09-22 — three-category taxonomy (MCP Apps/MCP-UI vs Manager GUI vs STMCP), spec mechanics, host matrix, portability test recipe, GEOX worked example"
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F1, F2, F4]
tags: [mcp, gui, mcp-apps, mcp-ui, sep-1865, portability, hosts, ui-inspector]
---
# MCP GUI Landscape — deep research 2026-09-22

> Compiled by FI-003 for `mcp-ops` Stage 3b/6a. Sources fetched 2026-09-22:
> mcpui.dev, modelcontextprotocol.io (`/extensions/apps/overview`, `/specification`),
> github.com/idosal/ui-inspector. Labels: OBS/EXT/UNVER.

## 1. Four categories — only one is the user-facing standard

| Category | What it is | Audience | Verdict for federation |
|---|---|---|---|
| **MCP Apps (SEP-1865) / MCP-UI** | Tool returns a `ui://` HTML panel the host renders in-chat | End user | **THE standard.** MCP-UI is the community SDK that implemented it first, now standardized; canonical repo `MCP-UI-Org/mcp-ui` (EXT 2026-09-22: 5.2k★, Apache-2.0, `@mcp-ui/client`/`@mcp-ui/server`, implements `text/html;profile=mcp-app`). Federation organs (GEOX) already on it. |
| **Manager GUI** (e.g. mcpmarket listing) | Dashboard to toggle MCP servers on/off across clients | Operator | **Skip.** Federation has `forge_probe`/`forge_registry_status`/WELL/FRAME. Claims UNVER (mcpmarket 403 on fetch). |
| **STMCP** | Vendor platform: monitor/start/stop MCP instances, IDE plugins, curated collections | Operator | **Skip.** Same class as above; claims UNVER (stmcp.com returned 402 payment wall). Never adopt unverified vendor surfaces. |
| **Desktop GUI-automation MCP** (e.g. `kitfactory/PyMCPAutoGUI`) | Server exposes mouse/keyboard/screenshot tools so an agent *drives* desktop apps (PyAutoGUI) | agent-as-user | **Opposite direction** — agent controls GUIs; MCP Apps serves UIs to humans. Not a GUI-for-MCP solution; irrelevant to organ surfaces. EXT 2026-09-22: 23★, MIT, 8 commits. |

Rule: **GUI = trust surface** (F13 doctrine) — build panels for human clarity, not ops dashboards the federation already covers.

## 2. MCP Apps spec mechanics (EXT, modelcontextprotocol.io 2026-07-28 era)

- Tool declares **`_meta.ui.resourceUri`** → `ui://...` resource, mime **`text/html;profile=mcp-app`**.
- Host may **preload** the UI resource before the tool call (enables streaming inputs).
- Render: **sandboxed iframe**; `_meta.ui.csp` controls external origins; `_meta.ui.permissions` for mic/camera etc.
- Bridge: **postMessage JSON-RPC dialect** — app↔host methods `ui/*` (e.g. `ui/initialize`), core `tools/call` shared. App can request tool calls, context updates, open links.
- Official SDK: `@modelcontextprotocol/ext-apps` (`App` class, AppBridge host module). Community: **`@mcp-ui/client`** (`AppRenderer` — props `client`, `toolName`, `toolInput`, `toolResult`, `sandbox={{url}}`, `onOpenLink`, `onMessage`), `@mcp-ui/server` (`createUIResource()`), Python `mcp-ui-server`, Ruby `mcp_ui_server`.
- Legacy MCP-UI hosts use the adapter guide (mcpui.dev/guide/mcp-apps); new builds target the spec only.

## 3. Host matrix (EXT mcpui.dev/guide/supported-hosts, fetched 2026-09-22)

- **Native MCP Apps:** Claude(.ai/Desktop), VS Code Copilot, MS 365 Copilot, Goose, LibreChat, Postman, MCPJam, Smithery, mcp-use, Archestra.AI.
- **ChatGPT:** does NOT implement MCP Apps — its own **Apps SDK**; UI actions partial. Federation route = gateway (`:3003`) absorbs the epoch difference.
- **fast-agent:** renders `ui://` but no UI actions.
- Discovery direction differs: MCP Apps hosts read `_meta.ui.resourceUri` on the **tool**; legacy MCP-UI hosts read embedded `ui://` **resources**. Support both channels when portability matters.

## 4. Portability test recipe (claim → proof ladder)

1. **Self-probe** (fast, no host needed): initialize → `resources/list` (follow `nextCursor`) →
   `resources/read` every `ui://` — assert mime `text/html;profile=mcp-app`, size >200b.
   Every stub (<200b) = conformance fail (`ui-resource-contents-valid`).
2. **Inspector**: mcpui.dev points at `github.com/idosal/ui-inspector`, **but its README currently
   reads as a fork of `modelcontextprotocol/inspector` (UNVER 2026-09-22)** — verify the package
   before trusting. Fallback: `npx @modelcontextprotocol/inspector --cli <streamable-http-url>`
   (UI mode default ports 6274/6277, Node ≥22.7.5).
3. **Second host**: run the same tool call in a non-origin host (Goose or LibreChat) — if the panel
   renders, portability is *proven*; one host only = *claimed*.
4. **Regression row**: `render pass/fail × host` in the regression script — one row per host, ever after.
5. Registry hygiene: regenerate surface registries **from the live probe**, never hand-maintained —
   reverse indexes (`bound_tools`) go stale silently when tools consolidate into mode-umbrellas.

## 5. Worked example — GEOX (2026-09-22)

GEOX `:8081` declares `io.modelcontextprotocol/ui`, 25 tools (24 ui-bound), 25 `ui://` resources
(22 renderable, 3 deprecated stubs). Claude renders Basin Explorer (OBS in production chat).
Findings + task list: `/root/forge_work/2026-09-22-GEOX-MCP-APPS-GUI-REMAINDER.md`.
GEOX proves adoption; remaining work is render-truth hygiene + cross-host proof (T8–T10).
