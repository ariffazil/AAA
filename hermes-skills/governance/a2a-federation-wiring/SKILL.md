---
name: a2a-federation-wiring
description: Wire A2A v1.0.0 protocol between Hermes (ASI) and OpenClaw (AGI) on VPS af-forge. Active 2026-05-04, updated with Docker bridge IP fix and endpoint split-brain diagnosis 2026-05-06.
triggers:
  - Setup A2A between Hermes and OpenClaw
  - Debug A2A routing (localhost:3001)
  - Add new agent to A2A mesh
  - A2A dispatch failing (fetch failed, local echo fallback)
---

# a2a-federation-wiring: ASI ↔ AGI A2A Mesh

## Topology

```
User / External Caller
         │
         ▼
http://localhost:3001   ← AAA A2A Gateway (Docker, host network)
│   Bearer: aaa-a2a-token-dev
│   x-a2a-key: aaa-a2a-apikey-dev
│
├── agent_id: "hermes"  →  http://127.0.0.1:18001  →  Hermes A2A Adapter (Python)
│                          calls: hermes chat -q "<text>" --provider minimax
│
└── agent_id: "openclaw" →  http://127.0.0.1:18002  →  OpenClaw A2A Adapter (Python)
                             calls: openclaw agent -m "<text>" --session-id <uuid> --json

Adapter logs:
  /var/log/hermes-a2a.log
  /var/log/openclaw-a2a.log
```

## Key Files

- `/opt/arifOS/a2a-adapters/hermes-a2a.py` — Hermes adapter, port 18001
- `/opt/arifOS/a2a-adapters/openclaw-a2a.py` — OpenClaw adapter, port 18002
- `/root/AAA/a2a-server/server.js` — patched to route by agent_id
- `/root/AAA/a2a-server/docker-compose.yml` — host network mode (CRITICAL)

## Agent IDs & Ports

| agent_id | Agent | CLI Command | Adapter Port |
|----------|-------|-------------|--------------|
| `"hermes"` | Hermes ASI | `hermes chat -q "<text>" --provider minimax` | 18001 |
| `"openclaw"` | OpenClaw AGI | `openclaw agent -m "<text>" --session-id <uuid> --json` | 18002 |

## A2A Dispatch Example

```bash
curl -X POST http://localhost:3001/a2a/message/send \
  -H "Authorization: Bearer aaa-a2a-token-dev" \
  -H "x-a2a-key: aaa-a2a-apikey-dev" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", "id": "task-001",
    "method": "SendMessage",
    "params": {
      "message": {"role": "user", "parts": [{"kind": "text", "text": "Your question here"}]},
      "taskId": "task-001",
      "contextId": "ctx-001",
      "agent_id": "hermes"
    }
  }'
```

## Critical Lessons

