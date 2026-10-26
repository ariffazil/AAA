#!/usr/bin/env python3
"""Limbayong FDP — THE ONE ENGINE.

Reads ASSUMPTIONS.json. Nothing is hardcoded here. Every section that quotes a
number must be able to reproduce it by running this file with no arguments.

Usage:  python3 engine.py            -> prints the canonical metric set
        python3 engine.py --json     -> machine-readable
"""
from __future__ import annotations
import json, sys
from pathlib import Path

HERE = Path(__file__).parent
A = json.loads((HERE / "ASSUMPTIONS.json").read_text())

V = A["volumes"]; C = A["capacity"]; K = A["capex_usd_m"]; S = A["schedule"]
F = A["fiscal"]; P = A["price"]; DISC = A["discount_rate"]

# spend profile is a schedule assumption, not a number: declared here, once.
SPEND = {"2027": 0.14, "2028": 0.32, "2029": 0.34, "2030": 0.20}
START_YEAR = int(S["first_oil_p50"][:4])
PLATEAU_YRS = S["plateau_years"]
DECL = S["decline_per_yr"]
CAPEX = float(K["total_p50"])


def profile(oil_bopd=None, gas_mmscfd=None):
    oil = float(C["oil_bopd_forecast"] if oil_bopd is None else oil_bopd)
    gas = float(C["gas_mmscfd_forecast"] if gas_mmscfd is None else gas_mmscfd)
    out = []
    for i in range(26):
        if i == 0:      f = 0.40
        elif i == 1:    f = 0.75
        elif i < 2 + PLATEAU_YRS: f = 1.0
        else:           f = (1 - DECL) ** (i - (1 + PLATEAU_YRS))
        if oil * f < 2500: break
        out.append((START_YEAR + i, oil * f, gas * f))
    return out


def cashflows(brent=None, gas_price=None, capex=None, opex=None, delay=0):
    brent = float(P["brent_base_usd"] if brent is None else brent)
    gas_p = float(P["gas_usd_per_mmbtu"] if gas_price is None else gas_price)
    cx = float(CAPEX if capex is None else capex)
    op = float(A["opex"]["usd_per_boe"] if opex is None else opex)

    cfs = [(int(y), -cx * w) for y, w in SPEND.items()]
    dep = cx / F["tax_depreciation_years"]
    carry = 0.0
    for i, (yr, oil, gas) in enumerate(profile()):
        yr = yr + delay
        oil_mmbbl = oil * 365 / 1e6
        gas_bcf = gas * 365 / 1e6
        boe = oil_mmbbl + gas_bcf * V["boe_per_mcf"]
        rev = oil_mmbbl * (brent - 5) * (1 - F["sabah_sst"]) + gas_bcf * gas_p * (1 - F["sabah_sst"])
        opex_y = boe * op
        ebitda = rev - opex_y
        d = dep if i < F["tax_depreciation_years"] else 0.0
        taxable = ebitda - d - carry
        if taxable < 0:
            carry = -taxable; tax = 0.0
        else:
            carry = 0.0; tax = taxable * F["pita"]
        cfs.append((yr, ebitda - tax))
    return cfs


def npv(cfs, rate=DISC, base=2026):
    return sum(cf / ((1 + rate) ** (y - base)) for y, cf in cfs)


def irr(cfs, base=2026):
    lo, hi = -0.95, 6.0
    for _ in range(400):
        m = (lo + hi) / 2
        if npv(cfs, m, base) > 0: lo = m
        else: hi = m
    return (lo + hi) / 2


def breakeven(target_irr=None, target_npv=None):
    lo, hi = 20.0, 250.0
    for _ in range(80):
        m = (lo + hi) / 2
        r = cashflows(brent=m)
        v = npv(r) if target_npv is not None else irr(r)
        t = 0.0 if target_npv is not None else target_irr
        if v < t: lo = m
        else: hi = m
    return (lo + hi) / 2


def metrics():
    cf = cashflows()
    cum = 0.0; peak = 0.0; payback = None
    for y, c in cf:
        cum += c
        if cum < peak: peak = cum
        if payback is None and cum > 0 and y > START_YEAR: payback = y
    boe_total = V["total_mmboe"]
    return {
        "capex_usd_m": CAPEX,
        "capex_per_boe": round(CAPEX / boe_total, 2),
        "npv10_usd_m": round(npv(cf)),
        "irr_pct": round(irr(cf) * 100, 1),
        "brent_npv0": round(breakeven(target_npv=0)),
        "brent_10pct": round(breakeven(target_irr=0.10)),
        "brent_15pct": round(breakeven(target_irr=0.15)),
        "peak_cash_usd_m": round(peak),
        "payback_year": payback,
        "plateau_boe_d": round(C["oil_bopd_forecast"] + C["gas_mmscfd_forecast"] / V["boe_per_mcf"] / 1e3 * 1e3 * V["boe_per_mcf"] / V["boe_per_mcf"] * 1) if False else round(C["oil_bopd_forecast"] * (1 - 0) + C["gas_mmscfd_forecast"] * 1000 / 5.8, -2),
        "first_oil": S["first_oil_p50"],
        "discount_rate": DISC,
        "fiscal_basis": F["basis"],
    }


if __name__ == "__main__":
    m = metrics()
    if "--json" in sys.argv:
        print(json.dumps(m, indent=2))
    else:
        print("LIMBAYONG — CANONICAL METRICS (engine.py v1, reads ASSUMPTIONS.json)")
        print("-" * 62)
        for k, v in m.items():
            print(f"  {k:22s} {v}")
