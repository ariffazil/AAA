---
name: aaa-a2a-gateway-discovery
description: Inspect and test the aaa-a2a Docker container (A2A gateway for arifOS federation). Use when container is running but you don't know its port, auth, or API format.
triggers:
  - aaa-a2a container running but unknown port
  - need to call A2A API but missing auth headers
  - federation agents show registered: false
  - POST /a2a/message/send returns error about message parts
---

# AAA A2A Gateway Discovery & Testing

## When to use
You need to inspect or test the `aaa-a2a` Docker container (A2A gateway for arifOS federation) and don't know its internals.

## Quick discovery

### 1. Find port
```bash
docker ps --format '{{.Names}} {{.Ports}}'
# → aaa-a2a   0.0.0.0:3001->3000/tcp

curl http://localhost:3001/health
```

### 2. Read server.js inside running container
The container runs Express directly from `/app/server.js`. No build step.
```bash
docker exec aaa-a2a sed -n '1,100p' /app/server.js   # config + routes
docker exec aaa-a2a sed -n '200,400p' /app/server.js  # message/send handler
docker exec aaa-a2a sed -n '400,600p' /app/server.js  # federation manifest
```

### 3. Get auth tokens
```bash
docker inspect aaa-a2a --format '{{range .Config.Env}}{{println .}}{{end}}' | grep -iE "A2A|TOKEN|KEY"
```
Dev fallback (from server.js source): `aaa-a2a-token-dev` / `aaa-a2a-apikey-dev`

### 4. Get federation manifest
```bash
curl http://localhost:3001/.well-known/arifos-federation.json
```

## Correct A2A API call format

```bash
curl -s -X POST http://localhost:3001/a2a/message/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer aaa-a2a-token-dev" \
  -H "x-a2a-key: aaa-a2a-apikey-dev" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "hello"}]
      },
      "agent_id": "hermes"
    }
  }'
```

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `"Each message part must have a kind"` | Missing `"kind": "text"` on parts | Add `"kind": "text"` to each part |
| `401 Unauthorized` | Missing auth headers | Add both `Authorization` and `x-a2a-key` |
| `"-32601 Endpoint /tasks not found"` | Wrong endpoint | Use `/a2a/message/send` not `/tasks` |

## Key architecture facts

- **Port**: 3001 (host) → 3000 (container)
- **Protocol**: A2A v1.0.0 (agentcommunicationprotocol.dev), JSON-RPC 2.0
- **Skills**: `agent-dispatch`, `agent-handoff`, `status-query` — auto-detected by keyword
- **Governance**: F9 anti-hallu check + 888_JUDGE gating on dispatch/handoff skills
- **Vault**: VAULT999 SEAL written async after task completion
- **Replay protection**: nonce + payload hash deduplication, 10 min TTL
- **Container entrypoint**: `node /app/server.js` — raw Express, no build
- **Hermes A2A endpoint**: `http://hermes-agent:3002/tasks` (Docker DNS, no auth from internal network)
- **Hermes dispatch requires**: `agent_id=hermes` in `params` — otherwise falls back to echo mode

## CRITICAL: Docker Bridge Networking — Agents Cannot Be Reached Via Bridge IP

**Problem**: The AAA A2A server runs inside a Docker container on a bridge network. The host machine has IP `172.19.0.1` on the container's bridge network. Agents running on the host (not in containers) cannot be reached via Docker bridge DNS (`hermes-agent`, `openclaw`) from inside the container — `wget` times out even with correct IPs.

**Solution — Two Options**:

### Option A: Host Networking for aaa-a2a (RECOMMENDED)
Change `aaa-a2a` docker-compose to use `network_mode: host`. The container then shares the host's network namespace and can reach host services at `127.0.0.1:PORT`.

```yaml
# docker-compose.yml for aaa-a2a
services:
  aaa-a2a:
    network_mode: host  # replaces ports: mapping
    # remove: ports: ["3001:3000"]
```

Then restart: `docker stop aaa-a2a && docker rm aaa-a2a && docker compose up -d`

Now the AAA A2A server can reach host adapters at `127.0.0.1:18001` (Hermes) and `127.0.0.1:18002` (OpenClaw).

### Option B: Custom HTTP Adapters on Host (Use When Option A Unavailable)
If host networking is not possible, deploy Python HTTP adapters on the host that bridge A2A JSON-RPC to the agent's CLI. See "Custom A2A Adapter Pattern" section below.

---

## Custom A2A Adapter Pattern

When an agent (Hermes, OpenClaw, etc.) doesn't natively speak A2A HTTP JSON-RPC, deploy a Python HTTP adapter on the host that:
1. Accepts A2A `SendMessage` requests at `/.well-known/agent-card.json` and `/a2a/message/send`
2. Converts the request to the agent's native CLI invocation
3. Parses the CLI output back into A2A JSON-RPC response format
4. Returns to the caller

