---
name: hermes-docker-debug
description: Debug and recover Hermes Agent Docker container — extractText crash, Docker networking, Python TCPServer EADDRINUSE
category: devops
tags: [hermes, docker, a2a, debugging, networking]
created: 2026-05-07
updated: 2026-05-07
owner: arif
---

# Hermes Agent Docker — Debug & Recovery

## Context
Hermes Agent (NousResearch Hermes) has TWO distinct runtime components:

1. **Host-side brain** — The real agent: `~/.hermes/` on the host. This is where config.yaml, workspace, skills, memory, sessions, and the main agent process live. The container knows nothing about this.
2. **Container A2A relay** — `hermes-agent:v1.0.3` container on port 3002. A thin Express.js A2A server that routes tasks TO the host-side agent via HTTP. It is NOT the agent itself — just a message relay.

**Key insight:** Debugging "Hermes agent" problems (model config, skills, session issues, memory) requires looking at `~/.hermes/` on the host, NOT the container. The container is a disposable relay.

### Workspace locations
| Layer | Path |
|-------|------|
| Host agent workspace | `/root/.hermes/` |
| Host agent config | `/root/.hermes/config.yaml` |
| Host agent .env (keys) | `/root/.hermes/.env` |
| Container app | `/app/src/server.js` (thin A2A relay only) |

## DeepSeek Provider Addition (2026-05-11)

When adding a new model provider to Hermes:
1. API key goes in `~/.hermes/.env` as `DEEPSEEK_API_KEY=sk-...`
2. Provider + model go in `~/.hermes/config.yaml` under `providers:` and `model:` / `fallback_model:`
3. Test auth with: `curl -X POST https://api.deepseek.com/chat/completions -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"test"}],"max_tokens":5}'`

### DeepSeek model quirks
- `deepseek-chat` and `deepseek-reasoner` both resolve to `deepseek-v4-flash` at API level
- `deepseek-reasoner` surfaces `reasoning_content` field (visible chain-of-thought) but same underlying flash model
- `deepseek-v4-flash` and `deepseek-v4-pro` are the explicit model IDs
- OpenAI-compatible format — drop-in for any OpenAI-compatible wrapper

## Common Crash Pattern

## Common Crash Pattern

### Symptom
Hermes agent returns nothing — AAA gateway returns `HOLD_888` error response instead of a real verdict. Container shows as `(unhealthy)`.

### Root Cause
`extractText()` in `server.js` crashes when A2A payload has malformed `parts`:
- `parts` is an object `{kind:'text',text:'...'}` instead of array `[{kind:'text',text:'...'}]`
- `.map()` on non-array throws `TypeError`
- `text.toLowerCase()` then throws `Cannot read properties of undefined`

### Two-Part Fix

**Fix 1 — `extractText()` in `/app/src/server.js`:**
```javascript
function extractText(candidate) {
  if (typeof candidate === 'string') return candidate;
  if (candidate && candidate.message && Array.isArray(candidate.message.parts)) {
    return candidate.message.parts.map(function(p) { return (p && p.text) || ''; }).join(' ').trim();
  }
  if (candidate && candidate.message && typeof candidate.message.text === 'string') {
    return candidate.message.text;
  }
  if (candidate && typeof candidate.text === 'string') return candidate.text;
  return '';  // was: JSON.stringify(candidate) — never return undefined
}
```

**Fix 2 — `deliberation()` guard in `/app/src/server.js`:**
```javascript
function deliberation(candidate, taskId, contextId) {
  if (!candidate) return { verdict: VERDICT.HOLD_888, rationale: 'No candidate — awaiting human input', confidence: 0.0 };
  var text = extractText(candidate);
  if (!text) return { verdict: VERDICT.HOLD_888, rationale: 'Empty message — awaiting human input', confidence: 0.0 };
  var lower = text.toLowerCase();
  // ...
}
```

**Apply fix:**
```bash
# Extract server.js from container
docker exec hermes-agent cat /app/src/server.js > /tmp/hermes_server.js

# Edit /tmp/hermes_server.js with patches above

# Copy back and restart
docker cp /tmp/hermes_server.js hermes-agent:/app/src/server.js
docker restart hermes-agent
```

**Verify:**
```bash
curl -s -X POST http://127.0.0.1:3002/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hermes-a2a-token-dev" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tasks/send","params":{"message":{"text":"test"},"skill":"888-judgment"}}'
# Should return verdict: SEAL with confidence
```

## Docker Container Networking

### Host → Container
- From host: `http://127.0.0.1:3002` (docker-proxy maps to container port 3002)
- `host.docker.internal` does NOT work inside container — use Docker bridge gateway instead

### Container → Host
- From inside other containers: `http://172.19.0.1:PORT` (Docker bridge gateway)
- Example: from `aaa-a2a` container → reach hermes-agent at `http://172.19.0.3:3002`
- Add to docker-compose service:
  ```yaml
  extra_hosts:
    - "host.docker.internal:host-gateway"
  ```
  (Note: `host-gateway` literal — not an IP — is the Docker magic DNS)

### Container → Container
- Service name as hostname: `http://hermes-agent:3002` (if on same docker network)
- Container IP: `172.19.0.x` (check via `docker inspect hermes-agent | grep IPAddress`)

## Python TCPServer EADDRINUSE Recovery

### Symptom
gateway-relay.py (or any Python HTTPServer) crashes with:
```
OSError: [Errno 98] Address already in use
```
`ss -tlnp` shows nothing on the port, but rebind fails immediately.

### Fix
Add `SO_REUSEADDR` before `serve_forever()`:
```python
class Handler(BaseHTTPRequestHandler):
    pass

PORT = 18001
server = HTTPServer(("0.0.0.0", PORT), Handler)
server.allow_reuse_address = True  # Add this BEFORE serve_forever
server.serve_forever()
```

## Docker Healthcheck Fix

If container shows `(unhealthy)` but app responds:
```bash
# Check Docker healthcheck status
docker inspect hermes-agent | grep -A 20 Health

# Verify app responds
docker exec hermes-agent wget -q -O- --timeout=5 http://localhost:3002/health
# Should return {"status":200} even if Docker healthcheck fails
```
