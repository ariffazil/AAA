#!/usr/bin/env python3
"""MET Malaysia weather: forecast + active warnings. Keyless via api.data.gov.my.
Endpoint returns ALL locations x 7 days; we filter client-side by location_name + date.
Usage: weather.py [location]   default: Pulau Pinang. JSON out."""
import json, sys, urllib.parse, urllib.request, datetime

WANT = sys.argv[1] if len(sys.argv) > 1 else "Pulau Pinang"
TODAY = datetime.date.today().isoformat()
TOMORROW = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
HDR = {"User-Agent": "hermes-my-reality/1.0", "Accept": "application/json"}

def get(url):
    req = urllib.request.Request(url, headers=HDR)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)

try:
    raw = get("https://api.data.gov.my/weather/forecast")
    if not isinstance(raw, list):
        print(json.dumps({"error": "structure-not-list"})); sys.exit(2)
except Exception as e:
    print(json.dumps({"error": str(e)[:120]})); sys.exit(1)

# client-side filter: rows for a location (contains match, case-insensitive), today/tomorrow
rows = [r for r in raw
        if WANT.lower() in str(r.get("location", {}).get("location_name", "")).lower()
        and r.get("date") in (TODAY, TOMORROW)]
if not rows:
    # fallback: exact district rows absent -> take georgetown-like defaults
    rows = [r for r in raw if r.get("location", {}).get("location_name", "").lower() == WANT.lower()
            and r.get("date") == TOMORROW]
if not rows:
    print(json.dumps({"error": f"no-rows-for:{WANT}", "total_rows": len(raw)})); sys.exit(1)

forecast = [{"loc": r.get("location", {}).get("location_name"), "date": r.get("date"),
             "summary": r.get("summary_forecast"), "when": r.get("summary_when"),
             "min_c": r.get("min_temp"), "max_c": r.get("max_temp")} for r in rows[:4]]

try:
    warn = get("https://api.data.gov.my/weather/warning")
    if not isinstance(warn, list):
        warn = warn.get("results", warn)
    warnings = [{"title": w.get("title", w.get("warning", "")),
                 "issued": w.get("issue_datetime", w.get("issued", "")),
                 "valid_to": w.get("valid_to", "")} for w in warn]
except Exception as e:
    warnings = [{"error": f"warning-endpoint: {str(e)[:80]}"}]

out = {"source": "met-malaysia-via-data.gov.my", "want": WANT, "rows_matched": len(rows),
       "forecast": forecast, "warning_count": len(warnings), "warnings": warnings[:5]}
print(json.dumps(out, ensure_ascii=False))
