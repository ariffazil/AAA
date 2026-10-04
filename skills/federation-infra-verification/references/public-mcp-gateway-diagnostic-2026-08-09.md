# Public MCP Gateway Diagnostic — 2026-08-09

Session: Arif asked "Tell me arifOS MCP server status" + "Make sure I can connect through https://mcp.arif-fazil.com/mcp"

## What was probed

Full 5-layer stack from local kernel to public endpoint:

### Layer 1: Local kernel health
```bash
curl -sf http://127.0.0.1:8088/health
```
Result: `status=healthy`, `tools=8`, `version=v2026.08.01`, `drift=False`
- PID 2544716, started 2026-08-09T10:46:35 UTC
- 13 floors active, enforcement=active
- Surface consistency: CONSISTENT (8 tools across all vantage points)
- Vault999 health: healthy, circuit breaker closed

### Layer 2: Source/runtime drift
- **Source** (`/root/arifOS`): commit `39f6b1d90` — `fix(kernel): F4 CLARITY normalization calibration`
- **Runtime** (`/opt/arifos/app`): commit `594f0d2e4` — `merge: DRIFT_8 runtime hot-fixes → source`
- **Remote** (`origin/main`): same as source (`39f6b1d90`)
- Runtime has 5 DRIFT_8 commits NOT in source/remote (local hotfixes)
- BUT kernel health says `drift=False` — `build_commit == deployed_commit == 39f6b1d`
- Conclusion: runtime's DRIFT_8 commits are in git history but the deployed code matches source. No restart needed.

### Layer 3: Caddy reverse proxy
```
mcp.arif-fazil.com {
    handle /mcp* {
        reverse_proxy 127.0.0.1:8088 {
            header_up Accept "application/json, text/event-stream, */*"
        }
    }
}
```
- Accept header injection for Perplexity MCP connector compatibility (2026-07-04 fix)
- CORS headers configured via `cors_public` import
- CSP headers present with all federation subdomains in `connect-src`

### Layer 4: Cloudflare tunnel
- `cloudflared.service`: active (running) since 2026-08-01
- PID 2936604, 29MB memory
- Some `context-canceled` errors for geox.arif-fazil.com/mcp — client-side disconnects, not server failures

### Layer 5: Public endpoint
```bash
curl -sf -m 10 -X POST https://mcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,...}'
```
Result: Full JSON-RPC initialize response
- Server: `ARIFOS MCP`, version `kanon-2026.08.09+39f6b1d`
- Protocol: `2025-11-25` (also supports `2026-07-28`, `2025-03-26`, `2024-11-05`)
- 8 canonical tools, 38 static resources, 24 templates
- Instructions include full boot sequence, close sequence, canonical 8 tools
- `websiteUrl: https://mcp.arif-fazil.com`

### Landing page
- `https://mcp.arif-fazil.com/` serves 76KB dynamic HTML
- Title: "arifOS MCP — Constitutional AI Gateway"
- Sections: Quickstart, Endpoints, SDK connect, Tools, Prompts, Resources, 13 Floors, Trinity Architecture
- **Dynamic**: JavaScript fetches `/health` at runtime — auto-populates version, tools, thermodynamic state
- Static file: `/var/www/html/mcp/index.html` (last modified Aug 3)
- No manual update needed per deploy — only edit when template design changes

### Additional endpoints verified
| Endpoint | Status | Detail |
|----------|--------|--------|
| `/health` | 200 | Full health JSON |
| `/tools` | 200 | Tool manifest |
| `/` (landing) | 200 | Dynamic HTML |

## Key learnings

1. **`/mcp` is POST-only** — GET returns empty body with 200 (not an error, just no GET handler). Must use `-X POST` with JSON-RPC body.

2. **Landing page self-updates** — No per-deploy intervention needed. The JS fetches live `/health` data.

3. **Source/runtime git mismatch ≠ drift** — The kernel's own drift check (`build_commit == deployed_commit`) is authoritative. Runtime can have extra git commits (DRIFT_8 hotfixes) while the deployed code matches source. Don't recommend restart based on git commit mismatch alone.

4. **Cloudflare `context-canceled` = client-side** — Not a server failure. The client disconnected before the response came back.

5. **CORS preflight blocks browser-based MCP clients** — The kernel's CORS middleware returns `400 Disallowed CORS origin` for non-allowlisted origins. Browser-based clients (MCPJam, ChatGPT MCP) fail before the POST even fires. Fix: add `import cors_public` to Caddy `/mcp*` handler. Full recipe: `references/cors-preflight-fix-2026-08-09.md`.

## Verdict

All 5 layers green (post-CORS fix). No restart needed. Public MCP endpoint fully functional for both curl and browser-based clients.
