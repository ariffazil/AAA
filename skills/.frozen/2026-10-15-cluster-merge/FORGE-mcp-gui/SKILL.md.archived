---
id: FORGE-mcp-gui
name: FORGE-mcp-gui
version: 1.1.0
description: Build and audit interactive MCP Apps, UI resources, sandbox messaging, and CSP-bound host integration
owner: AAA
risk_tier: medium
autonomy_tier: T2
floor_scope: [F1, F2, F4, F11, F12]
tags: [forge, mcp, apps, ui, sep-1865, csp]
---

# ⚒️ FORGE-mcp-gui — MCP GUI/Apps Development Skill

> **Forged:** 2026-07-19 by FORGE (000Ω) for AAA Control Plane
> **Hardened:** 2026-07-20 — ChatGPT-native MCP Apps standard (sovereign blueprint:
> `/root/forge_work/2026-07-20/GEOX-CHATGPT-MCP-GUI-BLUEPRINT.md`)
> **Zen Name:** FORGE-mcp-gui
> **Axis:** forge · **Tier:** AGI · **Class:** C2 Observe+Execute
> **Spec:** SEP-1865 (MCP Apps, ratified 2026-01-26)
> **Doctrine:** DITEMPA BUKAN DIBERI

---

## USE WHEN

The task involves:
- Building interactive UI for MCP tools (MCP Apps, mcp-ui, SEP-1865)
- Creating dashboards, charts, forms, maps, approval gates for MCP servers
- Wiring `_meta.ui.resourceUri` on tool definitions
- Using `@mcp-ui/server`, `@mcp-ui/client`, `@modelcontextprotocol/ext-apps`
- Using `mcp-ui-server` (Python) or `fastmcp` Prefab
- Debugging sandboxed iframe rendering in MCP hosts
- Declaring CSP (`_meta.ui.csp`) for secure UI rendering
- Handling hostContext adaptation (theme, locale, dimensions)
- Implementing model-in-the-loop patterns (sendMessage, updateModelContext)
- Setting tool visibility (`["model"]`, `["app"]`, `["model","app"]`)
- Comparing MCP Apps vs A2UI (Google) vs ChatGPT Apps SDK
- Bundling UI with Vite singlefile for MCP resource serving

---

## DO NOT USE WHEN

- The task is purely text/data output (no UI needed)
- The answer fits in a single text response
- The tool is autonomous with no human-interaction surface
- Building traditional web apps (not MCP-hosted)
- The task requires only MCP server-side logic without UI

---

## CANONICAL ARCHITECTURE

```
MCP Tool (server) ──→ _meta.ui.resourceUri: "ui://org/widget"
                           ↓
                    Host fetches resource via resources/read
                           ↓
                    Sandboxed iframe renders HTML
                           ↓
                    JSON-RPC over postMessage (View ↔ Host ↔ Server)
```

### Three Return Channels
```
content:          → model sees this (context window, keep small)
structuredContent → hidden from model, View hydrates with it (full data)
_meta:            → hidden from model, metadata only
```

---

## 15 CANONICAL TIPS (Load These Before Any MCP UI Task)

### 1. Control Data Flow
Model gets summary text. View gets full structured data. Save context tokens.

### 2. Always Ship Text Fallback
```python
return {
    "content": [{"type": "text", "text": "Summary..."}],
    "structuredContent": {"fullData": ...},
    "_meta": {"ui": {"resourceUri": "ui://org/widget"}}
}
```
Never UI-only — hosts may not support MCP Apps.

### 3. Adapt to HostContext
Two-layer: CSS `light-dark()` for first render, JS `data-theme` after hostContext arrives.
```javascript
app.onhostcontextchanged = (ctx) => {
  document.documentElement.setAttribute('data-theme', ctx.theme);
};
```

### 4. Separate Data Tools from Render Tools
Tool A returns data → model processes → Tool B renders UI. Avoids remounts.

