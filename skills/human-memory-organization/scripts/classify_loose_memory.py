#!/usr/bin/env python3
"""
classify_loose_memory.py — T1 re-runnable classifier for /root/memory/ root.

Scans /root/memory/ root for loose files (not in H1-H6 subdirs, not in
.archive, archive/, evidence/, ratifications/, rsi/, sessions/).
Applies the classification pattern rules.
EMITS A PLAN — does not move anything. The agent runs `mv` per the plan.

Usage:
  python3 classify_loose_memory.py [--memory-dir /root/memory]

Exit codes:
  0 — clean (no loose files at root)
  1 — loose files found (printed plan)
  2 — error
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# Classification rules: (regex_pattern, destination_relative_to_memory)
PATTERNS = [
    # H2 — Experience
    (r"^2026-\d{2}-\d{2}.*\.md$", "H2-experience/2026-{month}/"),
    (r"^2026-\d{2}-(SEAL|TRIBUNAL|AUDIT|THEORY|ZEN|INIT|CHAOS|BANGANG|ALIAS|EXTINCTION|RSI|MARHIN|GEOSCIENCE).*\.md$", "H2-experience/2026-{month}/"),
    (r"^.*-(SEAL|AUDIT|TRIBUNAL|THEORY|ZEN|INIT)-.*\.md$", "H2-experience/2026-{month}/"),
    (r"^overnight-.*\.md$", "H2-experience/2026-{month}/"),
    (r"^sensorium-.*\.md$", "H2-experience/2026-{month}/"),
    (r"^opencode-init-.*\.md$", "H2-experience/2026-{month}/"),
    (r"^carry-forward-.*\.md$", "H2-experience/2026-{month}/"),
    (r"^session-seal-.*\.md$", "H2-experience/2026-{month}/"),
    (r"^NEXT-SESSION-TODO\.md$", "H2-experience/2026-{month}/"),
    (r"^atlas333-.*\.md$", "H2-experience/2026-{month}/"),
    (r"^protocol-audit-session\.md$", "H2-experience/2026-{month}/"),
    # H3 — Knowledge
    (r"^STANDING_INSTRUCTION_.*\.md$", "H3-knowledge/"),
    (r"^.*RIGOR.*\.md$", "H3-knowledge/"),
    (r"^GEOX-.*\.md$", "H3-knowledge/"),
    (r"^fig\d+.*\.png$", "H3-knowledge/geox-figures/"),
    (r"^figure\d+.*\.png$", "H3-knowledge/<domain>/"),
    # H4 — Identity
    (r"^ARIF-FAZIL-.*\.pdf$", "H4-identity/"),
    (r"^.*BIOGRAPHY.*\.pdf$", "H4-identity/"),
    (r"^.*CV.*\.pdf$", "H4-identity/"),
]

# Subdirs that are NOT "loose" — already classified
CLASSIFIED_SUBDIRS = {
    "H1-capture", "H2-experience", "H3-knowledge", "H4-identity",
    "H5-scars", "H6-constitution",
    "archive", ".archive-2026-07", "evidence", "ratifications",
    "rsi", "sessions", ".github",
}


def month_from_filename(name):
    """Extract YYYY-MM from filename or mtime."""
    m = re.search(r"2026-(\d{2})", name)
    if m:
        return f"2026-{m.group(1)}"
    return "unclassified"


def classify(memory_dir):
    memory = Path(memory_dir)
    if not memory.exists():
        print(f"ERROR: {memory_dir} does not exist", file=sys.stderr)
        return 2

    loose = []
    for entry in memory.iterdir():
        if entry.is_file():
            loose.append(entry)
        elif entry.is_dir() and entry.name not in CLASSIFIED_SUBDIRS:
            print(f"WARN: stray directory at root: {entry.name}")

    if not loose:
        print(f"OK {memory_dir} is clean -- 0 loose files at root")
        return 0

    plan = defaultdict(list)
    unclassifiable = []

    for f in sorted(loose):
        name = f.name
        matched = False
        for pattern, dest_template in PATTERNS:
            if re.match(pattern, name):
                dest = dest_template.format(month=month_from_filename(name))
                dest = dest.replace("<domain>", "general")
                plan[dest].append(name)
                matched = True
                break
        if not matched:
            unclassifiable.append(name)

    print(f"PLAN Classification plan for {memory_dir}")
    print(f"   {len(loose)} loose files -> {len(plan)} destinations\n")
    for dest, files in sorted(plan.items()):
        print(f"-> {dest}")
        for fname in files:
            print(f"    mv '{fname}' '{dest}{fname}'")

    if unclassifiable:
        print(f"\nWARN {len(unclassifiable)} files NOT matched -- manual review:")
        for fname in unclassifiable:
            print(f"    {fname}")

    print(f"\nAfter execution, verify with:")
    print(f"  ls /root/memory/*.{{md,pdf,png}} 2>/dev/null | wc -l")
    print(f"  expect 0")

    return 1


if __name__ == "__main__":
    memory_dir = sys.argv[1] if len(sys.argv) > 1 else "/root/memory"
    sys.exit(classify(memory_dir))