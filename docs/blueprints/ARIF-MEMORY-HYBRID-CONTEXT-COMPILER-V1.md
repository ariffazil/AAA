# ARIF_MEMORY HYBRID CONTEXT COMPILER — v1 SPEC
**Status:** DESIGN SPEC — awaiting Arif "SAH" before code
**Author:** FI-005 per Arif's correction (one door, not two; replaceable implementation, not new public surface)
**Sealed:** 2026-10-03 11:32 +08

---

## 1. THE LAW (from Arif's correction)

```
One Door ≠ One Pipe
```

`arif_memory` is the **constitutional interface** (one door). The Hybrid Context Compiler is a **replaceable retrieval implementation** behind it (one pipe, can be swapped without changing the door).

**Forbidden:** public MCP named `arifOS.context`, `arif_context`, or any other retrieval-aggregator surface. Agents must continue to call `arif_memory(mode="recall")`.

**Allowed:** internal process on `:18095` (a pipe), called by `arif_memory` recall handler. Can be killed, replaced, or rate-limited without breaking the door.

---

## 2. ARCHITECTURE

```
Agent
  │
  │  arif_memory(mode="recall", query="...", budget=2000)
  ▼
arif_memory canonical handler  (THE DOOR)
  │
  │  for hybrid mode: delegate to compiler
  ▼
Hybrid Context Compiler  (THE PIPE)  — process on :18095, internal
  │
  ├── Retrieve_q  (Qdrant — semantic + sparse candidates)
  │     • uses bge-m3 (FROZEN, do not change in v1)
  │     • returns: [{id, text, source, vector_score}]
  │
  ├── Retrieve_g  (FalkorDB — entity + path expansion)
  │     • Cypher query, expand peer relations
  │     • returns: [{id, text, source, graph_score}]
  │
  ├── normalize_ids (entity resolution: source_id, memory_id → canonical)
  │
  ├── RRF(ranked_lists=[q, g], k=60)
  │     • combines without score calibration
  │
  ├── Admit(rrf_results)
  │     • check SRO (source requirements) — e.g. SRO_MISSING → reject
  │     • check provenance (vault attestation, signed)
  │     • check lifecycle (active, not tombstoned, not quarantined)
  │     • check temporal validity (observed_at within scope)
  │     • check scope (peer membership, organ boundaries)
  │
  ├── Budget(budget=2000, admitted_results)
  │     • token-budget packer (count, truncate if needed)
  │
  ├── build evidence bundle:
  │     { chunks, sources, per_item_provenance, retrieval_receipt, cost_ms }
  │
  ▼
return to arif_memory handler
  │
  ▼
back to Agent
```

---

## 3. THE FORMULA (Arif's, kept verbatim)

```
Context = Budget( Admit( Fuse( Retrieve_q, Retrieve_g ) ) )
```

NOT:

```
Context = RRF(Qdrant, FalkorDB)   ← this is the WRONG order
```

**Why:** if you RRF before admission, bad historical memory (SRO missing, lifecycle expired) can rank higher than fresh, provenanced, live memory. RRF respects rank but doesn't know about provenance.

---

## 4. INTERFACE (the door side, what changes for callers)

`arif_memory(mode="recall", payload={...}, query=..., budget=2000)` — **NO signature change**. New optional payload field:

```python
{
  "hybrid": true,        # default: false (preserves v4 baseline)
  "budget": 2000,        # tokens, default 2000, max 8000
  "peer": "arif",        # for FalkorDB person scoping
  "graph_expand": 1      # 0-3 hops, default 1
}
```

If `hybrid=false` (default) → use existing v4 recall (Qdrant only, baseline).
If `hybrid=true` → invoke compiler on :18095, return compiled result.

**Backward compat:** existing callers (Codex, Hermes, Kimi, etc.) see NO change. They get the same envelope shape, same verdict codes. The compile happens transparently when `hybrid=true` is set.

---

## 5. INTERNAL PIPE (the compiler, on :18095)

### 5.1 Components (all replaceable, all behind one Python FastMCP server)

