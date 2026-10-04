---
description: Live trace of wiring OpenClaw into AAA A2A mesh — the exact 4-error → green path. Read before declaring any new warga "wired" with config-only evidence.
forged: 2026-08-07
---

# OpenClaw → AAA Wiring: 4-Error Debug Path (2026-08-07)

A new warga with a DID, a signature key, and an organs.yaml entry is **not** wired to AAA. The A2A gateway enforces a multi-layer auth gate that requires progressive registration across THREE files. This is the exact sequence one OpenClaw dispatch walked through on 2026-08-07, error-by-error.

## The 4 failures, in order

### Error 1 — `400 -32600 "jsonrpc must be \"2.0\""`
**Cause:** built the envelope without `jsonrpc: "2.0"` root field.
**Fix:** add `jsonrpc`, `id`, `method` to envelope root BEFORE `params`. The A2A wire speaks JSON-RPC 2.0 over HTTP, not a custom envelope format.

### Error 2 — `403 -32001 "Sender actor_id \"openclaw:ingress\" is not canonical"`
**Cause:** used `openclaw:ingress` but the canonical set is plain: `aaa-architect`, `aaa-engineer`, `aaa-auditor`, `hermes`, `antigravity`, `arifos`, `aforge`, `geox`, `wealth`, `well`, `openclaw`, `forge`, `777-forge`, `anonymous`. The colon-form is **not** a valid actor.
**Fix:** `actor_id: "openclaw"` (the canonical short form). Keep the more specific key in `key_id` field for edge-key granularity.

### Error 3 — `403 -32001 "Agent openclaw has no registered policy — DENY ALL"`
**Cause:** actor is canonical but no policy registered. The AAA code does `registerAgentPolicy('X', { ... })` at server startup; new agents need a code-level entry, not just a registry file.
**Fix:** add to `/root/AAA/a2a-server/federation_envelope.js` at the seed-federation block (`registerAgentPolicy('hermes-asi', ...)` is the nearest neighbor):
```javascript
registerAgentPolicy('openclaw', {
  agent_role: 'router',
  allowed_tools: ['/tasks', 'arif_sense_observe', 'arif_ops_measure', 'arif_memory_recall', 'arif_reply_compose'],
  allowed_organs: ['arifOS', 'AAA', 'GEOX', 'WEALTH', 'WELL', 'A-FORGE'],
  irreversibility_threshold: 0.05,  // DISPLAY_ONLY = lowest
});
```

### Error 4 — `403 -32001 "/tasks not in allowed_tools for agent openclaw"`
**Cause:** the `/tasks` HTTP path is matched against `allowed_tools` literally. The list of M2/kernel tool names in the policy is only useful for kernel dispatch; the HTTP tool path must be added separately.
**Fix:** add `'/tasks'` to `allowed_tools` array. The full set: `['/tasks', 'arif_sense_observe', 'arif_ops_measure', 'arif_memory_recall', 'arif_reply_compose']`.

### Error 5 — `400 -32600 "params.message or params.text required"`
**Cause:** the A2A-side envelope structure was nested too deep (`params.envelope.body.query`). The `/tasks` endpoint flattens to A2A message shape: `params.message.parts[].text`.
**Fix:** reshape the JSON payload to:
```json
{
  "jsonrpc": "2.0",
  "id": "<uuid>",
  "method": "tasks.dispatch",
  "params": {
    "message": {
      "role": "agent",
      "messageId": "<uuid>",
      "parts": [{"type": "text", "text": "<query>"}]
    },
    "metadata": {
      "intent": "...", "ceiling": "DISPLAY_ONLY",
      "requested_capabilities": [...], ...
    }
  }
}
```
Query goes in `params.message.parts[0].text`. Everything else (intent, capabilities, context) goes in `params.metadata.*`.

## The 4 files that need to align

For any new w arga, all four must be touched. Skipping any one = the auth gate will catch it:

| # | File | What you add |
|---|---|---|
| 1 | `/root/AAA/secrets/did/registry.json` (+ runtime mirror) | `did:arif:<organ>` with `public_key_hex` + `algorithm: Ed25519` |
| 2 | `/root/AAA/federation/organs.yaml` | EDGE-class entry with `actor_id`, `did`, `signing_key`, authoritative_ceiling |
| 3 | `/root/AAA/a2a/registry/agents.yaml` | Agent card entry with `auth_scheme: ed25519-signature`, `trust_level: internal` |
| 4 | `/root/AAA/a2a-server/federation_envelope.js` | `registerAgentPolicy('<organ>', { ... })` call in the seed-federation block — **code-level, not config-level** |

After patching #4, `systemctl restart aaa-a2a`. The policy registration happens at startup; live config reload does NOT pick up new policies.

## Provably-wired proof (don't accept config-only verification)

A new w arga is **not** wired until a real dispatch returns 200 from AAA. The minimal proof:
```bash
cd /root/.openclaw/workspace/ops/hermes/plugins
python3 a2a_bridge/a2a_bridge.py --dispatch '{"query":"ping","intent":"POSITION_QUICK","reply_channel":"cli"}'
# look for: "Success: True" + "status\": 200 + "TASK_STATE_COMPLETED" in response
```

Until that fires, the bridge is half-built. Config can claim "wired" all it wants — the kernel enforces.

## The one thing not obvious from the docs

`systemctl restart aaa-a2a` is REQUIRED after `registerAgentPolicy` patches. The seed-federation block runs at module-load time. Live config reload will not pick up the new policy. Same for canonical-actor set changes — those are also module-load constants.

If you see a 403 referencing an actor that IS in the canonical set, the FIRST diagnostic question is "did this server start before or after I added the policy?"
