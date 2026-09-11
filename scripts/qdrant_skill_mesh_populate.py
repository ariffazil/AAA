#!/usr/bin/env python3
"""
P0.3/P0.4 — Skill Mesh Population & Capability Tagging
=======================================================
Reads all SKILL.md files under /root/AAA/skills/, classifies each into
a capability tier (fed-reasoning-heavy, fed-multimodal-vision, etc.),
and indexes every skill into the skill_mesh memory class via the
FederationMemory adapter. The arifOS kernel owns the substrate:
collection lifecycle and embedding are kernel-side (alignment
doctrine §1 — agents never touch the vector store directly).

Also injects capability_tier + ecology_state metadata frontmatter into
each SKILL.md file for future reference.

Forged: 2026-08-10 by 333-AGI under F13 directive.
Migrated 2026-09-12 to federation_memory_adapter (F13 SOVEREIGN
directive — /root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md).
"""

import os
import re
import sys
import json
from pathlib import Path

import yaml

_FEDERATION_DIR = Path(__file__).resolve().parents[1] / "federation"
if str(_FEDERATION_DIR) not in sys.path:
    sys.path.insert(0, str(_FEDERATION_DIR))

from federation_memory_adapter import FederationMemory

# ── Config ────────────────────────────────────────────────────────
SKILLS_ROOT = Path("/root/AAA/skills")
COLLECTION_CLASS = "skill_mesh"  # → arifOS_skill_mesh (memory_classes.yaml)
MEMORY_TIER = "canon"
PROGRESS_EVERY = 32  # print cadence (adapter stores one record per call)

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
    print("🔍 Skill Mesh Population — P0.3/P0.4 (FederationMemory)")
    print(f"   Skills root: {SKILLS_ROOT}")
    print(f"   Memory class: {COLLECTION_CLASS} (via federation_memory_adapter)")

    fm = FederationMemory(
        actor_id="aaa-skill-mesh-populate",
        session_id=os.getenv("ARIFOS_SESSION_ID", "system"),
    )

    # ── Discover all SKILL.md files ─────────────────────────────────
    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    # Exclude _retired
    skill_files = [f for f in skill_files if "_retired" not in str(f)]
    print(f"   Found {len(skill_files)} SKILL.md files (excluding _retired)")

    # ── Parse, classify, store via adapter ──────────────────────────
    # Collection lifecycle and embedding are kernel-owned (alignment
    # doctrine §1); each skill becomes one fm.store receipt.
    tagged_count = 0
    stored_count = 0

    for filepath in skill_files:
        skill = read_skill_md(filepath)
        name = skill["name"]
        desc = skill["description"]
        skill_id = skill["skill_id"]

        # Classify
        tier = classify_capability(name, desc)

        # Inject metadata into SKILL.md (P0.4)
        if inject_metadata(filepath, tier):
            tagged_count += 1

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

        fm.store(
            content=payload,
            tier=MEMORY_TIER,
            collection_class=COLLECTION_CLASS,
            tags=["skill-mesh", "populate", f"capability-tier:{tier}"],
            source_type="skill_index",
            source_uri=str(filepath),
        )
        stored_count += 1

        if stored_count % PROGRESS_EVERY == 0:
            print(f"   Stored {stored_count}/{len(skill_files)} skills...")

    # ── Verify via adapter stats ────────────────────────────────────
    stats = fm.stats(collection_class=COLLECTION_CLASS)
    print(f"\n✅ DONE: {stored_count} skills stored via class '{COLLECTION_CLASS}'")
    print(f"   Adapter stats: {json.dumps(stats, default=str)[:300]}")
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
        "skills_stored": stored_count,
        "skills_tagged": tagged_count,
        "capability_distribution": tiers,
    }


if __name__ == "__main__":
    result = main()
    print(f"\n📊 RESULT: {json.dumps(result)}")
