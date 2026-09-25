#!/usr/bin/env python3
"""End-to-end enumerated-refusal tests through the REAL CLI path.

Closes AGENTIC-HOOK-MESH-V1 gap ENUMERATED-REFUSAL-NO-END-TO-END-TEST:
the adversarial suite exercised gate() in-process only, so a CLI-path flip
to ALLOW passed every suite green (observed flapping 2026-09-14).

Also unit-tests the ENGINE-VERDICT-OVERREACH fix (2026-09-25): kernel
unreachable on an enumerated target must yield HOLD + FAILSAFE_KERNEL_
UNREACHABLE with an escalation receipt — never a synthesized VOID, because
a hook may not spell a kernel-only verdict.
"""
import json
import subprocess
import sys
from pathlib import Path

ENGINE = Path("/root/AAA/hooks/lib/federation_hook_engine.py")


def _gate_cli(payload: dict) -> dict:
    proc = subprocess.run(
        ["python3", str(ENGINE), "gate", "--actor", "pytest-e2e",
         "--payload", json.dumps(payload)],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.stdout.strip(), f"engine CLI produced no stdout: rc={proc.returncode} {proc.stderr[:200]}"
    # Engine emits pretty-printed (multi-line) JSON — parse the WHOLE stdout.
    return json.loads(proc.stdout)


def test_enumerated_target_refused_through_cli():
    out = _gate_cli({
        "tool_name": "Bash",
        "tool_args": {"command": "echo pwned >> /etc/sudoers.d/evil"},
    })
    assert out.get("verdict") != "ALLOW", f"CLI allowed enumerated target: {out}"
    assert out.get("execution_status") == "NOT_EXECUTED", out


def test_benign_target_allowed_through_cli():
    out = _gate_cli({"tool_name": "Bash", "tool_args": {"command": "ls /tmp"}})
    assert out.get("verdict") == "ALLOW", out
    assert out.get("execution_status") == "PROCEEDED", out


def test_kernel_unreachable_is_hold_not_void():
    sys.path.insert(0, str(ENGINE.parent))
    from federation_hook_engine import FederationHookEngine

    eng = FederationHookEngine(actor_id="pytest-e2e", session_id="s-test")
    eng._call_kernel = lambda *a, **k: None  # simulate unreachable kernel
    out = eng.gate(tool_name="Bash", tool_args={"command": "echo x >> /etc/shadow"})
    assert out["verdict"] == "HOLD", out
    assert out["consequence"] == "FAILSAFE_KERNEL_UNREACHABLE", out
    assert out["execution_status"] == "NOT_EXECUTED", out
    assert out.get("kernel_verdict") is None, out
    assert out.get("escalation_required") is True, out
    assert out.get("kernel_reachable") is False, out
