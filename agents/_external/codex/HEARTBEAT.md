# HEARTBEAT - Codex health probe contract

> **Format:** JSON over HTTP (curl-friendly)
> **Frequency:** Every 60s via federation heartbeat daemon (optional - Codex is a CLI, not a daemon)
> **Card version:** 2.5.0 (truth-repaired 2026-08-26 by 333-AGI)

## Liveness probe

```bash
# Version + binary present
codex --version
# Expected: codex-cli 0.147.0

# Binary resolution check
ls -la /root/.npm-global/bin/codex
# Expected: symlink to @openai/codex dist

# Config TOML parses
python3 -c "import tomllib; tomllib.load(open('/root/.codex/config.toml','rb')); print('OK')"
# Expected: OK

# MCP server mode (Codex-as-MCP for A-FORGE)
codex mcp-server --help | head -5
# Expected: prints stdio JSON-RPC usage
```

## Federation health (Codex awareness)

Before starting a Codex task, verify the upstream gateways are alive:

| Probe | Command | Expected |
|---|---|---|
| arifOS MCP | `curl -s http://127.0.0.1:8088/health` | `status: healthy, floors_active: 13` |
| A-FORGE | `curl -s http://127.0.0.1:7072/health` | `ok: true` |
| A-FORGE SSE | `curl -s http://127.0.0.1:7071/health` | `ok: true` |
| arifFlow FQ | `curl -s http://127.0.0.1:7073/health` | `diagnosis: BALANCED` |
| FLAME free lane | `curl -s http://127.0.0.1:18901/health` | `status: live` |
| AAA cockpit | `curl -s http://127.0.0.1:3001/health` | `status: healthy` |
| Config sanity | `codex doctor` | all checks pass |

If any upstream is RED, Codex must declare `DEGRADED_CONTEXT` to Arif in plain human - not silently fail.

## Health receipt format (for arifbrain-style federation observability)

```json
{
  "agent": "codex",
  "tier": "AGI",
  "version": "0.147.0",
  "binary": "/root/.npm-global/bin/codex",
  "binary_resolved": "/root/.npm-global/lib/node_modules/@openai/codex/bin/codex.js",
  "config": "/root/.codex/config.toml",
  "config_parses": true,
  "mcp_servers_loaded": 11,
  "model_provider": "fed",
  "declared_model": "forge-777",
  "wire_api": "responses",
  "approvals_reviewer": "guardian_subagent",
  "approval_policy": "on-request",
  "sandbox_mode": "workspace-write",
  "status": "healthy",
  "checks": {
    "binary": true,
    "config_parses": true,
    "mcp_servers_loaded": 11,
    "guardian_subagent_active": true,
    "arifos_kernel_reachable": true,
    "aforge_bridge_reachable": true,
    "arifflow_reachable": true,
    "flame_reachable": true,
    "aaa_reachable": true
  },
  "verified_against": "2026-08-26T20:55:00Z",
  "ts": "2026-08-26T20:55:00Z"
}
```

## Failure modes to surface (not swallow)

- `approvals_reviewer = "auto"` (deprecated) - **GUILTY** in pre-fix state, now SEALed
- YAML frontmatter missing on skill files - non-fatal warning
- `codex mcp` subcommand times out - escalate to A-FORGE bridge (port 7072)
- Native MCP via `[mcp_servers.*]` blocks in config.toml is the canonical surface (mcp.json retired 2026-07-27)
- Config TOML parse error - block startup, surface line number to user

## Codex CLI 0.134.0+ Capability Checks

```bash
# Profiles available
ls ~/.codex/*.config.toml 2>/dev/null
# Skills loaded
ls ~/.codex/skills/ 2>/dev/null
# Subagents configured
grep -A 5 "^\[agents\]" ~/.codex/config.toml
# Hooks wired
grep -A 5 "hooks" ~/.codex/config.toml ~/.codex/hooks.json 2>/dev/null
# OTel metrics
grep -A 3 "^\[otel\]" ~/.codex/config.toml
# Analytics opt-out
grep "analytics" ~/.codex/config.toml
```

---

*Forged: 2026-06-21 by Hermes (FORGE) - wiring HEARTBEAT to codex per federated loaders ask.*
*Truth-repaired: 2026-08-26 by 333-AGI - CLI 0.136.0 to 0.147.0, orgs 5 to 7 (added arifFlow + FLAME + AAA), mcp.json retired, single config.toml canonical.*
