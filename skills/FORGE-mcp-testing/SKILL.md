---
name: "forge-mcp-testing"
description: "How to test any MCP server — use MCPJam Inspector, not coding agents"
---

# MCP Testing — MCPJam Inspector

> **For all AAA agents, OpenClaw, opencode, Kimi Code, Codex, Claude Code, AGY CLI, Copilot, Hermes**
> Forged: 2026-08-08 | Domain: forge | Authority: F13 SOVEREIGN

## Iron Rule

**MCP servers are tested with MCPJam Inspector, not with coding agents.**

Coding agents (Claude Code, opencode, Kimi Code, AGY, Copilot, OpenClaw) are for **building** MCP servers. MCPJam is for **testing** them. Different tools, different jobs.

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
| **OAuth Debugger** | Guided conformance checks for all spec versions (03-26, 06-18, 11-25) |
| **CLI** | `npx @mcpjam/inspector@latest` — probe, doctor, evals from terminal |
| **SDK** | Programmatic inspection, snapshot server capabilities |
| **CI/CD** | Wire into GitHub Actions — gate PRs on regressions |

## Our Deployment

```
Container: mcpjam-federation (Docker, mcpjam/mcp-inspector:latest)
Status: Up, healthy
Ports:
  127.0.0.1:6274      → localhost (SSH tunnel)
  100.64.0.2:6274      → Tailscale mesh (Arif's Windows client)
  127.0.0.1:6277       → dev server, localhost only
Config: /opt/mcpjam/docker-compose.yaml
Data:   /opt/mcpjam/data
```

**Access:** `http://127.0.0.1:6274` (local) or `http://100.64.0.2:6274` (Tailscale)

## Feeding an Organ Into Inspector

1. Open `http://127.0.0.1:6274`
2. Click "Add MCP Server"
3. Enter URL: `http://localhost:8088/mcp` (for arifOS) or respective organ port
4. Inspector connects, lists all tools/resources/prompts
5. You can now: manually run tools, chat with LLM against it, trace every message

### Federation Organ URLs

| Organ | URL |
|---|---|
| arifOS | `http://localhost:8088/mcp` |
| A-FORGE | `http://localhost:7072/mcp` |
| GEOX | `http://localhost:8081/mcp/` |
| WEALTH | `http://localhost:18082/mcp` |
| WELL | `http://localhost:18083/mcp` |
| SIGNAL | `http://localhost:18084/mcp` |
| FRAME | `http://localhost:18085/mcp` |

## CLI Quick Reference

```bash
# Health probe
npx @mcpjam/inspector doctor http://localhost:8088/mcp

# List tools
npx @mcpjam/inspector tools http://localhost:8088/mcp

# Run evals
npx @mcpjam/inspector eval --server http://localhost:8088/mcp --suite /root/A-FORGE/evals/mcp/

# OAuth conformance
npx @mcpjam/inspector oauth http://localhost:8088/mcp --spec 03-26
```

## When to Use

- **Before deploying** an organ — feed it to inspector, run tools manually, verify schemas
- **After changing tool signatures** — check for breakage in inspector chat
- **When debugging a failure** — inspector trace shows the exact JSON-RPC that went wrong
- **CI runs** — wire `mcpjam doctor` into GitHub Actions pre-merge

## When NOT to Use

- To build features — use coding agents (Claude Code, opencode, Kimi Code)
- To run production workloads — inspector is a test tool
- As a replacement for federation health monitoring — use HEARTBEAT.md cron jobs

## Docker Management

```bash
# Check status
docker ps --filter name=mcpjam

# Restart
docker restart mcpjam-federation

# Update
docker pull mcpjam/mcp-inspector:latest && docker restart mcpjam-federation

# Logs
docker logs mcpjam-federation --tail 50
```

## Stateless MCP Note

MCPJam also hosts `stateless.mcpjam.com/mcp` — a stateless MCP compliance server (protocol 2026-07-28). If a coding agent can talk to that endpoint, it supports stateless MCP. Currently, **none of our agents do**. This is expected — the spec is new and SDK-level support is still emerging. Use `curl` with the stateless envelope to probe it directly:

```bash
curl -sS -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/list' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
```
