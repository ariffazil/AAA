#!/usr/bin/env python3
"""Conformance suite for the transport destination gate.

Run: python3 /root/AAA/scripts/test_transport_gate.py

The defect this guards (gateway log, 2026-09-18, three occurrences):
    "Queued-lane final send to 8410138119 failed:
     Forbidden: the bot can't send messages to the bot"

8410138119 is the bot's own id. So the negatives below are the whole point:
every one of them is a destination that LOOKS like a destination and would
silently swallow the brief.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/AAA/scripts")
from docforge import transport as T  # noqa: E402

WORK = Path("/tmp/docforge-transport-test")
PASS = FAIL = 0
FAILURES: list[str] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  [PASS] {label}" + (f" — {detail}" if detail else ""))
    else:
        FAIL += 1
        FAILURES.append(label)
        print(f"  [FAIL] {label}" + (f" — {detail}" if detail else ""))


def main() -> int:
    if WORK.exists():
        import shutil
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)

    lock = T.load_lock()
    if lock is None:
        print("cannot read the real identity lock — aborting rather than guessing")
        return 2
    bot_id = str(lock["bots"]["hermes"]["id"])
    arif_id = str(lock["humans"]["arif"]["telegram_user_id"])
    syed_id = str(lock["humans"]["syed"]["telegram_user_id"])

    print("=" * 76)
    print("1. THE PROVEN BUG — the bot's own id must never be a destination")
    print("=" * 76)
    d = T.verify(f"telegram:{bot_id}")
    check("bot id is HELD", d.verdict == "HOLD", str(d))
    check("the refusal names the real symptom",
          "bot can't send messages to the bot" in d.reason)
    check("a bare group id with no lock entry is HELD not allowed",
          T.verify("telegram:-999999999999").verdict == "HOLD")

    print()
    print("=" * 76)
    print("2. THE CORRECT DESTINATION")
    print("=" * 76)
    d = T.verify(f"telegram:{arif_id}")
    check("Arif's DM is ALLOWED", d.ok, str(d))
    check("resolved id matches the lock", d.resolved_id == arif_id)
    check("role is reported", d.role == "arif", d.role)
    d2 = T.verify(f"telegram:{arif_id}:148647")
    check("a verified topic thread is ALLOWED", d2.ok, str(d2))

    print()
    print("=" * 76)
    print("3. THE MIRROR DEFECT — right id, wrong human")
    print("=" * 76)
    d = T.verify(f"telegram:{syed_id}", expect_role="arif")
    check("Syed's id in an Arif-scoped send is HELD", d.verdict == "HOLD", str(d))
    check("refusal explains it is the wrong person", "wrong person" in d.reason)
    d = T.verify(f"telegram:{syed_id}", expect_role=None)
    check("same id is ALLOWED when the send is legitimately for him", d.ok, str(d))

    print()
    print("=" * 76)
    print("4. UNVERIFIABLE DESTINATIONS — bare names cannot carry a delivery")
    print("=" * 76)
    for t in ("origin", "local", "all", "telegram", "ARIF", "telegram:notanumber"):
        d = T.verify(t)
        check(f"{t!r} is not silently allowed", not d.ok,
              f"{d.verdict}: {d.reason[:60]}")

    print()
    print("=" * 76)
    print("5. FAIL CLOSED — no lock, no send")
    print("=" * 76)
    d = T.verify(f"telegram:{arif_id}", lock_path=WORK / "does-not-exist.json")
    check("missing lock -> DEGRADED, not ALLOW", d.verdict == "DEGRADED", str(d))
    check("reason says the send is refused rather than guessed",
          "refused rather than guessed" in d.reason)
    bad = WORK / "bad.json"
    bad.write_text("{not json")
    check("malformed lock -> DEGRADED",
          T.verify(f"telegram:{arif_id}", lock_path=bad).verdict == "DEGRADED")

    print()
    print("=" * 76)
    print("6. A LOCK THAT CHANGES MUST CHANGE THE VERDICT (no hardcoding)")
    print("=" * 76)
    alt = WORK / "alt-lock.json"
    alt.write_text(json.dumps({
        "humans": {"arif": {"telegram_user_id": "555000111"}},
        "groups": {}, "bots": {"hermes": {"id": "999888777"}},
    }))
    check("a different human id is ALLOWED under a different lock",
          T.verify("telegram:555000111", lock_path=alt).ok)
    check("the OLD bot id is still HELD under the new lock",
          T.verify(f"telegram:{bot_id}", lock_path=alt).verdict == "HOLD")
    check("a different bot id is HELD under the new lock",
          T.verify("telegram:999888777", lock_path=alt).verdict == "HOLD")

    print()
    print("=" * 76)
    print("7. SYSTEMIC SWEEP over the live scheduler")
    print("=" * 76)
    findings = T.scan_origins()
    for f in findings:
        print(f"    {f['verdict']:8} {f['job_id']:24} {str(f['name'])[:34]}")
        print(f"             {f['reason'][:100]}")
    check("sweep completed against the live jobs store",
          isinstance(findings, list), f"{len(findings)} finding(s)")

    # A sweep that always returns nothing is decoration. Prove it FALSIFIES by
    # feeding it the exact shape of the 2026-09-18 defect.
    fake = WORK / "jobs-with-bot-origin.json"
    fake.write_text(json.dumps({"jobs": [
        {"id": "j-bad-origin", "name": "silent brief", "enabled": True,
         "deliver": "origin", "origin": {"chat_id": bot_id, "user_id": arif_id}},
        {"id": "j-bad-target", "name": "wrong dm", "enabled": True,
         "deliver": f"telegram:{bot_id}", "origin": {"chat_id": arif_id}},
        {"id": "j-good", "name": "healthy brief", "enabled": True,
         "deliver": f"telegram:{arif_id}", "origin": {"chat_id": arif_id}},
        {"id": "j-disabled", "name": "retired", "enabled": False,
         "deliver": "origin", "origin": {"chat_id": bot_id}},
    ]}))
    found = T.scan_origins(jobs_path=fake)
    ids = {f["job_id"] for f in found}
    check("sweep CATCHES a job whose origin id is the bot",
          "j-bad-origin" in ids, f"flagged={sorted(ids)}")
    check("sweep CATCHES a job whose deliver target is the bot",
          "j-bad-target" in ids)
    check("sweep does NOT flag a correctly-addressed job", "j-good" not in ids)
    check("sweep ignores disabled jobs (a paused job cannot misdeliver)",
          "j-disabled" not in ids)
    check("the flag explains WHY it would fail",
          any("BOT id" in f["reason"] or "bot id" in f["reason"] for f in found))

    check("sweep FAILS CLOSED when the lock is unreadable",
          bool(T.scan_origins(jobs_path=fake,
                              lock_path=WORK / "nope.json"))
          and T.scan_origins(jobs_path=fake,
                             lock_path=WORK / "nope.json")[0]["verdict"] == "DEGRADED")

    print()
    print("=" * 76)
    print(f"RESULT  {PASS} passed, {FAIL} failed")
    if FAILURES:
        print("FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
    print("=" * 76)
    print("VERDICT:", "every unverifiable destination is refused"
          if not FAIL else "TRANSPORT GATE UNSOUND")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
