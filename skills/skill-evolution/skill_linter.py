#!/usr/bin/env python3
"""
SKILL LINTER — Validate skills against SKILL_INVARIANT_SCHEMA
=============================================================

Enforces:
- Required fields in invariant header
- Orthogonality (no overlap in same tier)
- Refusal boundary (refuses ≥ owns)
- Purpose singularity (one sentence)
- Cause class specificity (at least one)
- Dependency acyclicity

Usage:
  python3 skill_linter.py <skill_dir>
  python3 skill_linter.py /root/.agents/skills/FORGE-fastmcp
  python3 skill_linter.py --all  # lint all skills

DITEMPA BUKAN DIBERI — skills are contracts, not conversations.
"""

import yaml
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# ============================================================
# ENUMERATIONS
# ============================================================

COST_CLASSES = {"C0", "C1", "C2", "C3", "C4"}
TIERS = {
    "substrate_always",
    "constitutional",
    "forge_on_demand",
    "github_on_demand",
    "knowledge_on_demand",
    "agi_on_demand",
    "asi_sensory",
    "a2a_handoff",
}
REVERSIBILITY = {"REVERSIBLE", "GATED", "IRREVERSIBLE"}
RISK_LEVELS = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
CONVERGENCE = {"CONVERGED", "STABLE", "UNSTABLE", "DIVERGENT"}
CAUSE_CLASSES = {
    "SKILL_DEFECT",
    "MODEL_ERROR",
    "HARNESS_FAULT",
    "DATA_FAULT",
    "TASK_IMPOSSIBLE",
    "UPSTREAM_FAULT",
    "AMBIGUOUS_INTENT",
}
INSTITUTIONAL_STAGES = {"SENSE", "DECIDE", "GATE", "ACT", "ATTEST", "REVIEW"}

# ============================================================
# VALIDATION RULES
# ============================================================

HEADER_FIELDS = {
    "id": {"type": "str", "required": True, "pattern": r"^[A-Z][A-Z0-9-]+$"},
    "version": {"type": "str", "required": True, "pattern": r"^\d+\.\d+\.\d+$"},
    "purpose": {"type": "str", "required": True, "max_length": 200},
    "owns": {"type": "list", "required": True, "min_items": 1},
    "refuses": {"type": "list", "required": True, "min_items": 1},
    "cause_class": {"type": "list", "required": True, "min_items": 1},
    "cost_class": {"type": "str", "required": True, "enum": COST_CLASSES},
    "tier": {"type": "str", "required": True, "enum": TIERS},
    "permissions": {"type": "dict", "required": True},
    "dependencies": {"type": "dict", "required": True},
    "precedence": {"type": "int", "required": True, "min": 0},
    "conflicts_with": {"type": "list", "required": True},
    "contract": {"type": "dict", "required": True},
    "reversibility": {"type": "str", "required": True, "enum": REVERSIBILITY},
    "owner": {"type": "str", "required": True},
    "owner_organ": {"type": "str", "required": True},
    "accountability": {"type": "str", "required": True},
}


@dataclass
class LintResult:
    """Result of linting a skill."""

    skill_id: str
    skill_path: str
    passed: bool
    errors: List[str]
    warnings: List[str]


