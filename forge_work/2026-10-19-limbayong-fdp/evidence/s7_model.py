#!/usr/bin/env python3
"""
S7 Limbayong economics engine. Pure stdlib. Real 2026 USD, real discount rate.
Contractor-side (PCSB 100% WI) post-tax cash flow under a Malaysia Deepwater PSC.
"""
import json, math

# ---------------------------------------------------------------- config
YEARS = list(range(2026, 2046))
FIRST_OIL = 2030
END_PROD = 2043
BASE_BRENT = {2027: 84, 2028: 80, 2029: 77, 2030: 76}
for y in range(2031, 2046):
    BASE_BRENT[y] = 75
BRENT_2026 = 96.0  # EIA STEO Oct-2026 actual-ish

LIQ_MMBBL = 139.0
GAS_BCF = 790.9
BOE_PER_BCF = 1e6 / 6.0 / 1e6   # 1 bcf = 166,667 boe -> in MMboe: bcf*0.166667
GAS_MMBOE = GAS_BCF * 0.166667

LIQ_PLATEAU_BPD = 40_000
GAS_PLATEAU_MMSCFD = 150.0

CAPEX_TOTAL = 2900.0   # $M  (see build-up: wells 850 + subsea 600 + FPSO 485 + gas pipeline 650 + owners 315)
ABANDON = 200.0        # $M, 2045
OPEX_FIXED = 95.0      # $M/yr from first oil
OPEX_VAR = 4.00        # $/boe

ROYALTY = 0.10
CESS = 0.005
EXPORT_DUTY = 0.10     # on crude/condensate exported
SABAH_SST = 0.05       # on gas sold in Sabah
CR_CEIL_OIL = 0.70
CR_CEIL_GAS = 0.80
PIT = 0.38
CA_YEARS = 10
IA_RATE = 0.60         # PITA (Investment Allowances) Regs 2013 - deepwater >200m
IA_CAP = 0.70          # capped at 70% of statutory income per year
LIQ_DIFF = -1.00       # $/bbl vs Brent
GAS_PRICE = 6.50       # $/MMBtu


def shape(n, ramp, plateau_len, decline, start_idx):
    """unit profile: ramp fractions, plateau, exponential decline; returns list len(YEARS)."""
    prof = [0.0] * len(YEARS)
    i = start_idx
    for r in ramp:
        if i < len(prof):
            prof[i] = r
            i += 1
    for _ in range(plateau_len):
        if i < len(prof):
            prof[i] = 1.0
            i += 1
    d = 1.0
    while i < len(prof) and i - start_idx < n:
        d *= (1 - decline)
        prof[i] = d
        i += 1
    return prof


def build_profile(liq_scale=1.0, gas_scale=1.0, slip_years=0):
    fo = FIRST_OIL + slip_years
    s = YEARS.index(fo)
    lp = shape(18, [0.45, 0.85], 4, 0.17, s)
    gp = shape(18, [0.50, 0.88], 5, 0.13, s)
    # normalise to reserves
    lsum_bbl = sum(lp) * LIQ_PLATEAU_BPD * 365 / 1e6  # MMbbl if profile=1 at plateau
    gsum_bcf = sum(gp) * GAS_PLATEAU_MMSCFD * 365 / 1e6
    lmul = (LIQ_MMBBL * liq_scale) / lsum_bbl
    gmul = (GAS_BCF * gas_scale) / gsum_bcf
    liq = [p * LIQ_PLATEAU_BPD * 365 / 1e6 * lmul for p in lp]   # MMbbl/yr
    gas = [p * GAS_PLATEAU_MMSCFD * 365 / 1e6 * gmul for p in gp]  # bcf/yr
    return liq, gas


def capex_sched(slip_years=0, total=CAPEX_TOTAL):
    """FID Aug-2026. Phasing: 2026 5%, 2027 25%, 2028 40%, 2029 26%, 2030 4%."""
    base = {2026: 0.05, 2027: 0.25, 2028: 0.40, 2029: 0.26, 2030: 0.04}
    out = [0.0] * len(YEARS)
    for y, f in base.items():
        yy = y + slip_years
        if yy in YEARS:
            out[YEARS.index(yy)] += f * total
    return out


