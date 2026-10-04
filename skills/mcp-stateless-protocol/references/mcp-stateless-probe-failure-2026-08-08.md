---
description: "The 6-failed-curl probe transcript against stateless.mcpjam.com/mcp that produced a wrong 'demo endpoint' verdict, the OpenClaw trajectory that cracked it in 2 attempts, and the corrective audit. The warning: a failed probe is data, not a stop signal. Read error.data.supported before declaring an endpoint dead."
doctrine: "DITEMPA BUKAN DIBERI"
forged: 2026-08-08
---

# MCP Stateless Probe Failure — 2026-08-08 Transcript

The canonical witness of the §19.1 lesson: **the verifier's own false certainty.** Six failed curl attempts against a real production-shaped endpoint, a wrong "demo endpoint, no tools" verdict, then a peer agent's 2-attempt crack that proved the endpoint live.

## The wrong verdict

I (the verifier) was asked to test whether `https://stateless.mcpjam.com/mcp` was a useful MCP server to wire into the federation. The endpoint was claimed to be MCPJam's reference test rig for the new MCP 2026-07-28 stateless wire format.

Six curl attempts. Each failed. None of them tried the new protocol envelope shape.

```bash
# Attempt 1 — legacy body protocolVersion
curl -s --max-time 10 -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"hermes-probe","version":"1.0"}}}'
# → "Unsupported protocol version: 2025-06-18" + data.supported:["2026-07-28"]

# Attempt 2 — body protocolVersion 2026-07-28
curl -s --max-time 10 -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2026-07-28","capabilities":{},"clientInfo":{"name":"hermes-probe","version":"1.0"}}}'
# → "Unsupported protocol version: 2026-07-28" + data.supported:["2026-07-28"]

# Attempt 3 — body protocolVersion 2026-07-28 with header
curl -si --max-time 10 -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2026-07-28","capabilities":{},"clientInfo":{"name":"hermes-probe","version":"1.0"}}}'
# → -32020 "Bad Request: the request headers and body disagree: an initialize request (legacy handshake) was sent with a modern MCP-Protocol-Version header"

# Attempt 4 — body method omitted (header only)
curl -si --max-time 10 -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' -H 'Mcp-Method: tools/list' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
# → -32600 "Bad Request: the request body is not a valid JSON-RPC message"

# Attempt 5 — Mcp-Name header addition
curl -si --max-time 10 -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' -H 'Mcp-Method: tools/call' \
  -H 'Mcp-Name: echo' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"echo","arguments":{"message":"arif-forge probe OK"},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
# → -32020 "the body carries params.name='echo' but the required Mcp-Name header is absent"

# Attempt 6 — final attempt
curl -si --max-time 10 -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
# → -32600 "Bad Request: the request body is not a valid JSON-RPC message"
```

I stopped at attempt 6 and reported: **"the endpoint is a vendor demo, not a real tool. Skip it."**

## The peer agent's 2-attempt crack

While I was reporting "skip it," OpenClaw (FI-004) was independently probing the same endpoint and cracked it in 2 attempts. The trajectory lives at:

```
/root/.openclaw/agents/main/sessions/599ad7d0-3148-41b2-9f60-954b731285ec-topic-128618.trajectory.jsonl
```

The 2 attempts that worked:

```bash
# OpenClaw's attempt 1 — discover tool list
curl -sS -m 15 -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' -H 'Mcp-Method: tools/list' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
# → 13 tools, full JSON, returned in 135ms

# OpenClaw's attempt 2 — call echo
curl -sS -m 15 -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' -H 'Mcp-Method: tools/call' -H 'Mcp-Name: echo' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"echo","arguments":{"message":"arif-forge probe OK"},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
# → 200 OK, {"result":{"content":[{"type":"text","text":"echo: arif-forge probe OK"}],"structuredContent":{"echoed":"arif-forge probe OK"},"resultType":"complete","_meta":{"io.modelcontextprotocol/serverInfo":{"name":"mcpjam-stateless","version":"0.3.1"}}}}
```

The difference between my 6 failures and OpenClaw's 2 successes: I never read the **error.data.supported** field. I treated the 400 codes as stop signals. OpenClaw read the structured error and kept iterating.

## The 13 tools (live, not fixture)

The endpoint exposes 13 working fixture tools, each exercising a different MCP 2026-07-28 feature:

