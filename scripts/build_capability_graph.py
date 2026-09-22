#!/usr/bin/env python3
"""build_capability_graph.py — Capability-first view WITH LIVENESS (F13 verdict 2026-09-22).
v2: answers "what capabilities are ALIVE?" — each live entry carries last proof,
proof quality, freshness, confidence. Confidence = LIVE x proof_quality x freshness_w.
Capability survives; providers mutate. Proof expires; liveness decays."""
import json, sqlite3, sys
from datetime import datetime, timezone
SOT="/root/.config/federation-models.json"
DB="/root/.local/share/arifos/token_bank.db"
OUT="/root/.config/federation-capability-graph.json"
CAP_MAP={"vision":"Vision","multimodal_omni":"Vision","image_ocr":"Vision",
 "reasoning":"Reasoning","code":"Coding","agentic":"Coding","plan":"Reasoning",
 "tool_call":"Chat","analyze":"Reasoning","search":"Reasoning",
 "realtime":"Chat","audio":"Audio","video":"Video"}
QUALITY={"chat_completion":1.0,"direct_canary":0.95,"models_get":0.7,"agent_report":0.5,"UNATTESTED_LEGACY":0.1}
FRESH_W={"FRESH":1.0,"STALE":0.7,"AGING":0.35,"EXPIRED":0.0}
def freshness(ts):
    if not ts: return "EXPIRED"
    try: t=datetime.fromisoformat(str(ts).replace("Z","+00:00"))
    except ValueError: return "EXPIRED"
    if t.tzinfo is None: t=t.replace(tzinfo=timezone.utc)
    m=(datetime.now(timezone.utc)-t).total_seconds()/60
    return "FRESH" if m<=15 else "STALE" if m<=60 else "AGING" if m<=1440 else "EXPIRED"
VENDOR_RULES=[("mimo","xiaomi"),("xiaomi","xiaomi"),("qwen","alibaba"),("dashscope","alibaba"),
 ("bailian","alibaba"),("deepseek","deepseek"),("minimax","minimax"),("gemini","google"),
 ("antigravity","google"),("zhipu","zhipu"),("glm","zhipu"),("kimi","moonshot"),("moonshot","moonshot"),
 ("anthropic","anthropic"),("claude","anthropic"),("groq","groq"),("mistral","mistral"),
 ("k3","moonshot"),("mulerouter","AGGREGATE"),("opencode","AGGREGATE"),("tokenrouter","AGGREGATE")]
def vendor_of(model_key):
    mk=model_key.lower()
    for frag,v in VENDOR_RULES:
        if frag in mk: return v
    return mk.split("/")[0] if "/" in mk else mk
def survivability(vendors):
    n=len(vendors)
    return "STRONG" if n>=3 else "OK" if n==2 else "SINGLE_VENDOR" if n==1 else "DEAD"

DOMAIN_FOR={"Vision":"vision","Coding":"code","Reasoning":"code","JudgeSeat":"judge","Chat":"tool"}
_DQ={}
def domain_score(prov, model, cap):
    dom=DOMAIN_FOR.get(cap)
    if not dom: return None
    best=None
    for (p,m,d),sc in _DQ.items():
        if d!=dom: continue
        prov_ok = (prov and (p==prov or prov in p or p in prov))
        model_ok = (model and (m==model or model in m or m in model))
        if prov_ok and model_ok:
            best=sc; break
    return best
def load_domain_quality():
    import sqlite3 as _s
    try:
        with _s.connect("/root/.local/share/arifos/token_bank.db") as _c:
            for p,m,d,sc in _c.execute("SELECT provider_name,model_id,domain,score FROM route_quality"):
                _DQ[(p,m,d)]=sc
    except Exception: pass

