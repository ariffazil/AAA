# MCP 2026-07-28 Stateless Envelope — Probe Results

**Session:** 2026-08-08, two probes by different agents
**Endpoint probed:** `https://stateless.mcpjam.com/mcp`
**Result:** Live conformance test server with **13 working tools**, not a demo endpoint

---

## Hard-won lesson from this session

The endpoint is **NOT a demo**. It is a real test server exercising every major MCP 2026-07-28 feature:
stateless transport, MRTR (multi-round elicitation), progress streaming, sampling, and the
Tasks extension. The 13 tools are fixtures, but the implementation is production-shape.

Initial probe (this session) declared it "probably empty" after 6 failed handshake attempts.
The OpenClaw agent cracked it in 2 attempts via trajectory-log evidence. **Do not repeat the
first probe's mistake** — when the server says `-32600` or `-32602`, the answer is usually
**add the missing envelope key**, not "the endpoint is dead."

| Server field | Value |
|---|---|
| URL | `https://stateless.mcpjam.com/mcp` |
| Server name | `mcpjam-stateless` |
| Server version | `0.3.1` |
| Server hosting | Cloudflare (cf-ray visible) |
| Protocol | `2026-07-28` ONLY (stateless) |
| Auth at edge | None (public) |
| Tools | 13 (see below) |
| Tool surface feature | Exercises stateless transport, MRTR, progress streaming, sampling, Tasks extension |

---

## The 13 tools (don't list them as "empty")

| Tool | Purpose | Tests feature |
|---|---|---|
| `echo` | Round-trip a message | Basic RPC |
| `get-weather` | Deterministic fake weather | Output schema validation |
| `execute-sql` | Run query against regional DB | `Mcp-Param-Region` header routing |
| `long-task` | Run N steps with delay | Progress notifications via `_meta.progressToken` |
| `fail` | Force isError or throw | Error result handling |
| `ask-name` | Elicit name via form | MRTR (input_required resultType) |
| `confirm-launch` | Two-round confirmation | MRTR with signed requestState |
| `open-dashboard` | URL elicitation | Client-side URL launch |
| `summarize` | Send text to client LLM | Sampling |
| `list-client-roots` | Roots/list via MRTR | Roots capability |
| `never-satisfied` | Always asks again | Round-limit test |
| `trigger-notifications` | Publish list_changed events | Notifications |
| `run-task` | Returns CreateTaskResult | Tasks extension |

---

## Request shapes tested (this session)

| # | Shape | Result | Why |
|---|---|---|---|
| 1 | `protocolVersion` in body, no header | `-32022 UnsupportedProtocolVersion` | Body-only not accepted |
| 2 | `protocolVersion: "2026-07-28"` in body | `-32022 UnsupportedProtocolVersion` | Even correct version rejected if in body |
| 3 | `MCP-Protocol-Version: 2026-07-28` header + body `protocolVersion` | `-32020 HeaderMismatch` | Header says modern, body says initialize (legacy) |
| 4 | Header `2025-11-25` | `-32022 UnsupportedProtocolVersion` | Only `2026-07-28` accepted |
| 5 | `MCP-Protocol-Version: 2026-07-28` + `Mcp-Method: tools/list` + JSON-RPC body without `_meta` | `-32600 not a valid JSON-RPC message` | Missing `_meta` envelope keys |
| 6 | Header + `Mcp-Method: tools/list` + `_meta.io.modelcontextprotocol/*` keys | ✅ **200 OK**, full tool list returned | **This is the working shape** |

From the OpenClaw trajectory (verified working):

```bash
# Tool list — works without Mcp-Name header
curl -sS -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/list' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientInfo":{"name":"my-app","version":"1.0"},"io.modelcontextprotocol/clientCapabilities":{"roots":{"listChanged":false},"sampling":{},"elicitation":{}}}}}'

# Tool call — REQUIRES Mcp-Name header (the docs don't make this prominent)
curl -sS -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/call' \
  -H 'Mcp-Name: echo' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"echo","arguments":{"message":"hello"},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientInfo":{"name":"my-app","version":"1.0"},"io.modelcontextprotocol/clientCapabilities":{"roots":{"listChanged":false},"sampling":{},"elicitation":{}}}}}'
```

The `Mcp-Name` header is the single most-missed requirement. Without it, the response is:
`"the body carries params.name=\"echo\" but the required Mcp-Name header is absent"` (error `-32020`).

---

## Required envelope keys (final, working recipe)

```json
{
  "_meta": {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientInfo": {
      "name": "my-client",
      "version": "1.0"
    },
    "io.modelcontextprotocol/clientCapabilities": {
      "roots": { "listChanged": false },
      "sampling": {},
      "elicitation": {}
    }
  }
}
```

All three keys (`protocolVersion`, `clientInfo`, `clientCapabilities`) are required. Skipping
any one returns `-32602 Invalid params: missing envelope key(s)`.

---

## Successful response shape (from `echo` probe)

```json
{
  "result": {
    "content": [
      {"type": "text", "text": "echo: hello"}
    ],
    "structuredContent": {"echoed": "hello"},
    "resultType": "complete",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "mcpjam-stateless",
        "version": "0.3.1"
      }
    }
  },
  "jsonrpc": "2.0",
  "id": 2
}
```

The `resultType: "complete"` field is the new MCP 2.0 requirement to distinguish
finished results from `input_required` (MRTR continuation).

---

## The "declare dead" trajectory (don't repeat)

This session's first probe concluded: *"endpoint is strict, probably empty, vendor demo."*
That verdict was based on 6 failed handshakes. The verdict was wrong because:

1. The 6 attempts didn't include the working `_meta` envelope
2. The session kept retrying broken shapes without escalating to the trajectory log
3. "Tools probably empty" assumed the server returned null tools — it was returning `-32600`
4. The trajectory of an OpenClaw agent cracking `echo` in 2 attempts was available
   in the conversation but not consulted

**Lesson:** when the same probe fails 3+ times with the same error class, the agent
should:
1. Query the trajectory log / sibling-agent output for prior attempts
2. Try the *exact* shape that another agent successfully used
3. Re-classify the endpoint (live-worked vs demo) before declaring dead

---

## Use as a federation probe target

Even though the tools are fixtures, the endpoint is the **conformance test rig** for the
federation. Wire it in MCPJam sidebar, then probe a federation organ against the same
handshake. If your agent can call `echo` on `stateless.mcpjam.com` but not call `arif_observe`
on `127.0.0.1:8088`, the problem is the organ, not the agent.

---

## Related

- §11 in SKILL.md for the pattern
- Blog: `blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate`
- Spec draft: `modelcontextprotocol.io/specification/draft`
- FORGE-mcp-probe — the class-level skill that uses this endpoint as reference
