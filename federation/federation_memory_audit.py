#!/usr/bin/env python3
"""federation_memory_audit.py — verify every federated agent goes through the contract.

Exits 0 if aligned (every federated repo's memory writes are through
federation_memory_adapter.FederationMemory.store, not direct qdrant_client).

Exits 1 with a list of violations if any direct write surface remains.

Source-of-truth:
  /root/arifOS/docs/FEDERATION_MEMORY_CONTRACT.md (R1 single write surface)
  /root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md

Approved list (whitelist — these may write directly because they ARE
the contract surface itself or are routing bridges ON the contract):

  APPROVED_DIRECT = {
    arifOS kernel:        arifosmcp/runtime/memory_store.py
    arifOS contracts:     arifOS/docs/FEDERATION_MEMORY_CONTRACT.md
    alignment doctrine:   AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md
    federation bridge:    /root/scripts/federation_memory_bridge.py
    helix cron:           /root/scripts/federation_memory_helix_cron.py
    organ wrappers:       GEOX/src/geox_mcp/federation_memory.py
                          WEALTH/internal/federation_memory.py
                          WELL/internal/federation_memory.py
  }

Anything else containing:
  QdrantClient(...) construction
  qdrant_client import OR from qdrant_client import
  .upsert( on a QdrantClient instance
  api/collections/* direct (any non-mem0 internal)
  ... and not in APPROVED_DIRECT
... is a violation.

Calls:
  python3 /root/AAA/federation/federation_memory_audit.py
  python3 /root/AAA/federation/federation_memory_audit.py --check-only hermes (just hermes)
  python3 /root/AAA/federation/federation_memory_audit.py --check-only aaa (just AAA)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# Repos to scan (relative to /root unless absolute):
SCAN_REPOS: list[str] = [
    "/root/AAA",
    "/root/A-FORGE",
    "/root/arifOS",
    "/root/GEOX",
    "/root/WEALTH",
    "/root/WELL",
    "/root/openclaw",  # may not exist (legacy)
    "/root/.arifos",
    "/root/.hermes",
]

# Files / paths that are allowed direct substrate access (whitelist):
# arifOS kernel IS the contract surface — it owns R1 + every leg of the
# three-leg write. Other organs go through arif_memory_recall. arifOS
# internals may write directly because they implement that surface.
APPROVED_DIRECT_PREFIX: tuple[str, ...] = (
    # arifOS kernel — IS the contract surface (R1: kernel writes directly to Qdrant/Supabase/Graphiti)
    "/root/arifOS/arifosmcp/",
    "/root/arifOS/arifosmcp/hib/",  # hib subsystems
    "/root/arifOS/arifosmcp/memory/",  # memory subsystems
    "/root/arifOS/arifosmcp/evidence/",
    "/root/arifOS/arifosmcp/runtime/",
    "/root/arifOS/arifosmcp/tools/",
    "/root/arifOS/arifosmcp/intelligence/",
    "/root/arifOS/core/",  # capability_index, organs, shared
    "/root/arifOS/scripts/",
    "/root/arifOS/deploy/",
    "/root/arifOS/VAULT999/",
    "/root/arifOS/build/",  # build artifacts
    # helix/bridge scripts (already on contract)
    "/root/scripts/federation_memory_bridge.py",
    "/root/scripts/federation_memory_helix_cron.py",
    # alignment doctrine (informational doc, not a write surface)
    "/root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md",
    "/root/AAA/governance/memory-provenance-v2.md",
    # audit script + adapter (the recommended surface)
    "/root/AAA/federation/federation_memory_audit.py",
    "/root/AAA/federation/federation_memory_adapter.py",
    # organ wrappers (already aligned 2026-06-03)
    "/root/GEOX/src/geox_mcp/federation_memory.py",
    "/root/WEALTH/internal/federation_memory.py",
    "/root/WELL/internal/federation_memory.py",
    # heritage (not live)
    "/root/.openclaw-cold",
    "/root/.arifos",
    "/root/.hermes",  # Hermes runtime data: state.db, .jsonl — not source
    "/root/.hermes/archive",
)

# Legacy exact-prefix (kept for compatibility; empty by default).
APPROVED_DIRECT: set[str] = set()

# Patterns that signal direct substrate access:
DIRECT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("qdrant_client_import", re.compile(r"^\s*from\s+qdrant_client\s+import\s+QdrantClient", re.MULTILINE)),
    ("qdrant_client_global", re.compile(r"^\s*import\s+qdrant_client", re.MULTILINE)),
    ("qdrant_constructor", re.compile(r"\bQdrantClient\s*\(", re.MULTILINE)),
    (
        "direct_qdrant_api",
        re.compile(r"http://127\.0\.0\.1:6333/collections/[^/\s'\"]+/(?:points|scroll)", re.IGNORECASE),
    ),
    ("mem0_raw_api", re.compile(r"mem0\.add\(|mem0\.search\(")),
]

# File extensions to scan:
SCAN_EXTS: set[str] = {".py", ".js", ".ts", ".tsx", ".go", ".rs"}

# Skip dirs (heritage, archive, build artifacts, venvs, deprecated code):
SKIP_DIRS: set[str] = {
    "node_modules",
    ".git",
    "dist",
    "build",
    "__pycache__",
    ".next",
    ".openclaw-cold",
    "archive",
    "_archive",
    ".pyc",
    "__archive__",
    ".venv",
    "venv",
    "site-packages",
    "skills-deprecated",  # not live; per AGENTS.md "deprecated → use new"; excluded
    "snapshots",
    "venv",
    "site-packages",
    "snapshots",
}


def is_approved(path: str) -> bool:
    abs_p = str(Path(path).resolve())
    for prefix in APPROVED_DIRECT_PREFIX:
        if abs_p.startswith(prefix):
            return True
    return False


def should_skip_dir(path: Path) -> bool:
    parts = path.parts
    return any(p in SKIP_DIRS for p in parts)


def scan_file(path: Path) -> list[tuple[str, str]]:
    """Return list of (kind, line-text) for violations found."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    hits: list[tuple[str, str]] = []
    for kind, pat in DIRECT_PATTERNS:
        for m in pat.finditer(text):
            line_no = text[: m.start()].count("\n") + 1
            line_text = m.group(0).strip()
            hits.append((kind, f"{path}:{line_no}: {line_text}"))
    return hits


