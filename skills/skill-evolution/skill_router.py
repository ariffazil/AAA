#!/usr/bin/env python3
"""
SKILL ROUTER — Trust-aware skill selection
==========================================

Filters by trust_status before selecting.
Returns top 3 candidates with confidence + tier + cost_class.
Returns dependency closure when requested.

Usage:
  from skill_router import SkillRouter

  router = SkillRouter()

  # Route intent to skills (CANONICAL only by default)
  results = router.route("docker incident")

  # Route with EXPERIMENTAL included
  results = router.route("docker incident", include_experimental=True)

  # Get dependency closure
  closure = router.get_dependency_closure("FORGE-incident-triage")

DITEMPA BUKAN DIBERI — trust is the schema that selection queries.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

# ============================================================
# PRECEDENCE RULE
# ============================================================

# Institutional stage precedence (lower = earlier in flow)
STAGE_PRECEDENCE = {"SENSE": 0, "DECIDE": 1, "GATE": 2, "ACT": 3, "ATTEST": 4, "REVIEW": 5}

# Governance verdict precedence (higher = stricter)
VERDICT_PRECEDENCE = {
    "VOID": 4,  # highest — blocks everything
    "HOLD": 3,  # high — blocks action
    "SABAR": 2,  # medium — caution
    "SEAL": 1,  # low — approved
    "PASS": 0,  # lowest — no opinion
}

# Cost class precedence (higher = more expensive)
COST_PRECEDENCE = {
    "C0": 0,  # substrate (free)
    "C1": 1,  # low
    "C2": 2,  # medium
    "C3": 3,  # high
    "C4": 4,  # sovereign
}


@dataclass
class SkillCandidate:
    """A skill candidate returned by the router."""

    name: str
    trust_status: str
    tier: str
    cost_class: str
    purpose: str
    confidence: float
    stage: str
    precedence: int
    dependencies: List[str]
    conflicts_with: List[str]


class SkillRouter:
    """
    Trust-aware skill selection.

    Filters by trust_status before selecting.
    Returns top 3 candidates with confidence + tier + cost_class.
    Returns dependency closure when requested.
    """

    def __init__(
        self,
        skills_root: str = "/root/.agents/skills",
        trust_status_path: str = "/root/AAA/skills/SKILL_TRUST_STATUS.json",
        canonical_profile_path: str = "/root/AAA/skills/CANONICAL_SKILL_PROFILE.json",
    ):
        self.skills_root = Path(skills_root)
        self.trust_status_path = Path(trust_status_path)
        self.canonical_profile_path = Path(canonical_profile_path)

        # Load trust status
        self.trust_status = self._load_trust_status()

        # Load canonical profile (for tier info)
        self.canonical_tiers = self._load_canonical_tiers()

        # Load skill metadata
        self.skills = self._load_all_skills()

    def _load_trust_status(self) -> Dict[str, str]:
        """Load trust status from JSON."""
        if not self.trust_status_path.exists():
            return {}

        with open(self.trust_status_path) as f:
            data = json.load(f)

        return {s["name"]: s["trust_status"] for s in data.get("skills", [])}

    def _load_canonical_tiers(self) -> Dict[str, str]:
        """Load canonical tier assignments."""
        if not self.canonical_profile_path.exists():
            return {}

        with open(self.canonical_profile_path) as f:
            profile = json.load(f)

        tiers = {}
        for tier, data in profile.get("tiers", {}).items():
            skills = data if isinstance(data, list) else data.get("skills", [])
            for s in skills:
                tiers[s] = tier

        return tiers

    def _load_skill_metadata(self, skill_dir: Path) -> Optional[Dict]:
        """Load skill metadata from SKILL.md frontmatter."""
        import yaml

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return None

        content = skill_md.read_text()
        if not content.startswith("---"):
            return None

        try:
            _, frontmatter, _ = content.split("---", 2)
            return yaml.safe_load(frontmatter)
        except:
            return None

    def _load_all_skills(self) -> List[Dict]:
        """Load all skills with metadata."""
        skills = []

        for skill_dir in self.skills_root.iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("."):
                continue

            metadata = self._load_skill_metadata(skill_dir)
            if not metadata:
                continue

            skill_name = skill_dir.name
            trust = self.trust_status.get(skill_name, "UNKNOWN")
            tier = self.canonical_tiers.get(skill_name, metadata.get("tier", "unknown"))

            skills.append(
                {
                    "name": skill_name,
                    "id": metadata.get("id", skill_name),
                    "trust_status": trust,
                    "tier": tier,
                    "cost_class": metadata.get("cost_class", "C1"),
                    "purpose": metadata.get("purpose", metadata.get("description", "")),
                    "description": metadata.get("description", ""),
                    "tags": metadata.get("tags", []),
                    "trigger_phrases": metadata.get("trigger_phrases", []),
                    "dependencies": metadata.get("dependencies", {}).get("skills", []),
                    "conflicts_with": metadata.get("conflicts_with", []),
                    "permissions": metadata.get("permissions", {}),
                    "precedence": metadata.get("precedence", 0),
                }
            )

        return skills

    def _compute_confidence(self, skill: Dict, intent: str) -> float:
        """
        Compute confidence score for a skill against an intent.

        Uses keyword matching on purpose + description + tags + trigger phrases.
        """
        intent_lower = intent.lower()
        intent_words = set(re.findall(r"\w+", intent_lower))

        # Check purpose
        purpose_lower = skill.get("purpose", "").lower()
        purpose_words = set(re.findall(r"\w+", purpose_lower))
        purpose_overlap = len(intent_words & purpose_words)

        # Check description
        desc_lower = skill.get("description", "").lower()
        desc_words = set(re.findall(r"\w+", desc_lower))
        desc_overlap = len(intent_words & desc_words)

        # Check tags
        tags = skill.get("tags", [])
        tag_overlap = 0
        for tag in tags:
            if tag.lower() in intent_lower:
                tag_overlap += 1

        # Check trigger phrases
        trigger_overlap = 0
        for phrase in skill.get("trigger_phrases", []):
            phrase_lower = phrase.lower()
            if phrase_lower in intent_lower:
                trigger_overlap += 1

        # Check name
        name_lower = skill.get("name", "").lower()
        name_words = set(re.findall(r"\w+", name_lower))
        name_overlap = len(intent_words & name_words)

        # Compute confidence
        purpose_score = min(purpose_overlap / max(len(intent_words), 1), 1.0)
        desc_score = min(desc_overlap / max(len(intent_words), 1), 1.0)
        tag_score = min(tag_overlap / max(len(tags), 1), 1.0) if tags else 0.0
        trigger_score = min(trigger_overlap / max(len(skill.get("trigger_phrases", [])), 1), 1.0)
        name_score = min(name_overlap / max(len(intent_words), 1), 1.0)

        # Weight: name 30%, description 25%, purpose 20%, tags 15%, triggers 10%
        confidence = (
            name_score * 0.30 + desc_score * 0.25 + purpose_score * 0.20 + tag_score * 0.15 + trigger_score * 0.10
        )

        # Boost CANONICAL skills
        if skill.get("trust_status") == "CANONICAL":
            confidence *= 1.1

        return min(confidence, 1.0)

    def _check_conflict(self, skill: Dict, loaded_skills: List[str]) -> List[str]:
        """Check if skill conflicts with any loaded skills."""
        conflicts = []

        for loaded in loaded_skills:
            if loaded in skill.get("conflicts_with", []):
                conflicts.append(loaded)

        return conflicts

    def _resolve_conflict(self, skill_a: Dict, skill_b: Dict) -> str:
        """
        Resolve conflict between two skills using precedence rule.

        HARD RULE: When two loaded skills conflict, the skill with the
        STRICTER governance verdict wins. 888_HOLD always beats "restart
        immediately." A skill can NEVER override another skill's HOLD.
        """
        # Compare by precedence field
        prec_a = skill_a.get("precedence", 0)
        prec_b = skill_b.get("precedence", 0)

        if prec_a > prec_b:
            return skill_a["name"]
        elif prec_b > prec_a:
            return skill_b["name"]

        # If equal precedence, stricter cost class wins
        cost_a = COST_PRECEDENCE.get(skill_a.get("cost_class", "C1"), 1)
        cost_b = COST_PRECEDENCE.get(skill_b.get("cost_class", "C1"), 1)

        if cost_a > cost_b:
            return skill_a["name"]
        elif cost_b > cost_a:
            return skill_b["name"]

        # If still equal, CANONICAL wins
        if skill_a.get("trust_status") == "CANONICAL":
            return skill_a["name"]
        if skill_b.get("trust_status") == "CANONICAL":
            return skill_b["name"]

        # Truly equal — first loaded wins
        return skill_a["name"]

    def route(
        self, intent: str, include_experimental: bool = False, top_k: int = 3, loaded_skills: Optional[List[str]] = None
    ) -> List[SkillCandidate]:
        """
        Route intent to skill candidates.

        Filters by trust_status before selecting.
        Returns top 3 candidates with confidence + tier + cost_class.
        """
        if loaded_skills is None:
            loaded_skills = []

        candidates = []

        for skill in self.skills:
            # Filter by trust_status
            if not include_experimental and skill["trust_status"] != "CANONICAL":
                continue

            # Skip QUARANTINED
            if skill["trust_status"] == "QUARANTINED":
                continue

            # Compute confidence
            confidence = self._compute_confidence(skill, intent)

            if confidence < 0.1:
                continue

            # Check conflicts
            conflicts = self._check_conflict(skill, loaded_skills)

            # Get stage
            permissions = skill.get("permissions", {})
            stages = permissions.get("stages", ["ACT"])
            stage = stages[0] if stages else "ACT"

            candidates.append(
                SkillCandidate(
                    name=skill["name"],
                    trust_status=skill["trust_status"],
                    tier=skill["tier"],
                    cost_class=skill["cost_class"],
                    purpose=skill["purpose"][:100],
                    confidence=round(confidence, 3),
                    stage=stage,
                    precedence=skill.get("precedence", 0),
                    dependencies=skill.get("dependencies", []),
                    conflicts_with=conflicts,
                )
            )

        # Sort by confidence (descending)
        candidates.sort(key=lambda c: c.confidence, reverse=True)

        # Return top_k
        return candidates[:top_k]

    def get_dependency_closure(self, skill_name: str) -> Dict[str, Any]:
        """
        Get dependency closure for a skill.

        Returns the skill + all its dependencies in load order.
        """
        skill = next((s for s in self.skills if s["name"] == skill_name), None)
        if not skill:
            return {"error": f"Skill {skill_name} not found"}

        closure = []
        visited = set()

        def _collect_deps(name: str):
            if name in visited:
                return
            visited.add(name)

            s = next((sk for sk in self.skills if sk["name"] == name), None)
            if not s:
                return

            # Collect dependencies first (depth-first)
            for dep in s.get("dependencies", []):
                _collect_deps(dep)

            closure.append(
                {
                    "name": s["name"],
                    "trust_status": s["trust_status"],
                    "tier": s["tier"],
                    "cost_class": s["cost_class"],
                }
            )

        _collect_deps(skill_name)

        return {
            "skill": skill_name,
            "closure": closure,
            "load_order": [c["name"] for c in closure],
            "total_dependencies": len(closure) - 1,
        }

    def get_precedence_verdict(self, skill_a: str, skill_b: str, context: str = "") -> Dict[str, Any]:
        """
        Get precedence verdict when two skills conflict.

        HARD RULE: 888_HOLD always beats "restart immediately."
        A skill can NEVER override another skill's HOLD.
        """
        a = next((s for s in self.skills if s["name"] == skill_a), None)
        b = next((s for s in self.skills if s["name"] == skill_b), None)

        if not a or not b:
            return {"error": "One or both skills not found"}

        winner = self._resolve_conflict(a, b)

        return {
            "skill_a": skill_a,
            "skill_b": skill_b,
            "winner": winner,
            "reason": f"Precedence rule: {winner} wins by governance strictness",
            "context": context,
        }


# ============================================================
# CLI INTERFACE
# ============================================================

if __name__ == "__main__":
    import sys

    router = SkillRouter()

    if len(sys.argv) < 2:
        print("Usage: python3 skill_router.py <command> [args]")
        print("Commands:")
        print("  route <intent> [--experimental] [--top N]")
        print("  closure <skill_name>")
        print("  precedence <skill_a> <skill_b>")
        print("  status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "route":
        if len(sys.argv) < 3:
            print("Usage: route <intent> [--experimental] [--top N]")
            sys.exit(1)

        intent = sys.argv[2]
        include_exp = "--experimental" in sys.argv
        top_k = 3

        for i, arg in enumerate(sys.argv):
            if arg == "--top" and i + 1 < len(sys.argv):
                top_k = int(sys.argv[i + 1])

        results = router.route(intent, include_experimental=include_exp, top_k=top_k)

        print(f"=== SKILL ROUTE: '{intent}' ===")
        print(f"Filters: {'CANONICAL + EXPERIMENTAL' if include_exp else 'CANONICAL only'}")
        print(f"Top {top_k} candidates:")
        print()

        for i, r in enumerate(results, 1):
            print(f"  {i}. {r.name}")
            print(f"     Trust: {r.trust_status} | Tier: {r.tier} | Cost: {r.cost_class}")
            print(f"     Confidence: {r.confidence} | Stage: {r.stage}")
            print(f"     Purpose: {r.purpose}")
            if r.dependencies:
                print(f"     Dependencies: {r.dependencies}")
            if r.conflicts_with:
                print(f"     ⚠️  Conflicts: {r.conflicts_with}")
            print()

    elif command == "closure":
        if len(sys.argv) < 3:
            print("Usage: closure <skill_name>")
            sys.exit(1)

        result = router.get_dependency_closure(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif command == "precedence":
        if len(sys.argv) < 4:
            print("Usage: precedence <skill_a> <skill_b>")
            sys.exit(1)

        result = router.get_precedence_verdict(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))

    elif command == "status":
        canonical = sum(1 for s in router.skills if s["trust_status"] == "CANONICAL")
        experimental = sum(1 for s in router.skills if s["trust_status"] == "EXPERIMENTAL")
        quarantined = sum(1 for s in router.skills if s["trust_status"] == "QUARANTINED")

        print(f"=== SKILL ROUTER STATUS ===")
        print(f"Total skills: {len(router.skills)}")
        print(f"  CANONICAL:    {canonical}")
        print(f"  EXPERIMENTAL: {experimental}")
        print(f"  QUARANTINED:  {quarantined}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
