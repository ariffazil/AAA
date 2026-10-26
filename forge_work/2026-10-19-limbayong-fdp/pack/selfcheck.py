#!/usr/bin/env python3
"""Independent self-check of LIM-SFDP-v0.1.pdf against its own ledger.
Run as a separate pass. Reports, does not fix."""
import re, subprocess, json
from pathlib import Path

PDF = Path("/root/AAA/forge_work/2026-10-19-limbayong-fdp/pack/LIM-SFDP-v0.1.pdf")
txt = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                     capture_output=True, text=True).stdout
pages = txt.split("\f")

LEDGER = {
    "L-01": 347.0, "L-02": 372.5, "L-03": 398.0,
    "L-04": 35.0, "L-05": 37.5, "L-06": 40.0,
    "L-07": 121.5, "L-08": 139.7, "L-09": 159.2,
    "L-10": 30000, "L-11": 33507, "L-12": 37014,
    "L-13": 790.9, "L-14": 150, "L-15": 40000,
}
OPEN_ROWS = ["L-19", "L-20", "L-21", "L-25"]

fails, warns = [], []

# 1 — ledger values present and correctly stated
expect_str = {
    "L-01": "347", "L-02": "372.5", "L-03": "398", "L-04": "35 %",
    "L-05": "37.5 %", "L-06": "40 %", "L-07": "121.5", "L-08": "139.7",
    "L-09": "159.2", "L-10": "30,000 bopd", "L-11": "33,507 bopd",
    "L-12": "37,014 bopd", "L-13": "790.9", "L-14": "150 MMscfd",
    "L-15": "40,000 bopd",
}
for row, s in expect_str.items():
    if s not in txt:
        fails.append(f"{row}: expected string '{s}' not found in PDF")

# 2 — every ledger row ID referenced
for row in list(LEDGER) + OPEN_ROWS:
    if row not in txt:
        fails.append(f"{row}: row ID never cited in body text")

# 3 — point values of OOIP / plateau must never appear bare
for val, unit in [("347", "MMbbl"), ("372.5", "MMbbl"), ("398", "MMbbl"),
                  ("121.5", "MMbbl"), ("139.7", "MMbbl"), ("159.2", "MMbbl"),
                  ("30,000", "bopd"), ("33,507", "bopd"), ("37,014", "bopd")]:
    hits = len(re.findall(rf"{re.escape(val)}\s*{unit}", txt))
    if hits == 0:
        fails.append(f"point value {val} {unit} never appears attached to a unit")
    # a bare occurrence with no unit and no context word nearby
    for m in re.finditer(rf"(?<![\d.]){re.escape(val)}(?![\d.])", txt):
        ctx = txt[max(0, m.start()-40):m.end()+40].lower()
        unitwords = ("mmbbl", "bopd", "mmboe", "bwpd", "bcf", "e6", "l-", "mmscfd")
        if not any(w in ctx for w in unitwords):
            warns.append(f"bare '{val}' without unit in context: ...{ctx.strip()[:70]}...")
            break

# 4 — "economic limit" must be accompanied by OPEN
for m in re.finditer(r"economic limit", txt, re.I):
    ctx = txt[max(0, m.start()-200):m.end()+320]
    if "OPEN" not in ctx:
        fails.append("'economic limit' appears without an OPEN marker nearby")

# 5 — every figure has a caption
for n in (0, 1, 2):
    if f"Figure {n}" not in txt:
        fails.append(f"Figure {n} caption missing")

# 6 — page numbering from Part 1
numbered = sum(1 for p in pages if re.search(r"Page \d+ of \d+", p))
if numbered < 5:
    fails.append(f"page numbering present on only {numbered} pages")

# 7 — the classification line
cls = sum(1 for p in pages if "not a PCSB/PETRONAS document" in p)
if cls < 5:
    fails.append(f"classification footer on only {cls} pages")

# 8 — no PETRONAS branding claim / no Arif attribution
if "Arif" in txt:
    fails.append("author attribution to Arif found")
if re.search(r"\bPCSB[- ]?\d|\bPETRONAS\s+\d{3,}", txt):
    fails.append("PETRONAS-style document numbering found")

# 9 — arithmetic spot checks
import math
checks = [
    ("121.45", 347 * 0.35), ("139.6875", 372.5 * 0.375), ("159.2", 398 * 0.40),
    ("11.09", 121.45e6 / (30000 * 365)), ("11.42", 139.6875e6 / (33507 * 365)),
    ("11.78", 159.2e6 / (37014 * 365)), ("14.45", 790.9 / 54.75),
]
for label, val in checks:
    if abs(float(label) - val) / val > 0.001:
        fails.append(f"arithmetic mismatch: document says {label}, computes {val:.4f}")

print("SELF-CHECK — LIM-SFDP-v0.1.pdf")
print("=" * 60)
print(f"pages: {len([p for p in pages if p.strip()])}")
print(f"VERIFIED rows: {sum(1 for r in ['L-13','L-14','L-15','L-16','L-17','L-18'])}")
print(f"DERIVED rows : {sum(1 for r in ['L-02','L-05','L-07','L-08','L-09','L-11'])}")
print(f"ASSUMED rows : {sum(1 for r in ['L-01','L-03','L-04','L-06','L-10','L-12','L-22','L-23','L-24'])}")
print(f"OPEN rows    : {len(OPEN_ROWS)}")
print()
if fails:
    print(f"FAILED CHECKS ({len(fails)}):")
    for f in fails:
        print("  ✗", f)
else:
    print("FAILED CHECKS: none")
print()
if warns:
    print(f"WARNINGS ({len(warns)}):")
    for w in warns[:12]:
        print("  !", w)
else:
    print("WARNINGS: none")
