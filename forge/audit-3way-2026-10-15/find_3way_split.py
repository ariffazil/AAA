#!/usr/bin/env python3
"""
find_3way_split.py — arifOS kernel 3-way code split auditor
F13-ratified 2026-10-15 (Pick ①, read-only).

Scans for arifosmcp tools.py copies, hashes them, compares against
the pre-iter-3 snap, and reports divergence. Does NOT mutate.

Usage:
    python3 find_3way_split.py [--json] [--snap PATH]

Falsifier (1-line + 1 falsifier, per Pattern Library):
    Trigger: kernel diet patch deployed but Pydantic schema rejects new param.
    Falsifier: run this script; if SOURCE ≠ VENV hash, the deploy chain is broken.

Output: JSON to stdout (with --json) or human-readable table.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Canonical paths (probed 2026-10-15, first-party).
# SNAP is the pre-iter-3 ground truth per arifOS kernel iteration-3 memory.
DEFAULT_SNAP = Path("/root/forge_work/quantum-path/tools.py.snap-pre-iter3-d0d1054")
EXPECTED_HASH_SNAP = "e293a395b855fd1d9bae5e27ec09fcea7c3fdfde4893a2bb16b595cc8a501611"

# Diet function location (per arifOS kernel iteration-2 memory).
DIET_FUNCTION_LINE = 15405
DIET_FUNCTION_NAME = "_arif_mind_reason_tool"


def sha256_file(path: Path) -> str | None:
    """Return sha256 of file, or None if unreadable."""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return None


def find_tools_py_copies() -> list[Path]:
    """Find all arifosmcp runtime/tools.py copies on the filesystem.
    Excludes __pycache__ and .bak files.
    """
    roots = [Path("/opt/arifos"), Path("/root/arifOS"), Path("/root/arifOS-wt-mcp-hardening"),
             Path("/root/qrl-verify-20261014"), Path("/live")]
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        try:
            for p in root.rglob("arifosmcp/runtime/tools.py"):
                if "__pycache__" in str(p) or ".bak" in p.name:
                    continue
                found.append(p)
        except (OSError, PermissionError):
            pass
    return sorted(set(found))


def classify(path: Path) -> str:
    """Classify a tools.py copy by its role in the deploy chain.
    Order matters — most specific paths first.
    """
    s = str(path)
    # Orphan / non-canonical copies first
    if "/live/" in s:
        return "ORPHAN"
    if "/root/arifOS/" in s and "/build/" not in s:
        return "WORKING_COPY"  # F13's diet working repo
    if "/root/arifOS/" in s and "/build/" in s:
        return "WORKING_BUILD"  # Stale build of working copy
    if "/root/arifOS-wt-mcp-hardening/" in s:
        return "WORKTREE"
    if "/root/qrl-verify-" in s:
        return "WORKTREE"
    # Canonical /opt/arifos/ deploy chain
    if "/current/venv/" in s:
        return "VENV"
    if "/build/lib/" in s:
        return "BUILD"
    if "/app/" in s and "/arifosmcp/" in s:
        return "APP"
    if s.startswith("/opt/arifos/arifosmcp/runtime/"):
        return "SOURCE"
    # Quarantined copies
    if "/quarantine" in s:
        return "QUARANTINE"
    if "/app.quarantine" in s:
        return "QUARANTINE"
    return "UNKNOWN"


def check_diet_function(path: Path) -> dict:
    """Check if the diet function exists and if 'concise' is in its signature.

    Per DP-A (2026-10-15): the function line is 15383 in /opt/arifos/ source
    and 15405 in /root/arifOS/ working copy. We detect dynamically by finding
    'def _arif_mind_reason_tool' rather than hardcoding the line.

    Returns: {line_found, has_concise, line_number, line_content}
    """
    result = {"line_found": False, "has_concise": False,
              "line_number": None, "line_content": ""}
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            # Find the function def line.
            for i, line in enumerate(f, start=1):
                if "def _arif_mind_reason_tool(" in line:
                    result["line_found"] = True
                    result["line_number"] = i
                    result["line_content"] = line.strip()[:120]
                    # Read signature: lines from def until ')' at end of line.
                    if "concise" in line:
                        result["has_concise"] = True
                    # Also peek at next few lines (signature may span multiple).
                    sig_lines = [line]
                    for _ in range(15):
                        try:
                            nxt = next(f)
                        except StopIteration:
                            break
                        sig_lines.append(nxt)
                        if "concise" in nxt:
                            result["has_concise"] = True
                        if nxt.rstrip().endswith(") -> dict[str, Any]:") or \
                           nxt.rstrip().endswith(") -> dict:") or \
                           (nxt.rstrip().endswith(")") and "->" in nxt):
                            break
                    break
    except (OSError, PermissionError):
        pass
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="arifOS kernel 3-way code split auditor")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    parser.add_argument("--snap", type=Path, default=DEFAULT_SNAP,
                        help="Path to pre-iter-3 snap file (ground truth)")
    args = parser.parse_args()

    snap_hash = sha256_file(args.snap) if args.snap.exists() else None
    snap_status = "MATCH" if snap_hash == EXPECTED_HASH_SNAP else f"DRIFT (expected {EXPECTED_HASH_SNAP[:12]}...)"

    copies = find_tools_py_copies()
    report = {
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        "snap_path": str(args.snap),
        "snap_hash": snap_hash,
        "snap_status": snap_status,
        "expected_snap_hash": EXPECTED_HASH_SNAP,
        "copies": [],
        "deploy_chain_status": "UNKNOWN",
        "schema_generator_status": "NOT_PROBED",
    }

    for p in copies:
        h = sha256_file(p)
        size = p.stat().st_size if p.exists() else 0
        role = classify(p)
        diet = check_diet_function(p)
        matches_snap = (h == snap_hash)
        report["copies"].append({
            "path": str(p),
            "role": role,
            "sha256": h,
            "size_bytes": size,
            "matches_snap": matches_snap,
            "diet_function_line_found": diet["line_found"],
            "diet_function_has_concise": diet["has_concise"],
        })

    # Derive deploy chain status: SOURCE vs VENV divergence.
    src = next((c for c in report["copies"] if c["role"] == "SOURCE"), None)
    venv = next((c for c in report["copies"] if c["role"] == "VENV"), None)
    if src and venv:
        if src["sha256"] == venv["sha256"]:
            report["deploy_chain_status"] = "IN_SYNC"
        else:
            report["deploy_chain_status"] = f"DRIFT (source {src['sha256'][:12]}... != venv {venv['sha256'][:12]}...)"

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        # Human-readable table.
        print(f"=== arifOS 3-way code split audit ({report['audit_timestamp']}) ===")
        print(f"Snap: {args.snap}")
        print(f"Snap hash: {snap_hash}")
        print(f"Snap status: {snap_status}")
        print()
        print(f"{'Role':<8} {'Size (B)':<10} {'Hash (12ch)':<14} {'=Snap?':<6} {'Concise?':<9} Path")
        print("-" * 100)
        for c in report["copies"]:
            concise = "YES" if c["diet_function_has_concise"] else "NO"
            matches = "YES" if c["matches_snap"] else "NO"
            print(f"{c['role']:<8} {c['size_bytes']:<10} {c['sha256'][:12]:<14} {matches:<6} {concise:<9} {c['path']}")
        print()
        print(f"Deploy chain status: {report['deploy_chain_status']}")
        print(f"Schema generator: {report['schema_generator_status']} (probe fastmcp_ext/*.py for Pydantic model)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
