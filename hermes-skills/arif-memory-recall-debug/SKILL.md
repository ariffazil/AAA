---
name: arif-memory-recall-debug
description: "Diagnose arif_memory_recall returning _degraded DB connection failure via REST but working via direct Python call. Tests MemoryEngine singleton state across REST vs direct invocation paths."
triggers: ["arif_memory_recall degraded", "DB connection failed", "memory tool broken", "REST vs direct inconsistency"]
tags: ["arifOS", "debug", "memory", "postgres", "rest-api"]
category: devops
---

# arifMemoryRecall Debug

## Trigger
`arif_memory_recall` returns `_degraded: "DB connection failed"` via REST but works when the Python handler is called directly inside the container.

## Diagnostic Commands (in order)

```bash
# 1. REST test — see degraded response
curl -s http://localhost:8080/tools/arif_memory_recall \
  -H "Content-Type: application/json" \
  -d '{"mode":"recall","query":"constitution","session_id":"SEAL-xxx","actor_id":"ARIF"}' \
  --max-time 10 | python3 -m json.tool

# 2. Direct handler test inside container
docker exec arifosmcp python3 -c "
import sys; sys.path.insert(0, '/app')
from arifosmcp.runtime.tools import _CANONICAL_HANDLERS
h = _CANONICAL_HANDLERS.get('arif_memory_recall')
r = h(mode='recall', query='constitution', session_id='SEAL-xxx', actor_id='ARIF', memory_id=None)
print('OK' if r.get('status')=='OK' else 'FAIL', 'memories:', len(r.get('result',{}).get('memories',[])))
"

# 3. Check env vars
docker exec arifosmcp python3 -c "
import os
print('DATABASE_URL:', os.getenv('DATABASE_URL', 'NOT SET')[:50])
print('POSTGRES_URL:', os.getenv('POSTGRES_URL', 'NOT SET')[:50])
"

# 4. Check memory_store table
docker exec arifosmcp python3 -c "
import asyncio, sys, os
sys.path.insert(0, '/app')
from arifosmcp.memory_engine import MemoryEngine
async def t():
    me = MemoryEngine(postgres_url=os.getenv('POSTGRES_URL'), qdrant_url='http://qdrant:6333', ollama_url='http://ollama:11434')
    pool = await me._get_pg_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT COUNT(*) FROM memory_store')
        print('memory_store rows:', rows[0][0])
asyncio.run(t())
"

# 5. Check Qdrant availability
docker exec arifosmcp python3 -c "
import sys, os; sys.path.insert(0, '/app')
from arifosmcp.memory_engine import MemoryEngine
me = MemoryEngine(postgres_url=os.getenv('POSTGRES_URL'), qdrant_url='http://qdrant:6333', ollama_url='http://ollama:11434')
print('Qdrant client:', me._qdrant_client)
"
```

## Root Cause
`_memory_engine` in `tools.py` (~line 3261) is lazily initialized. The REST path (`call_tool_rest` in `rest_routes.py`) and direct Python call may use different singleton states. The fix is to use a module-level singleton getter pattern.

## Key Files
- `arifosmcp/runtime/tools.py` — `arif_memory_recall` handler (~line 3240), `_memory_engine` lazy init (~line 3261)
- `arifosmcp/memory_engine.py` — `MemoryEngine` class, `retrieve()` (~line 530)
- `arifosmcp/runtime/rest_routes.py` — `call_tool_rest` (~line 2388), `TOOL_ALIASES` (~line 68)

## Fix

Replace the lazy init pattern with a singleton getter in `tools.py`:

```python
_memory_engine: "MemoryEngine | None" = None

def _get_memory_engine() -> "MemoryEngine":
    global _memory_engine
    if _memory_engine is None:
        url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
        _memory_engine = MemoryEngine(
            postgres_url=url,
            qdrant_url=os.getenv("QDRANT_URL", "http://qdrant:6333"),
            ollama_url=os.getenv("OLLAMA_URL", "http://ollama:11434"),
        )
    return _memory_engine
```

Then replace all `_memory_engine` with `_get_memory_engine()` in `arif_memory_recall`.

## Verify Fix

```bash
curl -s http://localhost:8080/tools/arif_memory_recall \
  -H "Content-Type: application/json" \
  -d '{"mode":"recall","query":"constitution","session_id":"SEAL-xxx","actor_id":"ARIF"}' \
  --max-time 10 | python3 -c "
import sys,json
d=json.load(sys.stdin)
r=d.get('result',{}).get('result',{})
print('OK' if d.get('status')=='success' else 'FAIL', 'memories:', len(r.get('memories',[])), 'conf:', r.get('confidence'))
"
```

## Schema (no change needed)
```
arif_memory_recall(mode: str = "recall", query: str | None = None,
                   memory_id: str | None = None,
                   session_id: str | None = None,
                   actor_id: str | None = None,
                   metadata: dict | None = None) -> dict
```
Valid modes: `recall`, `store`, `get`, `list`, `init_recall`

## CRITICAL: `metadata.text` Required for `store` Mode

When calling `arif_memory_recall(mode='store', metadata={...})`, the `metadata` object **must** contain a `text` field. Without it, the tool returns `HOLD` with reason `"store mode requires metadata.text"`.

**WRONG (HOLD):**
```json
{
  "mode": "store",
  "query": "some text",
  "metadata": { "agent_id": "hermes-asi", "lane": "ASI" }
}
```

**CORRECT (SEAL):**
```json
{
  "mode": "store",
  "query": "some text",
  "metadata": {
    "text": "Human-readable description — this field is MANDATORY",
    "agent_id": "hermes-asi",
    "lane": "ASI"
  }
}
```

Note: Even with `stored: true`, the returned `memory_id` may be `null` if the underlying DB is degraded. Check `_degraded` field in result.

## Vault999 Seal Timeout

`arif_vault_seal` may time out (>10s) even when the vault999 sidecar is running. This is a known network/connection issue — the seal operation itself may complete on the backend, but the HTTP call times out. Workaround: do not block on vault seal for critical paths; write static files as fallback.

## Agent Card Registration Path

For Phase 0 identity binding, cards go in:
```
arifOS/arifosmcp/runtime/agent_registry/cards/{agent_id}.json
```
Not in the memory store — use static files + vault seal (with timeout awareness).

## Common Failure Modes
- Qdrant unavailable → falls back to Postgres ✓
- Graphiti DNS fail → caught as warning, continues ✓
- `memory_store` missing → `UndefinedTableError`, caught as warning ✓
- Wrong session_id → F11 AUTH HOLD (correct behavior)
- `metadata.text` missing → HOLD, add text field
- `memory_id` null with `stored: true` → DB degraded, check `_degraded` field
- Vault seal timeout → static file fallback, don't block on seal
