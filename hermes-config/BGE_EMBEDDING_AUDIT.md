# ═══════════════════════════════════════════════════════════════════════════
# BGE-M3 EMBEDDING AUDIT — arifOS Federation
# Authority: 888_JUDGE | Sovereign: Arif
# Date: 2026-05-11
# Auditor: A-FORGE 777
# ═══════════════════════════════════════════════════════════════════════════

## 1. EXECUTIVE SUMMARY

| Component | Status | Issue |
|-----------|--------|-------|
| **Ollama bge-m3** | ✅ LIVE | 1024-dim, responding on :11434 |
| **Qdrant vector DB** | ✅ LIVE | Collection `arifos_memory` created (1024-dim, cosine) |
| **arifOS container → Ollama** | ✅ REACHABLE | Embedding API works from container |
| **arifOS container → Qdrant** | ✅ REACHABLE | Health check passes |
| **vector_memory_qdrant.py** | ✅ WORKING | End-to-end store + query verified |
| **OpenClaw → Ollama** | ✅ REACHABLE | Host process can access localhost:11434 |
| **Hermes → Ollama** | ❌ **BROKEN** | Uses `127.0.0.1:11434` inside container |
| **arifOS qdrant_client pkg** | ❌ **MISSING** | Not installed in arifOS container |
| **Postgres pgvector** | ❌ **MISSING** | Extension not available in Postgres container |
| **Memory schema dim** | ❌ **MISMATCH** | Migration uses 1536-dim, bge-m3 is 1024-dim |
| **Dual memory systems** | ⚠️ **FRAGMENTED** | File-based vs vector-based don't share data |

**Verdict:** BGE-M3 is **partially wired**. The core vector pipeline (Ollama → bge-m3 → Qdrant) works when tested from the host. But **4 blockers** prevent production use in containers.

---

## 2. DETAILED FINDINGS

### 2.1 Ollama bge-m3 — ✅ LIVE

```
Host:     http://localhost:11434 / http://127.0.0.1:11434
Container: http://ollama:11434 (Docker network)
Model:    bge-m3:latest
Dim:      1024
Size:     1104 MB
Status:   ✅ Responding
```

**Tested from:**
- Host direct curl: ✅
- arifOS container (`docker exec arifosmcp`): ✅
- Hermes container: ❌ (wrong URL)
- OpenClaw host process: ✅

---

### 2.2 Qdrant — ✅ LIVE (but empty)

```
Host:      http://localhost:6333
Collection: arifos_memory (created manually during audit)
Dim:        1024 (cosine distance)
Points:     1 (test record inserted during audit)
Status:     ✅ Healthy
```

**Note:** Collection was created manually during this audit. Previously had **0 collections**.

---

### 2.3 arifOS Kernel — ⚠️ PARTIALLY WIRED

**What's Working:**
- `vector_memory_qdrant.py` is well-implemented with F2 truth scoring + F10 ontology checks
- End-to-end verified from host: store → embed → Qdrant → query → retrieve
- `OLLAMA_URL=http://ollama:11434` is set correctly in container env

**What's Broken:**

#### Blocker 1: `qdrant_client` Python package missing
```
Error: No module named 'qdrant_client'
Location: arifOS container
Impact: memory_engine.py, vector_memory_qdrant.py, constitutional_memory.py all fail
```

#### Blocker 2: Postgres pgvector extension missing
```
Error: extension "vector" is not available
Impact: memory_embeddings table creation failed
Status: memory_records and other tables created successfully
```

#### Blocker 3: Vector dimension mismatch
```
Migration:    vector(1536)  -- designed for OpenAI embeddings
bge-m3:       1024-dim    -- actual model output
Impact:       If pgvector is installed, embeddings would be truncated/padded
```

#### Blocker 4: Dual memory systems (architectural debt)

| System | Backend | Embeddings | Used By |
|--------|---------|------------|---------|
| `memory_store.py` | File JSON (`/root/.arifOS/memory/`) | ❌ No | `arif_memory_recall` tool |
| `memory_engine.py` | Postgres + Qdrant | ✅ Yes | `agents_66.py` |
| `vector_memory_qdrant.py` | Qdrant only | ✅ Yes | Constitutional memory |

**These three systems do NOT share data.** A memory stored via `arif_memory_recall` cannot be found via vector query.

#### Blocker 5: `memory_engine.py` references wrong table name
```python
# memory_engine.py line 431:
INSERT INTO memory_store (id, tier, text, metadata, qdrant_id, session_id)
# But migration creates: memory_records
```

#### Blocker 6: `agents_66.py` default URL is wrong
```python
# agents_66.py line 38:
ollama_url=os.getenv("OLLAMA_EMBEDDING_URL", "http://A-FORGE-ollama:11434")
# Correct: "http://ollama:11434"
# Not currently broken because OLLAMA_URL env var overrides it
```

