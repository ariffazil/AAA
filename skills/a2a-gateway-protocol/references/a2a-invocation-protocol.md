# A2A Invocation Protocol — Reference

Live-verified 2026-08-07. AAA A2A Gateway `:3001`, `aaa-a2a.service` active, `deployed_commit = source_commit = 6fdcaad`, no drift.

## Endpoint inventory

| Endpoint | Method | Purpose | Auth |
|---|---|---|---|
| `:3001/health` | GET | Liveness + drift | none |
| `:3001/.well-known/agent.json` | GET | Canonical federation agent card | none |
| `:3001/.well-known/agent-card.json` | GET | SDK-formatted card | none |
| `:3001/a2a/<lens>/agent-card.json` | GET | Lens-specific card (architect / engineer / auditor) | none |
| `:3001/a2a/message/send` | POST | Single-turn dispatch (A2A method `message/send`) | DID + A2A-Version |
| `:3001/a2a/message/stream` | POST | Streaming dispatch (SSE) | DID + A2A-Version |
| `:3001/a2a/tasks/send` | POST | Persistent task with taskId | DID + A2A-Version |
| `:3001/a2a/tasks/:taskId/cancel` | POST | Cancel running task | DID + A2A-Version |

## Error codes observed

- `-32600 Invalid Request` — missing `A2A-Version: 1.0` header
- `-32001 EMD_VALIDATION_BLOCKED` — missing `metadata.sovereign_did` envelope (tri-witness W3=0.1 < 0.3 threshold)
- `-32602` — missing or malformed `params.message`, or unknown agent name

## Full curl recipes

### Single message

```bash
curl -sf -X POST http://127.0.0.1:3001/a2a/message/send \
  -H "Content-Type: application/json" \
  -H "A2A-Version: 1.0" \
  -d '{
    "jsonrpc":"2.0",
    "method":"message/send",
    "params":{
      "message":{"role":"user","parts":[{"kind":"text","text":"your task here"}]},
      "configuration":{"agent":"555-ASI"}
    },
    "metadata":{"sovereign_did":"did:arifos:arif"},
    "id":1
  }'
```

### Persistent task

```bash
curl -sf -X POST http://127.0.0.1:3001/a2a/tasks/send \
  -H "Content-Type: application/json" \
  -H "A2A-Version: 1.0" \
  -d '{
    "jsonrpc":"2.0",
    "method":"tasks/send",
    "params":{
      "id":"task-uuid-here",
      "message":{"role":"user","parts":[{"kind":"text","text":"long-running task"}]},
      "configuration":{"agent":"333-AGI"}
    },
    "metadata":{"sovereign_did":"did:arifos:arif"},
    "id":1
  }'
```

### Multi-agent parallel dispatch (shell)

```bash
#!/usr/bin/env bash
A2A="http://127.0.0.1:3001/a2a"
TASK="$1"

dispatch() {
  local agent="$1" task="$2"
  curl -sf -X POST "$A2A/message/send" \
    -H "Content-Type: application/json" \
    -H "A2A-Version: 1.0" \
    -d "{\"jsonrpc\":\"2.0\",\"method\":\"message/send\",\"params\":{\"message\":{\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"$task\"}]},\"configuration\":{\"agent\":\"$agent\"}},\"metadata\":{\"sovereign_did\":\"did:arifos:arif\"},\"id\":1}"
}

dispatch 555-ASI "$TASK" &
dispatch 888-APEX "Judge this verdict for: $TASK" &
wait
```

## Agent names verified (live 2026-08-07)

`333-AGI`, `555-ASI`, `888-APEX`, `architect`, `engineer`, `auditor`, `hermes-asi`, `antigravity`, `openclaw`

## The 2026-08-07 hallucinated-config incident

In the OpenCode multi-agent debugging session, I dispatched an 888-APEX delegate to evaluate proposed fixes. The delegate returned a verdict asserting that `litellm-federation/opencode` was an undefined alias — a "real F2 TRUTH violation at the substrate level." That verdict came with a recommended fix.

Live verification:
```bash
grep -c "model_name: opencode" /root/A-FORGE/litellm-config.yaml
# Output: 5
```

The alias was defined 5× in the config. The delegate's "Finding C" was hallucinated — an authoritative-sounding verdict about absent config. If I'd acted on it, I would have made a code change to fix a non-existent bug, breaking a working system.

**Lesson:** delegated subagents can hallucinate config facts as confidently as they hallucinate any other fact. The fix:
1. Treat all delegation verdicts as opinions, not facts
2. For every factual claim, run the live probe before acting
3. If the verdict claims something is missing, grep for it. If it claims something is wrong, check the live state
4. Subagent "verified" claims are less trustworthy than direct grep

This skill's discipline: **existence ≠ function; fixing ≠ wired; opinion ≠ fact.**