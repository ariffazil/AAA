#!/usr/bin/env python3
"""BNM OPR (Overnight Policy Rate). Keyless.
PITFALL 1: requires Accept: application/vnd.BNM.API.v1+json — plain application/json gets 404.
PITFALL 2 (scar #4): /public/opr/ can LAG MPC announcements (observed 2026-08-15: API returned
2026-05-07 while latest MPC decision was 2026-07-09). Level was right, date was stale.
→ Adapter exposes data date + staleness flag. Never present API date as 'latest decision'.
Usage: opr.py   JSON out."""
import json, sys, urllib.request, datetime

URL = "https://api.bnm.gov.my/public/opr/"
HDR = {"User-Agent": "hermes-my-reality/1.0", "Accept": "application/vnd.BNM.API.v1+json"}

try:
    req = urllib.request.Request(URL, headers=HDR)
    with urllib.request.urlopen(req, timeout=15) as r:
        payload = json.load(r)
except Exception as e:
    print(json.dumps({"error": str(e)[:120], "hint": "check Accept header"})); sys.exit(1)

try:
    latest = payload["data"]
    if isinstance(latest, list):
        latest = latest[0]
    date_str = str(latest.get("date", ""))
    try:
        d = datetime.date.fromisoformat(date_str)
        age_days = (datetime.date.today() - d).days
    except ValueError:
        age_days = None
    out = {"source": "bnm-openapi", "opr_level": latest.get("new_opr_level"),
           "date": date_str, "change": latest.get("change_in_opr"),
           "age_days": age_days,
           "stale_warning": (age_days is not None and age_days > 75),
           "note": "API may lag latest MPC announcement — treat date as 'as published', not 'latest decision'"}
    print(json.dumps(out, ensure_ascii=False))
except (KeyError, TypeError, IndexError):
    print(json.dumps({"error": "structure-changed", "top_keys": list(payload.keys())[:8]})); sys.exit(2)
