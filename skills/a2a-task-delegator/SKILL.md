---
name: a2a-task-delegator
description: Standardized A2A v1.0 task delegation (message/send, tasks/get, tasks/cancel), precondition contracts, and output attestation for cross-vendor multi-agent swarms.
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Agent-to-Agent (A2A) Task Delegator Skill (`a2a-task-delegator`)

Task delegation, precondition locks, and output attestation contracts for multi-agent swarms (Claude Code, OpenCode, Kimi, Codex, Grok).

> **Live surface (OBS 2026-09-09):** Agent Card at `https://aaa.arif-fazil.com/.well-known/agent-card.json` — A2A v1.0 schema, official verbs, OAuth2 + Ed25519 proof. Canonical host: `forge.arif-fazil.com` (the `a-forge` subdomain 301-redirects there).
> **Drift note:** before 2026-09-09 this skill taught a fictional `a2a.delegate_task` method that no deployed surface ever exposed. Fixed after live-probe falsification. Witness before projection.

## Official JSON-RPC surface (deployed)

### Delegate work — `message/send`

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [
        {"kind": "text", "text": "run_playwright_e2e_test"},
        {"kind": "data", "data": {"target_url": "https://arif-fazil.com/earth/"}}
      ],
      "metadata": {
        "task_id": "task-20260909-001",
        "assignee": "warga_ui_auditor",
        "preconditions": [
          "dist/index.html built successfully",
          "Caddy proxy active"
        ],
        "expected_output_schema": {
          "errors_count": "number",
          "screenshot_path": "string"
        }
      }
    }
  },
  "id": 1
}
```

### Task lifecycle

```json
{"method": "tasks/get",    "params": {"id": "task-20260909-001"}}
{"method": "tasks/cancel", "params": {"id": "task-20260909-001", "reason": "precondition failed"}}
```

Preconditions and attestation conventions ride in `message.metadata` (federation convention) — the wire carries only official v1.0 verbs.

## Best Practices for Federation Agents

1. **State Locking**: acquire the state lock before starting a task — prevents race conditions across parallel agent runs.
2. **Attestation Receipt**: completed task receipt carries execution hash and status (`SEAL`, `HOLD`, `FAIL`).
3. **Card-first discovery**: resolve the counterparty's Agent Card before sending; honor its `supportedInterfaces`, `securitySchemes`, and capabilities.
4. **Drift guard**: before teaching or consuming any RPC surface, probe the live card — documentation lags deployment in both directions.
