---
name: openclaw-a2a-client-options
description: Three options to wire OpenClaw to an external A2A endpoint (AAA gateway on port 3001), with recommendation for Option 2 (thin MCP A2A client)
---

# openclaw-a2a-client-options

## Context
OpenClaw's A2A support is designed for:
1. **Inbound A2A servers** — the WebSocket protocol OpenClaw exposes
2. **ACP harnesses** — Claude Code, Gemini CLI, etc. that use the ACP protocol

OpenClaw does **NOT** have a native A2A client config for arbitrary HTTP A2A endpoints like the AAA gateway on port 3001.

## Three Options

### Option 1 — Custom Skill with exec/curl
Create an OpenClaw skill that wraps `curl` to call the A2A `tasks/send` endpoint.

```bash
curl -s -X POST http://127.0.0.1:3001/tasks \
  -H "Authorization: Bearer aaa-a2a-token-dev" \
  -H "x-a2a-key: aaa-a2a-apikey-dev" \
  -H "Content-Type: application/json" \
  -d '{"method":"tasks/send","params":{"taskId":"...","message":{...}}}'
```

**Drawback:** Tokens in skill code, no tool discovery, no structured responses.

### Option 2 — Thin MCP A2A Client Server (RECOMMENDED)
Build a minimal FastMCP server that wraps the AAA gateway A2A endpoints and exposes them as native MCP tools.

```
a2a_client_mcp/
  server.py          # FastMCP, exposes a2a_send_task, a2a_get_task, a2a_cancel_task
  pyproject.toml
  Dockerfile
```

Register in OpenClaw:
```json
"mcp": {
  "servers": {
    "a2a-client": {
      "command": "uvx",
      "args": ["a2a-client-mcp"]
    }
  }
}
```

**Benefits:**
- Native `a2a_send_task` tool callable from any OpenClaw session
- Auth managed in MCP server config (no hardcoded tokens in skills)
- Consistent with how arifOS, GEOX, WELL are already wired
- Easy to extend with `a2a_get_task`, `a2a_cancel_task`

### Option 3 — Extend AAA A2A Server with MCP Transport
Add an MCP transport layer to the existing AAA gateway (Node.js/Express).

**Drawback:** Couples A2A server and MCP transport concerns in the same service. Option 2 keeps them separate.

## Recommendation
**Option 2** — thin MCP A2A client. Cleanest long-term path. Aligns with existing arifOS federation pattern.

## Auth Tokens (dev)
- Bearer: `aaa-a2a-token-dev`
- x-a2a-key: `aaa-a2a-apikey-dev`
- Target: `http://127.0.0.1:3001/tasks`