| Component | Class | Backend | Lines |
|---|---|---|---|
| Qdrant semantic/sparse | `QdrantRetriever` | `qdrant_client.QdrantClient(host=127.0.0.1, port=6333)` | ~80 |
| FalkorDB entity/path | `FalkorRetriever` | `falkordb.FalkorDB(host=127.0.0.1, port=6380)` | ~80 |
| ID normalizer | `IdentityResolver` | (in-memory map) | ~30 |
| RRF fuser | `RRFFuser` | (pure) | ~25 |
| Admissibility gate | `AdmissibilityGate` | (uses L11 floor + SRO check) | ~60 |
| Token budget packer | `BudgetPacker` | (uses tiktoken or similar) | ~30 |
| **Total** | | | **~305 LOC** |

### 5.2 Admissibility gate rules (per Arif's note)

| Rule | Check | Source |
|---|---|---|
| Provenance | vault attestation exists, signed by ed25519 | `/root/.local/share/arifos/vault999/seal_chain.jsonl` |
| Lifecycle | not tombstoned, not quarantined | `arif_memory.audit` or L4 store |
| SRO | source requirements satisfied (e.g. facts have `source_citation`) | payload schema |
| Temporal | `observed_at` within `budget.temporal_window` (default 1y) | payload field |
| Scope | peer is in the requester's authorized peer set | session metadata |
| Constitutional | not rejected by F1-F13 (existing SRO check) | `arif_memory` L-floor |

**Failure mode:** if any rule fails, the chunk is **rejected with reason**, not silently filtered. Returns include `rejected` array with reasons for observability.

### 5.3 RRF implementation (k=60 default)

```python
def rrf(ranked_lists: list[list[dict]], k: int = 60) -> list[dict]:
    scores = {}
    for lst in ranked_lists:
        for rank, item in enumerate(lst):
            scores.setdefault(item["id"], {"item": item, "score": 0.0, "sources": []})
            scores[item["id"]]["score"] += 1.0 / (k + rank + 1)
            scores[item["id"]]["sources"].append(item["source"])
    return sorted(scores.values(), key=lambda x: -x["score"])
```

No score calibration required (RRF is rank-based, not score-based). Qdrant's cosine similarity and FalkorDB's graph distance can be different scales — RRF ignores that.

---

## 6. RECEIPT MODEL (per Arif's note: don't spam VAULT999)

### 6.1 Ordinary queries (default)

- **Not** written to VAULT999 (immutable).
- Written to **normal audit log**: `/root/.local/share/arifos/runtime/audit/arif_memory_context.log` (JSONL, append-only, rotated).
- Each entry: `{ts, session_id, actor, query_hash, n_results, n_admitted, n_rejected, cost_ms, sources_used}`

### 6.2 Consequential decisions (rare, F13-routed)

When the compiler result is used to support a SEALABLE decision (e.g. constitutional change, audit conclusion, evidence for a verdict):
- All admitted chunks + provenance + admit reasons are bundled
- Bundle hash + admission log is written to `vault999/seal_chain.jsonl` (immutable, F11)
- This is gated by caller (`payload.evidence_refs=true` + constitutional context)

**The 90/10 rule:** ~90% of recall queries are observation, not evidence for a SEAL. They go to ordinary log. ~10% are evidence, they go to VAULT999.

---

## 7. EVALUATION (per Arif's spec)

### 7.1 Required experiment

```
Qdrant-only (baseline, hybrid=false)
  vs
FalkorDB-only (fallback)
  vs
Fusion (hybrid=true, RRF + admit)
```

### 7.2 Metrics (per query, 50-query fixed set)

| Metric | Why it matters |
|---|---|
| Recall@k | Did we surface the relevant chunk? |
| Precision@k | Did we avoid noise? |
| Freshness accuracy | Are we preferring recent over old when query is time-sensitive? |
| Provenance completeness | % of admitted chunks with valid vault attestation |
| Contradiction surfacing | % of admit-rejections that expose a real SRO/lifecycle violation |
| Citation rate | % of admitted chunks that the agent actually uses in its answer |
| Latency (p50, p95) | Speed |
| Token cost | Average context size returned |
| **Decision-change rate** | P(decision changes correctly | better retrieved evidence) |

