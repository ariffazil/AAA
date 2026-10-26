#!/usr/bin/env python3
"""Conformance suite for docforge.registers — the permanent layer.

Run: python3 /root/AAA/scripts/test_registers.py

WHY THE NEGATIVES MATTER
  A register that merely stores what it is told is a second copy of the items.
  The defects that make it worthless are all SILENT:
    - a scar re-declared on a rebuild inflates its own recurrence
    - a contradiction omitted today disappears as if it were resolved
    - a state not re-observed is printed as if it were current
    - an EUREKA one-liner ages into the claim backlog forever
    - "settled" is claimed with no reason
  Each check below fails on one of those, not on formatting.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, "/root/AAA/scripts")

from docforge.state import Store  # noqa: E402
from docforge import registers as R  # noqa: E402

WORK = Path("/tmp/docforge-registers-test")
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


def item(iid, section, title, state, reality=None):
    d = {
        "item_id": iid,
        "section": section,
        "title": title,
        "claim_state": state,
        "summary": "s",
    }
    if reality:
        d["reality"] = reality
    return d


def raises(fn) -> bool:
    try:
        fn()
        return False
    except Exception:
        return True


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    db = WORK / "state.sqlite3"
    s = Store(db)

    e1 = [
        item("gulf", "SITUATION", "Gulf war risk", "OPEN", "GULF"),
        item("wall", "WALL", "Federal Court date", "OPEN"),
        item("static", "SITUATION", "Unchanged claim", "OPEN"),
        item("fact", "EUREKA", "Octopus has three hearts", "NEW"),
    ]
    s.record_edition("EDITION-001", "2026-10-01", e1)
    payload1 = {
        "_items": e1,
        "realities": [
            {
                "reality_id": "GULF",
                "label": "Gulf energy war",
                "domain": "energy",
                "status": "ACTIVE",
            }
        ],
        "states": [
            {
                "state_id": "GULF",
                "label": "Gulf energy war",
                "phase": "ELEVATED",
                "confidence": 0.7,
            }
        ],
        "contradictions": [
            {
                "cid": "C-001",
                "topic": "Hormuz traffic",
                "claim_a": "70% below pre-war",
                "source_a": "Iran minister",
                "claim_b": "82% recovered",
                "source_b": "Kpler",
            }
        ],
        "scars": [
            {
                "scar_id": "SCAR-DATE",
                "name": "Date contamination",
                "severity": "high",
                "symptom": "old article entered feed",
                "root_cause": "trusted source page date",
                "fix": "publication date mandatory",
                "occurrences": [{"edition": "EDITION-000", "note": "first"}],
                "recurred_today": True,
                "observed_note": "old article entered today's feed",
            }
        ],
    }
    c1 = R.record_registers(s, payload1, "EDITION-001", "2026-10-01")

    print("=" * 76)
    print("1. FIRST DECLARATION — registers persist, items bind to a reality")
    print("=" * 76)
    check("realities recorded", c1["realities"] == 1, str(c1))
    check("items bound", c1["items_bound"] == 1, str(c1))
    check(
        "scar has two witnessed occurrences",
        R.scar_ledger(s, "EDITION-001")[0]["recurrence"] == 2,
        str(R.scar_ledger(s, "EDITION-001")[0]["recurrence"]),
    )
    check(
        "scar recurred this edition",
        R.scar_ledger(s, "EDITION-001")[0]["recurred_this_edition"],
    )
    check(
        "state confidence is declared, not invented",
        R.states(s, "EDITION-001")[0]["confidence"] == 0.7,
    )

    print("=" * 76)
    print("2. REBUILD MUST NOT INFLATE — the EDITION-029 counter defect")
    print("=" * 76)
    R.record_registers(s, payload1, "EDITION-001", "2026-10-01")
    check(
        "same edition re-recorded, recurrence unchanged",
        R.scar_ledger(s, "EDITION-001")[0]["recurrence"] == 2,
        str(R.scar_ledger(s, "EDITION-001")[0]["recurrence"]),
    )

    # edition 2: state escalates, one new item, no scar / contradiction re-declared
    e2 = [
        item("gulf", "SITUATION", "Gulf war risk", "MOVED", "GULF"),
        item("wall", "WALL", "Federal Court date", "OPEN"),
        item("static", "SITUATION", "Unchanged claim", "OPEN"),
        item("void", "VOID", "Pipeline attack", "NEW"),
    ]
    s.record_edition("EDITION-002", "2026-10-02", e2)
    payload2 = {
        "_items": e2,
        "states": [
            {
                "state_id": "GULF",
                "label": "Gulf energy war",
                "phase": "ESCALATING",
                "confidence": 0.83,
            }
        ],
    }
    R.record_registers(s, payload2, "EDITION-002", "2026-10-02")

    print("=" * 76)
    print("3. ABSENT IS NOT RESOLVED")
    print("=" * 76)
    sc = R.scar_ledger(s, "EDITION-002")[0]
    check(
        "scar not re-declared retains recurrence",
        sc["recurrence"] == 2,
        str(sc["recurrence"]),
    )
    check(
        "scar not re-declared is not 'recurred today'", not sc["recurred_this_edition"]
    )
    cs = R.contradictions(s, "EDITION-002")
    check(
        "contradiction not re-declared stays OPEN",
        len(cs) == 1 and cs[0]["status"] == "OPEN",
    )
    check(
        "contradiction age counts editions",
        cs[0]["age_editions"] == 1,
        str(cs[0]["age_editions"]),
    )
    st = R.states(s, "EDITION-002")[0]
    check(
        "state phase moved",
        st["phase"] == "ESCALATING" and st["prev_phase"] == "ELEVATED",
        f"{st['prev_phase']}->{st['phase']}",
    )
    check(
        "state evidence counted from observations",
        st["evidence_count"] == 2,
        str(st["evidence_count"]),
    )

    print("=" * 76)
    print("4. CLOSING REQUIRES A REASON")
    print("=" * 76)
    check(
        "close without resolution is refused",
        raises(
            lambda: R.record_registers(
                s,
                {"contradictions": [{"cid": "C-001", "status": "RESOLVED"}]},
                "EDITION-002",
                "2026-10-02",
            )
        ),
    )
    check(
        "retire a scar with no fix is refused",
        raises(
            lambda: R.record_registers(
                s,
                {
                    "scars": [
                        {
                            "scar_id": "SCAR-DATE",
                            "status": "RETIRED",
                            "severity": "high",
                            "fix": "",
                        }
                    ]
                },
                "EDITION-002",
                "2026-10-02",
            )
        ),
    )
    R.record_registers(
        s,
        {
            "contradictions": [
                {
                    "cid": "C-001",
                    "status": "RESOLVED",
                    "resolution": "Kpler revised; Iran figure confirmed",
                }
            ]
        },
        "EDITION-002",
        "2026-10-02",
    )
    check(
        "contradiction closes with a reason",
        not R.contradictions(s, "EDITION-002"),
        "open list empty after resolution",
    )
    check(
        "closed contradiction is retained, not deleted",
        len(R.contradictions(s, "EDITION-002", include_closed=True)) == 1,
    )
    check(
        "reopening a closed contradiction is refused",
        raises(
            lambda: R.record_registers(
                s,
                {"contradictions": [{"cid": "C-001", "status": "OPEN"}]},
                "EDITION-002",
                "2026-10-02",
            )
        ),
    )

    print("=" * 76)
    print("5. AGEING IS COMPUTED, NOT FELT")
    print("=" * 76)
    e3 = [
        item("gulf", "SITUATION", "Gulf war risk", "OPEN", "GULF"),
        item("wall", "WALL", "Federal Court date", "SETTLED"),
        item("static", "SITUATION", "Unchanged claim", "OPEN"),
        item("void", "VOID", "Pipeline attack", "OPEN"),
    ]
    s.record_edition("EDITION-003", "2026-10-03", e3)
    age = {a["item_id"]: a for a in R.ageing(s, "EDITION-003")}
    check("EUREKA is not in the claim backlog", "fact" not in age, str(list(age)))
    check(
        "age counts editions since first seen",
        age["gulf"]["age_editions"] == 2,
        str(age["gulf"]["age_editions"]),
    )
    check("settled item leaves the ageing register", "wall" not in age)
    check(
        "stalled counts editions since last change",
        age["static"]["stalled_editions"] == 2,
        str(age["static"]["stalled_editions"]),
    )
    check(
        "an unchanged item is not marked as moving",
        age["static"]["claim_state"] == "OPEN",
    )
    check(
        "seen_editions counts exposure, not age",
        age["gulf"]["seen_editions"] == 3,
        str(age["gulf"]["seen_editions"]),
    )
    R.record_registers(
        s,
        {
            "scars": [
                {
                    "scar_id": "SCAR-DATE",
                    "name": "Date contamination",
                    "severity": "high",
                    "status": "ACTIVE",
                }
            ]
        },
        "EDITION-003",
        "2026-10-03",
    )
    sc3 = R.scar_ledger(s, "EDITION-003")[0]
    check(
        "declaring a standing scar does not invent a recurrence",
        sc3["recurrence"] == 2 and not sc3["recurred_this_edition"],
        f"recurrence={sc3['recurrence']} today={sc3['recurred_this_edition']}",
    )

    print("=" * 76)
    print("6. ENTROPY MEASURES METABOLISM, NOT THROUGHPUT")
    print("=" * 76)
    m2 = R.entropy(s, "EDITION-002")
    check("open claims exclude EUREKA", m2["open_claims"] == 4, str(m2["open_claims"]))
    check("open delta is the accretion", m2["open_delta"] == 1, str(m2["open_delta"]))
    check(
        "no exits means metabolism is unknown, not 100%",
        m2["metabolism"] is None,
        str(m2["metabolism"]),
    )
    check("verdict names accretion", m2["verdict"] == "ACCUMULATING", m2["verdict"])
    m3 = R.entropy(s, "EDITION-003")
    check(
        "settling an item turns the verdict",
        m3["verdict"] == "METABOLIZING",
        m3["verdict"],
    )
    check(
        "metabolism = settled / exits", m3["metabolism"] == 1.0, str(m3["metabolism"])
    )
    check(
        "unbound claims are counted honestly",
        m3["unbound_open_claims"] == 2,
        str(m3["unbound_open_claims"]),
    )
    check(
        "reality anchor persists across editions that omit it",
        age["gulf"]["reality"] == "GULF",
    )
    check(
        "reality rollup counts bound items",
        R.realities(s, "EDITION-003")[0]["bound_total"] == 1,
        str(R.realities(s, "EDITION-003")[0]),
    )

    print("=" * 76)
    print("7. THE RENDER CANNOT LEAK OR EXECUTE")
    print("=" * 76)
    R.record_registers(
        s,
        {
            "scars": [
                {"scar_id": "SCAR-X", "name": "<script>x</script>", "severity": "low"}
            ]
        },
        "EDITION-003",
        "2026-10-03",
    )
    body = R.render_registers_html(s, "EDITION-003") + R.render_entropy_html(
        s, "EDITION-003"
    )
    check("no internal path in the register HTML", "/root/" not in body)
    check(
        "producer text is escaped", "<script>" not in body and "&lt;script&gt;" in body
    )
    check(
        "register sections are numbered under the delta",
        "0.1" in body and "0.2" in body,
    )
    check(
        "summary is JSON-serialisable",
        bool(json.dumps(R.summary(s, "EDITION-003"), default=str)),
    )

    print("=" * 76)
    print("8. SCHEMA IS ADDITIVE AND IDEMPOTENT")
    print("=" * 76)
    before = {r[1] for r in s.conn.execute("PRAGMA table_info(items)")}
    R.ensure_schema(s.conn)
    R.ensure_schema(s.conn)
    after = {r[1] for r in s.conn.execute("PRAGMA table_info(items)")}
    check("reality column present", "reality" in before)
    check("re-running ensure_schema changes nothing", before == after)

    print("=" * 76)
    print(f"RESULT: {PASS} passed, {FAIL} failed")
    if FAILURES:
        print("FAILED: " + "; ".join(FAILURES))
    print("=" * 76)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
