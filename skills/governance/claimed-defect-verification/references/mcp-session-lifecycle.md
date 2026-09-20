# MCP Session Lifecycle — the handshake that makes `tools/call` dispatch

> Only needed when probing a **stateful** MCP endpoint (the common default: `FastMCP.http_app(stateless_http=False)`).
> A stateless endpoint needs none of this.

## Why a bare POST looks like a broken server

A stateful transport rejects `tools/call` and even `tools/list` **before method dispatch** when the
session lifecycle was not completed. The rejection is precise and correct — it names the missing step —
and that message is routinely escalated as a capability, contract, or guard failure.

## The three steps

```bash
PORT=8081

# 1. initialize — take the session id from the RESPONSE HEADER, never from the body
SID=$(curl -sD- -o/dev/null --max-time 10 -X POST "http://127.0.0.1:$PORT/mcp" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}' \
  | tr -d '\r' | grep -i '^mcp-session-id' | awk '{print $2}')

# 2. notifications/initialized — required before tools/call on some organs
curl -s --max-time 10 -X POST "http://127.0.0.1:$PORT/mcp" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# 3. now list and call
curl -s --max-time 10 -X POST "http://127.0.0.1:$PORT/mcp" \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

Two facts that dissolve most of the confusion:

- The session id is delivered in the **`Mcp-Session-Id` response header**. It is never a tool argument,
  so an organ that "demands a session" is **not** exposing an unsatisfiable contract and **no schema
  field is missing**.
- The `Accept: application/json, text/event-stream` header is mandatory. Omitting it yields
  `Not Acceptable: Client must accept text/event-stream`.

## Decode table

| Error returned | Actually means | Never report as |
|---|---|---|
| `SESSION_MISSING: Mcp-Session-Id header required` | step 1 skipped | "contract impossible to satisfy" |
| `Bad Request: Missing session ID` (code -32600) | step 1 skipped | "server broken" |
| `MCP_LIFECYCLE: tools/call rejected until client sends notifications/initialized` | step 2 skipped | "a runtime guard blocks this tool" |
| `Not Acceptable: Client must accept text/event-stream` | `Accept` header omitted | "endpoint down" |
| `Bad Request: Unsupported protocol version: <x>` | version newer than the SDK knows | "incompatible server" — see the era-mismatch notes in `mcp-testing` §5 |

## Expected results once the lifecycle is complete

Measured on a six-organ federation; the numbers moved between passes, so treat the *shape* as the
takeaway, not the values:

| Where the count comes from | Note |
|---|---|
| A REST `/tools` surface | one number |
| `tools/list` over a completed session | a **different** number (seen: 25 vs 27) |
| `health` | a third thing entirely — liveness, not capability |

Publish each figure with its surface. Never merge them into "the tool count".

## Health vs capability

A green `/health` beside a failing call is not a contradiction — it is two different questions.
A health endpoint that reports `key_loaded: true` while every request is refused is measuring process
liveness, not lane function. Read both, and say which gate each one tests.

## Also verify the name

Before declaring a tool missing, dump the advertised list and grep it:

```bash
# from a tools/list response saved to disk
grep -o '"name": *"[a-z_0-9]*"' /tmp/tools.json | sort -u
```

`Unknown tool: 'x'` where `x` was never advertised is a **name error**. Near-miss names (a longer or
suffixed variant of the real one) read as plausible and survive review, so compare against the listing
rather than against recollection.
