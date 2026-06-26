#!/usr/bin/env python3
"""
AAA Skill Validator — skills/validate.py
Validates each skill's SKILL.md frontmatter against schemas/aaa-skill.yaml.

Usage:
  python skills/validate.py                  # validate all skills
  python skills/validate.py github-pr-review # validate one skill
  python skills/validate.py --strict         # fail on warnings too
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

SKILLS_DIR   = Path(__file__).parent
SCHEMAS_DIR  = SKILLS_DIR.parent / "schemas"
SCHEMA_FILE  = SCHEMAS_DIR / "aaa-skill.yaml"

# Fields required by schema
REQUIRED = {"id", "name", "version", "description", "owner", "risk_tier",
            "host_compatibility", "version_lock"}

ALLOWED_OWNERS = {"AAA", "arifOS", "GEOX", "WEALTH", "WELL", "A-FORGE", "HERMES"}
ALLOWED_RISKS  = {"low", "medium", "high", "critical"}
ALLOWED_HOSTS  = {
    "claude-code", "claude", "codex", "openai", "kimi", "kimi-code",
    "opencode", "grok", "copilot", "copilot-cli", "continue", "antigravity",
    "openclaw", "openclaw-gateway", "mcp", "hermes-asi", "hermes",
    "apx-judge", "any-aaa-agent",
}
ALLOWED_FLOORS = {f"F{i}" for i in range(1, 14)}
ALLOWED_BLAST  = {"OBSERVE", "ANALYZE", "DRAFT", "MUTATE", "EXTERNAL_SIDE_EFFECT", "IRREVERSIBLE"}
ID_PATTERN     = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
VER_PATTERN    = re.compile(r"^\d+\.\d+\.\d+$")
HASH_PATTERN   = re.compile(r"^(pending|[a-f0-9]{64})$")


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}


def validate_skill(skill_dir: Path, strict: bool = False) -> list[str]:
    """Return list of error/warning strings. Empty = valid."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"  ERROR  {skill_dir.name}/SKILL.md not found"]

    text = skill_md.read_text(encoding="utf-8")
    try:
        meta = parse_frontmatter(text)
    except yaml.YAMLError as e:
        return [f"  ERROR  YAML parse failed: {str(e).splitlines()[0]}"]
    sid = meta.get("id", skill_dir.name)
    issues: list[str] = []

    def err(msg: str) -> None:
        issues.append(f"  ERROR  {msg}")

    def warn(msg: str) -> None:
        issues.append(f"  {'ERROR' if strict else 'WARN '}  {msg}")

    # Required fields
    for field in REQUIRED:
        if field not in meta:
            err(f"missing required field: '{field}'")

    # id
    if "id" in meta:
        if not ID_PATTERN.match(str(meta["id"])):
            err(f"id '{meta['id']}' must be kebab-case (a-z0-9 and hyphens)")
        if meta["id"] != skill_dir.name:
            warn(f"id '{meta['id']}' does not match directory name '{skill_dir.name}'")

    # version
    if "version" in meta and not VER_PATTERN.match(str(meta["version"])):
        err(f"version '{meta['version']}' must be MAJOR.MINOR.PATCH")

    # description
    if "description" in meta:
        desc = str(meta["description"])
        if len(desc) < 10:
            err("description too short (min 10 chars)")
        if len(desc) > 512:
            warn("description too long (max 512 chars recommended)")

    # owner
    if "owner" in meta and meta["owner"] not in ALLOWED_OWNERS:
        err(f"owner '{meta['owner']}' not in allowed set: {sorted(ALLOWED_OWNERS)}")

    # risk_tier
    if "risk_tier" in meta and meta["risk_tier"] not in ALLOWED_RISKS:
        err(f"risk_tier '{meta['risk_tier']}' must be one of: {sorted(ALLOWED_RISKS)}")

    # host_compatibility
    if "host_compatibility" in meta:
        compat = meta["host_compatibility"]
        if not isinstance(compat, list) or len(compat) == 0:
            err("host_compatibility must be a non-empty list")
        else:
            for vendor in compat:
                if vendor not in ALLOWED_HOSTS:
                    warn(f"unknown host_compatibility vendor: '{vendor}' — add to compile.py VENDOR_MAP")

    # floors
    if "floors" in meta:
        for floor in (meta["floors"] or []):
            if floor not in ALLOWED_FLOORS:
                err(f"unknown floor '{floor}' — must be F1..F13")

    # blast_radius
    if "blast_radius" in meta and meta["blast_radius"] not in ALLOWED_BLAST:
        err(f"blast_radius '{meta['blast_radius']}' not in allowed set")

    # version_lock
    if "version_lock" in meta:
        vl = meta["version_lock"]
        if not isinstance(vl, dict):
            err("version_lock must be an object")
        else:
            if vl.get("schema_version") != "1":
                err(f"version_lock.schema_version must be '1', got '{vl.get('schema_version')}'")
            if "artifact_hash" in vl and not HASH_PATTERN.match(str(vl["artifact_hash"])):
                err(f"version_lock.artifact_hash must be 'pending' or 64-char hex")

    # knowledge_basis
    if "knowledge_basis" in meta:
        kb = meta["knowledge_basis"]
        if not isinstance(kb, dict):
            err("knowledge_basis must be an object")
        else:
            for field in ("physics", "math", "language"):
                if field not in kb:
                    warn(f"knowledge_basis.{field} not declared (recommend adding)")

    # Promotion readiness (warnings only)
    if not meta.get("examples"):
        warn("no examples declared — add at least 1 for TREE777 promotion readiness")
    if not meta.get("tests"):
        warn("no tests declared — add at least 1 for TREE777 promotion readiness")

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AAA Skill Validator — validates SKILL.md frontmatter against aaa-skill.yaml schema"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        help="skill-id to validate, or 'all' (default)",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    if args.target == "all":
        skill_dirs = sorted(
            d for d in SKILLS_DIR.iterdir()
            if d.is_dir() and (d / "SKILL.md").exists()
        )
    else:
        candidate = SKILLS_DIR / args.target
        if not candidate.exists():
            print(f"ERROR: skill '{args.target}' not found", file=sys.stderr)
            sys.exit(1)
        skill_dirs = [candidate]

    total_errors = 0
    total_warns  = 0
    failed: list[str] = []

    for skill_dir in skill_dirs:
        issues = validate_skill(skill_dir, strict=args.strict)
        errors = [i for i in issues if "ERROR" in i]
        warns  = [i for i in issues if "WARN" in i]

        if issues:
            print(f"\n{skill_dir.name}:")
            for issue in issues:
                print(issue)

        total_errors += len(errors)
        total_warns  += len(warns)
        if errors:
            failed.append(skill_dir.name)

    print(f"\nDone. {len(skill_dirs)} skills validated.")
    print(f"  Errors:   {total_errors}")
    print(f"  Warnings: {total_warns}")

    if failed:
        print(f"\nFailed ({len(failed)}):")
        for name in failed:
            print(f"  {name}")
        sys.exit(1)
    else:
        print("\nAll skills VALID.")


if __name__ == "__main__":
    main()