### 7.3 Promotion gate (v1 → v2)

Compiler is promoted from v1 (experimental) to v2 (default) only if:

1. Decision-change rate is **statistically significantly higher** (p<0.05, n=50)
2. Latency p95 < 1.5 seconds (else fallback to v4 baseline)
3. Provenance completeness ≥ 99% (else SRO failure → reject v1)
4. Zero admitted chunks fail F11 audit (else VAULT999 spam → reject v1)

---

## 8. FAILURE MODES (per F13 doctrine)

| Mode | Behavior |
|---|---|
| Compiler unreachable | `arif_memory` recall returns SABAR with reason; caller can retry or fall back to v4 |
| Qdrant down | Compile returns FalkorDB-only result (flagged in receipt) |
| FalkorDB down | Compile returns Qdrant-only result (flagged in receipt) |
| Both down | Compile returns SABAR; v4 baseline also fails → SRO_MISSING |
| Admit gate rejects all | Compile returns HOLD with reason; not VOID (no data ≠ all clear) |
| VAULT999 down | Admit falls back to ordinary log; flag in receipt |

---

## 9. IMPLEMENTATION PHASES (per Law 10: simplicity)

### Phase 1 (1 week, T1-AUTO + T2): skeleton + baseline
- Write `arif_memory_hybrid_compiler/server.py` (FastMCP on :18095, ~300 LOC)
- Wire `arif_memory` recall handler to call it when `hybrid=true`
- 50-query test set (collected from real arifOS queries, anonymized)
- Run baseline (Qdrant-only, FalkorDB-only) and hybrid against the set
- Save metrics: `eval_results_v1.json`

### Phase 2 (1 week, T2 + F13 ASK): promotion gate
- If v1 beats baseline on decision-change rate → F13 ASK to make `hybrid=true` default
- If v1 doesn't beat → keep as opt-in, learn why, iterate

### Phase 3 (optional, T3): LLM reasoning layer
- Add `qwen2.5:3b` (or smaller) summarization of admitted chunks
- Only if decision-change rate improves further
- **Do not** add in v1 (Arif's gate: keep v1 deterministic)

---

## 10. WHAT WE **DON'T** BUILD (per Law 10)

- ❌ New public MCP surface (`arifOS.context` is FORBIDDEN)
- ❌ Cloud embedding model (bge-m3 is frozen)
- ❌ LLM reasoning layer (v2+)
- ❌ Cross-encoder reranker (v2+)
- ❌ New storage backend (use what we have)
- ❌ Hot cache invalidation system (v1 = read-mostly; cache via Qdrant's own)
- ❌ LLM-based chunk rewriting (v1 = return as-is)

---

## 11. F13 GATE (per Auto-Seal doctrine)

This spec requires Arif's "SAH" before any code is written. Spec lives at `/root/AAA/docs/blueprints/ARIF-MEMORY-HYBRID-CONTEXT-COMPILER-V1.md`. Receipts from research live at `/root/AAA/docs/audit-receipts/PATH1-RESEARCH-ARIFOS-CONTEXT-2026-10-03.md`.

**Mutation this turn:** ZERO. Spec only.

## 12. RECEIPTS

- [receipt: arif_memory-canonical-handler:/opt/arifos/arifosmcp/runtime/megaTools/tool_13_arif_memory.py]
- [receipt: recall-dispatch:engineering_memory_dispatch_impl,graph_tier_gate,vector_recall]
- [receipt: live-kernel-drift:ALIGNED,source=deployed=build=6ea807e]
- [receipt: qdrant-collections-9,vector-semantic-sparse-ready]
- [receipt: falkordb-8.6.3,cypher-vector-hybrid-native]
- [receipt: bge-m3-already-deployed-FROZEN]
- [receipt: 74-mcp-ports-active-no-new-needed]
- [receipt: vault-999-94499-entries-F11-audit-trail]
- [receipt: 1-door-1-pipe-doctrine:F13-ratified-by-Arif]
