---
name: docker-nodejs-crash-patch
description: Extract, patch, and redeploy a Node.js server running inside a Docker container — when you can't use docker exec -it or edit-in-place
tags: ["devops", "docker", "node.js", "debugging", "hotfix"]
related_skills: ["openclaw-gateway-restart-loop"]
category: devops
---

# docker-nodejs-crash-patch

Debug and hot-patch a crashing Node.js server inside a Docker container when direct edit access isn't available.

## Symptoms

- Container keeps restarting or returning HTTP 500
- Error: `TypeError: Cannot read properties of undefined (reading 'toLowerCase')` or similar null/undefined crash
- Container has no `curl`, `vi`, or editor available
- `docker exec <container> sed` or `docker exec <container> cat > file` don't work cleanly

## Workflow

### Step 1 — Extract the source to host

```bash
docker exec <container> cat /path/to/server.js > /tmp/server.js
# or if cat redirect doesn't work:
docker cp <container>:/path/to/server.js /tmp/server.js
```

### Step 2 — Patch locally on host

Use `patch` tool or editor to fix the crash. Key patterns:

**Null/undefined guard in text extraction:**
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
  return '';  // NEVER return undefined
}
```

**Null guard before calling extracted text:**
```javascript
function deliberation(candidate, taskId, contextId) {
  if (!candidate) return { verdict: VERDICT.HOLD_888, rationale: 'No candidate', confidence: 0.0 };
  var text = extractText(candidate);
  if (!text) return { verdict: VERDICT.HOLD_888, rationale: 'Empty message', confidence: 0.0 };
  var lower = text.toLowerCase();
  // ...
}
```

### Step 3 — Copy patched file into container

```bash
docker cp /tmp/server.js <container>:/path/to/server.js
```

### Step 4 — Restart the container

```bash
docker restart <container>
sleep 3
```

### Step 5 — Verify (without curl)

If container has no curl:
```bash
# Node.js built-in HTTP check
docker exec <container> node -e "const http=require('http');http.get('http://localhost:PORT/health',(r=>console.log(JSON.stringify({status:r.statusCode}))))"

# wget as fallback
docker exec <container> wget -q -O- --timeout=5 http://localhost:PORT/health
```

From host:
```bash
curl -s --max-time 5 http://127.0.0.1:PORT/health
```

## Key Rules

1. **Never return `undefined`** from extraction/parsing functions — return `''` or a safe default
2. **Guard at entry point** of any function that calls `.toLowerCase()`, `.split()`, `.map()` on extracted data
3. **Wait for port** after restart — give the server 3-5 seconds to bind before health-checking
4. **`docker cp`** works reliably; `docker exec cat >` redirect from outside is unreliable

## Common Crash Patterns

| Pattern | Fix |
|---------|-----|
| `text.toLowerCase()` on `undefined` | Null guard before call; `extractText` returns `''` not `undefined` |
| `parts.map()` when `parts` is object not array | `Array.isArray(candidate.message.parts)` guard |
| `candidate.message.parts[0].text` when parts is `null` | `(p && p.text) \|\| ''` guard in map |
| Missing `message` field in JSON-RPC params | Check `params.message` exists before `extractText(candidate.message)` |

## Verification Checklist

```bash
# 1. Source file patched in container
docker exec <container> grep -n "Array.isArray\|if (!text)" /path/to/server.js

# 2. Container is running
docker ps | grep <container>

# 3. Process responding
docker exec <container> node -e "const http=require('http');http.get('http://localhost:PORT/health',(r=>process.stdout.write(r.statusCode+'\n')))"

# 4. End-to-end JSON-RPC test from host
curl -s -X POST http://127.0.0.1:PORT/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tasks/send","params":{"message":{"text":"test"}}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['status']['state'])"
# expected: completed
```
