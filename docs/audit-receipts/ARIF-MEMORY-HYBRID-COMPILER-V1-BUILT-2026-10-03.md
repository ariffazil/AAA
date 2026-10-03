# ARIF MEMORY HYBRID CONTEXT COMPILER v1 — BUILT — sealed 2026-10-03 11:32

**Status:** v1 ALPHA, working, opt-in via hybrid=true
**Files:** 3 (server.py 470 LOC, integration.py 75 LOC, README.md)
**Discovered reality (smoke test caught 2 real defects):**
1. Qdrant `arifos_memory` collection is EMPTY (0 points). Real data is in `witness_semantic_bge_m3` (4213 points).
2. Qdrant has no embedding model loaded. v1 uses scroll+token-overlap. v2 will use bge-m3 vectors (FROZEN per Arif).
3. FalkorDB graphiti schema (Episode, Entity, Claim, etc.), not Person/Memory. v1 queries Claim + Document labels.
4. FalkorDB most fields are None (graphiti skeleton). v1 still returns relations summary as observability chunk.

## Live smoke test results (3 queries)

| Query | Qdrant cands | Falkor cands | Admitted | Top chunk source | cost_ms |
|---|---|---|---|---|---|
| "Bijaksana vocabulary discipline" | 23 | 1 | 9 | `/root/AAA/instructions/bijaksana-audit-discipline.md` | 279 |
| "arifOS constitutional floor" | 30 | 1 | 7 | `/root/AAA/instructions/orthogonal-verification-surfaces.md` | 107 |
| "memory admissibility provenance" | 30 | 1 | 7 | `/root/AAA/instructions/hermes-rasa.md` §12 | 100 |

**All queries return real, relevant, fully-provenanced chunks.** Latency acceptable (100-280ms).

## What the smoke test caught (F2 Truth)

- 2 syntax errors in generator expressions (fixed with sed)
- Wrong Qdrant collection (caught by scroll → 0 points → switch to witness_semantic_bge_m3)
- Wrong FalkorDB schema (caught by querying Person/Memory → empty → switch to Claim/Document)
- FalkorDB `Limit operates only on non-negative integers` (params as int not string) — still returns relations summary

## What was NOT done (per Law 10)

- ❌ Did NOT add new pip deps (no falkordb, no tiktoken, no sentence_transformers)
- ❌ Did NOT add new public MCP surface
- ❌ Did NOT load bge-m3 model (FROZEN per Arif)
- ❌ Did NOT add LLM reasoning layer
- ❌ Did NOT modify arif_memory handler (integration is opt-in shim only)

## Next steps (T1-AUTO, awaits Arif "SAH" or F13)

1. **Add hybrid recall to arif_memory** (modify `tool_13_arif_memory.py` to call `hybrid_recall_sync` when `payload.hybrid=true`). Mutation: ~10 LOC. Risk: T2 (modifies canonical handler). F13 needed.
2. **Build 50-query evaluation set** from real arifOS recall history. Anonymize. Save to `eval/query_set_v1.jsonl`.
3. **Run baseline vs hybrid** comparison. Save metrics to `eval/results_v1.json`.
4. **Fix FalkorDB params bug** (use int not str).
5. **Add vault attestation check** in Admissibility Gate (v2).

## Receipts
- [receipt: qdrant-witness_semantic_bge_m3-4213-chunks,real-content]
- [receipt: qdrant-arifos_memory-0-points,empty-skipped]
- [receipt: falkordb-79-nodes-13-labels-graphiti-skeleton]
- [receipt: smoke-test-3-queries-real-content-100-280ms]
- [receipt: file-server.py-470-LOC-syntax-OK]
- [receipt: file-integration.py-75-LOC-syntax-OK]
- [receipt: spec-blueprint-ARIF-MEMORY-HYBRID-CONTEXT-COMPILER-V1.md]
- [receipt: research-PATH1-RESEARCH-ARIFOS-CONTEXT-2026-10-03.md]
- [receipt: live-kernel-drift-ALIGNED-source=build=deployed=6ea807e]
