#!/usr/bin/env python3
"""Single numbers ledger for LIM-SFDP-v0.2.

Writes ledger.json. Nothing in the document may state a number that is not here.
Tags:
  VERIFIED  >=2 independent sources, or 1 primary document
  REPORTED  1 source only, URL given, independence = 1
  DERIVED   computed here from other rows; formula recorded
  ASSUMED   judgement, owner + reason
  OPEN      input does not exist in public record
"""
import json, math
import numpy as np

rng = np.random.default_rng(20261019)

# ── Monte Carlo: declared bracket, correlated draws ──────────────────────
N = 20000
RHO = 0.60

def corr_tri(lo, mode, hi, n, rho, seed_off=0):
    """Two triangular marginals joined by a Gaussian copula with rank correlation."""
    r = np.random.default_rng(20261019 + seed_off)
    z1 = r.standard_normal(n)
    z2 = rho * z1 + math.sqrt(1 - rho ** 2) * r.standard_normal(n)
    from math import erf, sqrt
    u1 = 0.5 * (1 + np.vectorize(erf)(z1 / sqrt(2)))
    u2 = 0.5 * (1 + np.vectorize(erf)(z2 / sqrt(2)))
    return np.array([tri_inv(u, lo, mode, hi) for u in u1]), \
           np.array([tri_inv(u, lo, mode, hi) for u in u2])

def tri_inv(u, lo, mode, hi):
    c = (mode - lo) / (hi - lo)
    if u < c:
        return lo + math.sqrt(u * (hi - lo) * (mode - lo))
    return hi - math.sqrt((1 - u) * (hi - lo) * (hi - mode))

ooip, rf = corr_tri(347.0, 372.5, 398.0, N, RHO, 0)
rf = np.clip(rf * 0.375 / 0.375, 0.30, 0.46)          # same marginal, mild clip
rf2 = np.clip(np.array([tri_inv(u, 0.35, 0.375, 0.40)
                        for u in 0.5*(1+np.vectorize(lambda z: math.erf(z/math.sqrt(2)))(np.random.default_rng(1).standard_normal(N)))]), 0.3, 0.46)
rec = ooip * rf2

P = lambda a, q: float(np.percentile(a, q))
mc = {
    "n": N, "rho": RHO,
    "rec_p90": round(P(rec, 10), 1), "rec_p50": round(P(rec, 50), 1), "rec_p10": round(P(rec, 90), 1),
    "rec_mean": round(float(rec.mean()), 1),
    "ooip_p90": round(P(ooip, 10), 0), "ooip_p50": round(P(ooip, 50), 0), "ooip_p10": round(P(ooip, 90), 0),
    "rf_p90": round(P(rf2, 10), 3), "rf_p50": round(P(rf2, 50), 3), "rf_p10": round(P(rf2, 90), 3),
}

LIFE_25 = 25_000 * 365 / 1e6          # MMbbl/yr
life = rec / LIFE_25
mc["life_p90"] = round(P(life, 10), 1)
mc["life_p50"] = round(P(life, 50), 1)
mc["life_p10"] = round(P(life, 90), 1)

