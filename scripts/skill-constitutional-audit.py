#!/usr/bin/env python3
"""Skill Constitutional Audit — AAA Skill Constitution v1.0 Enforcer.

Scans all SKILL.md files against the Skill Constitution (SKILL_CONSTITUTION.md)
and produces a compliance report with per-skill verdicts: PASS / HOLD / VOID.

Constitutional checks:
  1. Identity (Blindspot #1) — floor_scope, risk_tier, autonomy_tier, owner
  2. Consequences (Blindspot #2) — receipt declarations, sealing requirements
  3. Federation (Blindspot #4) — MCP server deps, skill deps matching body

Read-only. Never modifies skills. Outputs report only.

Usage:
  python3 skill-constitutional-audit.py                    # full audit, markdown
  python3 skill-constitutional-audit.py --format json      # JSON output
  python3 skill-constitutional-audit.py --skills geox-*    # filter by name
  python3 skill-constitutional-audit.py --fail-on hold     # exit 1 on HOLD+
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


SKILLS_DIR = Path("/root/.agents/skills")
VALID_FLOORS = {f"F{i}" for i in range(1, 14)}
VALID_RISK_TIERS = {"high", "medium", "low"}
VALID_AUTONOMY_TIERS = {"T1", "T2", "T3"}

# Floor requirements by risk tier
MIN_FLOORS = {"low": 2, "medium": 4, "high": 6}

# Receipt infrastructure skills
RECEIPT_SKILLS = {"claim-receipt-v1", "truth-receipt-enforcer"}
SEAL_SKILLS = {"999-vault-seal-immutable"}
GATE_SKILLS = {"claim-verification-gate"}


@dataclass
class Verdict:
    skill: str
    verdict: str  # PASS, HOLD, VOID
    checks: list[dict[str, str]] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for c in self.checks if c["status"] == "PASS")

    @property
    def held(self) -> int:
        return sum(1 for c in self.checks if c["status"] == "HOLD")

    @property
    def voided(self) -> int:
        return sum(1 for c in self.checks if c["status"] == "VOID")


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse YAML frontmatter from SKILL.md."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1].strip()
    if not fm_text:
        return {}
    if HAS_YAML:
        try:
            return yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            return {"_parse_error": True}
    # Minimal fallback
    result: dict[str, Any] = {}
    for line in fm_text.splitlines():
        if ":" in line and not line.strip().startswith("-"):
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def extract_body(text: str) -> str:
    """Return markdown body after frontmatter."""
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    return parts[2]


def extract_mcp_refs(body: str) -> set[str]:
    """Extract MCP server names referenced in body via mcp__<server>__* patterns."""
    return set(re.findall(r"mcp__([a-zA-Z0-9_-]+)__", body))


def extract_skill_refs(body: str) -> set[str]:
    """Extract skill names referenced in body."""
    refs = set()
    # Match common patterns: skill name in headers, lists, or prose
    for skill in RECEIPT_SKILLS | SEAL_SKILLS | GATE_SKILLS:
        if skill in body:
            refs.add(skill)
    return refs


def check_identity(skill_name: str, fm: dict[str, Any]) -> list[dict[str, str]]:
    """Blindspot #1: Check mandatory identity fields."""
    checks = []

    # id
    if "id" not in fm:
        checks.append({"field": "id", "status": "VOID", "msg": "Missing 'id' field"})
    elif fm["id"] != skill_name:
        checks.append({"field": "id", "status": "HOLD", "msg": f"id '{fm['id']}' != dir name '{skill_name}'"})

    # name
    if "name" not in fm:
        checks.append({"field": "name", "status": "VOID", "msg": "Missing 'name' field"})

    # version
    if "version" not in fm:
        checks.append({"field": "version", "status": "VOID", "msg": "Missing 'version' field"})

    # description
    if "description" not in fm:
        checks.append({"field": "description", "status": "VOID", "msg": "Missing 'description' field"})

    # owner
    if "owner" not in fm:
        checks.append({"field": "owner", "status": "VOID", "msg": "Missing 'owner' field"})

    # risk_tier
    risk = fm.get("risk_tier", "")
    if not risk:
        checks.append({"field": "risk_tier", "status": "VOID", "msg": "Missing 'risk_tier' field"})
    elif risk not in VALID_RISK_TIERS:
        checks.append({"field": "risk_tier", "status": "VOID", "msg": f"Invalid risk_tier '{risk}' — must be high/medium/low"})

    # floor_scope
    floors = fm.get("floor_scope", [])
    if not floors:
        checks.append({"field": "floor_scope", "status": "VOID", "msg": "Missing 'floor_scope' — skill is constitutionally blind"})
    else:
        if isinstance(floors, str):
            floors = [f.strip() for f in floors.strip("[]").split(",")]
        invalid = set(floors) - VALID_FLOORS
        if invalid:
            checks.append({"field": "floor_scope", "status": "VOID", "msg": f"Invalid floors: {invalid}"})
        # Risk-tier floor count check
        if risk in MIN_FLOORS and len(floors) < MIN_FLOORS[risk]:
            checks.append({
                "field": "floor_scope",
                "status": "HOLD",
                "msg": f"risk_tier={risk} requires ≥{MIN_FLOORS[risk]} floors, has {len(floors)}"
            })
        # T3 must have F1+F13
        autonomy = fm.get("autonomy_tier", "")
        if autonomy == "T3":
            if "F1" not in floors:
                checks.append({"field": "floor_scope", "status": "VOID", "msg": "T3 autonomy requires F1 (AMANAH)"})
            if "F13" not in floors:
                checks.append({"field": "floor_scope", "status": "VOID", "msg": "T3 autonomy requires F13 (SOVEREIGN)"})

    # autonomy_tier
    autonomy = fm.get("autonomy_tier", "")
    if not autonomy:
        checks.append({"field": "autonomy_tier", "status": "VOID", "msg": "Missing 'autonomy_tier' field"})
    elif autonomy not in VALID_AUTONOMY_TIERS:
        checks.append({"field": "autonomy_tier", "status": "VOID", "msg": f"Invalid autonomy_tier '{autonomy}' — must be T1/T2/T3"})

    return checks


