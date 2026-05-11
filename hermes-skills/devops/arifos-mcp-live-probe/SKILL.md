---
name: arifos-mcp-live-probe
description: Live-probe an arifOS federation MCP endpoint (8080-8083) via JSON-RPC over streamable-http. Tests transport, tool registry, session binding, and constitutional gating.
tags: [arifOS, MCP, JSON-RPC, streamable-http, probe, debug]
version: 2026.05.11
---

# arifOS MCP Live Probe

## Trigger
Any task that requires verifying an arifOS federation MCP server is genuinely alive, responding correctly, and enforcing constitutional tool gates — not just returning HTTP 200 from a `/health` endpoint.

## Context
arifOS MCP servers (ports 8080–8083) use FastMCP streamable-http transport. Naive curl POSTs return empty responses without proper headers. Tool calls are gated by stage (111/333/555/666/777/888/999) and return nine_signal envelopes.

## Required Headers
```
Content-Type: application/json
Accept: application/json          # REQUIRED — without this, 406 is returned
```

## Step-by-Step Probe Sequence

### Step 1 — Transport health (no auth needed)
```bash
curl -s --max-time 10 http://localhost:8080/health
# Expected: {"status":"ok","transport":"streamable-http","version":"..."}
```

### Step 2 — Tool registry (public, no session)
```bash
curl -s --max-time 10 -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
tools=[t['name'] for t in d['result']['tools']]
print(f'Tools count: {len(tools)}')
print('Tools:', ', '.join(sorted(tools)))
"
```

### Step 3 — Session init (required before gated tools)
```bash
SESSION_ID=$(curl -s --max-time 10 -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":2,"params":{"name":"arif_session_init","arguments":{"mode":"init","actor_id":"hermes-vps-probe","ack_irreversible":false}}}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result']['session_id'])" 2>/dev/null)
echo "Session: $SESSION_ID"
# Expected: session_id like "SEAL-xxxxxxxxxxxx"
```

### Step 4 — Test public tools (stage 111/333/555 — no actor binding needed)
```bash
# arif_sense_observe (stage 111) — search without args
curl -s --max-time 10 -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":3,"params":{"name":"arif_sense_observe","arguments":{}}}' \
  | python3 -m json.tool 2>/dev/null | head -40
# Expected: Status=SEAL, nine_signal=SELAMAT

# arif_mind_reason (stage 333)
curl -s --max-time 10 -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":4,"params":{"name":"arif_mind_reason","arguments":{"query":"test"}}}'
# Expected: Status=SEAL, nine_signal=SELAMAT

# arif_memory_recall (stage 555)
curl -s --max-time 10 -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":5,"params":{"name":"arif_memory_recall","arguments":{"query":"arifOS"}}}'
# Expected: Status=OK, nine_signal=SELAMAT, results count > 0
```

### Step 5 — Test authenticated tools (stage 666+)
```bash
# arif_heart_critique (stage 666 ASI) — without actor, returns VOID
curl -s --max-time 10 -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":6,"params":{"name":"arif_heart_critique","arguments":{"surface":"probe","depth":"shallow"}}}'
# Expected: Status=VOID, Output policy=DOMAIN_VOID (correct auth gating)

# arif_judge_deliberate (stage 888) — without actor binding, returns empty
curl -s --max-time 10 -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":7,"params":{"name":"arif_judge_deliberate","arguments":{}}}'
# Expected: empty response (correct — requires authenticated actor)

# arif_vault_seal (stage 999) — same
# Expected: empty response (correct — requires 999 auth)
```

### Step 6 — Test mode validation (tools enforce mode arguments)
```bash
# arif_kernel_route with no args — should return HOLD with correct mode
curl -s --max-time 10 -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":8,"params":{"name":"arif_kernel_route","arguments":{}}}'
# Expected: Status=HOLD, Output policy=DOMAIN_HOLD, nine_signal=RETAK
```

## Expected Result Summary

| Tool | Stage | Without session | With session |
|------|-------|-----------------|--------------|
| `arif_session_init` | 000 | SEAL | — |
| `arif_sense_observe` | 111 | SEAL | SEAL |
| `arif_mind_reason` | 333 | SEAL | SEAL |
| `arif_memory_recall` | 555 | OK | OK |
| `arif_heart_critique` | 666 | VOID | (needs actor) |
| `arif_kernel_route` | 444 | HOLD (no args) | HOLD |
| `arif_judge_deliberate` | 888 | empty | (needs actor) |
| `arif_vault_seal` | 999 | empty | (needs 999 auth) |

## Port Map
- arifOS: 8080
- GEOX: 8081
- WEALTH: 8082
- WELL: 8083

## Lessons Learned (DITEMPA BUKAN DIBERI)
1. **Accept header is mandatory** — without it, FastMCP 3.2.4 returns HTTP 406 on all POSTs. This is the #1 reason probes fail silently.
2. **Session init is required before most meaningful tools** — but stage 111/333/555 tools work without it (public stage).
3. **Auth-gated tools (888/999) return empty HTTP responses** when called without proper actor binding — not 403, not error, just empty body. This is correct constitutional behavior.
4. **nine_signal values are verified:** SEAL=SELAMAT, HOLD=RETAK, VOID has no nine_signal, domain responses vary.
5. **GEOX/WEALTH/WELL health endpoints return JSON but MCP endpoints need JSON-RPC** — don't assume health=working MCP. Always probe `/mcp` with `tools/list`.