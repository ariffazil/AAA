---
name: arifos-mcp-502-diagnosis
description: Diagnose 502 errors from arifOS federated MCP tools (well_forge_precheck, arif_heart_critique, etc.) — trace through OpenClaw catalog, identify expired tokens vs code bugs.
tags: ["arifOS", "openclaw", "mcp", "diagnosis", "502"]
category: devops
metadata:
  arifOS_operational: true
  non_coder_override: "Arif steers, agent diagnoses and executes"
---

# arifOS MCP 502 Diagnosis Protocol

When federated MCP tools return 502 "Upstream or external service errors":

## Step 1 — Identify the tool's server

Tools like `well_forge_precheck`, `arif_heart_critique` are NOT in arifOS core — they live in federated MCP servers.

Check the OpenClaw MCP catalog:
```bash
cat /root/.hermes/workspace/openclaw/mcp/catalog.yaml
```

## Step 2 — Find the server URL and auth

For afwell tools (`well_forge_precheck`, `arif_heart_critique`), server URL is:
```
https://afwell.fastmcp.app/mcp
```

Test auth:
```bash
curl -s "https://afwell.fastmcp.app/mcp" \
  -H "Accept: text/event-stream" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

**Key error signatures:**
- `"Bearer token required"` → no token configured
- `"invalid_token", "The access token expired"` → token expired, need rotation
- `"Upstream or external service errors"` → token expired or service down

## Step 3 — Check if server is disabled in catalog

```yaml
# In catalog.yaml:
- server_id: wealth-mcp
  enabled: false        # ← disabled = all tools return errors
  auto_start: false
  approval_policy: hold
```

## Step 4 — Token rotation

If token expired:
1. Login to the service dashboard (e.g., afwell.fastmcp.app)
2. Generate new API key
3. Update in: `/root/compose/.env` (FASTMCP_API_KEY), OpenClaw config, or vault

## Step 5 — Verify fix

After token update, restart the OpenClaw gateway or the specific MCP server container.

## Common Tool → Server Mappings

| Tool | Server URL | Auth |
|------|-----------|------|
| `well_forge_precheck` | afwell.fastmcp.app | Bearer (FASTMCP_API_KEY) |
| `arif_heart_critique` | afwell.fastmcp.app | Bearer |
| `wealth_*` tools | wealth.fastmcp.app | Bearer |
| `arifOS` core tools | localhost:8080 or arifOS.fastmcp.app | None |

## Gotcha

MCP 502 does NOT mean arifOS code is broken. It means a **federated upstream service** is unreachable or its token expired. Always check the federated catalog first before patching code.
