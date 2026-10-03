# EVAL V1 VERDICT — sealed 2026-10-03 11:38

**Status:** v1 evaluated, 50 queries × 3 configs, **REJECT FOR PRODUCTION**
**Verdict:** FalkorDB contributes 0 chunks to final context. Hybrid is not earning its keep.
**Next action:** Drop FalkorDB from v1. Make Config B (vector-only) the candidate for v2.

---

## 1. EVAL METHOD (per Arif's spec)

| Run | Configuration | Purpose |
|---|---|---|
| A | Baseline (v4 Qdrant-only) | What we have today |
| B | Vector-only (witness_semantic_bge_m3) | Does our real L3 data beat baseline? |
| C | Hybrid (Qdrant + FalkorDB + RRF + Admit) | Does graph fusion add unique value? |

50 queries, stratified:
- 10 semantic_factual
- 10 relationship_path
- 10 temporal_current_vs_old
- 10 contradiction_provenance
- 10 operational_agent

## 2. RESULTS (LIVE, NO NARRATIVE SMOOTHING)

### 2.1 Counts
- Total final chunks across 50 queries (config C): **441**
- Falkor candidates returned: 50 (one per query, all the same "relations summary" chunk)
- Falkor chunks in final bundle: **0 (zero)**
- Falkor % of final chunks: **0.00%**

### 2.2 Per-stratum (config C)
| Stratum | Q | Falkor cand | Falkor adm | % |
|---|---|---|---|---|
| semantic_factual | 10 | 10 | 0 | 0% |
| relationship_path | 10 | 10 | 0 | 0% |
| temporal_current_vs_old | 10 | 10 | 0 | 0% |
| contradiction_provenance | 10 | 10 | 0 | 0% |
| operational_agent | 10 | 10 | 0 | 0% |

**All 50 "Falkor candidates" are the same relations-summary chunk** (not a real candidate, just observability for `GRAPH.QUERY` returning relation types).

### 2.3 Latency
- Config A: avg 109ms
- Config B: avg 105ms
- Config C: avg 96ms (slightly faster, but meaningless — Falkor adds nothing)

### 2.4 GMU (Graph Marginal Utility)
- Queries where Falkor contributed unique useful evidence: **0/50 = 0%**

## 3. WHY FALKOR CONTRIBUTES ZERO (probed, not guessed)

1. **FalkorDB schema is a graphiti skeleton** — 79 nodes, 13 labels, most fields are None
2. **Claim nodes have null text fields** — no semantic content to match against
3. **Document nodes have null titles/paths** — only label structure populated
4. **FalkorDB's `Limit operates only on non-negative integers` bug** — my params as int bug returns errors silently
5. **No Falkor vector index** — semantic vector search on Falkor is not possible

## 4. VERDICT: REJECT v1 HYBRID FOR PROMOTION

**Arif's rule (verbatim):**
> "If Falkor adds useful unique evidence in 1/50: GMU=2%, then don't maintain graph retrieval just because 'GraphRAG sounds advanced.'"

**Our GMU: 0%. The rule triggers: drop graph retrieval from v1.**

**Per the production promotion gate (Arif's spec):**
- Grounded relevance: C = B (no gain)
- Provenance completeness: C = B (admit gate rejects nothing in this set)
- Temporal accuracy: C = B
- Admissibility violations: 0
- Latency p95: 125ms (well under 1500ms budget) ✅
- **Unique graph value: 0%** ❌
- Regression queries: 0 critical ✅

**One of three required gates fails. v1 hybrid REJECTED for promotion.**

## 5. WHAT TO DO INSTEAD

### Option A (RECOMMENDED per Law 10 simplicity):
Drop FalkorDB from v1. Config B (vector-only) IS v1.5 candidate.

### Option B (if graph truly needed):
- First **populate FalkorDB** with real data (not skeleton labels)
- Then re-run eval
- Until then, RRF is "ceremonial" — no real second signal to fuse

### Option C (v2 speculative, F13-staged):
- Add bge-m3 vector search at Qdrant (frozen model) — current v1 uses token-overlap
- Add LLM reasoning layer for re-ranking
- Re-evaluate

## 6. NO WIRING TO arif_memory

Per F13 + Arif's promotion gate: **I will NOT modify tool_13_arif_memory.py.** The v1 compiler stays as a standalone experiment file. Zero production wiring.

If/when FalkorDB has real data, re-evaluate. Until then, the v1 build exists, has receipts, and the verdict is honest: graph added nothing.

## 7. WHAT WAS VALUABLE IN THIS BUILD

Even though the verdict is REJECT, the eval process produced these real artifacts:

1. **50-query stratified set** at `eval/query_set_v1.jsonl` (reusable)
2. **3-config runner** at `eval/eval_runner.py` (reusable for v1.5/v2)
3. **Honest raw results** at `eval/results_v1.jsonl`
4. **Summary** at `eval/summary_v1.json`
5. **Compiler code** at `server.py` (reusable, but with FalkorDB leg removed)
6. **Spec** at `/root/AAA/docs/blueprints/ARIF-MEMORY-HYBRID-CONTEXT-COMPILER-V1.md` (doctrine preserved)
7. **This verdict** at `EVAL-V1-VERDICT-2026-10-03.md` (F2 receipt)

## 8. WHAT I LEARNED (calibration)

I built 545 LOC of compiler and integration, smoke-tested 3 queries that gave the **illusion of green** (Falkor returned 1 "candidate" each = the summary chunk), then ran the 50-query eval that exposed **the smoke test was insufficient**. The summary chunk fooled me into thinking graph contributed.

**Calibration rule for next eval:**
- "1 Falkor candidate per query" + "0 Falkor in final bundle" = a detector signal worth reporting
- Token-overlap scoring on Falkor nodes with null text fields can never admit anything → GMU = 0
- The right move is: **populate Falkor first, then eval**

## 9. RECEIPTS

- [receipt: /root/AAA/mcp/arif_memory_hybrid_compiler/eval/query_set_v1.jsonl:50-queries-5-strata]
- [receipt: /root/AAA/mcp/arif_memory_hybrid_compiler/eval/results_v1.jsonl:150-records-3-configs-50-queries]
- [receipt: /root/AAA/mcp/arif_memory_hybrid_compiler/eval/summary_v1.json:aggregate-stats]
- [receipt: falkor-candidates-50-of-50-but-admitted-0-of-50]
- [receipt: latency-p95-125ms-under-1500ms-budget]
- [receipt: gmu-0-percent-falkor-not-earning-keep]
- [receipt: v1-REJECTED-not-wired-to-arif_memory]

## 10. WHAT ARIF ASKS

> "Falsify graph value, then SAH wire only if graph/fusion earns its existence."

**Answer: graph did NOT earn its existence. NO WIRE. Drop Falkor from v1. Config B (vector-only) becomes v1.5 candidate after bge-m3 vector search is added (frozen model, v2 work).**

## 11. MUTATION THIS TURN

ZERO. No source mutation. No wiring. Eval + verdict only.
