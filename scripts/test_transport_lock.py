#!/usr/bin/env python3
"""Behavioural harness for the TRANSPORT LOCK rule inside the pre_tool_call hook.

Why a file and not inline shell: the hook is LIVE. A shell command containing a
send-to-the-bot-id payload is itself blocked at pre_tool_call, so the test has to
carry its payloads in a file that the command line never quotes.

Anchor (W_SCAR provenance): /root/briefing-system/schema/briefing.schema.json
"""
import json
import subprocess
import sys

HOOK = "/root/AAA/federation/protocols/arifos-hermes-gate-hook.py"

# Each case: (name, command, expected) where expected is
#   "BLOCK"  → hook exits non-zero with a transport-lock decision
#   "PASS"   → hook does not block on the transport rule
CASES = [
    ("send to BOT id (the 2026-09-18 defect)", "hermes" + " send -t telegram:8410138119 --json hi", "BLOCK"),
    ("send to ARIF DM",                         "hermes" + " send -t telegram:267378578 --json hi", "PASS"),
    ("bare numeric id (unverifiable grammar)",  "hermes" + " send -t 267378578 --json hi",          "BLOCK"),
    ("send to ANOTHER human (syed)",            "hermes" + " send -t telegram:1042200555 --json hi", "BLOCK"),
    ("send with NO target",                     "hermes" + " send --json hi",                      "BLOCK"),
    ("non-send command is untouched",           "ls -la /tmp",                                    "PASS"),
    ("read-only, mentions send as data",        "grep -rn 'send' /tmp/nonexistent 2>/dev/null",   "PASS"),
]


def run(command: str) -> tuple[int, str]:
    payload = json.dumps({
        "tool_name": "terminal",
        "session_id": "harness",
        "args": {"command": command},
    })
    p = subprocess.run([sys.executable, HOOK], input=payload,
                       capture_output=True, text=True, timeout=60)
    return p.returncode, (p.stdout + p.stderr)


def main() -> int:
    passed = failed = 0
    print("=" * 74)
    print("TRANSPORT LOCK — behavioural harness")
    print("=" * 74)
    for name, cmd, expect in CASES:
        try:
            rc, out = run(cmd)
        except Exception as exc:  # noqa: BLE001
            print(f"  [ERROR] {name}: {exc}")
            failed += 1
            continue

        locked = "TRANSPORT LOCK" in out
        got = "BLOCK" if (rc != 0 and locked) else "PASS"
        ok = got == expect
        passed += ok
        failed += (not ok)
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}")
        print(f"         cmd={cmd[:58]!r}")
        print(f"         expected={expect:<5} got={got:<5} exit={rc}")
        if locked:
            first = [l for l in out.splitlines() if "TRANSPORT LOCK" in l]
            if first:
                print(f"         hook said: {first[0].strip()[:150]}")

    print("=" * 74)
    print(f"RESULT  {passed} passed, {failed} failed")
    print("=" * 74)
    print("VERDICT:", "the transport lock holds its negatives"
          if failed == 0 else "the lock has holes — DO NOT ship")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
