---
name: "forge-mcp-testing"
description: "How to test any MCP server — use MCPJam Inspector, not coding agents"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# MCP Testing — MCPJam Inspector

> **For all AAA agents, OpenClaw, opencode, Kimi Code, Codex, Claude Code, AGY CLI, Copilot, Hermes, Grok**
> Forged: 2026-08-08 | Re-wired: 2026-08-09 | Domain: forge | Authority: F13 SOVEREIGN
> Upstream: https://github.com/MCPJam/inspector

## Iron Rule

**MCP servers are tested with MCPJam Inspector, not with coding agents.**

Coding agents (Claude Code, opencode, Kimi Code, AGY, Copilot, OpenClaw, Grok, Hermes) are for **building** MCP servers. MCPJam is for **testing** them. Different tools, different jobs.

Companion skill: **`FORGE-mcp-probe`** (CLI/SDK doctor + conformance). Load both when verifying an endpoint.

## Agent wiring (AAA catalog → harness views)

| Harness | Skill home | `FORGE-mcp-testing` | `FORGE-mcp-probe` |
|---|---|---|---|
| Grok | `~/.grok/skills` | symlink → AAA | symlink → AAA |
| Claude Code | `~/.claude/skills` | symlink → AAA | symlink → AAA |
| Codex | `~/.codex/skills` | symlink → AAA | symlink → AAA |
| OpenCode | `~/.arifos/agents/opencode/skills` + `~/.config/opencode/skills` | linked / copy | linked / copy |
| Hermes | `~/HERMES/skills` + `~/.hermes/skills` | copy (mesh) | copy (mesh) |
| Kimi Code | `~/.kimi-code/skills` | copy (mesh) | copy (mesh) |
| OpenClaw | `~/.openclaw/workspace/skills/{forge-mcp-*,FORGE-mcp-*}` | copy | copy |

Canon body: `/root/AAA/skills/FORGE-mcp-testing/`. After editing canon, re-copy hermes/kimi/openclaw (mesh-sync does not touch those trees).

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
Network:   host (required — organs bind 127.0.0.1; bridge cannot reach loopback)
Listen:    0.0.0.0:6274 inside host-net container (image DOCKER_CONTAINER=true)
Public:    UFW DENY on public NIC for 6274 — never Caddy/Cloudflare
Access:
  http://127.0.0.1:6274      → localhost / SSH tunnel
  http://100.64.0.2:6274      → Tailscale (Arif Windows)
Config: /opt/mcpjam/docker-compose.yaml
Data:   /opt/mcpjam/data
Seed:   /opt/mcpjam/data/federation-organs.json
Env:    /opt/mcpjam/.env (MCPJAM_* only — synced from KUNCI-MAS)
```

## Hosted API key (`sk_…`)

Docs: https://docs.mcpjam.com/reference/api-keys · https://docs.mcpjam.com/

| Item | Location |
|------|----------|
| Secret | `MCPJAM_API_KEY` in `/root/.secrets/kunci-mas.env` (mode 600) |
| Runtime env | `/opt/mcpjam/.env` (narrow — never mount full vault) |
| Sync | `/opt/mcpjam/sync-env-from-vault.sh` then `docker compose up -d` |
| Load in shell | `source /opt/mcpjam/env.sh` or `source /root/.secrets/kunci-mas.env` |
| API base | `https://app.mcpjam.com/api/v1` (`MCPJAM_API_BASE`) |
| Default project | `MCPJAM_PROJECT_ID` (hosted "Default") |

```bash
# Auth check (do not print the key)
source /opt/mcpjam/env.sh
curl -sS -H "Authorization: Bearer $MCPJAM_API_KEY" \
  "$MCPJAM_API_BASE/me" | jq '{id,email,name,plan}'
```

Local organ doctor (no key needed against localhost MCP): open the Inspector UI or use CLI `server doctor --url http://127.0.0.1:8088/mcp`.  
Hosted project ops / eval save / hosts / environments need `MCPJAM_API_KEY`.
## Feeding an Organ Into Inspector

1. Open `http://127.0.0.1:6274` (or Tailscale URL from Windows)
2. Click "Add MCP Server"
3. Enter URL from table below (prefer `127.0.0.1` when on host)
4. Inspector connects, lists tools/resources/prompts
5. Manually run tools, chat against it, trace every JSON-RPC message

### Federation Organ URLs (host-net; server-side probe)

| Organ | URL | Casual test? |
|---|---|---|
| arifOS | `http://127.0.0.1:8088/mcp` | yes (JUDGE_ONLY) |
| GEOX | `http://127.0.0.1:8081/mcp/` | yes (COMPUTE_ONLY) |
| WEALTH | `http://127.0.0.1:18082/mcp` | yes (COMPUTE_ONLY) |
| WELL | `http://127.0.0.1:18083/mcp` | yes (REFLECT_ONLY) |
| A-FORGE | `http://127.0.0.1:7072/mcp` | **no** — mutation surface; exclude casual |
| stateless ref | `https://stateless.mcpjam.com/mcp` | yes — protocol 2026-07-28 fixture |

## CLI Quick Reference

```bash
# UI already running on :6274 — do not start a second npx instance on same port
# From a free shell (stop container first if you need ephemeral CLI on 6274):
npx @mcpjam/inspector@latest doctor http://127.0.0.1:8088/mcp
npx @mcpjam/inspector@latest tools http://127.0.0.1:8088/mcp
npx @mcpjam/inspector@latest oauth http://127.0.0.1:8088/mcp --spec 03-26
```

## When to Use

- **Before deploying** an organ — feed it to inspector, run tools manually, verify schemas
- **After changing tool signatures** — check for breakage in inspector chat
- **When debugging a failure** — inspector trace shows the exact JSON-RPC that went wrong
- **CI runs** — wire `mcpjam doctor` into GitHub Actions pre-merge

## When NOT to Use

- To build features — use coding agents (Claude Code, opencode, Kimi Code)
- To run production workloads — inspector is a test tool
- As a replacement for federation health monitoring — use HEARTBEAT.md / doctor.sh

## Docker Management

```bash
docker ps --filter name=mcpjam
docker restart mcpjam-federation
docker pull mcpjam/mcp-inspector:latest && cd /opt/mcpjam && docker compose up -d
docker logs mcpjam-federation --tail 50
# verify Path A access (not public)
curl -sf -o /dev/null -w 'local=%{http_code}\n' http://127.0.0.1:6274/
curl -sf -o /dev/null -w 'ts=%{http_code}\n' http://100.64.0.2:6274/
ufw status | grep 6274   # expect DENY on public NIC
```

## Stateless MCP Note

MCPJam hosts `stateless.mcpjam.com/mcp` — a stateless MCP compliance server (protocol 2026-07-28). If a coding agent can talk to that endpoint, it supports stateless MCP. Use it as a reference rig, not production.

```bash
curl -sS -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/list' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
```
