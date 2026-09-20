# Running MCP servers — ops, mcporter CLI, health, lifeguard

> **Lane:** RUNNING
> **Absorbed from:** `mcp-ops` ← `/root/AAA/skills/domains/forge/mcp-ops` (SKILL.md sha256 `fa0e72aec76034b83859720918fbf57769690d4e6725688c89bbd3f961d8d432`) · `mcp-ops.DEPRECATED-2026-09-19` ← `/root/AAA/skills/domains/forge/mcp-ops.DEPRECATED-2026-09-19` (SKILL.md sha256 `fa0e72aec76034b83859720918fbf57769690d4e6725688c89bbd3f961d8d432`) · `mcp-ops` ← `/root/AAA/skills/engineering/mcp-ops` (SKILL.md sha256 `fa0e72aec76034b83859720918fbf57769690d4e6725688c89bbd3f961d8d432`) · `FORGE-mcp-ops` ← `/root/AAA/skills/capabilities/coding/mcp-ops` (SKILL.md sha256 `d98000a023a33bd29d37e5de1565fc6a4b566b9383aa9d1b7417f246bb715ebd`)

**Read this when:** You need to inspect, call, or health-check a live MCP server; you need the federation MCP endpoint map; or an MCP server is down and you need the lifeguard/auto-recovery path.

Scope: general MCP ops (mcporter CLI), federation FastMCP build/deploy/operate, and the MCP lifeguard health probe. Mutating a live federation organ still requires arifOS judgment first.

---
<!-- ===== PART: mcp-ops :: /root/AAA/skills/domains/forge/mcp-ops :: sha256 fa0e72aec76034b83859720918fbf57769690d4e6725688c89bbd3f961d8d432 ===== -->
# MCP Operations

> **mcporter** is the fastest way to inspect and call any MCP tool directly from terminal.
> **FastMCP** is available system-wide: `fastmcp --version` (v3.2.4)
> Skill hierarchy: mcp-builder (build) → fastmcp-deploy (deploy) → mcp-ops (operate + recover)
> *DITEMPA BUKAN DIBERI*

## Overview

Unified MCP operations covering three domains:
1. **General MCP Ops** — mcporter CLI for inspecting, calling, and debugging MCP servers from terminal.
2. **Federation MCP Ops** — FastMCP build/deploy/operate across federation organs.
3. **MCP Lifeguard** — Health probe and auto-recovery for constitutional federation MCP servers.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- Inspect, list, or call tools on any federation organ via mcporter.
- Build or extend a Python MCP server with FastMCP.
- Test a server locally before client wiring or deployment.
- Run ad-hoc HTTP or stdio MCP connections without permanent config.
- Check federation MCP health and tool availability.
- An MCP server returns connection refused, timeout, or 5xx.
- OpenClaw logs show `[bundle-mcp] failed to start server`.
- Model fallback chain is failing (DeepSeek 402, Kimi unknown model, Ollama cold-start).
- Need a federation MCP status dashboard.
- Generate CLI wrappers or TypeScript clients from a server spec.

## When NOT to Use

- **Do not use for production deployment** without `fastmcp-deploy` or site-architecture skills and arifOS judgment.
- **Do not mutate live federation servers** (restart, config change, port binding) without arifOS F1–F13 clearance.
- **Do not run untrusted MCP servers** outside the `arifos-untrusted-sandbox` skill.
- **Do not hardcode secrets** in server code or client configs; use env vars / SOPS.
- If the target organ is degraded or unknown → run `arifos-act` and escalate to health triage.

---

## Section 1: mcporter CLI

`mcporter` is pre-installed on af-forge at `/usr/bin/mcporter v0.9.0`.

### Discovery
```bash
mcporter list                                    # list all known servers
mcporter list arifOS --schema                    # list tools + schemas for one server
mcporter list --http-url http://localhost:8081/mcp --name geox  # ad-hoc HTTP
mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
```

### Call Tools
```bash
mcporter call arifOS.arif_measure mode=health    # call with key=value
mcporter call geox.geox_well_analyze_log well_id=MAHA-1 depth_top=1500 --output json
mcporter call well.well_validate_vitality --output json
mcporter call geox.geox_well_analyze_log --args '{"well_id": "MAHA-1", "depth_top": 1500}'  # JSON args
mcporter call "geox.geox_prospect_evaluate(well_id='MAHA-1')"  # function syntax
```

### Federation MCP Servers
```
arifOS MCP    → arifOS        (7 canonical tools, F1-F13)
GEOX          → geox          (28+ tools, earth intelligence) ✅ LIVE
WEALTH        → WEALTH        (20+ tools, capital intelligence)
WELL          → WELL          (17+ tools, human readiness)
A-FORGE       → a-forge-mcp   (29 tools, execution engine)
AAA           → aaa-a2a       (A2A gateway + cockpit)
OpenClaw GW   → openclaw      (A2A mesh)
```

