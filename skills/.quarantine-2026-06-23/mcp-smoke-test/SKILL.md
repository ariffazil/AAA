---
id: mcp-smoke-test
name: MCP Server Smoke Test
version: 1.0.0
description: Validate that MCP servers respond correctly to health probes and basic
  tool calls. Detect down servers, mismatched schemas, and transport errors.
owner: AAA
risk_tier: low
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
  skills: []
  servers: []
  tools:
  - health-probe
  - mcp-call
examples:
- Daily federation health check across all organs
tests:
- arifOS port 8088 responds with 13 tools
- GEOX port 8081 responds with petrophysics tools
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Ω
  functional:
  - Ops
  layer: RUNTIME
  autonomy_tier: T1
floor_scope:
- F2
- F3
- F11
---

# MCP Server Smoke Test

## Overview

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


Federation organs expose MCP surfaces on different ports. This skill validates that each server is reachable, returns the expected tool count, and responds to a basic tool call without errors.

## When to Use

- Daily federation health sweep
- After restarting any MCP server
- Before declaring a deployment successful
- When an agent reports "server unreachable"

## When NOT to Use

- Do not use to probe external/third-party MCP servers without permission
- Do not use as a load test — this is a smoke test, not a stress test
- Do not use to extract secrets from MCP servers

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| server_list | yes | Array of `{name, url, expected_tools}` |
| timeout_ms | no | Default 5000ms |

## Procedure

### Step 1: Health Probe

For each server in `server_list`:

1. Send HTTP GET to `/health` or root endpoint
2. Record: status code, response time, error (if any)
3. If status != 200 → flag as **DOWN**

### Step 2: Tool Surface Probe

For each healthy server:

1. List available tools (MCP `tools/list` or REST equivalent)
2. Count tools and compare to `expected_tools`
3. If count mismatch → flag as **DRIFT**

### Step 3: Basic Tool Call

For each healthy server:

1. Call a safe, read-only tool (e.g., `arif_floor_status`, `health`)
2. Verify response parses correctly
3. If parse error or exception → flag as **BROKEN**

### Step 4: Compile Report

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `curl` / `fetch` | HTTP health probe |
| `mcp-call` | MCP tool invocation |

## Forbidden Actions

- **NEVER** call destructive tools during smoke test
- **NEVER** send malformed input designed to crash servers
- **NEVER** probe ports not in the canonical federation list

## Output Format

```markdown
## Skill Result: mcp-smoke-test

### Summary
[X/Y] servers healthy, [Z] drift, [W] broken

### Per-Server Results
| Server | Status | Tools | RTT | Error |
|--------|--------|-------|-----|-------|
| arifOS | UP | 13/13 | 45ms | — |
| GEOX | UP | 28/28 | 120ms | — |
| WEALTH | DOWN | — | — | connection refused |

### Drift Detected
- None / [list]

### Recommendations
1. [Action] — [Server] — [Priority]
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| arifOS down | ops.agent + Arif | Immediate alert |
| Tool count drift >5 | AAA agent | Registry update needed |
| Repeated failures | A-FORGE agent | Deployment rollback check |

---

*Skill version 1.0.0 — AAA Skill Library*