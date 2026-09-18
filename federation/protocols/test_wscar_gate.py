#!/usr/bin/env python3
"""Black-box conformance harness for arifos-hermes-gate-hook.py (W_SCAR v2).

WHY THIS FILE EXISTS
--------------------
The gate was rewritten to v2 on 2026-09-18 and its author reported "11/11 tests
pass" — but no harness was left on disk. An unrepeatable test result is not
evidence; it is a claim. This file makes the claim checkable by anyone, forever.

Design: BLACK BOX. It shells out to the hook with a JSON payload on stdin and
asserts on the exit code and stdout. It never imports the hook's internals for
the behavioural cases, so it cannot drift from the implementation it tests.

Exit-code contract (from the hook's main):
    0  allow
    2  block (T3 / W_SCAR)
    3  block (JITU circuit breaker)

Reference (the artefact under test):
    /root/AAA/federation/protocols/arifos-hermes-gate-hook.py

Test receipts: every case uses session_id=SELFTEST_SESSION so that any receipt
this harness causes is filterable out of the real ledger.

Run:  python3 test_wscar_gate.py            (behavioural suite)
      python3 test_wscar_gate.py --regex    (regex unit checks only)
"""

import json
import os
import subprocess
import sys

GATE = "/root/AAA/federation/protocols/arifos-hermes-gate-hook.py"
SELFTEST_SESSION = "gate-selftest-2026-09-18"

# A guaranteed-NXDOMAIN host: RFC 2606 reserves .invalid, so this can never
# resolve and can never accidentally become a real citation.
UNRESOLVABLE = "https://nonexistent-domain-9f3a2b.invalid/report"
RESOLVABLE = "https://example.com/"

OPS_SKILL = (
    "/root/AAA/skills/domains/general/court/court-audit/"
    "agent-finding-verification/SKILL.md"
)

# (name, payload, expected_exit, why)
CASES = [
    # ---- A. v1 FALSE POSITIVES: wrongly blocked. Must ALLOW. ----
    (
        "A1 ops-tree target carries a trigger word in its PATH",
        {"tool_name": "read_file", "tool_input": {"path": OPS_SKILL}},
        0,
        "A path is not a claim; the word in the directory name asserts nothing.",
    ),
    (
        "A2 ops-tree WRITE (method tree is exempt)",
        {
            "tool_name": "write_file",
            "tool_input": {
                "path": "/root/AAA/skills/x/SKILL.md",
                "content": "budget cost money RM100 legal court",
            },
        },
        0,
        "Doctrine writes address no human, so they owe no market claim.",
    ),
    (
        "A3 chained READ-ONLY pipeline (cd && grep | head)",
        {
            "tool_name": "terminal",
            "tool_input": {
                "command": 'cd /root/AAA/federation/protocols && '
                'grep -n "health" arifos-hermes-gate-hook.py | head -5'
            },
        },
        0,
        "v1 anchored on the whole string, so a leading `cd` made grep look "
        "like a mutation. Every segment must now be a probe.",
    ),
    (
        "A4 exempt creative tool carries market words",
        {
            "tool_name": "text_to_speech",
            "tool_input": {"text": "harga minyak RM2.05 dan kos subsidi"},
        },
        0,
        "Narration is not assertion.",
    ),
    (
        "A5 read-only listing with no assertion content",
        {"tool_name": "terminal", "tool_input": {"command": "ls -la /root/.hermes/scripts/"}},
        0,
        "Nothing is claimed, so nothing is owed.",
    ),
    # ---- B. Claims WITHOUT admissible evidence. Must BLOCK (exit 2). ----
    (
        "B1 money claim, no evidence pointer",
        {
            "tool_name": "write_file",
            "tool_input": {
                "path": "/tmp/wscar-b1.txt",
                "content": "Subsidi bahan bakar dijangka mencecah RM58 bilion.",
            },
        },
        2,
        "v1 passed this because a bare number needs no magic word to slip through.",
    ),
    (
        "B2 legal claim, no evidence pointer",
        {
            "tool_name": "write_file",
            "tool_input": {
                "path": "/tmp/wscar-b2.txt",
                "content": "The court held that the ordinance is invalid.",
            },
        },
        2,
        "Same defect, different vocabulary family.",
    ),
    (
        "B3 health claim, no evidence pointer",
        {
            "tool_name": "write_file",
            "tool_input": {
                "path": "/tmp/wscar-b3.txt",
                "content": "Dos ubat ini selamat untuk pesakit.",
            },
        },
        2,
        "Third family; the gate must not be tuned to money alone.",
    ),
    (
        "B4 claim citing a URL that does NOT resolve",
        {
            "tool_name": "write_file",
            "tool_input": {
                "path": "/tmp/wscar-b4.txt",
                "content": f"Lihat {UNRESOLVABLE} — kos subsidi RM58 bilion.",
            },
        },
        2,
        "v1 asked 'does the payload contain the word source?'. A citation-shaped "
        "string that 404s is not a source. This is the whole point of v2.",
    ),
    (
        "B5 claim citing a non-existent evidence path",
        {
            "tool_name": "write_file",
            "tool_input": {
                "path": "/tmp/wscar-b5.txt",
                "content": "Rujuk /tmp/does-not-exist-evidence.json — kos RM58 bilion.",
            },
        },
        2,
        "Evidence paths are only admissible if they EXIST on disk.",
    ),
    # ---- C. NEGATIVE CONTROL: a valid citation must NOT be over-blocked. ----
    (
        "C1 claim WITH a resolvable URL (control — must ALLOW)",
        {
            "tool_name": "write_file",
            "tool_input": {
                "path": "/tmp/wscar-c1.txt",
                "content": f"Kos subsidi RM58 bilion. Rujuk {RESOLVABLE}",
            },
        },
        0,
        "Over-blocking is its own defect. Without this control, 'blocks "
        "everything' would score as a perfect gate.",
    ),
]