### Daemon
```bash
mcporter daemon start
mcporter daemon status
mcporter daemon stop
```

### Config / Auth / Codegen
```bash
mcporter config list
mcporter auth <server>
mcporter generate-cli --server geox
mcporter emit-ts <server> --mode client
```

---

## Section 2: FastMCP Federation Build/Deploy/Operate

### Install / Verify Tooling
```bash
uv add "fastmcp[tasks]==3.4.2"          # in a federation repo
pip install --break-system-packages "fastmcp[tasks]==3.4.2"  # system-wide
fastmcp --version                       # expect 3.4.2
```

### Build a FastMCP Server
```bash
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

### Test Locally
```bash
fastmcp inspect my_server.py:mcp
fastmcp list my_server.py:mcp --json
fastmcp call my_server.py:mcp get_customer customer_id=cust_123 --json
fastmcp run my_server.py:mcp --transport streamable_http --host 127.0.0.1 --port 8000
```

### Deploy
```bash
docker build -t my-mcp-server:latest .
fastmcp run my_server.py:mcp --transport http --port 8000 &
curl -s http://localhost:8000/mcp/v1/tools/list | jq '.tools[].name'
```

### Adding MCP Server to Claude Code
Edit `~/.mcp.json`:
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

### Federation MCP Conventions

| Convention | Rule |
|-----------|------|
| **Transport** | `streamable-http` for all federation servers |
| **Naming** | `{service}_{action}_{resource}` — e.g., `geox_well_analyze_log` |
| **Tool count** | Start with 1-3 high-value tools, expand only when stable |
| **Error handling** | Return structured errors, never raise raw exceptions |
| **Auth** | Environment variables only, never hardcoded |
| **Output schema** | Pydantic v2 BaseModel for all tool outputs |

---

## Section 3: MCP Lifeguard — Health Probe & Auto-Recovery

### MCP Endpoint Map

| Node | URL | Transport | Expected |
|------|-----|-----------|----------|
| arifOS | http://127.0.0.1:8088/mcp | streamable-http | 200 / JSON |
| GEOX | http://127.0.0.1:8081/mcp | streamable-http | 405 (POST only) |
| WEALTH | http://127.0.0.1:18082/mcp | streamable-http | JSON-RPC error |
| WELL | http://127.0.0.1:18083/mcp | streamable-http | JSON-RPC error |
| A-FORGE | http://127.0.0.1:7072/mcp | streamable-http | JSON-RPC error |

> **Note:** WEALTH and WELL return JSON-RPC errors on GET — this is normal. Connection refused or timeout is the real failure signal.

### Quick Pulse Check
```bash
for port in 8088 8081 18082 18083 7072; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "http://127.0.0.1:${port}/mcp" || echo "000")
  echo "Port $port: HTTP $code"
done
```

### Deep Probe with Response Time
```bash
for port in 8088 8081 18082 18083 7072; do
  rt=$(curl -s -o /dev/null -w "%{time_total}" --max-time 5 "http://127.0.0.1:${port}/mcp" || echo "999")
  echo "Port $port: ${rt}s"
done
```

### Auto-Restart Dead MCPs
```bash
mcp_map=(
  "8088:arifosmcp"
  "8081:geox_eic"
  "18082:wealth-organ"
  "18083:well"
)