### 5. Keep Model in the Loop
```javascript
app.sendMessage("User did X. Respond.");       // active trigger
app.updateModelContext({ cart: items });       // background awareness
```

### 6. Tool Visibility
```json
"visibility": ["app"]      // UI only — model can't call
"visibility": ["model"]    // model only — UI can't call
"visibility": ["model", "app"]  // both (default)
```

### 7. Predeclared Resources (Not Ad-Hoc HTML)
Register 5 widget templates. Tools fill them with data. Hosts prefetch.

### 8. Double-Iframe Sandbox
You don't build the sandbox — you declare for it. CSP keys are **domain lists** under `_meta.ui.csp` (`connectDomains`, `resourceDomains`), NOT raw CSP header directives:
```json
"_meta": {
  "ui": {
    "resourceUri": "ui://org/widget",
    "csp": {
      "connectDomains": ["api.example.com"],
      "resourceDomains": ["cdn.example.com", "images.example.com"]
    }
  }
}
```
(The older `connect-src` / `script-src` header-style example previously shown here is superseded — see CHATGPT-NATIVE APPS §3 below.)
Missing CSP → silent block → broken app.

### 9. CSP Is Your Passport
Inventory EVERY external dependency (APIs, CDNs, fonts, images). Declare all. Test with CSP enabled — not dev mode.

### 10. Vite Single-File Bundle
```bash
npm install vite-plugin-singlefile
```
One HTML file = one MCP resource. No path issues in iframe.

### 11. Loading & Error States
Skeleton on mount → partial on toolInput → full on toolResult → error on failure.

### 12. Idempotent Tools
Models retry. Use idempotency keys. `create_task(key=uuid)` not `create_task(name="x")`.

### 13. Atomic Tools, Not God Tools
12 well-named tools > 60 poorly-named. Model picks by description string.

### 14. Debugging Across Two Transport Layers
Layer 1: MCP protocol (server↔host) — stdio/SSE logs.
Layer 2: JSON-RPC postMessage (host↔View) — iframe console.
Switch Chrome DevTools frame dropdown to sandbox iframe.

### 15. FastMCP `app=True` (Python)
```python
@server.tool(app=True)
def show_chart(data: list[float]) -> Chart:
    return BarChart(data=data, title="Results")
```
`fastmcp dev apps` launches in-browser UI preview. No React needed.

---

## SDK REFERENCE

### TypeScript — Canonical (ext-apps)
```typescript
import { registerAppTool, registerAppResource } from '@modelcontextprotocol/ext-apps/server';
import { App } from '@modelcontextprotocol/ext-apps';
```

### TypeScript — Community (mcp-ui)
```typescript
import { createUIResource } from '@mcp-ui/server';
import { AppRenderer, UIResourceRenderer } from '@mcp-ui/client';
```

### Python — Community
```python
from mcp_ui_server import create_ui_resource
```

### Python — FastMCP 3.2 (Generative UI)
```python
from fastmcp import FastMCP
server = FastMCP("my-server")
server.add_provider("FileUpload")
server.add_provider("Approval")
@server.tool(app=True)
def my_tool(...): ...
```

### Ruby — Community
```ruby
require 'mcp_ui_server'
McpUiServer.create_ui_resource(...)
```

---

## HOST SUPPORT MATRIX

| Host | MCP Apps | Notes |
|------|----------|-------|
| Claude (web+desktop) | ✅ Full | First adopter |
| ChatGPT | ✅ Full | 2026-07 standard: ship via Developer Mode first (golden prompts), then plugin submission package (verified publisher, exact CSP, unique widget domain, privacy policy, support contact, screenshots, rollback note). Alias `_meta["openai/outputTemplate"]` required alongside `_meta.ui.resourceUri`. |
| Goose | ✅ Full | Open source |
| VS Code Insiders | ✅ | Via Copilot |
| MCPJam | ✅ Full | Local inspector/debugger |
| LibreChat | ✅ Partial | |
| Postman | ✅ Partial | |
| Smithery | ✅ Render only | |

---

## A2UI COMPARISON (Google, 2026-06-17)

