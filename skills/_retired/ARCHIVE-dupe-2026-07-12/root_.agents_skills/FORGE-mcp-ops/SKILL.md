---
id: mcp-ops
name: FORGE-mcp-ops
version: 1.0.0
description: "mcporter — Universal MCP CLI for inspecting, calling, and debugging MCP servers from terminal."
owner: AAA
risk_tier: low
floor_scope: [F2, F8]
autonomy_tier: T1
tags: [mcp, cli, mcporter, ops, debugging]
---

# mcporter — Universal MCP CLI (avAILABLE at /usr/bin/mcporter v0.9.0)

`mcporter` is the fastest way to inspect and call any MCP tool directly from terminal. It auto-discovers all federation servers.

## Discovery
```bash
mcporter list                                    # list all known servers
mcporter list arifOS --schema                   # list tools + schemas for one server
mcporter list --http-url http://localhost:8081/mcp --name geox  # ad-hoc HTTP
```

## Call Tools
```bash
mcporter call arifOS.arif_measure mode=health  # call with key=value
mcporter call geox.geox_well_analyze_log well_id=MAHA-1 depth_top=1500 --output json
mcporter call well.well_validate_vitality --output json
```

## Federation MCP Servers
```
arifOS MCP    → arifOS        (7 canonical tools, F1-F13)
GEOX          → geox          (28+ tools, earth intelligence) ✅ LIVE
WEALTH        → WEALTH        (20+ tools, capital intelligence)
WELL          → WELL          (17+ tools, human readiness)
A-FORGE       → a-forge-mcp   (29 tools, execution engine)
AAA           → aaa-a2a       (A2A gateway + cockpit)
OpenClaw GW   → openclaw      (A2A mesh)
```

## Daemon
```bash
mcporter daemon start   # persistent connections
mcporter daemon status
mcporter daemon stop
```

---

# MCP Server Operations — arifOS Federation

# MCP Server Operations — arifOS Federation

> FastMCP is available system-wide: `fastmcp --version` (v3.2.4)
> Skill hierarchy: mcp-builder (build) → fastmcp-deploy (deploy) → mcp-ops (operate)
> GEOX MCP bridge fixed 2026-05-27: /mcp endpoint now returns 11 canonical tools

---

## Federation MCP Servers

```
arifOS MCP    → http://localhost:8088/mcp   (13 tools, streamable-http, F1-F13)
GEOX          → http://localhost:8081/mcp      (20 tools, earth intelligence) ✅ LIVE
WEALTH       → http://localhost:18082/mcp    (33 tools, capital intelligence)
WELL          → http://localhost:18083/mcp    (13 tools, human readiness)
A-FORGE       → http://localhost:7071/mcp     (build + deploy engine)
arifosd       → http://localhost:18081/health (constitutional daemon)
OpenClaw GW   → http://localhost:18789/        (A2A mesh gateway)
```

## Check MCP Health
```bash
curl -sf http://localhost:8088/health | python3 -m json.tool
curl -sf http://localhost:8081/health
curl -sf http://localhost:18082/health
curl -sf http://localhost:18083/health
curl -sf http://localhost:7071/health
```

## FastMCP Build Workflow

### 1. Scaffold (use template)
```bash
# Copy API wrapper template
cp /root/arifOS/.venv/lib/python*/site-packages/fastmcp/templates/api_wrapper.py ./my_server.py

# Or use scaffold helper
python3 /root/arifOS/.venv/lib/python*/site-packages/fastmcp/scripts/scaffold.py \
  --template api_wrapper --name "My API" --output ./my_server.py
```

### 2. Implement Tools
```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Fetch customer by ID."""
    ...
```

### 3. Test Locally (before deploying)
```bash
# Inspect server
fastmcp inspect my_server.py:mcp

# List tools
fastmcp list my_server.py --json

# Call a tool
fastmcp call my_server.py get_customer customer_id=cust_123 --json
```

### 4. Deploy (use fastmcp-deploy skill)
```bash
# Build Docker image
docker build -t my-mcp-server:latest .

# Test HTTP transport locally first
fastmcp run my_server.py:mcp --transport http --port 8000 &

# Verify
curl -s http://localhost:8000/mcp/v1/tools/list | jq '.tools[].name'
```

---

## Adding MCP Server to Claude Code

Edit `~/.mcp.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "docker",
      "args": ["run", "--rm", "-p", "8000:8000", "my-mcp-server:latest"]
    }
  }
}
```

For HTTP-based servers (preferred in arifOS):
```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

---

## arifOS Federation MCP Conventions

| Convention | Rule |
|-----------|------|
| **Transport** | `streamable-http` for all federation servers |
| **Naming** | `{service}_{action}_{resource}` — e.g., `geox_well_analyze_log` |
| **Tool count** | Start with 1-3 high-value tools, expand only when stable |
| **Error handling** | Return structured errors, never raise raw exceptions |
| **Auth** | Environment variables only, never hardcoded |
| **Output schema** | Pydantic v2 BaseModel for all tool outputs |

---

## Troubleshooting

```bash
# MCP not responding — check endpoint
curl -s -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# GEOX MCP bridge — verify 11 canonical tools
curl -s http://localhost:8081/tools | python3 -c \
  "import sys,json; d=json.load(sys.stdin); \
   print(f'GEOX categories: {len(d.get(\"categories\",[]))}')"

# Port conflict
ss -tlnp | grep <port>

# FastMCP version
fastmcp --version
```
