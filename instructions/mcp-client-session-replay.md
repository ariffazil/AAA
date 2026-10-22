# MCP CLIENT SESSION REPLAY — FastMCP organs (F13 rec-C note, 2026-10-21)
> **Status:** DRAFT_AWAITING_F13 2026-10-21 — reproduction note for FastMCP session-scoped MCP behaviour; spec probe record, not ratified doctrine.

Organs (GEOX :8081, WEALTH :18082, WELL :18083, arifOS :8088) speak session-scoped
MCP. A bare `tools/list` returns **400** — that is SPEC behaviour, not organ
defect (reproduced 2026-10-21; PATCH 10 withdrawn by F13).

Correct client flow (all four steps; skip any → 400):

    1. POST /mcp  initialize  (protocolVersion: "2025-11-25",
       Accept: "application/json, text/event-stream")
    2. Capture `Mcp-Session-Id` from the RESPONSE HEADERS.
    3. POST notifications/initialized with header `Mcp-Session-Id: <sid>`.
    4. POST tools/call | tools/list with header `Mcp-Session-Id: <sid>`.

Reference implementation: /root/arifOS/scripts/federation_reality_probe.py
(_probe_mcp_tool_count — commit ba98c9a4c).

Known quirk (owner: A-FORGE): :7072/mcp initialize=200 with NO session header;
tools/list=404. Not a generic-MCP issue — A-FORGE lane to spec.

## Re-derivation

Core claim: arifOS :8088 speaks session-scoped MCP: a bare tools/list without the session handshake is rejected with 4xx (spec behaviour, not an organ defect); the working probe pattern is POST /mcp with Accept: application/json, text/event-stream.
Re-derive against live state:

```
$ curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8088/mcp -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
$ curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8088/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```
