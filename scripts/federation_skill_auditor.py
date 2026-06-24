#!/usr/bin/env python3
"""Federation Skill Auditor.

Audits skill directories across Kimi, project, AAA, OpenCode, HERMES, arifOS,
and WELL scopes for structural hygiene, content quality, cross-scope integrity,
and federation alignment.

Read-only by design. Never moves or deletes skills.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


try:
    import yaml

    HAS_YAML = True
except ImportError:  # pragma: no cover
    HAS_YAML = False


DEFAULT_CONFIG = Path(__file__).parent.parent / "config" / "skill_auditor.yaml"


@dataclass
class Finding:
    severity: str  # ERROR, WARNING, INFO
    scope: str
    skill: str
    check: str
    message: str


@dataclass
class SkillInfo:
    scope: str
    name: str
    path: Path
    frontmatter: dict[str, Any] = field(default_factory=dict)
    has_examples: bool = False
    has_tests: bool = False
    has_cli_binding: bool = False


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse YAML frontmatter from markdown text."""
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
    # Minimal fallback: extract simple key:value lines
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


def normalize_name(name: str) -> str:
    """Normalize skill name for duplicate detection."""
    return re.sub(r"[-_\s]+", "-", name.strip().lower())


def description_similarity(a: str, b: str) -> float:
    """Simple Jaccard similarity over words."""
    if not a or not b:
        return 0.0
    words_a = set(re.findall(r"\b\w+\b", a.lower()))
    words_b = set(re.findall(r"\b\w+\b", b.lower()))
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union)


def discover_skills(scope: str, scope_path: Path) -> list[SkillInfo]:
    """Discover skill directories in a scope."""
    skills: list[SkillInfo] = []
    if not scope_path.exists():
        return skills
    for entry in scope_path.iterdir():
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        skill_md = entry / "SKILL.md"
        if skill_md.exists():
            text = skill_md.read_text(encoding="utf-8", errors="ignore")
            fm = parse_frontmatter(text)
            name = fm.get("name") or fm.get("id") or entry.name
            skills.append(
                SkillInfo(
                    scope=scope,
                    name=name,
                    path=entry,
                    frontmatter=fm,
                    has_examples=(entry / "examples.md").exists(),
                    has_tests=(entry / "tests.md").exists(),
                    has_cli_binding=(entry / "bindings" / "cli.yaml").exists(),
                )
            )
        else:
            # Directory without SKILL.md
            skills.append(
                SkillInfo(
                    scope=scope,
                    name=entry.name,
                    path=entry,
                )
            )
    return skills


