#!/usr/bin/env python3
"""Falsification tests for musyawawah_gate.py — A2 amendment from CONVERGENCE.

5 scenarios (3 sentinel-testable + 2 noted as sentinel-skipped):

  T1: T2/Execute without musyawawah_reference (post-grace) → expect exit 1
  T2: T3/Seal without musyawawah_reference (post-grace)    → expect exit 1
  T3: T2/Execute WITH musyawawah_reference                  → expect exit 0
  T4: T2/Execute pre-grace (legacy exempt)                  → expect exit 0
  T5: T0/Verify (not T2/T3)                                 → expect exit 0

Scenarios noted as sentinel-skipped (require runtime gate, not sentinel):
  R3: override ack_irreversible=True → ALLOW + log (runtime)
  R4: VAULT999 unavailable → DENY fail-closed (runtime)

Usage:
  test_musyawawah_gate.py    run all scenarios
  test_musyawawah_gate.py --scenario T1   run one scenario
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GATE_CANDIDATES = [Path("/root/AAA/scripts/musyawarah_gate.py")]
GATE = next((p for p in GATE_CANDIDATES if p.is_file()), None)
if GATE is None:
    import glob
    matches = [m for m in glob.glob("/root/AAA/scripts/*musyaw*_gate.py") if "test" not in m]
    if matches:
        GATE = Path(matches[0])
if GATE is None:
    print("ERROR: gate script not found", file=__import__("sys").stderr)
    __import__("sys").exit(2)
GRACE = "2026-09-08"


def make_receipt(step_type: str, has_ref: bool, date: str, receipt_id: str = "test-001") -> dict:
    payload = {"allow_heavy": True, "phase": "test"} if not has_ref else {
        "allow_heavy": True,
        "phase": "test",
        "musyawawah_reference": f"musyawarah/{date}/{receipt_id}",
    }
    return {
        "receipt_id": receipt_id,
        "actor_id": "test-actor",
        "session_id": "test-session",
        "step_type": step_type,
        "created_at": f"{date}T11:00:00.000000Z",
        "epistemic_label": "Observation",
        "floor_verdict": "Pass",
        "payload": payload,
    }


def write_fixture(receipts: list) -> Path:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
    for r in receipts:
        f.write(json.dumps(r) + "\n")
    f.close()
    return Path(f.name)


def run_gate(fixture_path: Path, since: str = GRACE) -> tuple:
    """Returns (exit_code, stdout, stderr)."""
    result = subprocess.run(
        ["python3", str(GATE), "--path", str(fixture_path), "--since", since],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


# ── Scenario definitions ──

def scenario_T1_no_ref_post_grace() -> tuple:
    """T2/Execute, no musyawawah_reference, post-grace → expect exit 1."""
    r = make_receipt("Execute", has_ref=False, date="2026-09-08")
    fix = write_fixture([r])
    code, _, stderr = run_gate(fix)
    fix.unlink()
    return code != 0, code, stderr, "T1: T2/Execute no-ref post-grace"


def scenario_T2_seal_no_ref_post_grace() -> tuple:
    """T3/Seal, no musyawawah_reference, post-grace → expect exit 1."""
    r = make_receipt("Seal", has_ref=False, date="2026-09-09", receipt_id="test-seal-1")
    fix = write_fixture([r])
    code, _, stderr = run_gate(fix)
    fix.unlink()
    return code != 0, code, stderr, "T2: T3/Seal no-ref post-grace"


def scenario_T3_with_ref() -> tuple:
    """T2/Execute WITH musyawawah_reference → expect exit 0."""
    r = make_receipt("Execute", has_ref=True, date="2026-09-09", receipt_id="test-good-1")
    fix = write_fixture([r])
    code, _, stderr = run_gate(fix)
    fix.unlink()
    return code == 0, code, stderr, "T3: T2/Execute WITH ref"


def scenario_T4_legacy_pre_grace() -> tuple:
    """Pre-grace receipt (legacy exempt) → expect exit 0."""
    r = make_receipt("Execute", has_ref=False, date="2026-08-15", receipt_id="test-legacy-1")
    fix = write_fixture([r])
    code, _, stderr = run_gate(fix)
    fix.unlink()
    return code == 0, code, stderr, "T4: T2/Execute pre-grace (exempt)"


def scenario_T5_T0_not_in_scope() -> tuple:
    """T0/Verify is not T2/T3 → expect exit 0 (skipped, no violation)."""
    r = make_receipt("Verify", has_ref=False, date="2026-09-09", receipt_id="test-verify-1")
    fix = write_fixture([r])
    code, _, stderr = run_gate(fix)
    fix.unlink()
    return code == 0, code, stderr, "T5: T0/Verify out-of-scope"


SCENARIOS = [
    scenario_T1_no_ref_post_grace,
    scenario_T2_seal_no_ref_post_grace,
    scenario_T3_with_ref,
    scenario_T4_legacy_pre_grace,
    scenario_T5_T0_not_in_scope,
]


def main() -> None:
    args = sys.argv[1:]
    selected = None
    if "--scenario" in args:
        selected = [s for s in SCENARIOS if s.__name__.startswith(args[args.index("--scenario") + 1])]
    else:
        selected = SCENARIOS

    failures = []
    for scen in selected:
        passed, code, stderr, label = scen()
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {label} (exit={code})")
        if not passed:
            failures.append((label, stderr.strip()))
            print(f"       stderr: {stderr.strip()[:200]}")

    print()
    if failures:
        print(f"=== {len(failures)} FAILURE(S) ===")
        for label, err in failures:
            print(f"  - {label}: {err[:120]}")
        sys.exit(1)
    print(f"=== ALL {len(selected)} SCENARIOS PASSED ===")


if __name__ == "__main__":
    main()
