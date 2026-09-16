#!/usr/bin/env python3
"""MET regional earthquake watch via api.data.gov.my. Keyless.
836 events w/ distance-from-Malaysia vectors. Filter: recent + significant.
Usage: quake.py   JSON out."""
import json, sys, urllib.request, datetime

HDR = {"User-Agent": "hermes-my-reality/1.0", "Accept": "application/json"}
URL = "https://api.data.gov.my/weather/warning/earthquake"
NOW = datetime.datetime.now(datetime.timezone.utc)

try:
    req = urllib.request.Request(URL, headers=HDR)
    with urllib.request.urlopen(req, timeout=25) as r:
        quakes = json.load(r)
    if not isinstance(quakes, list):
        print(json.dumps({"error": "structure-not-list"})); sys.exit(2)
except Exception as e:
    print(json.dumps({"error": str(e)[:120], "url": URL})); sys.exit(1)

def parse_dt(s):
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.datetime.strptime(str(s)[:19], fmt)
        except Exception:
            continue
    return None

recent = []
for q in quakes:
    dt = parse_dt(q.get("localdatetime") or q.get("utcdatetime") or "")
    if dt is None or (NOW - dt).days > 7:
        continue
    try:
        mag = float(q.get("magnitude") or 0)
    except (TypeError, ValueError):
        mag = 0.0
    if mag >= 4.5:
        recent.append((dt, mag, q))
recent.sort(key=lambda x: x[0], reverse=True)

events = [{"when_local": q.get("localdatetime"), "mag": m, "depth_km": q.get("depth"),
           "loc": q.get("location"), "dist_from_my": q.get("n_distancemas") or q.get("nbm_distancemas")}
          for _, m, q in recent[:5]]

out = {"source": "met-malaysia-earthquake", "window": "7d mag>=4.5", "total_events": len(quakes),
       "significant_recent": len(recent), "events": events}
print(json.dumps(out, ensure_ascii=False))