def audit_skill(
    skill: SkillInfo,
    config: dict[str, Any],
    findings: list[Finding],
) -> None:
    """Run all configured checks against a single skill."""
    scope_config = config.get("scopes", {}).get(skill.scope, {})
    required_files = scope_config.get("required_files", ["SKILL.md"])
    required_bindings = scope_config.get("required_bindings", [])

    skill_md = skill.path / "SKILL.md"

    # Structural checks
    if not skill_md.exists():
        findings.append(
            Finding(
                severity="ERROR",
                scope=skill.scope,
                skill=skill.name,
                check="missing_skill_md",
                message="SKILL.md not found",
            )
        )
        return

    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    fm = skill.frontmatter

    if "_parse_error" in fm:
        findings.append(
            Finding(
                severity="ERROR",
                scope=skill.scope,
                skill=skill.name,
                check="frontmatter_parse",
                message="Frontmatter YAML parse error",
            )
        )
        return

    if not fm:
        findings.append(
            Finding(
                severity="ERROR",
                scope=skill.scope,
                skill=skill.name,
                check="frontmatter_missing",
                message="No YAML frontmatter found",
            )
        )

    if "name" not in fm:
        findings.append(
            Finding(
                severity="ERROR",
                scope=skill.scope,
                skill=skill.name,
                check="missing_name",
                message="Frontmatter missing 'name' field",
            )
        )
    else:
        declared = str(fm["name"])
        if normalize_name(declared) != normalize_name(skill.path.name):
            findings.append(
                Finding(
                    severity="WARNING",
                    scope=skill.scope,
                    skill=skill.name,
                    check="name_mismatch",
                    message=f"Skill name '{declared}' does not match directory '{skill.path.name}'",
                )
            )

    if "description" not in fm:
        findings.append(
            Finding(
                severity="WARNING",
                scope=skill.scope,
                skill=skill.name,
                check="missing_description",
                message="Frontmatter missing 'description' field",
            )
        )
    else:
        desc = str(fm["description"])
        if len(desc) > 400:
            findings.append(
                Finding(
                    severity="INFO",
                    scope=skill.scope,
                    skill=skill.name,
                    check="description_length",
                    message=f"Description is {len(desc)} chars (recommended ≤ 400)",
                )
            )
        vague_words = ["help", "assist", "improve"]
        if any(word in desc.lower() for word in vague_words):
            findings.append(
                Finding(
                    severity="WARNING",
                    scope=skill.scope,
                    skill=skill.name,
                    check="vague_description",
                    message="Description contains vague verbs (help/assist/improve) without strong object",
                )
            )

    if "version" not in fm:
        findings.append(
            Finding(
                severity="WARNING",
                scope=skill.scope,
                skill=skill.name,
                check="missing_version",
                message="Frontmatter missing 'version' field",
            )
        )

    # Required files
    for req_file in required_files:
        if req_file == "SKILL.md":
            continue
        if not (skill.path / req_file).exists():
            findings.append(
                Finding(
                    severity="WARNING",
                    scope=skill.scope,
                    skill=skill.name,
                    check=f"missing_{req_file.replace('.', '_')}",
                    message=f"Required file '{req_file}' not found",
                )
            )

    # Required bindings
    for binding in required_bindings:
        binding_path = skill.path / "bindings" / binding
        if not binding_path.exists():
            findings.append(
                Finding(
                    severity="INFO",
                    scope=skill.scope,
                    skill=skill.name,
                    check=f"missing_binding_{binding.replace('.', '_')}",
                    message=f"Binding '{binding}' not found",
                )
            )

    # Content quality
    body = extract_body(text)
    if "## Use When" not in body and "## Use when" not in body:
        findings.append(
            Finding(
                severity="WARNING",
                scope=skill.scope,
                skill=skill.name,
                check="missing_use_when",
                message="No 'Use When' section found",
            )
        )

    # Federation alignment
    if "mutation" in fm or "blast_radius" in fm or "approval_policy" in fm:
        mutation = fm.get("mutation", {})
        if isinstance(mutation, dict):
            if "class" not in mutation:
                findings.append(
                    Finding(
                        severity="INFO",
                        scope=skill.scope,
                        skill=skill.name,
                        check="incomplete_ag_constraint",
                        message="AGI/ASI constraint present but mutation.class missing",
                    )
                )
        approval = fm.get("approval_policy")
        mutation_class = mutation.get("class") if isinstance(mutation, dict) else None
        if approval == "auto" and mutation_class != "read_only":
            findings.append(
                Finding(
                    severity="WARNING",
                    scope=skill.scope,
                    skill=skill.name,
                    check="risk_tier_inconsistent",
                    message="approval_policy=auto requires mutation.class=read_only",
                )
            )

    # Authority order check: skill must not CLAIM judge/sovereign authority.
    # Mere mention of these terms in descriptive context is allowed.
    body_lower = body.lower()
    authority_terms = ("sovereign", "f13", "judge", "seal", "constitutional kernel", "arifos")
    claim_verbs = (
        "can ", "will ", "may ", "has authority", "is authorized", "is the ", "acts as ",
        "overrides", "bypasses", "supersedes", "trumps", "claims", "wields", "exercises",
        "grants authority", "holds authority", "final authority", "ultimate authority",
    )
    has_authority_term = any(term in body_lower for term in authority_terms)
    has_claim_verb = any(verb in body_lower for verb in claim_verbs)
    if has_authority_term and has_claim_verb:
        findings.append(
            Finding(
                severity="ERROR",
                scope=skill.scope,
                skill=skill.name,
                check="authority_claim",
                message="Skill appears to claim sovereign/judge/seal authority — violates federation authority order",
            )
        )


