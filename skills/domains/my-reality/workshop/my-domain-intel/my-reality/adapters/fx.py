#!/usr/bin/env python3
"""BNM exchange rates. Keyless official OpenAPI. Usage: fx.py [CUR]  default USD. JSON out."""
import json, sys, urllib.request, datetime

CUR = (sys.argv[1] if len(sys.argv) > 1 else "USD").upper()
DATE = datetime.date.today().strftime("%Y-%m-%d")
URL = f"https://api.bnm.gov.my/public/exchange-rate/{CUR}?date={DATE}"
HDR = {"User-Agent": "hermes-my-reality/1.0", "Accept": "application/vnd.BNM.API.v1+json"}

try:
    req = urllib.request.Request(URL, headers=HDR)
    with urllib.request.urlopen(req, timeout=15) as r:
        payload = json.load(r)
except Exception as e:
    print(json.dumps({"error": str(e)[:120], "url": URL})); sys.exit(1)

try:
    data = payload["data"]
    rate = data["rate"]
    out = {"source": "bnm-openapi", "currency": CUR, "date": rate.get("date", DATE),
           "buy": rate.get("buying_rate"), "sell": rate.get("selling_rate"),
           "middle": rate.get("middle_rate"), "unit": data.get("unit")}
    print(json.dumps(out, ensure_ascii=False))
except (KeyError, TypeError):
    print(json.dumps({"error": "structure-changed", "top_keys": list(payload.keys())[:8]})); sys.exit(2)
