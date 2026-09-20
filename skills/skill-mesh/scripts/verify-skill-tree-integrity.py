#!/usr/bin/env python3
"""Verify a skill tree is whole after a bulk move / dedupe / reclassification.

Run this AFTER the migration, BEFORE reporting. A moved count is not evidence the map is
right; only a row-by-row reconcile is.

Checks
  1. content multiset preserved  -- every SKILL.md hash present before is still present
                                    (needs --backup, a tarball of the pre-migration root)
  2. every map row resolves      -- <root>/<target>/SKILL.md exists
  3. unresolved rows             -- reported WITH the real location, found by leaf/dir match,
                                    so a wrong map row is corrected instead of re-authored
  4. strays                      -- on-disk SKILL.md claimed by no map row
  5. flat leftovers              -- real skill dirs still sitting at the tree root

Usage
  verify-skill-tree-integrity.py --root ~/.hermes/skills --map map.csv
  verify-skill-tree-integrity.py --root ~/.hermes/skills --map map.csv \
      --backup ~/.hermes-backups/skills-pre-migration-<ts>.tar.gz

The map CSV needs a column naming the target path; auto-detected from
[i]matrix_path, target_path, new_path, path[/i]. The skill name is auto-detected from
[i]skill, leaf, name[/i]. Rows whose action is ARCHIVE_COPY are expected to live under
--archive, not in the live tree.

Exit 0 = whole. Exit 1 = at least one check failed. Exit 2 = could not run (bad input).
"""

import argparse
import csv
import hashlib
import os
import sys
import tarfile

EXCLUDED = {".git", ".github", ".hub", ".archive", ".curator_backups", ".venv", "venv",
            "node_modules", "site-packages", "__pycache__", ".tox", ".nox",
            ".pytest_cache", ".mypy_cache", ".ruff_cache"}
SUPPORT = {"references", "templates", "assets", "scripts"}


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def walk_tree(root):
    """Mirror the loader's walk: follow symlinks, prune EXCLUDED and support dirs.

    Returns {relative_skill_dir: content_sha}. Support dirs are pruned ONLY below a dir that
    already holds SKILL.md, matching the loader -- otherwise a skill legitimately named
    'scripts' or 'references' disappears from the inventory.
    """
    found = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        has_md = "SKILL.md" in filenames
        dirnames[:] = [d for d in dirnames
                       if d not in EXCLUDED and not (has_md and d in SUPPORT)]
        if has_md:
            try:
                found[os.path.relpath(dirpath, root)] = sha(os.path.join(dirpath, "SKILL.md"))
            except OSError as exc:
                print(f"  !! unreadable SKILL.md at {dirpath}: {exc}")
    return found


def hashes_from_tarball(path):
    """Before-state hashes. Symlink members are skipped: their content lives outside the
    archive by design, which is exactly why a tarball alone is not a full rollback."""
    out = set()
    with tarfile.open(path) as tf:
        for member in tf.getmembers():
            if not member.isfile() or not member.name.endswith("SKILL.md"):
                continue
            handle = tf.extractfile(member)
            if handle is None:
                continue
            out.add(hashlib.sha256(handle.read()).hexdigest())
    return out


