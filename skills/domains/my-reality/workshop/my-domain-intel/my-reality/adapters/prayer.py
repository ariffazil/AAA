#!/usr/bin/env python3
"""JAKIM prayer times via AlAdhan (method=17). Keyless. Default: Penang.
Usage: prayer.py [lat lon]  → JSON one-liner. Exit 2 = parse/structure fail."""
import json, sys, urllib.request, datetime

LAT = sys.argv[1] if len(sys.argv) > 1 else "5.4141"
LON = sys.argv[2] if len(sys.argv) > 2 else "100.3288"
DATE = datetime.date.today().strftime("%d-%m-%Y")
URL = f"https://api.aladhan.com/v1/timings/{DATE}?latitude={LAT}&longitude={LON}&method=17"

try:
    req = urllib.request.Request(URL, headers={"User-Agent": "hermes-my-reality/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        payload = json.load(r)
except Exception as e:
    print(json.dumps({"error": str(e)[:120], "url": URL}))
    sys.exit(1)

try:
    t = payload["data"]["timings"]
    out = {
        "source": "aladhan-method17-jakim",
        "date": DATE, "lat": LAT, "lon": LON,
        "imsak": t["Imsak"], "fajr": t["Fajr"], "syuruk": t["Sunrise"],
        "dhuhr": t["Dhuhr"], "asr": t["Asr"], "maghrib": t["Maghrib"], "isha": t["Isha"],
    }
    print(json.dumps(out, ensure_ascii=False))
except (KeyError, TypeError):
    print(json.dumps({"error": "structure-changed", "top_keys": list(payload.get("data", {}).keys())[:8] if isinstance(payload, dict) else str(type(payload))}))
    sys.exit(2)
