#!/usr/bin/env python3
"""Falsification tests for person_data_gate.py — forged 2026-10-04 by FI-003 under F13.

The gate exists because a privacy audit of the then-public ariffazil/AAA found 5 real
third-party NRICs, a named person's medical data, and registries/persons.yaml published
despite declaring "local-only, no GitHub push" three times in its own header.

9 scenarios. The negative arms matter more than the positive ones: a gate that blocks
everything is an obstruction, and obstructions get --no-verify'd.

  T1: NRIC-shaped value with a valid date + place-of-birth code, staged  -> exit 1
  T2: protected person-registry path staged                              -> exit 1
  T3: clean staged content                                               -> exit 0
  T4: binary-coincidence shapes (day 93, month 31, month 82)             -> exit 0
  T5: value registered in the allowlist as synthetic                     -> exit 0
  T6: Telegram bot token staged                                          -> exit 1
  T7: bogus rev passed to --all                                          -> exit 1 (fail-closed)
  T8: the gate never prints the value it caught                          -> masked
  T9: a repo with no person registry                                     -> exit 0 (no-op)

T7 and T8 are the two that a naive implementation silently fails. T7 because returning ""
on a git error reads as "found nothing"; T8 because a control that echoes the secret it
caught is itself a leak.

Usage:
    test_person_data_gate.py                run all scenarios
    test_person_data_gate.py --scenario T4  run one scenario
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GATE = Path("/root/AAA/scripts/person_data_gate.py")
if not GATE.is_file():
    print(f"FATAL: gate not found at {GATE}", file=sys.stderr)
    sys.exit(1)

# Synthetic fixtures only. Never a real person's NRIC — that is the exact mistake the
# audit found in docs/blueprints/BEFORE-MODEL-CALLBACK-SPEC-v1.md.
SYN_NRIC = "990101-14-5001"
SYN_NRIC_2 = "880229-10-5002"
SYN_TOKEN = "1234567890:AASyntheticSelfTestValueNotARealToken00"


def make_repo():
    """A throwaway git repo so the tests never touch a real index."""
    d = tempfile.mkdtemp(prefix="pdg-test-")
    subprocess.run(["git", "init", "-q", d], check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=d, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=d, check=True)
    return Path(d)


def run_gate(repo, *args):
    return subprocess.run([sys.executable, str(GATE), *args],
                          cwd=str(repo), capture_output=True, text=True, timeout=120)


def stage(repo, name, content):
    p = repo / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    subprocess.run(["git", "add", name], cwd=str(repo), check=True)


def commit_all(repo):
    subprocess.run(["git", "commit", "-q", "--no-verify", "-m", "base"],
                   cwd=str(repo), check=True)


# ── scenarios ────────────────────────────────────────────────────────────────
def t1():
    """NRIC with a valid embedded date and place-of-birth code must block."""
    r = make_repo()
    stage(r, "notes/tenant.md", f"| Tenant | Someone (NRIC {SYN_NRIC}) |\n")
    res = run_gate(r)
    return res.returncode == 1 and "NRIC" in res.stderr, f"rc={res.returncode}"


def t2():
    """A protected person-registry path must block on any staged modification."""
    r = make_repo()
    stage(r, "registries/persons.yaml", "version: 1\npersons: []\n")
    commit_all(r)
    stage(r, "registries/persons.yaml", "version: 2\npersons: []\n")
    res = run_gate(r)
    return res.returncode == 1 and "PROTECTED-PATH" in res.stderr, f"rc={res.returncode}"


def t3():
    """Clean staged content must pass — otherwise the gate is an obstruction."""
    r = make_repo()
    stage(r, "docs/readme.md", "# Nothing sensitive here\n\nJust prose about gates.\n")
    stage(r, "scripts/x.py", "print('hello')\n")
    res = run_gate(r)
    return res.returncode == 0, f"rc={res.returncode} err={res.stderr[:90]}"


def t4():
    """Binary-coincidence shapes must NOT block.

    A naive `[0-9]{6}-[0-9]{2}-[0-9]{4}` scan of AAA returns 26,565 matches, 26,560 of
    which are coincidences in mcp/filings/cache/*.bin. Date + place-of-birth validation
    is what makes the gate usable.
    """
    r = make_repo()
    stage(r, "docs/noise.md", "\n".join([
        "320193-20-0000",   # day 93
        "193125-13-4165",   # month 31
        "628280-16-0203",   # month 82
        "140361-26-0353",   # day 61
        "202601-15-1234",   # month 15
        "latitude=5.4141&longitude=100.3288",
        "G=0.2811 P=0.8409 E=0.6739",
    ]) + "\n")
    res = run_gate(r)
    return res.returncode == 0, f"rc={res.returncode} err={res.stderr[:120]}"


def t5():
    """A value registered as synthetic must be skipped."""
    r = make_repo()
    allow = {"schema": "person-data-allowlist/v1", "allow": [
        {"value": SYN_NRIC, "synthetic": True, "reason": "test fixture",
         "approved_by": "test", "added": "2026-10-04"}]}
    stage(r, "registries/person_data_allowlist.json", json.dumps(allow))
    stage(r, "docs/uses-fixture.md", f"example NRIC {SYN_NRIC} is synthetic\n")
    res = run_gate(r)
    return res.returncode == 0, f"rc={res.returncode} err={res.stderr[:120]}"


def t6():
    """A Telegram bot token must block."""
    r = make_repo()
    stage(r, "docs/telegram.md", f"curl https://api.telegram.org/bot{SYN_TOKEN}/getMe\n")
    res = run_gate(r)
    return res.returncode == 1 and "BOT-TOKEN" in res.stderr, f"rc={res.returncode}"


def t7():
    """A bogus rev must fail CLOSED, not report clean.

    The first version of the gate returned "" on any git error, so `--all NOSUCHREV`
    printed nothing and exited 0 — indistinguishable from a clean tree.
    """
    r = make_repo()
    stage(r, "docs/a.md", "clean\n")
    commit_all(r)
    res = run_gate(r, "--all", "NOSUCHREV123")
    return res.returncode != 0 and "FAIL-CLOSED" in res.stderr, \
        f"rc={res.returncode} err={res.stderr[:120]}"


def t8():
    """The gate must never print the value it caught."""
    r = make_repo()
    stage(r, "docs/leak.md", f"NRIC {SYN_NRIC} and second {SYN_NRIC_2}\n")
    res = run_gate(r)
    out = res.stdout + res.stderr
    leaks = [v for v in (SYN_NRIC, SYN_NRIC_2) if v in out]
    masked = "9901xx-xx-5001" in out
    return res.returncode == 1 and not leaks and masked, \
        f"leaked={leaks} masked_present={masked}"


def t9():
    """In a repo with no person registry the gate must pass silently."""
    r = make_repo()
    stage(r, "src/main.py", "def f():\n    return 1\n")
    res = run_gate(r)
    return res.returncode == 0 and "PASS" in res.stdout, f"rc={res.returncode}"


SCENARIOS = {
    "T1": ("NRIC blocks", t1),
    "T2": ("protected path blocks", t2),
    "T3": ("clean content passes", t3),
    "T4": ("binary coincidences do not block", t4),
    "T5": ("allowlisted synthetic passes", t5),
    "T6": ("bot token blocks", t6),
    "T7": ("bogus rev fails closed", t7),
    "T8": ("caught value is never printed", t8),
    "T9": ("no-op in a repo without a registry", t9),
}


def main():
    only = None
    if "--scenario" in sys.argv:
        only = sys.argv[sys.argv.index("--scenario") + 1]
    fails = 0
    print("person_data_gate.py — falsification tests")
    for key, (label, fn) in SCENARIOS.items():
        if only and key != only:
            continue
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        if not ok:
            fails += 1
        print(f"  {'PASS' if ok else 'FAIL'}  {key}  {label}" + ("" if ok else f"   [{detail}]"))
    print(f"\n  {len(SCENARIOS) - fails}/{len(SCENARIOS)} scenarios pass")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
