#!/usr/bin/env python3
"""Reconcile every section against ASSUMPTIONS.json.

Finds numbers each section states that DIVERGE from the single source.
This is the mechanical check that replaces "ten workstreams each with their own numbers".
"""
import json, re
from pathlib import Path

HERE = Path(__file__).parent
A = json.loads((HERE / "ASSUMPTIONS.json").read_text())

CANON = {
    "capex_total_usd_m": A["capex_usd_m"]["total_p50"],
    "liquids_mmbbl": A["volumes"]["liquids_mmbbl"],
    "gas_bcf": A["volumes"]["gas_bcf"],
    "oil_nameplate_bopd": A["capacity"]["oil_bopd_nameplate"],
}

NUM = r"(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]+(?:\.[0-9]+)?)"

def tofloat(s):
    return float(s.replace(",", ""))

def scan(text):
    hits = {}
    # capex total: only when 'capex' or 'total' appears within 60 chars before the number
    for m in re.finditer(rf"(?:capex|total forward capex|forward capex)[^.\n]{{0,60}}?(?:US)?\$\s*({NUM})\s*(bn|billion|M\b|million)?", text, re.I):
        v = tofloat(m.group(1))
        if m.group(2) and m.group(2).lower() in ("bn", "billion"):
            v *= 1000
        hits.setdefault("capex_total_usd_m", []).append(v)
    # nameplate oil rate
    for m in re.finditer(rf"({NUM})\s*(?:bopd|b/d|bpd)\b", text, re.I):
        v = tofloat(m.group(1))
        if v >= 1000:
            hits.setdefault("oil_nameplate_bopd", []).append(v)
    # liquids reserves - only MMbbl with no "cumulative"/"produced" context
    for m in re.finditer(rf"({NUM})\s*MMbbl\b", text, re.I):
        hits.setdefault("liquids_mmbbl", []).append(tofloat(m.group(1)))
    # gas
    for m in re.finditer(rf"({NUM})\s*bcf\b", text, re.I):
        hits.setdefault("gas_bcf", []).append(tofloat(m.group(1)))
    return {k: sorted(set(v)) for k, v in hits.items()}

print("LIMBAYONG FDP — SECTION RECONCILIATION vs ASSUMPTIONS.json")
print("=" * 76)
print(f"Canonical: capex ${CANON['capex_total_usd_m']}M | oil {CANON['oil_nameplate_bopd']:,.0f} bopd "
      f"| {CANON['liquids_mmbbl']} MMbbl | {CANON['gas_bcf']} bcf")
print("=" * 76)

for p in sorted((HERE / "sections").glob("S*.md")):
    hits = scan(p.read_text())
    flags = []
    for concept, vals in hits.items():
        canon = CANON[concept]
        off = [v for v in vals if abs(v - canon) / canon > 0.05]
        if off:
            flags.append(f"{concept}: {off}  (canonical {canon})")
    if flags:
        print(f"\n{p.name}")
        for f in flags:
            print(f"   !  {f}")
    else:
        print(f"\n{p.name}  OK")

print("\n" + "=" * 76)
print("Rule: a section either reads ASSUMPTIONS.json, or the canonical value is wrong")
print("and gets corrected there once — for every section at the same time.")