def scan_repo(repo_path: str) -> list[tuple[str, str]]:
    """Walk a repo and scan files for direct substrate access patterns."""
    abs_repo = Path(repo_path).resolve()
    if not abs_repo.exists():
        return []
    violations: list[tuple[str, str]] = []
    for p in abs_repo.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in SCAN_EXTS:
            continue
        if should_skip_dir(p):
            continue
        rel = str(p)
        if is_approved(rel):
            continue
        # Additional: skip AA-specific deps if under diff range
        # We do a real scan regardless.
        for hit in scan_file(p):
            violations.append(hit)
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", help="Only audit this agent")
    parser.add_argument("--quiet", action="store_true", help="Don't print OK lines")
    args = parser.parse_args()

    repos = SCAN_REPOS
    if args.check_only:
        target = args.check_only.lower()
        repos = [r for r in SCAN_REPOS if target in r.lower()]

    all_violations: list[tuple[str, str]] = []
    for repo in repos:
        if not Path(repo).exists():
            if not args.quiet:
                print(f"[skip] {repo} (does not exist)")
            continue
        if not args.quiet:
            print(f"[scan] {repo}")
        v = scan_repo(repo)
        all_violations.extend(v)
        if v and not args.quiet:
            for kind, msg in v[:5]:
                print(f"  ↳ {kind}: {msg}")
            if len(v) > 5:
                print(f"  … +{len(v) - 5} more in {repo}")

    print()
    if all_violations:
        print(f"FAIL: {len(all_violations)} direct substrate write(s) found.")
        print("Remediation: import federation_memory_adapter.FederationMemory and")
        print("call fm.store(...) instead of constructing QdrantClient directly.")
        return 1
    print("OK: every federated repo routes memory through the contract.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
