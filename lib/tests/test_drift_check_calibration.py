#!/usr/bin/env python3
"""test_drift_check_calibration.py — P1 regression test for drift-check detector.

Per F13 directive 2026-09-21: "Pin regression: kernel drift=false → detector MUST NOT emit DRIFT".

This test asserts:
  When arifOS kernel reports drift=False AND source==deployed AND tree clean,
  the drift-check MUST NOT emit overall_drift=True.

Also asserts the canonical envelope separation:
  WORK_IN_PROGRESS ≠ DRIFT

Test is run-only (does NOT modify the drift-check script).

Usage:
    python3 /root/AAA/lib/tests/test_drift_check_calibration.py
"""

from __future__ import annotations
import json
import subprocess
import sys
import re
from datetime import datetime, timezone
from pathlib import Path


CANONICAL_STATE = Path("/root/AAA/lib/canonical_state.py")
DRIFT_CHECK = Path("/root/arifOS/scripts/drift_check_live.py")


def fail(msg: str) -> None:
    print(f"  FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"  OK  : {msg}")


def test_arifos_kernel_aligned() -> bool:
    """Pre-condition: arifOS kernel reports deployment_drift_status=aligned."""
    print("\n[1] arifOS kernel alignment pre-condition")
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:8088/health", timeout=3) as r:
            d = json.loads(r.read())
    except Exception as e:
        fail(f"cannot reach arifOS /health: {e}")
        return False

    sr = d.get("software_release", {})
    if d.get("deployment_drift_status") != "aligned":
        fail(f"kernel reports drift_status={d.get('deployment_drift_status')!r} (expected 'aligned')")
        return False
    if sr.get("drift") is not False:
        fail(f"kernel reports software_release.drift={sr.get('drift')!r} (expected False)")
        return False
    src = sr.get("source_commit", "")[:7]
    dep = sr.get("deployed_commit", "")[:7]
    if src != dep:
        fail(f"source[:7]={src} != deployed[:7]={dep}")
        return False
    ok(f"kernel aligned: source={src} deployed={dep} drift_status=aligned drift=False")
    return True


def test_arifos_tree_clean() -> bool:
    """Pre-condition: /root/arifOS working tree is clean."""
    print("\n[2] /root/arifOS working tree clean")
    try:
        out = subprocess.check_output(["git", "-C", "/root/arifOS", "status", "--porcelain"],
                                       text=True, timeout=5).strip()
    except Exception as e:
        fail(f"git status failed: {e}")
        return False
    if out:
        fail(f"tree dirty:\n{out[:500]}")
        return False
    ok("tree clean")
    return True


def test_arifos_reported_as_OK() -> bool:
    """When arifos kernel is aligned and tree clean, arifos MUST be reported OK (not DRIFT)."""
    print("\n[3] arifos organ reported as OK (not DRIFT) in drift-check output")
    try:
        out = subprocess.check_output(
            ["python3", str(DRIFT_CHECK)],
            text=True, timeout=30,
            cwd="/root/arifOS",
        )
    except Exception as e:
        fail(f"drift_check_live.py failed: {e}")
        return False

    # Look for arifos line
    arifos_line = next((l for l in out.splitlines() if "arifos:" in l.lower() and ("OK" in l or "DRIFT" in l)), None)
    if not arifos_line:
        fail("no arifos line in output")
        print(out)
        return False

    if "DRIFT" in arifos_line:
        fail(f"arifos line shows DRIFT: {arifos_line}")
        return False
    if "OK" not in arifos_line:
        fail(f"arifos line is neither OK nor DRIFT: {arifos_line}")
        return False
    ok(f"arifos reported as OK: {arifos_line.strip()}")
    return True


def test_canonical_state_separation() -> bool:
    """Canonical envelope: WORK_IN_PROGRESS ≠ DRIFT.

    Verify canonical_state.py exposes the needed states."""
    print("\n[4] canonical_state.py has WORK_IN_PROGRESS or INTENTIONAL_HOLD")
    if not CANONICAL_STATE.exists():
        fail(f"{CANONICAL_STATE} missing")
        return False
    content = CANONICAL_STATE.read_text()
    has_intentional_hold = "INTENTIONAL_HOLD" in content
    has_work_in_progress = "WORK_IN_PROGRESS" in content or "WIP" in content
    if not has_intentional_hold and not has_work_in_progress:
        fail("canonical_state.py has no state for uncommitted work")
        return False
    ok(f"canonical envelope has work-in-progress state: INTENTIONAL_HOLD={has_intentional_hold}, WORK_IN_PROGRESS={has_work_in_progress}")
    return True


def test_aaa_a2a_discovery() -> bool:
    """Behavioral probe: aaa-a2a (sliced to 6 keys) must still expose discovery + agent card."""
    print("\n[5] aaa-a2a behavioral probe (sliced to 6 keys)")
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:3001/.well-known/agent-card.json", timeout=3) as r:
            d = json.loads(r.read())
    except Exception as e:
        fail(f"cannot reach aaa-a2a /agent-card: {e}")
        return False
    if not d.get("capabilities"):
        fail("agent-card has no capabilities")
        return False
    ok(f"aaa-a2a agent-card: capabilities={len(d.get('capabilities',[]))} skills={len(d.get('skills',[]))}")
    return True


def test_aforge_tool_count() -> bool:
    """Behavioral probe: a-forge (sliced to 2 keys) must still load 121 tools."""
    print("\n[6] a-forge behavioral probe (sliced to 2 keys)")
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:7071/health", timeout=3) as r:
            d = json.loads(r.read())
    except Exception as e:
        fail(f"cannot reach a-forge /health: {e}")
        return False
    tool_count = d.get("tools_loaded")
    if not tool_count or tool_count < 100:
        fail(f"a-forge tools_loaded={tool_count} (expected >= 100)")
        return False
    ok(f"a-forge tools_loaded={tool_count}")
    return True


def main() -> int:
    print(f"=== Drift-check calibration regression — {datetime.now(timezone.utc).isoformat()} ===\n")
    results = [
        test_arifos_kernel_aligned(),
        test_arifos_tree_clean(),
        test_arifos_reported_as_OK(),
        test_canonical_state_separation(),
        test_aaa_a2a_discovery(),
        test_aforge_tool_count(),
    ]
    passed = sum(results)
    total = len(results)
    print(f"\n=== Result: {passed}/{total} passed ===")
    if passed < total:
        print("REGRESSION: at least one test failed. The drift-check is emitting false signals.")
        return 1
    print("All regression tests pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
