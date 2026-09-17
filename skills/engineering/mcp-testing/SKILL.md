---
name: mcp-testing
description: >
  Unified MCP server testing, probing, and conformance validation. Covers MCPJam Inspector methodology
  for deep conformance testing, MCPJam CLI/SDK probing for protocol version and stateless transport
  discovery, and quick smoke tests for federation organ health. Merges: FORGE-mcp-smoke-test,
  FORGE-mcp-probe, FORGE-mcp-testing.
id: mcp-testing
version: 2.0.0
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F11]
autonomy_tier: T1
tags: [mcp, testing, probe, conformance, mcpjam, smoke-test, ci, protocol, stateless]
capability_tier: fed-agent-subagent
ecology_state: WARM
supersedes:
  - FORGE-mcp-smoke-test
  - FORGE-mcp-probe
  - FORGE-mcp-testing
triggers:
  - "MCP test"
  - "MCP probe"
  - "MCP conformance"
  - "MCP smoke test"
  - "MCP server test"
  - "MCPJam Inspector"
  - "MCPJam"
  - "MCP protocol version"
  - "stateless MCP"
  - "MCP 2026-07-28"
  - "MCP server validation"
  - "MCP health check"
  - "MCP schema validation"
  - "MCP OAuth conformance"
  - "MCP transport test"
  - "MCP CI gate"
  - "MCPChatGPT conformance"
  - "MCP-App surface"
---

# MCP Testing

> **Iron Rule: MCP servers are tested with MCPJam Inspector, not with coding agents.**
> Coding agents are for **building** MCP servers. MCPJam is for **testing** them.
> *DITEMPA BUKAN DIBERI — Use the right tool, every time.*

## Overview

Unified MCP testing covering three domains:
1. **Smoke Test** — Quick health + schema sanity of federation-owned MCP servers (our 6 organs). Fast gate, not deep conformance.
2. **Probe** — MCPJam CLI/SDK probing of ANY endpoint (incl. external/unknown) for protocol version, surface discovery, stateless-transport conformance.
3. **Testing** — MCPJam Inspector methodology for deep conformance testing, tool-call verification, OAuth debugging.

### When to Use Which

| Situation | Use |
|-----------|-----|
| Quick organ health check (our 6 organs) | Smoke test |
| Protocol-era / stateless discovery on any endpoint | Probe |
| Deep conformance, tool-call verification, OAuth debugging | Testing (MCPJam Inspector) |
| CI gating on PRs | Probe (SDK) or Testing (Inspector evals) |

---

## Section 1: Smoke Test — Quick Federation Health

Validate that MCP servers respond correctly to health probes and basic tool calls. Detect down servers, mismatched schemas, and transport errors.

### Targets

- arifOS :8088
- A-FORGE :7071
- GEOX :8081
- WEALTH :18082
- WELL :18083

### ChatGPT/MCP-Apps Conformance Matrix

