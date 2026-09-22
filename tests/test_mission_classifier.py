"""
test_mission_classifier.py — P0 2026-09-21 (S6 federation-convergence).

Regression canaries for the mission classifier bug:

  Arif (F13): "Run semantic claim integrity and counterstory analysis
              using HERMES…" used to classify as MISSION=ACT because the
              classifier matched the word "run" alone.

  Fix: verb-object-compound matching (S6).
    "run an analysis"   → EXPLAIN (no external state change)
    "run tests"         → OBSERVE (read-only verification)
    "run deployment"    → ACT (external state change via "deploy"/"build"/"ship")

Constitutional:
    F2 TRUTH — every assertion cites the test case + expected mission
    F7 HUMILITY — confidence is bounded; classifier admits uncertainty
    F11 AUDIT — every assertion leaves evidence in stdout for receipt
"""

from __future__ import annotations

import sys
from pathlib import Path

# Import the router module directly
sys.path.insert(0, "/root/arifOS/arifosmcp")
from router import classify_intent, Mission  # noqa: E402

CANARIES = [
    # (intent, expected_mission, description)
    (
        "Run semantic claim integrity and counterstory analysis using HERMES",
        Mission.EXPLAIN,
        "Arif's directive: 'run semantic analysis' must NOT resolve to ACT",
    ),
    (
        "Run an analysis of the WEALTH capital_polix schema drift",
        Mission.EXPLAIN,
        "verb-object compound 'run an analysis' → EXPLAIN",
    ),
    (
        "Run the federation conformance tests",
        Mission.OBSERVE,
        "'run tests' is read-only verification, not mutation",
    ),
    (
        "Deploy the fix for the auth bug",
        Mission.ACT,
        "'deploy' is an explicit mutation verb → ACT",
    ),
    (
        "Build the A-FORGE mcp server",
        Mission.ACT,
        "'build' is an explicit mutation verb → ACT",
    ),
    (
        "Run the deployment pipeline",
        Mission.ACT,
        "'deployment' object noun resolves to ACT (deployment verb carries state change)",
    ),
    (
        "Why did the well test fail?",
        Mission.EXPLAIN,
        "Root cause inquiry → EXPLAIN (regression — must not regress)",
    ),
    (
        "What is happening with the VPS?",
        Mission.OBSERVE,
        "Status check → OBSERVE (regression)",
    ),
    (
        "Should we drill prospect Alpha?",
        Mission.DECIDE,
        "Decision inquiry → DECIDE (regression)",
    ),
    (
        "Watch the CPU and alert me if it exceeds 90%",
        Mission.MONITOR,
        "Watch directive → MONITOR (regression)",
    ),
    (
        "What did we decide about the Malay Basin prospect?",
        Mission.RECALL,
        "Memory recall → RECALL (regression)",
    ),
]


def _check(label, ok, detail=""):
    glyph = "✓" if ok else "✗"
    line = f"  {glyph} {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok


def main() -> int:
    print("=" * 70)
    print("FEDERATION E2E — mission classifier verb-object-statechange heuristic")
    print("  Test ID: P0-2026-09-21-S6")
    print("  Constitutional: F2 TRUTH + F7 HUMILITY + F11 AUDIT")
    print("=" * 70)

    all_ok = True
    print()
    for intent, expected, desc in CANARIES:
        got_mission, got_conf, got_triggers = classify_intent(intent)
        ok = got_mission == expected
        all_ok &= _check(
            f"{desc}",
            ok,
            f"got={got_mission.value} conf={got_conf} triggers={got_triggers[:2]}",
        )

    print()
    print("=" * 70)
    if all_ok:
        print("RESULT: PASS — mission classifier resolves verb-object correctly")
        return 0
    else:
        print("RESULT: FAIL — classifier still routes by single keyword")
        return 1


if __name__ == "__main__":
    sys.exit(main())
