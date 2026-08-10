#!/usr/bin/env python3
"""
AAA Auto-Ignition Engine — Intent Retriever & JIT Schema Injector.
Discovers skills dynamically via Qdrant semantic search instead of loading 204 static schemas.

Forged: 2026-08-10 by 333-AGI under F13 directive.
Binding: FED Router :7074, Qdrant :6333, arifFlow :7073.
"""

import os
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# ── Singleton encoder (loaded once, reused) ──
_encoder: Optional[SentenceTransformer] = None


def _get_encoder():
    global _encoder
    if _encoder is None:
        _encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    return _encoder


class IntentRetriever:
    """Semantic skill discovery engine. Queries Qdrant for best-matching skills."""

    def __init__(self, qdrant_host="localhost", qdrant_port=6333):
        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.collection = "arifos_skill_mesh"
        self.encoder = _get_encoder()

    def retrieve(
        self,
        task_prompt: str,
        top_k: int = 4,
        score_threshold: float = 0.55,
    ) -> List[Dict]:
        """
        Return top-k matching skills above threshold.
        Excludes COLD (pruned) skills from active context.
        """
        query_vector = self.encoder.encode(task_prompt).tolist()

        hits = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
        ).points

        active = []
        for hit in hits:
            p = hit.payload
            if p.get("ecology_state") != "COLD":
                active.append(
                    {
                        "skill_id": p.get("skill_id", "unknown"),
                        "name": p.get("name", p.get("skill_id", "")),
                        "confidence": round(hit.score, 4),
                        "capability_tier": p.get("capability_tier", "fed-agent-subagent"),
                        "schema": p.get("schema", {}),
                        "ecology_state": p.get("ecology_state", "WARM"),
                    }
                )
        return active

    def index_skill(
        self,
        skill_id: str,
        name: str,
        description: str,
        capability_tier: str,
        schema: dict,
        ecology_state: str = "WARM",
    ):
        """Index a single skill into Qdrant."""
        text = f"{name}: {description}"
        vector = self.encoder.encode(text).tolist()

        self.client.upsert(
            collection_name=self.collection,
            points=[
                {
                    "id": hash(skill_id) % (2**63),
                    "vector": vector,
                    "payload": {
                        "skill_id": skill_id,
                        "name": name,
                        "description": description,
                        "capability_tier": capability_tier,
                        "schema": schema,
                        "ecology_state": ecology_state,
                        "total_invocations": 0,
                        "success_count": 0,
                        "avg_latency_ms": 0.0,
                    },
                }
            ],
        )

    def update_ecology(self, skill_id: str, success: bool, latency_ms: float):
        """Update skill health metrics after execution."""
        points = self.client.retrieve(
            collection_name=self.collection,
            ids=[hash(skill_id) % (2**63)],
            with_payload=True,
        )
        if not points:
            return

        p = points[0].payload
        invocations = p.get("total_invocations", 0) + 1
        successes = p.get("success_count", 0) + (1 if success else 0)
        success_rate = successes / invocations if invocations > 0 else 1.0

        # Ecology state transitions
        if invocations > 10 and success_rate >= 0.95:
            new_state = "HOT"
        elif success_rate < 0.50:
            new_state = "COLD"
        else:
            new_state = p.get("ecology_state", "WARM")

        self.client.set_payload(
            collection_name=self.collection,
            points=[hash(skill_id) % (2**63)],
            payload={
                "total_invocations": invocations,
                "success_count": successes,
                "success_rate": success_rate,
                "avg_latency_ms": latency_ms,
                "ecology_state": new_state,
            },
        )


def build_jit_context(task_prompt: str) -> Dict:
    """
    One-call JIT context builder.
    Returns injected schemas + recommended capability tier.
    """
    retriever = IntentRetriever()
    skills = retriever.retrieve(task_prompt)

    return {
        "system_prompt_tools": [s["schema"] for s in skills],
        "recommended_capability": skills[0]["capability_tier"] if skills else "fed-reasoning-heavy",
        "matched_skills": [s["skill_id"] for s in skills],
        "match_count": len(skills),
    }


# ── CLI for indexing ──
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "search":
        query = " ".join(sys.argv[2:]) or "convert video to ASCII"
        result = build_jit_context(query)
        print(f"Query: {query}")
        print(f"Matched: {result['match_count']} skills → tier: {result['recommended_capability']}")
        for s_id in result["matched_skills"]:
            print(f"  - {s_id}")
    else:
        print("IntentRetriever ready. Usage: python3 intent_retriever.py search <prompt>")
        print("Qdrant: arifos_skill_mesh collection on :6333")
