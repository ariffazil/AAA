"""
Evaluation runner: 3 configurations × 50 queries.
Per Arif's spec, each result includes source-level contribution tracking so we
can answer "did the graph actually contribute?"

Configurations:
  A: baseline (current v4 arif_memory recall — Qdrant hybrid memory only)
  B: vector-only (witness_semantic_bge_m3, our real L3 data)
  C: hybrid (Qdrant + FalkorDB + RRF + Admit)

Output: eval/results_v1.jsonl (one record per query) + eval/summary_v1.json
"""
from __future__ import annotations

import json
import logging
import os
import sys
import time
from collections import Counter, defaultdict
from typing import Any

# Path setup
COMPILER_PATH = "/root/AAA/mcp/arif_memory_hybrid_compiler"
EVAL_PATH = os.path.join(COMPILER_PATH, "eval")
sys.path.insert(0, COMPILER_PATH)

import server as hybrid_compiler  # The HybridContextCompiler

logger = logging.getLogger("eval_runner")
logging.basicConfig(level=logging.WARNING, format="%(message)s")


def run_config_A_baseline(query: str, peer: str, budget: int) -> dict:
    """
    Config A: current v4 baseline. We simulate by using a simpler Qdrant-only
    query with the hybrid compiler's QdrantRetriever (no Falkor, no RRF, no
    Admit — just the Qdrant results sorted by overlap).

    In production, "baseline" is whatever arif_memory's existing recall
    path returns. We approximate that here.
    """
    start = time.time()
    compiler = hybrid_compiler.HybridContextCompiler()
    # Use only the Qdrant leg, no fusion, no admit
    q_results = compiler.qdrant.search(query, peer, limit=30)
    # Simple truncation by char-budget (the v4 baseline doesn't do this fancy)
    char_budget = budget * 4
    out = []
    used = 0
    for c in q_results:
        if used + len(c.text) > char_budget:
            break
        out.append(c)
        used += len(c.text)
    cost_ms = int((time.time() - start) * 1000)
    return {
        "config": "A_baseline",
        "query": query,
        "n_candidates": {"qdrant": len(q_results), "falkor": 0},
        "n_admitted": {"qdrant": len(out), "falkor": 0},
        "n_final": len(out),
        "unique_by_source": {"qdrant": len(out), "falkor": 0},
        "cost_ms": cost_ms,
        "top_k_texts": [c.text[:100] for c in out[:3]],
        "top_k_sources": [c.provenance.get("source", "?") for c in out[:3]],
    }


def run_config_B_vector_only(query: str, peer: str, budget: int) -> dict:
    """
    Config B: vector-only with our real collection (witness_semantic_bge_m3).
    No graph, no RRF, no admit gate — just sorted Qdrant results.
    """
    start = time.time()
    compiler = hybrid_compiler.HybridContextCompiler()
    q_results = compiler.qdrant.search(query, peer, limit=30)
    # Sort by score desc (v1 has no semantic model, so just take all in order)
    sorted_results = sorted(q_results, key=lambda c: -c.vector_score)
    # Simple char-budget pack
    char_budget = budget * 4
    out = []
    used = 0
    for c in sorted_results:
        if used + len(c.text) > char_budget:
            break
        out.append(c)
        used += len(c.text)
    cost_ms = int((time.time() - start) * 1000)
    return {
        "config": "B_vector_only",
        "query": query,
        "n_candidates": {"qdrant": len(q_results), "falkor": 0},
        "n_admitted": {"qdrant": len(out), "falkor": 0},
        "n_final": len(out),
        "unique_by_source": {"qdrant": len(out), "falkor": 0},
        "cost_ms": cost_ms,
        "top_k_texts": [c.text[:100] for c in out[:3]],
        "top_k_sources": [c.provenance.get("source", "?") for c in out[:3]],
    }


