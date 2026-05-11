---
name: arifos-mcp-chain-debug
description: Systematic inspection chain for debugging arifOS MCP tool chains — trace from tool name to handler to runtime dependencies
tags: [arifOS, MCP, debug, inspection]
last_updated: 2026-04-29
---

# arifOS MCP Chain Debug — Systematic Tool Inspection

## Trigger
Debugging any MCP tool that doesn't behave as documented on arifOS stack (arifOS MCP server in Docker on VPS).

## Problem Pattern
Tool appears in docs/registry but returns stub results, wrong data, or crashes.

## 8-Step Inspection Chain

### Step 1 — Find the tool's file
```bash
# Search for the tool function definition
grep -rn "def arif_<tool_name>" /root/arifOS/arifosmcp/

# Check if there's a compatibility shim (e.g. memory_recall.py → memory.py)
cat /root/arifOS/arifosmcp/tools/<tool_name>.py
```

### Step 2 — Check if tool is registered in MCP server
```bash
# Check tool families in agents_66.py
grep -n "TOOL_FAMILIES\|EXECUTION_TOOLS\|META_TOOLS\|PERCEPTION_TOOLS" /root/arifOS/arifosmcp/agents_66.py | head -10

# Search for the exact tool name in agents_66.py
grep -n "tool_name\|E03_memory\|M01_" /root/arifOS/arifosmcp/agents_66.py | grep -i "memory"
```

### Step 3 — Check unified_server.py import chain
```bash
# Check what's imported in the runtime server
grep -n "agents_66\|memory_engine\|public_registry" /root/arifOS/arifosmcp/unified_server.py

# Check tools/__init__.py exports
cat /root/arifOS/arifosmcp/tools/__init__.py
```

### Step 4 — Determine sync vs async
```python
# If tool handler is async:
async def _handler_e03_memory(agent_id: str, input_data: Any) -> Any:
    result = await memory_engine.execute(operation, memory, tier)
    return {"result": result}

# _register_tool in agents_66.py wraps it correctly:
@governed_tool
async def governed_wrapped_handler(req: dict[str, Any]):
    if inspect.iscoroutinefunction(handler):
        return await handler(name, req)
    return handler(name, req)  # sync for non-async
```

### Step 5 — Check runtime env vars inside container
```bash
# Critical env vars for arifOS stack
docker exec arifosmcp sh -c 'echo "DATABASE_URL=$DATABASE_URL"; echo "QDRANT_URL=$QDRANT_URL"; echo "OLLAMA_URL=$OLLAMA_URL"; echo "ARIFOS_VAULT_URL=$ARIFOS_VAULT_URL"'

# Check pip packages
docker exec arifosmcp sh -c "pip list 2>&1" | grep -iE 'asyncpg|psycopg|qdrant|httpx'
```

### Step 6 — Check container network reachability
```bash
# Test Ollama from inside arifosmcp container
docker exec arifosmcp sh -c "curl -s http://ollama:11434/api/embeddings -X POST -d '{\"model\":\"bge-m3\",\"prompt\":\"test\"}' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d.get(\"embedding\",[])))'"

# Test Qdrant
docker exec arifosmcp sh -c "curl -s http://qdrant:6333/collections | python3 -c 'import json,sys; print([c[\"name\"] for c in json.load(sys.stdin).get(\"result\",{}).get(\"collections\",[])])'"
```

### Step 7 — Check Postgres schema
```bash
# IMPORTANT: Use gosu postgres — plain psql may not be in PATH
docker exec postgres sh -c 'gosu postgres psql -U arifos_admin -d vault999 -c "\dt"'
docker exec postgres sh -c 'gosu postgres psql -U arifos_admin -d vault999 -c "SELECT COUNT(*) FROM memory_store;"'

# Schema inspection
docker exec postgres sh -c 'gosu postgres psql -U arifos_admin -d vault999 -c "\d memory_store"'
```

### Step 8 — Check module import health
```bash
# Try importing the module inside the container
docker exec arifosmcp sh -c "python3 -c 'from arifosmcp.memory_engine import MemoryEngine' 2>&1"
```

## Common Blockers on arifOS Stack

| Blocker | Symptom | Fix |
|---------|---------|-----|
| `asyncpg` not installed | `ModuleNotFoundError` on import | `pip install asyncpg` in Dockerfile or container |
| `memory_store` table missing | `INSERT INTO memory_store` fails | Run CREATE TABLE migration |
| `DATABASE_URL` empty | `create_pool(None)` fails | Set env var in docker-compose or code default |
| Tool is dead stub | Returns `[]` always | Find actual registered tool in agents_66.py |
| Wrong container hostname | `curl: (7) Failed to connect` | Use docker internal DNS: `ollama`, `qdrant`, `postgres` |

## Critical: Container `docker exec` Gotchas

The arifosmcp container is a minimal image. These tools do NOT exist inside it:
- `ps`, `grep`, `awk`, `sed`, `netstat`, `ss`, `wget`, `curl` — NOT available
- `psql` without `gosu postgres` prefix — may not be in PATH