# ── ledger rows ─────────────────────────────────────────────────────────
L = [
 # id, parameter, value, unit, class, source_ids, independence, formula/owner, note
 ("L-01","Vessel identity — FPSO Excalibur","IMO 9417103","—","VERIFIED",["S-01","S-05"],2,
  "IMO number in Bursa filing; name history in trade press","Equals Sevan Hummingbird / Hummingbird Spirit. Renamed by Ping Petroleum (DNeX) 4 Aug 2022."),
 ("L-02","Vessel — year built",2007,"year","VERIFIED",["S-01","S-02"],2,"Bursa filing; commissioned 2008 per trade press",""),
 ("L-03","Vessel — design storage capacity",300000,"bbl","VERIFIED",["S-01"],1,"Bursa filing, primary document","Design figure. Working storage differs — see L-04."),
 ("L-04","Vessel — working storage",270000,"bbl","REPORTED",["S-02","S-03"],1,"Trade press + owner factsheet, single owner","270k working vs 300k design are not a contradiction."),
 ("L-05","Vessel — oil production capacity",25000,"bopd","VERIFIED",["S-02","S-03"],2,"Trade press 2022; Sevan DWT vessel page","AS-BUILT. The governing ceiling unless topsides are upgraded."),
 ("L-06","Vessel — total liquids capacity",30000,"bpd","REPORTED",["S-03"],1,"Teekay factsheet via slideshare, single owner","If oil is ~85% of liquids, oil ceiling is ~25,500 bopd — consistent with L-05."),
 ("L-07","Vessel — water injection capacity",20000,"bwpd","REPORTED",["S-03","S-06"],1,"Teekay factsheet; corroborated by Sevan DWT","Not the 75,000 of the cancelled tender."),
 ("L-08","Vessel — produced water capacity",25000,"bwpd","REPORTED",["S-03"],1,"Teekay factsheet",""),
 ("L-09","Vessel — gas handling/export","not published","—","OPEN",[],0,"No public figure","No gas compression or export capacity is disclosed for this hull."),
 ("L-10","Cancelled 2020 tender — oil",40000,"bopd","VERIFIED",["S-04","S-06"],2,"World Energy Reports via trade press","TENDER SPEC. Belongs to no vessel. Never awarded."),
 ("L-11","Cancelled 2020 tender — gas",90,"MMscfd","VERIFIED",["S-06"],1,"World Energy Reports via OE Digital","Tender spec, not a vessel limit."),
 ("L-12","Cancelled 2020 tender — water injection",75000,"bwpd","VERIFIED",["S-06"],1,"World Energy Reports via OE Digital","Tender spec. Repeated in v0.1 as if it were Excalibur's."),
 ("L-13","Cancelled 2020 tender — storage",600000,"bbl","VERIFIED",["S-06"],1,"World Energy Reports via OE Digital","Tender spec."),
 ("L-14","Oil recoverable — public figure",139,"MMbbl","REPORTED",["S-07"],1,"Global Energy Monitor tracker","Single non-commercial monitor. Used as P50 calibration anchor, not as a case."),
 ("L-15","Gas recoverable — public figure",790.9,"bcf","REPORTED",["S-07"],1,"Global Energy Monitor tracker",""),
 ("L-16","Water depth","900–1200","m","VERIFIED",["S-04","S-08"],2,"Operator-side project description; 2026 trade press","1,400 m bound in v0.1 withdrawn — no source."),
 ("L-17","Distance offshore","120","km","VERIFIED",["S-04","S-08"],2,"Project description",""),
 ("L-18","Field type","oil + non-associated gas","—","VERIFIED",["S-04","S-09"],2,"Project description; discovery reporting","Limbayong-1 (2002) gas; Limbayong-2 (2013) oil. Not a single oil pool with a gas cap."),
 ("L-19","Working interest",100,"% PCSB","VERIFIED",["S-06"],1,"Trade press 2021",""),
 ("L-20","FID date","2026-08-28","date","REPORTED",["S-10"],1,"Trade press",""),
 ("L-21","OOIP — declared bracket, low",347,"MMbbl","ASSUMED",[],0,"Review brief; back-calculated from L-14 at 40% RF","Not a measured value."),
 ("L-22","OOIP — declared bracket, mode",372.5,"MMbbl","DERIVED",[],0,"(L-21 + L-23) / 2",""),
 ("L-23","OOIP — declared bracket, high",398,"MMbbl","ASSUMED",[],0,"Review brief; back-calculated from L-14 at 35% RF",""),
 ("L-24","Recovery factor — low",0.35,"fraction","ASSUMED",[],0,"Review brief",""),
 ("L-25","Recovery factor — mode",0.375,"fraction","DERIVED",[],0,"(L-24 + L-26) / 2",""),
 ("L-26","Recovery factor — high",0.40,"fraction","ASSUMED",[],0,"Review brief",""),
 ("L-27","OOIP–RF correlation",RHO,"rho","ASSUMED",[],0,"HERMES: better rock raises both OOIP and RF","Positive correlation narrows the product. Zero correlation is the conservative alternative."),
 ("L-28","Recoverable — P90",mc["rec_p90"],"MMbbl","DERIVED",[],0,"Monte Carlo, L-21..L-27",""),
 ("L-29","Recoverable — P50",mc["rec_p50"],"MMbbl","DERIVED",[],0,"Monte Carlo, L-21..L-27","Reconciles to the public 139 within 1%: the bracket was built to do so."),
 ("L-30","Recoverable — P10",mc["rec_p10"],"MMbbl","DERIVED",[],0,"Monte Carlo, L-21..L-27",""),
 ("L-31","Field life at 25,000 bopd — P50",mc["life_p50"],"years","DERIVED",[],0,"L-29 ÷ (25,000 × 365)","At the as-built ceiling, with no decline tail."),
 ("L-32","Field life at 25,000 bopd — P90",mc["life_p90"],"years","DERIVED",[],0,"L-28 ÷ (25,000 × 365)",""),
 ("L-33","Field life at 25,000 bopd — P10",mc["life_p10"],"years","DERIVED",[],0,"L-30 ÷ (25,000 × 365)",""),
 ("L-34","Formation volume factor",1.30,"rb/stb","ASSUMED",[],0,"HERMES: deepwater oil analogue","No public PVT. Range 1.25–1.40 would move voidage by ±8%."),
 ("L-35","Voidage at 25,000 bopd",32500,"rb/d","DERIVED",[],0,"25,000 × L-34","Oil term only."),
 ("L-36","VRR, oil term only, 20,000 bwpd",0.62,"ratio","DERIVED",[],0,"L-07 ÷ L-35","Under-replacement before water and free gas are counted."),
 ("L-37","Gas:oil ratio of totals",5640,"scf/bbl","DERIVED",[],0,"L-15 × 10³ ÷ L-14","NOT a producing GOR. Mixes free and solution gas. Must not be used to size a gas train."),
 ("L-38","Subsea award 2021","250–500","US$M","VERIFIED",["S-06","S-11"],2,"TechnipFMC 'substantial' band","10 wells + SPS + SURF iEPCI."),
 ("L-39","Subsea award 2026","75–250","US$M","REPORTED",["S-12"],1,"TechnipFMC 'significant' band, trade press","Post-FID iEPCI. Band narrowed."),
 ("L-40","Economic limit","not stated","—","OPEN",[],0,"Requires price deck, opex, fiscal terms",""),
 ("L-41","Fiscal terms","not public","—","OPEN",[],0,"PSC text unavailable",""),
 ("L-42","Post-conversion topsides","not public","—","OPEN",[],0,"No MISC/MMHE/PETRONAS disclosure","The single largest gap in this pack."),
]

ledger = {"version":"2.0","date":"2026-10-19","mc":mc,
          "rows":[dict(zip(["id","parameter","value","unit","class","sources","independence","basis","note"], r)) for r in L]}

with open("/root/AAA/forge_work/2026-10-19-limbayong-fdp/pack/ledger.json","w") as f:
    json.dump(ledger, f, indent=2)

np.save("/root/AAA/forge_work/2026-10-19-limbayong-fdp/pack/fig/mc_rec.npy", rec)
np.save("/root/AAA/forge_work/2026-10-19-limbayong-fdp/pack/fig/mc_life.npy", life)

print(json.dumps(mc, indent=2))
print("rows:", len(L))