for entry in "${mcp_map[@]}"; do
  port=${entry%%:*}
  container=${entry##*:}
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://127.0.0.1:${port}/mcp" || echo "000")
  if [ "$code" = "000" ] || [ "$code" = "502" ] || [ "$code" = "503" ]; then
    docker restart "$container"
    echo "$(date -Iseconds) RESTARTED $container (port $port, code $code)"
  fi
done
```

### Model Fallback Chain Monitor
```bash
# MiniMax
curl -s https://api.minimax.io/v1/models -H "Authorization: Bearer $MINIMAX_API_KEY" --max-time 5 | grep -q "MiniMax" && echo "MiniMax: OK" || echo "MiniMax: FAIL"

# DeepSeek
curl -s https://api.deepseek.com/v1/models -H "Authorization: Bearer $DEEPSEEK_API_KEY" --max-time 5 | grep -q "deepseek" && echo "DeepSeek: OK" || echo "DeepSeek: FAIL"

# Ollama local
curl -s http://127.0.0.1:11434/api/tags --max-time 5 | grep -q "qwen2.5:7b" && echo "Ollama: OK" || echo "Ollama: FAIL"
```

### Pre-Warm Ollama (Avoid Cold-Start)
```bash
curl -s http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:7b","prompt":"warmup","stream":false,"options":{"num_predict":1}}' \
  --max-time 30 > /dev/null
echo "Ollama warmed"
```

### Alert Conditions

| Condition | Action |
|-----------|--------|
| MCP HTTP 000/502/503 | Auto-restart container + log |
| MCP response > 3s | WARN in heartbeat |
| Model provider 401/402 | Disable from fallback chain + alert |
| Ollama cold-start > 15s | Pre-warm model via `/api/generate` |

### Lifeguard Rules
1. **Never restart Vault999** — append-only ledger, human ack required.
2. **Restart one MCP at a time** — avoid federation cascade.
3. **Log to `~/.openclaw/workspace/logs/mcp-lifeguard.log`**.
4. **Disable dead models** — don't let 402s burn event loop cycles.
5. **Pre-warm Ollama** on gateway startup if it's in fallbacks.

---

## Troubleshooting

```bash
# MCP not responding — check endpoint
curl -s -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# GEOX MCP bridge — verify canonical tools
curl -s http://localhost:8081/tools | python3 -c \
  "import sys,json; d=json.load(sys.stdin); \
   print(f'GEOX categories: {len(d.get(\"categories\",[]))}')"

# Port conflict
ss -tlnp | grep <port>

# FastMCP version
fastmcp --version
```

## Allowed Tools

| Tool / Capability | Purpose |
|-------------------|---------|
| `fastmcp` CLI | Scaffold, inspect, list, call, and run FastMCP servers |
| `mcporter` CLI | Discover and call MCP servers; daemon, auth, config, codegen |
| `curl` / `python3 -m json.tool` | Health probes and raw JSON-RPC checks |
| `uv` / `pip` | Install FastMCP in repo or system context |
| `docker restart` | Auto-restart dead MCP containers (lifeguard) |

## Forbidden Actions

- **NEVER** expose a FastMCP server on `0.0.0.0` in production; bind to `127.0.0.1` and let Caddy terminate TLS.
- **NEVER** hardcode credentials; use environment variables or SOPS.
- **NEVER** call a mutating tool on a live federation organ without arifOS judgment.
- **NEVER** skip `fastmcp inspect` before wiring a new server into a client.
- **NEVER** treat a successful health check as authorization to act beyond observer class.
- **NEVER** restart Vault999 — append-only ledger, human ack required.
- Escalate to **arifOS 888_JUDGE** if the call involves deletion, deployment, secrets, or constitutional files.

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Mutating action on live organ | arifOS 888_JUDGE | A2A / MCP verdict_request |
| Secret exposure in config or code | security.agent + arifOS judge | A2A message |
| Federation organ degraded/down | A-FORGE + service-health-triage skill | health probe + incident channel |
| Production deployment needed | arifOS 888_JUDGE + human (F13) | 888 HOLD |
| Tool call returns unexpected authority/scope | arifOS 888_JUDGE | hold with evidence |

---

*Consolidated 2026-08-26 from: FORGE-mcp-ops, FORGE-mcp-federation-ops, FORGE-mcp-lifeguard.*
*AAA Skill Library — version 2.0.0*

<!-- ===== PART (unique fragments only; the rest is byte-identical to the canonical copy above): mcp-ops.DEPRECATED-2026-09-19 :: /root/AAA/skills/domains/forge/mcp-ops.DEPRECATED-2026-09-19 :: sha256 fa0e72aec76034b83859720918fbf57769690d4e6725688c89bbd3f961d8d432 ===== -->

<!-- ===== PART (unique fragments only; the rest is byte-identical to the canonical copy above): mcp-ops :: /root/AAA/skills/engineering/mcp-ops :: sha256 fa0e72aec76034b83859720918fbf57769690d4e6725688c89bbd3f961d8d432 ===== -->

<!-- ===== PART (unique fragments only; the rest is byte-identical to the canonical copy above): FORGE-mcp-ops :: /root/AAA/skills/capabilities/coding/mcp-ops :: sha256 d98000a023a33bd29d37e5de1565fc6a4b566b9383aa9d1b7417f246bb715ebd ===== -->
# mcporter — Universal MCP CLI (avAILABLE at /usr/bin/mcporter v0.9.0)

`mcporter` is the fastest way to inspect and call any MCP tool directly from terminal. It auto-discovers all federation servers.


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


# GEOX MCP bridge — verify 11 canonical tools
curl -s http://localhost:8081/tools | python3 -c \
  "import sys,json; d=json.load(sys.stdin); \
   print(f'GEOX categories: {len(d.get(\"categories\",[]))}')"

