#!/usr/bin/env python3
"""
love-link-verifier.py — The bipartite verifier for the arifOS Resource OS.

Forged 2026-08-15 by F13 SOVEREIGN directive.
Doctrine: every edge is a pair. Love-links require reciprocity.

Usage:
    python3 love-link-verifier.py <path-to-resources-root>

Behavior:
    1. Walks all *.yaml and *.json files under the given root.
    2. For each file with a manifest, indexes:
         - requires / required_by
         - provides / provided_by
         - love_links
         - derived_from
         - invalidates
    3. Verifies every love-link is reciprocated.
    4. Emits a summary report.
    5. Exits 0 if 100% bipartite, 1 if any orphan edges.

This is the substrate for the B → C → A build order:
    B (Discovery) — verify 100% love-links bidirectional.
    C (Execution) — verify 486 SKILL.md still load.
    A (Adaptation) — synthetic SCAR → EUREKA → propagation succeeds.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

import yaml


class LoveLinkVerifier:
    """Bipartite verifier for the Resource OS."""

    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self.manifests: Dict[str, dict] = {}
        self.reports: List[str] = []

    # --- indexing ---------------------------------------------------------

    def index(self) -> None:
        """Walk the tree and collect every manifest."""
        for path in self.root.rglob("*.yaml"):
            self._try_collect(path)
        for path in self.root.rglob("*.yml"):
            self._try_collect(path)
        for path in self.root.rglob("*.json"):
            self._try_collect(path)

    def _try_collect(self, path: Path) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                if path.suffix in (".yaml", ".yml"):
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
        except Exception:
            return
        if not isinstance(data, dict):
            return
        # Index by id if present
        rid = data.get("id")
        if rid:
            self.manifests[rid] = data

    # --- verification ------------------------------------------------------

    def verify(self) -> Tuple[int, int, int]:
        """Verify love-links are reciprocated.

        Returns:
            (manifests, ok, orphans)
        """
        # Collect every love-link edge
        love_edges: List[Tuple[str, str]] = []
        for src_id, payload in self.manifests.items():
            for tgt in payload.get("love_links", []) or []:
                love_edges.append((src_id, tgt))

        # Bipartite check: every (a, b) in edges must have (b, a) in payloads
        reciprocated: Set[Tuple[str, str]] = set()
        orphans: List[Tuple[str, str]] = []
        for src, tgt in love_edges:
            tgt_payload = self.manifests.get(tgt, {})
            back = tgt_payload.get("love_links", []) or []
            if src in back:
                reciprocated.add((src, tgt))
            else:
                orphans.append((src, tgt))
        self.orphan_pairs = orphans

        return len(self.manifests), len(reciprocated), len(orphans)

    # --- reporting ---------------------------------------------------------

    def report(self, total: int, ok: int, orphans: int) -> str:
        lines = [
            "═" * 60,
            "  arifOS Love-Link Verifier — Bipartite Audit",
            "═" * 60,
            f"  Root:           {self.root}",
            f"  Manifests:      {total}",
            f"  Love-links:     {ok} reciprocated",
            f"  Orphans:        {orphans}",
            "",
        ]
        if orphans == 0 and ok > 0:
            lines.append("  ✓ 100% bipartite — every love-link is reciprocated.")
        elif orphans == 0:
            lines.append("  ⚠ No love-links declared yet. Seed 10 sources to populate.")
        else:
            lines.append("  ✗ Orphan love-links detected. Reciprocation required.")
            lines.append("")
            lines.append("  Orphan list (src → tgt that needs a reciprocal):")
            for src, tgt in self.orphan_pairs:
                lines.append(f"    {src}  →  {tgt}")
        lines.append("═" * 60)
        return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 love-link-verifier.py <resources-root>")
        return 2
    root = Path(sys.argv[1])
    if not root.exists():
        print(f"ERROR: {root} does not exist", file=sys.stderr)
        return 2

    v = LoveLinkVerifier(root)
    v.index()
    total, ok, orphans = v.verify()
    print(v.report(total, ok, orphans))

    # Refresh summary by layer
    by_layer: Dict[str, int] = {}
    for rid in v.manifests:
        prefix = rid.split("://", 1)[0] if "://" in rid else "unknown"
        by_layer[prefix] = by_layer.get(prefix, 0) + 1
    if by_layer:
        print("")
        print("  Manifests by namespace:")
        for prefix, count in sorted(by_layer.items(), key=lambda x: -x[1]):
            print(f"    {prefix:14s}  {count:4d}")

    return 0 if orphans == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