def check_consequences(skill_name: str, fm: dict[str, Any], body: str) -> list[dict[str, str]]:
    """Blindspot #2: Check consequence declarations."""
    checks = []
    risk = fm.get("risk_tier", "")
    autonomy = fm.get("autonomy_tier", "")
    declared_skills = set()
    deps = fm.get("dependencies", {})
    if isinstance(deps, dict):
        declared_skills = set(deps.get("skills", []) or [])

    body_refs = extract_skill_refs(body)

    # High-risk skills must reference receipt infrastructure
    if risk == "high":
        has_receipt = bool(declared_skills & (RECEIPT_SKILLS | GATE_SKILLS))
        if not has_receipt:
            checks.append({
                "field": "dependencies.skills",
                "status": "VOID",
                "msg": "risk_tier=high but no receipt/gate skill declared in dependencies"
            })

        # Check outputs declared
        outputs = fm.get("outputs", [])
        if not outputs:
            checks.append({
                "field": "outputs",
                "status": "HOLD",
                "msg": "risk_tier=high but no outputs declared"
            })

    # T3 must reference sealing
    if autonomy == "T3":
        has_seal = bool(declared_skills & SEAL_SKILLS)
        if not has_seal:
            checks.append({
                "field": "dependencies.skills",
                "status": "VOID",
                "msg": "autonomy_tier=T3 but no sealing skill (999-vault-seal-immutable) declared"
            })

    # Body references receipt infrastructure but doesn't declare it
    undeclared_receipts = body_refs & (RECEIPT_SKILLS | GATE_SKILLS | SEAL_SKILLS) - declared_skills
    if undeclared_receipts:
        checks.append({
            "field": "dependencies.skills",
            "status": "HOLD",
            "msg": f"Body references {undeclared_receipts} but not declared in dependencies"
        })

    return checks


