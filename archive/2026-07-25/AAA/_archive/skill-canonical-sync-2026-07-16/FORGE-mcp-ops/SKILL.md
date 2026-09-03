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

# mcporter — Universal MCP CLI (available at `/usr/bin/mcporter`, v0.9.0)

`mcporter` inspects and calls configured MCP servers. It is a transport client, not an authority layer: arifOS still owns judgment and A-FORGE still owns execution.

## Discovery
```bash
mcporter list
mcporter list arifos --schema
mcporter list geox --schema
mcporter list wealth --schema
mcporter list well --schema
mcporter list aforge --schema
```

## Call Tools
```bash
mcporter call arifos.arif_init mode=light actor_id=arif --output json
mcporter call geox.geox_basin basin_name="Malay Basin" --output json
mcporter call well.well_health_check include_federation=false --output json
```

## Federation MCP Servers

The following is a dated observation from `mcporter list` at 2026-07-15T10:45Z. Refresh before making a current claim:

| Server | Internal endpoint | Live tools | Role |
|---|---|---:|---|
| `arifos` | `127.0.0.1:8088/mcp` | 8 | Constitutional governance kernel |
| `aforge` | `127.0.0.1:7072/mcp` | 109 | Governed execution shell |
| `geox` | `127.0.0.1:8081/mcp` | 15 | Earth intelligence |
| `wealth` | `127.0.0.1:18082/mcp` | 12 | Capital intelligence |
| `well` | `127.0.0.1:18083/mcp` | 27 | Reflect-only human readiness |
| `aaa` | `127.0.0.1:3001` | A2A | Control-plane cockpit |

Configured discovery also showed 23 servers: 19 healthy and 4 offline. Offline servers remain UNKNOWN until probed again; their last-known schemas are not operational evidence.

## Authority Note (2026-07-15 kernel test)

arifOS `arif_judge` requires SOVEREIGN authority. The kernel interceptor resolves authority from **transport-level JWT/DPoP** — self-reported `actor_id` caps at MEDIUM. Without JWT, judge calls return `888_HOLD`.

To test the sovereign path, present valid JWT in `Authorization: Bearer <token>` header.

## Daemon
```bash
mcporter daemon start
mcporter daemon status
mcporter daemon stop
```

---

## MCP Server Operations — arifOS Federation

> FastMCP is available system-wide; check the installed version with `fastmcp --version`.
> Skill hierarchy: MCP builder → FastMCP deploy → MCP ops.
> Tool counts above are a live snapshot, not a contract. Schemas and ownership are authoritative.

## Check MCP Health
```bash
curl -sf http://127.0.0.1:8088/health | python3 -m json.tool
curl -sf http://127.0.0.1:8081/health
curl -sf http://127.0.0.1:18082/health
curl -sf http://127.0.0.1:18083/health
curl -sf http://127.0.0.1:7071/health
curl -sf http://127.0.0.1:7072/health
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
