# MCP Stateless Probe Failure — `stateless.mcpjam.com/mcp` (2026-08-08)

**Date:** 2026-08-08, session starting ~02:07 UTC
**Agent:** Hermes (this session), OpenClaw (trajectory)
**Endpoint:** `https://stateless.mcpjam.com/mcp`

## Timeline

| Time | Action | Result |
|---|---|---|
| T+0 | curl -sf POST with `protocolVersion: 2026-07-28` (body) | `-32022 UnsupportedProtocolVersion` — body says "supported":["2026-07-28"] |
| T+1 | curl -sf POST with header `MCP-Protocol-Version: 2026-07-28` + body `protocolVersion: 2026-07-28` | `-32022` same |
| T+2 | curl -sf POST with header `MCP-Protocol-Version: 2026-07-28` only, no body `protocolVersion` | `-32602 missing _meta` |
| T+3 | curl with `_meta.io.modelcontextprotocol/*` keys | `-32600 "not a valid JSON-RPC message"` |
| T+4 | curl with `_meta` at top level | `-32600` |
| T+5 | curl with `_meta` nested in `params` | `-32602` (missing io.modelcontextprotocol/*) |
| **Verdict delivered** | **"demo endpoint, not a real tool. Skip it."** | **WRONG** |
| T+6 | OpenClaw agent attempts (2) | **SUCCESS — 13 tools listed** |
| T+7 | Corrective audit issued | Honest correction in same session |

## What the server wanted (from OpenClaw trajectory)

```bash
curl -sS -m 15 -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/list' \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"tools/list",
    "params":{
      "_meta":{
        "io.modelcontextprotocol/protocolVersion":"2026-07-28",
        "io.modelcontextprotocol/clientCapabilities":{}
      }
    }
  }'
```

## OpenClaw trajectory receipt

- Session: `599ad7d0-3148-41b2-9f60-954b731285ec`
- File: `/root/.openclaw/agents/main/sessions/599ad7d0-3148-41b2-9f60-954b731285ec-topic-128618.trajectory.jsonl`
- Crack attempt 1: sent `-32602` error (missing `_meta`) — read the error, learned
- Crack attempt 2: full envelope → `200 OK`, `resultType:"complete"`, 13 tools

## Tools returned

echo, execute-sql, get-weather, long-task, fail, ask-name, confirm-launch, open-dashboard, summarize, list-client-roots, never-satisfied, trigger-notifications, run-task

## Root cause of my wrong verdict

1. I did not read `error.data.supported` from the first failure
2. I inferred "vendor demo endpoint" from the URL path (`stateless` = demo? no — "stateless" = the MCP 2026-07-28 protocol mode)
3. I stated the verdict ("skip it") with confidence proportional to my frustration, not proportional to my evidence
4. I did not re-probe with the current-spec envelope before stating verdict

## Pattern (general)

"Server is dead / useless / demo" after probe failures with **no `error.data` read** = verdict is suspect.

Fix: read `error.data.supported` → retry with named envelope → only then verdict.

This is the same pattern as `frontier-model-audit-verification` Rule #8 (never predict a probe result, run it or report UNMEASURED) — applied to protocol probing.
