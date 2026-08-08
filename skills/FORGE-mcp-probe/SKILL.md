---
id: FORGE-mcp-probe
name: FORGE-mcp-probe
version: 1.0.0
description: 'Probe any MCP server (local or HTTPS) using MCPJam CLI or SDK. Discover protocol version, tool/resource/prompt surface, OAuth conformance, and stateless transport (2026-07-28) support. Use this skill whenever an MCP server endpoint needs to be verified — whether it is the federation organs, a public HTTPS MCP server, or a third-party vendor endpoint.'
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F1, F2, F4, F11]
tags: [forge, mcp, probe, conformance, mcpjam, testing, ci]
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
- hermes
- openclaw
- agy
dependencies:
  servers: []
  tools:
    - forge_shell_dryrun
    - forge_filesystem_read
examples:
- "Probe the federation kernel at http://127.0.0.1:8088/mcp — what protocol version does it speak?"
- "Verify stateless MCP 2026-07-28 support against https://stateless.mcpjam.com/mcp"
- "Audit a third-party vendor MCP server before adding it to MCPJam sidebar"
- "Run conformance check across all federation organs in a single sweep"
tests:
- "Run the CLI against a known-good endpoint and confirm full tool list is returned"
- "Detect protocol version mismatch (e.g. client wants 2026-07-28, server is 2025-11-25)"
- "Produce JSON-RPC trace showing every request/response header + body"
- "Confirm OAuth flow is enabled or absent on a given server"
---

# ⚒️ FORGE-mcp-probe — MCP Conformance Testing Skill

> **Forged:** 2026-08-08 by 333-AGI for AAA Control Plane
> **Doctrine:** DITEMPA BUKAN DIBERI
> **Reference endpoint (the test rig):** `https://stateless.mcpjam.com/mcp`

## USE WHEN

The task involves:

- Validating that an MCP server speaks the expected protocol version (2025-03-26 / 2025-06-18 / 2025-11-25 / 2026-07-28)
- Discovering the full tool/resource/prompt surface of any MCP endpoint
- Auditing a third-party MCP server before wiring it into MCPJam sidebar or any agent
- Running stateless-transport conformance (the new 2026-07-28 wire format)
- OAuth conformance check (DCR, CIMD, pre-registration)
- CI gating: fail PR if the MCP server regresses on tool list or protocol version
- Cross-server sweep across all federation organs (arifOS, A-FORGE, AAA, GEOX, WEALTH, WELL)

## DO NOT USE WHEN

- The endpoint is not MCP (HTTP REST, GraphQL, gRPC) — wrong tool entirely
- The task is to BUILD an MCP server (use `forge_ephemeral` or the appropriate organ skill)
- The task is to call an MCP tool that you already trust (just call it)

## The Toolchain

MCPJam provides three layers. Use the right one for the task.

### Layer 1 — Web app (no install, free)

```
https://app.mcpjam.com
```

Paste the URL of any MCP server. Manual tool calling, OAuth flow debugging, full JSON-RPC trace. **HTTPS-only** — for local/HTTP servers use the CLI or Desktop.

### Layer 2 — CLI (terminal-first, CI-friendly)

```bash
# Probe a single endpoint
npx @mcpjam/inspector@latest https://stateless.mcpjam.com/mcp

# Probe the federation kernel
npx @mcpjam/inspector@latest http://127.0.0.1:8088/mcp

# Probe the bridge that A-FORGE exposes
npx @mcpjam/inspector@latest http://127.0.0.1:7072/mcp

# Doctor check (smoke + capability report)
npx @mcpjam/inspector@latest doctor http://127.0.0.1:8088/mcp

# OAuth conformance against a version
npx @mcpjam/inspector@latest oauth --version 2025-11-25 http://127.0.0.1:8088/mcp
```

After startup the CLI prints a localhost URL — open it in the browser for the same UI as `app.mcpjam.com` but pointed at your local server.

### Layer 3 — Docker (air-gap, fully local)

```bash
docker run -p 127.0.0.1:6274:6274 mcpjam/mcp-inspector
```

Binds 127.0.0.1 only (per `LOCALHOST_IS_PASSWORD` doctrine). For Docker → host server access on Mac/Win use `host.docker.internal:PORT`.

### Layer 4 — SDK (programmatic, for CI)

```bash
npm install @mcpjam/sdk
```

```typescript
import { MCPJamClient } from "@mcpjam/sdk";

const client = new MCPJamClient({ url: "https://stateless.mcpjam.com/mcp" });
const surface = await client.snapshot();
assert(surface.protocolVersion === "2026-07-28");
assert(surface.tools.length > 0);
```

Use in GitHub Actions to gate every PR on server conformance.

## The Canonical Reference: stateless.mcpjam.com/mcp

This is MCPJam's **own stateless MCP 2.0 reference server**. Every coding agent should:

