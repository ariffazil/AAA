---
name: "forge-mcp-testing"
description: "Use when testing any MCP server — protocol conformance validation via MCPJam Inspector, plus 2026-07-28 conformance matrix from live federation probe. How to test any MCP server — use MCPJam Inspector, not coding agents"
tags: [mcp, testing, conformance, mcpjam, protocol, 2026-07-28, stateless]
triggers:
  - "test MCP server"
  - "MCP conformance"
  - "protocol version check"
  - "MCPJam"
  - "MCP tools not working"
  - "stateless MCP"
  - "2026-07-28"
  - "OAuth MCP"
  - "MCP initialize"
---

# MCP Testing — MCPJam Inspector + 2026-07-28 Conformance

> For all AAA agents, OpenClaw, opencode, Kimi Code, Codex, Claude Code, AGY CLI, Copilot, Hermes
> Forged: 2026-08-08 | Hardened: 2026-09-17 | Authority: F13 SOVEREIGN

## Iron Rule

**MCP servers are tested with MCPJam Inspector, not with coding agents.**

Coding agents are for building. MCPJam is for testing. Different tools, different jobs.

## Why Not Coding Agents

- They speak legacy MCP (2024-11-05 initialize→session→call). You cannot test stateless MCP (2026-07-28) with them.
- They don't trace JSON-RPC messages. You can't see what went wrong.
- They don't run evals across multiple LLMs.
- They don't validate OAuth flow conformance.
- They don't give you schema inspection, output validation, or protocol compliance reports.

## What MCPJam Inspector Does

| Capability | What it gives you |
|---|---|
| **Debug** | Every JSON-RPC message traced, OAuth exchange visible |
| **Chat** | Talk to any LLM against your server, see every tool call |
| **Inspect** | Tools, resources, prompts — browsable, searchable |
| **Evaluate** | Test cases with expected tool calls, run across LLMs, track accuracy |
| **OAuth Debugger** | Guided conformance checks for all spec versions (03-26, 06-18, 11-25, 07-28) |
| **CLI** | `npx @mcpjam/inspector@latest` — probe, doctor, evals from terminal |
| **SDK** | Programmatic inspection, snapshot server capabilities |
| **CI/CD** | Wire into GitHub Actions — gate PRs on regressions |

## Our Deployment

```
Container: mcpjam-federation (Docker, mcpjam/mcp-inspector:latest)
Status: Up, healthy
Ports:
  127.0.0.1:6274      → localhost (SSH tunnel)
  100.64.0.2:6274      → Tailscale mesh
  127.0.0.1:6277       → dev server, localhost only
Config: /opt/mcpjam/docker-compose.yaml
Data:   /opt/mcpjam/data
```

## Federation Organ URLs

| Organ | URL |
|---|---|
| arifOS | `http://localhost:8088/mcp` |
| A-FORGE | `http://localhost:7072/mcp` |
| GEOX | `http://localhost:8081/mcp/` |
| WEALTH | `http://localhost:18082/mcp` |
| WELL | `http://localhost:18083/mcp` |
| SIGNAL | `http://localhost:18084/mcp` |
| FRAME | `http://localhost:18085/mcp` |

## 2026-07-28 Conformance Test Matrix

From live federation probe 2026-09-17. Use this as the checklist when validating any MCP server against the latest spec.

| # | Feature | Spec Requirement | How to Test | Pass Criteria |
|---|---|---|---|---|
| C1 | Protocol version in initialize | MUST advertise 2026-07-28 | `curl POST :port/mcp initialize` with `protocolVersion: "2026-07-28"` | Response `result.protocolVersion == "2026-07-28"` |
| C2 | Stateless transport | MUST work without session persistence | Send tools/call WITHOUT `MCP-Session-Id` header | Tool executes, no session error |
| C3 | `resultType` injection | MUST inject on list responses | `tools/list` → check `_meta.resultType` | `resultType: "complete"` present |
| C4 | Tasks capability | SHOULD declare if long-running work supported | Check `capabilities.tasks` in initialize response | Present if server supports |
| C5 | UI extensions | SHOULD declare if UI extensions supported | Check `capabilities.extensions.ui` | Present if server supports |
| C6 | `input_required` resultType | MUST exist for MRTR (Model-Responsive Task Routing) | Send a tool call that should HOLD; check resultType | `resultType: "input_required"` (NOT just `complete`) |
| C7 | Public discovery | SHOULD publish `/.well-known/mcp/server.json` | `curl :port/.well-known/mcp/server.json` | JSON with correct protocolVersion |
| C8 | OAuth PRM | SHOULD publish `/.well-known/oauth-protected-resource` | `curl :port/.well-known/oauth-protected-resource` | JSON with resource metadata |
| C9 | RFC 9207 audience | SHOULD bind audience claim | Check JWT/DPoP for `aud` claim | `aud` matches server identity |
| C10 | Bearer + DPoP | MUST enforce if configured | Send request with/without DPoP proof | Reject without, accept with |
| C11 | JSON Schema 2020-12 | SHOULD use for tool schemas | Check tool inputSchema `$schema` field | Points to json-schema.org |
| C12 | Canonical tool order | SHOULD return tools in canonical order | `tools/list` → check ordering | Consistent order across calls |

