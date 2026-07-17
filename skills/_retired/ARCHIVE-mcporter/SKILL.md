---
name: mcporter
description: Use mcporter CLI to list, configure, authenticate, and call MCP servers and tools directly from the terminal. Ad-hoc HTTP/stdio servers, daemon mode, code generation, and config management. Available at /usr/bin/mcporter v0.9.0 on af-forge.
version: 1.0.0
author: arifOS (based on Hermes official/mcp/mcporter)
tags: MCP, Tools, CLI, Discovery, Interop
agents: claude | opencode | kimi | codex
---

# mcporter — Universal MCP Client CLI

> Available at `/usr/bin/mcporter` v0.9.0 — no install needed on af-forge.
> For building MCP servers, use the `fastmcp` skill.

---

## When to Use

- Discover and inspect all MCP servers on the machine
- Call a specific MCP tool directly from terminal (no agent needed)
- Test a new MCP server before wiring into Codex or another client
- Ad-hoc connection to any HTTP MCP server without config
- Run a stdio MCP server on the fly for one-off calls
- Generate CLI wrappers or TypeScript clients from a server spec

---

## Quick Start

```bash
# List all known MCP servers
mcporter list

# List tools + schemas for a server
mcporter list arifOS --schema

# Call a tool
mcporter call arifOS.arif_ops_measure mode=health
```

---

## Discovery

```bash
# Auto-discover all servers from all client configs on this machine
mcporter list

# Connect to an HTTP MCP server ad-hoc (no config)
mcporter list --http-url https://geox.arif-fazil.com/mcp --name geox

# Run a stdio server on the fly
mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
```

---

## Calling Tools

```bash
# Key=value syntax
mcporter call arifOS.arif_session_init session_id=test

# JSON args
mcporter call geox.geox_well_analyze_log --args '{"well_id": "MAHA-1", "depth_top": 1500}'

# Machine-readable output
mcporter call well.well_validate_vitality --output json

# Function syntax
mcporter call "geox.geox_prospect_evaluate(well_id='MAHA-1')"
```

---

## Auth

```bash
# OAuth login for a server
mcporter auth <server | url>

# Reset auth
mcporter auth <server> --reset
```

---

## Daemon

For persistent server connections:

```bash
mcporter daemon start
mcporter daemon status
mcporter daemon stop
mcporter daemon restart
```

---

## Config

```bash
mcporter config list
mcporter config get <key>
mcporter config add <server>
mcporter config remove <server>
mcporter config import <path>
```

---

## Code Generation

```bash
# Generate CLI wrapper for a server
mcporter generate-cli --server geox

# Inspect a generated CLI
mcporter inspect-cli <path> --json

# Generate TypeScript types/client
mcporter emit-ts <server> --mode client
mcporter emit-ts <server> --mode types
```

---

## arifOS Federation Servers

| Server | Endpoint | Tools |
|--------|----------|-------|
| arifOS | `http://localhost:8088/mcp` | 13 (constitutional kernel) |
| GEOX | `http://localhost:8081/mcp` | 20 (earth intelligence) |
| WEALTH | `http://localhost:18082/mcp` | 33 (capital intelligence) |
| WELL | `http://localhost:18083/mcp` | 13 (human readiness) |

```bash
# Direct calls to federation servers
mcporter call arifOS.arif_ops_measure mode=health
mcporter call geox.geox_well_analyze_log well_id=MAHA-1
mcporter call WEALTH.wealth_synthesize
mcporter call WELL.well_validate_vitality
```

---

## Troubleshooting

```bash
# Server not found
mcporter list  # verify server is registered

# Auth required
mcporter auth <server>

# HTTP server not responding
curl -s http://localhost:8081/mcp  # verify server is up first

# Daemon not running
mcporter daemon start
```
