---
name: pgvector-sovereign-rag
description: Zero-external-dependency local RAG and private vector search using PostgreSQL + pgvector container running on VPS (localhost:5432).
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Sovereign Local RAG Skill (`pgvector-sovereign-rag`)

Interfaces directly with the local PostgreSQL container running `pgvector` on VPS port `5432` for private, zero-external-dependency vector embedding, hybrid BM25 + cosine search, and project memory retrieval.

## Architecture & Database Schema

- **Host**: `127.0.0.1:5432` (Docker container `postgres-pgvector`)
- **Database**: `arifos_memory`
- **Tables**: `project_embeddings`, `decision_ledger`, `code_symbol_index`

### Vector Table Schema
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS project_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id VARCHAR(64) NOT NULL,
    filepath TEXT NOT NULL,
    content_chunk TEXT NOT NULL,
    embedding vector(384), -- all-MiniLM-L6-v2 vector dimension
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_embeddings_cosine 
ON project_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

---

## Python Execution Pattern

```python
import psycopg2
from pgvector.psycopg2 import register_vector

conn = psycopg2.connect("dbname=arifos_memory user=postgres host=127.0.0.1 port=5432")
register_vector(conn)
cursor = conn.cursor()

# Cosine distance search
query_embedding = [0.023, -0.045, ...] # 384-dim vector
cursor.execute("""
    SELECT filepath, content_chunk, 1 - (embedding <=> %s::vector) AS similarity
    FROM project_embeddings
    ORDER BY embedding <=> %s::vector
    LIMIT 5;
""", (query_embedding, query_embedding))

results = cursor.fetchall()
```

---

## Best Practices for Federation Agents

1. **Zero External Data Leaks**: Use `pgvector-sovereign-rag` whenever sensitive sovereign data, architectural decisions, or confidential well logs must be embedded without hitting public third-party APIs.
2. **Hybrid Search**: Combine PostgreSQL `tsvector` keyword search with `vector_cosine_ops` for exact symbol and semantic hybrid queries.