def pick(fieldnames, candidates):
    for cand in candidates:
        if cand in fieldnames:
            return cand
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--map", required=True, dest="map_path")
    ap.add_argument("--backup", help="tarball of the pre-migration root (enables check 1)")
    ap.add_argument("--archive", default=".archive",
                    help="subdir holding preserved copies (default: .archive)")
    args = ap.parse_args()

    root = os.path.expanduser(args.root)
    if not os.path.isdir(root):
        print(f"exit 2: --root is not a directory: {root}")
        return 2
    if not os.path.isfile(args.map_path):
        print(f"exit 2: --map not found: {args.map_path}")
        return 2

    with open(args.map_path, newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        if not rows:
            print("exit 2: map has no rows")
            return 2
        tgt_col = pick(reader.fieldnames, ["matrix_path", "target_path", "new_path", "path"])
        name_col = pick(reader.fieldnames, ["skill", "leaf", "name"])
        act_col = pick(reader.fieldnames, ["action"])
    if not tgt_col or not name_col:
        print(f"exit 2: map needs a target-path column and a skill-name column; "
              f"saw {reader.fieldnames}")
        return 2

    on_disk = walk_tree(root)
    live = {k: v for k, v in on_disk.items() if not k.startswith(args.archive)}
    archive = {k: v for k, v in on_disk.items() if k.startswith(args.archive)}
    failures = []

    print(f"root: {root}")
    print(f"map : {args.map_path}  ({len(rows)} rows)")
    print(f"disk: {len(live)} live leaves, {len(archive)} archived")

    # leaf -> actual relative dirs, for locating a row whose target is wrong
    by_leaf = {}
    for rel in live:
        by_leaf.setdefault(os.path.basename(rel), []).append(rel)

    live_rows = [r for r in rows
                 if not act_col or (r.get(act_col) or "").upper() not in ("ARCHIVE_COPY", "ARCHIVED")]
    unresolved, misplaced = [], []
    for row in live_rows:
        target = (row.get(tgt_col) or "").strip()
        if not target:
            unresolved.append((row.get(name_col), "", "row has no target path"))
            continue
        if os.path.isfile(os.path.join(root, target, "SKILL.md")):
            continue
        leaf = os.path.basename(target.rstrip("/"))
        actual = by_leaf.get(leaf, [])
        if actual:
            misplaced.append((row.get(name_col), target, actual))
        else:
            unresolved.append((row.get(name_col), target, "no SKILL.md under any dir with that leaf"))

    if misplaced:
        print(f"\n[!] {len(misplaced)} rows name a target that does not exist -- content lives elsewhere")
        for name, claimed, actual in misplaced:
            print(f"    {name}")
            print(f"      map says : {claimed}")
            print(f"      lives at : {', '.join(actual)}")
        failures.append(f"{len(misplaced)} misplaced rows")
    if unresolved:
        print(f"\n[!] {len(unresolved)} rows unresolved")
        for name, target, why in unresolved:
            print(f"    {name}: {target} ({why})")
        failures.append(f"{len(unresolved)} unresolved rows")

    claimed_leaves = {os.path.basename((r.get(tgt_col) or "").rstrip("/"))
                      for r in rows if r.get(tgt_col)}
    strays = sorted(rel for rel in live if os.path.basename(rel) not in claimed_leaves)
    if strays:
        print(f"\n[!] {len(strays)} on-disk leaves claimed by no map row (strays)")
        for rel in strays[:25]:
            print(f"    {rel}")
        if len(strays) > 25:
            print(f"    ... and {len(strays) - 25} more")
        failures.append(f"{len(strays)} strays")

    flat = sorted(d for d in os.listdir(root)
                  if not d.startswith(".") and os.path.isdir(os.path.join(root, d))
                  and os.path.isfile(os.path.join(root, d, "SKILL.md")))
    if flat:
        print(f"\n[!] {len(flat)} skill dirs still flat at the tree root")
        for d in flat:
            print(f"    {d}/")
        failures.append(f"{len(flat)} root-level skill dirs")

    if args.backup:
        if not os.path.isfile(args.backup):
            print(f"\n[!] --backup not found: {args.backup}")
            failures.append("backup missing")
        else:
            before = hashes_from_tarball(args.backup)
            now = set(on_disk.values())
            lost = before - now
            print(f"\ncontent multiset: {len(before)} hashes in backup, {len(now)} on disk")
            if lost:
                print(f"[!] {len(lost)} pieces of content in the backup are NOT on disk")
                failures.append(f"{len(lost)} lost content pieces")
            else:
                print("    no content lost")
            print("    note: symlink leaves resolve outside the root; the tarball cannot hold")
            print("          their content. Full rollback = tarball + legacy old->new map +")
            print("          the canonical catalog left untouched.")

    print()
    if failures:
        print("RESULT: FAIL -- " + "; ".join(failures))
        return 1
    print("RESULT: OK -- tree whole, map reconciles with disk")
    return 0


if __name__ == "__main__":
    sys.exit(main())
