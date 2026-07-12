# AAA Ports — C-009 Survey (Batch B, 2026-07-12)

**Status:** CANONICAL port map for AAA organ  
**Source of truth:** `systemctl cat aaa-a2a` + live probe + `a2a-server/a2a-port-map.json`

## What AAA is (and is not)

| Surface | Port | Protocol | Role |
|---------|------|----------|------|
| **AAA A2A gateway + cockpit** | **3001** | HTTP / A2A | Live production (`aaa-a2a.service` → `a2a-server/server.js`) |
| Health | 3001 `/health` | HTTP JSON | `status=healthy`, protocol A2A |
| Agent card | 3001 `/.well-known/agent-card.json` | HTTP JSON | A2A discovery |
| **MCP tool surface** | **not on AAA** | — | Constitutional tools live on **arifOS :8088** `/mcp` |

**Resolution (C-009):** AAA does **not** expose a separate organ MCP tools/list on 3001.  
3001 is **A2A + cockpit UI**, not a domain MCP server like GEOX/WEALTH/WELL.  
Agents that need MCP verbs connect to **arifOS** first (governance), then domain organs.

## Related ports (NOT AAA MCP)

| Port | Process (observed) | Role |
|------|-------------------|------|
| 8787 | openclaw gateway | Edge gateway (not AAA MCP) |
| 8931 | playwright-mcp | Browser MCP |
| 3050 | 1mcp aggregate | Multi-MCP fan-in |
| 4173 | vite preview (sites) | Static site preview |
| 7071/7072 | A-FORGE | Execution API / MCP |
| 8088 | arifOS | Kernel MCP |

## How to connect

```bash
# AAA health (A2A)
curl -s http://127.0.0.1:3001/health | python3 -m json.tool

# Agent card
curl -s http://127.0.0.1:3001/.well-known/agent-card.json | python3 -m json.tool

# MCP tools (kernel, not AAA)
curl -s http://127.0.0.1:8088/health | python3 -m json.tool
```

## Unit

```
aaa-a2a.service
  ExecStart=/usr/bin/node /root/AAA/a2a-server/server.js
  Environment=PORT=3001
  Environment=ARIFOS_LOCAL_URL=http://127.0.0.1:8088
```

*Batch B C-009 closed by documentation, not by inventing a phantom AAA MCP port.*
