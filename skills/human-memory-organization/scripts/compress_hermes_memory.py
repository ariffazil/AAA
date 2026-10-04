#!/usr/bin/env python3
"""
Hermes Flat Memory → Helix Compression Script
T1 re-runnable. Backs up before write. Preserves identity-bearing content.

Usage:
    python3 compress_hermes_memory.py                    # dry-run (preview only)
    python3 compress_hermes_memory.py --apply             # apply compression
    python3 compress_hermes_memory.py --apply --profile aaa-hermes  # specific profile

The script:
1. Reads MEMORY.md + USER.md from both global and profile-specific locations
2. Reports current sizes
3. If --apply, backs up to timestamped .bak, then truncates whitespace
4. Prints before/after byte counts

Note: this script does NOT auto-compress content. It provides the byte budget info
and backs up. Content compression requires LLM reasoning (identity vs operational
split) which is done by the agent, not a script. The agent reads the files, decides
what to merge/drop, then writes_file the compressed version.
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

GLOBAL_MEM = Path.home() / ".hermes/memories"
PROFILES_ROOT = Path.home() / ".hermes/profiles"
PROFILES_ALT = Path("/usr/local/lib/hermes-agent/profiles")

MEMORY_FILES = ["MEMORY.md", "USER.md"]
CHAR_LIMIT = 6000  # Hermes memory tool hard limit per file


def find_profile_dir(profile_name: str) -> Path | None:
    """Find profile memory dir (try both known locations)."""
    for root in [PROFILES_ROOT, PROFILES_ALT]:
        d = root / profile_name / "memories"
        if d.exists():
            return d
    return None


def get_file_info(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path), "exists": False, "bytes": 0, "chars": 0, "pct": 0}
    text = path.read_text(encoding="utf-8")
    return {
        "path": str(path),
        "exists": True,
        "bytes": path.stat().st_size,
        "chars": len(text),
        "pct": round(len(text) / CHAR_LIMIT * 100, 1),
    }


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    ts = int(datetime.now().timestamp())
    backup = path.with_suffix(f".md.bak.{ts}")
    shutil.copy2(path, backup)
    return backup


def main():
    parser = argparse.ArgumentParser(description="Hermes memory compression diagnostics + backup")
    parser.add_argument("--apply", action="store_true", help="Create backups before agent compresses")
    parser.add_argument("--profile", default="aaa-hermes", help="Profile name (default: aaa-hermes)")
    args = parser.parse_args()

    profile_dir = find_profile_dir(args.profile)

    print(f"=== Hermes Memory Budget Report ===")
    print(f"Profile: {args.profile}")
    print(f"Char limit per file: {CHAR_LIMIT:,}")
    print()

    files_to_check = []

    # Global
    for fname in MEMORY_FILES:
        p = GLOBAL_MEM / fname
        files_to_check.append(get_file_info(p))

    # Profile-specific
    if profile_dir:
        for fname in MEMORY_FILES:
            p = profile_dir / fname
            files_to_check.append(get_file_info(p))
    else:
        print(f"⚠️  Profile '{args.profile}' not found in {PROFILES_ROOT} or {PROFILES_ALT}")

    total_chars = 0
    total_budget = 0

    for info in files_to_check:
        if info["exists"]:
            status = "🔴 FULL" if info["pct"] > 90 else "🟡 HIGH" if info["pct"] > 70 else "🟢 OK"
            print(f"{status} {info['path']}")
            print(f"   {info['chars']:,} chars / {CHAR_LIMIT:,} ({info['pct']}%)")
            total_chars += info["chars"]
            total_budget += CHAR_LIMIT

            if args.apply:
                backup = backup_file(Path(info["path"]))
                if backup:
                    print(f"   📦 Backed up → {backup.name}")

            print()

    if total_chars > 0:
        total_pct = round(total_chars / total_budget * 100, 1)
        print(f"Total: {total_chars:,} / {total_budget:,} ({total_pct}%)")

    print()
    print("=== Compression Checklist ===")
    print("1. Identity-bearing entries (KEEP): personality, persons, address pref, architecture")
    print("2. Operational detail (COMPRESS to 1-line): git hashes, ports, specific paths")
    print("3. Filesystem-recoverable (DROP): anything in git log, H2-experience, or H5-scars")
    print()
    print("After compression: agent uses write_file() to save compressed MEMORY.md + USER.md")


if __name__ == "__main__":
    main()