---

### 2.4 HERMES — ❌ BROKEN

```yaml
session_search:
  provider: ollama
  model: bge-m3
  base_url: http://127.0.0.1:11434   # ❌ WRONG
```

**Problem:** Hermes runs inside a Docker container (`hermes-agent` on `arifos_core_network`). `127.0.0.1` inside the container refers to the container itself, not the host. Ollama is not running inside the Hermes container.

**Fix:** Change to `http://ollama:11434`

---

### 2.5 OpenClaw — ✅ WORKING

```json
"memorySearch": {
  "enabled": true,
  "remote": { "baseUrl": "http://localhost:11434" },
  "provider": "ollama",
  "model": "bge-m3"
}
```

**Status:** ✅ OpenClaw runs as a host process (PID 395730), so `localhost:11434` correctly resolves to the host's Ollama instance.

---

## 3. END-TO-END TEST RESULTS

### Test 1: Vector Store + Query (Host)
```python
Content: {"floor": "F01", "name": "AMANAH", ...}
Store:   ✅ ok=True, point_id=1f4ef282..., vector_size=1024
Query:   ✅ 1 result, score=0.6648
```

### Test 2: Embedding Generation (arifOS Container)
```bash
docker exec arifosmcp curl http://ollama:11434/api/embeddings
Result: ✅ 1024-dim vector returned
```

### Test 3: Qdrant Collection (Host)
```bash
curl http://localhost:6333/collections
Result: ✅ arifos_memory exists, 1024-dim, cosine
```

### Test 4: arifOS Container Qdrant Client
```bash
docker exec arifosmcp python3 -c "import qdrant_client"
Result: ❌ No module named 'qdrant_client'
```

---

## 4. FIX PRIORITIES

### 🔴 P0 — Hermes session_search URL (blocks container usage)
**File:** `AAA/hermes-config/config.yaml`
**Change:** `http://127.0.0.1:11434` → `http://ollama:11434`

### 🔴 P0 — Install qdrant_client in arifOS container
**Action:** Add `qdrant-client` to arifOS requirements/dockerfile
**Impact:** Unblocks memory_engine.py, vector_memory_qdrant.py, constitutional_memory.py

### 🟡 P1 — Install pgvector in Postgres container
**Action:** Use `pgvector/pgvector:pg16` image or install extension
**Impact:** Unblocks memory_embeddings table

### 🟡 P1 — Fix vector dimension in migration
**File:** `arifosmcp/migrations/001_memory_schema.sql`
**Change:** `vector(1536)` → `vector(1024)`

### 🟡 P1 — Fix memory_engine.py table name
**File:** `arifosmcp/memory_engine.py`
**Change:** `memory_store` → `memory_records`

### 🟢 P2 — Unify memory systems (architectural)
**Decision needed:** Consolidate `memory_store.py`, `memory_engine.py`, and `vector_memory_qdrant.py` into single backend
**Recommendation:** Retire `memory_store.py`, migrate to `vector_memory_qdrant.py` as canonical

### 🟢 P2 — Fix agents_66.py default URL
**File:** `arifosmcp/agents_66.py`
**Change:** `http://A-FORGE-ollama:11434` → `http://ollama:11434`

---

## 5. IMMEDIATE FIXES APPLIED DURING AUDIT

1. ✅ Created Qdrant collection `arifos_memory` (1024-dim, cosine)
2. ✅ Verified vector store + query pipeline from host
3. ✅ Verified embedding generation from arifOS container
4. ✅ Verified OpenClaw → Ollama connectivity

---

## 6. RECOMMENDED DEPLOYMENT ORDER

```bash
# Step 1: Fix Hermes config
sed -i 's|http://127.0.0.1:11434|http://ollama:11434|' /root/AAA/hermes-config/config.yaml

# Step 2: Install qdrant-client in arifOS container
#   (Requires Dockerfile update + rebuild)

# Step 3: Fix Postgres pgvector
#   (Requires switching to pgvector image or installing extension)

# Step 4: Fix migration and re-run
#   (Update 001_memory_schema.sql, then psql)

# Step 5: Restart federation stack
#   docker compose restart arifosmcp hermes-agent
```

---

## 7. COST IMPACT

BGE-M3 runs locally via Ollama. **Zero API cost** for embeddings.

| Component | Cost |
|-----------|------|
| Ollama bge-m3 inference | $0 (local CPU/GPU) |
| Qdrant storage | $0 (local container) |
| **Total embedding cost** | **$0/month** |

---

*Audit completed: 2026-05-11T09:15Z*
*Authority: A-FORGE 777 | Fixes require 888_JUDGE for container rebuilds*
