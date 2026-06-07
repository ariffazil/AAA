# HEARTBEAT — Codex health probe contract

> **Format:** JSON over HTTP (curl-friendly)
> **Frequency:** Every 60s via federation heartbeat daemon (optional — Codex is a CLI, not a daemon)

## Liveness probe

```bash
# Version + binary present
codex --version
# Expected: codex-cli 0.136.0

# MCP server mode (Codex-as-MCP for A-FORGE)
codex mcp-server --help | head -5
# Expected: prints stdio JSON-RPC usage

# Live tool load
timeout 10 codex exec "echo F1-AMANAH" --skip-git-repo-check
# Expected: no error, session-id printed
```

## Federation health (Codex awareness)

Before starting a Codex task, verify the upstream gateways are alive:

| Probe | Command | Expected |
|---|---|---|
| arifOS MCP | `curl -s http://127.0.0.1:8088/health \| jq .status` | `"healthy"` |
| A-FORGE | `curl -s http://127.0.0.1:7071/health \| jq .ok` | `true` |
| VAULT999-writer | `curl -s http://127.0.0.1:5001/health \| jq .vault_seals_count` | `>= 61` |
| Config sanity | `codex doctor` | all checks pass |

If any upstream is RED, Codex must declare `DEGRADED_CONTEXT` to Arif in plain human — not silently fail.

## Health receipt format (for arifbrain-style federation observability)

```json
{
  "agent": "codex",
  "tier": "AGI",
  "version": "0.136.0",
  "binary": "/usr/local/bin/codex",
  "config": "/root/.codex/config.toml",
  "mcp_config": "/root/.codex/mcp.json",
  "approvals_reviewer": "guardian_subagent",
  "status": "healthy",
  "checks": {
    "binary": true,
    "config_parses": true,
    "mcp_servers_loaded": 8,
    "guardian_subagent_active": true,
    "arifos_kernel_reachable": true,
    "aforge_bridge_reachable": true
  },
  "ts": "2026-06-06T18:40:00Z"
}
```

## Failure modes to surface (not swallow)

- `approvals_reviewer = "auto"` (deprecated) — **GUILTY** in pre-fix state, now SEALed
- YAML frontmatter missing on skill files — non-fatal warning
- `codex mcp` subcommand times out — escalate to A-FORGE bridge (port 7071)
- Native MCP `false` — codex uses **stdio JSON-RPC via `codex mcp-server`** for in-process routing; A-FORGE for cross-process
