#!/usr/bin/env python3
"""
P0.3/P0.4 — Qdrant Skill Mesh Population & Capability Tagging
=============================================================
Reads all 184 SKILL.md files under /root/AAA/skills/, classifies each into
a capability tier (fed-reasoning-heavy, fed-multimodal-vision, etc.),
creates the arifOS_skill_mesh collection in Qdrant (:6333), and indexes
every skill using all-MiniLM-L6-v2 embeddings.

Also injects capability_tier + ecology_state metadata frontmatter into
each SKILL.md file for future reference.

Forged: 2026-08-10 by 333-AGI under F13 directive.
"""

import os
import re
import hashlib
import time
import sys
import json
from pathlib import Path
from typing import Optional

import yaml
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# ── Config ────────────────────────────────────────────────────────
SKILLS_ROOT = Path("/root/AAA/skills")
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "arifOS_skill_mesh"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2 output dim
BATCH_SIZE = 32

# ── Capability tier classification ────────────────────────────────
# Keyword-based heuristic: scan skill name + description for capability signals.
# This is Phase 1 — future iterations will learn from actual usage patterns.

CAPABILITY_PATTERNS = {
    "fed-reasoning-heavy": [
        "reasoning",
        "judge",
        "plan",
        "think",
        "analysis",
        "verdict",
        "constitutional",
        "critique",
        "evaluate",
        "strategy",
        "architecture",
        "design",
        "forge-evaluate",
        "apex",
        "godel",
        "humility",
        "cognitive",
        "atlas",
        "eureka",
        "paradox",
        "logic",
        "proof",
        "axiom",
        "refactor",
    ],
    "fed-multimodal-vision": [
        "vision",
        "image",
        "video",
        "visual",
        "screenshot",
        "ocr",
        "multimodal",
        "photo",
        "picture",
        "draw",
        "render",
        "vlm",
        "camera",
        "canvas",
        "imagegen",
        "imag(e|ing)",
        "mini.max",
    ],
    "fed-long-context": [
        "document",
        "pdf",
        "context",
        "long",
        "compress",
        "summarize",
        "ingest",
        "article",
        "paper",
        "book",
        "literature",
        "chunk",
        "extract",
        "readme",
        "audit",
        "report",
    ],
    "fed-agent-subagent": [
        "subagent",
        "spawn",
        "parallel",
        "orchestrat",
        "dispatch",
        "federation",
        "mesh",
        "sync",
        "onboarding",
        "handoff",
        "delegate",
        "agentic",
        "cross-agent",
        "a2a",
        "dag",
        "workflow",
        "pipeline",
    ],
    "fed-realtime-voice": [
        "voice",
        "audio",
        "speech",
        "tts",
        "stt",
        "sound",
        "music",
        "transcribe",
        "listen",
        "speak",
    ],
}


def classify_capability(name: str, description: str) -> str:
    """Classify a skill into its capability tier based on keyword heuristics."""
    text = (name + " " + description).lower()
    scores = {}
    for tier, patterns in CAPABILITY_PATTERNS.items():
        score = sum(1 for p in patterns if re.search(p, text))
        scores[tier] = score

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "fed-agent-subagent"  # Default: most general
    return best


# ── SKILL.md reader ────────────────────────────────────────────────
def read_skill_md(filepath: Path) -> dict:
    """Parse a SKILL.md file — extract name, description, and frontmatter."""
    try:
        content = filepath.read_text()
    except Exception:
        return {"name": filepath.parent.name, "description": "", "filepath": str(filepath)}

    # Try to extract YAML frontmatter
    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                pass
            body = parts[2]

    # Extract name from frontmatter or filename
    name = frontmatter.get("name") or frontmatter.get("title") or filepath.parent.name

    # Extract description
    description = frontmatter.get("description", "")
    if not description:
        # Grab first meaningful line of body
        for line in body.strip().split("\n"):
            clean = line.strip().lstrip("#").strip()
            if clean and len(clean) > 10:
                description = clean[:200]
                break

    return {
        "name": name,
        "description": description,
        "frontmatter": frontmatter,
        "filepath": str(filepath),
        "skill_id": filepath.parent.name,
    }


