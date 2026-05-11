---
name: arifos-memory-engine-debug
description: Debug and bootstrap the arifOS MemoryEngine — Postgres + Qdrant dual-write runtime. Diagnoses import failures, password issues, missing tables, and connectivity problems.
---

# arifOS Memory Engine — Debug & Bootstrap Skill

## Context
arifOS MCP stack uses `MemoryEngine` (dual-write: Postgres + Qdrant). Blockers are common on fresh installs or after container rebuilds.

## Prerequisites
- `asyncpg` installed in arifosmcp container
- `qdrant-client` installed in arifosmcp container
- Postgres `arifos_admin` password known or resettable
- Ollama reachable at `http://ollama:11434`

## Diagnostic Sequence

### Step 1 — Check MemoryEngine imports
```bash
docker exec arifosmcp python3 -c "from arifosmcp.memory_engine import MemoryEngine; print('OK')"
```
If `asyncpg` missing: `pip install asyncpg qdrant-client` inside container.

### Step 2 — Postgres connectivity
```bash
# Test via Unix socket (no password needed if trust auth)
docker exec postgres sh -c 'gosu postgres psql -U arifos_admin -d vault999 -c "SELECT 1"'

# Test via TCP with password
docker exec arifosmcp python3 -c "
import asyncio, asyncpg
async def t():
    conn = await asyncpg.connect('postgresql://arifos_admin:<PASSWORD>@postgres:5432/vault999', timeout=5)
    print(await conn.fetchrow('SELECT current_database()'))
    await conn.close()
asyncio.run(t())
"
```

### Step 3 — Postgres password reset (if unknown)
```bash
# Connect via Unix socket (trust auth = no password needed)
docker exec postgres sh -c 'gosu postgres psql -U arifos_admin -d vault999 -c "ALTER USER arifos_admin WITH PASSWORD '\''NEW_PASSWORD'\'';"'
```
Note: `gosu` is at `/usr/local/bin/gosu` in the postgres container.

### Step 4 — Create memory_store table
```bash
docker exec postgres sh -c 'gosu postgres psql -U arifos_admin -d vault999' << 'EOSQL'
CREATE TABLE IF NOT EXISTS memory_store (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tier        TEXT NOT NULL CHECK (tier IN ('ephemeral', 'working', 'canon', 'sacred', 'quarantine')),
    text        TEXT NOT NULL DEFAULT '',
    metadata    JSONB NOT NULL DEFAULT '{}',
    qdrant_id   UUID,
    session_id  TEXT,
    epoch       TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_memory_store_tier ON memory_store(tier);
CREATE INDEX IF NOT EXISTS idx_memory_store_session ON memory_store(session_id);
CREATE INDEX IF NOT EXISTS idx_memory_store_created ON memory_store(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memory_store_deleted ON memory_store(deleted_at) WHERE deleted_at IS NULL;
EOSQL
```

### Step 5 — Verify Qdrant collections
```bash
curl -s http://localhost:6333/collections | python3 -c "import json,sys; print([c['name'] for c in json.load(sys.stdin)['result']['collections']])"

# Collections named arifos_vault_<tier> auto-created on first store
```

### Step 6 — Full store/retrieve test
```python
import asyncio
from arifosmcp.memory_engine import MemoryEngine

async def test():
    me = MemoryEngine(
        postgres_url="postgresql://arifos_admin:PASSWORD@postgres:5432/vault999",
        qdrant_url="http://qdrant:6333",
        ollama_url="http://ollama:11434",
        embedding_model="bge-m3",
    )
    r = await me.store({"text": "test memory", "metadata": {}}, tier="working")
    print(f"stored: {r}")
    result = await me.retrieve("test query", tier="working", limit=3)
    print(f"retrieved: {result}")
    await me.close()

asyncio.run(test())
```

## Qdrant v1.17 API Reference (this VPS runs v1.17.0)

**CRITICAL:** The version on this VPS uses different endpoints than older Qdrant docs:

| Operation | Endpoint | Method | Body |
|-----------|----------|--------|------|
| Semantic search | `/collections/<name>/points/query` | POST | `{"query": vector, "limit": N, "with_payload": true}` |
| Scroll/list all | `/collections/<name>/points/scroll` | POST | `{"limit": 100, "with_payload": true, "with_vectors": true}` |
| Upsert | `/collections/<name>/points` | PUT | `{"points": [{"id": "<UUID>", "vector": [...], "payload": {...}}]}` |

**Point ID rules:** Must be UUID or unsigned integer. String IDs like `"arch-20260429"` → `HTTP 400 Bad Request`. Use `uuid.uuid4()` to generate valid IDs.

**Test connectivity from container:**
```bash
docker exec arifosmcp curl -s http://qdrant:6333/collections
docker exec arifosmcp curl -s --max-time 60 -X POST http://ollama:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "bge-m3", "prompt": "test"}'
```

## Federation Shared Memory Architecture

Both bots (arifOS MCP + A-FORGE) dual-write to `federation_shared` collection for cross-bot memory visibility:

```
arifOS MCP  → arifos_vault_<tier> (private)
           → federation_shared (shared, tagged writer_bot="arifOS_MCP")

A-FORGE     → local mem.json (private)
           → federation_shared (shared, tagged writer_bot="A-FORGE")
```