1. **Docker bridge blocks host access** — aaa-a2a MUST use `network_mode: host` in docker-compose.yml. Without it, wget from inside the container cannot reach host ports 18001/18002. This was the single biggest blocker.
2. **ENDPOINT SPLIT-BRAIN** — The AAA Gateway dispatches via `/a2a/message/send` (non-standard A2A). The Python adapters ONLY implement `/tasks`. Direct adapter calls work; gateway-mediated calls fail. Fix: add `/a2a/message/send` alias in adapters (see Adapter Patch section below).
3. **Docker bridge IP is unreachable from host-mode container** — server.js defaults to `http://172.19.0.1:18001` but `172.19.0.x` is Docker's internal bridge subnet. A container in `network_mode: host` has NO bridge interface — it must use `127.0.0.1`. Symptom: `fetch failed` in gateway logs despite adapters running. Fix: `sed -i 's|172\.19\.0\.1|127\.0.0.1|g' /app/server.js` inside the container.
4. **Local echo fallback masks real failures** — When downstream adapter is unreachable, the gateway falls back to local echo and returns `state: "completed"` with the echoed text. You cannot tell from the HTTP response alone whether the real agent ran. Always check: (a) adapter logs at `/var/log/hermes-a2a.log`, (b) `docker logs aaa-a2a` for `fetch failed` errors.
5. **Token discovery** — run `docker logs aaa-a2a | grep -i token` to find the bearer token and API key at startup.
6. **OpenClaw output parsing** — the `--json` flag outputs the JSON mixed with plugin loading logs. Use regex to extract: `re.search(r'\{.*\}', stdout, re.DOTALL)`. Then read `result.payloads[0].text`.
7. **OpenClaw session ID** — always pass `--session-id <uuid>` to avoid session collisions. Each A2A call gets a unique session.
8. **Hermes chat -q** — correct command is `hermes chat -q "<text>" --provider minimax`. Do NOT use `--no-tui` (invalid flag) or `hermes exec` (command doesn't exist).
9. **Adapter startup** — must run as background processes with nohup. Cannot foreground. Logs go to `/var/log/hermes-a2a.log` and `/var/log/openclaw-a2a.log`.
10. **Killing adapters** — use `ss -tlnp | grep 18001` to find PID, then `kill -9 <pid>`. `pkill` works but always verify port is free before restarting.
11. **AAA A2A server routing** — server.js `executeTask` routes by `targetAgent` field. When adding a new agent, you must: (a) add the adapter, (b) add the route in server.js using `127.0.0.1` (NOT `172.19.0.1`), (c) `docker cp server.js aaa-a2a:/app/server.js && docker restart aaa-a2a`.
12. **Adapter vs systemd** — adapters currently run via nohup, not systemd. Systemd unit files exist at `/opt/arifOS/a2a-adapters/*.service` but have not been daemon-reload'd. Restart after crash: manually kill old PID and nohup restart.
13. **VAULT999 404 inside container** — the gateway cannot reach `http://vault999:8100` from inside the container (even in host mode, Docker's DNS naming doesn't always resolve). Falls back to `/root/.arifos/vault.jsonl` on the host filesystem. Vault writes are safe but not canonical.
14. **POST /tasks returns -32601 "Method not found"** — catch-all 404 from server.js line ~1082. Possible causes: (a) Auth failure → authMiddleware returns 401 before route (test with `-H "Authorization: Bearer aaa-a2a-token-dev" -H "x-a2a-key: aaa-a2a-apikey-dev"`); (b) Env vars empty in container → server uses dev fallback tokens. Check: `docker exec aaa-a2a sh -c 'echo "TOKEN: $A2A_TOKEN KEY: $A2A_API_KEY"'`; (c) Route exists but middleware chain rejects before handler; (d) Wrong HTTP method or missing Content-Type header. Dev tokens: `Bearer=aaa-a2a-token-dev`, `x-a2a-key=aaa-a2a-apikey-dev`.
15. **Both adapters must run simultaneously** — `hermes-a2a.py` on 18001 AND `openclaw-a2a.py` on 18002. A missing openclaw-a2a adapter means OpenClaw-bound tasks fail with `fetch failed`.
16. **Federation manifest agents are STANDBY, not live** — The manifest at `http://127.0.0.1:3001/.well-known/arifos-federation.json` registers 6 agents but internal ones (aaa-architect, aaa-engineer, aaa-auditor) show `role: "internal"` and `state: "standby"`. They need to be spawned as running processes to become ONLINE.

## Diagnostic Sequence (always run in this order)

```bash
# Step 1 — Verify adapters are listening on host
ss -tlnp | grep -E "18001|18002"

# Step 2 — Test adapter DIRECTLY (bypasses gateway)
curl -s -X POST http://127.0.0.1:18001/tasks \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test","method":"tasks/send","params":{"message":{"role":"user","parts":[{"kind":"text","text":"ping"}]},"taskId":"test","contextId":"test-ctx"}}'

# Step 3 — Test /tasks endpoint on AAA gateway (A2A v1.0.0 spec)
curl -s -X POST http://127.0.0.1:3001/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer aaa-a2a-token-dev" \
  -H "x-a2a-key: aaa-a2a-apikey-dev" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tasks/send","params":{"message":{"role":"user","parts":[{"kind":"text","text":"ping"}]},"taskId":"test-fix-001"}}'
# If -32601 "Method not found" → auth failure or route ordering issue. Check:
docker exec aaa-a2a grep -n "app\.(post|get|use)" /app/server.js | grep -A1 "/tasks"

# Step 4 — Test via gateway /a2a/message/send (non-standard A2A)
curl -s -X POST http://localhost:3001/a2a/message/send \
  -H "Authorization: Bearer aaa-a2a-token-dev" \
  -H "x-a2a-key: aaa-a2a-apikey-dev" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test","method":"SendMessage","params":{"message":{"role":"user","parts":[{"kind":"text","text":"ping"}]},"taskId":"test","contextId":"test-ctx","agent_id":"hermes"}}'

# Step 5 — Check gateway logs for "fetch failed" or "172.19"
docker logs aaa-a2a 2>&1 | grep -E "fetch|172\.19|hermes|error" | tail -20

# Step 6 — Check adapter logs
tail -5 /var/log/hermes-a2a.log
```

If Step 2 succeeds but Step 3 fails → POST /tasks auth/route issue (see Lesson 14).
If Step 3 succeeds but Step 4 fails → endpoint mismatch or IP routing bug (see Lesson 2).
If Step 4 returns state "completed" but contains "falling back to local echo" → adapter unreachable (check IP/port).

## Adapter Patch — Add /a2a/message/send endpoint alias

Both Python adapters only handle `/tasks`. The gateway calls `/a2a/message/send`. Patch to add alias:

```python
# In hermes-a2a.py, find do_POST():
# Add this at the start of do_POST(), before path matching:
if self.path == "/a2a/message/send":
    self.path = "/tasks"

# Then existing "/tasks" handler processes normally.
```

Restart adapter after patching:
```bash
kill $(ss -tlnp | grep 18001 | sed 's/.*pid=\([0-9]*\).*/\1/')
nohup /root/.hermes/venv/bin/python3 /opt/arifOS/a2a-adapters/hermes-a2a.py >> /var/log/hermes-a2a.log 2>&1 &
```

## Gateway Routing Fix (if seeing fetch failed for adapters)

```bash
# Check what IP the gateway is using
docker exec aaa-a2a grep -n "172\.19\.0\.1\|18001\|18002" /app/server.js | head -10

# Fix: replace Docker bridge IP with 127.0.0.1
docker exec aaa-a2a sed -i 's|172\.19\.0\.1|127\.0\.0\.1|g' /app/server.js

# Verify the change
docker exec aaa-a2a grep -n "18001\|18002" /app/server.js

# Restart gateway
docker restart aaa-a2a

# Re-test via gateway (Step 3 above)
```

## Adapter Restart Sequence

```bash
# 1. Find and kill old adapter
kill -9 $(ss -tlnp | grep 18001 | sed 's/.*pid=\([0-9]*\).*/\1/') 2>/dev/null

# 2. Restart Hermes adapter
/root/.hermes/venv/bin/python3 /opt/arifOS/a2a-adapters/hermes-a2a.py >> /var/log/hermes-a2a.log 2>&1 &

# 3. Restart OpenClaw adapter
/root/.hermes/venv/bin/python3 /opt/arifOS/a2a-adapters/openclaw-a2a.py >> /var/log/openclaw-a2a.log 2>&1 &

# 4. Verify
sleep 2 && ss -tlnp | grep -E "18001|18002"
```

## AAA A2A Server Routing (server.js patch reference)

When adding a new agent_id to the mesh, add a case block inside `executeTask`. **CRITICAL: Use `127.0.0.1` NOT Docker bridge IPs:**

```javascript
// In server.js executeTask() function — add route:
case 'your-agent-id':
  targetUrl = 'http://127.0.0.1:<your-port>';  // host port, NOT 172.19.0.x
  break;
```

Then deploy: `docker cp server.js aaa-a2a:/app/server.js && docker restart aaa-a2a`

## Agent Card Endpoints

- Hermes: `http://127.0.0.1:18001/.well-known/agent-card.json`
- OpenClaw: `http://127.0.0.1:18002/.well-known/agent-card.json`
- AAA Gateway: `http://localhost:3001/.well-known/agent-card.json`

## Telegram Ownership

| Agent | Telegram Bot | Token |
|-------|-------------|-------|
| Hermes (ASI) | @ASI_arifos_bot | NousResearch OAuth |
| OpenClaw (AGI) | @AGI_ASI_bot | 8149595687:* |
