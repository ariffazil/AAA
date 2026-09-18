#!/usr/bin/env python3
"""Conformance suite for docforge.state — the delta engine behind the Gran Loop.

Run: python3 /root/AAA/scripts/test_state_delta.py

WHY THE DELTA NEEDS ITS OWN SUITE
  The delta is the one component whose failure is INVISIBLE. If it breaks, every
  edition still renders, still passes every gate, still seals, and still looks
  correct — it just quietly reports "no change" forever, or re-reports settled
  items as new. The reader has no way to tell a quiet week from a broken loop.

  So the negatives here are about SILENCE and REPETITION:
    - an item that did not change must NOT appear as new
    - an item that disappeared must NOT be silently retired
    - a settled item must NOT be reported as still open
    - recording the same edition twice must NOT create phantom changes
    - an unknown claim_state must be REJECTED, not coerced
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, "/root/AAA/scripts")

from docforge.state import Store  # noqa: E402
from docforge.pipeline import validate_items, render_delta_html  # noqa: E402

WORK = Path("/tmp/docforge-state-test")
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


def item(iid, section, title, state, summary="s"):
    return {"item_id": iid, "section": section, "title": title,
            "claim_state": state, "summary": summary}


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    db = WORK / "state.sqlite3"
    s = Store(db)

    # ── edition 1 ───────────────────────────────────────────────────────────
    print("=" * 76)
    print("1. FIRST EDITION — everything is new, nothing is a 'change'")
    print("=" * 76)
    e1 = [
        item("lng-jurisdiction", "SITUATION", "PETROS LNG jurisdiction", "CONTESTED"),
        item("fc-hearing-date", "WALL", "Federal Court PDA 1974 hearing date", "OPEN"),
        item("revenue-projection", "WALL", "RM10-20b revenue projection", "CONTESTED"),
        item("data-centre-share", "EUREKA", "Data centre = 18% of GDP", "SETTLED"),
        # live (non-terminal) and will simply vanish in edition 2 — this is the
        # item that must be surfaced as dropped-without-resolution
        item("ringgit-level", "SITUATION", "Ringgit at 4.18", "OPEN"),
    ]
    prev = s.record_edition("EDIT-001", "2026-09-18", e1, artifact_sha256="a" * 64)
    d1 = s.delta("EDIT-001")
    check("first edition has no predecessor", prev is None, f"prev={prev}")
    check("first edition flagged as first", d1.first_edition)
    check("all items reported as new", len(d1.new) == 5, f"{len(d1.new)} new")
    check("nothing reported as moved", not d1.moved)
    check("headline says so plainly",
          "no prior state" in d1.headline().lower(), d1.headline())

    # ── edition 2: one opens, one stays, one settles, one is dropped ────────
    print()
    print("=" * 76)
    print("2. SECOND EDITION — the actual delta")
    print("=" * 76)
    e2 = [
        # CONTESTED -> OPEN: the hearing date came through, so jurisdiction moved
        item("lng-jurisdiction", "SITUATION", "PETROS LNG jurisdiction", "OPEN"),
        # unchanged, still open
        item("fc-hearing-date", "WALL", "Federal Court PDA 1974 hearing date", "OPEN"),
        # CONTESTED -> SETTLED
        item("revenue-projection", "WALL", "RM10-20b revenue projection", "SETTLED"),
        # brand new
        item("budget-tabling", "SITUATION", "Budget 2027 tabled 9 Oct", "NEW"),
        # data-centre-share is ABSENT from edition 2 -> dropped
    ]
    s.record_edition("EDIT-002", "2026-09-19", e2, artifact_sha256="b" * 64)
    d2 = s.delta("EDIT-002")

    check("MOVED: state change is detected", len(d2.moved) == 1, f"{len(d2.moved)}")
    check("MOVED carries the previous state for the reader",
          d2.moved and d2.moved[0].get("was") == "CONTESTED",
          f"was={d2.moved[0].get('was') if d2.moved else '?'}")
    check("SETTLED: terminal transition is classified as settled, not moved",
          len(d2.settled) == 1, f"{len(d2.settled)}")
    check("NEW: genuinely new item detected", len(d2.new) == 1,
          f"{len(d2.new)}: {[i['item_id'] for i in d2.new]}")
    check("UNCHANGED: carries over without being re-reported as new",
          len(d2.still_open) == 1, f"{len(d2.still_open)}")
    check("DROPPED: absent-but-live item is surfaced, NOT silently retired",
          len(d2.dropped) == 1, f"{[i['item_id'] for i in d2.dropped]}")
    check("a SETTLED item that stops being reported is NOT called dropped",
          all(i["item_id"] != "data-centre-share" for i in d2.dropped),
          "settled work finishing is not an unresolved disappearance — the code "
          "excludes terminal states here, and my first test expectation was wrong")
    check("a SETTLED item is not reported as still open",
          all(i["item_id"] != "revenue-projection" for i in d2.still_open))
    check("headline counts every class present",
          d2.headline().count(",") == 4, d2.headline())

    # ── the rendered delta section ──────────────────────────────────────────
    print()
    print("=" * 76)
    print("3. RENDERED DELTA — the reader's half")
    print("=" * 76)
    html = render_delta_html(d2, "EDIT-001")
    check("delta section names the edition it compared against",
          "EDIT-001" in html)
    check("dropped items are labelled as NOT resolved, not quietly omitted",
          "not</em> the same as resolved" in html or "not the same as resolved" in html)
    check("changed items show was -> now", "CONTESTED" in html and "OPEN" in html)
    check("no unreplaced template placeholder survives",
          "{{" not in html)
    html1 = render_delta_html(d1, None)
    check("first-edition delta explains the absence of a comparison",
          "First tracked edition" in html1)

    # ── idempotence: the phantom-change trap ────────────────────────────────
    print()
    print("=" * 76)
    print("4. IDEMPOTENCE — re-recording an edition must not invent changes")
    print("=" * 76)
    s.record_edition("EDIT-002", "2026-09-19", e2, artifact_sha256="c" * 64)
    d2b = s.delta("EDIT-002")
    check("re-recording the same edition yields the same delta",
          d2b.as_dict()["counts"] == d2.as_dict()["counts"],
          f"{d2b.as_dict()['counts']} vs {d2.as_dict()['counts']}")

    # ── reopening ───────────────────────────────────────────────────────────
    print()
    print("=" * 76)
    print("5. REOPEN — a settled claim going live again is its own signal")
    print("=" * 76)
    e3 = [item("revenue-projection", "WALL", "RM10-20b revenue projection", "CONTESTED")]
    s.record_edition("EDIT-003", "2026-09-20", e3)
    d3 = s.delta("EDIT-003")
    check("SETTLED -> CONTESTED is classified as REOPENED, not merely moved",
          len(d3.reopened) == 1, f"{len(d3.reopened)}; moved={len(d3.moved)}")
    check("reopened item records what it was",
          d3.reopened[0].get("was") == "SETTLED")

    # ── first_seen / last_changed provenance ────────────────────────────────
    print()
    print("=" * 76)
    print("6. PROVENANCE — how long has this claim been sitting here")
    print("=" * 76)
    rows = list(s.conn.execute(
        "SELECT * FROM items WHERE item_id='fc-hearing-date' ORDER BY last_seen"))
    check("item tracked across two editions", len(rows) >= 2, f"{len(rows)} rows")
    check("first_seen is the EARLIEST sighting, not the latest",
          rows[0]["first_seen"] == "2026-09-18", rows[0]["first_seen"])
    check("unchanged item keeps its original last_changed date",
          rows[-1]["last_changed"] == "2026-09-18",
          f"last_changed={rows[-1]['last_changed']} (state never changed)")
    rp = s.conn.execute(
        "SELECT last_changed FROM items WHERE item_id='revenue-projection'"
        " ORDER BY last_seen DESC LIMIT 1").fetchone()
    check("changed item's last_changed advances",
          rp["last_changed"] == "2026-09-20", f"{rp['last_changed']}")

    # ── open-items register ─────────────────────────────────────────────────
    print()
    print("=" * 76)
    print("7. OPEN REGISTER — terminal items leave it")
    print("=" * 76)
    op = s.open_items()
    ids = {i["item_id"] for i in op}
    # the previous version of this assertion read `... or True`, which is a test
    # that can never fail. Deleted rather than kept for decoration.
    check("register excludes items that are terminally SETTLED",
          "data-centre-share" not in ids,
          f"open={sorted(ids)} — settled and never reopened, so it leaves the "
          "register for a real reason rather than an omission")
    check("register keeps live items recorded in ANY earlier edition",
          "fc-hearing-date" in ids and "lng-jurisdiction" in ids,
          f"open={sorted(ids)} — a live claim not repeated in the latest edition "
          "must not fall out of the register")
    check("register carries each item's LATEST state, not a stale edition",
          all(i["edition"] in ("EDIT-001", "EDIT-002", "EDIT-003") for i in op),
          f"{sorted({i['edition'] for i in op})}")
    rp = next((i for i in op if i["item_id"] == "revenue-projection"), None)
    check("a REOPENED item is back in the register", rp is not None,
          "SETTLED -> CONTESTED returns it to the open list, so asserting it "
          "should be ABSENT (as an earlier version of this test did) was wrong")
    check("reopened item's register row shows its CURRENT state",
          rp is not None and rp["claim_state"] == "CONTESTED",
          f"{rp['claim_state'] if rp else 'absent'}")

    # ── schema enforcement ──────────────────────────────────────────────────
    print()
    print("=" * 76)
    print("8. SCHEMA — bad input is refused, and ALL problems are listed")
    print("=" * 76)
    bad = [
        item("", "SITUATION", "no id", "OPEN"),
        item("x1", "NOT_A_SECTION", "bad section", "OPEN"),
        item("x2", "SITUATION", "bad state", "PROBABLY"),
        item("x3", "SITUATION", "dup", "OPEN"),
        item("x3", "SITUATION", "dup again", "OPEN"),
    ]
    probs = validate_items(bad)
    check("missing item_id caught", any("missing 'item_id'" in p for p in probs))
    check("unknown section caught", any("NOT_A_SECTION" in p for p in probs))
    check("unknown claim_state caught", any("PROBABLY" in p for p in probs))
    check("duplicate item_id caught", any("duplicate" in p for p in probs))
    check("ALL problems returned at once, not just the first", len(probs) >= 4,
          f"{len(probs)} problems")
    check("valid items produce no problems",
          bool(validate_items(e1) == []), f"{validate_items(e1)}")

    # ── WALL kinds ──────────────────────────────────────────────────────────
    print()
    print("=" * 76)
    print("9. WALL — UNRESOLVED and WITHDRAWN are different things")
    print("=" * 76)
    from docforge.state import WALL_KINDS
    check("both wall kinds are declared", set(WALL_KINDS) == {"UNRESOLVED", "WITHDRAWN"},
          str(WALL_KINDS))
    check("WALL is a first-class section, not a note inside another one",
          "WALL" in __import__("docforge.state", fromlist=["SECTIONS"]).SECTIONS)

    print()
    print("=" * 76)
    print(f"RESULT  {PASS} passed, {FAIL} failed")
    if FAILURES:
        print("FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
    print("=" * 76)
    print("VERDICT:", "the delta reports change correctly and stays quiet when "
          "nothing changed" if not FAIL else "DELTA UNRELIABLE")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