1. Wire it as an MCP server in their config
2. Probe it once at boot to confirm their MCP client speaks 2026-07-28
3. Use it as the baseline when comparing any other MCP server

| Property | Value |
|---|---|
| URL | `https://stateless.mcpjam.com/mcp` |
| Protocol | `2026-07-28` only (stateless) |
| Server name | `mcpjam-stateless` |
| Server version | `0.3.1` |
| Auth | None |
| Tools | 13 (echo, get-weather, execute-sql, long-task, fail, ask-name, confirm-launch, open-dashboard, summarize, list-client-roots, never-satisfied, trigger-notifications, run-task) |
| Why it matters | Exercises every major 2026-07-28 feature: stateless transport, MRTR, progress streaming, sampling, Tasks extension |

### The handshake that works

```bash
curl -sS -X POST 'https://stateless.mcpjam.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/list' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }'
```

**Three rules** — every stateless MCP 2026-07-28 call needs ALL of these:
1. **`MCP-Protocol-Version: 2026-07-28`** header (not body `params.protocolVersion`)
2. **`Mcp-Method: <method>`** header for routing (load balancer can route on this)
3. **`_meta.io.modelcontextprotocol/*`** envelope keys (NOT `_meta.protocolVersion`)

If your MCP client only sends body `protocolVersion`, it will be rejected with `-32020 HeaderMismatch`.

## Federation Sweep Recipe

Run this in any AAA / Hermes / Kimi session to audit the whole federation at once:

```bash
for port in 8088 7071 7072 8081 18082 18083 3001; do
  echo "=== :$port ==="
  npx @mcpjam/inspector@latest doctor "http://127.0.0.1:$port/mcp" 2>&1 | head -30
done
```

Expected output (live as of 2026-08-08):

| Port | Organ | Status | Protocol |
|---|---|---|---|
| 8088 | arifOS | healthy | 2025-11-25 |
| 7071 | A-FORGE | healthy | (stateless_tools: 48) |
| 7072 | A-FORGE bridge | healthy | 2025-11-25 |
| 8081 | GEOX | healthy | 2025-11-25 |
| 18082 | WEALTH | degraded ⚠️ | 2025-11-25 |
| 18083 | WELL | healthy | 2025-11-25 |
| 3001 | AAA | healthy | 2025-11-25 |

The federation is mostly on `2025-11-25`. The **stateless.mcpjam.com endpoint is the only 2026-07-28 server** in your stack today. Use it to verify the agent's MCP client supports the new format before you upgrade any organ.

## Output Format

When this skill is invoked, the agent MUST return:

```
[OBS] MCP probe results for <endpoint>
- protocol_version: 2025-11-25 (or 2026-07-28)
- transport: stateful (Streamable-HTTP) | stateless
- tools: N (list: tool_a, tool_b, ...)
- resources: N
- prompts: N
- oauth: enabled | absent
- mrtr_support: yes | no | unknown
- tasks_extension: yes | no | unknown
- duration: X ms
- verdict: PASS | PARTIAL | FAIL
- next_action: <one concrete step>
```

A `verdict: PASS` means the server speaks the expected protocol and exposes the expected tools. `PARTIAL` means it works but with caveats (e.g. protocol mismatch, missing tools). `FAIL` means the probe could not establish a session or returned an error.

## Why This Skill Exists

Before this skill, agents probed MCP servers with ad-hoc curl scripts. That works for simple cases but breaks at:

- Protocol version negotiation (header vs body)
- Stateless transport (the new 2026-07-28 wire format)
- OAuth flow debugging
- Multi-round elicitation (MRTR)
- Tasks extension polling

MCPJam wraps all of this. **Use it. Don't reinvent the probe.**

## Pitfalls

- The CLI binds `127.0.0.1` for security — do NOT expose `6274` publicly
- For Docker on Mac/Win, use `host.docker.internal:PORT` not `127.0.0.1:PORT`
- The hosted web app (`app.mcpjam.com`) is HTTPS-only — for HTTP servers use CLI or Docker
- Don't trust a single probe — re-probe with a fresh session_id and confirm the result matches (Rule #7 from `frontier-model-audit-verification`: probe-to-witness)
- The `stateless.mcpjam.com/mcp` endpoint is reference-only — it has fixture tools (echo, fake weather), not real production capabilities
- MCPJam is **Apache 2.0**, free, and run by the same people who publish MCPJam Inspector — not a vendor lock-in

## Related

- `forge_ephemeral` — for building new MCP servers, not testing them
- `AUDIT-recursive-audit` — for federation-wide audits beyond MCP
- `kernel-security-claim-audit` — for verifying arifOS security claims
- `frontier-model-audit-verification` — Rule #7 probe-to-witness applies here too

---

*DITEMPA BUKAN DIBERI — Use the right tool, every time.*
