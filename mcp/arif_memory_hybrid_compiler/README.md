# arif_memory Hybrid Context Compiler — v1

**Status:** v1 ALPHA — wired as internal pipe, opt-in via `hybrid=true`

**Law:** "One Door ≠ One Pipe" (Arif 2026-10-03)
- **Door:** `arif_memory(mode="recall")` (canonical, constitutional, unchanged)
- **Pipe:** This compiler (replaceable, on :18095 internal, opt-in)

## What it does

Aggregates retrieval from two backends (Qdrant + FalkorDB), admits by SRO/provenance rules, packs to token budget, returns evidence bundle.

```
Context = Budget( Admit( Fuse( Retrieve_q(Qdrant), Retrieve_g(FalkorDB) ) ) )
```

## What it does NOT do (v1)

- ❌ Add new public MCP surface
- ❌ Load new embedding model (bge-m3 is FROZEN)
- ❌ LLM reasoning layer
- ❌ Cross-encoder rerank
- ❌ Cross-encoder rewriting
- ❌ Vector search at Qdrant (no model loaded; v1 uses scroll+token-overlap)

## Files

| File | Purpose | LOC |
|---|---|---|
| `server.py` | FastMCP server, hybrid compiler, retrievers, gate, packer | ~470 |
| `integration.py` | Thin wrapper for arif_memory recall handler | ~75 |
| `README.md` | This file | - |

## Backends (live probed)

| Backend | Status | Content |
|---|---|---|
| Qdrant `witness_semantic_bge_m3` | UP, 4213 real chunks | `text`, `source`, `doc_type`, `section`, `ts`, `model` |
| Qdrant `arifos_memory` | UP, 0 points (empty) | - |
| FalkorDB `arifos` | UP, 79 nodes, 13 labels | Episode, Entity, Precedent, Event, Repo, Claim, Day, Topic, Document, Organization, Saga, Community, Episodic (most fields None) |
| Postgres `vault999` | UP, 365k observations (L5 telemetry) | - |
| VAULT999 | UP, 94499 entries (L6) | - |

## API

```python
from arif_memory_hybrid_compiler.integration import hybrid_recall_sync

result = hybrid_recall_sync(
    query="what is the constitutional floor?",
    peer="arif",
    budget=2000,
)
# result = {chunks, rejected, counts, sources_used, fallback, budget, cost_ms, receipt}
```

## Opt-in via arif_memory

```python
arif_memory(
    mode="recall",
    query="...",
    payload={
        "hybrid": True,        # opt-in (default: False = v4 baseline)
        "budget": 2000,
        "peer": "arif",
        "graph_expand": 1,
    },
)
```

## Failure modes

| Mode | Behavior |
|---|---|
| Qdrant unreachable | FalkorDB-only result, flagged in receipt |
| FalkorDB unreachable | Qdrant-only result, flagged in receipt |
| Both unreachable | SABAR with reason; caller can fall back to v4 baseline |
| All candidates fail admit | HOLD with reason, not VOID (no data ≠ all clear) |
| Latency p95 > 1.5s | Fall back to v4 baseline automatically |

## Audit log

Every query writes to `/root/.local/share/arifos/runtime/audit/arif_memory_context.log` (ordinary log, NOT VAULT999 — per Arif's note). VAULT999 reserved for SEAL-class decisions only.

## Evaluation (per Arif)

v1 promotes to v2 only if (50-query fixed set):
- Decision-change rate significantly higher (p<0.05)
- Latency p95 < 1.5s
- Provenance completeness ≥ 99%
- Zero F11 audit failures

## Receipts
- Spec: `/root/AAA/docs/blueprints/ARIF-MEMORY-HYBRID-CONTEXT-COMPILER-V1.md`
- Research: `/root/AAA/docs/audit-receipts/PATH1-RESEARCH-ARIFOS-CONTEXT-2026-10-03.md`
