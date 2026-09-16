#!/usr/bin/env python3
"""BNM base rates per bank. Keyless.
PITFALL: requires Accept: application/vnd.BNM.API.v1+json — plain application/json gets 404.
Usage: base_rate.py   JSON out."""
import json, sys, urllib.request

URL = "https://api.bnm.gov.my/public/base-rate/"
HDR = {"User-Agent": "hermes-my-reality/1.0", "Accept": "application/vnd.BNM.API.v1+json"}

try:
    req = urllib.request.Request(URL, headers=HDR)
    with urllib.request.urlopen(req, timeout=15) as r:
        payload = json.load(r)
except Exception as e:
    print(json.dumps({"error": str(e)[:120], "hint": "check Accept header"})); sys.exit(1)

try:
    data = payload["data"]
    rows = data if isinstance(data, list) else data.get("rates", [])
    banks = [{"bank": b.get("bank_name", "?"), "base_rate": b.get("base_rate"),
              "base_lending": b.get("base_lending_rate"), "effective": b.get("effective_date")}
             for b in rows[:6]]
    out = {"source": "bnm-openapi", "banks_total": len(rows), "sample": banks}
    print(json.dumps(out, ensure_ascii=False))
except (KeyError, TypeError):
    print(json.dumps({"error": "structure-changed", "top_keys": list(payload.keys())[:8]})); sys.exit(2)
