---
id: forge-embedding-qdrant-integration
name: forge-embedding-qdrant-integration
version: 1.0.0-2026.09.21
description: "Use when embedding docs into Qdrant. Ollama/Qwen backends."
owner: curator
risk_tier: medium
floor_scope: ['F1', 'F2', 'F4']
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Embedding + Qdrant Integration

> DITEMPA BUKAN DIBERI

## When to Use

- Indexing federation documents into Qdrant for semantic search
- Building RAG pipelines over arifOS knowledge base
- Diagnosing Qdrant upsert failures or silent data loss
- Choosing between API embeddings (Qwen) and local embeddings (Ollama)

## When NOT to Use

- Redis caching — use forge-redis-qdrant-integration
- Qwen seat/quota management — use qwen-token-plan-team-edition
- MCP server wiring — use mcp-ops

## Embedding Backends

### Priority: Ollama Local (free, unlimited)

```bash
# bge-m3 — 1024 dim, multilingual, best local
curl -s http://localhost:11434/api/embeddings \
  -d '{"model": "bge-m3", "prompt": "text"}'

# nomic-embed-text — 768 dim, lightweight
curl -s http://localhost:11434/api/embeddings \
  -d '{"model": "nomic-embed-text", "prompt": "text"}'
```

Ollama embeds one text at a time. Loop with 50ms delay for batches.

### Fallback: Qwen API (quota-limited)

Endpoint: https://dashscope-intl.aliyuncs.com/compatible-mode/v1/embeddings
Auth: DASHSCOPE_API_KEY (NOT Token Plan keys)

| Model | Dim | Tokens/call | Quota |
|---|---|---|---|
| text-embedding-v3 | 64-1024 | ~9 | 1M free, 8-day expiry |
| text-embedding-v4 | 512-2048 | ~10 | 1M free, 8-day expiry |
| qwen3.7-text-embedding | 1024 | ~17-25 | 1M free, 49-day expiry |

Batch limit = 10 texts per call. Vision/rerank models need DashScope native SDK.

## Critical Pitfalls

- **Qdrant point IDs must be UUIDs.** Arbitrary strings are rejected silently — HTTP says acknowledged but point is never stored. Use uuid.uuid5(NAMESPACE_URL, key).
- **acknowledged ≠ committed.** Always verify points_count after bulk upsert.
- **Token Plan endpoint returns 404 for embeddings.** Use dashscope-intl.aliyuncs.com.
- **Free quotas burn fast.** 1M tokens at ~10 tok/call = ~100K texts. A 2000-char chunk is about 500 tokens.
- **Qwen batch limit = 10.** Not 20. HTTP 400 for larger.

## Witness Semantic Layer (arifOS)

| Field | Value |
|---|---| 
| Collection | witness_semantic |
| Vector dim | 1024, cosine distance |
| Backend | Ollama bge-m3 primary, Qwen fallback |
| Config | /root/arifOS/witness-semantic/config/embed_config.py |
| Indexer | /root/arifOS/witness-semantic/scripts/witness_indexer.py |
| Search | /root/arifOS/witness-semantic/scripts/witness_search.py |
| Sources Phase 1 | instruction, canon, eureka, governance, session_closure, scar |
| Sources Phase 2 | skill (694 files, deferred) |

## Constitutional Floor

| Floor | Application |
|---|---|
| F1 | Embeddings carry provenance — every vector traces to a source file |
| F2 | Vector store is retrieval index, not truth source. File is canonical |
| F4 | One collection per domain. doc_type enables filtered search |
| F12 | Text sanitized before embedding — no injection in stored vectors |

DITEMPA BUKAN DIBERI
