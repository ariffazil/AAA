#!/usr/bin/env python3
"""Health check: probe federation organs and report TWO axes.

2026-10-27 (333-AGI): a 200 is a response, not a state. The old version printed
"healthy" for every HTTP 200 and hid arifOS HOLD, GEOX HOLD, AAA deployment
drift and WELL REFLECT_ONLY behind a green tick. Measured the same minute:
11/11 "surfaces up" while `now --json` read arifOS/GEOX/WELL DEGRADED.

Output now separates:
  reachable  — an HTTP response arrived (200, auth-gated 401/403, or a body)
  state      — OPERATIONAL / DEGRADED / UNKNOWN, read from the response BODY

- 401/403 on /health means the service is UP but auth-gated — never DOWN.
  (HTTP 000 / connection refused is the only DOWN signal.)
- A non-JSON body is reachable but UNKNOWN, never silently healthy.
- Exit 0 when every surface is reachable (backward compatible with `make prove`).
  --strict exits 0 only when every surface is OPERATIONAL.
"""
import json
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
    ('CHRON', 18102, '/health'),
]

UP_CODES = {200, 301, 308}
GATED_CODES = {401, 403}

OK_WORDS = {'ok', 'okay', 'healthy', 'up', 'pass', 'passing', 'flowing',
            'sealed', 'active', 'ok-v3-vector'}
WARN_WORDS = {'degraded', 'hold', 'warn', 'warning', 'partial', 'unmeasured',
              'held', 'reflect_only', 'dirty'}
FAIL_WORDS = {'down', 'failed', 'failure', 'error', 'void', 'unreachable'}


def _word(value) -> str:
    return str(value or '').strip().lower().replace(' ', '_')


def state_from_body(body) -> tuple[str, list[str]]:
    """Return (OPERATIONAL|DEGRADED|UNKNOWN, notes) from a health body.

    Reads the organ's own words. Nested governance fields are included because
    the outer `status` can say `healthy` while execution is held.
    """
    if isinstance(body, str):
        text = body.strip()
        if text.lower().startswith("i'm alive") or text.lower() == 'ok':
            return 'OPERATIONAL', [f'liveness text: {text[:60]}']
        return 'UNKNOWN', ['JSON body is a string, not an object']
    if not isinstance(body, dict):
        return 'UNKNOWN', ['body is not a JSON object']

    notes: list[str] = []
    words: list[str] = []

    for key in ('status', 'state', 'verdict', 'health'):
        w = _word(body.get(key))
        if w:
            words.append(w)

    thermo = body.get('thermodynamic')
    if isinstance(thermo, dict) and _word(thermo.get('verdict')):
        words.append(_word(thermo.get('verdict')))
        notes.append(f"thermodynamic.verdict={_word(thermo.get('verdict'))}")

    if 'ok' in body and isinstance(body.get('ok'), bool):
        words.append('ok' if body['ok'] else 'failed')

    for key in ('execution_readiness', 'readiness'):
        w = _word(body.get(key))
        if w:
            words.append(w)
            notes.append(f'{key}={w}')

    if body.get('floor_passed') is False:
        notes.append('floor_passed=false')
        words.append('hold')

    if body.get('deployment_drift') is True:
        notes.append('deployment_drift=true')
        words.append('degraded')

    if isinstance(body.get('working_tree'), str) and _word(body['working_tree']) == 'dirty':
        notes.append('working_tree=DIRTY')

    if _word(body.get('authority')) == 'reflect_only':
        notes.append('authority=REFLECT_ONLY')

    if not words:
        return 'UNKNOWN', notes or ['no status field in body']

    if any(w in WARN_WORDS for w in words):
        return 'DEGRADED', notes
    if any(w in FAIL_WORDS for w in words):
        return 'DEGRADED', notes
    if any(w in OK_WORDS for w in words):
        return 'OPERATIONAL', notes
    return 'UNKNOWN', notes + [f"unrecognized status={words[0]}"]


def _fed_router_note() -> str:
    """Functional state of the FED router (:7074), separate from :4000 liveliness."""
    try:
        r = httpx.get('http://127.0.0.1:7074/health', timeout=3)
        body = r.json()
    except Exception:
        return ''
    bl12 = body.get('bl12') if isinstance(body.get('bl12'), dict) else {}
    state = bl12.get('state') or body.get('state') or 'UNKNOWN'
    keys = bl12.get('routing_keys_known')
    if keys is None:
        return f'router={state}'
    return f'router={state} keys={keys}'


def main() -> int:
    strict = '--strict' in sys.argv
    as_json = '--json' in sys.argv
    rows = []
    reachable = 0
    operational = 0

    for name, port, path in ORGANS:
        row = {'name': name, 'port': port, 'path': path,
               'reachable': False, 'http': None, 'state': 'UNKNOWN', 'notes': []}
        try:
            r = httpx.get(
                f'http://127.0.0.1:{port}{path}',
                headers={'Host': f'{name.lower()}.arif-fazil.com'},
                timeout=5,
            )
            row['http'] = r.status_code
            if r.status_code in GATED_CODES:
                row['reachable'] = True
                row['state'] = 'AUTH_GATED'
                row['notes'].append(f'auth-gated {r.status_code}')
            elif r.status_code in UP_CODES or r.status_code == 400:
                # 400: domain-header listeners answer 400 when probed directly — still alive.
                row['reachable'] = True
                body = None
                notes = []
                try:
                    body = r.json()
                except Exception:
                    try:
                        text = r.text.strip()
                    except Exception:
                        text = ''
                    if text and len(text) < 200:
                        row['notes'].append(f'text body: {text[:80]}')
                        if text.lower().startswith("i'm alive") or text.lower().startswith('ok'):
                            row['state'] = 'OPERATIONAL'
                            row['notes'].append('liveness text only')
                    else:
                        row['notes'].append('non-JSON body')
                if body is not None:
                    row['state'], notes = state_from_body(body)
                row['notes'].extend(notes)
            else:
                row['notes'].append(f'http {r.status_code}')
        except Exception as exc:
            row['notes'].append(f'{type(exc).__name__}: {exc}')

        if row['reachable']:
            reachable += 1
        if row['state'] == 'OPERATIONAL':
            operational += 1
        if name == 'FED':
            note = _fed_router_note()
            if note:
                row['notes'].append(note)
        rows.append(row)

    if as_json:
        print(json.dumps({
            'surfaces': rows,
            'reachable': reachable,
            'operational': operational,
            'total': len(ORGANS),
            'strict_ok': operational == len(ORGANS),
        }, indent=2))
    else:
        icon = {'OPERATIONAL': '✅', 'AUTH_GATED': '🟡', 'DEGRADED': '⚠️ ', 'UNKNOWN': '❔'}
        for row in rows:
            mark = icon.get(row['state'], '❔')
            notes = f" ({'; '.join(row['notes'])})" if row['notes'] else ''
            print(f"  {mark} {row['name']} (:{row['port']}) — {row['state']}{notes}")
        print(f"  Result: {reachable}/{len(ORGANS)} reachable · "
              f"{operational}/{len(ORGANS)} operational")

    return 0 if (operational == len(ORGANS) if strict else reachable == len(ORGANS)) else 1


if __name__ == '__main__':
    sys.exit(main())
