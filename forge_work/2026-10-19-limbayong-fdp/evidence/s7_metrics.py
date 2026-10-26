#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/root/AAA/forge_work/2026-10-19-limbayong-fdp/evidence')
from s7_model import *

def metrics(**kw):
    rows = run(**kw)
    boe = sum(r['boe'] for r in rows)
    cap = sum(r['capex'] for r in rows)
    opex = sum(r['opex'] for r in rows)
    return dict(rows=rows, boe=boe, capex=cap, opex=opex,
                npv=npv(rows), irr=irr(rows), payback=payback(rows),
                utc=(cap + opex) / boe if boe else 0.0,
                gross=sum(r['gross'] for r in rows),
                tax=sum(r['tax'] for r in rows),
                roy=sum(r['roy'] for r in rows), cess=sum(r['cess'] for r in rows),
                eduty=sum(r['eduty'] for r in rows), sst=sum(r['sst'] for r in rows),
                ent=sum(r['ent'] for r in rows),
                netcf=sum(r['pt'] for r in rows))

b = metrics()
gov = b['roy'] + b['cess'] + b['eduty'] + b['sst'] + b['tax']
print("=== BASE ===")
print(f"boe {b['boe']:.1f}  capex {b['capex']:.0f}  opex {b['opex']:.0f}  gross {b['gross']:.0f}  ent {b['ent']:.0f}")
print(f"NPV10 {b['npv']:.0f}  IRR {b['irr']*100:.2f}%  payback {b['payback']}  UTC {b['utc']:.2f}")
print(f"roy {b['roy']:.0f} cess {b['cess']:.0f} eduty {b['eduty']:.0f} sst {b['sst']:.0f} tax {b['tax']:.0f}")
print(f"govt take {gov:.0f} = {gov/b['gross']*100:.1f}% of gross; contractor net CF {b['netcf']:.0f}")

# no-IA
n = metrics(ia_on=False)
print(f"NO investment allowance: NPV10 {n['npv']:.0f}  IRR {n['irr']*100:.2f}%  tax {n['tax']:.0f}  (IA worth {n['npv']-b['npv']:.0f} $M)")

# proper oil-only counterfactual: no gas, no pipeline
og = metrics(gas_scale=1e-9, capex_mult=2250/2900)
print(f"OIL ONLY (no gas, no pipeline, capex 2250): NPV10 {og['npv']:.0f} IRR {og['irr']*100:.2f}% UTC {og['utc']:.2f}")

# breakevens
def solve_root(f, lo, hi):
    for _ in range(120):
        mid = (lo + hi) / 2
        if f(mid) > 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2

m0 = solve_root(lambda m: npv(run(price_mult=m)), 0.05, 3.0)
print(f"\nNPV10=0 Brent: mult {m0:.4f} -> ${75*m0:.1f}/bbl (2030-35 ref), whole-path equivalent ${84*m0:.1f} at 2027")
m15 = solve_root(lambda m: irr(run(price_mult=m)) - 0.15, 0.2, 5.0)
print(f"IRR=15% Brent: mult {m15:.4f} -> ${75*m15:.1f}/bbl (2030-35 ref), ${84*m15:.1f} at 2027")

# reserves breakeven
rs = solve_root(lambda s: npv(run(liq_scale=s, gas_scale=s)), 0.02, 1.5)
print(f"Reserves breakeven (NPV10=0): scale {rs:.4f} -> {139*rs:.1f} MMbbl + {790.9*rs:.0f} bcf = {270.8*rs:.1f} MMboe")

# 15% IRR reserves
rs15 = solve_root(lambda s: irr(run(liq_scale=s, gas_scale=s)) - 0.15, 0.5, 6.0)
print(f"Reserves for 15% IRR: scale {rs15:.4f} -> {270.8*rs15:.1f} MMboe")

cases = [
 ('Oil price -25% ($56.3)',      dict(price_mult=0.75)),
 ('Oil price +25% ($93.8)',      dict(price_mult=1.25)),
 ('Reserves -30%',               dict(liq_scale=0.70, gas_scale=0.70)),
 ('Reserves +30%',               dict(liq_scale=1.30, gas_scale=1.30)),
 ('Capex +30%',                  dict(capex_mult=1.30)),
 ('Capex -30%',                  dict(capex_mult=0.70)),
 ('Opex +30%',                   dict(opex_mult=1.30)),
 ('Opex -30%',                   dict(opex_mult=0.70)),
 ('Schedule +18m (+8% capex)',   dict(slip=2, capex_mult=1.08)),
 ('Schedule -6m',                dict(slip=-1)),
 ('Gas price -40% ($3.90)',      dict(gas_price=GAS_PRICE*0.60)),
 ('Gas price +40% ($9.10)',      dict(gas_price=GAS_PRICE*1.40)),
]
out = []
print("\n=== TORNADO ===")
for k, v in cases:
    m = metrics(**v)
    out.append((k, m['npv'], m['npv']-b['npv'], m['irr']))
    print(f"{k:30s} NPV10 {m['npv']:8.0f}  dNPV {m['npv']-b['npv']:8.0f}  IRR {m['irr']*100:6.2f}%")

print("\n=== DECKS ===")
for name, mult in [('LOW  $55 flat', 55/75), ('BASE', 1.0), ('HIGH $90 flat', 90/75)]:
    m = metrics(price_mult=mult)
    print(f"{name:16s} NPV10 {m['npv']:8.0f} IRR {m['irr']*100:6.2f}% payback {m['payback']} UTC {m['utc']:.2f}")

print("\n=== CASHFLOW (base) ===")
cum = 0
for r in b['rows']:
    cum += r['pt']
    print(f"{r['year']}|{r['boe']:.2f}|{r['gross']:.0f}|{r['opex']:.0f}|{r['capex']:.0f}|{r['ent']:.0f}|{r['tax']:.0f}|{r['pt']:.0f}|{cum:.0f}")
print(f"\ntotal: boe {b['boe']:.1f} gross {b['gross']:.0f} capex {b['capex']:.0f} opex {b['opex']:.0f} ent {b['ent']:.0f} tax {b['tax']:.0f} net {b['netcf']:.0f}")
