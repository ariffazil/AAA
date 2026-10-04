# Stateless MCP Migration Checklist (2026-07-28 Spec)

> Forged 2026-08-11 from A-FORGE diagnosis session.

## What Changed in the Spec

The 2026-07-28 MCP specification removes all protocol-level session state:

| Before (stateful) | After (stateless) |
|---|---|
| `initialize` handshake required | No handshake — first request = first action |
| `Mcp-Session-Id` header on every request | Removed entirely |
| Server maintains session DB (Redis/memory) | No server-side session storage |
| Sticky sessions required for LB | Standard round-robin LB works |
| Can't scale to zero | Serverless-ready (Cloud Run, CF Workers) |

## What to Remove from Existing Servers

```javascript
// DELETE: Session ID injection middleware
if (!req.headers["mcp-session-id"]) {
  req.headers["mcp-session-id"] = randomUUID(); // ← REMOVE
}

// DELETE: Session ID generator in transport config
sessionIdGenerator: () => randomUUID()  // ← REMOVE

// DELETE: Session validation on initialize
if (hasSessionId && isInitialize) { /* error */ }  // ← REMOVE
```

## What to Add

```javascript
// Every request carries inline metadata:
// Client sends: POST /mcp
// {
//   "jsonrpc": "2.0",
//   "method": "tools/call",
//   "params": { "name": "forge_shell", "arguments": {...} },
//   "_meta": {
//     "protocolVersion": "2026-07-28",
//     "capabilities": { "tools": {}, "resources": {} }
//   }
// }

// Server reads _meta instead of session state
const meta = req.body?._meta;
const version = meta?.protocolVersion;
```

## New Routing Headers

| Header | Purpose | Example |
|---|---|---|
| `Mcp-Method` | JSON-RPC method name | `tools/call` |
| `Mcp-Name` | Tool/resource/prompt name | `forge_shell` |

These let gateways (Caddy, Cloudflare, API gateways) inspect traffic **without parsing JSON bodies**.

## Discovery Method

```
POST /mcp
{
  "jsonrpc": "2.0",
  "method": "server/discover",
  "params": {},
  "_meta": { "protocolVersion": "2026-07-28" }
}
→ Returns: capabilities, supported methods, tool list
→ No session created
```

## Migration Checklist

1. [ ] Remove `Mcp-Session-Id` header handling (read + inject)
2. [ ] Remove `sessionIdGenerator` from transport config
3. [ ] Remove session DB / Redis dependency for MCP
4. [ ] Add `_meta` parsing for protocol version + capabilities
5. [ ] Add `Mcp-Method` / `Mcp-Name` header support (optional, for gateway compatibility)
6. [ ] Add `server/discover` method (optional)
7. [ ] Update Caddy: remove sticky session directives if any
8. [ ] Test: client sends tools/call without any session header → should work
9. [ ] Test: two concurrent clients, no session isolation needed (stateless = no cross-client state)

## A-FORGE Specific Notes

A-FORGE `server.js` currently has session injection hack (lines ~191-253):
- `sessionIdGenerator: () => randomUUID()` — remove
- Session ID auto-injection middleware — remove
- `session_required_tool_count` metric — remove or repurpose

The StreamableHTTPServerTransport from `@modelcontextprotocol/sdk` v1.29+ supports stateless mode when no session generator is provided.

## Infrastructure Benefits (ΔS ≤ 0)

- **One less Redis dependency** for MCP session storage
- **Standard load balancing** — no sticky sessions needed
- **Scale to zero** — serverless platforms can spin down idle MCP servers
- **Simpler debugging** — each request is self-contained, no session replay needed

## References

- [SEP-2575: Make MCP Stateless](https://modelcontextprotocol.io/specification/2026-07-28)
- [Google Developers Blog: Scaling AI Agent Infrastructure with MCP Stateless](https://blog.google/developers/2026-08-06-mcp-stateless)
- [The 2026-07-28 Specification](https://modelcontextprotocol.io/blog/2026-07-28-spec)
