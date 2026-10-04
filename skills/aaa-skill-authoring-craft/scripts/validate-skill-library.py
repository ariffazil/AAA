#!/usr/bin/env python3
"""
validate-skill-library.py — sweep ALL SKILL.md files for broken frontmatter.

Found 2 broken skills in 435 during a 2026-08-09 sweep (hermes-propose-seal:
unquoted colon in description; well-governance-ops: no frontmatter at all).
Run this after any bulk skill edit or before a skill-mesh sync.

Usage:
    python3 validate-skill-library.py [root1 root2 ...]
    (defaults: profile skills + /root/HERMES/skills)
"""
import os
import glob
import sys
import yaml

DEFAULT_ROOTS = [
    "/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills",
    "/root/HERMES/skills",
]

def validate(root: str, seen: dict, problems: list) -> int:
    """Scan one root; return count of unique skills found."""
    found = 0
    for skill_md in glob.glob(f"{root}/**/SKILL.md", recursive=True):
        name = os.path.basename(os.path.dirname(skill_md))
        if name in seen:
            continue
        seen[name] = skill_md
        found += 1
        try:
            with open(skill_md) as f:
                content = f.read()
            if not content.startswith("---"):
                problems.append(f"NO_FRONTMATTER: {name} ({skill_md})")
                continue
            parts = content.split("---", 2)
            if len(parts) < 3:
                problems.append(f"MALFORMED: {name} ({skill_md})")
                continue
            fm = yaml.safe_load(parts[1])
            if not fm or "name" not in fm:
                problems.append(f"NO_NAME: {name} ({skill_md})")
                continue
            if not fm.get("description"):
                problems.append(f"EMPTY_DESC: {name} ({skill_md})")
        except Exception as e:
            problems.append(f"PARSE_ERROR: {name} — {e} ({skill_md})")
    return found

def main():
    roots = sys.argv[1:] or DEFAULT_ROOTS
    seen, problems = {}, []
    total = sum(validate(r, seen, problems) for r in roots)
    print(f"Scanned {len(seen)} unique skills across {len(roots)} root(s).")
    if problems:
        print(f"PROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"  {p}")
        sys.exit(1)
    print("All SKILL.md files valid.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