def check_federation(skill_name: str, fm: dict[str, Any], body: str) -> list[dict[str, str]]:
    """Blindspot #4: Check federation dependency declarations."""
    checks = []
    deps = fm.get("dependencies", {})
    declared_mcp = set()
    if isinstance(deps, dict):
        declared_mcp = set(deps.get("mcp_servers", []) or [])

    body_mcp_refs = extract_mcp_refs(body)

    # Body references MCP servers not declared
    undeclared = body_mcp_refs - declared_mcp
    if undeclared:
        checks.append({
            "field": "dependencies.mcp_servers",
            "status": "VOID",
            "msg": f"Body uses mcp__{undeclared}__* but servers not declared in dependencies"
        })

    # Declare MCP servers but body doesn't use them (minor — could be meta-skill)
    unused = declared_mcp - body_mcp_refs
    if unused:
        checks.append({
            "field": "dependencies.mcp_servers",
            "status": "PASS",
            "msg": f"Declared but not directly referenced in body: {unused} (acceptable for meta-skills)"
        })

    return checks


def audit_skill(skill_dir: Path) -> Verdict:
    """Run all constitutional checks against a single skill."""
    skill_name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return Verdict(
            skill=skill_name,
            verdict="VOID",
            checks=[{"field": "SKILL.md", "status": "VOID", "msg": "SKILL.md not found"}]
        )

    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    fm = parse_frontmatter(text)
    body = extract_body(text)

    if "_parse_error" in fm:
        return Verdict(
            skill=skill_name,
            verdict="VOID",
            checks=[{"field": "frontmatter", "status": "VOID", "msg": "YAML parse error"}]
        )

    if not fm:
        return Verdict(
            skill=skill_name,
            verdict="VOID",
            checks=[{"field": "frontmatter", "status": "VOID", "msg": "No YAML frontmatter found"}]
        )

    all_checks = []
    all_checks.extend(check_identity(skill_name, fm))
    all_checks.extend(check_consequences(skill_name, fm, body))
    all_checks.extend(check_federation(skill_name, fm, body))

    # Determine overall verdict
    statuses = {c["status"] for c in all_checks}
    if "VOID" in statuses:
        verdict = "VOID"
    elif "HOLD" in statuses:
        verdict = "HOLD"
    else:
        verdict = "PASS"

    return Verdict(skill=skill_name, verdict=verdict, checks=all_checks)


