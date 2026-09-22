#!/usr/bin/env python3
"""Cross-tree divergence probe — classify every co-named file across N source trees.

Read-only. This is Step 1 of canonical-source-designation: the measurement that must
precede any canonical designation. Nothing is written, nothing is moved.

Usage:
    python3 tree_divergence_probe.py TREE_A TREE_B [TREE_C ...] [--ext .py] [--depth N]

Example:
    python3 tree_divergence_probe.py /root/chron /root/AAA/scripts

Dispositions printed are PROVISIONAL. A strict subset is structural; whether to keep or
refuse the loser's unique logic is a judgement you make by reading the diffs — see
references/divergence-triage.md.

    IDENTICAL            all copies byte-identical
    STRICT_SUBSET        one copy's lines are all present in another's (nothing unique)
    DIVERGED_INCOMPATIBLE both copies carry lines the other lacks -> read both, HOLD
    TREE_ORIGINAL        present in exactly one tree
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import os
import sys
from pathlib import Path

SKIP_DIR_PARTS = {"__pycache__", ".git", ".mypy_cache", ".pytest_cache", "node_modules", ".venv"}
SKIP_DIR_PREFIXES = ("backup-", ".backup", ".archived", ".archive", "originals-moved-", "my-shims-superseded-", ".pre-")


def walk(root: Path, ext: str, depth: int) -> dict[str, Path]:
    found: dict[str, Path] = {}
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        if len(rel.parts) > depth:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_PARTS and not d.startswith(SKIP_DIR_PREFIXES)]
        for fn in filenames:
            if fn.endswith(ext):
                found.setdefault(fn, Path(dirpath) / fn)
    return found


def digest(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        return f"ERR:{exc.errno}"


def lines(path: Path) -> list[str]:
    try:
        return path.read_text(errors="replace").splitlines()
    except OSError:
        return []


def unique_counts(a: Path, b: Path) -> tuple[int, int]:
    d = list(difflib.unified_diff(lines(a), lines(b), n=0))
    return (
        sum(1 for l in d if l.startswith("-") and not l.startswith("---")),
        sum(1 for l in d if l.startswith("+") and not l.startswith("+++")),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("trees", nargs="+", help="two or more source-tree roots")
    ap.add_argument("--ext", default=".py", help="file extension to consider (default .py)")
    ap.add_argument("--depth", type=int, default=1, help="max subdirectory depth (default 1)")
    args = ap.parse_args()

    if len(args.trees) < 2:
        print("need at least two trees to compare", file=sys.stderr)
        return 2

    inventories = {t: walk(Path(t), args.ext, args.depth) for t in args.trees}
    all_names = sorted({n for inv in inventories.values() for n in inv})

    if not all_names:
        print(f"no {args.ext} files found under any tree", file=sys.stderr)
        return 1

    present = {n: [t for t, inv in inventories.items() if n in inv] for n in all_names}
    identical, subset, incompatible, tree_original = [], [], [], []

    for name in all_names:
        trees = present[name]
        print(f"\n=== {name}")
        for t in args.trees:
            p = inventories[t].get(name)
            if p is None:
                print(f"    {t:24s}  --")
                continue
            link = " LINK" if p.is_symlink() else "     "
            print(f"    {t:24s}{link} {p.stat().st_size:8d}B  sha256:{digest(p)[:16]}")

        if len(trees) == 1:
            print(f"    -> TREE_ORIGINAL ({trees[0]}); designating source, do not move")
            tree_original.append(name)
            continue

        base = inventories[trees[0]].get(name)
        verdict = "IDENTICAL"
        for other_t in trees[1:]:
            other = inventories[other_t].get(name)
            if base and other and digest(base) == digest(other):
                continue
            if base and other:
                old_only, new_only = unique_counts(base, other)
                print(f"    -> unique: {trees[0]}={old_only}  {other_t}={new_only}")
                if old_only and new_only:
                    verdict = "DIVERGED_INCOMPATIBLE"
                elif verdict != "DIVERGED_INCOMPATIBLE":
                    verdict = "STRICT_SUBSET"
        print(f"    -> {verdict}")
        {"IDENTICAL": identical, "STRICT_SUBSET": subset, "DIVERGED_INCOMPATIBLE": incompatible}[verdict].append(name)

    print("\n" + "=" * 72)
    for label, names in (
        ("IDENTICAL", identical),
        ("STRICT_SUBSET", subset),
        ("DIVERGED_INCOMPATIBLE (read both, HOLD)", incompatible),
        ("TREE_ORIGINAL (single tree)", tree_original),
    ):
        print(f"{label:36s} {len(names)}")
        for n in names:
            print(f"      {n}")
    print(
        "\nProvisional only. For every DIVERGED_INCOMPATIBLE pair, read both diffs before "
        "converging; for every STRICT_SUBSET, confirm the unique lines are prose, not logic."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
