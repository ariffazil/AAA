#!/usr/bin/env python3
"""Health check: probe all federation organs.

2026-08-15 upgrade:
- Full 10-surface coverage (was 4) — aligns `make health` with `now` + FRAME baseline.
- FED :4000 probed via /health/liveliness (no-auth); its /health is auth-gated.
- 401/403 on /health means the service is UP but auth-gated — never DOWN.
  (HTTP 000 / connection refused is the only DOWN signal.)
Exit code 0 only when every surface is up (auth-gated counts as up).
"""
import sys

import httpx

# (name, port, health_path)
ORGANS = [
    ('arifOS', 8088, '/health'),
    ('A-FORGE', 7071, '/health'),
    ('A-FORGE-MCP', 7072, '/health'),
    ('GEOX', 8081, '/health'),
    ('WEALTH', 18082, '/health'),
    ('WELL', 18083, '/health'),
    ('AAA', 3001, '/health'),
    ('arifFlow', 7073, '/health'),
    ('FED', 4000, '/health/liveliness'),
    ('FRAME', 18085, '/health'),
]

UP_CODES = {200, 301, 308}
GATED_CODES = {401, 403}

ok = 0
for name, port, path in ORGANS:
    try:
        r = httpx.get(
            f'http://127.0.0.1:{port}{path}',
            headers={'Host': f'{name.lower()}.arif-fazil.com'},
            timeout=5,
        )
        if r.status_code in UP_CODES or r.status_code == 400:
            # 400: domain-header listeners answer 400 when probed directly — still alive.
            print(f'  ✅ {name} (:{port}) — healthy')
            ok += 1
        elif r.status_code in GATED_CODES:
            print(f'  🟡 {name} (:{port}) — up (auth-gated, {r.status_code})')
            ok += 1
        else:
            print(f'  ⚠️  {name} (:{port}) — status {r.status_code}')
    except Exception as e:
        print(f'  ❌ {name} (:{port}) — unreachable: {e}')
print(f'  Result: {ok}/{len(ORGANS)} surfaces up')
sys.exit(0 if ok == len(ORGANS) else 1)
