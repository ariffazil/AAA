#!/usr/bin/env python3
"""Solvency table from filed statements - the two-detector view.

Input: CSV with a header row containing at least:
    period,end_year,assets,equity
and ideally:
    net_income,ocf,cash,borrowings

end_year is a decimal year (2024.99 for FY2024) used as the time axis.
All money columns must share one unit; state that unit in the output.

Output, per row:
    D       = ln(assets / (assets - equity))     distance to the debt barrier
    lambda  = -(dD/dt) over a 3-row window       rate the barrier closes
    T       = D / lambda / (1 + burn)            years to the barrier
              burn = min(|ocf|/assets, 0.6) when ocf < 0
              T = inf when lambda <= 0  (gap not closing)
    ocf/pat, cash/borrowings, gearing

Usage:
    python3 solvency_table.py statements.csv [--label "Company name"]

Read T ONLY beside the cash columns. A fabrication case shows a healthy-looking
T while cash coverage collapses - that is the whole point of printing both.
"""
import csv
import math
import sys

BURN_CAP = 0.6


def num(row, key):
    v = row.get(key)
    if v is None or str(v).strip() == "":
        return None
    try:
        return float(str(v).replace(",", "").replace("%", "").strip())
    except ValueError:
        return None


def analyse(rows):
    """Return a list aligned with `rows`; entries are dicts or None."""
    out = []
    prev_d = None
    prev_t = None
    for r in rows:
        assets = num(r, "assets")
        equity = num(r, "equity")
        if assets is None or equity is None or assets <= 0 or equity >= assets:
            # Cannot form a distance for this row. Chaining continues only if the
            # previous usable row is still known, so the rate stays honest.
            out.append(None)
            continue

        t = num(r, "end_year")
        liabilities = assets - equity
        d = math.log(assets / liabilities)
        net_income = num(r, "net_income")
        ocf = num(r, "ocf")
        cash = num(r, "cash")
        borrowings = num(r, "borrowings")

        lam = None
        if prev_d is not None and prev_t is not None and t is not None and t > prev_t:
            lam = -(d - prev_d) / (t - prev_t)

        if lam is None:
            tv = None
        elif lam > 1e-9:
            burn = 0.0
            if ocf is not None and ocf < 0:
                burn = min(abs(ocf) / assets, BURN_CAP)
            tv = d / lam / (1.0 + burn)
        else:
            tv = math.inf

        out.append({
            "period": r.get("period"),
            "assets": assets,
            "liabilities": liabilities,
            "leverage": liabilities / assets,
            "d": d,
            "lam": lam,
            "t": tv,
            "conv": (ocf / net_income) if (ocf is not None and net_income and net_income > 0) else None,
            "cov": (cash / borrowings) if (cash is not None and borrowings) else None,
            "gear": (borrowings / equity) if (borrowings is not None and equity) else None,
        })
        prev_d, prev_t = d, t
    return out


def fmt(v, spec="{:.3f}"):
    if v is None:
        return "--"
    if isinstance(v, float) and math.isinf(v):
        return "inf"
    return spec.format(v)


def verdict(r):
    t, conv = r["t"], r["conv"]
    if t is not None and isinstance(t, float) and math.isinf(t) and conv is not None and conv < 0.5:
        return "MODEL BLIND + CASH FAILING -> fabrication signature"
    if t is not None and not (isinstance(t, float) and math.isinf(t)) and t < 1:
        if conv is not None and conv < 0.5:
            return "tight runway AND cash not converting"
        return "tight runway, cash still healthy -> erosion only"
    if conv is not None and conv < 0.5:
        return "cash not converting -> check for accrual-only profit"
    return "no alarm on either detector"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    label = "company"
    if "--label" in sys.argv:
        label = sys.argv[sys.argv.index("--label") + 1]

    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    res = analyse(rows)

    print(f"SOLVENCY TABLE - {label}")
    print("=" * 98)
    print(f"{'period':14}{'assets':>14}{'liab':>14}{'L/A':>7}{'D':>8}{'lambda':>10}"
          f"{'T(y)':>9}{'OCF/PAT':>9}{'cash/borr':>11}{'gear':>7}")
    print("-" * 98)
    for r in res:
        if r is None:
            print(f"{'[skipped]':14}  -- row unusable: assets/equity missing or equity >= assets --")
            continue
        lam_s = "--" if r["lam"] is None else f"{r['lam']:+.4f}"
        print(f"{str(r['period'])[:13]:14}{r['assets']:>14,.0f}{r['liabilities']:>14,.0f}"
              f"{r['leverage']:>7.3f}{r['d']:>8.3f}{lam_s:>10}"
              f"{fmt(r['t'], '{:.2f}'):>9}"
              f"{fmt(r['conv'], '{:.2f}'):>9}"
              f"{fmt(r['cov'], '{:.3f}'):>11}"
              f"{fmt(r['gear'], '{:.2f}'):>7}")

    print()
    print("TWO DETECTORS, READ TOGETHER")
    for r in res:
        if r is None:
            continue
        print(f"  {str(r['period'])[:13]:14} T={fmt(r['t'], '{:.2f}'):>7}  "
              f"OCF/PAT={fmt(r['conv'], '{:.2f}'):>6}  cov={fmt(r['cov'], '{:.3f}'):>7}  "
              f"{verdict(r)}")

    print()
    print("T is a triage number, not a date. Publish it only beside the cash columns.")


if __name__ == "__main__":
    main()
