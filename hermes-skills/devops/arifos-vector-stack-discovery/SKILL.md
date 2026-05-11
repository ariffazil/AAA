---
name: arifos-vector-stack-discovery
category: devops
description: Diagnose the arifOS vector embedding stack — what actually runs vs what's in compose files. Find Ollama bge-m3, Qdrant status, Graphiti MCP status, and determine the fastest path to working embeddings.
---

# arifOS Vector Stack Discovery

## Context
On the arifOS VPS (af-forge), the intended vector stack (Qdrant + Ollama bge-m3 + Graphiti MCP) may not be fully deployed. Before attempting any embedding/vector search work, run this discovery to find what's actually available.

## Diagnostic Steps

### Step 1: Check what's actually running (docker ps)
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "ollama|qdrant|graphiti"
```

Expected outputs:
- `ollama-engine-prod` ✅ = Ollama running (mapped to 127.0.0.1:11434)
- `qdrant` ❌ = Not running (no container, despite being in compose)
- `graphiti-mcp` ❌ = Not running

### Step 2: Confirm Ollama models
```bash
docker exec ollama-engine-prod ollama list
```
Look for `bge-m3:latest` — the arifOS preferred embedding model.

### Step 3: Test Ollama embedding (inside container)
```bash
docker exec ollama-engine-prod curl -s http://localhost:11434/api/embeddings -d '{"model":"bge-m3","input":"test"}'
```
Note: curl from host to 127.0.0.1:11434 times out — must exec into container.

### Step 4: Check Qdrant (if container exists)
```bash
docker ps -a --format "{{.Names}}" | grep qdrant
```
No output = Qdrant not deployed (not an error — it's optional for simple use cases).

### Step 5: Check Graphiti MCP
```bash
docker ps -a --format "{{.Names}}" | grep graphiti
```
Graphiti is a temporal memory MCP server — optional, not required for basic vector embedding.

## Decision Tree

| Situation | Action |
|-----------|--------|
| Ollama running + bge-m3 available | Use Ollama direct for embeddings |
| Ollama running, no bge-m3 | Pull with: `docker exec ollama-engine-prod ollama pull bge-m3` |
| Ollama not running | Start via compose or use remote embedding API |
| Need Qdrant | `docker compose -f deploy/machine-law/docker-compose.yml up -d qdrant` |

## Fastest Path to Working BGE Embeddings (2026-05-06)

Given current deployment state:
- Ollama ✅ (bge-m3 installed) at 127.0.0.1:11434
- Qdrant ❌ not running
- Graphiti ❌ not running

**Recommended: Ollama direct** — no Qdrant needed for document ingestion:

```python
import httpx, json

# Generate BGE embedding via Ollama
async def embed_bge_m3(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "http://127.0.0.1:11434/api/embeddings",
            json={"model": "bge-m3", "input": text}
        )
        return resp.json()["embedding"]

# Store as JSON (simple) or SQLite with vector column
# For small corpora: just store as JSONLines with embedding + metadata
```

## Key Files
- arifOS memory_engine: `/root/arifOS/arifosmcp/memory_engine.py`
- Compose stack: `/root/arifOS/deploy/machine-law/docker-compose.yml`
- .env: `OLLAMA_URL`, `QDRANT_URL`, `GRAPHITI_URL` env vars

## Verified (2026-05-06)
- Ollama bge-m3: ✅ installed at 127.0.0.1:11434 (docker exec from host)
- bge-m3 model ID: `790764642607`, 1.2 GB
- Qdrant: ✅ RUNNING on port 6333 (36 points, 1024-dim, collection "arifosmcp")
- Graphiti: ⚠️ degraded — telemetry present but retrieval path broken
- arif_memory_recall: ❌ HOLLOW STUB — returns empty arrays for all vector modes

## Critical Diagnostic: Check /health First

Always start with:
```bash
curl -s http://127.0.0.1:8080/health | python3 -m json.tool
```

Key fields in `/health` response:
- `capability_map.vector_memory` → "enabled" means Qdrant is configured
- `graphiti_read` → "degraded" means Graphiti MCP is degraded
- `storage.vector_memory` → "configured" confirms Qdrant is live
- `seal_readiness.graphiti_read` → if degraded, vector search will return empty

## Critical Finding: arif_memory_recall Is a Hollow Stub

**The MCP tool `arif_memory_recall` does NOT touch Qdrant.** All modes return empty/fake:
- `mode="recall"` → `{"memories": [], "confidence": 0.0}`
- `mode="store"` → generates UUID but never writes to Qdrant
- `mode="search"` → `{"results": []}`
- `mode="context"` → `{"context_window": []}`

**Implication:** Infrastructure (Qdrant + Ollama) can be fully live, but if the MCP tool isn't wired to it, vector search returns nothing. This is the #1 failure mode — do NOT assume the tool works just because the stack is deployed.

## When to Suspect Stub Behavior
1. `curl -s http://127.0.0.1:8080/tools | python3 -m json.tool` shows the tool exists
2. But `curl -X POST http://127.0.0.1:8080/tools/call -d '{"name":"arif_memory_recall","arguments":{"mode":"recall","query":"test"}}'` returns empty arrays
3. Qdrant has points but no retrieval path

## Fastest Fix Path
1. Check `/health` capability_map for `vector_memory: enabled`
2. If Qdrant has points but arif_memory_recall returns empty → tool stub confirmed
3. Fix: wire Ollama BGE-M3 + Qdrant REST API into the actual tool handler