def audit_cross_scope(
    all_skills: list[SkillInfo],
    findings: list[Finding],
) -> None:
    """Cross-scope integrity checks."""
    # Duplicate names
    by_name: dict[str, list[SkillInfo]] = defaultdict(list)
    for skill in all_skills:
        by_name[normalize_name(skill.name)].append(skill)

    for name, skills in by_name.items():
        if len(skills) > 1:
            scopes = ", ".join(sorted({s.scope for s in skills}))
            findings.append(
                Finding(
                    severity="WARNING",
                    scope="cross-scope",
                    skill=name,
                    check="duplicate_name",
                    message=f"Skill name appears in multiple scopes: {scopes}",
                )
            )

    # Description similarity
    skills_with_desc = [
        s for s in all_skills if isinstance(s.frontmatter, dict) and s.frontmatter.get("description")
    ]
    threshold = 0.85
    checked: set[tuple[str, str]] = set()
    for i, a in enumerate(skills_with_desc):
        for b in skills_with_desc[i + 1 :]:
            key = tuple(sorted([normalize_name(a.name), normalize_name(b.name)]))
            if key in checked:
                continue
            checked.add(key)
            desc_a = str(a.frontmatter.get("description", ""))
            desc_b = str(b.frontmatter.get("description", ""))
            sim = description_similarity(desc_a, desc_b)
            if sim >= threshold:
                findings.append(
                    Finding(
                        severity="INFO",
                        scope="cross-scope",
                        skill=f"{a.name} / {b.name}",
                        check="description_similarity",
                        message=f"Description similarity {sim:.2f} — possible trigger collision",
                    )
                )

    # References to quarantine paths
    quarantine_pattern = re.compile(r"\.quarantine-\d{4}-\d{2}-\d{2}")
    for skill in all_skills:
        skill_md = skill.path / "SKILL.md"
        if not skill_md.exists():
            continue
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        if quarantine_pattern.search(text):
            findings.append(
                Finding(
                    severity="ERROR",
                    scope=skill.scope,
                    skill=skill.name,
                    check="quarantine_reference",
                    message="Skill references a quarantined path",
                )
            )


def load_config(path: Path) -> dict[str, Any]:
    """Load auditor configuration."""
    if not path.exists():
        print(f"Config not found at {path}; using defaults.", file=sys.stderr)
        return {
            "scopes": {
                "kimi": {
                    "path": "/root/.arifos/agents/kimi/skills",
                    "required_files": ["SKILL.md", "examples.md", "tests.md"],
                    "required_bindings": ["cli.yaml"],
                },
                "project": {
                    "path": "/root/.agents/skills",
                    "required_files": ["SKILL.md"],
                    "required_bindings": [],
                },
                "aaa": {
                    "path": "/root/AAA/skills",
                    "required_files": ["SKILL.md"],
                    "required_bindings": [],
                },
                "opencode": {
                    "path": "/root/.arifos/agents/opencode/skills",
                    "required_files": ["SKILL.md"],
                    "required_bindings": [],
                },
            }
        }
    if HAS_YAML:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raise RuntimeError("PyYAML required to read config")


