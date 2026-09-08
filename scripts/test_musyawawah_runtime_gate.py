#!/usr/bin/env python3
"""Falsification tests for musyawawah_runtime_gate reference impl — Phase A3/A4.

8 scenarios covering the decision tree (Phase A3 = write, Phase A4 = run):

  T1: T0 baseline (OBSERVE_ONLY)           → ALLOW (no musyawawah)
  T2: T1 baseline (EXECUTE_REVERSIBLE)     → ALLOW (no musyawawah)
  T3: T2 with valid musyawawah_reference   → ALLOW
  T4: T2 with invalid format               → DENY (fail-closed)
  T5: T2 with no musyawawah_reference      → DENY (fail-closed)
  T6: T2 with F13 override                  → ALLOW_BYPASS (logged)
  T7: T3 SEAL with valid reference          → ALLOW
  T8: T3 SEAL no reference                 → DENY (fail-closed)

Failure modes tested (Phase A5 evidence):
  F1: empty string reference                → DENY (not crash)
  F2: non-string reference                  → DENY (type-check)
  F3: path traversal (..)                   → DENY (regex rejects)
  F4: future-dated reference                → ALLOW (no expiration in Phase A)

DITEMPA BUKAN DIBERI — Phase A3, 2026-09-08 by FI-003.
"""
import importlib.util
import sys
from pathlib import Path

# Dynamic import (path resolution for Unicode lookalike safety)
GATE_CANDIDATES = [
    Path("/root/AAA/scripts/musyawawah_runtime_gate.py"),
]
GATE = next((p for p in GATE_CANDIDATES if p.is_file()), None)
if GATE is None:
    import glob
    matches = glob.glob("/root/AAA/scripts/musyaw*runtime_gate.py")
    matches = [m for m in matches if "test" not in m]
    if matches:
        GATE = Path(matches[0])
if GATE is None:
    print("ERROR: musyawawah_runtime_gate.py not found", file=sys.stderr)
    sys.exit(2)

spec = importlib.util.spec_from_file_location("musyawawah_runtime_gate", GATE)
gate = importlib.util.module_from_spec(spec)
sys.modules["musyawawah_runtime_gate"] = gate  # register before exec so @dataclass can resolve module
spec.loader.exec_module(gate)

from musyawawah_runtime_gate import (  # noqa: E402
    ActionClass,
    InvocationContext,
    Verdict,
    check_with_log,
)


def case(label: str, ctx, expected_verdict: Verdict) -> tuple:
    v, r = check_with_log(ctx)
    passed = (v == expected_verdict)
    return passed, label, v.value, r


# ── 8 main scenarios ──

SCENARIOS = [
    # (label, context, expected)
    ("T1: T0 baseline (OBSERVE_ONLY)",
     InvocationContext(action_class=ActionClass.OBSERVE_ONLY),
     Verdict.ALLOW),

    ("T2: T1 baseline (EXECUTE_REVERSIBLE)",
     InvocationContext(action_class=ActionClass.EXECUTE_REVERSIBLE),
     Verdict.ALLOW),

    ("T3: T2 with valid musyawawah_reference",
     InvocationContext(
         action_class=ActionClass.EXECUTE_HIGH_IMPACT,
         musyawawah_reference="musyawawah/2026-09-08-no-gate-task6/CONVERGENCE.md",
     ),
     Verdict.ALLOW),

    ("T4: T2 with invalid format",
     InvocationContext(
         action_class=ActionClass.EXECUTE_HIGH_IMPACT,
         musyawawah_reference="malicious-ref",
     ),
     Verdict.DENY),

    ("T5: T2 with no musyawawah_reference",
     InvocationContext(
         action_class=ActionClass.EXECUTE_HIGH_IMPACT,
     ),
     Verdict.DENY),

    ("T6: T2 with F13 override (ack_irreversible)",
     InvocationContext(
         action_class=ActionClass.EXECUTE_HIGH_IMPACT,
         ack_irreversible=True,
     ),
     Verdict.ALLOW_BYPASS),

    ("T7: T3 SEAL with valid reference",
     InvocationContext(
         action_class=ActionClass.SEAL,
         musyawawah_reference="musyawawah/2026-09-08-no-gate-task6/CONVERGENCE.md",
     ),
     Verdict.ALLOW),

    ("T8: T3 SEAL no reference",
     InvocationContext(action_class=ActionClass.SEAL),
     Verdict.DENY),
]


# ── Failure modes (Phase A5) ──

FAILURE_MODES = [
    ("F1: empty string reference",
     InvocationContext(
         action_class=ActionClass.EXECUTE_HIGH_IMPACT,
         musyawawah_reference="",
     ),
     Verdict.DENY),

    ("F2: None reference (omitted)",
     InvocationContext(action_class=ActionClass.EXECUTE_HIGH_IMPACT),
     Verdict.DENY),

    ("F3: path traversal attempt",
     InvocationContext(
         action_class=ActionClass.SEAL,
         musyawawah_reference="musyawawah/../../../etc/passwd",
     ),
     Verdict.DENY),

    ("F4: future-dated reference (no expiration in Phase A)",
     InvocationContext(
         action_class=ActionClass.EXECUTE_HIGH_IMPACT,
         musyawawah_reference="musyawawah/2099-12-31-future-task/CONVERGENCE.md",
     ),
     Verdict.ALLOW),  # structural check passes — semantic check is Path B
]


def main() -> None:
    args = sys.argv[1:]
    selected_label = None
    if "--only" in args:
        selected_label = args[args.index("--only") + 1]

    selected = []
    if selected_label:
        selected = [
            (label, ctx, expected)
            for (label, ctx, expected) in SCENARIOS + FAILURE_MODES
            if selected_label in label
        ]
    else:
        selected = SCENARIOS + FAILURE_MODES

    failures = []
    for label, ctx, expected in selected:
        passed, label, verdict, reason = case(label, ctx, expected)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {label}  →  {verdict}")
        if not passed:
            failures.append((label, verdict, reason))
            print(f"       expected: {expected.value}")
            print(f"       reason:   {reason[:120]}")

    print()
    if failures:
        print(f"=== {len(failures)} FAILURE(S) ===")
        for label, v, r in failures:
            print(f"  - {label}: got={v} reason={r[:100]}")
        sys.exit(1)
    print(f"=== ALL {len(selected)} SCENARIOS PASSED ===")


if __name__ == "__main__":
    main()