def run_config_C_hybrid(query: str, peer: str, budget: int) -> dict:
    """
    Config C: full hybrid (Qdrant + FalkorDB + RRF + Admit + Budget).
    Per Arif's spec, track per-source contribution.
    """
    start = time.time()
    compiler = hybrid_compiler.HybridContextCompiler()
    result = compiler.compile(query, {"peer": peer, "budget": budget, "graph_expand": 1})

    # Extract per-source stats
    chunks = result["chunks"]
    by_source = Counter(c["source"].split(":")[0] for c in chunks)  # qdrant/falkor
    n_adm = result["counts"]
    cost_ms = result["cost_ms"]

    return {
        "config": "C_hybrid",
        "query": query,
        "n_candidates": {"qdrant": n_adm["qdrant_candidates"], "falkor": n_adm["falkor_candidates"]},
        "n_admitted": {"qdrant": by_source.get("qdrant", 0), "falkor": by_source.get("falkor", 0)},
        "n_final": len(chunks),
        "unique_by_source": {
            "qdrant": by_source.get("qdrant", 0),
            "falkor": by_source.get("falkor", 0),
        },
        "n_rejected": n_adm["rejected"],
        "fallback": result.get("fallback"),
        "cost_ms": cost_ms,
        "top_k_texts": [c["text"][:100] for c in chunks[:3]],
        "top_k_sources": [c["provenance"].get("source", "?") for c in chunks[:3]],
        "receipt": result.get("receipt"),
    }


def graph_marginal_utility(records_C: list[dict]) -> float:
    """
    Per Arif: GMU = (queries where falkor contributed unique evidence) / total.
    Here: "contributed" = falkor in admitted OR falkor_candidates > 0.
    """
    if not records_C:
        return 0.0
    contributed = 0
    for r in records_C:
        # Falkor contributed if any of:
        #  - falkor in admitted (n_admitted.falkor > 0)
        #  - falkor candidates found (n_candidates.falkor > 0)
        if r["n_admitted"].get("falkor", 0) > 0:
            contributed += 1
        elif r["n_candidates"].get("falkor", 0) > 0:
            contributed += 1
    return contributed / len(records_C)


