---
name: mcp-dual-era-transport
description: Use when an organ 400s on server/discover probes.
---

# MCP Dual-Era Transport (2026-07-28 stateless + 2025-11-25 legacy)

## Trigger
A federation organ answers the legacy `initialize` + `tools/list` handshake but returns
**HTTP 400** to a modern stateless probe:

```
POST /mcp
MCP-Protocol-Version: 2026-07-28
Mcp-Method: server/discover
{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{...}}}
```

## Diagnose before fixing (two gates, in this order)
With `mcp` 1.x installed, a stateless request is rejected *before method dispatch*:

1. `mcp/server/streamable_http.py::StreamableHTTPSessionManager._validate_session()` —
   `"Bad Request: Missing session ID"` (HTTP 400, code -32600). The app runs the
   transport stateful (`FastMCP.http_app(stateless_http=False)`), so any POST without
   `Mcp-Session-Id` dies here — including `tools/list`.
2. `...::_validate_protocol_version()` vs `mcp/shared/version.py::SUPPORTED_PROTOCOL_VERSIONS`
   (its `LATEST_PROTOCOL_VERSION` is the newest the SDK knows) — `"Bad Request: Unsupported
   protocol version: <newer>"`, HTTP 400 **even with a valid session id**.

Also check whether the SDK knows the method at all: `grep -rn "server/discover" <site-packages>/mcp <site-packages>/fastmcp`.

Triage commands (run both, they are different failure modes):
```bash
# 1. stateless (expect 'Missing session ID' on a stateful organ)
curl -s -w '\n%{http_code}\n' -X POST $URL/mcp -H 'Content-Type: application/json' \
  -H 'MCP-Protocol-Version: <newer>' -H 'Mcp-Method: server/discover' -d '{...}'
# 2. session + newer header (expect 'Unsupported protocol version')
SID=$(curl -sD- -o/dev/null -X POST $URL/mcp -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"<sdk-newest>","capabilities":{},"clientInfo":{"name":"p","version":"1"}}}' | tr -d '\r' | grep -i '^mcp-session-id' | awk '{print $2}')
curl -s -w '\n%{http_code}\n' -X POST $URL/mcp -H 'Content-Type: application/json' \
  -H 'Mcp-Session-Id: $SID' -H 'MCP-Protocol-Version: <newer>' -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

## Do NOT bump the SDK
`mcp` 2.x renamed `McpError` -> `MCPError` and dropped
`StreamableHTTPServerTransport._check_accept_headers`. Any transport built against 1.x
(most federation organs) fails at import after a bump. A naive `pip install -U mcp` looks
like per-organ breakage but is one shared-pin drift.

## Fix pattern — additive ASGI shim, transport untouched
Add a pure-ASGI middleware registered **innermost** (call `add_middleware` *before* all app
middlewares: Starlette inserts at index 0, so first-added runs last — after
auth/origin/version/lifecycle gates, so no security gate is bypassed):

- short-circuit pure legacy traffic (`Mcp-Session-Id` present + SDK-supported version) —
  never read the body, never rewrite;
- rewrite an unsupported `MCP-Protocol-Version` value down to the SDK-negotiated version;
- answer the unknown discovery method natively (`server/discover`) — mirror the shape the
  organ's already-working peers emit (probe them: `resultType`, `supportedVersions`,
  `capabilities`, `instructions`, `ttlMs`, `cacheScope`, `_meta` serverInfo/protocolVersion);
- bridge *other* session-less era-declared requests onto ONE shared internal session:
  ASGI-call `initialize` downstream, capture the `mcp-session-id` response header, send
  `notifications/initialized`, then inject the header and re-dispatch; on a 404 (stale
  session) drop it and rebuild once. If bootstrap fails, forward untouched so the client
  gets the transport's real error — never a fabricated success.

Deploy hazard: the git checkout you edit may not be the tree the unit runs. Check
`systemctl cat <unit>` for `WorkingDirectory`/`ExecStart`, then `sha256sum` both copies and
only then copy files in (the live tree is often a separate clone with a dirty worktree).

## Verify before and after, both directions
Keep a probe script printing, for staging and live: modern `server/discover` (200 + result),
legacy `initialize`/`notifications/initialized`/`tools/list` (same sorted tool-name list
before == after; compare hashes), one stateless `tools/call`, and `/health` surface_drift
`canonical == live`. Stage on an unused port with the live env file and a copied data dir
first; only then deploy, restart the unit, and re-run health immediately; keep a
one-command rollback script that restores the backed-up file and restarts.
Note for audits: a bodyless POST with neither session nor era headers still 400s — that is
the transport's own protocol violation, an intentional boundary, not a regression.
