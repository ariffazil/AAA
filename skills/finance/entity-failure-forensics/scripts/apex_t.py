#!/usr/bin/env python3
"""
apex_t.py — distance-to-failure (T) from reported balance sheets.

    D = ln(assets / liabilities)          gap to the contractual barrier
    lambda = rate the gap is closing      estimated from a trailing window
    T = D / lambda                        time to the barrier

lambda <= 0 means the gap is NOT closing -> T is unbounded (inf).

CORRECTNESS NOTE — read before trusting any output
--------------------------------------------------
First-passage is governed by the LONG-run drift. A trust-decay term written as
max(0, g_long - mu_short) returns T = inf for every observation whose short-run
momentum exceeds its long-run trend — which silently drops one whole quadrant of
the panel. In the origin run that was ~50% of all observations, and every one of
them sat in the quadrant the author expected to be most dangerous.

Infinite values clustered in one category are a BUG SIGNATURE, not a finding.
`summarise()` prints the infinity count for this reason. Read it before reading
any median.

Usage
-----
    python3 apex_t.py --selftest
    python3 apex_t.py --csv panel.csv --assets assets --liab liabilities
    python3 apex_t.py --csv panel.csv --assets assets --equity equity

Expected CSV columns: a period identifier (numeric year), plus the asset figure
and either liabilities or equity. Optional: ocf (operating cash flow) to apply the
cash-burn amplifier. Rows are grouped by an optional `entity` column.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys

INF = float("inf")


def distance(assets: float, liabilities: float) -> float:
    """D = ln(assets / liabilities). Returns nan for non-positive inputs."""
    if assets is None or liabilities is None:
        return float("nan")
    if assets <= 0 or liabilities <= 0:
        return float("nan")
    return math.log(assets / liabilities)


def closing_rate(d_prev: float, d_now: float, years: float) -> float:
    """lambda = -(d_now - d_prev) / years.

    Positive lambda == the gap is closing (the entity is approaching the barrier).
    """
    if d_prev is None or d_now is None or years is None or years <= 0:
        return float("nan")
    if not (math.isfinite(d_prev) and math.isfinite(d_now)):
        return float("nan")
    return -(d_now - d_prev) / years


def t_score(d: float, lam: float, ocf: float | None = None,
            assets: float | None = None, burn_cap: float = 0.6) -> float:
    """T = D / lambda, accelerated when operating cash flow is negative.

    lambda <= 0  ->  INF (the gap is not closing; the question is ill-posed)
    """
    if d is None or lam is None:
        return float("nan")
    if not (math.isfinite(d) and math.isfinite(lam)):
        return float("nan")
    if lam <= 1e-6:
        return INF
    base = d / lam
    if ocf is not None and ocf < 0 and assets and assets > 0:
        burn = min(abs(ocf) / assets, burn_cap)
        base = base / (1.0 + burn)
    return base


def cash_conversion(ocf: float | None, pat: float | None) -> float:
    """OCF / reported profit. Only meaningful when profit is positive."""
    if ocf is None or pat is None or pat <= 0:
        return float("nan")
    return ocf / pat


def cash_coverage(cash: float | None, borrowings: float | None) -> float:
    """Cash and equivalents / total borrowings."""
    if cash is None or borrowings is None or borrowings <= 0:
        return float("nan")
    return cash / borrowings


# ---------------------------------------------------------------- series build

def build_series(periods, assets, liabilities, ocf=None, window=3):
    """Return [{period, D, lambda, T, ...}] for one entity.

    `periods` must be numeric and sorted ascending. Rows with a non-finite D are
    emitted with D=nan and NO lambda/T — they are kept so the gap is visible
    downstream rather than silently dropped.
    """
    n = len(periods)
    out = []
    for i in range(n):
        d = distance(assets[i], liabilities[i])
        lam = float("nan")
        if i >= window:
            yrs = periods[i] - periods[i - window]
            lam = closing_rate(out[i - window]["D"], d, yrs)
        o = ocf[i] if ocf is not None else None
        out.append({
            "period": periods[i],
            "assets": assets[i],
            "liabilities": liabilities[i],
            "D": d,
            "lambda": lam,
            "T": t_score(d, lam, o, assets[i]),
        })
    return out


def summarise(series, label=""):
    """Print the diagnostics you must read BEFORE interpreting any median."""
    finite = [r for r in series if math.isfinite(r["T"])]
    infs = [r for r in series if r["T"] == INF]
    nans = [r for r in series if math.isnan(r["T"])]
    ts = sorted(r["T"] for r in finite)
    med = ts[len(ts) // 2] if ts else float("nan")
    print(f"{label}")
    print(f"  observations        : {len(series)}")
    print(f"  finite T            : {len(finite)}")
    print(f"  infinite T (lambda<=0): {len(infs)}")
    print(f"  no T (missing data) : {len(nans)}")
    print(f"  median finite T     : {med:.2f}" if ts else "  median finite T     : n/a")
    if infs and len(infs) > 0.4 * len(series):
        print("  !! >40% of observations returned T=inf.")
        print("     Check whether they cluster in one category — that is a formula")
        print("     bug, not a finding. See the module docstring.")
    return {"n": len(series), "finite": len(finite), "inf": len(infs), "median": med}


# ------------------------------------------------------------------- plotting

def gap_aware_plot(ax, x, y, **kw):
    """Plot only contiguous runs of finite values; leave gaps as gaps.

    Never interpolate or connect across a missing period. A connected line makes an
    unreported or unaudited stretch look continuous — which is exactly the illusion
    a failure analysis exists to detect.
    """
    xs, ys = list(x), list(y)
    run_x, run_y = [], []
    for xi, yi in zip(xs, ys):
        ok = yi is not None and isinstance(yi, (int, float)) and math.isfinite(yi)
        if ok:
            run_x.append(xi)
            run_y.append(yi)
        else:
            if run_x:
                ax.plot(run_x, run_y, **kw)
            run_x, run_y = [], []
    if run_x:
        ax.plot(run_x, run_y, **kw)
    return ax


# ------------------------------------------------------------------ csv loader

def load_csv(path, assets_col, liab_col, entity_col=None, period_col=None,
             ocf_col=None, window=3):
    """Load a panel CSV and build T series per entity (or as a single series)."""
    groups = {}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            key = row.get(entity_col, "_") if entity_col else "_"
            try:
                period = float(row[period_col]) if period_col else float(len(groups.get(key, [])))
                a = float(row[assets_col])
                l = float(row[liab_col])
            except (KeyError, TypeError, ValueError):
                continue
            o = None
            if ocf_col:
                try:
                    o = float(row[ocf_col])
                except (KeyError, TypeError, ValueError):
                    o = None
            groups.setdefault(key, []).append((period, a, l, o))

    out = {}
    for key, rows in groups.items():
        rows.sort(key=lambda r: r[0])
        periods = [r[0] for r in rows]
        assets = [r[1] for r in rows]
        liabs = [r[2] for r in rows]
        ocfs = [r[3] for r in rows]
        ocfs = ocfs if any(o is not None for o in ocfs) else None
        out[key] = build_series(periods, assets, liabs, ocfs, window)
    return out


# --------------------------------------------------------------------- selftest

def _selftest():
    ok = True

    def check(name, got, want, tol=1e-9):
        nonlocal ok
        if isinstance(want, float) and math.isfinite(want) and isinstance(got, float) and math.isfinite(got):
            good = abs(got - want) <= tol
        else:
            good = got == want
        print(f"  [{'ok' if good else 'FAIL'}] {name}: got={got!r} want={want!r}")
        ok = ok and good

    check("distance(100,50)", distance(100, 50), math.log(2))
    check("distance(50,100) is negative", distance(50, 100) < 0, True)
    check("distance guards zero", math.isnan(distance(0, 10)), True)
    check("closing_rate closes", closing_rate(0.7, 0.4, 3), 0.1)
    check("closing_rate widens is negative", closing_rate(0.4, 0.7, 3) < 0, True)
    check("t_score basic", t_score(0.4, 0.1), 4.0)
    check("t_score lambda<=0 -> inf", t_score(0.4, -0.01), INF)
    check("t_score lambda=0 -> inf", t_score(0.4, 0.0), INF)
    check("t_score burn amplifier shortens", t_score(0.4, 0.1, -50.0, 100.0) < 4.0, True)
    check("cash_conversion needs positive profit", math.isnan(cash_conversion(10, -5)), True)
    check("cash_conversion normal", cash_conversion(120, 100), 1.2)
    check("cash_coverage", cash_coverage(50, 100), 0.5)

    # gap awareness: a nan must break the run, not be skipped
    ser = build_series([2018, 2019, 2020, 2021],
                       [100, 90, None, 70],
                       [50, 55, None, 60],
                       window=1)
    check("nan row preserved in series", math.isnan(ser[2]["D"]), True)
    check("nan row has no T", math.isnan(ser[2]["T"]), True)
    check("finite rows still scored", math.isfinite(ser[1]["T"]), True)

    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Distance-to-failure (T) from balance sheets.")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--csv")
    p.add_argument("--assets", default="assets")
    p.add_argument("--liab", default="liabilities")
    p.add_argument("--equity", help="derive liabilities as assets - equity")
    p.add_argument("--entity", default="entity")
    p.add_argument("--period", default="fy")
    p.add_argument("--ocf")
    p.add_argument("--window", type=int, default=3)
    a = p.parse_args(argv)

    if a.selftest:
        return _selftest()
    if not a.csv:
        p.print_help()
        return 2

    if a.equity:
        # materialise a liability column, then reuse the same loader
        rows = []
        with open(a.csv, newline="") as fh:
            rd = csv.DictReader(fh)
            fields = list(rd.fieldnames or []) + ["_liab"]
            for r in rd:
                try:
                    r["_liab"] = float(r[a.assets]) - float(r[a.equity])
                except (KeyError, TypeError, ValueError):
                    r["_liab"] = ""
                rows.append(r)
        tmp = a.csv + ".liab.csv"
        with open(tmp, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        a.csv, a.liab = tmp, "_liab"

    series = load_csv(a.csv, a.assets, a.liab, a.entity, a.period, a.ocf, a.window)
    for key, s in series.items():
        summarise(s, label=f"entity={key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
