#!/usr/bin/env python3
"""Negative-control suite for alpha_zen_gate.

A gate that only ever says PASS is indistinguishable from no gate. Each case
below breaks ONE rule and must be refused. The suite also asserts that the good
card still passes, so a gate cannot be "fixed" into permanent refusal.

Anchor (W_SCAR provenance): /root/AAA/scripts/chron_events.json
"""
import copy
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOOD = Path("/root/AAA/forge_work/alpha-zen/cards/2026-09-18-morning.json")
TMP = Path("/tmp/az_gate_test.json")
GATE = HERE / "alpha_zen_gate.py"


def run(card: dict) -> tuple[int, str]:
    TMP.write_text(json.dumps(card, ensure_ascii=False))
    r = subprocess.run([sys.executable, str(GATE), str(TMP)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def case(name: str, mutate, expect: str) -> bool:
    c = copy.deepcopy(GOOD_CARD)
    mutate(c)
    rc, out = run(c)
    failed = (rc != 0)
    ok = (failed if expect == "HOLD" else not failed)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        tail = [l for l in out.splitlines() if l.strip().startswith(('✗', 'VERDICT'))]
        print(f"         expected={expect} got={'HOLD' if failed else 'PASS'}")
        for t in tail[:3]:
            print(f"         {t.strip()[:120]}")
    return ok


TODAY = date.today()
_MON = ["Jan", "Feb", "Mac", "Apr", "Mei", "Jun", "Jul", "Ogos", "Sep", "Okt", "Nov", "Dis"]
_ISO = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_DM = re.compile(r"\b\d{1,2}\s+(?:Sept|Sep|Jan|Feb|Mac|Apr|Mei|Jun|Jul|Ogos|Okt|Nov|Dis)\b", re.I)


def _d(d: date) -> str:
    return f"{d.day} {_MON[d.month - 1]} {d.year}"


def make_fresh(card: dict) -> dict:
    """Re-stamp every source date to TODAY before the suite runs.

    WHY THIS EXISTS — the suite's fixture is a dated CARD FILE, and the gate's own
    G11 rule expires any priced source older than STALE_DAYS. So a suite that was
    20/20 on the day it was written decays into failure on a timer: measured
    2026-09-21, 14/20 with all six failures being positive controls whose fixture
    had aged past four days.

    A suite that always fails gets ignored, and a gate nobody runs is not a gate —
    the same rot as a config allow-list that drifts behind the runtime, or a
    validator that refuses every write. The fix is to re-stamp the fixture at load
    and let the two G11 cases supply their OWN relative dates, so the rule is still
    exercised in BOTH directions: an old source must HOLD, a fresh one must PASS.
    """
    out = copy.deepcopy(card)
    for r in out.get("rows", []):
        for who in ("arif", "syed"):
            cell = r.get(who) or {}
            if cell.get("source"):
                cell["source"] = _DM.sub(_d(TODAY), _ISO.sub(TODAY.isoformat(),
                                                            cell["source"]))
    return out


GOOD_CARD = make_fresh(json.loads(GOOD.read_text()))

CASES = [
    ("good card passes", lambda c: None, "PASS"),
    ("8 rows instead of 9",
     lambda c: c["rows"].pop(), "HOLD"),
    ("only 2 KENA_TAHU rows",
     lambda c: c["rows"].__setitem__(2, {**c["rows"][2], "tier": "EUREKA"}), "HOLD"),
    ("KENA_TAHU row with no source",
     lambda c: c["rows"][0]["arif"].pop("source"), "HOLD"),
    ("Syed loses every gym signal",
     lambda c: [r["syed"].__setitem__("text", "Emas dalam julat sempit hari ni.")
                for r in c["rows"]], "HOLD"),
    ("Syed loses every gold signal",
     lambda c: [r["syed"].__setitem__("text", "Latihan kekuatan kena ukur, bukan beban.")
                for r in c["rows"]], "HOLD"),
    ("Arif loses every structural signal",
     lambda c: [r["arif"].__setitem__("text", "Hari ni cuaca panas di utara.")
                for r in c["rows"]], "HOLD"),
    ("quote with no author",
     lambda c: c["yin_quote"].pop("author"), "HOLD"),
    ("quote attributed to 'unknown'",
     lambda c: c["yin_quote"].__setitem__("author", "unknown"), "HOLD"),
    ("private marker leaks into the card",
     lambda c: c["rows"][3]["arif"].__setitem__(
         "text", "Dia pernah cakap perkara ni secara peribadi, jadi aku pilih ini."), "HOLD"),
    ("duplicate subject on two rows",
     lambda c: (c["rows"][6]["arif"].__setitem__(
                    "text", c["rows"][7]["arif"]["text"]),
                c["rows"][6]["syed"].__setitem__(
                    "text", c["rows"][7]["syed"]["text"])), "HOLD"),
    ("empty Syed lane on one row",
     lambda c: c["rows"][4]["syed"].__setitem__("text", ""), "HOLD"),
    # G11 — the parallel lane's failure mode: a real source with a stale number.
    ("stale price (gold source 30 days old)",
     lambda c: c["rows"][0]["syed"].__setitem__(
         "source", f"Kitco, {_d(TODAY - timedelta(days=30))}"), "HOLD"),
    ("price with an undated source",
     lambda c: c["rows"][0]["syed"].__setitem__("source", "Kitco"), "HOLD"),
    ("fresh price still passes",
     lambda c: c["rows"][0]["syed"].__setitem__(
         "source", f"JM Bullion, {_d(TODAY)}"), "PASS"),
    # G12 — the frozen countdown, found in both this card AND a parallel engine.
    ("prose carries a frozen day-count",
     lambda c: c["rows"][2]["arif"].__setitem__(
         "text", "Belanjawan 2027 dibentang 9 Oktober — 21 hari."), "HOLD"),
    ("prose cites the date instead",
     lambda c: c["rows"][2]["arif"].__setitem__(
         "text", "Belanjawan 2027 dibentang 9 Oktober."), "PASS"),
    ("a price window is not a frozen countdown",
     lambda c: c["rows"][2]["arif"].__setitem__(
         "text", "Harga minyak kuat kuasa 17-23 Sept, jadi harga hari ini berbeza."), "PASS"),
    # G12 false-positive guards — a validator must not invent holds.
    ("deep-time figure is not a countdown",
     lambda c: c["rows"][7]["arif"].__setitem__(
         "text", "Perak Man berusia 11,000 tahun, dikebumikan dalam posisi janin."), "PASS"),
    ("year-scale fact is not a countdown",
     lambda c: c["rows"][7]["arif"].__setitem__(
         "text", "Struktur itu terbentuk 300 juta tahun dulu."), "PASS"),
]


def main() -> int:
    print("=" * 70)
    print("alpha_zen_gate — negative-control suite")
    print("=" * 70)
    passed = sum(case(n, m, e) for n, m, e in CASES)
    total = len(CASES)
    print("=" * 70)
    print(f"RESULT  {passed}/{total} passed")
    print("VERDICT:", "the gate holds its negatives"
          if passed == total else "the gate has holes — DO NOT TRUST IT")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