def markdown_report(verdicts: list[Verdict]) -> str:
    """Generate markdown compliance report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total = len(verdicts)
    passed = sum(1 for v in verdicts if v.verdict == "PASS")
    held = sum(1 for v in verdicts if v.verdict == "HOLD")
    voided = sum(1 for v in verdicts if v.verdict == "VOID")

    lines = [
        "# AAA Skill Constitutional Audit",
        "",
        f"**Generated:** {now}",
        f"**Constitution:** SKILL_CONSTITUTION.md v1.0",
        f"**Skills scanned:** {total}",
        f"**✅ PASS:** {passed}",
        f"**⚠️ HOLD:** {held}",
        f"**❌ VOID:** {voided}",
        f"**Compliance rate:** {passed}/{total} ({100*passed//max(total,1)}%)",
        "",
        "## Verdict Summary",
        "",
        "| Verdict | Skill | Pass | Hold | Void |",
        "|---------|-------|------|------|------|",
    ]

    for v in sorted(verdicts, key=lambda x: ({"VOID": 0, "HOLD": 1, "PASS": 2}[x.verdict], x.skill)):
        icon = {"PASS": "✅", "HOLD": "⚠️", "VOID": "❌"}[v.verdict]
        lines.append(f"| {icon} {v.verdict} | {v.skill} | {v.passed} | {v.held} | {v.voided} |")

    # Detail section for non-PASS skills
    non_pass = [v for v in verdicts if v.verdict != "PASS"]
    if non_pass:
        lines.extend(["", "## Findings", ""])
        for v in sorted(non_pass, key=lambda x: ({"VOID": 0, "HOLD": 1}[x.verdict], x.skill)):
            icon = {"HOLD": "⚠️", "VOID": "❌"}[v.verdict]
            lines.append(f"### {icon} {v.skill} — {v.verdict}")
            lines.append("")
            for c in v.checks:
                if c["status"] != "PASS":
                    lines.append(f"- **{c['field']}** [{c['status']}] {c['msg']}")
            lines.append("")

    # Blindspot summary
    identity_voids = sum(
        1 for v in verdicts
        for c in v.checks
        if c["status"] == "VOID" and c["field"] in ("floor_scope", "risk_tier", "autonomy_tier", "owner")
    )
    consequence_voids = sum(
        1 for v in verdicts
        for c in v.checks
        if c["status"] == "VOID" and "receipt" in c["msg"].lower() or "seal" in c["msg"].lower()
    )
    federation_voids = sum(
        1 for v in verdicts
        for c in v.checks
        if c["status"] == "VOID" and c["field"] == "dependencies.mcp_servers"
    )

    lines.extend([
        "## Blindspot Analysis",
        "",
        "| Blindspot | VOID Count | Description |",
        "|-----------|-----------|-------------|",
        f"| #1 Identity | {identity_voids} | Skills without floor_scope, risk_tier, autonomy_tier, or owner |",
        f"| #2 Consequences | {consequence_voids} | Skills missing receipt/sealing declarations |",
        f"| #4 Federation | {federation_voids} | Skills with undeclared MCP server dependencies |",
        "",
    ])

    lines.append("")
    return "\n".join(lines)


def json_report(verdicts: list[Verdict]) -> str:
    """Generate JSON compliance report."""
    return json.dumps({
        "generated": datetime.now(timezone.utc).isoformat(),
        "constitution": "SKILL_CONSTITUTION.md v1.0",
        "total": len(verdicts),
        "passed": sum(1 for v in verdicts if v.verdict == "PASS"),
        "held": sum(1 for v in verdicts if v.verdict == "HOLD"),
        "voided": sum(1 for v in verdicts if v.verdict == "VOID"),
        "verdicts": [
            {
                "skill": v.skill,
                "verdict": v.verdict,
                "checks": v.checks,
            }
            for v in verdicts
        ],
    }, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AAA Skill Constitutional Audit")
    parser.add_argument("--skills-dir", type=Path, default=SKILLS_DIR, help="Skills directory")
    parser.add_argument("--skills", type=str, default="", help="Comma-separated skill name filter (glob)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path, default=None, help="Write report to file")
    parser.add_argument("--fail-on", choices=["pass", "hold", "void"], default="hold",
                        help="Exit 1 if any skill at or above this level")
    args = parser.parse_args(argv)

    if not args.skills_dir.exists():
        print(f"Skills directory not found: {args.skills_dir}", file=sys.stderr)
        return 1

    # Discover skills
    skill_dirs = []
    for entry in sorted(args.skills_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        if args.skills:
            import fnmatch
            patterns = [p.strip() for p in args.skills.split(",")]
            if not any(fnmatch.fnmatch(entry.name, p) for p in patterns):
                continue
        skill_dirs.append(entry)

    # Audit
    verdicts = [audit_skill(d) for d in skill_dirs]

    # Report
    if args.format == "json":
        report = json_report(verdicts)
    else:
        report = markdown_report(verdicts)

    if args.output:
        args.output.write_text(report, encoding="utf-8")
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)

    # Exit code
    level_rank = {"pass": 2, "hold": 1, "void": 0}
    fail_rank = level_rank[args.fail_on]
    worst = min(({"PASS": 2, "HOLD": 1, "VOID": 0}[v.verdict] for v in verdicts), default=2)
    return 1 if worst <= fail_rank else 0


if __name__ == "__main__":
    sys.exit(main())