class SkillLinter:
    """
    Validate skills against SKILL_INVARIANT_SCHEMA.

    Enforces:
    - Required fields in invariant header
    - Orthogonality (no overlap in same tier)
    - Refusal boundary (refuses ≥ owns)
    - Purpose singularity (one sentence)
    - Cause class specificity (at least one)
    - Dependency acyclicity
    """

    def __init__(self, skills_root: str = "/root/.agents/skills"):
        self.skills_root = Path(skills_root)
        self.all_skills: List[Dict] = []

    def _load_skill_metadata(self, skill_dir: Path) -> Optional[Dict]:
        """Load skill metadata from SKILL.md frontmatter."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return None

        content = skill_md.read_text()

        # Extract YAML frontmatter
        if not content.startswith("---"):
            return None

        try:
            _, frontmatter, _ = content.split("---", 2)
            return yaml.safe_load(frontmatter)
        except (ValueError, yaml.YAMLError):
            return None

    def _check_required_fields(self, metadata: Dict) -> List[str]:
        """Check that all required header fields are present."""
        errors = []

        for field, rules in HEADER_FIELDS.items():
            if rules.get("required") and field not in metadata:
                errors.append(f"Missing required field: {field}")

        return errors

    def _check_field_types(self, metadata: Dict) -> List[str]:
        """Check that field types are correct."""
        errors = []

        for field, rules in HEADER_FIELDS.items():
            if field not in metadata:
                continue

            value = metadata[field]
            expected_type = rules.get("type")

            if expected_type == "str" and not isinstance(value, str):
                errors.append(f"Field '{field}' must be string, got {type(value).__name__}")
            elif expected_type == "list" and not isinstance(value, list):
                errors.append(f"Field '{field}' must be list, got {type(value).__name__}")
            elif expected_type == "dict" and not isinstance(value, dict):
                errors.append(f"Field '{field}' must be dict, got {type(value).__name__}")
            elif expected_type == "int" and not isinstance(value, int):
                errors.append(f"Field '{field}' must be int, got {type(value).__name__}")

        return errors

    def _check_enums(self, metadata: Dict) -> List[str]:
        """Check that enum fields have valid values."""
        errors = []

        for field, rules in HEADER_FIELDS.items():
            if field not in metadata:
                continue

            value = metadata[field]
            enum_values = rules.get("enum")

            if enum_values and value not in enum_values:
                errors.append(f"Field '{field}' has invalid value '{value}'. Must be one of: {enum_values}")

        return errors

    def _check_patterns(self, metadata: Dict) -> List[str]:
        """Check that pattern fields match their regex."""
        import re

        errors = []

        for field, rules in HEADER_FIELDS.items():
            if field not in metadata:
                continue

            value = metadata[field]
            pattern = rules.get("pattern")

            if pattern and isinstance(value, str) and not re.match(pattern, value):
                errors.append(f"Field '{field}' value '{value}' does not match pattern '{pattern}'")

        return errors

    def _check_list_constraints(self, metadata: Dict) -> List[str]:
        """Check list constraints (min_items)."""
        errors = []

        for field, rules in HEADER_FIELDS.items():
            if field not in metadata:
                continue

            value = metadata[field]
            min_items = rules.get("min_items")

            if min_items and isinstance(value, list) and len(value) < min_items:
                errors.append(f"Field '{field}' must have at least {min_items} items, got {len(value)}")

        return errors

    def _check_invariants(self, metadata: Dict) -> Tuple[List[str], List[str]]:
        """Check invariant rules."""
        errors = []
        warnings = []

        # Purpose singularity
        purpose = metadata.get("purpose", "")
        if purpose.count(".") > 1:
            errors.append("Purpose has multiple sentences — split into two skills")

        # Refusal boundary
        owns = metadata.get("owns", [])
        refuses = metadata.get("refuses", [])
        if len(refuses) < len(owns):
            warnings.append("Skill refuses fewer things than it owns — insufficient boundary")

        # Cause class specificity
        cause_class = metadata.get("cause_class", [])
        if len(cause_class) < 1:
            errors.append("Skill has no cause_class — cannot own any failures")

        # Contract completeness
        contract = metadata.get("contract", {})
        if not contract.get("inputs"):
            errors.append("Contract has no inputs defined")
        if not contract.get("outputs"):
            errors.append("Contract has no outputs defined")

        # Permissions completeness
        permissions = metadata.get("permissions", {})
        if not permissions.get("agents"):
            warnings.append("Permissions has no agents defined — defaults to '*'")
        if not permissions.get("stages"):
            warnings.append("Permissions has no stages defined — may fire in any stage")

        return errors, warnings

    def _check_orthogonality(self, metadata: Dict) -> List[str]:
        """Check that skill doesn't overlap with others in same tier."""
        errors = []

        skill_id = metadata.get("id")
        skill_tier = metadata.get("tier")
        skill_owns = set(metadata.get("owns", []))

        for other in self.all_skills:
            other_id = other.get("id")
            other_tier = other.get("tier")
            other_owns = set(other.get("owns", []))

            if other_id == skill_id:
                continue

            if other_tier == skill_tier:
                overlap = skill_owns & other_owns
                if overlap:
                    errors.append(f"Orthogonality violation: overlaps with {other_id} on {overlap}")

        return errors

    def _check_dependency_cycles(self, metadata: Dict) -> List[str]:
        """Check that dependencies don't form cycles."""
        errors = []

        skill_id = metadata.get("id")
        dependencies = metadata.get("dependencies", {}).get("skills", [])

        if skill_id in dependencies:
            errors.append(f"Self-referencing dependency: {skill_id}")

        # TODO: Full cycle detection across all skills

        return errors

    def lint_skill(self, skill_dir: Path) -> LintResult:
        """Lint a single skill directory."""
        skill_path = str(skill_dir)
        skill_name = skill_dir.name

        # Load metadata
        metadata = self._load_skill_metadata(skill_dir)
        if not metadata:
            return LintResult(
                skill_id=skill_name,
                skill_path=skill_path,
                passed=False,
                errors=["Cannot load SKILL.md or no YAML frontmatter"],
                warnings=[],
            )

        # Run all checks
        errors = []
        warnings = []

        errors.extend(self._check_required_fields(metadata))
        errors.extend(self._check_field_types(metadata))
        errors.extend(self._check_enums(metadata))
        errors.extend(self._check_patterns(metadata))
        errors.extend(self._check_list_constraints(metadata))

        inv_errors, inv_warnings = self._check_invariants(metadata)
        errors.extend(inv_errors)
        warnings.extend(inv_warnings)

        errors.extend(self._check_orthogonality(metadata))
        errors.extend(self._check_dependency_cycles(metadata))

        return LintResult(
            skill_id=metadata.get("id", skill_name),
            skill_path=skill_path,
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def lint_all(self) -> List[LintResult]:
        """Lint all skills in the skills root."""
        results = []

        # First pass: load all metadata
        for skill_dir in self.skills_root.iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("."):
                continue

            metadata = self._load_skill_metadata(skill_dir)
            if metadata:
                self.all_skills.append(metadata)

        # Second pass: lint each skill
        for skill_dir in self.skills_root.iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("."):
                continue

            result = self.lint_skill(skill_dir)
            results.append(result)

        return results


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 skill_linter.py <skill_dir>")
        print("       python3 skill_linter.py --all")
        sys.exit(1)

    linter = SkillLinter()

    if sys.argv[1] == "--all":
        results = linter.lint_all()

        passed = sum(1 for r in results if r.passed)
        failed = sum(1 for r in results if not r.passed)

        print(f"=== SKILL LINT RESULTS ===")
        print(f"Total: {len(results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print()

        for result in results:
            status = "✅" if result.passed else "❌"
            print(f"{status} {result.skill_id}")
            for error in result.errors:
                print(f"    ERROR: {error}")
            for warning in result.warnings:
                print(f"    WARN: {warning}")

        sys.exit(0 if failed == 0 else 1)

    else:
        skill_dir = Path(sys.argv[1])
        if not skill_dir.exists():
            print(f"Error: {skill_dir} does not exist")
            sys.exit(1)

        result = linter.lint_skill(skill_dir)

        if result.passed:
            print(f"✅ {result.skill_id} — PASSED")
        else:
            print(f"❌ {result.skill_id} — FAILED")
            for error in result.errors:
                print(f"  ERROR: {error}")
            for warning in result.warnings:
                print(f"  WARN: {warning}")

        sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
