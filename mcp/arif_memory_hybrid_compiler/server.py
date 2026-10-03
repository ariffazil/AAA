"""
arif_memory Hybrid Context Compiler — v1 INTERNAL PIPE
════════════════════════════════════════════════════════════
This is the IMPLEMENTATION behind arif_memory(mode="recall", hybrid=true).
It is NOT a public MCP surface. It runs on :18095 internally and is called
only by arif_memory canonical handler.

LAW (Arif 2026-10-03): "One Door ≠ One Pipe"
  - The DOOR is arif_memory (constitutional interface).
  - The PIPE is this compiler (replaceable retrieval impl).

DISCOVERED REALITY (v1 smoke test 2026-10-03):
  - Qdrant: arifos_memory collection is EMPTY (0 points).
  - Qdrant: witness_semantic_bge_m3 has 4213 real chunks.
  - Qdrant: no embedding model loaded. Must use scroll/filter OR local bge-m3.
  - FalkorDB: 79 nodes, 13 labels, but most fields are None (graphiti skeleton).
  - FalkorDB: relations are real (ALLOWED, REVIEWED, EXECUTED_ON, etc.)
  - bge-m3 is FROZEN per Arif. We do NOT load a new embedding model in v1.
  - v1 uses Qdrant scroll/filter + FalkorDB relations. v2 adds semantic vector query.

DITEMPA BUKAN DIBERI ⚒️
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any

import redis as redis_lib
from fastmcp import FastMCP
from qdrant_client import QdrantClient

logger = logging.getLogger("arif_memory.hybrid_compiler")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")

# ── CONFIG (hardcoded, no env override) ───────────────────────────
QDRANT_HOST = "127.0.0.1"
QDRANT_PORT = 6333
FALKORDB_HOST = "127.0.0.1"
FALKORDB_PORT = 6380
FALKORDB_GRAPH = "arifos"
AUDIT_LOG = "/root/.local/share/arifos/runtime/audit/arif_memory_context.log"
RRF_K = 60
DEFAULT_BUDGET = 2000
MAX_BUDGET = 8000
MCP_PORT = 18095

# Real L3 collection (4213 real chunks). v1 uses scroll+filter (no embedding).
SEMANTIC_COLLECTION = "witness_semantic_bge_m3"
# Per Arif: bge-m3 is FROZEN. We do NOT load the model. v2 will add it.

# ── DATA TYPES ────────────────────────────────────────────────────
@dataclass
class Chunk:
    id: str
    text: str
    source: str
    vector_score: float = 0.0
    graph_score: float = 0.0
    rrf_score: float = 0.0
    provenance: dict = field(default_factory=dict)
    rejected: bool = False
    reject_reasons: list = field(default_factory=list)

@dataclass
class RetrievalReceipt:
    query_hash: str
    n_qdrant: int
    n_falkor: int
    n_admitted: int
    n_rejected: int
    cost_ms: int
    sources_used: list
    fallback_used: str | None = None
    ts: str = ""

# ── AUDIT LOG (ordinary log, not VAULT999) ──────────────────────
def log_receipt(receipt: RetrievalReceipt):
    receipt.ts = datetime.now(timezone.utc).isoformat()
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(asdict(receipt)) + "\n")

# ── QDRANT RETRIEVER (v1: scroll+text-filter; v2: vector+caching) ──
class QdrantRetriever:
    """
    v1: Uses scroll + simple text match (token overlap scoring).
        v2: Will use bge-m3 vectors (frozen) with Qdrant-side query.
    """
    def __init__(self):
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, timeout=15)
        self.collection = SEMANTIC_COLLECTION

    def search(self, query: str, peer: str | None, limit: int = 30) -> list[Chunk]:
        """
        v1 strategy:
          1. Scroll all points (bounded by limit)
          2. Score by simple token overlap (proxy for semantic)
          3. Return top N by score
        v2: replace with bge-m3 vector search (frozen).
        """
        # Normalize query: lowercase, split to tokens
        q_tokens = set(t.lower() for t in query.split() if len(t) > 2)
        if not q_tokens:
            return []

        try:
            chunks = []
            offset = None
            # Scroll through up to 1000 points (bounded — v2 will use proper search)
            scrolled_count = 0
            max_scroll = 1000
            while scrolled_count < max_scroll:
                points, offset = self.client.scroll(
                    collection_name=self.collection,
                    limit=100,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False,
                )
                for p in points:
                    text = (p.payload or {}).get("text", "")
                    if not text:
                        continue
                    # Token overlap score
                    text_tokens = set(t.lower() for t in text.split() if len(t) > 2)
                    if not text_tokens:
                        continue
                    overlap = len(q_tokens & text_tokens)
                    if overlap == 0:
                        continue
                    score = overlap / len(q_tokens)  # recall-style
                    chunks.append(Chunk(
                        id=str(p.id),
                        text=text,
                        source=f"qdrant:{self.collection}",
                        vector_score=score,
                        provenance={
                            "collection": self.collection,
                            "qdrant_id": str(p.id),
                            "source": (p.payload or {}).get("source", ""),
                            "doc_type": (p.payload or {}).get("doc_type", ""),
                            "section": (p.payload or {}).get("section", ""),
                            "ts": (p.payload or {}).get("ts", ""),
                        },
                    ))
                scrolled_count += len(points)
                if offset is None:
                    break

            # Sort by score, take top N
            chunks.sort(key=lambda c: -c.vector_score)
            return chunks[:limit]
        except Exception as e:
            logger.exception(f"qdrant search failed: {e}")
            return []

# ── FALKORDB RETRIEVER (entity + relations) ───────────────────────
class FalkorRetriever:
    """
    v1: Returns relations among real nodes.
        Most fields are None in current graph (graphiti skeleton).
        We return relation triples + claim text where present.
    v2: Add vector similarity on Claim/Episode.text.
    """
    def __init__(self):
        self.r = redis_lib.Redis(
            host=FALKORDB_HOST, port=FALKORDB_PORT, decode_responses=True
        )

    def search(self, query: str, peer: str | None, hops: int = 1, limit: int = 20) -> list[Chunk]:
        q_tokens = set(t.lower() for t in query.split() if len(t) > 2)
        if not q_tokens:
            return []

        chunks = []

        # 1. Search Claim nodes (most likely to have text)
        try:
            # FalkorDB uses positional params, not "params" keyword
            cypher_claims = """
            MATCH (c:Claim)
            WHERE c.text IS NOT NULL OR c.claim IS NOT NULL
            RETURN c.id, c.text, c.claim, c.subject
            LIMIT $limit
            """
            result = self.r.execute_command(
                "GRAPH.QUERY", FALKORDB_GRAPH, cypher_claims, "COMPACT",
                str(limit * 2)
            )
            if len(result) > 1:
                for row in result[1]:
                    if len(row) >= 3:
                        cid, ctext, cclaim, csubject = ("" if row[0] is None else str(row[0]), "" if row[1] is None else str(row[1]), "" if row[2] is None else str(row[2]), "" if len(row) < 4 or row[3] is None else str(row[3]))
                        text = ctext or cclaim or csubject
                        if not text:
                            continue
                        # Token overlap score
                        text_tokens = set(t.lower() for t in text.split() if len(t) > 2)
                        overlap = len(q_tokens & text_tokens)
                        if overlap == 0:
                            continue
                        score = overlap / len(q_tokens)
                        chunks.append(Chunk(
                            id=f"falkor:Claim:{cid}",
                            text=text,
                            source="falkor:Claim",
                            graph_score=score,
                            provenance={
                                "falkor_id": cid,
                                "label": "Claim",
                                "subject": csubject,
                            },
                        ))
        except Exception as e:
            logger.warning(f"falkor Claim query failed: {e}")

        # 2. Search Document nodes
        try:
            cypher_docs = """
            MATCH (d:Document)
            WHERE d.path IS NOT NULL OR d.title IS NOT NULL
            RETURN d.id, d.title, d.path
            LIMIT $limit
            """
            result = self.r.execute_command(
                "GRAPH.QUERY", FALKORDB_GRAPH, cypher_docs, "COMPACT",
                str(limit)
            )
            if len(result) > 1:
                for row in result[1]:
                    if len(row) >= 3:
                        did, dtitle, dpath = ("" if row[0] is None else str(row[0]), "" if row[1] is None else str(row[1]), "" if row[2] is None else str(row[2]))
                        text = dtitle or dpath
                        if not text:
                            continue
                        text_tokens = set(t.lower() for t in text.split() if len(t) > 2)
                        overlap = len(q_tokens & text_tokens)
                        if overlap == 0:
                            continue
                        score = overlap / len(q_tokens) * 0.8  # lower weight for doc structure
                        chunks.append(Chunk(
                            id=f"falkor:Document:{did}",
                            text=text,
                            source="falkor:Document",
                            graph_score=score,
                            provenance={
                                "falkor_id": did,
                                "label": "Document",
                                "path": dpath,
                            },
                        ))
        except Exception as e:
            logger.warning(f"falkor Document query failed: {e}")

        # 3. Return relations (provenance, not candidates)
        # Note: relations in current graph have None endpoints. We capture structure.
        try:
            cypher_rels = """
            MATCH (n)-[r]->(m)
            RETURN type(r), count(r) AS n
            LIMIT 20
            """
            rel_result = self.r.execute_command(
                "GRAPH.QUERY", FALKORDB_GRAPH, cypher_rels, "COMPACT"
            )
            if len(rel_result) > 1 and rel_result[1]:
                rel_summary = ", ".join(
                    f"{row[0]}={row[1]}" for row in rel_result[1] if len(row) >= 2
                )
                # Attach as a single Chunk for observability (not for RRF rank)
                chunks.append(Chunk(
                    id="falkor:relations:summary",
                    text=f"Available relations: {rel_summary}",
                    source="falkor:Graph",
                    graph_score=0.0,  # not ranked
                    provenance={"rel_count": sum(int(row[1]) for row in rel_result[1] if len(row) >= 2 and str(row[1]).isdigit())},
                ))
        except Exception as e:
            logger.warning(f"falkor relations query failed: {e}")

        chunks.sort(key=lambda c: -c.graph_score)
        return chunks[:limit]

# ── ID NORMALIZER ────────────────────────────────────────────────
class IdentityResolver:
    def normalize(self, chunks: list[Chunk]) -> list[Chunk]:
        seen = set()
        for c in chunks:
            if c.id in seen:
                c.id = f"{c.id}#{c.source}"
            seen.add(c.id)
        return chunks

# ── RRF FUSER ────────────────────────────────────────────────────
class RRFFuser:
    def fuse(self, ranked_lists: list[list[Chunk]], k: int = RRF_K) -> list[Chunk]:
        scores: dict[str, Chunk] = {}
        for lst in ranked_lists:
            for rank, chunk in enumerate(lst):
                # Skip relation summary chunk (not a candidate)
                if "summary" in chunk.id and "relations" in chunk.id:
                    continue
                if chunk.id not in scores:
                    scores[chunk.id] = chunk
                scores[chunk.id].rrf_score += 1.0 / (k + rank + 1)
        fused = sorted(scores.values(), key=lambda c: -c.rrf_score)
        return fused

# ── ADMISSIBILITY GATE (Arif's law: Admit BEFORE Budget) ─────────
class AdmissibilityGate:
    """
    v1 SRO rules (per Arif):
      - text non-empty and ≥ 10 chars
      - provenance: source path OR falkor_id present
      - v2: vault attestation check, lifecycle check
    """
    def admit(self, chunks: list[Chunk], payload: dict) -> list[Chunk]:
        for c in chunks:
            if not c.text or len(c.text.strip()) == 0:
                c.rejected = True
                c.reject_reasons.append("SRO_MISSING: empty text")
                continue
            if len(c.text) < 10:
                c.rejected = True
                c.reject_reasons.append("SRO_MISSING: text < 10 chars")
                continue
            # Provenance: at least one of source/qdrant_id/falkor_id must be present
            has_provenance = bool(
                c.provenance.get("source")
                or c.provenance.get("qdrant_id")
                or c.provenance.get("falkor_id")
            )
            if not has_provenance:
                c.rejected = True
                c.reject_reasons.append("SRO_MISSING: no provenance")
                continue
            # FalkorDB claim needs at least text content
            if c.source.startswith("falkor:") and not c.text.strip():
                c.rejected = True
                c.reject_reasons.append("SRO_MISSING: empty falkor content")
                continue
            # All passed
            c.provenance["admitted"] = True
        return chunks

# ── BUDGET PACKER ────────────────────────────────────────────────
class BudgetPacker:
    def pack(self, chunks: list[Chunk], budget: int) -> list[Chunk]:
        # v1: char-based approximation (1 token ≈ 4 chars).
        # v2: tiktoken for exact counting.
        char_budget = budget * 4
        out = []
        used = 0
        for c in chunks:
            if c.rejected:
                continue
            cost = len(c.text)
            if used + cost > char_budget:
                if used < char_budget * 0.8:
                    c.text = c.text[:char_budget - used] + "\n[...TRUNCATED]"
                    out.append(c)
                    used = char_budget
                break
            out.append(c)
            used += cost
        return out

# ── COMPILER (THE PIPE) ──────────────────────────────────────────
class HybridContextCompiler:
    def __init__(self):
        self.qdrant = QdrantRetriever()
        self.falkor = FalkorRetriever()
        self.normalizer = IdentityResolver()
        self.fuser = RRFFuser()
        self.gate = AdmissibilityGate()
        self.packer = BudgetPacker()

    def compile(self, query: str, payload: dict) -> dict:
        start = time.time()
        peer = payload.get("peer", "arif")
        budget = min(payload.get("budget", DEFAULT_BUDGET), MAX_BUDGET)
        graph_hops = payload.get("graph_expand", 1)

        # 1. Retrieve (Qdrant: semantic/sparse, FalkorDB: entity/path)
        q_results = self.qdrant.search(query, peer, limit=30)
        g_results = self.falkor.search(query, peer, hops=graph_hops, limit=20)

        sources_used = []
        if q_results:
            sources_used.append(f"qdrant({self.qdrant.collection})")
        if g_results:
            sources_used.append(f"falkor({FALKORDB_GRAPH})")
        fallback = None
        if not q_results and not g_results:
            fallback = "both_backends_down"

        # 2. Normalize IDs
        all_chunks = self.normalizer.normalize(q_results + g_results)

        # 3. RRF fuse (pre-rank for budget priority)
        fused = self.fuser.fuse([q_results, g_results])

        # 4. Admit (SRO + provenance + lifecycle)
        admitted_attempt = self.gate.admit(fused, payload)

        # 5. Budget pack
        packed = self.packer.pack(admitted_attempt, budget)

        # 6. Evidence bundle
        n_admitted = len(packed)
        n_rejected = sum(1 for c in all_chunks if c.rejected)
        n_q = len(q_results)
        n_g = len(g_results)

        evidence = {
            "chunks": [
                {
                    "id": c.id,
                    "text": c.text,
                    "source": c.source,
                    "rrf_score": round(c.rrf_score, 6),
                    "provenance": c.provenance,
                } for c in packed
            ],
            "rejected": [
                {"id": c.id, "reasons": c.reject_reasons, "source": c.source}
                for c in all_chunks if c.rejected
            ],
            "counts": {
                "qdrant_candidates": n_q,
                "falkor_candidates": n_g,
                "admitted": n_admitted,
                "rejected": n_rejected,
            },
            "sources_used": sources_used,
            "fallback": fallback,
            "budget": budget,
            "cost_ms": int((time.time() - start) * 1000),
        }

        # 7. Receipt (ordinary log)
        receipt = RetrievalReceipt(
            query_hash=hashlib.sha256(query.encode()).hexdigest()[:16],
            n_qdrant=n_q, n_falkor=n_g,
            n_admitted=n_admitted, n_rejected=n_rejected,
            cost_ms=evidence["cost_ms"],
            sources_used=sources_used,
            fallback_used=fallback,
        )
        log_receipt(receipt)
        evidence["receipt"] = asdict(receipt)

        return evidence

# ── MCP SERVER (FastMCP, :18095) ──────────────────────────────────
mcp = FastMCP("arif_memory.hybrid_compiler")
compiler = HybridContextCompiler()

@mcp.tool
def hybrid_compile(query: str, payload: dict | None = None) -> dict:
    """INTERNAL: Compile hybrid context. Called by arif_memory recall only."""
    return compiler.compile(query, payload or {})

if __name__ == "__main__":
    mcp.run(transport="http", port=MCP_PORT, host="127.0.0.1")