### Quick Conformance Probe

```bash
# Full conformance probe for any MCP server
PORT=${1:-8088}
echo "=== C1: Protocol version ==="
curl -sS -X POST "http://localhost:$PORT/mcp" \
  -H 'Content-Type: application/json' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2026-07-28","capabilities":{},"clientInfo":{"name":"conformance","version":"1"}}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('PASS' if d.get('result',{}).get('protocolVersion','')=='2026-07-28' else 'FAIL:', d.get('result',{}).get('protocolVersion','MISSING'))"

echo "=== C2: Stateless transport ==="
curl -sS -X POST "http://localhost:$PORT/mcp" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('PASS: tools=' + str(len(d.get('result',{}).get('tools',[]))))" 2>/dev/null || echo "FAIL: needs session"

echo "=== C3: resultType injection ==="
curl -sS -X POST "http://localhost:$PORT/mcp" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/list","params":{}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); m=d.get('result',{}).get('_meta',{}); print('PASS' if 'resultType' in m else 'FAIL:', m)" 2>/dev/null || echo "FAIL: no _meta"

echo "=== C7: Public discovery ==="
curl -sS "http://localhost:$PORT/.well-known/mcp/server.json" 2>/dev/null \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('PASS: version=' + d.get('protocolVersion','MISSING'))" 2>/dev/null || echo "FAIL: no discovery endpoint"

echo "=== C8: OAuth PRM ==="
curl -sS "http://localhost:$PORT/.well-known/oauth-protected-resource" 2>/dev/null \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('PASS: PRM present')" 2>/dev/null || echo "FAIL: no PRM endpoint (F13 HOLD for auth surface)"
```

## Known Federation Conformance State (2026-09-17)

| Organ | C1 | C2 | C3 | C6 | C7 | C8 | Notes |
|---|---|---|---|---|---|---|---|
| arifOS :8088 | ✅ | ✅ | ✅ | ❌ missing | ❌ F13 HOLD | Drift honest, kernel truth |
| WEALTH :18082 | ✅ | ✅ | — | — | — | — | |
| WELL :18083 | ❌ 2025-11-25 | ? | — | — | — | Laggard, manifest bumped |
| A-FORGE :7072 | (A2A) | ✅ 87 stateless | — | — | — | 121 tools |

## Feeding an Organ Into Inspector

1. Open `http://127.0.0.1:6274`
2. Click "Add MCP Server"
3. Enter URL: `http://localhost:8088/mcp` (for arifOS) or respective organ port
4. Inspector connects, lists all tools/resources/prompts
5. Manually run tools, chat with LLM, trace every message

## CLI Quick Reference

```bash
# Health probe
npx @mcpjam/inspector doctor http://localhost:8088/mcp

# List tools
npx @mcpjam/inspector tools http://localhost:8088/mcp

# Run evals
npx @mcpjam/inspector eval --server http://localhost:8088/mcp --suite /root/A-FORGE/evals/mcp/

# OAuth conformance
npx @mcpjam/inspector oauth http://localhost:8088/mcp --spec 07-28

# Stateless MCP compliance endpoint
curl -sS -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/list' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28"}}}'
```

## Stdout Purity Check

A stdio MCP server that prints ANY human text to stdout corrupts the JSON-RPC stream.

```bash
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"purity","version":"1"}}}' \
  | node /path/to/server.js serve --transport stdio 2>/dev/null | head -5
# Every line must be valid JSON. Any banner/prose = fix in source.
```

- Fix the SOURCE, then the artifact. `console.log` → `console.error` in TS/JS source AND built `dist/`.
- Do not run full rebuild for one-line banner fix when tree has in-flight source.
- Receipt: restart consumer, count Traceback lines. 0 = pass.

## When to Use

- Before deploying an organ — feed to inspector, verify schemas
- After changing tool signatures — check for breakage in inspector chat
- When debugging a failure — inspector trace shows exact JSON-RPC
- CI runs — wire `mcpjam doctor` into GitHub Actions pre-merge
- **Validating 2026-07-28 conformance** — use the 12-point matrix above

## When NOT to Use

- Building features — use coding agents
- Production workloads — inspector is a test tool
- Federation health monitoring — use HEARTBEAT.md cron jobs
