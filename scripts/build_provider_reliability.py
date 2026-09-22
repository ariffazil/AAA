#!/usr/bin/env python3
"""build_provider_reliability.py — Scar Gravity materializer (F13 verdict 2026-09-22).
Providers remember consequences: scar_events (weight x recency) -> reliability 0..1.
Fed_router consumes /root/.config/fed-provider-reliability.json (mtime-cached).
Empty events => all neutral 1.0. Run after any scar event or weight change."""
import json, os, sys
from datetime import datetime, timezone, timedelta
SCARS="/root/AAA/federation/provider-failure-patterns/scars.json"
EVENTS="/root/AAA/federation/provider-failure-patterns/scar_events.jsonl"
OUT="/root/.config/fed-provider-reliability.json"
def main():
    weights={s["id"]: float(s.get("w_scar",0.5)) for s in json.load(open(SCARS))["scars"]}
    now=datetime.now(timezone.utc)
    penalty={}  # provider -> accumulated weighted penalty
    counts={}
    if os.path.exists(EVENTS):
        for line in open(EVENTS, encoding="utf-8"):
            line=line.strip()
            if not line: continue
            try: e=json.loads(line)
            except json.JSONDecodeError: continue
            prov=e.get("provider"); sid=e.get("scar_id","")
            if not prov: continue
            try: t=datetime.fromisoformat(str(e.get("ts","")).replace("Z","+00:00"))
            except ValueError: t=now
            age_days=max(0.0,(now-t).total_seconds()/86400.0)
            recency=1.0 if age_days<=7 else max(0.25, 1.0-(age_days-7)/30.0)
            w=weights.get(sid,0.5)*recency
            penalty[prov]=penalty.get(prov,0.0)+w
            counts[prov]=counts.get(prov,0)+1
    providers={}
    # neutral entries for every provider seen in scars index history? keep event-driven only
    for prov,p in sorted(penalty.items()):
        reliability=round(max(0.0, 1.0-min(1.0,p/2.0)),3)  # p/2 saturates at 2.0 weighted events
        providers[prov]={"reliability":reliability,"weighted_penalty":round(p,3),
                         "scar_events":counts.get(prov,0),
                         "scars":[json.loads(l)["scar_id"] for l in open(EVENTS,encoding="utf-8") if l.strip() and json.loads(l).get("provider")==prov][-5:] if os.path.exists(EVENTS) else []}
    doc={"schema":"fed-provider-reliability/v1","generated":now.isoformat(),
         "doctrine":"Scar Gravity — providers remember consequences, not merely incidents.",
         "w_scar_scale":"0.0-1.0 (scar-weight-registry v1.1.0)","providers":providers}
    json.dump(doc, open(OUT,"w"), indent=1, ensure_ascii=False)
    print(f"OK reliability: {len(providers)} providers with gravity (neutral others=1.0)")
    for k,v in providers.items(): print(f"  {k}: reliability={v['reliability']} events={v['scar_events']}")
if __name__=="__main__": sys.exit(main())
