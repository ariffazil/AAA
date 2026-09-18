#!/usr/bin/env python3
"""Conformance suite for the feedback ledger.

Run: python3 /root/AAA/scripts/test_feedback.py

WHY THE NEGATIVES MATTER HERE MORE THAN ANYWHERE
  This is the only component that lets a sentence in a chat change what the
  machine does tomorrow. The failure mode is not a broken document — it is a
  machine that quietly obeys a mood, or one that keeps obeying an instruction
  the reader thought he had withdrawn. So the suite pins:

    - the raw comment is preserved VERBATIM (the rule is derived, never a
      replacement for what he actually said)
    - a duplicate instruction is not stacked
    - a retired rule stops applying
    - retirement without a reason is REFUSED
    - empty feedback is REFUSED
    - "stop doing X" and "do more X" derive OPPOSITE directions
    - a long news paragraph is not mistaken for feedback about the format
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, "/root/AAA/scripts")
from docforge.feedback import (FeedbackStore, capture_candidates,  # noqa: E402
                               derive_rule, normalise)

WORK = Path("/tmp/docforge-feedback-test")
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
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    s = FeedbackStore(WORK / "state.sqlite3")

    print("=" * 76)
    print("1. DERIVATION — opposite instructions must not collapse to one keyword")
    print("=" * 76)
    r_sup, d_sup = derive_rule("buang naratif politik ni")
    r_emp, d_emp = derive_rule("fokus pada OD1")
    print(f"     'buang naratif politik ni' -> {r_sup} [{d_sup}]")
    print(f"     'fokus pada OD1'           -> {r_emp} [{d_emp}]")
    check("'buang X' derives SUPPRESS", d_sup == "suppress")
    check("'fokus X' derives EMPHASISE", d_emp == "emphasise")
    check("the two directions are DIFFERENT", d_sup != d_emp,
          "a store that keeps only the keyword would apply the wrong one")
    check("a statement of fact is neither, and says so",
          derive_rule("apa cerita hari ni")[1] == "note")
    check("framing like 'HERMES:' is stripped",
          normalise("HERMES: fokus pada OD1") == "fokus pada OD1",
          normalise("HERMES: fokus pada OD1"))
    check("the instruction text survives normalisation",
          "OD1" in normalise("  fokus   pada   OD1  "))

    print()
    print("=" * 76)
    print("2. RECORDING — raw comment kept verbatim, rule derived beside it")
    print("=" * 76)
    raw = "Buang naratif politik ni. Fokus pada OD1."
    rec = s.add(raw, edition_ref="EDITION-002")
    check("recorded", rec["fb_id"] > 0 and not rec["duplicate"])
    rows = s.all_rows()
    check("raw_text is VERBATIM", rows[0]["raw_text"] == raw,
          f"{rows[0]['raw_text']!r}")
    check("the derived rule is a separate field, not a replacement",
          rows[0]["rule"] != rows[0]["raw_text"])
    check("scope defaults to brief", rows[0]["scope"] == "brief")
    check("it starts active", rows[0]["active"] == 1)
    check("applied_count starts at zero", rows[0]["applied_count"] == 0)

    print()
    print("=" * 76)
    print("3. NEGATIVES — what must be REFUSED")
    print("=" * 76)
    try:
        s.add("   ")
        check("empty feedback is REFUSED", False, "it was accepted")
    except ValueError as e:
        check("empty feedback is REFUSED", True, str(e)[:50])

    dup = s.add(raw, edition_ref="EDITION-003")
    check("a duplicate instruction is NOT stacked", dup.get("duplicate") is True,
          dup.get("note", ""))
    check("and the store still holds exactly one row", len(s.all_rows()) == 1,
          f"{len(s.all_rows())} rows")
    check("duplicate detection ignores cosmetic whitespace",
          s.add("  Buang   naratif politik ni. Fokus pada OD1.  ",
                edition_ref="EDITION-004").get("duplicate") is True)

    try:
        s.retire(1, "")
        check("retirement without a reason is REFUSED", False, "it was accepted")
    except ValueError as e:
        check("retirement without a reason is REFUSED", True, str(e)[:60])

    print()
    print("=" * 76)
    print("4. RETIREMENT — a withdrawn rule must stop applying")
    print("=" * 76)
    check("rule is active before retirement", len(s.active()) == 1)
    check("retire returns True for a live rule", s.retire(1, "noted, one-off reaction"))
    check("retired rule leaves the active set", len(s.active()) == 0,
          f"{len(s.active())} active")
    check("retirement is recorded, not deleted", len(s.all_rows()) == 1)
    check("the reason is stored and readable",
          "one-off" in (s.all_rows()[0]["retire_reason"] or ""))
    check("retiring an already-retired rule is a no-op, not a silent success",
          s.retire(1, "again") is False)
    check("a retired rule can be re-stated as a new ACTIVE entry",
          s.add(raw)["duplicate"] is False,
          "the reader changing his mind is legitimate, and the history stays")

    print()
    print("=" * 76)
    print("5. EXPORT — the rules reach where the build reads them")
    print("=" * 76)
    s2 = FeedbackStore(WORK / "state2.sqlite3")
    s2.add("fokus pada OD1 dan tarikh Mac 2027", edition_ref="EDITION-002")
    s2.add("buang ramalan harga yang tiada sumber", edition_ref="EDITION-003")
    out = s2.export_rules(WORK / "rules.md")
    txt = out.read_text()
    check("export file written", out.is_file(), out.name)
    check("both standing instructions appear", txt.count("- **") == 2,
          f"{txt.count('- **')} entries")
    check("each rule carries the words it came from", "heard as" in txt)
    check("the export states the consequence of ignoring it",
          "retirement" in txt)
    check("applied_count increments on export",
          s2.active()[0]["applied_count"] == 1,
          str(s2.active()[0]["applied_count"]))
    s2.export_rules(WORK / "rules.md")
    check("a second export increments again (staleness becomes visible)",
          s2.active()[0]["applied_count"] == 2)
    empty = FeedbackStore(WORK / "state3.sqlite3").export_rules(
        WORK / "rules3.md").read_text()
    check("an empty ledger says so instead of inventing content",
          "None standing" in empty)

    print()
    print("=" * 76)
    print("6. CAPTURE — a news paragraph is NOT feedback about the format")
    print("=" * 76)
    long_news = ("The Federal Court granted leave in March and the Sarawak "
                 "petition followed in February, which means the constitutional "
                 "question is now ahead of the commercial one and the parties "
                 "are effectively betting on the outcome rather than settling.")
    check("a long news paragraph yields no candidates",
          capture_candidates(long_news) == [],
          f"{capture_candidates(long_news)}")
    mixed = "Good brief today.\nBuang naratif politik.\nfokus pada OD1"
    cands = capture_candidates(mixed)
    check("directive lines inside a message ARE candidates", len(cands) == 2,
          str(cands))
    check("a plain compliment yields nothing", capture_candidates("nice one") == [])
    check("a directive with no verb is not guessed at",
          capture_candidates("the ringgit at 4.18") == [])

    print()
    print("=" * 76)
    print(f"RESULT  {PASS} passed, {FAIL} failed")
    if FAILURES:
        print("FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
    print("=" * 76)
    print("VERDICT:", "feedback is recorded, reversible, and auditable"
          if not FAIL else "FEEDBACK LEDGER UNSOUND")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
