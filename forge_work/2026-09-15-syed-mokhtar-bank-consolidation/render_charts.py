#!/usr/bin/env python3
"""Render charts for the Bank Muamalat / Syed Mokhtar banking consolidation brief."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

BASE = "/root/AAA/forge_work/2026-09-15-syed-mokhtar-bank-consolidation"
CH = os.path.join(BASE, "charts")
os.makedirs(CH, exist_ok=True)
D = json.load(open(os.path.join(BASE, "data/dataset.json")))

NAVY = "#0d2b45"; TEAL = "#1b7f79"; AMBER = "#d98324"; RED = "#b3402f"
GREY = "#6b7280"; LGREY = "#d9dee3"; GREEN = "#2f7d4f"

plt.rcParams.update({
    "figure.dpi": 140, "savefig.dpi": 140, "font.size": 10.5,
    "axes.edgecolor": LGREY, "axes.labelcolor": NAVY, "text.color": NAVY,
    "xtick.color": GREY, "ytick.color": GREY, "axes.titlecolor": NAVY,
    "axes.grid": True, "grid.color": LGREY, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "font.family": "DejaVu Sans",
})

def finish(fig, name, title, source, sub=None):
    fig.suptitle(title, fontsize=13.5, fontweight="bold", x=0.012, ha="left", y=0.985)
    if sub:
        fig.text(0.012, 0.935, sub, fontsize=9.6, color=GREY, ha="left")
    fig.text(0.012, 0.012, "Source: " + source, fontsize=7.8, color=GREY, ha="left")
    fig.savefig(os.path.join(CH, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("ok", name)

# 1 — ranking of Islamic banking assets
def c01():
    d = D["market_structure"]["islamic_bank_assets_comparison_rm_bn"]
    labels = ["Maybank Islamic\n(subsidiary of Maybank)", "Bank Rakyat\n(co-operative / DFI)",
              "Bank Islam\n(largest standalone)", "MBSB Bank", "Bank Muamalat", "Al Rajhi Malaysia"]
    vals = [d["Maybank Islamic (subsidiary)"], d["Bank Rakyat (cooperative/DFI)"],
            d["Bank Islam (largest standalone)"], d["MBSB Bank"], d["Bank Muamalat"], d["Al Rajhi Malaysia"]]
    cols = [NAVY, GREY, TEAL, AMBER, RED, LGREY]
    fig, ax = plt.subplots(figsize=(9.6, 4.3))
    y = np.arange(len(vals))[::-1]
    ax.barh(y, vals, color=cols, height=0.62)
    for yy, v in zip(y, vals):
        ax.text(v + 6, yy, f"{v:,.1f}", va="center", fontsize=9.4, color=NAVY, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Total assets (RM billion)")
    ax.set_xlim(0, 430)
    ax.axvline(d["Bank Islam (largest standalone)"], color=TEAL, ls=":", lw=1.1)
    finish(fig, "c01_ranking.png",
           "Malaysia's Islamic banking asset ladder — three different 'largest' claims",
           "Fitch (Feb 2026); The Edge (Sep 2026); Bank Rakyat (FY2025); Bank Islam 2Q26; MBSB Bank 2026; MARC (Aug 2026)",
           "Only Bank Islam, MBSB Bank and Bank Muamalat are standalone full-fledged Islamic banks. Bank Rakyat is a co-operative; Maybank Islamic is a subsidiary. 16 Islamic banks + 1 international + 2 Islamic DFIs licensed.")

# 2 — combination scenarios
def c02():
    c = D["combinations_rm_bn"]
    keys = list(c.keys())
    vals = [c[k] for k in keys]
    order = np.argsort(vals)[::-1]
    keys = [keys[i] for i in order]; vals = [vals[i] for i in order]
    fig, ax = plt.subplots(figsize=(9.6, 3.9))
    x = np.arange(len(vals))
    ax.bar(x, vals, color=[TEAL, AMBER, RED, GREY, NAVY], width=0.58)
    ax.axhline(106.7, color=TEAL, ls="--", lw=1.3)
    ax.text(len(vals) - 0.45, 109, "Bank Islam today: RM107bn", fontsize=8.8, color=TEAL, ha="right")
    ax.axhline(390, color=NAVY, ls="--", lw=1.3)
    ax.text(len(vals) - 0.45, 393, "Maybank Islamic: RM390bn", fontsize=8.8, color=NAVY, ha="right")
    for xx, v in zip(x, vals):
        ax.text(xx, v + 5, f"{v:,.1f}", ha="center", fontsize=9.4, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(keys, fontsize=8.6)
    ax.set_ylabel("Combined total assets (RM billion)"); ax.set_ylim(0, 430)
    finish(fig, "c02_combinations.png",
           "The 'largest Islamic bank' claim only holds in one narrow lane",
           "DER from MBSB (1Q26), Bank Muamalat (Dec 2025), Bank Islam (Jun 2026), Affin Islamic (1Q26), Bank Rakyat (FY2025)",
           "Only MBSB Bank + Bank Muamalat crosses Bank Islam's RM107bn — by RM3.4bn, or 3%. Nothing in this set approaches Maybank Islamic.")

# 3 — BMMB asset trajectory
def c03():
    d = D["bank_muamalat"]["assets_rm_bn"]
    k = list(d.keys()); v = [d[x] for x in k]
    fig, ax = plt.subplots(figsize=(9.6, 3.5))
    ax.plot(k, v, marker="o", color=TEAL, lw=2.2, ms=7)
    for kk, vv in zip(k, v):
        ax.annotate(f"{vv:,.1f}", (kk, vv), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9.4, fontweight="bold")
    ax.set_ylabel("Total assets (RM billion)"); ax.set_ylim(15, 54)
    finish(fig, "c03_assets_trajectory.png",
           "Bank Muamalat — asset growth has stalled into a crawl",
           "The Edge (Feb 2024, Jul 2024); MARC Ratings (Aug 2026)",
           "Growth: 22.9bn (FY17) -> 31.5bn (FY22) -> 45.7bn (Dec-25). Financing growth collapsed from 14.1% (2024) to 4.6% (2025) — below the 7.9% Islamic sector average.")

# 4 — financing growth
def c04():
    d = D["bank_muamalat"]["financing_growth_pct"]
    k = ["FY2022", "FY2023", "FY2024", "FY2025"]
    v = [d[x] for x in k]
    fig, ax = plt.subplots(figsize=(9.6, 3.4))
    x = np.arange(len(k))
    ax.bar(x, v, color=[TEAL, TEAL, AMBER, RED], width=0.5)
    ax.axhline(d["sector_FY2025"], color=NAVY, ls="--", lw=1.2)
    ax.text(len(k) - 0.5, d["sector_FY2025"] + 0.4, "Islamic sector FY2025: 7.9%", fontsize=8.8, color=NAVY, ha="right")
    for xx, vv in zip(x, v):
        ax.text(xx, vv + 0.4, f"{vv:.1f}%", ha="center", fontsize=9.6, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(k)
    ax.set_ylabel("Financing growth (% YoY)"); ax.set_ylim(0, 21)
    finish(fig, "c04_financing_growth.png",
           "Bank Muamalat fell below the sector for the first time — the scale problem, made visible",
           "MARC Ratings (Aug 2026); The Edge (Jul 2024)",
           "Aggressive double-digit growth 2022-24; abrupt deceleration in 2025. Size is not the binding constraint — funding cost and asset quality are.")

# 5 — GIF ratio
def c05():
    d = D["bank_muamalat"]["gif_pct"]
    k = ["FY2018", "FY2022", "FY2023", "FY2024", "FY2025", "1Q2026"]
    v = [d[x] for x in k]
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.plot(k, v, marker="s", color=RED, lw=2.2, ms=7)
    ax.axhline(d["industry_FY2023"], color=NAVY, ls="--", lw=1.2)
    ax.text(0.02, d["industry_FY2023"] + 0.03, "Industry average (FY2023): 1.69%", fontsize=8.8, color=NAVY)
    for kk, vv in zip(k, v):
        ax.annotate(f"{vv:.2f}%", (kk, vv), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9.2, fontweight="bold")
    ax.set_ylabel("Gross impaired financing (%)"); ax.set_ylim(0.6, 1.95)
    finish(fig, "c05_gif_ratio.png",
           "Asset quality reversed: from best-in-class to worse-than-industry",
           "MARC Ratings (Aug 2026); The Edge (Jul 2024)",
           "After the early-2025 fraud incident (~RM100m of accounts routed to AKPK), BMMB's GIF ratio exceeded the industry average for the first time in recent years.")

# 6 — PBT
def c06():
    d = D["bank_muamalat"]["pbt_rm_m"]
    k = ["FY2022", "FY2024", "FY2025", "1H2026 (annualised)"]
    v = [d["FY2022"], d["FY2024"], d["FY2025"], d["1H2026"] * 2]
    fig, ax = plt.subplots(figsize=(9.6, 3.4))
    x = np.arange(len(k))
    ax.bar(x, v, color=[TEAL, GREY, GREEN, AMBER], width=0.5)
    for xx, vv in zip(x, v):
        ax.text(xx, vv + 7, f"{vv:,.1f}", ha="center", fontsize=9.6, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(k, fontsize=9)
    ax.set_ylabel("Profit before tax (RM million)"); ax.set_ylim(0, 370)
    finish(fig, "c06_pbt_series.png",
           "Bank Muamalat profit — a record year, then an immediate fade",
           "MARC Ratings (Aug 2026); The Star (26 Aug 2026); The Edge (Feb 2024)",
           "FY2022 figure is profit before zakat and tax. FY2024 carried elevated provisions on a large legacy account; FY2025 rebounded on a RM75.7m release. 1H26 annualisation is indicative only.")

# 7 — capital
def c07():
    d = D["bank_muamalat"]["capital_pct"]
    cats = ["CET1", "Tier 1", "Total capital"]
    dec = [d["CET1_Dec2025"], d["Tier1_Dec2025"], d["Total_Dec2025"]]
    jun = [d["CET1_Jun2026"], d["Tier1_Jun2026"], d["Total_Jun2026"]]
    x = np.arange(3); w = 0.34
    fig, ax = plt.subplots(figsize=(9.6, 3.4))
    ax.bar(x - w/2, dec, w, label="31 Dec 2025", color=NAVY)
    ax.bar(x + w/2, jun, w, label="30 Jun 2026", color=AMBER)
    for xx, vv in zip(x - w/2, dec): ax.text(xx, vv + 0.25, f"{vv:.2f}%", ha="center", fontsize=9)
    for xx, vv in zip(x + w/2, jun): ax.text(xx, vv + 0.25, f"{vv:.2f}%", ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(cats); ax.set_ylabel("% of risk-weighted assets")
    ax.set_ylim(0, 21); ax.legend(frameon=False, fontsize=9)
    finish(fig, "c07_capital.png",
           "Capital is adequate but drifting down — thin headroom for an acquisition currency",
           "Bank Muamalat Pillar 3 Disclosures, 1H ended 30 June 2026",
           "CET1 eased to 12.02% from 12.27%. Adequate against regulatory minima, but BMMB cannot buy another bank with its own paper without diluting shareholders who have no listed stock to trade.")

# 8 — funding mix
def c08():
    f = D["bank_muamalat"]["funding"]
    labels = ["Customer deposits\n(% of total funding)", "CASA ratio", "Top-20 depositor\nconcentration",
              "Retail (% of deposits\n+ investment accounts)", "Wholesale / other\nfunding"]
    vals = [f["deposits_pct_of_funding"], f["casa_pct"], f["top20_depositor_pct"], f["retail_pct_of_deposits_and_IA"],
            100 - f["deposits_pct_of_funding"]]
    cols = [TEAL, GREEN, RED, AMBER, GREY]
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    x = np.arange(len(vals))
    ax.bar(x, vals, color=cols, width=0.55)
    for xx, vv in zip(x, vals):
        ax.text(xx, vv + 1.2, f"{vv:.1f}%", ha="center", fontsize=9.6, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8.4)
    ax.set_ylabel("%"); ax.set_ylim(0, 100)
    finish(fig, "c08_funding_mix.png",
           "The structural weakness is funding, not capital: a small retail base and one concentrated wholesale book",
           "Bank Muamalat Pillar 3 / MARC Ratings (1Q2026 data, Aug 2026)",
           "CASA above industry average is the strength. A 47% top-20 depositor concentration and only 12% retail funding is the fragility — and the main reason a merger with a retail-heavy partner is strategically attractive.")

# 9 — liquidity
def c09():
    f = D["bank_muamalat"]["funding"]
    fig, ax = plt.subplots(figsize=(9.6, 3.2))
    metrics = ["Liquidity coverage\nratio (LCR)", "Net stable funding\nratio (NSFR)"]
    vals = [f["lcr_pct"], f["nsfr_pct"]]
    mins = [100, 100]
    x = np.arange(2); w = 0.32
    ax.bar(x - w/2, vals, w, color=TEAL, label="Actual (1Q2026)")
    ax.bar(x + w/2, mins, w, color=GREY, label="Regulatory minimum")
    for xx, vv in zip(x - w/2, vals): ax.text(xx, vv + 3, f"{vv:.1f}%", ha="center", fontsize=9.6, fontweight="bold")
    for xx, vv in zip(x + w/2, mins): ax.text(xx, vv + 3, f"{vv}%", ha="center", fontsize=9.4)
    ax.set_xticks(x); ax.set_xticklabels(metrics, fontsize=9.4)
    ax.set_ylabel("%"); ax.set_ylim(0, 185); ax.legend(frameon=False, fontsize=9)
    finish(fig, "c09_liquidity.png",
           "Liquidity buffers are comfortable — no forced-seller pressure",
           "MARC Ratings (Aug 2026), citing 1Q2026 BMMB disclosures",
           "This matters: a bank in distress sells. A bank with 160% LCR and 108% NSFR waits. Nothing in BMMB's numbers forces a transaction.")

# 10 — peers
def c10():
    p = D["peers"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 3.7), gridspec_kw={"width_ratios": [1, 1]})
    # quarterly net profit
    labels = ["2Q2025", "2Q2026"]
    mbsb = [p["mbsb"]["net_profit_2Q25_rm_m"], p["mbsb"]["net_profit_2Q26_rm_m"]]
    bim = [126.69, p["bank_islam"]["net_profit_2Q26_rm_m"]]
    x = np.arange(2); w = 0.35
    ax1.bar(x - w/2, bim, w, color=TEAL, label="Bank Islam")
    ax1.bar(x + w/2, mbsb, w, color=RED, label="MBSB")
    for xx, vv in zip(x - w/2, bim): ax1.text(xx, vv + 3, f"{vv:.0f}", ha="center", fontsize=9)
    for xx, vv in zip(x + w/2, mbsb): ax1.text(xx, vv + 3, f"{vv:.0f}", ha="center", fontsize=9, fontweight="bold")
    ax1.set_xticks(x); ax1.set_xticklabels(labels); ax1.set_ylabel("Net profit (RM million)")
    ax1.set_ylim(0, 175); ax1.legend(frameon=False, fontsize=8.6); ax1.set_title("2Q net profit", fontsize=10.5)
    # assets
    names = ["Bank Islam", "MBSB Bank", "Bank Muamalat"]
    vals = [p["bank_islam"]["assets_rm_bn"], 64.4, 45.7]
    ax2.barh(np.arange(3)[::-1], vals, color=[TEAL, AMBER, RED], height=0.55)
    for yy, vv in zip(np.arange(3)[::-1], vals):
        ax2.text(vv + 2, yy, f"{vv:.1f}", va="center", fontsize=9.4, fontweight="bold")
    ax2.set_yticks(np.arange(3)[::-1]); ax2.set_yticklabels(names, fontsize=9)
    ax2.set_xlabel("Total assets (RM billion)"); ax2.set_xlim(0, 130); ax2.set_title("Asset base", fontsize=10.5)
    finish(fig, "c10_peer_contrast.png",
           "The two merger partners are both under pressure — which cuts both ways",
           "The Star / The Edge (Aug 2026); MBSB Bank and Bank Islam disclosures",
           "MBSB's 2Q26 profit halved and it cut FY26 ROE guidance to 2-3%. A weakened acquirer is a weaker negotiating position — but also a stronger appetite for scale.")

# 11 — DRB-HICOM dependency
def c11():
    d = D["drb_hicom"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 3.7), gridspec_kw={"width_ratios": [1.1, 1]})
    segs = ["Bank Muamalat\nPBT (1H26)", "Rest of DRB-HICOM\nPBT (1H26)"]
    vals = [d["bank_muamalat_pbt_share_of_group_1H26_pct"], 100 - d["bank_muamalat_pbt_share_of_group_1H26_pct"]]
    ax1.bar(segs, vals, color=[AMBER, NAVY], width=0.5)
    for i, vv in enumerate(vals):
        ax1.text(i, vv + 1.2, f"{vv:.1f}%", ha="center", fontsize=10, fontweight="bold")
    ax1.set_ylabel("% of group pre-tax profit"); ax1.set_ylim(0, 100)
    ax1.set_title("Where DRB-HICOM's profit comes from", fontsize=10.5)
    # market cap vs stake value band
    lo, hi = 3.23 * 0.85 * 0.7, 3.23 * 1.20 * 0.7
    ax2.bar(["DRB-HICOM\nmarket cap"], [d["market_cap_rm_bn"]], color=GREY, width=0.42)
    ax2.bar(["Value of its 70%\nBank Muamalat stake"], [hi], color=AMBER, width=0.42)
    ax2.bar(["Value of its 70%\nBank Muamalat stake"], [hi - lo], bottom=[lo], color=RED, width=0.42)
    ax2.text(1, hi + 0.08, f"RM{lo:.2f}–{hi:.2f}bn", ha="center", fontsize=9.4, fontweight="bold")
    ax2.text(0, d["market_cap_rm_bn"] + 0.08, f"RM{d['market_cap_rm_bn']:.2f}bn", ha="center", fontsize=9.4, fontweight="bold")
    ax2.set_ylabel("RM billion"); ax2.set_ylim(0, 3.2)
    ax2.set_title("One asset outweighs the whole group", fontsize=10.5)
    finish(fig, "c11_drb_dependency.png",
           "Why the pare-down never happens: Bank Muamalat is a third of the profit and more than the market cap",
           "DER: DRB-HICOM 2Q26 filing; BMMB Pillar 3 (Jun 2026); MARC; band = 0.85x-1.20x book on RM3.23bn equity, 70% share",
           "DRB-HICOM traded at RM1.87bn (97 sen) in Aug 2026 while its Bank Muamalat stake alone is worth an estimated RM1.9-2.7bn. Any sale unlocks value; any sale also removes roughly a third of group profit.")

# 12 — valuation triangulation
def c12():
    v = D["valuation_triangulation"]
    eq = v["equity_rm_bn"]
    labels = list(v["bands"].keys()); mult = list(v["bands"].values())
    total = [eq * m for m in mult]
    drb = [t * 0.7 for t in total]; khaz = [t * 0.3 for t in total]
    x = np.arange(len(mult)); w = 0.36
    fig, ax = plt.subplots(figsize=(9.6, 3.7))
    ax.bar(x - w/2, drb, w, color=NAVY, label="DRB-HICOM 70%")
    ax.bar(x + w/2, khaz, w, color=TEAL, label="Khazanah 30%")
    for xx, vv in zip(x - w/2, drb): ax.text(xx, vv + 0.05, f"{vv:.2f}", ha="center", fontsize=9.2)
    for xx, vv in zip(x + w/2, khaz): ax.text(xx, vv + 0.05, f"{vv:.2f}", ha="center", fontsize=9.2)
    ax.set_xticks(x); ax.set_xticklabels([f"{m:.2f}x\nP/B" for m in mult], fontsize=9)
    ax.set_ylabel("Implied stake value (RM billion)"); ax.set_ylim(0, 4.6)
    ax.legend(frameon=False, fontsize=9)
    finish(fig, "c12_valuation.png",
           "Price is the recurring deadlock — a RM1.2-4.1bn band for the seller's stake",
           "DER: BMMB shareholders' equity circa RM3.23bn (Pillar 3, Jun 2026) x precedent P/B multiples",
           "0.85x is the MBSB-MIDF 2023 clearing price; 1.20x is the 2008 price DRB-HICOM itself paid; 1.80x is the 2013 BIMB-Bank Islam price. History says DRB-HICOM anchors near the top of the band; buyers anchor at the bottom.")

# 13 — timeline
def c13():
    t = D["timeline"]
    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    n = len(t)
    ys = np.arange(n)[::-1]
    cols = {"COMPLETED": GREEN}.get
    for y, item in zip(ys, t):
        out = item["outcome"]
        c = GREEN if out == "COMPLETED" else (AMBER if "UNMET" in out or "STATUS QUO" in out or "NO DEFINITE" in out else RED)
        ax.scatter(0, y, s=95, color=c, zorder=3)
        ax.text(0.035, y + 0.16, f"{item['year']} — {item['event']}", fontsize=9.1, va="bottom")
        ax.text(0.035, y - 0.30, f"Outcome: {out}", fontsize=8.4, va="top", color=c, fontweight="bold")
        if y > 0:
            ax.plot([0, 0], [y, ys[n - 1 - (n - 1 - list(ys).index(y)) - 1] if False else y - 1], color=LGREY, lw=1.4, zorder=1)
    ax.set_xlim(-0.02, 1.35); ax.set_ylim(-0.9, n - 0.3)
    ax.set_yticks([]); ax.set_xticks([]); ax.grid(False)
    for s in ax.spines.values(): s.set_visible(False)
    finish(fig, "c13_timeline.png",
           "Eighteen years, eleven attempts, one completed deal — and it wasn't Bank Muamalat's",
           "The Edge Malaysia (2010, 2016, 2019, 2024, 2025); Asian Banking & Finance; Reuters; Bursa announcements; MARC (Aug 2026)",
           "The only transaction that closed in this lineage is the 2023 MBSB-MIDF purchase. Bank Muamalat has been the constant asset and never the completed transaction.")

# 14 — scenarios
def c14():
    s = D["scenarios"]
    labels = [x["label"] for x in s]; probs = [x["prob"] for x in s]
    fig, ax = plt.subplots(figsize=(9.8, 3.8))
    y = np.arange(len(s))[::-1]
    cols = [GREY, TEAL, AMBER, NAVY, RED, LGREY]
    ax.barh(y, probs, color=cols, height=0.6)
    for yy, p in zip(y, probs):
        ax.text(p + 0.008, yy, f"{p*100:.0f}%", va="center", fontsize=9.6, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Probability over the next 12 months"); ax.set_xlim(0, 0.62)
    ax.xaxis.set_major_formatter(lambda v, pos: f"{v*100:.0f}%")
    finish(fig, "c14_scenarios.png",
           "Scenario map — status quo is the base case, not the absence of a case",
           "INT — probabilities are the analyst's judgement, anchored on an 0-for-10 completion record and the RM6bn+ two-sided funding requirement",
           "A transaction that creates a RM110bn Islamic bank requires the seller, the buyer, Khazanah, EPF and BNM to agree on price, control and capital simultaneously. Every leg has failed separately at least once.")

# 15 — void analysis
def c15():
    v = D["void_vocabulary"]
    cats = list(v.keys()); counts = [len(v[c]) for c in cats]
    fig, ax = plt.subplots(figsize=(9.8, 3.8))
    x = np.arange(len(cats))
    ax.bar(x, counts, color=RED, width=0.55)
    for xx, c in zip(x, counts):
        ax.text(xx, c + 0.1, str(c), ha="center", fontsize=9.6, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels([c.replace(" & ", " &\n") for c in cats], fontsize=8.2)
    ax.set_ylabel("Absent terms observed in the record")
    ax.set_ylim(0, max(counts) + 1.6)
    finish(fig, "c15_void.png",
           "The void layer — what the 18-year record never says out loud",
           "VOID analysis: keyword sweep against the published record (2024-2026 coverage, BMMB disclosures, DRB-HICOM filings)",
           "Not one of these categories appears in any current disclosure. The silence is uniform, which usually means the constraint is upstream of the transaction — i.e. shareholder control and price, not execution.")

# 16 — system share
def c16():
    m = D["market_structure"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 3.6), gridspec_kw={"width_ratios": [1.15, 1]})
    yrs = ["2007", "Jan 2026", "2026 actual", "Government target"]
    vals = [m["share_2007_pct"], m["islamic_share_of_banking_assets_pct_jan2026"], m["islamic_financing_share_of_system_loans_pct"], m["government_target_pct"]]
    ax1.bar(yrs, vals, color=[GREY, NAVY, TEAL, AMBER], width=0.5)
    for i, vv in enumerate(vals):
        ax1.text(i, vv + 0.8, f"{vv:.1f}%", ha="center", fontsize=9.6, fontweight="bold")
    ax1.set_ylabel("Islamic share of banking (%)"); ax1.set_ylim(0, 58)
    ax1.set_title("Islamic finance share of the system", fontsize=10.5)
    ax1.tick_params(axis="x", labelsize=8.4)
    rest = 100 - m["top7_islamic_share_of_islamic_system_pct"]
    ax2.pie([m["top7_islamic_share_of_islamic_system_pct"], rest],
            labels=["Top 7 Islamic banks", "Long tail (11+ institutions)"],
            colors=[NAVY, LGREY], autopct="%1.1f%%", startangle=100,
            textprops={"fontsize": 9})
    ax2.set_title("Concentration inside Islamic banking", fontsize=10.5)
    finish(fig, "c16_system_share.png",
           "A consolidating sector with a very long tail: 76-77% of assets in seven institutions",
           "Fitch Ratings (Feb 2026); Bernama (Jan 2026); S&P Global; BNM",
           "Islamic banking is still compounding at roughly twice conventional growth. Scale is the industry's stated answer to thin margins — which is the structural argument every merger rumour leans on.")

order = [c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c12, c13, c14, c15, c16]
for fn in order:
    try:
        fn()
    except Exception as e:
        print("FAIL", fn.__name__, type(e).__name__, e)
print("charts written to", CH)
