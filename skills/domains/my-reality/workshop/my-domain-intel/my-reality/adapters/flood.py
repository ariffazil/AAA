#!/usr/bin/env python3
"""JPS/DID flood station watch. 15-min cadence via api.data.gov.my. Keyless.
NOTE: state values are UPPERCASE; alert = water_level_indicator in ALERT/WARNING/DANGER
(null indicator + rain gauge ON is NOT an alert).
Usage: flood.py [state ...]   default: Pulau Pinang Selangor. JSON out."""
import json, sys, urllib.request

WANT = [s.upper() for s in (sys.argv[1:] or ["Pulau Pinang", "Selangor"])]
HDR = {"User-Agent": "hermes-my-reality/1.0", "Accept": "application/json"}
URL = "https://api.data.gov.my/flood-warning"
ALERT_STATES = {"ALERT", "WARNING", "DANGER"}

try:
    req = urllib.request.Request(URL, headers=HDR)
    with urllib.request.urlopen(req, timeout=25) as r:
        stations = json.load(r)
    if not isinstance(stations, list):
        print(json.dumps({"error": "structure-not-list"})); sys.exit(2)
except Exception as e:
    print(json.dumps({"error": str(e)[:120], "url": URL})); sys.exit(1)

sel = [s for s in stations if str(s.get("state", "")).upper() in WANT]
alert = [s for s in sel if str(s.get("water_level_indicator") or "").upper() in ALERT_STATES]
compact = [{"station": s.get("station_name", s.get("station_id")), "district": s.get("district"),
            "state": s.get("state"),
            "indicator": s.get("water_level_indicator"),
            "trend": s.get("water_level_trend"),
            "level_m": s.get("water_level_current"),
            "updated": s.get("water_level_update_datetime", s.get("rainfall_update_datetime"))}
           for s in alert[:12]]

out = {"source": "jps-did-via-data.gov.my", "states": WANT, "stations_seen": len(sel),
       "total_national": len(stations), "alert_count": len(alert), "alerts": compact}
print(json.dumps(out, ensure_ascii=False))