| | MCP Apps | A2UI |
|---|----------|------|
| Rendering | Sandboxed iframe | Host-native components |
| Flexibility | Unlimited | Component catalog only |
| Security | CSP + double-iframe | Capability-based |
| Consistency | Manual (CSS vars) | Automatic (design system) |
| Use when | Maps, 3D, PDFs, custom JS | Forms, structured data |

**Three hybrid patterns:**
1. A2UI over MCP Tools — declarative JSON as tool result
2. MCP App inside A2UI — iframe embedded in declarative surface
3. A2UI inside MCP App — ship A2UI renderer inside iframe

---

## CHATGPT-NATIVE APPS (2026-07 standard)

Contract source: sovereign blueprint `/root/forge_work/2026-07-20/GEOX-CHATGPT-MCP-GUI-BLUEPRINT.md` (authoritative for the GEOX consolidation; the rules below generalize to any ChatGPT-targeted MCP App). Where this section disagrees with older material in this skill, **this section wins**.

### 1. UI Binding Keys
- **Primary standard key:** `_meta.ui.resourceUri` on the tool definition.
- **ChatGPT compatibility alias:** emit `_meta["openai/outputTemplate"]` ALONGSIDE the primary key — never instead of it. Both point at the same `ui://` resource.
- **Optional:** `openai/toolInvocation/invoking` and `openai/toolInvocation/invoked` status strings (tool-call spinner copy).

### 2. Resource MIME + Versioned URIs
- Resource MIME MUST be exactly **`text/html;profile=mcp-app`**. The host only enables the app bridge for this exact profile MIME — plain `text/html` renders nothing.
- **Version every `ui://` URI — it is a cache key.** Pattern: `ui://geox/workbench-v1.html`. Bump the version segment to invalidate stale caches.

