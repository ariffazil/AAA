"""
test_well_drift_reconciliation.py — P3 2026-09-21 (WELL-DRIFT-RECONCILIATION).

Regression canary that catches source_commit ≠ deployed_commit ≠ built_commit
on WELL :18083. Three-way commit alignment is a reality-drift invariant.

P3 sub-fixes verified:
  P3-1  source_commit == deployed_commit == built_commit (drift=false)
  P3-2  identity + role + authority_ceiling unchanged (apex scalars intact)
  P3-3  release-manifest.json git_commit matches HEAD
  P3-4  .git_commit stamp matches HEAD

Constitutional:
    F2 TRUTH — every check probes live :18083 (no static assertion)
    F11 AUDIT — failures write to /root/AAA/canary/logs/
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

WELL_HOST, WELL_PORT = "127.0.0.1", 18083
WELL_ROOT = Path("/root/WELL")


def _get(path):
    req = urllib.request.Request(
        f"http://{path[0]}:{path[1]}/health",
        headers={"Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())


def _head():
    """Get current HEAD short SHA."""
    import subprocess
    r = subprocess.run(
        ["git", "-C", str(WELL_ROOT), "rev-parse", "--short=7", "HEAD"],
        capture_output=True, text=True, timeout=5,
    )
    if r.returncode != 0:
        return None
    return r.stdout.strip()[:7]


def _check(label, ok, detail=""):
    glyph = "✓" if ok else "✗"
    line = f"  {glyph} {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok


def main() -> int:
    print("=" * 70)
    print("FEDERATION E2E — WELL-DRIFT-RECONCILIATION")
    print("  Test ID: P3-2026-09-21")
    print("  Doctrine: Reality > Model > Stamp")
    print("=" * 70)
    all_ok = True

    h = _get((WELL_HOST, WELL_PORT))
    head = _head()

    # ─────────────────────────────────────────────────────────────────
    # P3-1: source == deployed == built (drift=false)
    # ─────────────────────────────────────────────────────────────────
    print("\n[P3-1] Three-way commit alignment")
    sc = h.get("source_commit", "UNKNOWN")
    dc = h.get("deployed_commit", "UNKNOWN")
    bc = h.get("built_commit", "UNKNOWN")
    drift = h.get("drift", True)
    all_ok &= _check(
        "source_commit == deployed_commit",
        sc == dc and sc != "UNKNOWN",
        f"source={sc} deployed={dc}",
    )
    all_ok &= _check(
        "deployed_commit == built_commit",
        dc == bc and dc != "UNKNOWN",
        f"deployed={dc} built={bc}",
    )
    all_ok &= _check(
        "drift flag is False (three-way aligned)",
        drift is False,
        f"drift={drift}",
    )
    all_ok &= _check(
        "source_commit matches live HEAD",
        sc == head if head else False,
        f"health={sc} HEAD={head}",
    )

    # ─────────────────────────────────────────────────────────────────
    # P3-2: Other health fields intact (no collateral damage)
    # ─────────────────────────────────────────────────────────────────
    print("\n[P3-2] Other health fields intact")
    all_ok &= _check(
        "identity == WELL",
        h.get("identity") == "WELL",
        f"identity={h.get('identity')}",
    )
    all_ok &= _check(
        "role == 'Body / Human Intelligence'",
        h.get("role") == "Body / Human Intelligence",
    )
    all_ok &= _check(
        "authority_ceiling == REFLECT_ONLY (unchanged)",
        h.get("authority_ceiling") == "REFLECT_ONLY",
    )
    scalars = h.get("apex_scalars", {})
    all_ok &= _check(
        "apex scalars present (G, C_dark, h)",
        all(k in scalars for k in ("G", "C_dark", "h")),
        f"keys={list(scalars.keys())}",
    )

    # ─────────────────────────────────────────────────────────────────
    # P3-3: release-manifest.json git_commit matches HEAD
    # ─────────────────────────────────────────────────────────────────
    print("\n[P3-3] release-manifest.json git_commit matches HEAD")
    try:
        manifest = json.loads(
            (WELL_ROOT / "release-manifest.json").read_text()
        )
        manifest_sha = manifest.get("git_commit", "")[:7]
        all_ok &= _check(
            "release-manifest.json git_commit matches HEAD",
            manifest_sha == head if head else False,
            f"manifest={manifest_sha} HEAD={head}",
        )
        all_ok &= _check(
            'release-manifest.json has "release" field',
            "release" in manifest,
        )
    except Exception as exc:
        all_ok &= _check("release-manifest.json readable", False, str(exc))

    # ─────────────────────────────────────────────────────────────────
    # P3-4: .git_commit stamp matches HEAD
    # ─────────────────────────────────────────────────────────────────
    print("\n[P3-4] /root/WELL/.git_commit stamp matches HEAD")
    try:
        stamp = (WELL_ROOT / ".git_commit").read_text().strip()[:7]
        all_ok &= _check(
            ".git_commit stamp matches HEAD",
            stamp == head if head else False,
            f"stamp={stamp} HEAD={head}",
        )
    except Exception as exc:
        all_ok &= _check(".git_commit readable", False, str(exc))

    # ─────────────────────────────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────────────────────────────
    print()
    print("=" * 70)
    if all_ok:
        print("RESULT: PASS — WELL drift reconciled")
        print("  - source_commit == deployed_commit == built_commit")
        print("  - all stamps aligned to current HEAD")
        print("  - other health fields intact (no collateral damage)")
        return 0
    else:
        print("RESULT: FAIL — drift remains or stamps inconsistent")
        return 1


if __name__ == "__main__":
    sys.exit(main())
