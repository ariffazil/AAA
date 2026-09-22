#!/usr/bin/env python3
"""G13 suite — positive control + five negative controls.

A gate that only ever says PASS is indistinguishable from no gate, so every
negative control here MUST produce HOLD for the suite to mean anything.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/AAA/scripts")
import alpha_zen_gate as G  # noqa: E402

BASE = json.loads(
    Path("/root/AAA/forge_work/alpha-zen/cards/2026-09-21-morning.json").read_text()
)

SIG = [
    {"who": "shared", "text": "Selat Hormuz masih tutup, tapi Brent bacaan sistem 99.36 "
     "dan trend dia DOWNTREND. Pasaran dah bayar perang tu lebih awal."},
    {"who": "arif", "text": "PETRONAS untung RM27.2 bilion separuh tahun, tapi dividen 2026 "
     "dipotong 38% jadi RM20 bilion. Minyak naik, kerajaan dapat kurang."},
    {"who": "syed", "text": "Emas 4,363.30, EMA masih susun bullish, RSI 59.3. Tapi verdict "
     "sistem SABAR — reward-to-risk cuma 1.0."},
    {"who": "shared", "text": "Fed naik 25 basis mata 16 September, kali pertama sejak 2023. "
     "BoJ ikut ke 1.25%, paras tertinggi dalam 31 tahun."},
    {"who": "syed", "text": "ACSM keluar Position Stand latihan rintangan 2026 — kemas kini "
     "pertama dalam tujuh belas tahun. Konsisten kalahkan sempurna."},
    {"who": "arif", "text": "Yang di-Pertuan Besar batalkan semua pelantikan exco Negeri "
     "Sembilan. Kuasa bukan benda yang kau dakwa — ia benda yang orang bagi."},
    {"who": "shared", "text": "MET Malaysia masih amaran angin kencang dan laut bergelora "
     "sampai 24 September, ombak sampai 3.5 meter."},
]


def gate(card: dict) -> tuple[bool, list[str]]:
    p = Path("/tmp/g13-probe.json")
    p.write_text(json.dumps(card, ensure_ascii=False))
    ok, errs, warns = G.run(p)
    return ok, [e for e in errs if e.startswith("G13")]


def build(sigs=None) -> dict:
    c = copy.deepcopy(BASE)
    c["signals"] = sigs if sigs is not None else copy.deepcopy(SIG)
    return c


cases: list[tuple[str, dict, bool]] = [
    ("positive — 7 grounded lines, both anchors present", build(), True),
    ("no signals array at all (back-compat)", {k: v for k, v in build().items()
                                               if k != "signals"}, True),
    ("gym line removed -> Syed's body anchor gone",
     build([s for s in SIG if "ACSM" not in s["text"]]), False),
    ("gold line removed -> Syed's trading anchor gone",
     build([s for s in SIG if "Emas" not in s["text"]]), False),
    ("every line Syed's -> Arif reading a stranger's card",
     build([{**s, "who": "syed"} for s in SIG]), False),
    ("frozen day-count smuggled into prose",
     build(copy.deepcopy(SIG) + [{"who": "shared", "text":
          "Belanjawan tinggal 18 hari lagi dari sekarang."}]), False),
    ("private marker reprinted",
     build(copy.deepcopy(SIG) + [{"who": "shared", "text":
          "Macam yang dia pernah cakap pasal OD1."}]), False),
    ("only 3 lines -> still a card that fits but says too little",
     build(copy.deepcopy(SIG)[:3]), False),
    ("machine label leaking to the reader",
     build(copy.deepcopy(SIG) + [{"who": "shared", "text":
          "ARIF: ini baris yang bocor label."}]), False),
]

fails = 0
for name, card, want_pass in cases:
    ok, g13 = gate(card)
    got = ok and not g13
    mark = "OK  " if got == want_pass else "FAIL"
    if got != want_pass:
        fails += 1
    print(f"[{mark}] expect={'PASS' if want_pass else 'HOLD'}  {name}")
    for e in g13:
        print(f"          └ {e[:120]}")

print()
print(f"G13 suite: {len(cases) - fails}/{len(cases)} " +
      ("— PASS" if fails == 0 else "— BROKEN, negative controls did not fire"))
sys.exit(1 if fails else 0)