App-surface extension of the generic smoke test, for servers exposing MCP-App (`ui://`) surfaces. Authoritative contract: the sovereign GEOX blueprint at `/root/forge_work/2026-07-20/GEOX-CHATGPT-MCP-GUI-BLUEPRINT.md` (contracts #2, #4, #8, #9, #10). The generic health/smoke layers remain the floor; a server that advertises `_meta.ui.resourceUri` on any tool passes only when all five layers below also pass.

#### Layer A — Deterministic boot-contract invariants (blueprint #2)

The server must fail startup if a UI-bound tool references a `ui://` resource that `resources/read` cannot serve; the smoke test asserts the same at runtime:

1. `tools/list` names == canonical app registry.
2. `resources/list` covers every `ui://` URI referenced by any tool's `_meta.ui.resourceUri`.
3. `resources/read` on each of those URIs returns MIME `text/html;profile=mcp-app`.

Compact pytest example (raw JSON-RPC over the MCP endpoint):

```python
import httpx

MCP_URL = "http://localhost:8081/mcp"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
UI_MIME = "text/html;profile=mcp-app"

def rpc(method: str, params: dict | None = None) -> dict:
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    resp = httpx.post(MCP_URL, json=body, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()["result"]

def test_boot_contract(registry_tool_names: set[str]):
    tools = rpc("tools/list")["tools"]
    assert {t["name"] for t in tools} == registry_tool_names
    bound = {
        t["_meta"]["ui"]["resourceUri"]
        for t in tools
        if t.get("_meta", {}).get("ui", {}).get("resourceUri")
    }
    listed = {r["uri"] for r in rpc("resources/list")["resources"]}
    assert bound <= listed
    for uri in bound:
        contents = rpc("resources/read", {"uri": uri})["contents"]
        assert any(c["mimeType"] == UI_MIME for c in contents), uri
```

#### Layer B — structuredContent vs outputSchema (blueprint #4)

On `tools/call` happy path, every tool returning `structuredContent` must declare an `outputSchema` from the pinned families and the returned `structuredContent` must validate against it (jsonschema). Smoke must also reject secrets, trace IDs, and dense arrays in `structuredContent`.

#### Layer C — Error surface (blueprint #9)

Tool-originated failures return `CallToolResult` with `isError: true` so the model can self-corrupt — never a protocol crash. Smoke: trigger a known-bad input on a protected tool and assert `isError: true` with no JSON-RPC error envelope and no transport failure.

#### Layer D — Auth matrix (blueprint #8)

OAuth 2.1 resource server with RFC 9728 protected-resource metadata. Smoke asserts:
- Unauthenticated call to a protected tool → 401 with valid `WWW-Authenticate` header.
- Wrong-audience token → hard 401.
- Expired token → hard 401.
- Missing scope → fail closed (401/403), never a silent success.

#### Layer E — Host-surface evidence gates (blueprint #10)

Submission-path gates, in order:
1. Developer Mode golden prompts — direct, indirect, and negative prompt sets all pass.
2. API Playground — raw JSON-RPC log check confirms expected exchange.
3. Web + Android + iOS — render, resize, and state-persistence evidence captured per surface.

---

## Section 2: Probe — MCPJam CLI/SDK Conformance

Probe any MCP server (local or HTTPS) using MCPJam CLI or SDK. Discover protocol version, tool/resource/prompt surface, OAuth conformance, and stateless transport support.

### The Toolchain

#### Layer 1 — Web app (no install, free)
```
https://app.mcpjam.com
```
Paste the URL of any MCP server. Manual tool calling, OAuth flow debugging, full JSON-RPC trace. **HTTPS-only** — for local/HTTP servers use the CLI or Desktop.

#### Layer 2 — CLI (terminal-first, CI-friendly)
```bash
# Probe a single endpoint
npx @mcpjam/inspector@latest https://stateless.mcpjam.com/mcp

# Probe the federation kernel
npx @mcpjam/inspector@latest http://127.0.0.1:8088/mcp

# Doctor check (smoke + capability report)
npx @mcpjam/inspector@latest doctor http://127.0.0.1:8088/mcp

# OAuth conformance against a version
npx @mcpjam/inspector@latest oauth --version 2025-11-25 http://127.0.0.1:8088/mcp
```

#### Layer 3 — Docker (air-gap, fully local)
```bash
docker run -p 127.0.0.1:6274:6274 mcpjam/mcp-inspector
```
Binds 127.0.0.1 only (per `LOCALHOST_IS_PASSWORD` doctrine).

#### Layer 4 — SDK (programmatic, for CI)
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

### The Canonical Reference: stateless.mcpjam.com/mcp

MCPJam's own stateless MCP 2.0 reference server. Every coding agent should:
1. Wire it as an MCP server in their config.
2. Probe it once at boot to confirm their MCP client speaks 2026-07-28.
3. Use it as the baseline when comparing any other MCP server.

| Property | Value |
|---|---|
| URL | `https://stateless.mcpjam.com/mcp` |
| Protocol | `2026-07-28` only (stateless) |
| Server name | `mcpjam-stateless` |
| Server version | `0.3.1` |
| Auth | None |
| Tools | 13 (echo, get-weather, execute-sql, long-task, fail, ask-name, confirm-launch, open-dashboard, summarize, list-client-roots, never-satisfied, trigger-notifications, run-task) |

### The Handshake That Works

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
2. **`Mcp-Method: <method>`** header for routing
3. **`_meta.io.modelcontextprotocol/*`** envelope keys (NOT `_meta.protocolVersion`)

### Protocol Eras (2026-08-09)

| Era | Version | Wire shape | arifOS |
|-----|---------|------------|--------|
| **Modern (preferred)** | `2026-07-28` | Stateless: `server/discover`, no Mcp-Session-Id, per-request `_meta`, `Mcp-Method`/`Mcp-Name` | **Supported** |
| Legacy handshake | `2025-11-25` | initialize + session | **Supported** |

### Federation Sweep Recipe

```bash
for port in 8088 7071 7072 8081 18082 18083 3001; do
  echo "=== :$port ==="
  npx @mcpjam/inspector@latest doctor "http://127.0.0.1:$port/mcp" 2>&1 | head -30
done
```

Expected output (live as of 2026-08-08):

| Port | Organ | Status | Protocol |
|---|---|---|---|
| 8088 | arifOS | healthy | 2026-07-28 |
| 7071 | A-FORGE | healthy | (stateless_tools: 48) |
| 7072 | A-FORGE bridge | healthy | 2025-11-25 |
| 8081 | GEOX | healthy | 2025-11-25 |
| 18082 | WEALTH | degraded ⚠️ | 2025-11-25 |
| 18083 | WELL | healthy | 2025-11-25 |
| 3001 | AAA | healthy | 2025-11-25 |

### Output Format

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

---

## Section 3: Testing — MCPJam Inspector Methodology

### What MCPJam Inspector Does

| Capability | What it gives you |
|---|---|
| **Debug** | Every JSON-RPC message traced, OAuth exchange visible |
| **Chat** | Talk to any LLM against your server, see every tool call |
| **Inspect** | Tools, resources, prompts — browsable, searchable |
| **Evaluate** | Test cases with expected tool calls, run across LLMs, track accuracy |
| **OAuth Debugger** | Guided conformance checks for all spec versions |
| **CLI** | `npx @mcpjam/inspector@latest` — probe, doctor, evals from terminal |
| **SDK** | Programmatic inspection, snapshot server capabilities |
| **CI/CD** | Wire into GitHub Actions — gate PRs on regressions |

### Our Deployment

```
Container: mcpjam-federation (Docker, mcpjam/mcp-inspector:latest)
Network:   host (required — organs bind 127.0.0.1)
Listen:    0.0.0.0:6274 inside host-net container
Public:    UFW DENY on public NIC for 6274 — never Caddy/Cloudflare
Access:
  http://127.0.0.1:6274      → localhost / SSH tunnel
  http://100.64.0.2:6274      → Tailscale (Arif Windows)
Config: /opt/mcpjam/docker-compose.yaml
Data:   /opt/mcpjam/data
Seed:   /opt/mcpjam/data/federation-organs.json
Env:    /opt/mcpjam/.env (MCPJAM_* only — synced from KUNCI-MAS)
```

### Hosted API Key (`sk_…`)

| Item | Location |
|------|----------|
| Secret | `MCPJAM_API_KEY` in `/root/.secrets/kunci-mas.env` (mode 600) |
| Runtime env | `/opt/mcpjam/.env` |
| Sync | `/opt/mcpjam/sync-env-from-vault.sh` then `docker compose up -d` |
| API base | `https://app.mcpjam.com/api/v1` (`MCPJAM_API_BASE`) |

### Feeding an Organ Into Inspector

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

### CLI Quick Reference

```bash
npx @mcpjam/inspector@latest doctor http://127.0.0.1:8088/mcp
npx @mcpjam/inspector@latest tools http://127.0.0.1:8088/mcp
npx @mcpjam/inspector@latest oauth http://127.0.0.1:8088/mcp --spec 03-26
```

### Docker Management

```bash
docker ps --filter name=mcpjam
docker restart mcpjam-federation
docker pull mcpjam/mcp-inspector:latest && cd /opt/mcpjam && docker compose up -d
docker logs mcpjam-federation --tail 50
curl -sf -o /dev/null -w 'local=%{http_code}\n' http://127.0.0.1:6274/
curl -sf -o /dev/null -w 'ts=%{http_code}\n' http://100.64.0.2:6274/
ufw status | grep 6274   # expect DENY on public NIC
```

### When to Use Inspector

- **Before deploying** an organ — feed it to inspector, run tools manually, verify schemas.
- **After changing tool signatures** — check for breakage in inspector chat.
- **When debugging a failure** — inspector trace shows the exact JSON-RPC that went wrong.
- **CI runs** — wire `mcpjam doctor` into GitHub Actions pre-merge.

### When NOT to Use Inspector

- To build features — use coding agents.
- To run production workloads — inspector is a test tool.
- As a replacement for federation health monitoring — use HEARTBEAT.md / doctor.sh.

---

## Pitfalls

- The CLI binds `127.0.0.1` for security — do NOT expose `6274` publicly.
- For Docker on Mac/Win, use `host.docker.internal:PORT` not `127.0.0.1:PORT`.
- The hosted web app (`app.mcpjam.com`) is HTTPS-only — for HTTP servers use CLI or Docker.
- Don't trust a single probe — re-probe with a fresh session_id and confirm the result matches.
- The `stateless.mcpjam.com/mcp` endpoint is reference-only — it has fixture tools, not real production capabilities.
- MCPJam is **Apache 2.0**, free, and run by the same people who publish MCPJam Inspector — not a vendor lock-in.

## Related

- `mcp-ops` — for operating, calling, and debugging MCP servers (the operational counterpart).
- `AUDIT-recursive-audit` — for federation-wide audits beyond MCP.
- `forge_ephemeral` — for building new MCP servers, not testing them.

---

*Consolidated 2026-08-26 from: FORGE-mcp-smoke-test, FORGE-mcp-probe, FORGE-mcp-testing.*
*AAA Skill Library — version 2.0.0*
