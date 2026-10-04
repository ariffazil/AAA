# A-FORGE Dual-Port Diagnostic (2026-08-11)

## Situation
User reported: "A-FORGE actually healthy beb — port 7071 respond penuh" but 7072 failed to connect.

## Three systemd units involved

| Unit | Port | Binary | State | Diagnosis |
|---|---|---|---|---|
| **a-forge.service** | 7071 | `server.js` | ✅ running (58min) | Healthy, 116 tools, `/mcp` returns 200 |
| **a-forge-mcp.service** | 7072 | `serve.js` | ❌ dead since 11:14:49 | Clean SIGTERM, `Restart=on-failure` ignores clean exits |
| **a-forge-mcp-test.service** | 7072 (wanted) | `server.js` ← **wrong** | ❌ failed 17h ago | Exit 226/NAMESPACE — wrong binary + RestrictNamespaces=yes |

## Why 7072 is down

`a-forge-mcp.service` received a clean SIGTERM at 11:14:49 today. Not a crash. Not OOM. Not segfault. The journal's final line before death:
```
[McpPolicyGate] audit log write failed
```
That's just the audit logger getting cut mid-request as the process shut down.

**`Restart=on-failure` in the unit file means clean exits (`code=killed, signal=TERM`) don't trigger restart.**

Someone ran `systemctl stop a-forge-mcp.service` — likely the deploy script from 2026-08-08 (`e1eb1d4f` commit: "add make deploy-local + verify to A-FORGE") or a manual stop.

Tailscale still advertises 7072 on the mesh (`100.64.0.2:7072`) but nothing local listens — so mesh clients connecting there will time out.

## Why a-forge-mcp-test.service failed

Created 2026-08-10 19:07, started 19:08:26, died 19:08:37 (26ms runtime). Three bugs stacked:

1. **Wrong binary**: `ExecStart=.../server.js` — that's the Sense wrapper (7071 binary), not `serve.js` (7072 MCP gateway)
2. **Namespace restriction**: `privilege-inversion.conf` adds `RestrictNamespaces=yes`, and Node.js startup needs namespace ops
3. **ReadWritePaths too narrow**: only `/root/A-FORGE` and `/root/.agent-workbench` — the MCP audit log at `/root/A-FORGE/data/mcp-audit.jsonl` might work but `/tmp` is `PrivateTmp`

It's a throwaway test unit (`disabled`, not enabled). Harmless noise.

## Diagnostic commands

```bash
# Check both ports
curl -sf http://127.0.0.1:7071/health | jq '{status, tool_count, authority_ceiling}'
curl -sf http://127.0.0.1:7072/health | jq '{status, tool_count, authority_ceiling}'

# Check both systemd units
systemctl status a-forge.service --no-pager -l | head -25
systemctl status a-forge-mcp.service --no-pager -l | head -25

# Check port bindings
ss -tlnp | grep -E "707[12]"

# Check what binary each unit runs
systemctl cat a-forge.service | grep ExecStart
systemctl cat a-forge-mcp.service | grep ExecStart

# Check recent journal for stop reason
journalctl --since "11:00" --until "11:20" -u a-forge-mcp.service --no-pager | tail -15
```

## Fix

```bash
# Start the MCP service
systemctl start a-forge-mcp.service

# Verify it's listening
ss -tlnp | grep :7072
curl -sf http://127.0.0.1:7072/health | jq '{status, tool_count}'
```

## Key takeaway

A-FORGE is NOT a single service. It's two separate Node.js processes with different responsibilities. When diagnosing A-FORGE issues, always check both ports and both systemd units. The "A-FORGE is healthy" claim is ambiguous until you specify which port/service you mean.