**Collection setup:**
```bash
curl -s -X PUT http://localhost:6333/collections/federation_shared \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 1024, "distance": "Cosine"}}'
```

**Federation payload schema (every shared point must include):**
```json
{
  "text": "...",         // original text
  "summary": "...",      // <=200 char summary for embedding
  "writer_bot": "arifOS_MCP | A-FORGE | AGI_ASI_bot",
  "original_collection": "arifos_vault_working | openclaw_memory",
  "migrated": true,      // true for migrated points, absent for new writes
  "original_id": "..."   // original point ID before migration
}
```

**Migration script:** `/root/migrate_to_federation.py` — reads from private collections via scroll, re-writes to federation_shared with new UUIDs and writer_bot tags.

## Common Blockers

| Blocker | Symptom | Fix |
|---------|---------|-----|
| `asyncpg` missing | `ModuleNotFoundError: No module named 'asyncpg'` | `pip install asyncpg` in container |
| Wrong postgres password | `InvalidPasswordError` | Reset via `gosu postgres psql` (Unix socket, no pw) |
| `memory_store` table missing | `UndefinedTable` on INSERT | Run CREATE TABLE SQL above |
| Qdrant collection missing | Qdrant returns error on upsert | Auto-created on first store; or create manually |
| DATABASE_URL env var empty | MemoryEngine gets None | Set env var: `export DATABASE_URL="postgresql://arifos_admin:PASSWORD@postgres:5432/vault999"` |
| `pg_id` not UUID | `ValueError: badly formed hexadecimal UUID string` | memory_engine.py retrieve expects UUID pg_ids; don't insert non-UUID pg_ids |

### CRITICAL: `rest_routes.py` sync/async bug
The REST endpoint `/tools/<tool>` at `rest_routes.py:2434` does `await tool_fn(**filtered)` on ALL tools — including sync functions that return plain `dict`. This causes:
```
TypeError: object dict can't be used in 'await' expression
```
**Symptom:** Every sync tool call (like `arif_memory_recall`) returns HTTP 500 via REST, but works via MCP protocol.

**Fix:** Check if coroutine before awaiting:
```python
import asyncio as _asyncio
if _asyncio.iscoroutinefunction(tool_fn):
    result = await tool_fn(**filtered)
else:
    result = tool_fn(**filtered)
```

**Also:** `rest_routes.py` is NOT mounted in the docker-compose image — it uses the baked-in image version. Add to volume mounts:
```yaml
- /root/arifOS/arifosmcp/runtime/rest_routes.py:/app/arifosmcp/runtime/rest_routes.py:ro
```

### CRITICAL: `***` in env var display — don't trust repr
`docker exec arifosmcp python3 -c "import os; print(repr(os.environ['POSTGRES_URL']))"` may show `***` (display masking by the terminal tool), but the ACTUAL password may be correct. Similarly Python's repr might mask passwords.

**Always verify with character codes:**
```python
# BAD — trusts display
print(os.environ['POSTGRES_URL'])  # shows ***

# GOOD — reads actual value
u = os.environ['POSTGRES_URL']
idx = u.find('@')
pwd_segment = u[u.find(':')+3:idx]
print('Char codes:', [ord(c) for c in pwd_segment])
# ArifPostgres2026! → [65, 114, 105, 102, 80, 111, 115, 116, 103, 114, 101, 115, 50, 48, 50, 54, 33]
```

**Root cause of `***` password:** Docker compose `environment:` section may have literal `***` instead of the real password. The `.env` file may show the real value, but the compose `environment:` block overrides it. Fix: set `POSTGRES_URL` directly in the compose `environment:` block with the real password.

## Important Architecture Notes

### MCP Tool Names — Where arif_memory_recall ACTUALLY lives
`arif_memory_recall` exists in TWO places — only ONE is live:

| File | Status | What it does |
|------|--------|--------------|
| `arifosmcp/tools/memory.py` | **DEAD STUB** | Returns hardcoded empty arrays — not registered |
| `arifosmcp/runtime/tools.py` (line ~2557) | **LIVE** | Calls `MemoryEngine.retrieve()` via `_run_async` — actual implementation |

The live tool uses `mode` parameter: `recall` (vector search), `store`, `get`, `list`, `prune`, `search`, `context`, `dry_run`.

### MCP HTTP Transport Session Requirement
When calling arifOS MCP via direct HTTP (not via OpenClaw gateway), tool calls require an active MCP session:
```
Missing session → HTTP 400 "Missing session ID"
Fix: Use OpenClaw gateway (port 18789) or establish MCP session before calling tools
```

### Container Hostnames (Docker network)
- postgres: `postgres:5432`
- qdrant: `qdrant:6333`
- ollama: `ollama:11434` (NOT `ollama_engine`)

### Persistent pip installs
Add to `pyproject.toml` or `requirements.txt` so they survive container rebuilds:
```
asyncpg>=0.31.0
qdrant-client>=1.17.0
```

## Run From
`/root/arifOS/` — PYTHONPATH must include `/usr/src/app` when running ad-hoc scripts inside the container.
