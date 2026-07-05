#!/usr/bin/env python3
"""
constitutional_runner.py — CLI for the constitutional test suite.

Usage:
    python constitutional_runner.py all       # run the full suite via pytest
    python constitutional_runner.py list      # list test files + counts
    python constitutional_runner.py dry-run   # show pytest --collect-only output
    python constitutional_runner.py stage <N> # run tests for stage N (1-4)

Stage mapping:
    0.2 → test_drift_detection.py (identity anchor)
    1   → test_conformance_spine.py (harmonic IDs + invariants)
    2   → test_tool_proliferation_gate.py (TOOLCREATIONGATE 3-check)
    3   → test_identity_binding.py + test_bridging_seal_overrides.py
    e2e → test_conformance_spine.py::test_conformance_spine_e2e + test_well_freshness.py

Exit code = number of failed tests (0 = all-pass).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).parent
STAGE_FILES = {
    "0.2": ["test_drift_detection.py"],
    "1": ["test_conformance_spine.py"],
    "2": ["test_tool_proliferation_gate.py"],
    "3": ["test_identity_binding.py", "test_bridging_seal_overrides.py"],
    "e2e": ["test_conformance_spine.py", "test_well_freshness.py"],
}


def list_tests() -> int:
    print("Constitutional test files:")
    for f in sorted(HERE.glob("test_*.py")):
        size = f.stat().st_size
        n_lines = sum(1 for _ in f.open())
        print(f"  {f.name:<42} {n_lines:>4} lines  {size:>6} bytes")
    print(f"\nStage mapping:")
    for stage, files in STAGE_FILES.items():
        print(f"  stage {stage:<4} → {', '.join(files)}")
    return 0


def dry_run() -> int:
    rc = subprocess.call(
        ["python3", "-m", "pytest", str(HERE), "--collect-only", "-q"],
        cwd=str(HERE.parent.parent.parent),  # AAA root
    )
    return rc


def run_all() -> int:
    rc = subprocess.call(
        ["python3", "-m", "pytest", str(HERE), "-v"],
        cwd=str(HERE.parent.parent.parent),
    )
    return rc


def run_stage(stage: str) -> int:
    files = STAGE_FILES.get(stage)
    if not files:
        print(f"unknown stage {stage!r}. Available: {list(STAGE_FILES.keys())}")
        return 2
    paths = [str(HERE / f) for f in files]
    rc = subprocess.call(
        ["python3", "-m", "pytest", *paths, "-v"],
        cwd=str(HERE.parent.parent.parent),
    )
    return rc


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    cmd = sys.argv[1]
    if cmd == "list":
        return list_tests()
    if cmd == "dry-run":
        return dry_run()
    if cmd == "all":
        return run_all()
    if cmd == "stage":
        if len(sys.argv) < 3:
            print("usage: constitutional_runner.py stage <N>")
            return 1
        return run_stage(sys.argv[2])
    print(f"unknown command {cmd!r}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
