#!/usr/bin/env python3
"""Charts for the Bank Muamalat Shariah-authenticity report."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = "/root/AAA/forge_work/2026-09-15-bank-muamalat-authenticity"
CH = os.path.join(BASE, "charts")
os.makedirs(CH, exist_ok=True)
D = json.load(open(os.path.join(BASE, "data/dataset.json")))

NAVY="#0d2b45"; TEAL="#1b7f79"; AMBER="#d98324"; RED="#b3402f"
GREY="#6b7280"; LGREY="#d9dee3"; GREEN="#2f7d4f"; PURPLE="#5d4a7a"

plt.rcParams.update({
    "figure.dpi":140,"savefig.dpi":140,"font.size":10.5,
    "axes.edgecolor":LGREY,"axes.labelcolor":NAVY,"text.color":NAVY,
    "xtick.color":GREY,"ytick.color":GREY,"axes.titlecolor":NAVY,
    "axes.grid":True,"grid.color":LGREY,"grid.linewidth":0.6,
    "axes.axisbelow":True,"font.family":"DejaVu Sans",
})

def finish(fig,name,title,source,sub=None):
    fig.suptitle(title,fontsize=13.2,fontweight="bold",x=0.012,ha="left",y=0.985)
    if sub: fig.text(0.012,0.938,sub,fontsize=9.4,color=GREY,ha="left")
    fig.text(0.012,0.012,"Source: "+source,fontsize=7.7,color=GREY,ha="left")
    fig.savefig(os.path.join(CH,name),bbox_inches="tight",facecolor="white")
    plt.close(fig); print("ok",name)

# C1 — the authenticity gap
def c01():
    a=D["authenticity_gap"]
    fig, ax = plt.subplots(figsize=(9.8,3.9))
    items=[
        ("Debt-based (tawarruq /\ncommodity murabahah)", a["debt_based_share_pct"], NAVY),
        ("Risk-sharing — broad\ndefinition (upper estimate)", a["pls_share_broad_estimate_pct"][1], TEAL),
        ("Risk-sharing — broad\ndefinition (lower estimate)", a["pls_share_broad_estimate_pct"][0], AMBER),
        ("Risk-sharing — narrow\n(musharakah + mudharabah, high)", a["pls_share_narrow_estimate_pct"][1], RED),
        ("Risk-sharing — narrow\n(musharakah + mudharabah, low)", a["pls_share_narrow_estimate_pct"][0], PURPLE),
    ]
    y=np.arange(len(items))[::-1]
    for yy,(lab,v,c) in zip(y,items):
        ax.barh(yy,v,color=c,height=0.6)
        ax.text(v+1.4,yy,f"{v:.2f}%" if v<5 else f"{v:.0f}%",va="center",fontsize=9.6,fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels([i[0] for i in items],fontsize=8.8)
    ax.set_xlabel("Share of Islamic banking financing / assets (%)"); ax.set_xlim(0,105)
    finish(fig,"c01_authenticity_gap.png",
      "The authenticity gap — an industry built almost entirely on debt-based structures",
      "Semantic Scholar (commodity murabahah ~90%+); UKM working paper series (Malaysia PLS); Chong & Liu 2009 / Nor & Ismail 2020; PMC comparative study",
      "Estimates differ by definition — narrow measures count only pure mushārakah/muḍārabah; broad measures include all profit-and-loss-sharing forms. Both ends of the range leave risk-sharing as a minority practice.")

# C2 — BMMB book composition
def c02():
    b=D["bmmb"]["book_composition_pct"]
    labels=["Home financing\n(tawarruq today)","Personal financing\n(tawarruq / inah)","Other\n(auto, Ar Rahnu, revolving\ncredit, acceptance credits)"]
    vals=[b["home_financing"],b["personal_financing"],b["other"]]
    cols=[RED,AMBER,GREY]
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10.4,3.8),gridspec_kw={"width_ratios":[1,1.05]})
    ax1.bar(labels,vals,color=cols,width=0.55)
    for i,v in enumerate(vals): ax1.text(i,v+0.9,f"{v:.1f}%",ha="center",fontsize=9.8,fontweight="bold")
    ax1.set_ylabel("% of gross financing"); ax1.set_ylim(0,46); ax1.tick_params(axis="x",labelsize=7.6)
    ax1.set_title("Where the book sits today",fontsize=10.4)
    # target
    t=D["targets"]
    tl=["Mushārakah mutanāqisah\nhome financing","Risk-sharing\n(halal, waqf, climate)","Residual debt-based"]
    tv=[25.0,30.0,45.0]
    ax2.bar(tl,tv,color=[TEAL,TEAL,NAVY],width=0.55)
    for i,v in enumerate(tv): ax2.text(i,v+0.9,f"{v:.0f}%",ha="center",fontsize=9.8,fontweight="bold")
    ax2.set_ylabel("% of gross financing"); ax2.set_ylim(0,58); ax2.tick_params(axis="x",labelsize=7.6)
    ax2.set_title("A plausible 7-year destination",fontsize=10.4)
    finish(fig,"c02_book_target.png",
      "The asset glide — the founding book is debt-based by construction",
      "Bank Muamalat Annual Report FY2024 (home financing 33.51%); The Edge (Mar 2024 personal financing 28.6%); target is analytic (INT)",
      "Home financing and Ar Rahnu are both structured on tawarruq; the Gold-i account is real-asset but the wrapper is an investment account, not risk-sharing. Nothing in the current book is a genuine profit-and-loss-sharing exposure of scale.")

# C3 — funding side
def c03():
    f=D["bmmb"]["funding"]; t=D["targets"]
    fig,ax=plt.subplots(figsize=(9.8,3.7))
    cats=["Customer deposits\n(% of total funding)","Deposit + investment\naccount funding","Retail share of\nfunding base","Top-20 depositor\nconcentration","Investment accounts\n(muḍārabah / mushārakah)\nas share of funding"]
    cur=[f["deposits_pct_of_funding"],None,f["retail_pct"],f["top20_depositor_pct"],None]
    tgt=[None,60.0,None,25.0,t["ia_share_of_funding_pct"]]
    x=np.arange(len(cats)); w=0.36
    cv=[0 if v is None else v for v in cur]
    tv=[0 if v is None else v for v in tgt]
    ax.bar(x-w/2,cv,w,color=NAVY,label="Today (observed)")
    ax.bar(x+w/2,tv,w,color=TEAL,label="7-year destination (analytic)")
    for xx,v in zip(x-w/2,cv):
        if v: ax.text(xx,v+1.2,f"{v:.1f}%",ha="center",fontsize=8.8)
    for xx,v in zip(x+w/2,tv):
        if v: ax.text(xx,v+1.2,f"{v:.0f}%",ha="center",fontsize=8.8,fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(cats,fontsize=7.7)
    ax.set_ylabel("%"); ax.set_ylim(0,110); ax.legend(frameon=False,fontsize=8.8)
    finish(fig,"c03_funding_side.png",
      "Why the funding side comes first — deposits are a debt contract, investment accounts are not",
      "Bank Muamalat Pillar 3 / MARC Ratings (1Q2026 data, Aug 2026); targets are analytic (INT)",
      "90.2% deposit funding means the bank carries the loss, not the funder. Investment accounts place the loss where Islamic contract law puts it. This is also the commercially rational fix: it replaces concentrated wholesale money with a stable, granular, lower-cost base.")

# C4 — capital sensitivity
def c04():
    cs=D["capital_sensitivity"]; b=D["bmmb"]
    shifts=[0,2,5,8,10,15]
    baseline=cs["rwa_today_rm_bn"]
    rwa=[baseline + s*cs["per_rm1bn_pls_shift_rwa_rm_bn"] for s in shifts]
    cap15 = [(r * 0.15 - b["shareholders_equity_rm_bn_jun2026"]) for r in rwa]
    fig,ax=plt.subplots(figsize=(9.8,3.8))
    ax.bar([str(s) for s in shifts], rwa, color=[GREY,AMBER,AMBER,AMBER,RED,RED], width=0.55)
    for i,(s,r) in enumerate(zip(shifts,rwa)):
        ax.text(i,r+0.7,f"{r:.1f}",ha="center",fontsize=9.4,fontweight="bold")
        if s>0:
            need=(r*0.15-b["shareholders_equity_rm_bn_jun2026"])
            ax.text(i,r*0.5,f"+RM{need:.1f}bn\nCET1",ha="center",fontsize=7.8,color="white",fontweight="bold")
    ax.set_xlabel("Risk-sharing assets added to the book (RM billion)")
    ax.set_ylabel("Implied risk-weighted assets (RM billion)")
    ax.set_ylim(0,max(rwa)*1.22)
    finish(fig,"c04_capital_sensitivity.png",
      "The capital penalty — risk-sharing assets consume far more regulatory capital than debt",
      "DER: BMMB CET1 12.02% and equity RM3.23bn (Pillar 3, Jun 2026); literature reports mushārakah/muḍārabah exposures risk-weighted up to 400% vs debt-based financing",
      "This is the single largest structural reason Islamic banks avoid risk-sharing. Each RM1bn shifted toward mushārakah/muḍārabah adds roughly RM3bn of RWA and, at a 15% CET1 target, about RM450m of new equity. Converting the model therefore requires either a capital raise or a regulatory calibration of risk weights — it is a policy ask, not only a bank-side choice.")

# C5 — glide path
def c05():
    px=D["phases"]
    fig,ax=plt.subplots(figsize=(10.0,4.4))
    spans={"P0":(0,1),"P1":(1,3),"P2":(2,5),"P3":(3,7),"P4":(2,6),"P5":(5,7.6)}
    cols={"P0":NAVY,"P1":TEAL,"P2":AMBER,"P3":GREEN,"P4":PURPLE,"P5":RED}
    y=np.arange(len(px))[::-1]
    for yy,p in zip(y,px):
        s,e=spans[p["id"]]
        ax.barh(yy,e-s,left=s,color=cols[p["id"]],height=0.52)
        ax.text(s+0.08,yy,p["id"]+" · "+p["name"],va="center",fontsize=8.6,color="white",fontweight="bold")
        ax.text(e+0.12,yy,p["deliverable"][:60],va="center",fontsize=7.6,color=GREY)
    ax.set_yticks([]); ax.set_xlabel("Years from decision"); ax.set_xlim(0,13)
    ax.set_xticks(range(0,9))
    finish(fig,"c05_glidepath.png",
      "The glide path — and the one instruction that matters most: scale comes last",
      "Analytic sequence (INT), anchored on BNM's i-CITA programme (Sep 2025) and the Investment Account framework",
      "Phases overlap by design. P5 is deliberately placed after P1 and P2, not before: consolidating a debt-based balance sheet first makes conversion harder, not easier — a larger legacy book, more people whose incentives are volume, and greater political sensitivity to any doctrinal tightening.")

# C6 — sector selection
def c06():
    secs=[
        ("Halal industry &\nfood security",9.0,8.5,"Long horizon, unpredictable cashflows, national priority"),
        ("Waqf property\ndevelopment",8.5,9.2,"Asset-backed by construction, permanent capital, social mandate"),
        ("Climate transition\nexposure",8.0,7.0,"Long-dated, cashflow-uncertain — BNM names it explicitly"),
        ("Home financing\n(mushārakah mutanāqisah)",9.5,6.0,"Largest single book, clearest symbolic shift, hardest to migrate"),
        ("SME working capital\n(murābahah)",4.0,4.5,"Short cycle, predictable cashflow — debt is defensible here"),
        ("Unsecured personal\nfinancing",2.0,3.0,"Where tawarruq adds least and attracts most criticism"),
    ]
    fig,ax=plt.subplots(figsize=(9.8,4.6))
    for lab,x,y,note in secs:
        c = GREEN if (x>=8 and y>=7) else (AMBER if x>=7 else RED)
        ax.scatter(x,y,s=340,color=c,alpha=0.85,zorder=3,edgecolor="white",linewidth=1.5)
        ax.annotate(lab,(x,y),textcoords="offset points",xytext=(0,-26),ha="center",fontsize=7.4)
    ax.axvspan(7.5,10,color=GREEN,alpha=0.05)
    ax.axhspan(7,10,color=GREEN,alpha=0.05)
    ax.set_xlabel("Economic case for risk-sharing  →")
    ax.set_ylabel("Social / maqasid impact  →")
    ax.set_xlim(0,10.6); ax.set_ylim(1,10.4)
    ax.text(9.9,10.1,"START HERE",fontsize=8.4,color=GREEN,ha="right",fontweight="bold")
    ax.text(1.0,2.0,"DEFEND AS DEBT",fontsize=8.4,color=RED,fontweight="bold")
    finish(fig,"c06_sector_map.png",
      "Convert where risk-sharing wins on economics, not only on doctrine",
      "Analytic scoring (INT) anchored on BNM AR2025 rationale for i-CITA and BMMB book composition (FY2024)",
      "The strategic discipline is to convert where the Islamic contract is also the better commercial contract. Fighting for risk-sharing in short-cycle, predictable-cashflow lending is where credibility is lost — and where the industry's tawarruq dependence is actually defensible.")

# C7 — juristic divergence
def c07():
    rows=[
        ("Organised tawarruq\n(al-tawarruq al-munaẓẓam)","Accepted, with parameters\n(SAC; policy document 2018)","Impermissible\n(OIC Fiqh Academy, 2003)", True),
        ("Bay' al-'inah\n(sale-and-buyback)","Accepted by Malaysian SAC","Rejected by AAOIFI\nand Gulf bodies", True),
        ("AAOIFI Shariah\nstandards","Not the primary reference\n(SAC rulings prevail)","Primary reference\nfor Gulf institutions", False),
        ("Risk-sharing emphasis","Declared (Kuala Lumpur Declaration)","Declared", False),
    ]
    fig,ax=plt.subplots(figsize=(10.2,3.1)); ax.axis("off")
    ax.text(0.02,0.93,"Position",fontsize=9.2,fontweight="bold",color=NAVY,transform=ax.transAxes)
    ax.text(0.42,0.93,"Malaysian SAC framework",fontsize=9.2,fontweight="bold",color=TEAL,transform=ax.transAxes)
    ax.text(0.73,0.93,"AAOIFI / Gulf scholarly position",fontsize=9.2,fontweight="bold",color=RED,transform=ax.transAxes)
    y=0.78
    for pos,my,gulf,flag in rows:
        col = "#fdf1ee" if flag else "#f4f7f9"
        ax.add_patch(plt.Rectangle((0.01,y-0.11),0.98,0.20,facecolor=col,edgecolor=LGREY,transform=ax.transAxes))
        ax.text(0.02,y-0.015,pos,fontsize=7.8,transform=ax.transAxes,va="center")
        ax.text(0.42,y-0.015,my,fontsize=7.8,transform=ax.transAxes,va="center",color=TEAL)
        ax.text(0.73,y-0.015,gulf,fontsize=7.8,transform=ax.transAxes,va="center",color=RED)
        y-=0.22
    finish(fig,"c07_divergence.png",
      "Where the Malaysian framework and the Gulf scholarly position actually differ",
      "BNM Shariah Resolutions; BNM Tawarruq policy document (reissued Dec 2018); OIC Fiqh Academy 17th session (2003); AAOIFI standards; academic literature on divergence",
      "This is a genuine juristic divergence, not a compliance failure in either direction. But it defines the choice: a bank claiming authenticity under 'real Islamic teaching' must state which standard it holds itself to — and if the stricter one, must accept the commercial cost of that choice.")

# C8 — talent
def c08():
    t=D["talent"]
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10.2,3.3),gridspec_kw={"width_ratios":[1,1.1]})
    ax1.bar(["Active Shariah\nCommittee members","Required\n(imminent)"],[t["active_shariah_committee_members_my"],t["required_soon"]],color=[AMBER,RED],width=0.5)
    for i,v in enumerate([t["active_shariah_committee_members_my"],t["required_soon"]]):
        ax1.text(i,v+3,str(v),ha="center",fontsize=10,fontweight="bold")
    ax1.set_ylabel("Personnel"); ax1.set_ylim(0,235)
    ax1.annotate("",xy=(1,t["required_soon"]),xytext=(0,0),arrowprops=dict(arrowstyle="<->",color=GREY))
    ax1.set_title(f"Committee gap: {t['gap']}",fontsize=10.2)
    ax2.bar(["Current\ncommittee pool","Projected shortfall\nof qualified practitioners"],[t["active_shariah_committee_members_my"],t["projected_practitioner_deficit"]],color=[TEAL,RED],width=0.45)
    for i,v in enumerate([t["active_shariah_committee_members_my"],t["projected_practitioner_deficit"]]):
        ax2.text(i,v+25,f"{v:,}",ha="center",fontsize=10,fontweight="bold")
    ax2.set_ylabel("Personnel"); ax2.set_ylim(0,1700)
    ax2.set_title("Depth problem, not just a committee problem",fontsize=10.2)
    finish(fig,"c08_talent.png",
      "You cannot build an authentic bank without building the people who can judge it",
      "Industry association projections and Malaysian Islamic finance talent reporting (2026)",
      "Malaysia has 136 active Shariah Committee members against an imminent requirement of 196 — a gap of 60 — and a projected deficit running into the thousands for qualified practitioners. An authenticity programme without a talent pipeline is a ten-year promise with no engine.")

# C9 — social finance engine
def c09():
    fig,ax=plt.subplots(figsize=(9.8,4.0)); ax.axis("off")
    boxes=[
        (0.05,0.62,0.26,0.24,"Zakat routing\n\nAutomatic deduction on haul\nand nisab (Gold-i), channelled\nto state Islamic authorities", TEAL),
        (0.37,0.62,0.26,0.24,"Waqf engine\n\nPermanent capital, waqf property\ndevelopment, asset-backed\nby construction", PURPLE),
        (0.69,0.62,0.26,0.24,"Qardhul hasan\n\nBenevolent loans funded from\nShariah non-compliance income\nplus a fixed share of profit", GREEN),
        (0.21,0.16,0.26,0.24,"Microfinance\n(iTEKAD model)\n\nMicro-entrepreneurs, iTEKAD\nProtection takaful", AMBER),
        (0.53,0.16,0.26,0.24,"Maqasid reporting\n\nAnnual, third-party verified:\nwealth distribution, real-asset\nownership, social reach", NAVY),
    ]
    for x,y,w,h,txt,c in boxes:
        ax.add_patch(plt.Rectangle((x,y),w,h,facecolor=c,alpha=0.10,edgecolor=c,linewidth=1.6,transform=ax.transAxes))
        ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=7.6,transform=ax.transAxes,color=NAVY)
    for x0,y0,x1,y1 in [(0.31,0.74,0.37,0.74),(0.63,0.74,0.69,0.74),(0.50,0.62,0.42,0.40),(0.70,0.62,0.66,0.40)]:
        ax.annotate("",xy=(x1,y1),xytext=(x0,y0),arrowprops=dict(arrowstyle="->",color=GREY,lw=1.3),xycoords=ax.transAxes,textcoords=ax.transAxes)
    finish(fig,"c09_social_engine.png",
      "Social finance as the core, not the CSR appendix",
      "Bank Muamalat Gold-i (automatic zakat on haul/nisab); GABV membership; BNM iTEKAD and i-CITA programmes (AR2025)",
      "Bank Muamalat already operates the pieces: automatic zakat deduction, the region's first GABV membership, and Shariah training in waqf, zakat and sadaqah. Scaling these from side programmes into core infrastructure is the cheapest available route to a differentiated institution.")

# C10 — failure modes
def c10():
    f=D["failure_modes"]
    fig,ax=plt.subplots(figsize=(9.8,3.7))
    labs=[x["mode"] for x in f]; vals=[x["prob"] for x in f]
    y=np.arange(len(f))[::-1]
    cols=[RED,RED,AMBER,AMBER,GREEN]
    ax.barh(y,vals,color=cols,height=0.6)
    for yy,v in zip(y,vals): ax.text(v+0.008,yy,f"{v*100:.0f}%",va="center",fontsize=9.6,fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(labs,fontsize=9)
    ax.set_xlabel("Probability over a 10-year authenticity programme (judgement)"); ax.set_xlim(0,0.56)
    ax.xaxis.set_major_formatter(lambda v,pos:f"{v*100:.0f}%")
    finish(fig,"c10_failure_modes.png",
      "The most likely outcome is a bigger replica — and that is what the sequencing is designed to prevent",
      "INT — analyst judgement, anchored on the observed industry ratio (debt-based ~90%+) and the IFSB's own 2026 finding that products 'increasingly mimic conventional banking'",
      "Three of the four most likely failure modes are marketing and capital failures, not doctrinal ones. That is the practical lesson: sincerity is not the scarce input — sequencing and capital are.")

# C11 — metric dashboard
def c11():
    m=D["metrics"]
    keys=list(m.keys())
    fig,ax=plt.subplots(figsize=(10.2,4.6)); ax.axis("off")
    ax.text(0.02,0.95,"Measure",fontsize=9,fontweight="bold",color=NAVY,transform=ax.transAxes)
    ax.text(0.37,0.95,"Today",fontsize=9,fontweight="bold",color=NAVY,transform=ax.transAxes)
    ax.text(0.60,0.95,"Destination",fontsize=9,fontweight="bold",color=TEAL,transform=ax.transAxes)
    ax.text(0.82,0.95,"Verification",fontsize=9,fontweight="bold",color=NAVY,transform=ax.transAxes)
    y=0.855
    for k in keys:
        row=m[k]; fill="#fafcfd" if int(y*10)%2==0 else "#ffffff"
        ax.add_patch(plt.Rectangle((0.01,y-0.095),0.98,0.115,facecolor=fill,edgecolor=LGREY,transform=ax.transAxes))
        ax.text(0.02,y-0.035,k,fontsize=7.6,transform=ax.transAxes,va="center",color=NAVY)
        ax.text(0.37,y-0.035,row["current"],fontsize=7.4,transform=ax.transAxes,va="center",color=GREY)
        ax.text(0.60,y-0.035,row["target"],fontsize=7.4,transform=ax.transAxes,va="center",color=TEAL,fontweight="bold")
        ax.text(0.82,y-0.035,row["audit"],fontsize=7.2,transform=ax.transAxes,va="center",color=GREY)
        y-=0.118
    finish(fig,"c11_dashboard.png",
      "How you would know it is real — the measurability test",
      "Analytic (INT). Every row is chosen because it is externally auditable and would be uncomfortable to publish if the answer were bad.",
      "An authenticity claim that cannot be measured, and is not verified by someone with the standing to say no, is marketing. The second column is the whole point: if the bank will not publish the first column, the rest of the programme is decoration.")

# C12 — sequence contrast
def c12():
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10.4,3.9),gridspec_kw={"width_ratios":[1,1]})
    for ax,title,steps,cols,note in [
        (ax1,"Path A — scale first (the tempting mistake)",
         ["Merger","Bigger book","Same 90% debt-based mix","Conversion now much harder"],
         [RED,RED,RED,RED],"Legacy book larger · volume incentives entrenched ·\ndoctrinal tightening becomes politically expensive"),
        (ax2,"Path B — convert first, then scale",
         ["Fix funding side","Migrate the asset book","Publish maqasid + audit","Then consolidate"],
         [TEAL,TEAL,TEAL,GREEN],"Smaller before larger · ROE dips early ·\nbut the model is proven while the stakes are low")]:
        ax.axis("off")
        ax.text(0.5,0.97,title,fontsize=9.6,fontweight="bold",ha="center",transform=ax.transAxes,color=NAVY)
        y=0.80
        for i,(s,c) in enumerate(zip(steps,cols)):
            ax.add_patch(plt.Rectangle((0.08,y-0.055),0.84,0.11,facecolor=c,alpha=0.13,edgecolor=c,linewidth=1.5,transform=ax.transAxes))
            ax.text(0.5,y,s,fontsize=8.4,ha="center",va="center",transform=ax.transAxes,color=NAVY)
            if i<len(steps)-1:
                ax.annotate("",xy=(0.5,y-0.075),xytext=(0.5,y-0.055),arrowprops=dict(arrowstyle="->",color=GREY),transform=ax.transAxes,xycoords=ax.transAxes,textcoords=ax.transAxes)
            y-=0.185
        ax.text(0.5,0.045,note,fontsize=6.9,ha="center",transform=ax.transAxes,color=GREY)
    finish(fig,"c12_sequence.png",
      "The sequencing decision — the single highest-leverage choice in the whole programme",
      "Analytic (INT)",
      "Both paths are defensible on a spreadsheet. They diverge on one question: whether the conversion is attempted while the institution is still small enough for the experiment to be survivable.")

for fn in [c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12]:
    try: fn()
    except Exception as e: print("FAIL",fn.__name__,type(e).__name__,e)
print("done ->",CH)
