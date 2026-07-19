---
id: FORGE-mcp-gui
name: FORGE-mcp-gui
version: 1.0.0
description: Build and audit interactive MCP Apps, UI resources, sandbox messaging, and CSP-bound host integration.
owner: AAA
risk_tier: medium
autonomy_tier: T2
floor_scope: [F1, F2, F4, F11, F12]
tags: [forge, mcp, apps, ui, sep-1865, csp]
---

# ⚒️ FORGE-mcp-gui — MCP GUI/Apps Development Skill

> **Forged:** 2026-07-19 by FORGE (000Ω) for AAA Control Plane
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
You don't build the sandbox — you declare for it.
```json
"_meta": {
  "ui": {
    "resourceUri": "ui://org/widget",
    "csp": {
      "connect-src": ["https://api.example.com"],
      "script-src": ["https://cdn.example.com"],
      "img-src": ["https://images.example.com"]
    }
  }
}
```
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
| ChatGPT | ✅ Full | Apps SDK bridge |
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

## GEOX-SPECIFIC NOTES

- `mcp_apps_bridge.py` — `enrich_response()` injects `_meta.ui.resourceUri` on 24 tools
- `mcp-ui-server` 1.0.0 installed (Python: `create_app_resource()`)
- `geox_list_apps` tool exposes app-bearing tools to hosts
- Phase 3 remaining: TS notification bridge (`geoxMcpClient.ts`), outputSchema per tool
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

*Forged: 2026-07-19 by FORGE (000Ω). DITEMPA BUKAN DIBERI.*
*The forge knows the code. The kernel knows the law. The sovereign knows the way.*