def inject_metadata(filepath: Path, capability_tier: str, ecology_state: str = "WARM"):
    """Inject capability_tier and ecology_state into SKILL.md frontmatter."""
    try:
        content = filepath.read_text()
    except Exception:
        return

    # Check if metadata already exists
    if "capability_tier:" in content and "ecology_state:" in content:
        return  # Already tagged

    new_content = content

    # Add to YAML frontmatter if it exists
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            # Add fields to frontmatter
            fm_lines = fm_text.strip().split("\n")
            has_cap = any("capability_tier:" in line for line in fm_lines)
            has_eco = any("ecology_state:" in line for line in fm_lines)

            new_fm_lines = list(fm_lines)
            if not has_cap:
                new_fm_lines.append(f"capability_tier: {capability_tier}")
            if not has_eco:
                new_fm_lines.append(f"ecology_state: {ecology_state}")

            new_content = f"---\n" + "\n".join(new_fm_lines) + f"\n---{parts[2]}"
    else:
        # No frontmatter — add one
        new_content = f"---\ncapability_tier: {capability_tier}\necology_state: {ecology_state}\n---\n{content}"

    if new_content != content:
        filepath.write_text(new_content)
        return True
    return False


# ── Main ────────────────────────────────────────────────────────────
def main():
    print("🔍 Qdrant Skill Mesh Population — P0.3/P0.4")
    print(f"   Skills root: {SKILLS_ROOT}")
    print(f"   Qdrant: {QDRANT_HOST}:{QDRANT_PORT}")

    # ── Discover all SKILL.md files ─────────────────────────────────
    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    # Exclude _retired
    skill_files = [f for f in skill_files if "_retired" not in str(f)]
    print(f"   Found {len(skill_files)} SKILL.md files (excluding _retired)")

    # ── Load encoder ────────────────────────────────────────────────
    print("   Loading encoder (all-MiniLM-L6-v2)...")
    encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    print("   Encoder ready.")

    # ── Create/Recreate Qdrant collection ────────────────────────────
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    # Check if collection exists
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in collections:
        print(f"   Dropping existing collection '{COLLECTION_NAME}'...")
        client.delete_collection(COLLECTION_NAME)

    print(f"   Creating collection '{COLLECTION_NAME}' (vectors={VECTOR_SIZE})...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print("   Collection created.")

    # ── Parse, classify, embed, index ────────────────────────────────
    tagged_count = 0
    indexed_count = 0
    points_batch = []

    for i, filepath in enumerate(skill_files):
        skill = read_skill_md(filepath)
        name = skill["name"]
        desc = skill["description"]
        skill_id = skill["skill_id"]

        # Classify
        tier = classify_capability(name, desc)

        # Inject metadata into SKILL.md (P0.4)
        if inject_metadata(filepath, tier):
            tagged_count += 1

        # Embed
        text = f"{name}: {desc}" if desc else name
        vector = encoder.encode(text).tolist()

        # Build payload
        payload = {
            "skill_id": skill_id,
            "name": name,
            "description": desc[:500],
            "capability_tier": tier,
            "ecology_state": "WARM",
            "total_invocations": 0,
            "success_count": 0,
            "avg_latency_ms": 0.0,
            "filepath": str(filepath),
        }

        # Use hash-based ID
        point_id = abs(hash(skill_id)) % (2**63)
        points_batch.append(PointStruct(id=point_id, vector=vector, payload=payload))

        # Batch upsert
        if len(points_batch) >= BATCH_SIZE:
            client.upsert(collection_name=COLLECTION_NAME, points=points_batch)
            indexed_count += len(points_batch)
            print(f"   Indexed {indexed_count}/{len(skill_files)} skills...")
            points_batch = []

    # Flush remaining
    if points_batch:
        client.upsert(collection_name=COLLECTION_NAME, points=points_batch)
        indexed_count += len(points_batch)
        print(f"   Indexed {indexed_count}/{len(skill_files)} skills.")

    # ── Verify ───────────────────────────────────────────────────────
    count = client.count(collection_name=COLLECTION_NAME).count
    print(f"\n✅ DONE: {count} skills indexed in '{COLLECTION_NAME}'")
    print(f"   Metadata injected into {tagged_count} SKILL.md files")

    # ── Capability distribution ──────────────────────────────────────
    tiers = {}
    for tier in CAPABILITY_PATTERNS:
        tiers[tier] = sum(
            1
            for f in skill_files
            if classify_capability(*(read_skill_md(f)["name"], read_skill_md(f)["description"])) == tier
        )
    print(f"   Capability distribution: {json.dumps(tiers, indent=2)}")

    return {
        "skills_indexed": count,
        "skills_tagged": tagged_count,
        "capability_distribution": tiers,
    }


if __name__ == "__main__":
    result = main()
    print(f"\n📊 RESULT: {json.dumps(result)}")