### Hermes Adapter (port 18001)
Hermes uses `hermes chat -q "text" --provider minimax --max-turns 3` (NO `--no-tui` flag — not valid).

```python
#!/root/.hermes/venv/bin/python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, subprocess, uuid, datetime, os

PORT = 18001
HERMES_BIN = "/root/.hermes/venv/bin/hermes"

def a2a_resp(task_id, context_id, text, state="completed"):
    return {
        "jsonrpc": "2.0", "id": task_id,
        "result": {
            "id": task_id, "contextId": context_id,
            "status": {
                "state": state,
                "message": {"role": "agent",
                    "parts": [{"kind": "text", "text": text[:3000]}],
                    "messageId": str(uuid.uuid4()),
                    "taskId": task_id, "contextId": context_id,
                    "timestamp": datetime.datetime.utcnow().isoformat()+"Z"},
            },
            "artifacts": [], "history": [], "kind": "task"
        }
    }

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        cl = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(cl).decode() if cl else "{}"
        try: req = json.loads(body)
        except: self.send_error(400); return
        p = req.get("params", {})
        task_id = p.get("taskId") or f"hm-{uuid.uuid4().hex[:10]}"
        context_id = p.get("contextId") or str(uuid.uuid4())
        msg = p.get("message", {})
        if isinstance(msg, dict):
            text = " ".join(part["text"] for part in msg.get("parts", []) if part.get("kind") == "text")
        else:
            text = str(msg)
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Connection", "close"); self.end_headers()
        try:
            env = os.environ.copy(); env["HERMES_HOME"] = "/root/.hermes"
            result = subprocess.run(
                [HERMES_BIN, "chat", "-q", text, "--provider", "minimax", "--max-turns", "3"],
                capture_output=True, text=True, timeout=55, env=env
            )
            output = result.stdout.strip()[:2000] or result.stderr.strip()[:1000] or "(no output)"
        except subprocess.TimeoutExpired: output = "[timeout after 55s]"
        except Exception as e: output = f"[error: {e}]"
        self.wfile.write(json.dumps(a2a_resp(task_id, context_id, output)).encode())

    def do_GET(self):
        if ".well-known/agent-card.json" in self.path:
            card = {"name": "AAA Hermes ASI", "description": "ASI — Hermes as A2A agent",
                "url": "http://127.0.0.1:18001/", "protocol_version": "1.0.0",
                "capabilities": {"streaming": False, "push_notifications": False},
                "authentication": {"schemes": ["bearer"]},
                "skills": [{"id": "deliberate", "name": "Constitutional Judgment"}], "lane": "ASI"}
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(json.dumps(card).encode())
        else: self.send_error(404)

    def log_message(self, fmt, *args): print(f"[HERMES-A2A] {fmt%args}", flush=True)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Hermes A2A adapter listening on port {PORT}", flush=True)
    server.serve_forever()
```

Save as `/opt/arifOS/a2a-adapters/hermes-a2a.py`, run: `python3 /opt/arifOS/a2a-adapters/hermes-a2a.py &`

### OpenClaw Adapter (port 18002)
OpenClaw uses `openclaw agent -m "text" --session-id <uuid> --json`. Output must be parsed from JSON — key is `result.payloads[0].text`.

```python
# Extract OpenClaw response text from JSON output:
import re
def extract_text(stdout):
    match = re.search(r'\{.*\}', stdout, re.DOTALL)
    if not match: return None
    data = json.loads(match.group())
    payloads = data.get("result", {}).get("payloads", [])
    if payloads and payloads[0].get("text"): return payloads[0]["text"]
    return None
```

CLI invocation: `subprocess.run(["openclaw", "agent", "-m", text, "--session-id", session_id, "--json"], ...)`

### Routing from AAA A2A Server to Adapters
After patching server.js to add routing, the key URLs are:
- Hermes: `http://127.0.0.1:18001/a2a/message/send`
- OpenClaw: `http://127.0.0.1:18002/a2a/message/send`

---

## Hermes A2A CLI Syntax (Critical: No --no-tui)

**CORRECT**: `hermes chat -q "text" --provider minimax --max-turns 3`
**WRONG**: `hermes exec ...` (no such command) and `hermes chat ... --no-tui` (not a valid flag)

Test: `hermes chat -q "Who are you?" --provider minimax --max-turns 2`

## OpenClaw A2A CLI Syntax

**Single turn**: `openclaw agent -m "text" --session-id <uuid> --json`
**Output format**: `{..., "result": {"payloads": [{"text": "...", "mediaUrl": null}], ...}}`

Test: `timeout 120 openclaw agent -m "What is 2+2?" --session-id test-001 --json 2>&1 | grep -v "^\[plugins\]" | python3 -c "..."`

---

## CRITICAL: Hermes dispatch routing patch for server.js

