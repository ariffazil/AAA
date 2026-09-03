# Agent Landscape Audit — 2026-05-17

> **Source:** This file is produced by a live federation runtime audit session.
> Do not treat as authoritative — re-audit periodically, especially after config changes.

## Architecture Claim Under Review

> "OpenClaw → Hermes for deep constitutional reasoning. OpenClaw connects to arifOS MCP. Hermes is the constitutional backstop."

## Actual Runtime State (2026-05-17 UTC ~02:20–02:30)

### Process Map

| PID | Process | Role |
|-----|---------|------|
| 972480 | `openclaw` (Node.js) | Telegram bot gateway — @AGI_ASI_bot, port 18789 |
| 966974 | `hermes-agent gateway` (Python) | Hermes gateway — @ASI_arifos_bot |
| 5210 | `python3` (openclaw-a2a.py) | OpenClaw A2A adapter, port 18002 |
| 1036 | `python3` (hermes-a2a.py) | Hermes A2A adapter, port 18001 |

**Critical finding:** Two separate Python A2A adapters running independently, NOT a chain.

### Telegram Bot Tokens

| Bot | Token prefix | Port |
|-----|-------------|------|
| @AGI_ASI_bot (OpenClaw) | `8149595687:***` | 18789 |
| @ASI_arifos_bot (Hermes) | `841013...19DA` | 18001 → 3001 |

### MCP Configuration (openclaw.json)

```json
"mcp": {
  "servers": {
    "arifos": { "url": "http://127.0.0.1:8080/mcp", "transport": "streamable-http" },
    "geox":   { "url": "http://127.0.0.1:8081/mcp" },
    "well":   { "url": "http://127.0.0.1:8083/mcp" },
    "wealth": { "url": "http://127.0.0.1:8082/mcp" }
  }
}
```

arifOS MCP is **present in config** — contrary to a stale report of `mcpServers: {}`.

### Connectivity Tests

```bash
# Node.js fetch FROM host — WORKS
node -e "fetch('http://127.0.0.1:8080/mcp').then(r=>r.text()).then(d=>console.log(d.slice(0,100)))"
// → OK: {"service":"arifOS AAA MCP Server","version":"v2026.05.05-SSCT"...

# arifOS MCP endpoint
curl http://127.0.0.1:8080/mcp
// → {"service":"arifOS AAA MCP Server","tool_count":13} — 200 OK
```

Node.js `fetch()` on the host can reach `127.0.0.1:8080`. The "TypeError: fetch failed" error seen in some agent reports was a **stale observation**, not current state.

### Docker Network

arifOS MCP container (`arifosmcp`) runs in `arifos_core_network`. Port 8080 is mapped to `127.0.0.1:8080` on the host.

---

## Verdict on Architecture Claims

### Claim: "OpenClaw → Hermes for deliberation" — ❌ WRONG

**Reality:** Two independent Telegram bots on separate tokens. Both call the same OpenClaw gateway for inference. No delegation chain exists.

```
@AGI_ASI_bot  → OpenClaw gateway (18789) → model
@ASI_arifos_bot → hermes-a2a.py (18001) → AAA Gateway (3001) → OpenClaw gateway (18789) → model
```

### Claim: "OpenClaw connects to arifOS MCP" — ✅ CONFIRMED (configured)

arifOS, GEOX, WEALTH, WELL all configured as MCP servers in openclaw.json. Endpoint is reachable.

### Claim: "Hermes is the constitutional backstop" — ❌ MISLEADING

arifOS MCP is the constitutional backstop (F1-F13 floors live there). Hermes is a Telegram relay + A2A bridge. Constitutional reasoning fires only when MCP tools are actually invoked — routine chat bypasses it.

### Claim: "arifOS MCP has 13 tools" — ✅ CONFIRMED

`curl http://127.0.0.1:8080/mcp` returns `tool_count: 13`. Full tool schema available at `POST http://127.0.0.1:8080/mcp` with `tools/list` method.

---

## Key Lesson: Cross-Check Before Accepting

**A single agent's report can be stale.** One agent reported `mcpServers: {}` and `bundle-mcp failed: TypeError: fetch failed`. Independent verification showed:

- `mcpServers` was populated
- Node.js fetch to 127.0.0.1:8080 succeeded

When validating architecture claims, always run your own probes:
```bash
curl -s http://127.0.0.1:8080/mcp
node -e "fetch('http://127.0.0.1:8080/mcp').then(r=>r.text()).then(console.log)"
docker ps --format "{{.Names}}\t{{.Status}}"
```

---

## The MCP Invocation Gap

MCP tools are **configured** but not necessarily **invoked** on every message.

| Message Type | What Happens |
|---|---|
| Routine Telegram DM | Model inference only. No F1-F13 floors. |
| Tool-invoked message | arifOS MCP tool called → constitutional floors enforced |
| A2A delegation | Hermes spawns subagent (delegate_task) → real shell command executed |

To make constitutional floors run on every message, OpenClaw would need to call arifOS MCP tools proactively — currently it only does so when explicitly triggered.

---

## Known Issues

### Telegram sendChatAction failures
```
telegram sendChatAction failed: Network request for 'sendChatAction' failed!
```
Recurs every ~3 seconds in OpenClaw logs. Secondary failure — the bot still responds to DMs. Likely a network/firewall issue with Telegram API from the VPS. Does not block primary function.

---

*Audit completed by OpenCode (Hermes subagent) during federation validation session.*