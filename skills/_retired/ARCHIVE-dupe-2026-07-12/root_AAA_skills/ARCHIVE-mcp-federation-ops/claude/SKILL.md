---
id: mcp-federation-ops
name: MCP Federation Operations
version: 1.0.0
description: Build, inspect, call, and operate FastMCP servers and the mcporter CLI
  across federation organs.
owner: AAA
risk_tier: medium
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
dependencies:
  skills:
  - arifos-act
  servers: []
  tools: []
examples:
- Inspect a new FastMCP server before wiring it into a client
- Call arifOS health checks across all federation organs with mcporter
- Scaffold and test a new FastMCP server locally
- Ad-hoc connect to an HTTP MCP server for one-off tool calls
tests:
- mcporter list returns known federation servers
- fastmcp inspect succeeds on a server module
- fastmcp call returns expected JSON for a representative tool
- Health endpoints respond for arifOS, GEOX, WEALTH, WELL, A-FORGE
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Δ
  functional:
  - Routing
  - Forge
  layer:
  - RUNTIME
  - CODING/FI
  autonomy_tier: T2
floor_scope:
- F2
- F3
- F4
- F8
- F10
- F11
- F12
---

# MCP Federation Operations

## Overview

Operate the federation's Model Context Protocol (MCP) surface: build FastMCP servers in Python, inspect and call tools via the `fastmcp` and `mcporter` CLIs, and route requests across arifOS, GEOX, WEALTH, WELL, and A-FORGE. This skill covers both construction (scaffold → implement → test → run) and runtime operations (discovery → health → direct tool calls).

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- Build or extend a Python MCP server with FastMCP.
- Inspect, list, or call tools on any federation organ.
- Test a server locally before client wiring or deployment.
- Run ad-hoc HTTP or stdio MCP connections without permanent config.
- Generate CLI wrappers or TypeScript clients from a server spec.
- Check federation MCP health and tool availability.

## When NOT to Use

- **Do not use for production deployment** without the `fastmcp-deploy` or site-architecture skills and arifOS judgment.
- **Do not mutate live federation servers** (restart, config change, port binding) without arifOS F1–F13 clearance.
- **Do not run untrusted MCP servers** outside the `arifos-untrusted-sandbox` skill.
- **Do not hardcode secrets** in server code or client configs; use env vars / SOPS.
- If the target organ is degraded or unknown → run `arifos-act` and escalate to health triage.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| server_module | yes for build | Python file exposing a `FastMCP` instance, e.g. `my_server.py:mcp` |
| server_name | yes for ops | Federation server alias or HTTP endpoint, e.g. `geox`, `arifOS` |
| tool_name | yes for calls | Canonical `{service}_{action}_{resource}` tool name |
| arguments | yes for calls | Key=value pairs, JSON blob, or function-style args |
| transport | no | `streamable_http` (federation default), `stdio`, or `http` |

## Procedure

### Step 1: Install / Verify Tooling

```bash
# FastMCP CLI + library
uv add "fastmcp[tasks]==3.4.2"          # in a federation repo
pip install --break-system-packages "fastmcp[tasks]==3.4.2"  # system-wide
fastmcp --version                       # expect 3.4.2

# mcporter is pre-installed on af-forge
mcporter --version                      # /usr/bin/mcporter v0.9.0
```

### Step 2: Build a FastMCP Server

```bash
# Scaffold from template
fastmcp scaffold --template api_wrapper --name "My API" --output ./my_server.py
```

Implement tools following federation conventions:

```python
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("my-server")

class CustomerOutput(BaseModel):
    id: str
    name: str
    segment: str
    confidence: float

@mcp.tool()
def get_customer(customer_id: str) -> CustomerOutput:
    """Fetch customer by ID with confidence score."""
    ...
```

### Step 3: Test Locally

```bash
fastmcp inspect my_server.py:mcp
fastmcp list my_server.py:mcp --json
fastmcp call my_server.py:mcp get_customer customer_id=cust_123 --json
fastmcp run my_server.py:mcp --transport streamable_http --host 127.0.0.1 --port 8000
```

### Step 4: Discover Federation Servers

```bash
mcporter list                                     # all known servers
mcporter list arifOS --schema                     # tools + schemas
mcporter list --http-url http://localhost:8081/mcp --name geox   # ad-hoc
mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
```

### Step 5: Call Federation Tools

```bash
# Key=value syntax
mcporter call arifOS.arif_ops_measure mode=health
mcporter call geox.geox_well_analyze_log well_id=MAHA-1 depth_top=1500 --output json

# JSON args
mcporter call geox.geox_well_analyze_log --args '{"well_id": "MAHA-1", "depth_top": 1500}'

# Function syntax
mcporter call "geox.geox_prospect_evaluate(well_id='MAHA-1')"
```

### Step 6: Check Federation Health

```bash
curl -sf http://localhost:8088/health  | python3 -m json.tool   # arifOS
curl -sf http://localhost:8081/health                            # GEOX
curl -sf http://localhost:18082/health                           # WEALTH
curl -sf http://localhost:18083/health                           # WELL
curl -sf http://localhost:7071/health                            # A-FORGE
```

### Step 7: Daemon / Config / Codegen (Optional)

```bash
mcporter daemon start
mcporter daemon status
mcporter daemon stop

mcporter config list
mcporter auth <server>

mcporter generate-cli --server geox
mcporter emit-ts <server> --mode client
```

## Allowed Tools

| Tool / Capability | Purpose |
|-------------------|---------|
| `fastmcp` CLI | Scaffold, inspect, list, call, and run FastMCP servers |
| `mcporter` CLI | Discover and call MCP servers; daemon, auth, config, codegen |
| `curl` / `python3 -m json.tool` | Health probes and raw JSON-RPC checks |
| `uv` / `pip` | Install FastMCP in repo or system context |

## Forbidden Actions

- **NEVER** expose a FastMCP server on `0.0.0.0` in production; bind to `127.0.0.1` and let Caddy terminate TLS.
- **NEVER** hardcode credentials; use environment variables or SOPS.
- **NEVER** call a mutating tool on a live federation organ without arifOS judgment.
- **NEVER** skip `fastmcp inspect` before wiring a new server into a client.
- **NEVER** treat a successful health check as authorization to act beyond observer class.
- Escalate to **arifOS 888_JUDGE** if the call involves deletion, deployment, secrets, or constitutional files.

## Output Format

```
## Skill Result: mcp-federation-ops

### Summary
One-paragraph summary of what was built, inspected, or called.

### Evidence
- Server/tool inspected: <name>
- Health status: <OK / DEGRADED / DOWN>
- Sample call result: <short JSON or summary>
- Schema compliance: <pass / fail / notes>

### Recommendations
- Next step (e.g., deploy, fix, escalate)
- Any drift or version mismatch found

### Escalations
- None / <list>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Mutating action on live organ | arifOS 888_JUDGE | A2A / MCP verdict_request |
| Secret exposure in config or code | security.agent + arifOS judge | A2A message |
| Federation organ degraded/down | A-FORGE + service-health-triage skill | health probe + incident channel |
| Production deployment needed | arifOS 888_JUDGE + human (F13) | 888 HOLD |
| Tool call returns unexpected authority/scope | arifOS 888_JUDGE | hold with evidence |

---

*Skill synthesized from: `.claude/skills/mcp-ops.md`, `.codex/skills/fastmcp.md`, `.codex/skills/mcporter.md`*
*AAA Skill Library — version 1.0.0*