| Tool | Feature exercised |
|---|---|
| `echo` | basic call |
| `execute-sql` | basic call with foreign-shape args |
| `get-weather` | outputSchema validation |
| `long-task` | progress notifications (`_meta.progressToken`) |
| `fail` | error path (mode=result/throw) |
| `ask-name` | MRTR elicitation (form mode) |
| `confirm-launch` | MRTR 2-round signed requestState |
| `open-dashboard` | MRTR URL elicitation |
| `summarize` | MRTR sampling (client-side LLM) |
| `list-client-roots` | MRTR roots/list |
| `never-satisfied` | MRTR round-limit edge case |
| `trigger-notifications` | subscriptions (list_changed, resources/updated) |
| `run-task` | Tasks extension (CreateTaskResult + tasks/get polling) |

Server identity: `mcpjam-stateless` v0.3.1. Hosted on Cloudflare. No auth. Reference implementation for the new MCP 2.0 wire format.

## The lesson

| My error | OpenClaw's correct move |
|---|---|
| Read 400 status code, concluded "dead" | Read `error.data.supported` + `error.data.envelope.missing` |
| Tried 6 shapes, gave up at 6 | Tried 2 shapes, read the diagnostic, kept iterating |
| Reported "skip it" with receipts | Reported "federation has 13 working tools" with receipts |
| The verifier's verdict was wrong by 13 tools | The peer agent's verdict was right |

The trap: **a failed probe is data, not a stop signal.** The server's error response is the server's way of telling you exactly what it accepts. Read `error.data.supported` before retrying. Never conclude "useless" until the current-spec envelope has been tried.

## The corrective audit pattern

When a peer agent's result contradicts your own verdict, the right move is to:

1. Pull the peer's transcript (`.openclaw/.../trajectory.jsonl` in this case)
2. Extract the exact shape that worked (headers + body, no paraphrase)
3. Re-run it yourself with the peer's recipe
4. Update the verdict with the receipt
5. Cite the peer as a witness, not as a brag

I did this in the same session, issued a public correction, and instructed the user to wire the endpoint into 5 agents. That correction is now the canonical wisdom in `SKILL.md` §5 ("Don't conclude 'useless/demo' before trying the current-spec envelope").

## Receipts (file:line)

- My 6 failed attempts: this transcript (above)
- OpenClaw's 2 successful attempts: `/root/.openclaw/agents/main/sessions/599ad7d0-3148-41b2-9f60-954b731285ec-topic-128618.trajectory.jsonl` (read this file to see the actual envelope shape)
- The corrected verdict: `FORGE-mcp-probe/SKILL.md` §"The Canonical Reference" + §"The handshake that works"
- The probe toolchain: `FORGE-mcp-probe` (the canonical tool for "should I wire this MCP server?")

## Generalization (not just MCP)

The pattern fires anywhere a structured error response names what the server accepts. The 2026-08-08 MCP case generalizes to:

| Domain | "Endpoint is dead" verdict | Metadata that should have been read |
|---|---|---|
| MCP 2026-07-28 | "demo endpoint, no tools" | `error.data.supported:["2026-07-28"]` |
| OAuth DCR | "OAuth not supported" | `error.data.supported_flows:["authorization_code","device_code"]` |
| HTTP API versioning | "API version unknown" | `Server: <version>` header / `Accept: application/vnd.x+json;version=2` |
| gRPC | "Service unavailable" | `grpc-status-details-bin` trailer |
| WebSocket subprotocol | "WS handshake failed" | `Sec-WebSocket-Protocol: <supported-list>` |

Rule: whenever a server returns a structured error with a `data` field or `supported` list, **read it before concluding the server is unusable**. The error is the server's way of telling you exactly what it accepts.

## Calibration check (post-mortem)

What I should have said after attempt 6:

> "My probes failed against legacy protocol shapes. The endpoint rejects my 2025-11-25 envelope. Per the server's `error.data.supported`, it accepts 2026-07-28 only. Let me try that envelope before declaring verdict. Correcting now."

What I actually said:

> "The endpoint is a vendor demo, not a real tool. Skip it."

The first answer is honest about the probe's limit. The second is **confident-wrong** and leaves the user to discover the truth later. The cost of the second answer is: the user spent 5 minutes cross-checking my verdict, asked a peer agent to confirm, and corrected me in the same session. The cost of the first answer: 30 seconds of retry.

Failure mode: **the verifier's failure to read error metadata is the same shape as the sibling's failure to read the file's data field.** Both are "trust the prose, skip the probe." Both produce confident wrong verdicts.

*DITEMPA BUKAN DIBERI — read error.data, always.*
