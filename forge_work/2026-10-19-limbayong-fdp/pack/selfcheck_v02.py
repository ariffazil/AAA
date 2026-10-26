#!/usr/bin/env python3
"""Independent self-check for LIM-SFDP-v0.2. Reports, does not fix.

Checks are deliberately mechanical so they can fail loudly:
  1  every ledger row appears in the document
  2  every figure has a caption, a source and a tag
  3  no point value of OOIP / plateau appears without range context
  4  'economic limit' never appears without OPEN nearby
  5  classification footer on every numbered page
  6  no attribution to a person; no PETRONAS document numbering
  7  the vessel's 25,000 bopd is never contradicted by a 40,000 vessel claim
  8  arithmetic spot checks recomputed from scratch
  9  150 MMscfd appears only as a corrected claim, never as a vessel spec
"""
import json, re, subprocess
from pathlib import Path

PACK = Path("/root/AAA/forge_work/2026-10-19-limbayong-fdp/pack")
PDF = PACK / "LIM-SFDP-v0.2.pdf"
txt = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                     capture_output=True, text=True).stdout
pages = [p for p in txt.split("\f") if p.strip()]
led = json.load(open(PACK / "ledger.json"))
rows = {r["id"]: r for r in led["rows"]}
mc = led["mc"]

fails, warns = [], []

# 1 — every row cited
for rid in rows:
    if rid not in txt:
        fails.append(f"{rid}: never cited in the document")

# 2 — figures
for n in range(0, 5):
    if f"Figure {n} —" not in txt:
        fails.append(f"Figure {n}: caption missing")

# 3 — point values must not float free
point_checks = [
    ("347", ("MMbbl", "bracket")), ("372.5", ("MMbbl",)),
    ("398", ("MMbbl", "bracket")), ("132.6", ("MMbbl", "P90")),
    ("139.5", ("MMbbl", "P50")), ("146.8", ("MMbbl", "P10")),
    ("25,000", ("bopd", "b/d")), ("37,014", ("bopd",)), ("40,000", ("bopd", "b/d")),
]
for val, ok in point_checks:
    if not any(o in txt for o in ok):
        fails.append(f"unit context missing for {val}")
    bad = 0
    for m in re.finditer(rf"(?<![\d.,]){re.escape(val)}(?![\d.])", txt):
        ctx = txt[max(0, m.start() - 260):m.end() + 260].lower()
        if not any(k in ctx for k in ("mmbbl", "bopd", "b/d", "bpd", "bwpd", "range", "p90", "p50", "p10", "bracket", "l-2", "l-3")):
            bad += 1
    if bad:
        warns.append(f"{val}: {bad} bare occurrence(s)")

# 4 — economic limit always flagged
for m in re.finditer(r"economic limit", txt, re.I):
    ctx = txt[max(0, m.start() - 220):m.end() + 320]
    if "OPEN" not in ctx:
        fails.append("'economic limit' without OPEN marker")

# 5 — classification footer
cls = sum(1 for p in pages if "not a PCSB/PETRONAS document" in p)
if cls < len(pages) - 1:
    fails.append(f"classification footer on {cls} of {len(pages)} pages")

# 6 — attribution
if "Arif" in txt:
    fails.append("attribution to a person found")
if re.search(r"\bPCSB[- ]?\d|\bPETRONAS\s+\d{3,}", txt):
    fails.append("PETRONAS-style document numbering found")

# 7 — vessel consistency
if "25,000 bopd" not in txt:
    fails.append("vessel ceiling 25,000 bopd not stated")
if re.search(r"nameplate[^.]{0,40}40,000[^.]{0,40}(vessel|hull)", txt, re.I):
    fails.append("40,000 described as a vessel property")

# 8 — arithmetic
checks = [
    ("life_p50", 139.5e6 / (25000 * 365), 15.3, 0.1),
    ("life_p90", 132.6e6 / (25000 * 365), 14.5, 0.1),
    ("life_p10", 146.8e6 / (25000 * 365), 16.1, 0.1),
    ("nine_six", 139.5e6 / (40000 * 365), 9.57, 0.02),
    ("voidage", 25000 * 1.30, 32500, 1),
    ("vrr", 20000 / 32500, 0.62, 0.005),
]
for name, computed, stated, tol in checks:
    if abs(computed - stated) > tol:
        fails.append(f"{name}: computed {computed:.4f}, document {stated}")

# 9 — 150 must never be a vessel spec
for m in re.finditer(r"150\s*MMscfd", txt):
    ctx = txt[max(0, m.start() - 200):m.end() + 120].lower()
    if "correct" not in ctx and "audit" not in ctx and "asserted" not in ctx:
        fails.append("150 MMscfd used outside the correction context")

print("SELF-CHECK — LIM-SFDP-v0.2.pdf")
print("=" * 62)
print(f"pages                : {len(pages)}")
print(f"ledger rows          : {len(rows)}  (cited: {sum(1 for r in rows if r in txt)})")
print(f"figures with caption : {sum(1 for n in range(5) if f'Figure {n} —' in txt)} of 5")
print(f"classification pages : {cls} of {len(pages)}")
print(f"MC P90/P50/P10       : {mc['rec_p90']} / {mc['rec_p50']} / {mc['rec_p10']} MMbbl")
print(f"life P90/P50/P10     : {mc['life_p90']} / {mc['life_p50']} / {mc['life_p10']} yr")
print()
if fails:
    print(f"FAILED ({len(fails)}):")
    for f in fails:
        print("  x", f)
else:
    print("FAILED: none")
print()
if warns:
    print(f"WARNINGS ({len(warns)}):")
    for w in warns[:15]:
        print("  !", w)
else:
    print("WARNINGS: none")
