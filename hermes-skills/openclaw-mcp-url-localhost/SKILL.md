---
name: openclaw-mcp-url-localhost
description: Fix OpenClaw MCP server timeouts when gateway runs on same VPS as Docker containers — patch Cloudflare public URLs to localhost. When openclaw mcp list shows servers unreachable but curl localhost:PORT/mcp works, this is the fix.
category: devops
---

## Problem

OpenClaw's `~/.openclaw/openclaw.json` has MCP server URLs configured as public Cloudflare addresses:

```json
"arifos": { "url": "https://arifos.arif-fazil.com/mcp", "transport": "streamable-http" }
```

These timeout or return 522 when the gateway runs on the same VPS as the containers, because Cloudflare isn't proxying internal Docker networks.

## Diagnosis

```bash
# These all fail from the VPS:
curl https://arifos.arif-fazil.com/mcp        # 522 or timeout
curl https://wealth.arif-fazil.com/mcp        # timeout
curl https://geox.arif-fazil.com/mcp          # timeout

# But these all succeed from the VPS:
curl http://127.0.0.1:8080/mcp    # arifOS ✅
curl http://127.0.0.1:8081/mcp    # GEOX ✅
curl http://127.0.0.1:8082/mcp    # WEALTH ✅
curl http://127.0.0.1:8083/mcp    # WELL ✅
```

Also check Docker port mappings:
```bash
docker port arifosmcp    # → 8080/tcp -> 127.0.0.1:8080
docker port geox_eic     # → 8081/tcp -> 0.0.0.0:8081
docker port wealth-organ # → 8082/tcp -> 127.0.0.1:8082
docker port well         # → 8083/tcp -> 127.0.0.1:8083
```

## Fix

1. **Backup first:**
   ```bash
   cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d)
   ```

2. **Patch all 4 federation MCP URLs in `~/.openclaw/openclaw.json`:**
   ```json
   "arifos": { "url": "http://127.0.0.1:8080/mcp" }
   "geox":   { "url": "http://127.0.0.1:8081/mcp" }
   "wealth": { "url": "http://127.0.0.1:8082/mcp" }
   "well":   { "url": "http://127.0.0.1:8083/mcp" }
   ```

3. **Restart gateway:**
   ```bash
   # Find orphaned root process
   ps aux | grep openclaw | grep gateway
   # Kill it
   kill <PID>
   # Restart via systemd
   systemctl --user start openclaw-gateway
   ```

4. **Verify:**
   ```bash
   openclaw mcp list
   # Should show all 4 servers as reachable
   ```

## Verification Commands

```bash
# Direct MCP JSON-RPC POST test (all return tool counts)
curl -s -X POST http://127.0.0.1:8080/mcp -H "Content-Type: application/json" -H "Accept: application/json" -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python3 -c "import sys,json; print(len(json.load(sys.stdin)['result']['tools']), 'tools')"

# Expected tool counts (arifOS era 2026.05.01):
# arifOS → 13 tools
# WEALTH → 50 tools
# GEOX   → 118 tools
# WELL   → 45 tools
```

## Gateway Orphan Detection

If `systemctl --user status openclaw-gateway` shows FAILED but a root-owned node process is running:
- Systemd service is broken (exit code 78)
- But the gateway itself is running as orphaned root process
- Fix: kill the orphan PID, restart via systemd

## arifOS-Specific Note

arifOS `/mcp` endpoint requires `Accept: application/json` header. GEOX and WELL return `405 Method Not Allowed` on GET — use POST for JSON-RPC. WEALTH and arifOS return metadata on GET.

## Security Note

`http://127.0.0.1` is only accessible from the VPS itself. This is correct — the gateway binds to localhost only, so external traffic routes through Cloudflare → Caddy → container. The localhost URLs are for gateway-to-container communication on the same host.
