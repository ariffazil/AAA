# AAA A2A Gateway — Multi-Agent Invocation Path (2026-08-07)

## When to use this reference

The user asks "why can't I spawn multi-agent from CLI" or "how do I dispatch parallel agents from one terminal." OpenCode's `--agent` flag only accepts `mode: primary` agents; subagents (555-ASI, 888-APEX, image-analyzer, dispatch) are rejected at CLI level. The proper cross-process path is the AAA A2A Gateway on port 3001.

## Live endpoint inventory (probed 2026-08-07 04:32 UTC)

| Endpoint | Method | Purpose | Auth |
|---|---|---|---|
| `:3001/health` | GET | Liveness + drift status + Apex scalars | none |
| `:3001/.well-known/agent.json` | GET | Canonical federation agent card (gateway itself) | none |
| `:3001/.well-known/agent-card.json` | GET | SDK-formatted card | none |
| `:3001/a2a/architect/agent-card.json` | GET | 333-AGI card (lens: architect) | none |
| `:3001/a2a/engineer/agent-card.json` | GET | 333-AGI card (lens: engineer) | none |
| `:3001/a2a/auditor/agent-card.json` | GET | 333-AGI card (lens: auditor) | none |
| `:3001/a2a/hermes-asi/agent-card.json` | GET | Hermes card | none |
| `:3001/a2a/antigravity/agent-card.json` | GET | Antigravity card | none |
| `:3001/a2a/openclaw/agent-card.json` | GET | OpenClaw card | none |
| `:3001/a2a/message/send` | POST | Send message to agent (A2A protocol `message/send`) | DID envelope + `A2A-Version: 1.0` |
| `:3001/a2a/tasks/send` | POST | Submit persistent task (`tasks/send`) | DID envelope + `A2A-Version: 1.0` |
| `:3001/a2a/tasks/:taskId/cancel` | POST | Cancel running task | DID envelope + `A2A-Version: 1.0` |

## Required headers (constitutive — fail without these)

```
Content-Type: application/json
A2A-Version: 1.0
```

Without `A2A-Version: 1.0` → server returns `-32600 Invalid Request`:
```json
{"error":{"code":-32600,"message":"Invalid Request","data":{"details":"A2A-Version header is required. Set A2A-Version: 1.0"}}}
```

## Required envelope (DID-bound)

Every `message/send` or `tasks/send` must carry a `metadata` block with a DID. Without it → `-32001 EMD_VALIDATION_BLOCKED` (tri-witness W3=0.1 < threshold 0.3).

```json
{
  "metadata": {
    "sovereign_did": "did:arifos:arif"
  }
}
```

Agent-card endpoint (`metadata.sovereign_did`) is the minimum viable envelope for non-sealed dispatch.

## Concrete invocation: message/send to 555-ASI

```bash
curl -X POST http://127.0.0.1:3001/a2a/message/send \
  -H "Content-Type: application/json" \
  -H "A2A-Version: 1.0" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "your task here"}]
      },
      "configuration": {"agent": "555-ASI"}
    },
    "metadata": {"sovereign_did": "did:arifos:arif"},
    "id": 1
  }'
```

## Multi-agent fan-out from shell (parallel dispatch)

```bash
#!/usr/bin/env bash
A2A="http://127.0.0.1:3001/a2a"
DID="did:arifos:arif"

dispatch() {
  curl -sf -X POST "$A2A/message/send" \
    -H "Content-Type: application/json" \
    -H "A2A-Version: 1.0" \
    -d "{
      \"jsonrpc\":\"2.0\",
      \"method\":\"message/send\",
      \"params\":{
        \"message\":{\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"$2\"}]},
        \"configuration\":{\"agent\":\"$1\"}
      },
      \"metadata\":{\"sovereign_did\":\"$DID\"},
      \"id\":1
    }"
}

# Parallel dispatch — 555-ASI researches, 888-APEX judges
dispatch 555-ASI "Analyze the drift in arifOS kernel" &
dispatch 888-APEX "Judge this analysis: the drift is a watch item" &
wait
```

## Error codes (live)

| Code | Meaning | Fix |
|---|---|---|
| `-32600` | Missing `A2A-Version: 1.0` header | Add `-H "A2A-Version: 1.0"` |
| `-32001` | Missing DID envelope (W3 tri-witness fail) | Add `"metadata": {"sovereign_did": "did:arifos:arif"}` |
| `-32602` | Wrong field name (`message` not `message`) or missing `message` key | Check JSON shape matches A2A spec |

## Live-verified state (2026-08-07 04:32 UTC)

- `aaa-a2a.service` active, port 3001 on `127.0.0.1` + tailscale `100.64.0.2`
- `deployed_commit = source_commit = 6fdcaad` → **no drift**
- Apex scalars: `G=0.875 HEALTHY`, `C_dark=0.008 SAFE`, `W3=0.879 CONSENSUS`
- All 3 core agent-cards present: 333-AGI, 555-ASI, 888-APEX
- Membrane v0.3 active — every response carries `_membrane` envelope
- Service is stateless per-request (no long-lived background dispatch worker on 3001 itself)

## Pitfalls

1. **Missing `A2A-Version` header** → `-32600` at gateway, silent failure if caller ignores errors.
2. **Missing DID envelope** → `-32001` tri-witness block. The gate is real, not cosmetic.
3. **Wrong agent name** in `configuration.agent` → `-32602`. Use exact registered names: `333-AGI`, `555-ASI`, `888-APEX`, `hermes-asi`, `architect`, `engineer`, `auditor`, `antigravity`, `openclaw`.
4. **`message/stream` returns SSE** — use `--no-buffer` and parse line-by-line; a plain `curl` capture returns incomplete output.
5. **12MB payload limit** (Express config: `limit: '12mb'`). Payloads over 12 MB are rejected.
6. **Stateless dispatch**: the A2A gateway is HTTP stateless — there is no persistent worker queue behind `:3001`. Long-running tasks will timeout unless the target agent has its own async completion path.
7. **`subagent_depth` in OpenCode config** is a separate concept — it controls how many levels deep OpenCode agents can nest their own subagents. It does NOT control the A2A gateway or cross-process invocation.

## Cross-references

- `federation-peer-consultation` — for when the user wants to CONSULT another agent, not dispatch a task to it
- `federation-infra-verification` §3 — MCP service probing patterns (port health, Accept-header gates)
- `federation-model-routing` — for resolving which model an alias like `litellm-federation/opencode` actually serves

---

**Date:** 2026-08-07
**Type:** class-level reference (multi-agent invocation via A2A gateway)
**Source:** `/root/HERMES/plans/2026-08-07_120000-aaa-a2a-multigent-invocation.md` (copied from live-verified probe session)