def markdown_report(
    all_skills: list[SkillInfo],
    findings: list[Finding],
    config: dict[str, Any],
) -> str:
    """Generate markdown audit report."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    lines = [
        "# Federation Skill Audit Report",
        "",
        f"**Generated:** {now}",
        f"**Scopes audited:** {len(config.get('scopes', {}))}",
        f"**Skills scanned:** {len(all_skills)}",
        f"**ERROR:** {counts['ERROR']}",
        f"**WARNING:** {counts['WARNING']}",
        f"**INFO:** {counts['INFO']}",
        "",
        "## Summary by scope",
        "",
        "| Scope | Skills | ERROR | WARNING | INFO |",
        "|---|---|---|---|---|",
    ]

    by_scope: dict[str, list[SkillInfo]] = defaultdict(list)
    for s in all_skills:
        by_scope[s.scope].append(s)

    for scope in sorted(by_scope):
        skills = by_scope[scope]
        scope_findings = [f for f in findings if f.scope == scope]
        e = sum(1 for f in scope_findings if f.severity == "ERROR")
        w = sum(1 for f in scope_findings if f.severity == "WARNING")
        i = sum(1 for f in scope_findings if f.severity == "INFO")
        lines.append(f"| {scope} | {len(skills)} | {e} | {w} | {i} |")

    cross_findings = [f for f in findings if f.scope == "cross-scope"]
    if cross_findings:
        lines.extend([
            "",
            "## Cross-scope findings",
            "",
            "| Severity | Skill | Check | Message |",
            "|---|---|---|---|",
        ])
        for f in cross_findings:
            lines.append(f"| {f.severity} | {f.skill} | {f.check} | {f.message} |")

    # Per-scope findings
    for scope in sorted(by_scope):
        scope_findings = [f for f in findings if f.scope == scope]
        if not scope_findings:
            continue
        lines.extend([
            "",
            f"## {scope} findings",
            "",
            "| Severity | Skill | Check | Message |",
            "|---|---|---|---|",
        ])
        for f in scope_findings:
            lines.append(f"| {f.severity} | {f.skill} | {f.check} | {f.message} |")

    # Rot classification
    rot_map = {
        "doc-rot": ["missing_examples_md", "missing_tests_md", "missing_use_when"],
        "trigger-rot": ["duplicate_name", "description_similarity", "vague_description"],
        "unused-rot": [],
        "api-rot": ["missing_version"],
        "fake-rot": [],
        "creep-rot": ["authority_claim", "risk_tier_inconsistent"],
    }
    rot_counts: dict[str, int] = {k: 0 for k in rot_map}
    for f in findings:
        for rot_type, checks in rot_map.items():
            if f.check in checks:
                rot_counts[rot_type] += 1

    lines.extend([
        "",
        "## Rot classification",
        "",
        "| Rot class | Count |",
        "|---|---|",
    ])
    for rot_type, count in rot_counts.items():
        lines.append(f"| {rot_type} | {count} |")

    lines.append("")
    return "\n".join(lines)


def json_report(all_skills: list[SkillInfo], findings: list[Finding]) -> str:
    """Generate JSON audit report."""
    return json.dumps(
        {
            "skills_scanned": len(all_skills),
            "findings": [
                {
                    "severity": f.severity,
                    "scope": f.scope,
                    "skill": f.skill,
                    "check": f.check,
                    "message": f.message,
                }
                for f in findings
            ],
        },
        indent=2,
    )


def github_report(findings: list[Finding]) -> str:
    """Generate GitHub Actions annotation format."""
    lines = []
    for f in findings:
        level = "error" if f.severity == "ERROR" else "warning"
        lines.append(f"::{level}::{f.scope}/{f.skill}: {f.check} — {f.message}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Federation Skill Auditor")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to auditor config",
    )
    parser.add_argument(
        "--scopes",
        type=str,
        default="",
        help="Comma-separated list of scopes to audit",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "github"],
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--fail-on",
        choices=["error", "warning", "info"],
        default="error",
        help="Minimum severity to fail",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write report to file",
    )
    args = parser.parse_args(argv)

    config = load_config(args.config)
    scopes = config.get("scopes", {})

    if args.scopes:
        wanted = {s.strip() for s in args.scopes.split(",")}
        scopes = {k: v for k, v in scopes.items() if k in wanted}

    all_skills: list[SkillInfo] = []
    findings: list[Finding] = []

    for scope_name, scope_config in scopes.items():
        scope_path = Path(scope_config["path"])
        skills = discover_skills(scope_name, scope_path)
        all_skills.extend(skills)
        for skill in skills:
            audit_skill(skill, config, findings)

    audit_cross_scope(all_skills, findings)

    if args.format == "markdown":
        report = markdown_report(all_skills, findings, config)
    elif args.format == "json":
        report = json_report(all_skills, findings)
    else:
        report = github_report(findings)

    if args.output:
        args.output.write_text(report, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(report)

    severity_rank = {"ERROR": 3, "WARNING": 2, "INFO": 1}
    fail_rank = severity_rank[args.fail_on.upper()]
    worst = max(
        (severity_rank.get(f.severity, 0) for f in findings),
        default=0,
    )

    return 1 if worst >= fail_rank else 0


if __name__ == "__main__":
    sys.exit(main())