def main():
    load_domain_quality()
    sot=json.load(open(SOT))
    health={}
    try:
        with sqlite3.connect(DB) as c:
            for row in c.execute("SELECT provider_name,model_id,status,witness_type,witness_time,witness_class,witness_score FROM route_health"):
                    health.setdefault(row[0], []).append(row)
    except Exception: pass
    
    def live_entry(mk):
        prov=mk.split("/")[0] if "/" in mk else ""
        cands=[]
        for p,rows in health.items():
            if not (p==prov or (prov and prov in p) or (p and p in mk)): continue
            for row in rows:
                if row[1]=="probe" or row[1] in mk: cands.append(row)
        if not cands: return None
        def _score(row):
            if row[2] not in ("LIVE", "RATE_LIMITED"):
                return -1.0
            fr = freshness(row[4]); q = QUALITY.get(row[3] or "UNATTESTED_LEGACY", 0.3)
            cls = (row[5] if len(row) > 5 else None) or "liveness"
            cap = 1.0 if cls in ("capability", "quality") else 0.7
            return (1.0 if row[2] == "LIVE" else 0.4) * q * FRESH_W[fr] * cap
        best = max(cands, key=_score)
        if _score(best) < 0:
            return None
        wtype=best[3] or "UNATTESTED_LEGACY"; wt=best[4]
        fr=freshness(wt); q=QUALITY.get(wtype,0.3)
        conf=round((1.0 if best[2]=="LIVE" else 0.4)*q*FRESH_W[fr],3)
        wclass=(best[5] if len(best)>5 else None) or "liveness"
        if conf>0 and wclass not in ("capability","quality"): conf=round(conf*0.7,3)
        wscore = best[6] if len(best)>6 else None
        if conf>0 and wscore is not None: conf=round(conf*(0.6+0.4*float(wscore)),3)
        return {"model_key":mk,"status":best[2],"witness":wtype,"last_proof":wt,
                "freshness":fr,"proof_quality":q,"witness_score":(best[6] if len(best)>6 else None),"confidence":conf}
    caps={}
    judge=[]
    for m in sot.get("models",[]):
        mk=m.get("model_key","")
        if any(r in (m.get("constitutional_roles") or []) for r in ("666_JUDGE","999_SEAL")):
            judge.append(mk); caps.setdefault("JudgeSeat",set()).add(mk)
        for c in (m.get("capabilities") or []):
            n=CAP_MAP.get(c) or ("LongContext" if c.startswith("long_") else None)
            if n: caps[n].add(mk) if n in caps else caps.setdefault(n,{mk})
            if n: caps[n].add(mk)
        mods=m.get("modalities") or []
        if "image" in mods: caps.setdefault("Vision",set()).add(mk)
        if (m.get("context_window") or 0)>=500000: caps.setdefault("LongContext",set()).add(mk)
        cin=m.get("cost_per_1m_input")
        if cin is not None and cin<=0.2: caps.setdefault("CheapInference",set()).add(mk)
    out={}
    for name,models in sorted(caps.items()):
        models=sorted(x for x in models if x)
        entries=[e for e in (live_entry(mk) for mk in models) if e]
        entries.sort(key=lambda e:-e["confidence"])
        for e in entries:
            if e["confidence"]<=0: continue
            _dq=domain_score((e["model_key"].split("/")[0] if "/" in e["model_key"] else ""), e["model_key"].split("/")[-1], name)
            if _dq is None:
                e["competence"]="unproven"; e["confidence"]=round(e["confidence"]*0.9,3)
            else:
                e["competence"]=f"scored:{_dq}"
                e["confidence"]=round(e["confidence"]*(0.5+0.5*float(_dq)),3)
        alive=[e for e in entries if e["confidence"]>0]
        proofs=[e["last_proof"] for e in entries if e["last_proof"]]
        alive_vendors=sorted({vendor_of(e["model_key"]) for e in alive}-{"AGGREGATE"})
        all_vendors=sorted({vendor_of(mk) for mk in models}-{"AGGREGATE"})
        out[name]={"capability":name,"catalog_models":len(models),
            "alive_witnessed":len(alive),
            "alive_vendors":alive_vendors,
            "survivability":survivability(alive_vendors),
            "vendor_pool":all_vendors,
            "vendor_floor":len(all_vendors),
            "top_alive":entries[:5],
            "oldest_proof":min(proofs) if proofs else None,
            "expired_witnessed":sum(1 for e in entries if e["freshness"]=="EXPIRED"),
            "mean_confidence":round(sum(e["confidence"] for e in entries)/len(entries),3) if entries else 0.0}
    doc={"schema":"fed-capability-liveness-graph/v3",
         "generated":datetime.now(timezone.utc).isoformat(),
         "doctrine":"Capability survives; providers mutate. Proof expires; liveness decays.",
         "confidence":"LIVE x proof_quality x freshness x class_cap x quality_score_gate x DOMAIN_COMPETENCE (scored:0.5+0.5*domain or unproven x0.9) — Alive!=Capable!=Competent; survivability=alive independent vendors (aggregates excluded)",
         "source":SOT,"capabilities":out,
         "judge_seats":sorted(judge),
         "judge_seat_liveness":[e for e in (live_entry(m) for m in judge) if e]}
    json.dump(doc, open(OUT,"w"), indent=1, ensure_ascii=False)
    print(f"OK liveness graph v3: {len(out)} capabilities")
    for k,v in out.items(): print(f"  {k}: alive={v['alive_witnessed']}/{v['catalog_models']} conf={v['mean_confidence']} oldest={v['oldest_proof']}")
    print("JudgeSeat liveness:", [(e['model_key'],e['confidence'],e['freshness']) for e in doc['judge_seat_liveness']])
if __name__=="__main__": sys.exit(main())