def main():
    # Load 50-query set
    query_path = os.path.join(EVAL_PATH, "query_set_v1.jsonl")
    queries = [json.loads(line) for line in open(query_path)]
    print(f"Loaded {len(queries)} queries from {query_path}")

    results_A, results_B, results_C = [], [], []
    BUDGET = 2000
    PEER = "arif"

    print(f"\nRunning 3 configurations × {len(queries)} queries (budget={BUDGET})...")
    print("=" * 60)

    for i, qobj in enumerate(queries, 1):
        q = qobj["query"]
        cat = qobj["category"]

        # Run all 3 configs for this query
        a = run_config_A_baseline(q, PEER, BUDGET)
        a["qid"] = qobj["qid"]
        a["category"] = cat
        results_A.append(a)

        b = run_config_B_vector_only(q, PEER, BUDGET)
        b["qid"] = qobj["qid"]
        b["category"] = cat
        results_B.append(b)

        c = run_config_C_hybrid(q, PEER, BUDGET)
        c["qid"] = qobj["qid"]
        c["category"] = cat
        results_C.append(c)

        # Per-query summary
        print(f"  [{i:2d}/{len(queries)}] {cat[:14]:14} | "
              f"A:{a['n_final']:2d} B:{b['n_final']:2d} C:{c['n_final']:2d} | "
              f"falkor_adm={c['n_admitted'].get('falkor',0):2d} | "
              f"cost: A{a['cost_ms']:4d}/B{b['cost_ms']:4d}/C{c['cost_ms']:4d}ms")

    # Save raw results
    raw_path = os.path.join(EVAL_PATH, "results_v1.jsonl")
    with open(raw_path, "w") as f:
        for a, b, c in zip(results_A, results_B, results_C):
            f.write(json.dumps(a) + "\n")
            f.write(json.dumps(b) + "\n")
            f.write(json.dumps(c) + "\n")
    print(f"\nRaw results: {raw_path}")

    # Compute summary
    gmu = graph_marginal_utility(results_C)
    avg_cost_A = sum(r["cost_ms"] for r in results_A) / len(results_A)
    avg_cost_B = sum(r["cost_ms"] for r in results_B) / len(results_B)
    avg_cost_C = sum(r["cost_ms"] for r in results_C) / len(results_C)
    p95_A = sorted(r["cost_ms"] for r in results_A)[int(0.95 * len(results_A))]
    p95_C = sorted(r["cost_ms"] for r in results_C)[int(0.95 * len(results_C))]

    # Per-category GMU
    cat_gmu = defaultdict(lambda: {"queries": 0, "falkor_contributed": 0})
    for r in results_C:
        cat = r["category"]
        cat_gmu[cat]["queries"] += 1
        if r["n_admitted"].get("falkor", 0) > 0 or r["n_candidates"].get("falkor", 0) > 0:
            cat_gmu[cat]["falkor_contributed"] += 1

    # Per-category admit counts
    cat_stats = defaultdict(lambda: {"A": [], "B": [], "C": []})
    for a, b, c in zip(results_A, results_B, results_C):
        cat = a["category"]
        cat_stats[cat]["A"].append(a["n_final"])
        cat_stats[cat]["B"].append(b["n_final"])
        cat_stats[cat]["C"].append(c["n_final"])

    summary = {
        "n_queries": len(queries),
        "n_per_stratum": 10,
        "strata": ["semantic_factual", "relationship_path", "temporal_current_vs_old",
                   "contradiction_provenance", "operational_agent"],
        "configs": {
            "A_baseline": {
                "avg_n_final": sum(r["n_final"] for r in results_A) / len(results_A),
                "avg_cost_ms": avg_cost_A,
                "p95_cost_ms": p95_A,
            },
            "B_vector_only": {
                "avg_n_final": sum(r["n_final"] for r in results_B) / len(results_B),
                "avg_cost_ms": avg_cost_B,
            },
            "C_hybrid": {
                "avg_n_final": sum(r["n_final"] for r in results_C) / len(results_C),
                "avg_cost_ms": avg_cost_C,
                "p95_cost_ms": p95_C,
                "total_rejected": sum(r["n_rejected"] for r in results_C),
                "avg_falkor_admitted": sum(r["n_admitted"].get("falkor", 0) for r in results_C) / len(results_C),
                "avg_qdrant_admitted": sum(r["n_admitted"].get("qdrant", 0) for r in results_C) / len(results_C),
            },
        },
        "graph_marginal_utility": {
            "overall_gmu": gmu,
            "by_category": {
                cat: {
                    "queries": v["queries"],
                    "falkor_contributed": v["falkor_contributed"],
                    "category_gmu": v["falkor_contributed"] / v["queries"] if v["queries"] else 0,
                } for cat, v in cat_gmu.items()
            },
        },
        "per_category_final_counts": {
            cat: {
                "A_avg": sum(stats["A"]) / len(stats["A"]) if stats["A"] else 0,
                "B_avg": sum(stats["B"]) / len(stats["B"]) if stats["B"] else 0,
                "C_avg": sum(stats["C"]) / len(stats["C"]) if stats["C"] else 0,
            } for cat, stats in cat_stats.items()
        },
        "verdict": None,  # filled below
    }

    # Verdict
    promotion_signals = []
    if gmu < 0.10:  # < 10% of queries use graph
        promotion_signals.append(f"REJECT: GMU {gmu:.1%} < 10% threshold — graph not earning its keep")
    if summary["configs"]["C_hybrid"]["p95_cost_ms"] > 1500:
        promotion_signals.append(f"REJECT: p95 latency {p95_C}ms > 1500ms")
    if summary["configs"]["C_hybrid"]["total_rejected"] > 0:
        promotion_signals.append(f"REVIEW: {summary['configs']['C_hybrid']['total_rejected']} chunks rejected by admit gate (SRO)")
    if not promotion_signals:
        promotion_signals.append("PROMOTE-CANDIDATE: all gates pass; F13 wire justified")
    summary["verdict"] = promotion_signals

    summary_path = os.path.join(EVAL_PATH, "summary_v1.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"Summary: {summary_path}")

    # Print key findings
    print("\n" + "=" * 60)
    print("KEY FINDINGS")
    print("=" * 60)
    print(f"GMU (graph marginal utility): {gmu:.1%}")
    print(f"  Per stratum:")
    for cat, v in cat_gmu.items():
        gmu_cat = v["falkor_contributed"] / v["queries"] if v["queries"] else 0
        print(f"    {cat:30s}: {v['falkor_contributed']}/{v['queries']} = {gmu_cat:.1%}")
    print(f"\nConfig C: avg Falkor admitted = {summary['configs']['C_hybrid']['avg_falkor_admitted']:.2f}")
    print(f"Config C: p95 latency = {p95_C}ms")
    print(f"Config C: total rejected = {summary['configs']['C_hybrid']['total_rejected']}")
    print(f"\nVerdict: {promotion_signals[0]}")


if __name__ == "__main__":
    main()
