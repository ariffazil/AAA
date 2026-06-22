# ADR 014: MCP Concurrency & 888_HOLD Resolution (PHOENIX-73C)

## Status
Accepted

## Context
During the architectural review of the federation's MCP tools for constitutional alignment (F1/F13), we established that all high-risk tools (flagged with `"requires_888": true`) must consult the centralized arifOS Kernel (APEX, port 3002) for an `888_HOLD` verdict before proceeding.

However, the MCP SDK utilizing the `streamable-http` transport (identified as PHOENIX-73C) uses a singleton SSE stream key. This means only ONE SSE client can hold the stream open per session at a time. Attempting concurrent SSE connections results in a `409 Conflict`. 

If an organ's MCP server holds an active SSE connection with a client, and then attempts to open a *new* SSE connection to APEX to resolve the `888_HOLD`, this could lead to deadlocks, timeouts, or dropped connections, violating our robust engineering standards.

## Decision
To circumvent the PHOENIX-73C SSE limitation while maintaining synchronous enforcement of `888_HOLD`:

1. **POST-based JSON-RPC for Consultations**: When an organ's high-risk tool is invoked and needs to consult APEX, it MUST NOT use the SSE transport to communicate with APEX. Instead, it must utilize a synchronous **POST-based JSON-RPC** call to the APEX `888_HOLD` endpoint.
2. **Stateless Holding**: This allows the organ to hold the primary client's SSE stream open while the server-side logic blocks on the standard HTTP POST request to APEX.
3. **Timeout & Fallback**: The POST request to APEX must implement a strict timeout. If APEX is unreachable or fails to respond within the timeout, the tool MUST fail closed (Deny by default) in accordance with F1 (Amanah: Reversible-first).

## Consequences
- **Positive:** We resolve the `409 Conflict` risks associated with PHOENIX-73C. 
- **Positive:** `888_HOLD` checks remain robust and do not interfere with the primary client-to-organ SSE stream.
- **Negative:** Organ developers must explicitly implement standard HTTP POST handlers for the APEX check rather than reusing an initialized `streamable-http` client, slightly increasing boilerplate code.
