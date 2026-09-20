#!/usr/bin/env python3
"""Size a Malaysian separation package from a formula the employer has supplied.

    python3 exit_package_calc.py --salary 20000 --years 13 --per-year 1.5 --flat 5 --burn 12000
    python3 exit_package_calc.py --salary 20000 --years 13 --cap 24 --salary-for-tax 240000
    python3 exit_package_calc.py --salary 20000 --years 13 --json

Inputs: the scheme's multiple (months of wages per completed year), any flat addition in months,
any total cap in months, the monthly base the multiple applies to, completed years of service, and
optionally the person's monthly burn and their other employment income for the year of receipt.

Outputs: months of wages, gross, exempt slice, taxable remainder, tax, net, the anniversary
step-up in ringgit, the extra tax from receiving the lump in a salaried year, and months of runway.

NOT tax advice, and it does not decide the case -- route the final figure to a licensed tax agent
(parent SKILL.md, Advisory stance 2). The RM10,000-per-completed-year exemption assumed here fails
ENTIRELY if the scheme expressly or impliedly provides for re-employment; check that clause first,
or every net figure below is wrong.
"""

from __future__ import annotations

import argparse
import json

# --- EDITABLE: Malaysia resident individual income tax, chargeable-income bands ----------
# (band width in MYR, rate applied to that band). VERIFY against the current tax-authority
# schedule for the YEAR OF RECEIPT before quoting any figure -- widths and rates move at budgets.
RESIDENT_BANDS = [
    (5_000, 0.00),
    (15_000, 0.01),
    (15_000, 0.03),
    (15_000, 0.06),
    (20_000, 0.11),
    (30_000, 0.19),
    (300_000, 0.25),
    (200_000, 0.26),
    (1_400_000, 0.28),
    (float("inf"), 0.30),
]

# RM10,000 x completed years of service, restricted to the amount received.
EXEMPT_PER_YEAR = 10_000


def tax_on(chargeable: float, bands=RESIDENT_BANDS) -> float:
    """Progressive tax on chargeable income."""
    if chargeable <= 0:
        return 0.0
    total, remaining = 0.0, chargeable
    for width, rate in bands:
        if remaining <= 0:
            break
        take = min(remaining, width)
        total += take * rate
        remaining -= take
    return total


def package_months(years: int, per_year: float, flat: float, cap: float | None):
    """Months of wages the formula produces, and the uncapped figure."""
    raw = per_year * years + flat
    return (min(raw, cap) if cap else raw), raw