def run_gate(payload: dict) -> tuple[int, str]:
    env = dict(os.environ, ARIFOS_TRACE_ID=f"trc-selftest")
    p = subprocess.run(
        [sys.executable, GATE],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    return p.returncode, (p.stdout or "").strip()


def behavioural() -> int:
    print("=" * 74)
    print("W_SCAR v2 — BLACK-BOX CONFORMANCE")
    print(f"target: {GATE}")
    print("=" * 74)
    passed = failed = 0
    jitu_seen = False

    for name, payload, expect, why in CASES:
        payload.setdefault("session_id", SELFTEST_SESSION)
        try:
            code, out = run_gate(payload)
        except subprocess.TimeoutExpired:
            print(f"FAIL  {name}\n      timeout after 30s")
            failed += 1
            continue

        if "JITU" in out:
            jitu_seen = True

        ok = code == expect
        verdict = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"{verdict}  {name}")
        print(f"      exit={code} expected={expect}")
        if not ok or os.environ.get("VERBOSE"):
            print(f"      why: {why}")
            if out:
                print(f"      stdout: {out[:220]}")

    print("-" * 74)
    print(f"behavioural: {passed}/{len(CASES)} passed, {failed} failed")
    if jitu_seen:
        print("⚠️  JITU appeared in output — the circuit breaker may be tripped,")
        print("    which blocks everything and makes these results meaningless.")
    return 1 if failed else 0


def regex_units() -> int:
    """Static checks on the three patterns that gate admissible evidence."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("gate_under_test", GATE)
    if spec is None or spec.loader is None:
        print(f"FAIL  cannot load gate module from {GATE}")
        return 1
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    checks = [
        # (.jsonl must come BEFORE .json, or the match truncates to .json)
        (
            "jsonl not truncated to json",
            lambda: mod.EVIDENCE_PATH_RE.findall("/x/evidence.jsonl")
            == ["/x/evidence.jsonl"],
        ),
        (
            "json still matches",
            lambda: mod.EVIDENCE_PATH_RE.findall("/x/e.json") == ["/x/e.json"],
        ),
        (
            "txt is NOT admissible evidence",
            lambda: mod.EVIDENCE_PATH_RE.findall("/x/notes.txt") == [],
        ),
        # A .py path must not clear a hold — source code is not a market source.
        (
            "py is NOT admissible evidence",
            lambda: mod.EVIDENCE_PATH_RE.findall("/x/script.py") == [],
        ),
        (
            "receipt id recognised (bare)",
            lambda: bool(mod.RECEIPT_RE.search("receipt_id: rcpt-123456")),
        ),
        (
            "receipt id recognised (JSON quoted — the first live catch)",
            lambda: bool(mod.RECEIPT_RE.search('"receipt_id": "rcpt-abcdef"')),
        ),
        (
            "NEGATIVE CONTROL: bare word 'source' is not a receipt id",
            lambda: not mod.RECEIPT_RE.search("this has no source at all"),
        ),
    ]

    print("=" * 74)
    print("REGEX UNIT CHECKS")
    print("=" * 74)
    passed = failed = 0
    for name, fn in checks:
        try:
            ok = bool(fn())
        except Exception as exc:  # noqa: BLE001
            ok = False
            name = f"{name} [raised {type(exc).__name__}]"
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        passed += ok
        failed += not ok
    print("-" * 74)
    print(f"regex: {passed}/{len(checks)} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    if "--regex" in sys.argv:
        sys.exit(regex_units())
    rc = behavioural()
    print()
    rc |= regex_units()
    sys.exit(rc)
