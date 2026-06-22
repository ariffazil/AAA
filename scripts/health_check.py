#!/usr/bin/env python3
"""Health check: probe all federation organs."""
import sys

import httpx

ORGANS = {'arifOS': 8088, 'GEOX': 8081, 'WEALTH': 18082, 'WELL': 18083}
ok = 0
for name, port in ORGANS.items():
    try:
        r = httpx.get(f'http://localhost:{port}/health', timeout=5)
        if r.status_code == 200:
            print(f'  ✅ {name} (:{port}) — healthy')
            ok += 1
        else:
            print(f'  ⚠️  {name} (:{port}) — status {r.status_code}')
    except Exception as e:
        print(f'  ❌ {name} (:{port}) — unreachable: {e}')
print(f'  Result: {ok}/{len(ORGANS)} organs healthy')
sys.exit(0 if ok == len(ORGANS) else 1)
