---
name: mcp-transport-fix
owner: HERMES
description: Fix MCP auth failures when external clients cannot connect.
version: 1.0.0
author: Hermes
tags: MCP, transport, auth, Claude, ChatGPT
---

# MCP Transport Fix — SSE vs Streamable HTTP

> When Claude/ChatGPT/Cursor fail to connect, the transport is the cause.

## The Rule

External MCP clients (Claude, ChatGPT, Cursor, Gemini) expect **Streamable HTTP** (`POST /mcp`), not SSE (`GET /sse`).

If `transport="sse"`, external clients fail:
- `POST /sse → 405`
- `POST /mcp → 404`

## The Fix

### 1. Server

```python
# BEFORE
mcp.run(transport="sse", port=port, host="127.0.0.1")
# AFTER
mcp.run(transport="streamable-http", port=port, host="127.0.0.1")
```

### 2. Caddy

Remove `rewrite * /sse` — POST /mcp must go directly to backend.

### 3. Restart service

Transport is module-level config; restart required.

## Verification

```bash
curl -X POST http://127.0.0.1:PORT/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
# Should return tool definitions
```

## Pitfall

SSE works for local clients (Hermes, OpenCode) via `GET /sse`. Failure only manifests on external platforms that POST to `/mcp`. Test both.

## Proven

CHRON MCP (:18102) — SSE caused Claude/ChatGPT failures. Fix: streamable-http + Caddy rewrite removed.