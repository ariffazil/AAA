#!/usr/bin/env python3
"""
run_all.py — F1–F13 Floor Benchmark Runner
=============================================

Runs all floor test files via pytest and aggregates results into
``results/aggregate.json``.

Usage:
    python benchmarks/floors/run_all.py
    python benchmarks/floors/run_all.py --verbose
    python benchmarks/floors/run_all.py --floor F01_reversibility
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import pytest

RESULTS_DIR = Path(__file__).resolve().parent / "results"

# All floor test modules in dependency order
FLOOR_MODULES = [
    "F01_reversibility",
    "F02_truth",
    "F03_tri_witness",
    "F04_clarity",
    "F05_peace",
    "F06_empathy",
    "F07_humility",
    "F08_genius",
    "F09_antihantu",
    "F10_ontology",
    "F11_auditability",
    "F12_resilience",
    "F13_sovereign",
    "F_multi_floor",
]

FLOOR_NAMES = {
    "F01_reversibility": "F1 AMANAH",
    "F02_truth": "F2 TRUTH",
    "F03_tri_witness": "F3 TRI-WITNESS",
    "F04_clarity": "F4 CLARITY",
    "F05_peace": "F5 PEACE",
    "F06_empathy": "F6 EMPATHY",
    "F07_humility": "F7 HUMILITY",
    "F08_genius": "F8 GENIUS",
    "F09_antihantu": "F9 ANTI-HANTU",
    "F10_ontology": "F10 ONTOLOGY",
    "F11_auditability": "F11 AUDITABILITY",
    "F12_resilience": "F12 RESILIENCE",
    "F13_sovereign": "F13 SOVEREIGN",
    "F_multi_floor": "MULTI-FLOOR",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="F1–F13 Floor Benchmark Runner",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose pytest output",
    )
    parser.add_argument(
        "--floor", "-f",
        type=str,
        default=None,
        help="Run a single floor (e.g. F01_reversibility)",
    )
    parser.add_argument(
        "--skip-unavailable", "-s",
        action="store_true",
        default=True,
        help="Skip floors where kernel is unavailable (default: True)",
    )
    parser.add_argument(
        "--fail-fast", "-x",
        action="store_true",
        help="Stop on first failure",
    )
    return parser.parse_args()


def load_floor_results(floor: str) -> dict[str, Any] | None:
    """Load the per-floor result file if it exists."""
    path = RESULTS_DIR / f"{floor}_results.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def aggregate_results() -> dict[str, Any]:
    """Aggregate all individual floor results into a single report."""
    all_floors = []
    total_tests = 0
    total_passed = 0
    total_failed = 0
    floor_summaries = []

    for floor in FLOOR_MODULES:
        data = load_floor_results(floor)
        if data is None:
            floor_summaries.append({
                "floor": floor,
                "name": FLOOR_NAMES.get(floor, floor),
                "status": "NOT_RUN",
                "total": 0,
                "passed": 0,
                "failed": 0,
                "pass_rate": 0.0,
            })
            continue

        results = data.get("results", [])
        summary = data.get("summary", {})
        t = summary.get("total", len(results))
        p = summary.get("passed", 0)
        f = summary.get("failed", 0)

        total_tests += t
        total_passed += p
        total_failed += f

        floor_summaries.append({
            "floor": floor,
            "name": FLOOR_NAMES.get(floor, floor),
            "status": "PASS" if f == 0 else "FAIL",
            "total": t,
            "passed": p,
            "failed": f,
            "pass_rate": summary.get("pass_rate", round(p / t * 100, 1) if t else 0.0),
            "tests": [
                {
                    "test_id": r["test_id"],
                    "description": r["description"],
                    "expected_verdict": r["expected_verdict"],
                    "actual_verdict": r["actual_verdict"],
                    "passed": r["passed"],
                }
                for r in results
            ],
        })
        all_floors.extend(results)

    overall_pass_rate = round(total_passed / total_tests * 100, 1) if total_tests else 0.0

    return {
        "meta": {
            "suite": "F1–F13 Constitutional Floor Benchmarks",
            "version": "v2026.06.14",
            "forged_by": "FORGE-000Ω",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "overall_pass_rate": overall_pass_rate,
            "floors_run": len([s for s in floor_summaries if s["status"] != "NOT_RUN"]),
            "floors_total": len(FLOOR_MODULES),
        },
        "floor_summaries": floor_summaries,
        "all_results": all_floors,
    }


def print_report(aggregate: dict[str, Any]) -> None:
    """Print a human-readable summary to stdout."""
    meta = aggregate["meta"]
    print("=" * 70)
    print(f"  F1–F13 Floor Benchmark Aggregate Report")
    print(f"  {meta['suite']}")
    print(f"  Forged: {meta['timestamp']}  |  Version: {meta['version']}")
    print("=" * 70)
    print(f"\n  Overall: {meta['total_passed']}/{meta['total_tests']} passed "
          f"({meta['overall_pass_rate']}%)")
    print(f"  Floors: {meta['floors_run']}/{meta['floors_total']} executed\n")
    print("-" * 70)
    print(f"  {'Floor':<22} {'Tests':>6} {'Passed':>7} {'Failed':>7} {'Rate':>7}  Status")
    print("-" * 70)

    for f in aggregate["floor_summaries"]:
        status = f["status"]
        status_icon = "✅" if status == "PASS" else ("❌" if status == "FAIL" else "⏭️")
        print(f"  {f['name']:<22} {f['total']:>6} {f['passed']:>7} "
              f"{f['failed']:>7} {f['pass_rate']:>6.1f}%  {status_icon} {status}")

    print("-" * 70)
    print(f"\n  Results directory: {RESULTS_DIR}")
    print(f"  Aggregate JSON:   {RESULTS_DIR / 'aggregate.json'}")
    print()


def main() -> int:
    args = parse_args()

    # Ensure results directory
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Build pytest arguments
    pytest_args = [
        str(Path(__file__).resolve().parent),
        "--tb=short",
        "--no-header",
        "-q",
    ]

    if args.verbose:
        pytest_args.remove("-q")
        pytest_args.append("-v")

    if args.fail_fast:
        pytest_args.append("-x")

    if args.floor:
        # Run a single floor file
        floor_file = Path(__file__).resolve().parent / f"{args.floor}.py"
        if not floor_file.exists():
            print(f"ERROR: Floor file not found: {floor_file}", file=sys.stderr)
            return 1
        pytest_args = [str(floor_file)] + [a for a in pytest_args if a != str(Path(__file__).resolve().parent)]
        if args.verbose:
            print(f"Running single floor: {args.floor}")

    # Run pytest
    exit_code = pytest.main(pytest_args)

    # Aggregate results
    aggregate = aggregate_results()
    agg_path = RESULTS_DIR / "aggregate.json"
    with open(agg_path, "w") as f:
        json.dump(aggregate, f, indent=2, default=str)

    print_report(aggregate)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
