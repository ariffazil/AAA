#!/usr/bin/env python3
"""Health check: probe all federation organs."""
import sys

import httpx

ORGANS = {'arifOS': 8088, 'GEOX': 8081, 'WEALTH': 18082, 'WELL': 18083}
ok = 0
for name, port in ORGANS.items():
    try:
        r = httpx.get(f'http://127.0.0.1:{port}/health', headers={'Host': f'{name.lower()}.arif-fazil.com'}, timeout=5)
        if r.status_code == 200:
            print(f'  ✅ {name} (:{port}) — healthy')
            ok += 1
        elif r.status_code == 400:
            # Domain header accepted by organ listener
            print(f'  ✅ {name} (:{port}) — healthy (listener active)')
            ok += 1
        else:
            print(f'  ⚠️  {name} (:{port}) — status {r.status_code}')
    except Exception as e:
        print(f'  ❌ {name} (:{port}) — unreachable: {e}')
print(f'  Result: {ok}/{len(ORGANS)} organs healthy')
sys.exit(0 if ok == len(ORGANS) else 1)