**Symptom**: `POST /a2a/message/send` with `agent_id=hermes` returns `[AAA Gateway] Received: "..."` instead of routing to Hermes.

**Root cause**: `executeTask()` in `server.js` had no Hermes/OpenClaw routing logic. It only did local echo.

**Fix — Add routing blocks to `executeTask`** in `server.js` (~line 389):

```javascript
// After: const task = await storage.upsertTask(...)
// ADD these blocks BEFORE the local echo logic:

// Route to Hermes adapter on host port 18001
if (targetAgent === 'hermes') {
    try {
        const res = await fetch(`http://127.0.0.1:18001/a2a/message/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ jsonrpc: '2.0', id: taskId, method: 'SendMessage',
                params: { message, taskId, contextId } }),
            signal: AbortSignal.timeout(55000)
        });
        const data = await res.json();
        task.status = { state: 'completed', message: data.result?.status?.message };
        await storage.upsertTask(task);
        pushEvents(sessionId, { type: 'TaskCompleted', taskId, result: data.result });
        return;
    } catch (err) {
        console.error('[AAA] Hermes routing failed:', err.message);
    }
}

// Route to OpenClaw adapter on host port 18002
if (targetAgent === 'openclaw') {
    try {
        const res = await fetch(`http://127.0.0.1:18002/a2a/message/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ jsonrpc: '2.0', id: taskId, method: 'SendMessage',
                params: { message, taskId, contextId } }),
            signal: AbortSignal.timeout(55000)
        });
        const data = await res.json();
        task.status = { state: 'completed', message: data.result?.status?.message };
        await storage.upsertTask(task);
        pushEvents(sessionId, { type: 'TaskCompleted', taskId, result: data.result });
        return;
    } catch (err) {
        console.error('[AAA] OpenClaw routing failed:', err.message);
    }
}

// === LOCAL PROCESSING follows (echo/default) ===
```

**Update call sites to pass `agent_id`**:
```javascript
// message/send handler — find: await executeTask(taskId, contextId, message);
// Change to: await executeTask(taskId, contextId, message, params.agent_id);

// message/stream handler — same change
```

**Deploy workflow**:
1. `cp /root/AAA/a2a-server/server.js /root/AAA/a2a-server/server.js.bak4wire`
2. Edit with the patches above
3. `docker cp /root/AAA/a2a-server/server.js aaa-a2a:/app/server.js`
4. `docker restart aaa-a2a`
5. Verify: `docker logs --tail 5 aaa-a2a` → should show "[AAA A2A] Hardened server running on port 3001"

---

## CRITICAL: Minimal container — no curl, no python3, no sed

The `aaa-a2a` container has NONE of the standard tools. Only `node` and `wget` are available.

**Test internal connectivity from aaa-a2a to another container**:
```bash
# DNS resolution
docker exec aaa-a2a python3 -c "import socket; print(socket.gethostbyname('hermes-agent'))"  # FAILS - no python3
docker exec aaa-a2a nslookup hermes-agent  # FAILS - no nslookup

# WORKS - use wget's DNS resolution output
docker exec aaa-a2a wget -q -O- --timeout=5 http://hermes-agent:3002/.well-known/agent-card.json

# Works: find container IP on shared Docker network
docker inspect hermes-agent --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
# Then: docker exec aaa-a2a wget -q -O- --timeout=5 http://<IP>:3002/tasks
```

**Copy files in/out of minimal containers**:
```bash
# Copy FROM container to host (works)
docker exec aaa-a2a cat /app/server.js > /tmp/aaa_server.js

# Copy TO container (works - tee over stdin)
cat /tmp/aaa_server.js | docker exec -i aaa-a2a tee /app/server.js > /dev/null

# Copy single file to container
docker cp /tmp/patch.js aaa-a2a:/tmp/patch.js
docker exec aaa-a2a sh -c "cp /tmp/patch.js /app/server.js"
```

**No python3 available inside aaa-a2a** — for Python tests, run from host or another container.

## Verify dispatch works end-to-end

```bash
# Test Hermes dispatch (should return HOLD_888 for irreversible actions)
curl -s -X POST http://localhost:3001/a2a/message/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer aaa-a2a-token-dev" \
  -H "x-a2a-key: aaa-a2a-apikey-dev" \
  -d '{"jsonrpc":"2.0","id":1,"method":"message/send",
       "params":{"message":{"role":"user","parts":[{"kind":"text","text":"Propose: delete a file. High risk irreversible. Verdict?"}]},"agent_id":"hermes"}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); txt=d['result']['status']['message']['parts'][0]['text']; print('HOLD_888:', 'HOLD_888' in txt)"
```

## Related files
- `/root/AAA/a2a-server/server.js` — source on host (update after patching!)
- `/root/AAA/acp/a2a_client.py` — Python A2A client wrapper