**What DOES work inside arifosmcp container:**
```bash
# Python is available (python3)
docker exec arifosmcp python3 -c "import socket; print('ok')"

# Socket check via Python
docker exec arifosmcp python3 -c "
import socket
for port in [8080, 8083, 3000]:
    s = socket.socket()
    try:
        s.connect(('localhost', port))
        print(f'Port {port}: OPEN')
    except: print(f'Port {port}: CLOSED')
    s.close()
"

# HTTP request via Python urllib
docker exec arifosmcp python3 -c "
import urllib.request
r = urllib.request.urlopen('http://localhost:8080/health', timeout=3)
print(f'HTTP {r.status}')
"

# Read files
docker exec arifosmcp sh -c 'cat /proc/1/cmdline'   # PID 1 command
docker exec arifosmcp sh -c 'ls /proc/'             # process list

# Check file existence and content
docker exec arifosmcp sh -c 'ls -la /usr/local/bin/startup.sh'
docker exec arifosmcp sh -c 'sed -n "11p" /app/arifosmcp/runtime/tools.py'

# Check line counts (no grep, use python)
docker exec arifosmcp python3 -c "
with open('/app/arifosmcp/runtime/tools.py') as f:
    print(len(f.readlines()), 'lines')
"
```

**NEVER use semicolons in `docker exec sh -c '...'` inline commands** — the semicolon terminates the shell command prematurely. Use separate `docker exec` calls or a Python script file instead.

**`asyncio.run()` is required** inside the container for async operations:
```bash
docker exec -e PYTHONPATH=/tmp/pylibs:/app arifosmcp python3 -c "
import asyncio
from arifosmcp.memory_engine import MemoryEngine

async def test():
    engine = MemoryEngine(
        postgres_url='postgresql://arifos_admin:PASS@postgres:5432/vault999',
        qdrant_url='http://qdrant:6333',
        ollama_url='http://ollama:11434'
    )
    result = await engine.retrieve('query', tier='working', limit=3)
    print(result)

asyncio.run(test())
"
```

**MemoryEngine signature (ARGH zero-indexed, NOT env vars by name):**
```python
MemoryEngine(postgres_url, qdrant_url, ollama_url, embedding_model, supabase_url, supabase_key)
# postgres_url is the FIRST positional arg — NOT "DATABASE_URL"
# It takes a postgresql:// URI directly
```

### MCP HTTP/SSE Transport (critical for direct JSON-RPC calls)
The arifOS MCP server requires BOTH Accept headers:
```bash
curl -s -N http://127.0.0.1:8080/mcp -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
```
Without `text/event-stream` in Accept, returns `406 Not Acceptable`.

Output is SSE-wrapped JSON: `event: message\ndata: {...json...}` — extract with:
```bash
curl -s -N ... | grep -o '"name":"[^"]*"'   # count tools
curl -s -N ... | python3 -c "import sys,json; d=json.load(sys.stdin); print(d)"  # full parse
```

## Critical: Deployed Server vs Local Repo Divergence
The live VPS server (`arifos.arif-fazil.com/mcp`) may run a DIFFERENT version of
`arifosmcp/runtime/tools.py` than the local repo. Key symptom: live responses have
nine_signal at TOP LEVEL but local code analysis suggests it should be nested.

**Why this happens:** The MCP server promotes `result.nine_signal` → top-level
in its HTTP handler before returning. Local code that reads `response.get("nine_signal")`
at top level will find it on live but miss it in local unit tests.

**Rule: Always test against live endpoint first, then verify local code matches.**
```bash
# Live server nine_signal response format (confirmed working):
curl -s -N https://arifos.arif-fazil.com/mcp \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"arif_ops_measure","arguments":{"mode":"status"}}}' \
  2>&1 | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('nine_signal','MISSING'))"
```

## Pre-existing Undefined Names (found 2026-04-29 audit)
These exist in the codebase and are NOT from recent changes — do NOT "fix" them
as part of unrelated bug hunts; they require targeted refactors:
- `ThreatTier` — used at tools.py:2340 (needs import from core.threat)
- `VerdictCode` — used at tools.py:3408-3437
- `c_verdict` — used throughout tools.py:3408-3445
- `candidate` — used at tools.py:3426-3428
- `epistemic` — used at tools.py:3430
- `thermo` — used at tools.py:3434
- `amanah` — used at tools.py:3436
- `contract` — used at tools.py:3437-3441
- Duplicate dict key `"verdict"` — tools.py:4612-4614 (second overwrites first)

## Common Blockers on arifOS Stack
- `/root/arifOS/arifosmcp/agents_66.py` — tool registry + handlers (lines ~735-1337)
- `/root/arifOS/arifosmcp/unified_server.py` — FastMCP server factory
- `/root/arifOS/arifosmcp/memory_engine.py` — MemoryEngine class
- `/root/arifOS/arifosmcp/tools/memory.py` — dead `arif_memory_recall` stub
- `/root/arifOS/arifosmcp/tools/__init__.py` — tool exports
- `/root/arifOS/arifosmcp/constitutional_map.py` — CANONICAL_TOOLS floor specs

## Rule
**Never patch first. Always test live endpoint first** — the deployed server may run
a different version of tools.py than local repo. Local code analysis alone can be
misleading. Verify live behavior before tracing local root causes.

**When live and local disagree:** Live server wins. Local repo may be stale.
