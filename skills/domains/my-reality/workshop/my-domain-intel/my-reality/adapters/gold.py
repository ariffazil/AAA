#!/usr/bin/env python3
"""BNM Kijang Emas (Malaysian gold bullion coin) prices. Keyless official OpenAPI.
Usage: gold.py   JSON out with all denominations."""
import json, sys, urllib.request, datetime

DATE = datetime.date.today().strftime("%Y-%m-%d")
URL = f"https://api.bnm.gov.my/public/kijang-emas/?date={DATE}"
HDR = {"User-Agent": "hermes-my-reality/1.0", "Accept": "application/vnd.BNM.API.v1+json"}

try:
    req = urllib.request.Request(URL, headers=HDR)
    with urllib.request.urlopen(req, timeout=15) as r:
        payload = json.load(r)
except Exception as e:
    print(json.dumps({"error": str(e)[:120], "url": URL}))
    sys.exit(1)

try:
    data = payload["data"]
    out = {"source": "bnm-openapi", "effective_date": data.get("effective_date", DATE)}
    for den in ("one_oz", "half_oz", "quarter_oz"):
        d = data.get(den)
        if isinstance(d, dict):
            out[den] = {"buy": d.get("buying"), "sell": d.get("selling")}
    print(json.dumps(out, ensure_ascii=False))
except (KeyError, TypeError):
    print(json.dumps({"error": "structure-changed", "top_keys": list(payload.keys())[:8]}))
    sys.exit(2)