def settled(salary, years, per_year, flat, cap, salary_for_tax=0.0, bands=RESIDENT_BANDS):
    """The whole package, after tax, for one exit date.

    salary_for_tax is the person's OTHER employment income in the year of receipt. With it set,
    'tax' is the marginal tax actually borne by the lump -- which is the number that prices a
    deferral. With it at zero, 'tax' is the tax on the lump alone in a clean year.
    """
    months, raw = package_months(years, per_year, flat, cap)
    gross = salary * months
    exempt = min(EXEMPT_PER_YEAR * years, gross)
    chargeable = max(0.0, gross - exempt)
    other = max(0.0, salary_for_tax)
    tax = tax_on(chargeable + other, bands) - tax_on(other, bands)
    return {
        "years": years,
        "months_of_wages": round(months, 2),
        "months_uncapped": round(raw, 2),
        "absorbed_by_cap": bool(cap and raw > cap),
        "gross": round(gross, 2),
        "exempt": round(exempt, 2),
        "taxable": round(chargeable, 2),
        "tax": round(tax, 2),
        "net": round(gross - tax, 2),
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Size a Malaysian separation package from a formula.")
    p.add_argument("--salary", type=float, required=True,
                   help="monthly BASE the multiple applies to (basic, not basic+allowances)")
    p.add_argument("--years", type=int, required=True, help="completed years of service")
    p.add_argument("--per-year", type=float, default=1.5, help="months of wages per completed year")
    p.add_argument("--flat", type=float, default=0.0, help="flat addition, in months")
    p.add_argument("--cap", type=float, default=None, help="total cap in months (0 or omit = none)")
    p.add_argument("--burn", type=float, default=None, help="monthly burn, for runway in months")
    p.add_argument("--salary-for-tax", type=float, default=0.0,
                   help="their other employment income in the year of receipt (annual, MYR)")
    p.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    a = p.parse_args()

    here = settled(a.salary, a.years, a.per_year, a.flat, a.cap, a.salary_for_tax)
    nxt = settled(a.salary, a.years + 1, a.per_year, a.flat, a.cap, a.salary_for_tax)
    clean = settled(a.salary, a.years, a.per_year, a.flat, a.cap, 0.0)

    out = {
        "exit_now": here,
        "exit_after_anniversary": nxt,
        "anniversary_step_up_net": round(nxt["net"] - here["net"], 2),
        "anniversary_step_up_gross": round(nxt["gross"] - here["gross"], 2),
        "lump_in_clean_year": clean,
        "cost_of_salaried_year_receipt": round(here["tax"] - clean["tax"], 2),
    }
    if a.burn:
        out["runway_months_net"] = round(here["net"] / a.burn, 1)
        out["runway_months_gross"] = round(here["gross"] / a.burn, 1)

    if a.json:
        print(json.dumps(out, indent=2))
        return

    m = here
    print("FORMULA  {:g} month(s) x {} completed year(s) + {:g} month(s)".format(
        a.per_year, a.years, a.flat))
    print("BASE     RM{:,.0f}/month  (basic -- confirm what 'one month's wages' means)".format(a.salary))
    print("PAYOUT   {} months of wages{}".format(
        m["months_of_wages"],
        " (uncapped would be {}, ABSORBED BY CAP)".format(m["months_uncapped"])
        if m["absorbed_by_cap"] else ""))
    print()
    print("  gross            RM{:>14,.0f}".format(m["gross"]))
    print("  exempt slice     RM{:>14,.0f}   (RM10,000 x {} years{})".format(
        m["exempt"], a.years, ", restricted to amount received" if m["exempt"] < 10_000 * a.years else ""))
    print("  taxable          RM{:>14,.0f}".format(m["taxable"]))
    print("  tax              RM{:>14,.0f}".format(m["tax"]))
    print("  net              RM{:>14,.0f}   ({:.0f}% of gross)".format(
        m["net"], 100 * m["net"] / m["gross"] if m["gross"] else 0))
    print()
    if m["absorbed_by_cap"]:
        print("CAP       binding -- waiting for the next service anniversary adds NOTHING.")
    else:
        print("ANNIVERSARY  exit after it: {} months, net RM{:,.0f}  (step-up RM{:,.0f} net / RM{:,.0f} gross)".format(
            nxt["months_of_wages"], nxt["net"],
            nxt["net"] - here["net"], nxt["gross"] - here["gross"]))
    print("RECEIPT YEAR  lump in a year with no salary: tax RM{:,.0f}. With RM{:,.0f} of other income: tax RM{:,.0f} (deferral worth RM{:,.0f}).".format(
        clean["tax"], a.salary_for_tax, here["tax"], here["tax"] - clean["tax"]))
    if a.burn:
        print("RUNWAY    net buys {:.1f} months at RM{:,.0f}/month burn (gross {:.1f}).".format(
            here["net"] / a.burn, a.burn, here["gross"] / a.burn))
    else:
        print("RUNWAY    unknown -- supply --burn. Monthly burn is the number the whole advisory turns on.")
    print()
    print("Verify the tax bands in RESIDENT_BANDS against the schedule for the year of receipt, and")
    print("confirm the scheme does not provide for re-employment (that can forfeit the exemption).")


if __name__ == "__main__":
    main()
