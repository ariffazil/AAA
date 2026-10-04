# OpenClaw → AAA Wiring: 4-Error Debug Path (2026-08-07)

The exact sequence a fresh A2A dispatch from OpenClaw walked through on 2026-08-07, error-by-error, before reaching `200 TASK_STATE_COMPLETED`.

## Error cascade (in order)

### 1. `400 -32600 "jsonrpc must be \"2.0\""`
Envelope missing `jsonrpc: "2.0"` root field. A2A speaks JSON-RPC 2.0 over HTTP.  
**Fix:** add `jsonrpc`, `id`, `method` at root BEFORE `params`.

### 2. `403 -32001 "Sender actor_id \"openclaw:ingress\" is not canonical"`
The colon-form (`openclaw:ingress`) is not in `CANONICAL_ACTORS` in `federation_envelope.js:266`.  
**Fix:** use `actor_id: "openclaw"` (the canonical short form). Store granular identity in `key_id`.

### 3. `403 -32001 "Agent openclaw has no registered policy — DENY ALL"`
`AGENT_POLICIES` Map is empty for `openclaw`. The policy is registered at code level, not config level.  
**Fix:** add `registerAgentPolicy('openclaw', { ... })` in the seed-federation block of `federation_envelope.js` (line ~492, after `hermes-asi`). Required fields: `agent_role`, `allowed_tools`, `allowed_organs`, `irreversibility_threshold`.

### 4. `403 -32001 "/tasks not in allowed_tools for agent openclaw"`
`allowed_tools` checked against HTTP path literally. Kernel tool names are for dispatch; HTTP path must be listed separately.  
**Fix:** add `'/tasks'` to `allowed_tools` array.

### 5. `400 -32600 "params.message or params.text required"`
Envelope nested too deep (`params.envelope.body.query`).  
**Fix:** flatten to A2A wire shape:
```
params.message.parts[0].text = <query>
params.metadata.intent = <intent>
params.metadata.ceiling = "DISPLAY_ONLY"
```

## 4 files that must align

| File | What |
|---|---|
| `/root/AAA/secrets/did/registry.json` + runtime mirror | DID + public key |
| `/root/AAA/federation/organs.yaml` | EDGE class, ceiling, domains |
| `/root/AAA/a2a/registry/agents.yaml` | Agent card, auth_scheme |
| `/root/AAA/a2a-server/federation_envelope.js` | `registerAgentPolicy()` call |

## Critical: restart required after policy patches

`registerAgentPolicy` runs at module-load time. `systemctl restart aaa-a2a` is mandatory after adding the policy. Live reload does NOT pick up new policies.

## Proof-of-wire

Don't accept config-only verification. The minimal proof:
```bash
python3 a2a_bridge/a2a_bridge.py --dispatch '{"query":"ping","intent":"POSITION_QUICK","reply_channel":"cli"}'
# must show: "Success: True" + "status": 200 + "TASK_STATE_COMPLETED"
```
