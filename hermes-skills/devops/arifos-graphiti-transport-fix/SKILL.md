---
name: arifos-graphiti-transport-fix
description: Restore graphiti temporal memory to arifOS — transport mismatch between arifOS GraphitiClient (POST/MCP) and all graphiti MCP servers (SSE-only). Code-level rewrite required.
tags: [graphiti, arifOS, memory-engine, MCP, SSE, transport, neo4j]
last_updated: 2026-04-30
---

# arifOS Graphiti MCP Transport Fix

## Problem

arifOS `memory_engine.py` reports `graphiti_enabled: false`. Every graphiti MCP server returns 404 on POST `/mcp` because they only support SSE transport.

## Root Cause — Transport Mismatch

arifOS `GraphitiClient` calls graphiti via **HTTP POST**:
```python
self._graphiti = GraphitiClient(os.getenv("GRAPHITI_URL", "http://graphiti-mcp:8000/mcp"))
```

All graphiti MCP servers use **SSE-only transport**:
- `gifflet/graphiti-mcp-server` — FastMCP, `--transport sse` only, no POST `/mcp`
- `rawr-ai/mcp-graphiti` — GET `/sse` + POST `/messages/<session_id>`, no `/mcp` POST endpoint

GET `/sse` → `200 OK` with SSE stream (alive)
POST `/mcp` → `404 Not Found` (no such endpoint)

## What Was Tried

1. Pulled `ghcr.io/architect-ai/graphiti-mcp` — does not exist
2. Pulled `rawr-ai/mcp-graphiti` — builds fine, runs on port 8000, SSE-only transport confirmed
3. Built `gifflet/graphiti-mcp-server` from source — FastMCP SSE-only confirmed
4. Tried Neo4j 5.23.0, 5.26.0 — 5.26.0 required password reset due to db format change
5. Tried port 8008 to avoid conflict with WEALTH on 8000 — worked

## Fix — Code-Level Rewrite Required

arifOS `GraphitiClient` in `memory_engine.py` must be rewritten to use SSE transport.

### SSE Transport Protocol (rawr-ai/mcp-graphiti)

```
1. GET /sse  → receives session_id in "event: endpoint" → data: /messages/<session_id>
2. POST /messages/<session_id> with JSON-RPC "initialize"
3. POST /messages/<session_id> with JSON-RPC tool calls (add_episode, search_episodes, get_status)
4. Read responses from SSE stream
```

### arifOS memory_engine.py locations to change

- `_graphiti_add()` — currently does HTTP POST; needs SSE session + POST to `/messages/<session_id>`
- `_graphiti_search()` — currently does HTTP POST; needs SSE session + POST to `/messages/<session_id>`

## Working Stack (Post-Restore)

| Component | Status | Port |
|-----------|--------|------|
| Neo4j (graphiti-neo4j) | ✅ Running | 7474/7687 |
| graphiti-mcp (rawr-ai) | ✅ Running | 8008 (host) |
| arifOS GraphitiClient | ❌ Broken | — |

## Docker Commands (Pre-Restore)

```bash
# Neo4j (graphiti requires graph DB)
docker run -d \
  --name graphiti-neo4j \
  --restart unless-stopped \
  --network arifos_core_network \
  -p "127.0.0.1:7474:7474" -p "127.0.0.1:7687:7687" \
  -v /root/volumes/neo4j:/data \
  -e NEO4J_AUTH=neo4j/arifgraph2026 \
  neo4j:5.26.0

# graphiti-mcp (rawr-ai, built from source)
git clone --depth 1 https://github.com/rawr-ai/mcp-graphiti.git /tmp/mcp-graphiti
cd /tmp/mcp-graphiti && docker build -t graphiti-mcp:latest .
docker tag graphiti-mcp:latest ghcr.io/ariffazil/graphiti-mcp:latest

OPENAI_KEY=$(docker exec arifosmcp python3 -c "import os; print(os.environ.get('OPENAI_API_KEY',''))")
docker run -d \
  --name graphiti-mcp \
  --restart unless-stopped \
  --network arifos_core_network \
  -p "127.0.0.1:8008:8000" \
  -e NEO4J_URI=bolt://graphiti-neo4j:7687 \
  -e NEO4J_USER=neo4j \
  -e NEO4J_PASSWORD=arifgraph2026 \
  -e "OPENAI_API_KEY=$OPENAI_KEY" \
  -e OPENAI_BASE_URL=http://ollama:11434/v1 \
  -e MODEL_NAME=qwen2.5:7b \
  -e EMBEDDINGS_MODEL=bge-m3:latest \
  graphiti-mcp:latest
```

## Key Files

- `/root/arifOS/arifosmcp/memory_engine.py` — GraphitiClient (needs rewrite)
- `/root/compose/docker-compose.yml` — add graphiti-mcp and graphiti-neo4j services