### 3. CSP via `_meta.ui.csp`
- Mandatory, exact domains: **`connectDomains`** (fetch/XHR/WS targets) and **`resourceDomains`** (scripts, styles, images, fonts).
- Optional: `domain` (widget's own domain), `prefersBorder` (host chrome hint).
- **Avoid `frameDomains`** — third-party iframes draw review scrutiny at submission.
- This supersedes the older `connect-src` / `script-src` header-style example (corrected in place at Tip #8).
- v1 pattern: single-file Vite bundle (inline JS) for the workbench shell → `resourceDomains` stays empty or near-empty.

### 4. Host Bridge Layering
- **Portable MCP Apps `ui/*` bridge FIRST:** `ui/initialize`, `ui/notifications/tool-input`, `ui/notifications/tool-result`, `tools/call`, `ui/message`, `ui/update-model-context`.
- **`window.openai` is an optional, feature-detected enhancement layer** (`if (window.openai) { ... }`) — never a requirement.
- **Never branch on product** ("if ChatGPT do X, if Claude do Y"). One portable path + progressive enhancement.

### 5. Three Return Channels Discipline
- `structuredContent` — widget props + model narration data ONLY. No secrets, no trace IDs, no dense raw arrays.
- `content` — text fallback **ALWAYS**. Hosts without MCP Apps support still get the answer; model context stays small.
- `_meta` — metadata and binding keys only.

### 6. Tool Error Contract
- Tool-originated failures return CallToolResult with **`isError: true`** and a readable message — the model can self-correct and retry.
- **Never surface a tool failure as a protocol-level error/crash.** A protocol crash kills the host session; `isError` keeps the loop alive.

### 7. Developer Mode Golden Prompts (First Host Gate)
Pass all three in ChatGPT Developer Mode before any other surface:
- **DIRECT** — "Open the GEOX Well Witness workbench for well X" → widget renders.
- **INDIRECT** — "Why is porosity low at 2,400 m in well X?" → model chains data tools, view tool renders the widget.
- **NEGATIVE** — out-of-scope / destructive ask → clean text refusal, no widget, no crash.

After Developer Mode: API Playground instrumentation → web + Android + iOS render/state evidence → plugin submission package (see HOST SUPPORT MATRIX).

---

## GEOX-SPECIFIC NOTES

- **Well Witness — first vertical slice (blueprint `pr/geox-well-witness-v1`):** split into `geox_well_ingest` → `geox_petrophysics` → `geox_well_view`; only the view tool binds `ui://geox/workbench-v1.html` (MIME `text/html;profile=mcp-app` + exact CSP). Exit gate: `resources/read` returns valid app HTML and renders in Inspector.
- `mcp_apps_bridge.py` — `enrich_response()` injects `_meta.ui.resourceUri` on 24 tools; harden to also emit the `_meta["openai/outputTemplate"]` alias alongside (CHATGPT-NATIVE §1).
- `mcp-ui-server` 1.0.0 installed (Python: `create_app_resource()`)
- `geox_list_apps` tool exposes app-bearing tools to hosts
- Phase 3 remaining: TS notification bridge (`geoxMcpClient.ts`), outputSchema per tool (blueprint families: GeoxStatusResult, GeoxArtifactResult, GeoxWellResult, GeoxSeismicResult, GeoxMapResult, GeoxProspectResult, GeoxClaimResult, GeoxEvidenceResult)
- High-value UI targets: `geox_map_render_preview`, `geox_seismic_cognition`, `geox_well_desk`

---

## FLOOR ALIGNMENT

| Floor | Binding | MCP UI Application |
|-------|---------|-------------------|
| F1 AMANAH | HARD | UI resources are reversible. Text fallback ensures no data loss. |
| F2 TRUTH | HARD | `structuredContent` vs `content` prevents model hallucination on raw data. |
| F4 CLARITY | HARD | UI reduces entropy — visual > wall of JSON. |
| F6 MARUAH | HARD | Approval gates for destructive actions. Human in loop. |
| F7 HUMILITY | HARD | Sandbox isolation. Model delegates to UI, doesn't claim omniscience. |
| F8 GENIUS | DERIVED | `visibility: ["app"]` for high-risk tools prevents model misuse. |
| F9 ANTI-HANTU | HARD | UI is rendered HTML, not consciousness. Tool, not being. |
| F11 AUDIT | HARD | JSON-RPC messages are loggable. CSP enforces declared domains. |
| F12 INJECTION | HARD | Sandboxed iframe blocks host DOM access. CSP blocks undeclared origins. |
| F13 SOVEREIGN | HARD | Approval gate = Arif's veto in UI form. |

---

## DEBUGGING CHECKLIST

- [ ] CSP domains declared in `_meta.ui.csp`?
- [ ] Text fallback returned alongside UI?
- [ ] `tools/list` shows `_meta.ui.resourceUri`?
- [ ] Host supports MCP Apps extension?
- [ ] Vite singlefile bundle (no relative path errors)?
- [ ] hostContext handled (theme, locale, dimensions)?
- [ ] Loading state rendered before toolResult arrives?
- [ ] Error state for failed tool execution?
- [ ] Chrome DevTools frame switched to sandbox iframe?
- [ ] `cloudflared` tunnel for remote host testing?

---

## ADDITIONAL REFERENCES

- MCP Apps Spec: https://github.com/modelcontextprotocol/ext-apps
- MCP-UI: https://github.com/MCP-UI-Org/mcp-ui
- SEP-1865: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md
- FastMCP 3.2: https://github.com/jlowin/fastmcp
- A2UI: https://developers.googleblog.com/a2ui-and-mcp-apps/
- MCPJam Inspector: https://github.com/idosal/ui-inspector
- Comprehensive Report: `/root/A-FORGE/forge_work/2026-07-19/MCP-GUI-COMPREHENSIVE-REPORT-2026-07-19.md`

---

*Forged: 2026-07-19 by FORGE (000Ω). Hardened 2026-07-20 to the ChatGPT-native blueprint. DITEMPA BUKAN DIBERI.*
*The forge knows the code. The kernel knows the law. The sovereign knows the way.*
