
"""Limbayong FDP — HERMES CEO independent screening model.
All assumptions are classed in the report. This model exists to CROSS-CHECK
the delegated sections, not to replace them.
"""
CAPEX_BASE = 3169.0  # USD million, AACE class 4 central
SPEND = {2027:0.15, 2028:0.40, 2029:0.30, 2030:0.15}

def profile(plat=66000, start=2029, plat_years=6, decl=0.14):
    out=[]
    for i,y in enumerate(range(start, start+20)):
        if i==0: r=plat*0.35
        elif i==1: r=plat*0.70
        elif i < 2+plat_years: r=plat
        else: r=plat*((1-decl)**(i-(1+plat_years)))
        if r<2500: break
        out.append((y,r))
    return out

def npv(cfs, rate=0.10, base=2026):
    return sum(cf/((1+rate)**(y-base)) for y,cf in cfs)

def irr(cfs, base=2026):
    lo,hi=-0.95,3.0
    for _ in range(400):
        mid=(lo+hi)/2
        v=sum(cf/((1+mid)**(y-base)) for y,cf in cfs)
        if v>0: lo=mid
        else: hi=mid
    return (lo+hi)/2

def model(brent=70, opex_boe=12, gas_price=6.0, capex=None, delay=0, plat=66000,
          gas_share=0.393, cr_cap=0.70, profit_share=0.70, pita=0.38, export_duty=0.05):
    capex = CAPEX_BASE if capex is None else capex
    prof = profile(plat, 2029+delay)
    oild = (brent-5)*(1-export_duty)
    cfs = [(y, -capex*SPEND[y]) for y in SPEND]
    cum_cost = 0.0
    for y,r in prof:
        boe = r*365/1e6
        rev = boe*(1-gas_share)*oild + boe*gas_share*5.8*gas_price
        opex = boe*opex_boe
        cum_cost += capex*SPEND.get(y,0.0) + opex
        recoverable = min(cum_cost, rev*cr_cap)
        cum_cost -= recoverable
        profit = rev - recoverable
        contractor_profit = profit*profit_share
        tax = max(0.0, contractor_profit)*pita
        cfs.append((y, recoverable + contractor_profit - opex - tax))
    return npv(cfs), irr(cfs), cfs
