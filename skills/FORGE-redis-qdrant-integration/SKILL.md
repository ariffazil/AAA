---
id: FORGE-redis-qdrant-integration
name: FORGE-redis-qdrant-integration
version: 1.0.0-2026.07.17
description: "Redis + Qdrant integration — caching layer and vector memory for federation semantic search."
owner: A-FORGE
risk_tier: medium
floor_scope: ['F1', 'F2', 'F4']
autonomy_tier: T1
---
# ⚒️ Redis + Qdrant Integration — Caching & Vector Memory

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Redis as caching layer for MCP tool registry and session state; Qdrant as vector store for witness embeddings, semantic memory retrieval, and similarity search across federation knowledge.

## When to Use
- Caching MCP tool lists, health probes, or computed results (Redis)
- Session state and lease TTL management (Redis)
- Semantic search across witness receipts, seals, or docs (Qdrant)
- Embedding storage for tri-witness evidence vectors (Qdrant)
- Tool/skill discovery via semantic similarity (Qdrant)

## When NOT to Use
- Relational data that needs ACID — use `postgres-schema-design`
- Append-only immutable records — use `vault999-witness`
- File/blob storage — use S3/R2

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Redis keys have TTL; stale cache never blocks fresh reads |
| F2 TRUTH | Cache headers (`stale-while-revalidate`) published with every cached response |
| F4 CLARITY | One cache key naming convention across all organs |
| F11 AUDIT | Cache misses and evictions logged; Qdrant writes carry provenance |
| F12 INJECTION | Vector embeddings sanitized before upsert — no prompt injection in stored vectors |

## Commands & Patterns

```typescript
// Redis — tool registry cache with TTL
const CACHE_TTL = 300; // 5 minutes
await redis.set(`tool:${organ}:list`, JSON.stringify(tools), { EX: CACHE_TTL });

// Redis — session state
await redis.set(`session:${sessionId}`, JSON.stringify(session), { EX: 3600 });

// Qdrant — witness collection upsert
const point: PointStruct = {
  id: receiptId,
  vector: embedding,  // 1536-dim from embedding model
  payload: {
    witness_type: 'tri_witness',
    organ: 'geox',
    verdict: 'CONSENSUS',
    timestamp: Date.now(),
  },
};
await qdrant.upsert('witness_receipts', { points: [point] });

// Qdrant — semantic search
const results = await qdrant.search('witness_receipts', {
  vector: queryEmbedding,
  limit: 10,
  with_payload: true,
});
```

## Refusal Surface
- ❌ Redis persistence for critical audit data (use VAULT999)
- ❌ Qdrant as primary data store (vectors + relational in Postgres)
- ❌ Storing secrets or keys in Redis
- ❌ Embedding user PII into Qdrant vectors
- ❌ Cache-aside without invalidation strategy
