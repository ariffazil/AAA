---
name: fastmcp-http-session-debug
description: Debug FastMCP HTTP/SSE transport — session handshake, Accept header negotiation, and DelegatedTruthTool session errors. Discovered 2026-05-01 when A-FORGE delegation to WEALTH returned 406 Not Acceptable.
tags: [FastMCP, MCP, HTTP, SSE, session, A-FORGE, WEALTH, delegation]
last_updated: 2026-05-04
---

# FastMCP HTTP/SSE Session Protocol Debug

> **NOTE (2026-05-05):** GEOX and WELL have been patched to accept **plain JSON POST without session handshake**. arifOS and WEALTH do NOT have the monkey-patch — they rely on `Accept: application/json` header workaround (arifOS) or FastMCP's built-in `json_response=True` behavior (WEALTH). See `arifos-mcp-406-debug` for full details.

## The Two Modes

### Mode A — Session-based (original MCP HTTP/SSE)
Requires initialize handshake + session cookie on every request. Used when `stateless_http=False`.

### Mode B — Stateless JSON (2026-05-04 patch on GEOX/WELL; arifOS uses Accept header workaround)
GEOX and WELL accept plain JSON POST via monkey-patch on `StreamableHTTPServerTransport._check_accept_headers`. arifOS relies on `Accept: application/json` header workaround. WEALTH accepts plain JSON via FastMCP's built-in `json_response=True` behavior.

**See:** `arifos-mcp-streamable-http-debug` for the full patch + all 4 service details.

## Problem (Historical — pre-2026-05-04)

A-FORGE `DelegatedTruthTool` calls WEALTH MCP at `https://wealth.arif-fazil.com/mcp` but got:
```
406 Not Acceptable: Client must accept both application/json and text/event-stream
```
OR after adding Accept header:
```
Session not found
```

## Root Cause (Historical)

FastMCP HTTP/SSE transport is **session-based** by default. Plain JSON POST without handshake → 406 or Session not found.

## Correct MCP HTTP/SSE Query Protocol (for unpatched servers)

### Step 1 — Initialize (get session cookie)

```bash
RESPONSE=$(curl -s -X POST "https://WEALTH_URL/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0",
    "method":"initialize",
    "params":{
      "protocolVersion":"2024-11-05",
      "capabilities":{},
      "clientInfo":{"name":"test","version":"1.0"}
    },
    "id":1
  }')
```

Extract the `Mcp-Session-Id` from response headers:
```bash
curl -s -X POST "https://WEALTH_URL/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{...initialize payload above...}' \
  -D - 2>/dev/null | grep -i "mcp-session-id" | awk '{print $2}' | tr -d '\r'
```

### Step 2 — Use session cookie on subsequent calls

```bash
SESSION_ID="<extracted-session-id>"

curl -s -X POST "https://WEALTH_URL/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":2}'
```

### Key headers on EVERY request:
- `Content-Type: application/json`
- `Accept: application/json, text/event-stream` — **both**, not just JSON
- `Mcp-Session-Id: <session-id>` — from initialize response

## Why DelegatedTruthTool is Broken

`DelegatedTruthTool.ts` does this:
```typescript
const response = await fetch(`${this.laneBaseUrl}/mcp`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },  // ❌ Missing Accept
  body: JSON.stringify({ jsonrpc: "2.0", method: "tools/call", ... }),
});
```

Missing:
1. `Accept: application/json, text/event-stream` header
2. MCP session handshake (initialize → get session ID → use in subsequent calls)

## Verified Servers Using This Protocol

| Server | URL | Port |
|--------|-----|------|
| WEALTH | https://wealth.arif-fazil.com/mcp | 8082 (internal) |

## Fix Direction

DelegatedTruthTool needs to:
1. Do the MCP session handshake on first call (cache session ID)
2. Store the session cookie
3. Reuse it on all subsequent calls to that laneBaseUrl
4. Add `Accept: application/json, text/event-stream` header

This requires using a proper MCP client library (`@modelcontextprotocol/sdk`) rather than raw `fetch`.
