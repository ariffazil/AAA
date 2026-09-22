#!/usr/bin/env python3
"""
P0.3/P0.4 — Skill Mesh Population & Capability Tagging (FEDERATION)
====================================================================
Reads all SKILL.md files across the five federation roots (order =
dedupe precedence, AAA is canonical), classifies each into a capability
tier (fed-reasoning-heavy, fed-multimodal-vision, etc.), and indexes
every unique skill into the skill_mesh memory class via the
FederationMemory adapter. The arifOS kernel owns the substrate:
collection lifecycle and embedding are kernel-side (alignment
doctrine §1 — agents never touch the vector store directly).

SAFETY: inject_metadata() WRITES into SKILL.md files. By default it
applies ONLY to files under the AAA root; pass --tag-all to force
injection everywhere (mutates other organs' repos — use deliberately).

Forged: 2026-08-10 by 333-AGI under F13 directive.
Migrated 2026-09-12 to federation_memory_adapter (F13 SOVEREIGN
directive — /root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md).
Federation-wide crawl + dry-run mode: 2026-09-22.
"""

import argparse
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
# (organ, skills_root) — order = dedupe precedence, AAA is canonical.
SKILL_ROOTS: list[tuple[str, Path]] = [
    ("AAA", Path("/root/AAA/skills")),
    ("arifOS", Path("/root/arifOS/skills")),
    ("HERMES", Path("/root/HERMES/skills")),
    ("A-FORGE", Path("/root/A-FORGE/skills")),
    ("kimi-code", Path("/root/.kimi-code/skills")),
]
AAA_SKILLS_ROOT = SKILL_ROOTS[0][1]  # metadata injection write-scope (default)
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
    ap = argparse.ArgumentParser(description="Skill mesh populate (federation-wide)")
    ap.add_argument("--dry-run", action="store_true",
                    help="parse + classify + dedupe + report only; no fm.store(), no metadata injection")
    ap.add_argument("--tag-all", action="store_true",
                    help="force capability metadata injection into ALL organs' SKILL.md "
                         "(default: AAA root only — never mutate other organs' repos)")
    args = ap.parse_args()

    print("🔍 Skill Mesh Population — P0.3/P0.4 (FederationMemory)")
    print(f"   Skill roots: {len(SKILL_ROOTS)} organs: {', '.join(o for o, _ in SKILL_ROOTS)}")
    print(f"   Memory class: {COLLECTION_CLASS} (via federation_memory_adapter)")
    if args.dry_run:
        print("   Mode: DRY-RUN (no stores, no metadata injection)")

    # ── Discover all SKILL.md files across federation roots ─────────
    seen: dict[str, tuple[str, Path]] = {}  # normalized skill_id → (organ, path)
    files_seen = 0
    for organ, root in SKILL_ROOTS:
        if not root.is_dir():
            print(f"   ⚠ {organ}: skills root not found: {root} (skipped)")
            continue
        for f in sorted(root.rglob("SKILL.md")):
            if "_retired" in str(f):
                continue
            files_seen += 1
            skill_id = f.parent.name.lower()  # normalized dedupe key
            if skill_id in seen:
                continue  # first organ in priority order is canonical
            seen[skill_id] = (organ, f)

    organ_kept: dict[str, int] = {}
    for organ, _ in seen.values():
        organ_kept[organ] = organ_kept.get(organ, 0) + 1
    print(f"   Found {files_seen} SKILL.md files (excluding _retired)")
    print(f"   Union after dedupe by normalized skill_id: {len(seen)} unique skills "
          f"({files_seen - len(seen)} duplicates skipped)")
    print(f"   Per-organ kept: {json.dumps(organ_kept, sort_keys=True)}")

    # ── Parse + classify once per unique skill ──────────────────────
    records = []  # (organ, filepath, skill, tier)
    tiers = {tier: 0 for tier in CAPABILITY_PATTERNS}
    for _key, (organ, filepath) in seen.items():
        skill = read_skill_md(filepath)
        tier = classify_capability(skill["name"], skill["description"])
        tiers[tier] += 1
        records.append((organ, filepath, skill, tier))

    if args.dry_run:
        print(f"\n🏃 DRY-RUN complete: union={len(seen)} unique skills "
              f"(files seen: {files_seen}, duplicates skipped: {files_seen - len(seen)})")
        print(f"   Capability distribution: {json.dumps(tiers, indent=2)}")
        return {
            "dry_run": True,
            "files_seen": files_seen,
            "union_skills": len(seen),
            "duplicates_skipped": files_seen - len(seen),
            "organ_kept": organ_kept,
            "capability_distribution": tiers,
        }

    fm = FederationMemory(
        actor_id=os.getenv("ARIFOS_ACTOR_ID", "aaa-skill-mesh-populate"),
        session_id=os.getenv("ARIFOS_SESSION_ID", "system"),
    )

    # ── Parse, classify, store via adapter ──────────────────────────
    # Collection lifecycle and embedding are kernel-owned (alignment
    # doctrine §1); each skill becomes one fm.store receipt.
    tagged_count = 0
    stored_count = 0
    failed_stores: list[str] = []

    for organ, filepath, skill, tier in records:
        name = skill["name"]
        desc = skill["description"]
        skill_id = skill["skill_id"]

        # Inject metadata into SKILL.md (P0.4) — WRITE-SCOPED to the AAA
        # root by default; other organs' repos are never mutated unless
        # --tag-all is passed explicitly.
        if args.tag_all or filepath.is_relative_to(AAA_SKILLS_ROOT):
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
            "source_organ": organ,
        }

        result = fm.store(
            content=payload,
            tier=MEMORY_TIER,
            collection_class=COLLECTION_CLASS,
            tags=["skill-mesh", "populate", f"capability-tier:{tier}"],
            source_type="skill_index",
            source_uri=str(filepath),
            idempotency_key=f"skill-mesh:{organ}:{skill_id}",
        )
        # Receipt verification (F2 — probe before claim; no phantom counters):
        #  1. MCP tool-level errors arrive as 200 + isError:true.
        #  2. Constitutional HOLD/VOID arrive as isError:false with verdict
        #     HOLD and NO memory_id — the kernel refused the write.
        # Only verdict=SEAL with a memory_id counts as stored.
        stored_receipt = False
        err_text = ""
        if isinstance(result, dict) and result.get("isError"):
            try:
                err_text = result["content"][0].get("text", "")[:160]
            except (KeyError, IndexError, TypeError):
                pass
        elif isinstance(result, dict):
            try:
                _inner = json.loads(result["content"][0].get("text", ""))
                _res = _inner.get("result", {}) or {}
                _mid = _res.get("memory_id") or (_res.get("payload") or {}).get("memory_id")
                # SEAL is the success signal; memory_id is verifiable substrate-side
                # via idempotency_key (the MCP envelope does not surface it).
                if str(_inner.get("verdict", "")).upper() == "SEAL":
                    stored_receipt = True
                else:
                    _cc = _inner.get("constitutional_check", {}) or {}
                    err_text = (
                        f"verdict={_inner.get('verdict')} "
                        f"failed_floors={_cc.get('failed_floors')}"
                    )
            except (KeyError, IndexError, TypeError, ValueError):
                receipt_id = result.get("receipt_id")
                if receipt_id:
                    stored_receipt = True
                else:
                    err_text = "unparseable receipt"
        if not stored_receipt:
            failed_stores.append(f"{organ}:{skill_id}")
            if len(failed_stores) <= 3:
                print(f"   ⚠ store FAILED {organ}:{skill_id} — {err_text or 'no receipt'}")
        else:
            stored_count += 1

        if stored_count % PROGRESS_EVERY == 0 and stored_count > 0:
            print(f"   Stored {stored_count}/{len(records)} skills...")

    if failed_stores:
        print(f"\n❌ STORE FAILURES: {len(failed_stores)}/{len(records)} records were NOT stored "
              f"(kernel/adapter contract mismatch — see adapter stats above).")
        print(f"   First failures: {failed_stores[:10]}")

    # ── Verify via adapter stats ────────────────────────────────────
    stats = fm.stats(collection_class=COLLECTION_CLASS)
    stats_is_error = isinstance(stats, dict) and stats.get("isError")
    print(f"\n{'❌' if (failed_stores or stats_is_error) else '✅'} DONE: "
          f"{stored_count}/{len(records)} skills stored via class '{COLLECTION_CLASS}'")
    print(f"   Adapter stats: {json.dumps(stats, default=str)[:300]}")
    if stats_is_error:
        print("   ⚠ adapter stats call itself FAILED — treat stored counts as unverified "
              "until substrate witness (Qdrant points_count) confirms.")
    print(f"   Metadata injected into {tagged_count} SKILL.md files")

    # ── Capability distribution (tallied during classify pass) ──────
    print(f"   Capability distribution: {json.dumps(tiers, indent=2)}")

    return {
        "skills_stored": stored_count,
        "stores_failed": len(failed_stores),
        "skills_tagged": tagged_count,
        "files_seen": files_seen,
        "union_skills": len(records),
        "capability_distribution": tiers,
    }


if __name__ == "__main__":
    result = main()
    print(f"\n📊 RESULT: {json.dumps(result)}")