def run(price_mult=1.0, liq_scale=1.0, gas_scale=1.0, capex_mult=1.0,
        opex_mult=1.0, gas_price=GAS_PRICE, slip=0, ia_on=True, verbose=False):
    liq, gas = build_profile(liq_scale, gas_scale, slip)
    capex = capex_sched(slip, CAPEX_TOTAL * capex_mult)
    rows = []
    uncov = 0.0
    ca_pool = 0.0
    ca_remaining = 0.0
    ia_pool = 0.0
    loss_cf = 0.0
    for i, y in enumerate(YEARS):
        brent = BASE_BRENT.get(y, 75) * price_mult
        oil_rev = liq[i] * (brent + LIQ_DIFF)                   # MMbbl x $/bbl = $M
        gas_rev = gas[i] * 1.0371 * gas_price                  # bcf x 1.0371e6 MMBtu/bcf x $/MMBtu = $M
        gross = oil_rev + gas_rev
        roy = ROYALTY * gross
        cess = CESS * gross
        eduty = EXPORT_DUTY * oil_rev
        sst = SABAH_SST * gas_rev
        net = gross - roy - eduty - sst            # cost-recovery base
        base_oil = net * (oil_rev / gross) if gross > 0 else 0.0
        base_gas = net - base_oil
        opex = (OPEX_FIXED + OPEX_VAR * (liq[i] + gas[i] * 0.166667)) * opex_mult if liq[i] + gas[i] > 0 else 0.0
        # capex added to cost pool (excluding abandonment, which is non-recoverable here)
        cost_pool = uncov + opex + capex[i]
        ceil = CR_CEIL_OIL * base_oil + CR_CEIL_GAS * base_gas
        cost_oil = min(cost_pool, ceil)
        uncov = cost_pool - cost_oil
        profit = net - cost_oil
        # volume-based profit split (Deepwater PSC): oil 50% to 100 MMbbl cum, 60% beyond; gas 50%
        # compute cumulative liquids to date
        cum_liq = sum(liq[:i + 1])
        if cum_liq <= 100.0:
            ps_oil = 0.50
        else:
            ps_oil = 0.60
        ps_gas = 0.50
        p_oil = profit * (base_oil / net) if net > 0 else 0.0
        p_gas = profit - p_oil
        ent = cost_oil + ps_oil * p_oil + ps_gas * p_gas - cess
        host = profit - (ps_oil * p_oil + ps_gas * p_gas)   # PETRONAS profit share as host
        # ---- tax
        ca_pool += capex[i]
        ca_this = 0.0
        ia_pool += IA_RATE * capex[i]          # qualifying capex within 10 yrs of FDP approval
        # straight line over CA_YEARS from first production year
        if FIRST_OIL + slip <= y < FIRST_OIL + slip + CA_YEARS and ca_pool > 0:
            ca_this = ca_pool / CA_YEARS
        stat = ent - opex - ca_this - loss_cf
        if stat < 0:
            loss_cf = -stat
            stat = 0.0
        else:
            loss_cf = 0.0
        # investment allowance
        if y >= FIRST_OIL + slip:
            ia_pool += 0.0
        ia_pool = max(ia_pool, 0.0)
        exempt = min(IA_CAP * stat, ia_pool) if ia_on else 0.0
        ia_pool -= exempt
        tax = PIT * (stat - exempt)
        pt = ent - opex - capex[i] - tax
        rows.append(dict(year=y, liq=liq[i], gas=gas[i], boe=liq[i] + gas[i] * 0.166667,
                         oil_rev=oil_rev, gas_rev=gas_rev, gross=gross, roy=roy, cess=cess,
                         eduty=eduty, sst=sst, opex=opex, capex=capex[i], cost_oil=cost_oil,
                         profit=profit, ent=ent, host=host, ca=ca_this, ia=exempt, tax=tax, pt=pt,
                         uncov=uncov))
    # abandonment
    rows[-1]['capex'] += ABANDON
    rows[-1]['pt'] -= ABANDON
    return rows


def npv(rows, r=0.10, key='pt', start=2026):
    return sum(row[key] / (1 + r) ** (row['year'] - start) for row in rows)


def irr(rows, key='pt'):
    lo, hi = -0.95, 3.0
    for _ in range(200):
        mid = (lo + hi) / 2
        v = npv(rows, mid, key)
        if v > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def payback(rows, key='pt'):
    c = 0.0
    for row in rows:
        c += row[key]
        if c >= 0:
            return row['year']
    return None


def solve(fn, target, lo, hi, iters=80):
    for _ in range(iters):
        mid = (lo + hi) / 2
        v = fn(mid)
        if (v - target) * (fn(lo) - target) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


if __name__ == '__main__':
    rows = run()
    tot_capex = sum(r['capex'] for r in rows)
    tot_opex = sum(r['opex'] for r in rows)
    tot_boe = sum(r['boe'] for r in rows)
    print(f"total boe {tot_boe:.1f} MMboe  liq {sum(r['liq'] for r in rows):.1f} MMbbl gas {sum(r['gas'] for r in rows):.1f} bcf")
    print(f"capex {tot_capex:.0f} opex {tot_opex:.0f} gross rev {sum(r['gross'] for r in rows):.0f}")
    print(f"NPV10 {npv(rows):.0f}  IRR {irr(rows)*100:.1f}%  payback {payback(rows)}")
    print(f"UTC {(tot_capex+tot_opex)/tot_boe:.2f} $/boe")
    for r in rows:
        print(f"{r['year']} {r['boe']:6.1f} rev{r['gross']:8.1f} opex{r['opex']:6.1f} capex{r['capex']:7.1f} ent{r['ent']:7.1f} tax{r['tax']:6.1f} pt{r['pt']:8.1f}")
